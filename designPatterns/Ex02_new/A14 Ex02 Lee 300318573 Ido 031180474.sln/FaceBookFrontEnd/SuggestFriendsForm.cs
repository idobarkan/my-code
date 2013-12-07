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

namespace FaceBookFrontEnd
{
    public partial class SuggestFriendsForm : Form
    {
        private User m_LoggedInUser;
        private FacebookBackend m_Fb;
        private Utilities m_Util;
        private ErrorProvider m_ErrorProvider;

        public SuggestFriendsForm(User i_LoginUser, FacebookBackend i_Fb)
        {
            InitializeComponent();
            this.m_LoggedInUser = i_LoginUser;
            this.m_Fb = i_Fb;
            this.m_Util = new Utilities();
            this.m_ErrorProvider = new ErrorProvider();
        }

        private bool validateControls(Func<String, bool> isValid, params Control[] ControlsToValidate)
        {
            bool isControlsValid = true;
            
            foreach (var control in ControlsToValidate)
            {
                isControlsValid = isValid(control.Text);
                
                if (!isControlsValid)
                {
                    m_ErrorProvider.SetError(control, Utilities.sr_FillFieldNumber);
                }
                else
                {
                    m_ErrorProvider.SetError(control, String.Empty);
                    m_ErrorProvider.Clear();
                }
            }
            
            return isControlsValid;
        }

        private void buttonSuggestByPhotos_Click(object sender, EventArgs e)
        {
            listBoxSuggestedByPhotos.Items.Clear();
            pictureBoxFriendByPhoto.Image = null;
            Cursor.Current = Cursors.WaitCursor;
            
            suggestFriendsByPhotos();
        }

        private void suggestFriendsByPhotos()
        {
            bool isValid = validateControls(m_Util.isValidNunber, textBoxMaxResults);
            List<User> suggestFriendsByPhotos = null;
            
            if (isValid)
            {
                suggestFriendsByPhotos = new List<User>();
                suggestFriendsByPhotos = m_Fb.GetSuggestions<Photo, int>(eRecommendationSource.Photos, m_LoggedInUser,
                    Int32.Parse(textBoxMaxResults.Text), (Photo photos) => photos.Tags != null ? photos.Tags.Count : 0);
                
                foreach (User user in suggestFriendsByPhotos)
                {
                    listBoxSuggestedByPhotos.Items.Add(user);
                }
            }
        }

        private void suggestFriendsByEvents()
        {
            bool isValid = validateControls(m_Util.isValidNunber, textBoxMaxResults);
            List<User> suggestFriendsByEvents = null;
            if (isValid)
            {
                suggestFriendsByEvents = new List<User>();
                suggestFriendsByEvents = m_Fb.GetSuggestions<Event, int>(eRecommendationSource.Events, m_LoggedInUser,
                    Int32.Parse(textBoxMaxResults.Text), (Event events) => events.AttendingUsers != null ? events.AttendingUsers.Count : 0);
                foreach (User user in suggestFriendsByEvents)
                {
                    listBoxSuggestedByEvent.Items.Add(user);
                }
            }
        }

        private void buttonSuggestedByEvent_Click(object sender, EventArgs e)
        {
            listBoxSuggestedByEvent.Items.Clear();
            pictureBoxFriendByEvent.Image = null;
            Cursor.Current = Cursors.WaitCursor;
            suggestFriendsByEvents();   
        }

      

        private void listBoxSuggestedByPhotos_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (listBoxSuggestedByPhotos.SelectedItems.Count == 1)
            {
                User selectedFriend = listBoxSuggestedByPhotos.SelectedItem as User;
                if (selectedFriend.PictureNormalURL != null)
                {
                    pictureBoxFriendByPhoto.LoadAsync(selectedFriend.PictureNormalURL);
                }
            }
        }

        private void listBoxSuggestedByEvent_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (listBoxSuggestedByEvent.SelectedItems.Count == 1)
            {
                User selectedFriend = listBoxSuggestedByEvent.SelectedItem as User;
                if (selectedFriend.PictureNormalURL != null)
                {
                    pictureBoxFriendByEvent.LoadAsync(selectedFriend.PictureNormalURL);
                }
            }
        }
    }
}
