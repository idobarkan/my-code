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

    internal class PhotosFriendsRecommender : IFriendsRecommender
    {
        public List<User> GetSuggestions<T, TKey>(User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc)
        {
            var suggestedUsers = new List<User>();
            var aggregatedPhotos = new List<Photo>();
            foreach (var album in i_LoggedInUser.Albums)
            {
                foreach (var photo in album.Photos)
                {
                    aggregatedPhotos.Add(photo);
                }
            }
            var sortedPhotosByUpdateTime = aggregatedPhotos.Select(x => x)
                                    .OrderBy<Photo, TKey>(i_OrderByFunc as Func<Photo, TKey>)
                                    .Reverse();

            return getFriendSuggestionsFromPhotos(i_LoggedInUser, sortedPhotosByUpdateTime, i_MaxResults);
            
        }

        private List<User> getFriendSuggestionsFromPhotos(
            User i_LoggedInUser, IEnumerable<Photo> photos, int i_MaxResults)
        {
            var suggestedUsers = new List<User>();
            var alreadySuggestedUsersIds = new HashSet<string>(i_LoggedInUser.Friends.Select(f => f.Id));
            alreadySuggestedUsersIds.Add(i_LoggedInUser.Id);
            foreach (var photo in photos)
            {
                if (photo.Tags != null)
                {
                    foreach (var tag in photo.Tags)
                    {
                        if (!alreadySuggestedUsersIds.Contains(tag.User.Id))
                        {
                            suggestedUsers.Add(tag.User);
                            alreadySuggestedUsersIds.Add(tag.User.Id);
                        }
                    } 
                }
            }
            return suggestedUsers.Select(x => x).Take(i_MaxResults).ToList();
        }
    }
}
