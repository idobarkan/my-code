using System;
using System.Collections.Generic;
using FacebookWrapper.ObjectModel;
namespace FaceBookBackEnd
{
    interface IFriendsRecommender
    {
        List<User> GetSuggestions<T, TKey>(User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc);
    }
}
