// -----------------------------------------------------------------------
// <copyright file="CheckInsFriendsRecommender.cs" company="">
// TODO: Update copyright text.
// </copyright>
// -----------------------------------------------------------------------

namespace FaceBookBackEnd
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using FacebookWrapper.ObjectModel;
    using FacebookWrapper;
    using System.Linq.Expressions;

    internal class CheckInsFriendsRecommender : IFriendsRecommender
    {
        public List<User> GetSuggestions<T, TKey>(User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc)
        {
            var aggregatedCheckins = new List<Checkin>();
            foreach (var checkin in i_LoggedInUser.Checkins)
            {
                aggregatedCheckins.Add(checkin);
            }
            var sortedCheckinsByCreateTime = aggregatedCheckins.Select(x => x)
                            .OrderBy<Checkin, TKey>(i_OrderByFunc as Func<Checkin, TKey>)
                                    .Reverse();
            return getFriendSuggestionsFromCheckins(i_LoggedInUser, sortedCheckinsByCreateTime, i_MaxResults);
        }

        private List<User> getFriendSuggestionsFromCheckins(
            User i_LoggedInUser, IEnumerable<Checkin> checkins, int i_MaxResults)
        {
            var suggestedUsers = new List<User>();
            var alreadySuggestedUsersIds = new HashSet<string>(i_LoggedInUser.Friends.Select(f => f.Id));
            alreadySuggestedUsersIds.Add(i_LoggedInUser.Id);
            foreach (var checkin in checkins)
            {
                try
                {
                    if (checkin.TaggedUsers != null)
                    {
                        foreach (var taggedUser in checkin.TaggedUsers)
                        {
                            if (!alreadySuggestedUsersIds.Contains(taggedUser.Id))
                            {
                                suggestedUsers.Add(taggedUser);
                                alreadySuggestedUsersIds.Add(taggedUser.Id);
                            }
                        }
                    }
                }
                catch (Microsoft.CSharp.RuntimeBinder.RuntimeBinderException)
                {
                    // this is sometimes thrown from facebook Dll for an un known reason
                }
            }
            return suggestedUsers.Select(x => x).Take(i_MaxResults).ToList();
        }
    }
}
