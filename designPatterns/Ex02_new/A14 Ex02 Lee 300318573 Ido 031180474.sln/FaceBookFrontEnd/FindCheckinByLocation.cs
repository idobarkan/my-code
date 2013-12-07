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
        private Utilities m_Util;
        private CheckinHolder m_CheckinHolder;
        private User m_LoggedInUser;
        private ErrorProvider m_ErrorProviderNumber;
        private ErrorProvider m_ErrorProviderText;
        private double UserDistance { get; set; }
        private int MaxCount { get; set; }
        private String SortBy { get; set; }
        private String UserLocation { get; set; }
        private DateTime Date { get; set; }

        public FindCheckinByLocationForm(User i_LoggedInUser)
        {
            InitializeComponent();
            this.m_LoggedInUser = i_LoggedInUser;
            this.m_ErrorProviderNumber = new ErrorProvider();
            this.m_ErrorProviderText = new ErrorProvider();
            this.m_Util = new Utilities();
            this.m_CheckinHolder = new CheckinHolder();
        }

        private bool validateControls(Func<String, bool> i_IsValid, ErrorProvider i_ErrorProvider, params Control[] i_ControlsToValidate)
        {
            bool isControlsValid = true;
            foreach (var control in i_ControlsToValidate)
            {
                isControlsValid = i_IsValid(control.Text);

                if (!isControlsValid)
                {
                    i_ErrorProvider.SetError(control, Utilities.sr_FillField);
                }
                else
                {
                    i_ErrorProvider.SetError(control, String.Empty);
                    i_ErrorProvider.Clear();
                }
            }

            return isControlsValid;
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
            m_Util.clearListBox(listBoxViewCheckinLikes, listBoxViewCheckinComments);

            listBoxViewCheckinLikes.Visible = false;
            listBoxViewCheckinComments.Visible = false;
        }

        private void fetchCheckinByPlace(User i_LoggedInUser)
        {
            listBoxCheckinByPlace.Items.Clear();
            m_CheckinHolder.setRecentCheckins(i_LoggedInUser, Date, SortBy, MaxCount);
            m_CheckinHolder.setAllCheckinByPlace(UserLocation, UserDistance, listBoxAddressSuggestion.SelectedItem.ToString());

            foreach (Checkin checkin in m_CheckinHolder.CheckinByPlace)
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
                    listBoxViewCheckinLikes.Items.Add(m_Util.noItem(Utilities.sr_Likes));
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
                    listBoxViewCheckinComments.Items.Add(m_Util.noItem(Utilities.sr_Comments));
                }

                listBoxViewCheckinComments.Visible = true;
            }
        }

        private void fetchAddressSuggestion()
        {
            m_CheckinHolder.setUserAddresses(UserLocation);

            foreach (GoogleMapsReference address in m_CheckinHolder.UserAddressSuggestions)
            {
                listBoxAddressSuggestion.Items.Add(address.Description);
            }
        }

        private void clearForm()
        {
            updateControls();
            m_Util.clearListBox(listBoxCheckinByPlace, listBoxAddressSuggestion, listBoxCheckinChoosen);

            pictureBoxCheckinUser.Image = null;

            m_Util.disableControls(ButtonCheckin, linkLabelLikes, linkLabelComments);
        }

        private void buttonFindLocation_Click(object sender, EventArgs e)
        {
            clearForm();

            bool isLocationValid = validateControls(m_Util.isUserTextValid, m_ErrorProviderText, textBoxLocation);

            if (isLocationValid)
            {
                UserLocation = textBoxLocation.Text;
                fetchAddressSuggestion();
            }
            else return;
        }

        private void ButtonCheckin_Click(object sender, EventArgs e)
        {
            Cursor.Current = Cursors.WaitCursor;
            bool isControlsNumbersValid = validateControls(m_Util.isValidNunber, m_ErrorProviderNumber, textBoxDistance);

            bool isControlsTextValid = validateControls(m_Util.isUserTextValid, m_ErrorProviderText, dateTimePickerUser, comboBoxSortBy, comboBoxMaxCount);
            
            if (isControlsTextValid & isControlsNumbersValid)
            {
                initializeUserCheckinInput();
            }
            else return;

            fetchCheckinByPlace(this.m_LoggedInUser);
            m_Util.enableControls(listBoxCheckinByPlace);
        }

        private void listBoxAddressSuggestion_SelectedIndexChanged(object sender, EventArgs e)
        {
            m_Util.clearListBox(listBoxCheckinByPlace, listBoxCheckinChoosen);
            pictureBoxCheckinUser.Image = null;

            if (listBoxAddressSuggestion.SelectedItems.Count == 1)
            {
                Cursor.Current = Cursors.WaitCursor;
                m_Util.enableControls(ButtonCheckin);
            }
        }

        private void listBoxCheckinByPlace_SelectedIndexChanged(object sender, EventArgs e)
        {
            m_Util.clearListBox(listBoxCheckinChoosen);
            
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
                    listBoxCheckinChoosen.Items.Add(m_Util.noItem(Utilities.sr_Messages));
                }

                if (selectedCheckin.From.PictureNormalURL != null)
                {
                    pictureBoxCheckinUser.LoadAsync(selectedCheckin.From.PictureNormalURL);
                }

                m_Util.enableControls(linkLabelComments, linkLabelLikes);
            }
        }

        private void linkLabelComments_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            m_Util.clearListBox(listBoxViewCheckinComments);
            fetchCheckinComments();
        }

        private void linkLabelLikes_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            m_Util.clearListBox(listBoxViewCheckinLikes);
            fetchCheckinLikes();
        }
    }
}
