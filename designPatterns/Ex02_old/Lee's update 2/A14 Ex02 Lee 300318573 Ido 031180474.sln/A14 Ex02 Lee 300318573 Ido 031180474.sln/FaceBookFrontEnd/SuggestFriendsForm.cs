﻿using System;
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

namespace FaceBookFrontEnd
{
    public partial class SuggestFriendsForm : Form
    {
        private User m_LoggedInUser;
        private FacebookBackend m_Fb;
        public SuggestFriendsForm(User i_LoginUser, FacebookBackend i_Fb)
        {
            this.m_LoggedInUser = i_LoginUser;
            this.m_Fb = i_Fb;
            InitializeComponent();
        }

        private void UsersSuggestions()
        {
           // List<User> recentTags = m_Fb.GetSuggestions2<Checkin, int>(eRecommendationSource.Checkins, m_LoggedInUser, 10, (Checkin c) => c.Comments.Count);
        }

      
        private void buttonSuggestByPhotos_Click(object sender, EventArgs e)
        {
            List<User> recentTags = this.m_Fb.GetSuggestions2<Photo, int>(
                eRecommendationSource.Photos, 
                m_LoggedInUser, 
                10, 
                (Photo p) => p.Tags == null? Int32.MaxValue :p.Tags.Count);
            foreach (User user in recentTags)
            {
                listBoxSuggestedByPhotos.Items.Add(user);
            }
        }

        private void buttonSuggestedByCheckin_Click(object sender, EventArgs e)
        {
            List<User> recentTags = m_Fb.GetSuggestions2<Checkin, int>(
                eRecommendationSource.Checkins, 
                m_LoggedInUser, 
                10, 
                (Checkin c) => c.Comments.Count);
            foreach (User user in recentTags)
            {
                listBoxSuggestedByCheckin.Items.Add(user);
            }
        }

        private void buttonSuggestedByEvent_Click(object sender, EventArgs e)
        {
            List<User> sugestedFriends = m_Fb.GetSuggestions2<Event, int>(
                eRecommendationSource.Checkins, 
                m_LoggedInUser, 
                10, 
                (Event ev) => ev.InvitedUsers.Count);
            foreach (User user in sugestedFriends)
            {
                listBoxSuggestedByCheckin.Items.Add(user);
            }
        }
    }
}
