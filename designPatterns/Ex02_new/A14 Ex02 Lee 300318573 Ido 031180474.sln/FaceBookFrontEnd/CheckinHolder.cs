using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using FacebookWrapper.ObjectModel;
using FacebookWrapper;
using FaceBookBackEnd;
using FindTagsAround;
using FaceBookFrontEnd;

namespace FaceBookFrontEnd
{
    internal class CheckinHolder
    {
        private List<GoogleMapsReference> m_UserAddressSuggestions;
        private List<Checkin> m_RecentCheckins;
        private List<Checkin> m_CheckinByPlace;
        
        public List<Checkin> RecentCheckins
        {
            get { return m_RecentCheckins; }
        }

        public List<GoogleMapsReference> UserAddressSuggestions
        {
            get { return m_UserAddressSuggestions; }
        }

        public List<Checkin> CheckinByPlace
        {
            get { return m_CheckinByPlace; }
        }
        
        internal void setUserAddresses(String i_UserInput)
        {
            GoogleMapsLocationProvider locationPrvdr = new GoogleMapsLocationProvider();
            m_UserAddressSuggestions = locationPrvdr.GetLocationSuggestions(i_UserInput);
        }
        
        private string findUserReferenceLocation(String i_AddressSelected)
        {
            String reference = String.Empty;
            foreach (var location in m_UserAddressSuggestions)
            {
                if (location.Description == i_AddressSelected)
                {
                    reference = location.Reference;
                }
            }
            return reference;
        }
        
        internal void setRecentCheckins(User i_LoggedUser, DateTime i_Date, String i_SortBy, int i_MaxCount)
        {
            FacebookCheckInVicinityProvider fbVicinityProv = new FacebookCheckInVicinityProvider();
            m_RecentCheckins = fbVicinityProv.getAllUserFriendsRecentTags(i_LoggedUser, i_Date, i_SortBy, i_MaxCount);
        }
        
        internal void setAllCheckinByPlace(String userLocation, double userDistance, String addressSelected)
        {
            GoogleMapsLocationProvider locationPrvdr = new GoogleMapsLocationProvider();
            GeographicalDistanceComputer distanceComputer = new GeographicalDistanceComputer();
            String reference = findUserReferenceLocation(addressSelected);
            Coordinate userCoordinates = locationPrvdr.GetLocationCoordinates(reference);
            Coordinate friendCoordinate = null;
            m_CheckinByPlace = new List<Checkin>();
                  
            foreach (var checkin in RecentCheckins)
            {
                if (checkin.Place.Location.Latitude == null || checkin.Place.Location.Longitude == null)
                {
                    continue;
                }
                else
                {
                    friendCoordinate = new Coordinate((double)checkin.Place.Location.Latitude, (double)checkin.Place.Location.Longitude);
                }
                    if (distanceComputer.IsNear(friendCoordinate, userDistance, userCoordinates))
                {
                    CheckinByPlace.Add(checkin);
                }
            }
        }
    }
}
