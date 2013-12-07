using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using Microsoft.WindowsAzure.Diagnostics;
using Microsoft.WindowsAzure.ServiceRuntime;
using System.Drawing;
using System.IO;
using System.Diagnostics;
using Microsoft.WindowsAzure;
using Microsoft.WindowsAzure.StorageClient;

namespace WorkerRole1
{
    public class WorkerRole : RoleEntryPoint
    {
        private CloudQueue queue;
        private CloudBlobContainer container;
        private const string BLOB_CONTAINER_NAME = "filescontainer";
        private const string Q_NAME = "tasksq";
        private const string CONNECTION_STRING_AZURE_CONF = "DataConnectionStringAzure";
        
        public override void Run()
        {
            Trace.TraceInformation("Listening for queue messages...");
            bool qIsAlive = false;

            while (true)
            {
                try
                {
                    // retrieve a new message from the queue
                    CloudQueueMessage msg = queue.GetMessage();
                    if (msg != null)
                    {
                        qIsAlive = true;
                        // parse message retrieved from queue
                        var guid = msg.AsString;
                        Trace.TraceInformation("Processing files with guid '{0}'.", guid);

                        // download original image from blob storage
                        var dataMemoryStream = DownloadBlob("data", guid);
                        var exceMemoryStream = DownloadBlob("exec", guid);
                        
                        // process the data with the executable
                        var result = ProcessData(dataMemoryStream, exceMemoryStream);
                        UploadProcessResult(result[0], result[1], guid);

                        // remove message from queue
                        queue.DeleteMessage(msg);

                        Trace.TraceInformation("Finished processing '{0}'.", guid);
                    }
                    else
                    {
                        qIsAlive = false;
                    }
                    System.Threading.Thread.Sleep(qIsAlive ? 1000 : 5000);
                }
                catch (StorageClientException e)
                {
                    Trace.TraceError("Exception when processing queue item. Message: '{0}'", e.Message);
                    System.Threading.Thread.Sleep(5000);
                }
            }
        }

        private string[] ProcessData(MemoryStream dataMemoryStream, MemoryStream exceMemoryStream)
        {
            string localDataPath = saveFileLocally("data", dataMemoryStream);
            string localexecutablePath = saveFileLocally("exec", exceMemoryStream);
            string output = "";
            string error = "";

            int timeoutMilliSeconds = 30 * 1000;

            Process myProcess = new Process();
            var startInfo = new ProcessStartInfo();
            startInfo.Arguments = localDataPath;
            startInfo.FileName = localexecutablePath;
            startInfo.UseShellExecute = false;
            startInfo.RedirectStandardOutput = true;
            startInfo.RedirectStandardError = true;

            try
            {
                using (Process exeProcess = Process.Start(startInfo))
                {
                    exeProcess.WaitForExit(timeoutMilliSeconds);
                    if (exeProcess.ExitCode == 0)
                        output = exeProcess.StandardOutput.ReadToEnd();   
                    else
                        error = exeProcess.StandardOutput.ReadToEnd();
                }
            }
            catch (Exception processLaunchFailed)
            {
                Trace.TraceError("Exception while running process.error: {0}", processLaunchFailed.Message);
            }

            return new string[] { output, error };
        }

        private string saveFileLocally(string filename, MemoryStream dataStream)
        {
            string tmpPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            string filePath = string.Format(@"{0}\{1}", tmpPath, filename);
            
            if (File.Exists(filePath))
                File.Delete(filePath);

            FileStream fStream = new FileStream(filePath, FileMode.CreateNew);
            BinaryWriter bWriter = new BinaryWriter(fStream);
            bWriter.Write(dataStream.GetBuffer());
            bWriter.Close();
            fStream.Close();
            return filePath;
        }

        private MemoryStream DownloadBlob(string type, string guid)
        {
            CloudBlockBlob fileBlob = container.GetBlockBlobReference(string.Format("{0}{1}", type, guid));
            MemoryStream fileMemoryStream = new MemoryStream();
            fileBlob.DownloadToStream(fileMemoryStream);
            fileMemoryStream.Seek(0, SeekOrigin.Begin);
            return fileMemoryStream;
        }

        private void UploadProcessResult(string output, string error, string guid)
        {
            string uniqueBlobName = string.Format("{0}{1}", "result", guid);
            CloudBlockBlob blob = container.GetBlockBlobReference(uniqueBlobName);
            blob.Properties.ContentType = "text";
            blob.UploadText(string.Format("{0}%{1}", output, error));
            System.Diagnostics.Trace.TraceInformation("Uploaded result to blob storage as '{0}'", uniqueBlobName);
        }

        public override bool OnStart()
        {
            DiagnosticMonitor.Start("DiagnosticsConnectionString");

            // Restart the role upon all configuration changes
            RoleEnvironment.Changing += RoleEnvironmentChanging;

            // Set the global configuration setting publisher for the storage account, which 
            // will be called when the account access keys are updated in the service configuration file.
            // Calling SetConfigurationSettingPublisher in OnStart method is important otherwise the
            // system raises an exception when FromConfigurationSetting is called.
            CloudStorageAccount.SetConfigurationSettingPublisher((configName, configSetter) =>
            {
                try
                {
                    configSetter(RoleEnvironment.GetConfigurationSettingValue(configName));
                }
                catch (RoleEnvironmentException e)
                {

                    Trace.TraceError(e.Message);
                    System.Threading.Thread.Sleep(5000);
                }
            });

            // Create a new instance of a CloudStorageAccount object from a specified configuration setting. 
            // This method may be called only after the SetConfigurationSettingPublisher 
            // method has been called to configure the global configuration setting publisher.
            // You can call the SetConfigurationSettingPublisher method in the OnStart method
            // of the worker role before calling FromConfigurationSetting.
            // If you do not do this, the system raises an exception. 
            var storageAccount = CloudStorageAccount.FromConfigurationSetting(CONNECTION_STRING_AZURE_CONF);

            // initialize blob storage
            CloudBlobClient blobStorage = storageAccount.CreateCloudBlobClient();
            container = blobStorage.GetContainerReference(BLOB_CONTAINER_NAME);

            // initialize queue storage 
            CloudQueueClient queueStorage = storageAccount.CreateCloudQueueClient();
            queue = queueStorage.GetQueueReference(Q_NAME);

            Trace.TraceInformation("Creating container and queue...");

            bool storageInitialized = false;
            while (!storageInitialized)
            {
                try
                {
                    // create the blob container and allow public access
                    container.CreateIfNotExist();
                    var permissions = container.GetPermissions();
                    permissions.PublicAccess = BlobContainerPublicAccessType.Container;
                    container.SetPermissions(permissions);

                    // create the message queue
                    queue.CreateIfNotExist();
                    storageInitialized = true;
                }
                catch (StorageClientException e)
                {
                    if (e.ErrorCode == StorageErrorCode.TransportError)
                    {
                        Trace.TraceError("Storage services initialization failure. "
                          + "Check your storage account configuration settings. If running locally, "
                          + "ensure that the Development Storage service is running. Message: '{0}'", e.Message);
                        System.Threading.Thread.Sleep(5000);
                    }
                    else
                    {
                        throw;
                    }
                }
            }

            return base.OnStart();
        }

        private void RoleEnvironmentChanging(object sender, RoleEnvironmentChangingEventArgs e)
        {
            if (e.Changes.Any(change => change is RoleEnvironmentConfigurationSettingChange))
                e.Cancel = true;
        }
    }
}

