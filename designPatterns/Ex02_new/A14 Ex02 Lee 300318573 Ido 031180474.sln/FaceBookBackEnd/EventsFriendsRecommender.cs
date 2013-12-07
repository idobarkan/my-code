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
        public List<User> GetSuggestions<T, TKey>(User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc)
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
            var alreadySuggestedUsersIds = new HashSet<string>(i_LoggedInUser.Friends.Select(f => f.Id));
            alreadySuggestedUsersIds.Add(i_LoggedInUser.Id);
            foreach (var event_ in events)
            {
                foreach (var user in event_.AttendingUsers)
                {
                    if (!alreadySuggestedUsersIds.Contains(user.Id))
                    {
                        suggestedUsers.Add(user);
                        alreadySuggestedUsersIds.Add(user.Id); 
                    } 
                }
            }
            return suggestedUsers.Select(x => x).Take(i_MaxResults).ToList();
        }
    }
}
