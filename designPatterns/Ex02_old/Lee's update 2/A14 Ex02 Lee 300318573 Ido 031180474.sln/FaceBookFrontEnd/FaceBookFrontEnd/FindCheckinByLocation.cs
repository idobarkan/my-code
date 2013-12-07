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
using BasicFacebookFeatures.WithSingltonAppSettings;

namespace FaceBookFrontEnd
{
    public partial class FindCheckinByLocationForm : Form
    {
        private CheckinApp m_CheckinApp;
        private User m_LoggedInUser;

        private double UserDistance { get; set; }
        private int MaxCount { get; set; }
        private String SortBy { get; set; }
        private String UserLocation { get; set; }
        private DateTime Date { get; set; }

        public FindCheckinByLocationForm(User i_LoggedInUser)
        {
            this.m_LoggedInUser = i_LoggedInUser;
            InitializeComponent();
            m_CheckinApp = new CheckinApp();
        }

        private void initCheckinpp()
        {
            m_CheckinApp.setupControlsToValidate(dateTimePickerUser, textBoxDistance, comboBoxSortBy, comboBoxMaxCount);
            m_CheckinApp.validate();
        }

        private void initializeUserCheckinInput()
        {
            UserDistance = Convert.ToDouble(textBoxDistance.Text);
            SortBy = comboBoxSortBy.SelectedItem.ToString();

            MaxCount = Int32.Parse(comboBoxMaxCount.SelectedItem.ToString());
            Date = dateTimePickerUser.Value.Date;
        }

        private void updateControls()
        {
            m_CheckinApp.clearListBox(listBoxViewCheckinLikes, listBoxViewCheckinComments);
            listBoxViewCheckinLikes.Visible = false;
            listBoxViewCheckinComments.Visible = false;
        }

        private void fetchCheckinByPlace(User i_LoggedInUser)
        {
            listBoxCheckinByPlace.Items.Clear();
            m_CheckinApp.getRecentCheckins(i_LoggedInUser, Date, SortBy, MaxCount);
            m_CheckinApp.allCheckinByPlace(UserLocation, UserDistance, listBoxAddressSuggestion.SelectedItem.ToString());
            foreach (Checkin checkin in m_CheckinApp.CheckinByPlace)
            {
                listBoxCheckinByPlace.Items.Add(checkin);
            }

            if (listBoxCheckinByPlace.Items.Count == 0)
            {
                MessageBox.Show(string.Format("No friend was found in {0} at {1} around {2} meters", listBoxAddressSuggestion.SelectedItem, Date.Date, UserDistance));
            }
        }

        private void fetchCheckinLikes()
        {
            if (listBoxCheckinByPlace.SelectedItems.Count == 1)
            {
                Checkin selectedCheckin = listBoxCheckinByPlace.SelectedItem as Checkin;

                foreach (User user in selectedCheckin.LikedBy)
                {
                    listBoxViewCheckinLikes.Items.Add(user);
                }

                if (listBoxViewCheckinLikes.Items.Count == 0)
                {
                    listBoxViewCheckinLikes.Items.Add("Likes");
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
                }

                if (listBoxViewCheckinComments.Items.Count == 0)
                {
                    listBoxViewCheckinComments.Items.Add(typeof(Comment));
                }

                listBoxViewCheckinComments.Visible = true;
            }
        }
        private void fetchAddressSuggestion()
        {
            m_CheckinApp.setUserAddresses(UserLocation);

            foreach (GoogleMapsReference address in m_CheckinApp.UserAddressSuggestions)
            {
                listBoxAddressSuggestion.Items.Add(address.Description);
            }
        }

        private void clearForm()
        {
            updateControls();
            m_CheckinApp.clearListBox(listBoxCheckinByPlace, listBoxAddressSuggestion, listBoxCheckinChoosen);
            pictureBoxCheckinUser.Image = null;
            m_CheckinApp.disableControls(ButtonCheckin, linkLabelLikes, linkLabelComments);
        }

        private void buttonFindLocation_Click(object sender, EventArgs e)
        {
            clearForm();

            m_CheckinApp.validateUserLocation(textBoxLocation);
            if (m_CheckinApp.IsControlsValid)
            {
                UserLocation = textBoxLocation.Text;
                fetchAddressSuggestion();
            }
            else return;
        }

        private void ButtonCheckin_Click(object sender, EventArgs e)
        {
            Cursor.Current = Cursors.WaitCursor;
            initCheckinpp();
            if (m_CheckinApp.IsControlsValid)
            {
                initializeUserCheckinInput();
            }
            else return;

            fetchCheckinByPlace(this.m_LoggedInUser);

            m_CheckinApp.enableControl(listBoxCheckinByPlace);

        }

        private void listBoxAddressSuggestion_SelectedIndexChanged(object sender, EventArgs e)
        {
            m_CheckinApp.clearListBox(listBoxCheckinByPlace, listBoxCheckinChoosen);
            pictureBoxCheckinUser.Image = null;
            if (listBoxAddressSuggestion.SelectedItems.Count == 1)
            {
                Cursor.Current = Cursors.WaitCursor;
                m_CheckinApp.enableControl(ButtonCheckin);
            }
        }

        private void listBoxCheckinByPlace_SelectedIndexChanged(object sender, EventArgs e)
        {
            m_CheckinApp.clearListBox(listBoxCheckinChoosen);
            if (listBoxCheckinByPlace.SelectedItems.Count == 1)
            {
                updateControls();

                Checkin selectedCheckin = listBoxCheckinByPlace.SelectedItem as Checkin;
                if (selectedCheckin.Message != null)
                {
                    listBoxCheckinChoosen.Items.Add("Checkin messege: " + selectedCheckin.Message);
                }
                    
                else
                {
                    listBoxCheckinChoosen.Items.Add(m_CheckinApp.noItem("Message"));
                }
                if (selectedCheckin.From.PictureNormalURL != null)
                {
                    pictureBoxCheckinUser.LoadAsync(selectedCheckin.From.PictureNormalURL);
                }
                m_CheckinApp.enableControl(linkLabelComments, linkLabelLikes);
            }
        }

        private void linkLabelComments_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            m_CheckinApp.clearListBox(listBoxViewCheckinComments);
            fetchCheckinComments();
        }

        private void linkLabelLikes_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            m_CheckinApp.clearListBox(listBoxViewCheckinLikes);
            fetchCheckinLikes();
        }
    }
}
