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
        private IFriendsRecommender m_CheckInsFriendsRecommender = new CheckInsFriendsRecommender();
        private IFriendsRecommender m_PhotosFriendsRecommender = new PhotosFriendsRecommender();
        private IFriendsRecommender m_EventsFriendsRecommender = new EventsFriendsRecommender();

        public User LogIn()
        {
            return m_LogIner.LogIn();
        }

        public List<User> GetSuggestions<T, TKey>(eRecommendationSource i_Source, User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc)
        {
            if (i_Source == eRecommendationSource.Checkins)
            {
                return m_CheckInsFriendsRecommender.GetSuggestions<T, TKey>(
                    i_LoggedInUser,
                    i_MaxResults,
                    i_OrderByFunc
                        );
            }
            else if (i_Source == eRecommendationSource.Photos)
            {
                return m_PhotosFriendsRecommender.GetSuggestions<T, TKey>(
                    i_LoggedInUser,
                    i_MaxResults,
                    i_OrderByFunc
                        );
            }
            else if (i_Source == eRecommendationSource.Events)
            {
                return m_EventsFriendsRecommender.GetSuggestions<T, TKey>(
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
