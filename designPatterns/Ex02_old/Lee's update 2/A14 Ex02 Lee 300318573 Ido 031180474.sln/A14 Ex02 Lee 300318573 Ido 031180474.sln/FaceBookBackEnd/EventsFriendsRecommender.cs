// -----------------------------------------------------------------------
// <copyright file="PhotosFriendsRecommender.cs" company="">
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

    internal class EventsFriendsRecommender : IFriendsRecommender
    {
        public List<User> GetSuggestions(User i_LoggedInUser, eRecommendationSortKey i_sortBy, int i_MaxResults)
        {
            var suggestedUsers = new List<User>();
            var aggregatedEvents = new List<Event>();
            foreach (var event_ in i_LoggedInUser.Events)
            {
                aggregatedEvents.Add(event_);
            }
            if (i_sortBy == eRecommendationSortKey.StartTime)
            {
                var sortedPhotosByUpdateTime = aggregatedEvents.Select(x => x)
                                       .OrderBy(x => x.StartTime);

                suggestedUsers = getFriendSuggestionsFromEvents(i_LoggedInUser, sortedPhotosByUpdateTime, i_MaxResults);
            }
            else if (i_sortBy == eRecommendationSortKey.AttendingUsers)
            {
                var sortedPhotosByAttendingUsers = aggregatedEvents.Select(x => x)
                                   .OrderBy(x => x.AttendingUsers.Count);
                suggestedUsers = getFriendSuggestionsFromEvents(i_LoggedInUser, sortedPhotosByAttendingUsers, i_MaxResults);
            }
            else if (i_sortBy == eRecommendationSortKey.WallPosts)
            {
                var sortedPhotosByWallPosts = aggregatedEvents.Select(x => x)
                                   .OrderBy(x => x.WallPosts.Count);
                suggestedUsers = getFriendSuggestionsFromEvents(i_LoggedInUser, sortedPhotosByWallPosts, i_MaxResults);
            }
            return suggestedUsers;
        }

        public List<User> GetSuggestions2<T, TKey>(User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc)
        {
            var aggregatedEvents = new List<Event>();

            foreach (var event_ in i_LoggedInUser.Events)
            {
                aggregatedEvents.Add(event_);
            }
            var sortedPhotosByUpdateTime = aggregatedEvents.Select(x => x).ToList()
                                    .OrderBy<Event, TKey>(i_OrderByFunc as Func<Event, TKey>)
                                    .Reverse();

            return getFriendSuggestionsFromEvents(i_LoggedInUser, sortedPhotosByUpdateTime, i_MaxResults);
        }

        private List<User> getFriendSuggestionsFromEvents(
            User i_LoggedInUser, IEnumerable<Event> events, int i_MaxResults)
        {
            var suggestedUsers = new List<User>();
            foreach (var event_ in events)
            {
                foreach (var user in event_.AttendingUsers)
                {
                    if (!i_LoggedInUser.Friends.Contains(user))
                    {
                        suggestedUsers.Add(user);
                    }
                }
            }
            return suggestedUsers.Select(x => x).Take(i_MaxResults).ToList();
        }
    }


}
