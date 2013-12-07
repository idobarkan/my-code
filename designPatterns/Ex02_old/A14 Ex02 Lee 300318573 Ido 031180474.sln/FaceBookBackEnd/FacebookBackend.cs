using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using FacebookWrapper.ObjectModel;
using FacebookWrapper;
using System.IO;

namespace FaceBookBackEnd
{
    public class FacebookBackend : IAuthenticator, IFriendSuggestionsProvider
    {
        private LogIner m_LogIner = new LogIner();
        private CheckInsFriendsRecommender m_CheckInsFriendsRecommender = new CheckInsFriendsRecommender();
        private PhotosFriendsRecommender m_PhotosFriendsRecommender = new PhotosFriendsRecommender();
        private EventsFriendsRecommender m_EventsFriendsRecommender = new EventsFriendsRecommender();

        public User LogIn()
        {
            return m_LogIner.LogIn();
        }

        public List<User> GetSuggestions(string i_Source, User i_LoggedInUser, string i_sortBy, int i_MaxResults)
        {
            if (i_Source == "FromCheckins")
            {
                return m_CheckInsFriendsRecommender.GetSuggestions(i_LoggedInUser, i_sortBy, i_MaxResults); 
            }
            else if (i_Source == "FromPhotos")
            {
                return m_PhotosFriendsRecommender.GetSuggestions(i_LoggedInUser, i_sortBy, i_MaxResults);
            }
            else if (i_Source == "FromEvents")
            {
                return m_EventsFriendsRecommender.GetSuggestions(i_LoggedInUser, i_sortBy, i_MaxResults);
            }
            else
            {
                throw new Exception("unknown source");
            }
        }

        public List<User> GetSuggestions2<T, TKey>(string i_Source, User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc)
        {
            if (i_Source == "FromCheckins")
            {
                return m_CheckInsFriendsRecommender.GetSuggestions2<T, TKey>(
                    i_LoggedInUser,
                    i_MaxResults,
                    i_OrderByFunc
                        );
            }
            else if (i_Source == "FromPhotos")
            {
                return m_PhotosFriendsRecommender.GetSuggestions2<T, TKey>(
                    i_LoggedInUser,
                    i_MaxResults,
                    i_OrderByFunc
                        );
            }
            else if (i_Source == "FromEvents")
            {
                return m_EventsFriendsRecommender.GetSuggestions2<T, TKey>(
                    i_LoggedInUser,
                    i_MaxResults,
                    i_OrderByFunc
                        );
            }
            else
            {
                throw new Exception("unknown source");
            }
        }
    }
}
