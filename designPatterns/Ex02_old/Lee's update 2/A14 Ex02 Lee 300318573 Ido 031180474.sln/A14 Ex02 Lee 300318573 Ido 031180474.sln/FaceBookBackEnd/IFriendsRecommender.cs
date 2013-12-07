using System;
using System.Collections.Generic;
using FacebookWrapper.ObjectModel;
namespace FaceBookBackEnd
{
    interface IFriendsRecommender
    {
        List<User> GetSuggestions(User i_LoggedInUser, eRecommendationSortKey i_sortBy, int i_MaxResults);
        List<User> GetSuggestions2<T, TKey>(User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc);
    }
}
