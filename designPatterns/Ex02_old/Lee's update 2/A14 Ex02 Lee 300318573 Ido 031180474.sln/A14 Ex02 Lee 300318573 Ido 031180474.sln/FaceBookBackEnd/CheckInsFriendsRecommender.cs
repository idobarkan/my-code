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
        public List<User> GetSuggestions(User i_LoggedInUser, eRecommendationSortKey i_sortBy, int i_MaxResults)
        {
            List<User> suggestedUsers = null;
            var aggregatedCheckins = new List<Checkin>();
            foreach (var checkin in i_LoggedInUser.Checkins)
            {
                aggregatedCheckins.Add(checkin);
            }

            if (i_sortBy == eRecommendationSortKey.CreateTime)
            {
                var sortedCheckinsByCreateTime = aggregatedCheckins.Select(x => x)
                                .OrderBy(x => x.CreatedTime);
                suggestedUsers = getFriendSuggestionsFromCheckins(i_LoggedInUser, sortedCheckinsByCreateTime, i_MaxResults);
            }
            else if (i_sortBy == eRecommendationSortKey.Likes)
            {
                var sortedCheckinsByLikes = aggregatedCheckins.Select(x => x)
                                .OrderBy(x => x.LikedBy.Count);
                suggestedUsers = getFriendSuggestionsFromCheckins(i_LoggedInUser, sortedCheckinsByLikes, i_MaxResults);

            }
            else if (i_sortBy == eRecommendationSortKey.Comments)
            {
                var sortedCheckinsByComments = aggregatedCheckins.Select(x => x)
                                .OrderBy(x => x.Comments.Count);
                suggestedUsers = getFriendSuggestionsFromCheckins(i_LoggedInUser, sortedCheckinsByComments, i_MaxResults);
            }
            else
            {
                suggestedUsers = getFriendSuggestionsFromCheckins(i_LoggedInUser, aggregatedCheckins, i_MaxResults);
            }

            return suggestedUsers;
        }

        public List<User> GetSuggestions2<T, TKey>(User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc)
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
            foreach (var checkin in checkins)
            {
                try
                {
                    if (checkin.TaggedUsers != null)
                    {
                        foreach (var taggedUser in checkin.TaggedUsers)
                        {
                            if (!i_LoggedInUser.Friends.Contains(taggedUser))
                            {
                                suggestedUsers.Add(taggedUser);
                            }
                        }
                    }
                }
                catch (Microsoft.CSharp.RuntimeBinder.RuntimeBinderException)
                {
                    
                }
            }
            return suggestedUsers.Select(x => x).Take(i_MaxResults).ToList();
        }
    }
}
