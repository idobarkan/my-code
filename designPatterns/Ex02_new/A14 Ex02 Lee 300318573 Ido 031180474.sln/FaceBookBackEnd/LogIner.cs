
namespace FaceBookBackEnd
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using FacebookWrapper.ObjectModel;
    using FacebookWrapper;
    using System.IO;


    internal class LogIner
    {
        private User m_LoggedInUser = null;
        private readonly string APP_ID = "556910297710526";
        private string m_AccessToken;

        public User LogIn()
        {
            if (m_LoggedInUser == null)
            {
                LoginResult loginResult;
                string accessTokenFromDisk = tryGetAccessTokenFromDisk();
                if (accessTokenFromDisk != null &&
                    !string.IsNullOrEmpty(accessTokenFromDisk.ToString()))
                {
                    loginResult = FacebookService.Connect(accessTokenFromDisk);
                }
                else // nothing saved in disk
                {
                    loginResult = tryLogInWithAppID();
                }

                checkLogInResult(loginResult);
                m_AccessToken = loginResult.AccessToken;
                m_LoggedInUser = loginResult.LoggedInUser;
                saveAccessTokenToDisk();
            }
            return m_LoggedInUser;
        }

            private void checkLogInResult(LoginResult loginResult)
        {
            if (!string.IsNullOrEmpty(loginResult.ErrorMessage))
            {
                throw new Exception(loginResult.ErrorMessage);
            }
        }

        private LoginResult tryLogInWithAppID()
        {
            LoginResult loginResult;
            loginResult = FacebookService.Login(APP_ID,
            "user_activities", "friends_activities",
            "user_checkins", "friends_checkins",
            "user_events", "friends_events",
            "user_groups" , "friends_groups",
            "user_likes", "friends_likes",
            "user_location", "friends_location",
            "user_notes", "friends_notes",
            "user_photo_video_tags", "friends_photo_video_tags",
            "user_photos", "friends_photos",
            "user_photos", "friends_photos",
            "user_status", "friends_status",
            "user_videos", "friends_videos");
            
            return loginResult;
        }

        private string tryGetAccessTokenFromDisk()
        {
            StringBuilder sb = new StringBuilder();
            try
            {
                using (StreamReader sr = new StreamReader(getAccessTokenFilePath()))
                {
                    sb.Append(sr.ReadToEnd());
                }
            }
            catch (FileNotFoundException)
            {
                return null;
            }
            return sb.ToString();
        }

        private void saveAccessTokenToDisk()
        {
            string filePath = getAccessTokenFilePath();
            using (StreamWriter outfile = new StreamWriter(filePath))
            {
                outfile.Write(m_AccessToken);
            }
        }

        private string getAccessTokenFilePath()
        {
            string filePath = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
                "userinfo.txt");
            return filePath;
        }
    }
}
