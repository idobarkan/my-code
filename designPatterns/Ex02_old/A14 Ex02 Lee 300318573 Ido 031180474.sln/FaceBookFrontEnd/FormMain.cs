using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using FacebookWrapper.ObjectModel;
using FacebookWrapper;
using FaceBookBackEnd;
using FindTagsAround;
using FaceBookFrontEnd;
//using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace BasicFacebookFeatures.WithSingltonAppSettings
{
    public partial class FacebookForm : Form
    {
        public FacebookForm()
        {
            InitializeComponent();
        }
        User m_LoggedInUser;

        private void loginAndInit()
        {
            /// App: Demo
            /// Owner: design.patterns
            /// User: design.patterns
            /// 
            /// use this AccessToken to connect to design.patterns user via :
            /// LoginResult result = FacebookService.Connect("CAATyiqZBEpU0BAK6GldJGFK36ZAw1ZCORZBUb6fpZAkQjz7UsPDupRJaZB3xG0ptGGLZAHhV4cPu26eUa6KU1jWVr5HCkGDaDdPS0hYqjKU5MbJUohI4vvZBhZC5st3BqmllQuZBUfgGWXaKUZBZBMIx86nSAZAwOGRro2e8VvPUU9dP3UgZDZD");

            /// Use the FacebookService.Login method to display the login form to any user who wish to use this application.
            /// You can then save the result.AccessToken for future auto-connect to this user:
            // These are NOT the complete list of permissions.
            // The documentation regarding permissions can be found here: https://developers.facebook.com/docs/reference/login/
            //"user_activities", "friends_activities",
            //"user_birthday", "friends_birthday",
            //"user_checkins", "friends_checkins",
            //"user_education_history", "friends_education_history",
            //"user_events", "friends_events",
            //"user_groups" , "friends_groups",
            //"user_hometown", "friends_hometown",
            //"user_interests", "friends_interests",
            //"user_likes", "friends_likes",
            //"user_location", "friends_location",
            //"user_notes", "friends_notes",
            //"user_online_presence", "friends_online_presence",
            //"user_photo_video_tags", "friends_photo_video_tags",
            //"user_photos", "friends_photos",
            //"user_photos", "friends_photos",
            //"user_relationships", "friends_relationships",
            //"user_relationship_details","friends_relationship_details",
            //"user_religion_politics","friends_religion_politics",
            //"user_status", "friends_status",
            //"user_videos", "friends_videos",
            //"user_website", "friends_website",
            //"user_work_history", "friends_work_history",
            //"email",
            //"read_friendlists",
            //"read_insights",
            //"read_mailbox",
            //"read_requests",
            //"read_stream",
            //"xmpp_login",

            //"create_event",
            //"rsvp_event",
            //"sms",
            //"publish_checkins",
            //"manage_friendlists",
            //"manage_pages",

            //"offline_access"


        }

        private void fetchUserInfo()
        {
            picture_smallPictureBox.LoadAsync(m_LoggedInUser.PictureNormalURL);
            if (m_LoggedInUser.Statuses.Count > 0)
            {
                textBoxStatus.Text = m_LoggedInUser.Statuses[0].Message;
            }
        }

        private void buttonLogin_Click(object sender, EventArgs e)
        {
            FacebookBackend fb = new FacebookBackend();
            m_LoggedInUser = fb.LogIn();
            if (m_LoggedInUser != null)
            {
                fetchUserInfo();
            }
        }

        private void buttonSetStatus_Click(object sender, EventArgs e)
        {
            m_LoggedInUser.PostStatus(textBoxStatus.Text);
        }

        private void linkNewsFeed_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            fetchNewsFeed();
        }

        private void fetchNewsFeed()
        {
            foreach (Post post in m_LoggedInUser.NewsFeed)
            {
                if (post.Message != null)
                {
                    listBoxNewsFeed.Items.Add(post.Message);
                }
                else if (post.Caption != null)
                {
                    listBoxNewsFeed.Items.Add(post.Caption);
                }
                else
                {
                    listBoxNewsFeed.Items.Add(string.Format("[{0}]", post.Type));
                }
            }
        }

        private void linkFriends_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            fetchFriends();
        }

        private void fetchFriends()
        {
            listBoxFriends.DisplayMember = "Name";
            foreach (User friend in m_LoggedInUser.Friends)
            {
                listBoxFriends.Items.Add(friend);
            }
        }

        private void listBoxFriends_SelectedIndexChanged(object sender, EventArgs e)
        {
            displaySelectedFriend();
        }

        private void displaySelectedFriend()
        {
            if (listBoxFriends.SelectedItems.Count == 1)
            {
                User selectedFriend = listBoxFriends.SelectedItem as User;
                if (selectedFriend.PictureNormalURL != null)
                {
                    pictureBoxFriend.LoadAsync(selectedFriend.PictureNormalURL);
                }
                else
                {
                    picture_smallPictureBox.Image = picture_smallPictureBox.ErrorImage;
                }
            }
        }

        private void labelEvents_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            fetchEvents();
        }

        private void fetchEvents()
        {
            listBoxEvents.DisplayMember = "Name";
            foreach (Event fbEvent in m_LoggedInUser.Events)
            {
                listBoxEvents.Items.Add(fbEvent);
            }
        }

        private void listBoxEvents_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (listBoxEvents.SelectedItems.Count == 1)
            {
                Event selectedEvent = listBoxEvents.SelectedItem as Event;
                pictureBoxEvent.LoadAsync(selectedEvent.PictureNormalURL);
            }
        }

        //private void linkCheckins_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        //{
        //    fetchCheckins();
        //}

        //private void fetchCheckins()
        //{
        //    foreach (Checkin checkin in m_LoggedInUser.Checkins)
        //    {
        //        listBoxCheckins.Items.Add(checkin);
        //    }
        //}

        //Lee's addition
        private void fetchCheckinByPlace(String i_location)
        {
            FacebookCheckInVicinityProvider fbVicinityProv = new FacebookCheckInVicinityProvider();
            GoogleMapsLocationProvider locationPrvdr = new GoogleMapsLocationProvider();
            GeographicalDistanceComputer distanceComputer = new GeographicalDistanceComputer();
            double userDistance = Convert.ToDouble(textBoxDistance.Text);
            String refernce = String.Empty;
            DateTime date = dateTimePickerUser.Value.Date;
            foreach (var location in userAddressSuggestions)
            {
                if (location.Description == i_location)
                {
                    refernce = location.Reference;
                }
            }
            Coordinate userCoordinates = locationPrvdr.GetLocationCoordinates(refernce);
            Coordinate friendCoordinate = null;
            var recentTags = fbVicinityProv.getAllUserFriendsRecentTags(m_LoggedInUser, date, "CreatedTime", 100);

            foreach (var checkin in recentTags)
            {
                friendCoordinate = new Coordinate(checkin.Place.Location.Latitude, checkin.Place.Location.Longitude);
                if (distanceComputer.IsNear(friendCoordinate, userDistance, userCoordinates))
                {
                    listBoxCheckinByPlace.Items.Add(checkin);
                }
            }

            if (listBoxCheckinByPlace.Items.Count == 0)
            {
                MessageBox.Show(string.Format("No friend was found in {0} at {1} around {2} meters", i_location, date.Date, userDistance));
                listBoxCheckinByPlace.Visible = false;
            }
        }

        private void ButtonMyLocation_Click(object sender, EventArgs e)
        {
            listBoxAddressSuggestion.Items.Clear();
            listBoxCheckinByPlace.Items.Clear();
            fetchAddressSuggestion();
        }

        private void fetchAddressSuggestion()
        {

            GoogleMapsLocationProvider locationPrvdr = new GoogleMapsLocationProvider();
            string userInput = textBoxLocation.Text;
            userAddressSuggestions = locationPrvdr.GetLocationSuggestions(userInput);

            foreach (GoogleMapsReference address in userAddressSuggestions)
            {
                listBoxAddressSuggestion.Items.Add(address.Description);

            }
            listBoxAddressSuggestion.Visible = true;

        }

        private List<GoogleMapsReference> userAddressSuggestions { get; set; }

        private void listBoxAddressSuggestion_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (listBoxAddressSuggestion.SelectedItems.Count == 1)
            {
                String userLocationSelect = listBoxAddressSuggestion.SelectedItem.ToString();

                DialogResult dialogResult = MessageBox.Show(userLocationSelect, "Your Location you choose is", MessageBoxButtons.OKCancel);
                if (dialogResult == DialogResult.OK)
                {
                    listBoxAddressSuggestion.Items.Clear();
                    listBoxAddressSuggestion.Visible = false;
                    listBoxCheckinByPlace.Visible = true;
                    Cursor.Current = Cursors.WaitCursor;
                    fetchCheckinByPlace(userLocationSelect);
                }
            }
        }

        private void listBoxCheckinByPlace_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (listBoxCheckinByPlace.SelectedItems.Count == 1)
            {
                linkLabelComments.Visible = true;
                linkLabelLikes.Visible = true;

                listBoxViewCheckinLikes.Items.Clear();
                listBoxViewCheckinLikes.Visible = false;

                listBoxViewCheckinComments.Items.Clear();
                listBoxViewCheckinComments.Visible = false;
                
                Checkin selectedCheckin = listBoxCheckinByPlace.SelectedItem as Checkin;
                StringBuilder message = new StringBuilder();
                message.Append(selectedCheckin.ToString()).Append(Environment.NewLine).Append("Checkin message: ").Append(selectedCheckin.Message);
                MessageBox.Show(message.ToString());
            }
        }

        private void linkLabelComments_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            fetchCheckinComments();
        }


        private void linkLabelLikes_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            fetchCheckinLikes();
        }

        private void fetchCheckinLikes()
        {
            
            if (listBoxCheckinByPlace.SelectedItems.Count == 1)
            {
                Checkin selectedCheckin = listBoxCheckinByPlace.SelectedItem as Checkin;
                
                foreach (User user in selectedCheckin.LikedBy)
                {

                    listBoxViewCheckinLikes.Items.Add(user);
                    if (!m_LoggedInUser.Friends.Contains(user))
                    {
                        //TODO somthing..
                    }
                }
                listBoxViewCheckinLikes.Visible = true;
            }
        }

        private void fetchCheckinComments()
        {
            if (listBoxCheckinByPlace.SelectedItems.Count == 1)
            {
                Checkin selectedCheckin = listBoxCheckinByPlace.SelectedItem as Checkin;
                foreach (Comment comment in selectedCheckin.Comments)
                {
                    listBoxViewCheckinComments.Items.Add(comment);
                    if (!m_LoggedInUser.Friends.Contains(comment.From))
                    {
                        //TODO somthing..               
                    }
                }
                listBoxViewCheckinComments.Visible = true;
            }
        }

        private void listBoxViewCheckinComments_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void listBoxViewCheckinLikes_SelectedIndexChanged(object sender, EventArgs e)
        {
            
        }
    }

    // Application: Class Example (by design.patterns)
    // AppID: 185561228241561
}
