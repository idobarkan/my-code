using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Net;
using System.Text;
using System.IO;
using System.Data;
using Microsoft.WindowsAzure;
using Microsoft.WindowsAzure.ServiceRuntime;
using Microsoft.WindowsAzure.StorageClient;


namespace WebRole1
{
    public partial class _Default : Page
    {
        private static bool storageInitialized = false;
        private static object gate = new Object();
        private static CloudBlobClient blobStorage;
        private static CloudQueueClient queueStorage;
        private const string BLOB_CONTAINER_NAME = "filescontainer";
        private const string Q_NAME = "tasksq";
        private const string CONNECTION_STRING_AZURE_CONF = "DataConnectionStringAzure";

        protected void Page_Load(object sender, EventArgs e)
        {
            InitializeStorage();
            var dataTable = new DataTable();
            dataTable.Columns.Add("result");
            foreach (var s in ExecutableOutputs())
            {
                var dataRow = dataTable.NewRow();
                dataRow["result"] = s;
                dataTable.Rows.Add(dataRow);
            }

            ResultsRepeater.DataSource = dataTable;
            ResultsRepeater.DataBind();
        }

        protected void DataUploadButton_Click(object sender, EventArgs e)
        {
            try
            {
                if (!DataFileUploadControl.HasFile)
                    throw new Exception("missing data file");
                if (!ExecFileUploadControl.HasFile)
                    throw new Exception("missing execution file");

                InitializeStorage();
                
                //upload bothe files to storage
                var guid = Guid.NewGuid().ToString();
                UploadBlob(DataFileUploadControl.PostedFile, "data", guid);
                UploadBlob(ExecFileUploadControl.PostedFile, "exec", guid);

                // queue a message to process the file
                var queue = queueStorage.GetQueueReference(Q_NAME);
                var message = new CloudQueueMessage(String.Format("{0}", guid));
                queue.AddMessage(message);
                System.Diagnostics.Trace.TraceInformation("Queued message to process blob '{0}'", guid);
                Label1.Text = "upload OK";
            }
            catch (Exception uploadException)
            {
                //show error to the user
                Label1.Text = uploadException.Message;
                System.Diagnostics.Trace.TraceInformation("got exception while uploading files '{0}'", uploadException.Message);
            }
            
        }

        private void UploadBlob(HttpPostedFile postedFile, string type, string guid)
        {
            CloudBlobContainer container = blobStorage.GetContainerReference(BLOB_CONTAINER_NAME);
            string uniqueBlobName = string.Format("{0}{1}", type, guid);
            CloudBlockBlob blob = container.GetBlockBlobReference(uniqueBlobName);
            blob.Properties.ContentType = postedFile.ContentType;
            blob.UploadFromStream(postedFile.InputStream);
            System.Diagnostics.Trace.TraceInformation("Uploaded {0} '{0}' to blob storage as '{1}'", type, postedFile.FileName, uniqueBlobName);
        }

        protected List<string> ExecutableOutputs()
        {
            var result = new List<string>();

            CloudBlobContainer container = blobStorage.GetContainerReference(BLOB_CONTAINER_NAME);
            var blobsList = container.ListBlobs();
            foreach (IListBlobItem blobItem in blobsList)
            {
                var lastPArt = blobItem.Uri.OriginalString.Split('/').Last();
                if (lastPArt.LastIndexOf("result") != -1)
                {
                    CloudBlockBlob fileBlob = container.GetBlockBlobReference(blobItem.Uri.ToString());
                    MemoryStream fileMemoryStream = new MemoryStream();
                    fileBlob.DownloadToStream(fileMemoryStream);
                    fileMemoryStream.Seek(0, SeekOrigin.Begin);
                    result.Add(Encoding.Default.GetString(fileMemoryStream.GetBuffer()));
                }
                    
            }
            return result;
        }

        private void InitializeStorage()
        {
            if (storageInitialized)
                return;

            lock (gate)
            {
                if (storageInitialized)
                    return;

                CloudStorageAccount.SetConfigurationSettingPublisher(configurationSettingPublisher);

                try
                {
                    // Create a new instance of a CloudStorageAccount object from a specified configuration setting. 
                    // This method may be called only after the SetConfigurationSettingPublisher 
                    // method has been called to configure the global configuration setting publisher.
                    // You can call the SetConfigurationSettingPublisher method in the OnStart method.
                    var storageAccount = CloudStorageAccount.FromConfigurationSetting(CONNECTION_STRING_AZURE_CONF);

                    // create blob container for files
                    blobStorage = storageAccount.CreateCloudBlobClient();
                    CloudBlobContainer container = blobStorage.GetContainerReference(BLOB_CONTAINER_NAME);
                    container.CreateIfNotExist();

                    // configure container for public access
                    var permissions = container.GetPermissions();
                    permissions.PublicAccess = BlobContainerPublicAccessType.Container;
                    container.SetPermissions(permissions);

                    // create queue to communicate with worker role
                    queueStorage = storageAccount.CreateCloudQueueClient();
                    CloudQueue queue = queueStorage.GetQueueReference(Q_NAME);
                    queue.CreateIfNotExist();
                }
                catch (WebException)
                {

                    StringBuilder buffer = new StringBuilder();
                    buffer.Append("Storage services initialization failure.");
                    buffer.Append(" Check your storage account configuration settings.");
                    buffer.Append(" If running locally,");
                    buffer.Append(" ensure that the Development Storage service is running.");

                    throw new WebException(buffer.ToString());

                }

                storageInitialized = true;
            }
        }

        private void configurationSettingPublisher(string s, Func<string, bool> func)
        {
            func(RoleEnvironment.GetConfigurationSettingValue(s));
        }
           
    }
}