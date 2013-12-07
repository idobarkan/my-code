using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using FacebookWrapper.ObjectModel;
using FacebookWrapper;
using FaceBookBackEnd;
using FindTagsAround;
using FaceBookFrontEnd;
using System.Windows.Forms;



namespace FaceBookFrontEnd
{
    class CheckinApp
    {
        public CheckinApp()
        {

        }
        private List<Control> m_lstControlsToValidate;
        private List<GoogleMapsReference> m_UserAddressSuggestions;
        private ErrorProvider m_ErrorProvider = new ErrorProvider();
        private List<Checkin> m_RecentCheckins;
        private List<Checkin> m_CheckinByPlace;
        private bool m_IsControlsValid;
        public bool IsControlsValid { get { return m_IsControlsValid; }
            private set { m_IsControlsValid = value; }
        }
        public List<Checkin> RecentCheckins
        {
            get { return m_RecentCheckins; }
            private set { m_RecentCheckins = value; }
        }
        public List<GoogleMapsReference> UserAddressSuggestions
        {
            get { return m_UserAddressSuggestions; }
            private set { m_UserAddressSuggestions = value; }
        }
        public List<Checkin> CheckinByPlace
        {
            get { return m_CheckinByPlace; }
            private set { m_CheckinByPlace = value; }
        }
        public List<Control> ControlsToValidate
        {
            get { return m_lstControlsToValidate; }
            set { m_lstControlsToValidate = value; }
        }

        internal void clearListBox(params ListBox[] listBoxex)
        {
            foreach (ListBox listBox in listBoxex)
            {
                listBox.Items.Clear();
            }
        }
        internal void disableControls(params Control[] controls)
        {
            foreach (Control control in controls)
            {
                control.Enabled = false;
            }
        }
        internal void enableControl(params Control[] controls)
        {
            foreach (Control control in controls)
            {
                control.Enabled = true;
            }
        }

        internal void setupControlsToValidate(params Control[] list)
        {
            ControlsToValidate = new List<Control>();
            for (int i = 0; i < list.Length; i++)
            {
                ControlsToValidate.Add(list[i]);
            }
        }
        internal void validate()
        {
            //Then, you can iterate over them, and set the error accordingly:
            //ControlError = new List<Control>();
            IsControlsValid = true;
           
            foreach (var control in ControlsToValidate)
            {
                if (string.IsNullOrEmpty(control.Text))
                {
                    m_ErrorProvider.SetError(control, "please fill this field");
                    IsControlsValid = false;
                }
                else
                {
                    m_ErrorProvider.SetError(control, String.Empty);
                    m_ErrorProvider.Clear();
                }
            }
        }
        internal void validateUserLocation(TextBox i_userText)
        {
            IsControlsValid = true;
            if (string.IsNullOrEmpty(i_userText.Text))
            {
                m_ErrorProvider.SetError(i_userText, "please fill this field");
                IsControlsValid = false;
            }
            else
            {
                m_ErrorProvider.SetError(i_userText, String.Empty);
                m_ErrorProvider.Clear();
            }
        }

        internal void setUserAddresses(String i_UserInput)
        {
            GoogleMapsLocationProvider locationPrvdr = new GoogleMapsLocationProvider();
            UserAddressSuggestions = locationPrvdr.GetLocationSuggestions(i_UserInput);

        }
        internal string findUserReferenceLocation(String i_AddressSelected)
        {
            String reference = String.Empty;
            foreach (var location in UserAddressSuggestions)
            {
                if (location.Description == i_AddressSelected)
                {
                    reference = location.Reference;
                }
            }
            return reference;
        }

        internal void getRecentCheckins(User i_LoggedUser, DateTime i_Date, String i_SortBy, int i_MaxCount)
        {
            FacebookCheckInVicinityProvider fbVicinityProv = new FacebookCheckInVicinityProvider();
            RecentCheckins = fbVicinityProv.getAllUserFriendsRecentTags(i_LoggedUser, i_Date, i_SortBy, i_MaxCount);
        }
        internal void allCheckinByPlace(String userLocation, double userDistance, String addressSelected)
        {
            GoogleMapsLocationProvider locationPrvdr = new GoogleMapsLocationProvider();
            GeographicalDistanceComputer distanceComputer = new GeographicalDistanceComputer();
            String reference = findUserReferenceLocation(addressSelected);
            Coordinate userCoordinates = locationPrvdr.GetLocationCoordinates(reference);
            Coordinate friendCoordinate = null;
            CheckinByPlace = new List<Checkin>();
            foreach (var checkin in RecentCheckins)
            {
                friendCoordinate = new Coordinate(checkin.Place.Location.Latitude, checkin.Place.Location.Longitude);
                if (distanceComputer.IsNear(friendCoordinate, userDistance, userCoordinates))
                {
                    CheckinByPlace.Add(checkin);//Items.Add(checkin);
                }
            }

        }
        internal String noItem(String type)
        {
            StringBuilder message = new StringBuilder();
            message.Append("No ").Append(type).Append(" on this checkin.");
            return message.ToString();
        }
    }
}
