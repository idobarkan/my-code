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

        private User m_LoggedInUser;
        private FacebookBackend m_FacebookEnd;
               public User LogedInUser;
        
        public FacebookForm(User i_LoggedIngUser, FacebookBackend i_FacebookEnd)
        {
            InitializeComponent();
            this.m_LoggedInUser = i_LoggedIngUser;
            this.m_FacebookEnd = i_FacebookEnd;
            fetchUserInfo();
        }
    
        private void fetchUserInfo()
        {
            picture_smallPictureBox.LoadAsync(m_LoggedInUser.PictureNormalURL);
            if (m_LoggedInUser.Statuses.Count > 0)
            {
                textBoxStatus.Text = m_LoggedInUser.Statuses[0].Message;
            }
        }

        private void FindFriendsCheckin_Click(object sender, EventArgs e)
        {
            FindCheckinByLocationForm findCheckin = new FindCheckinByLocationForm(m_LoggedInUser);
            findCheckin.ShowDialog();
        }
        private void buttonSuggestFriends_Click(object sender, EventArgs e)
        {
            SuggestFriendsForm suggestFriend = new SuggestFriendsForm(m_LoggedInUser, m_FacebookEnd);
            suggestFriend.ShowDialog();
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

        private void linkCheckins_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            fetchCheckins();
        }

        private void fetchCheckins()
        {
            foreach (Checkin checkin in m_LoggedInUser.Checkins)
            {
                listBoxCheckins.Items.Add(checkin);
            }
        }

         private void linkLabelCheckins_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            fetchCheckins();
        }
        
       

        

        

       
    }

    // Application: Class Example (by design.patterns)
    // AppID: 185561228241561
}
