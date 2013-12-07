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
        public List<User> GetSuggestions(User i_LoggedInUser, eRecommendationSortKey i_sortBy, int i_MaxResults)
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
            if (i_sortBy == eRecommendationSortKey.UpdateTime)
            {
                var sortedPhotosByUpdateTime = aggregatedPhotos.Select(x => x)
                                       .OrderBy(x => x.UpdateTime)
                                       .Take(i_MaxResults);

                suggestedUsers = getFriendSuggestionsFromPhotos(i_LoggedInUser, sortedPhotosByUpdateTime, i_MaxResults);
            }
            else if (i_sortBy == eRecommendationSortKey.Likes)
            {
                var sortedPhotosByLikes = aggregatedPhotos.Select(x => x)
                                   .OrderBy(x => x.LikedBy.Count)
                                   .Take(i_MaxResults);
                suggestedUsers = getFriendSuggestionsFromPhotos(i_LoggedInUser, sortedPhotosByLikes, i_MaxResults);
            }
            else if (i_sortBy == eRecommendationSortKey.Tags)
            {
                var sortedPhotosByTags = aggregatedPhotos.Select(x => x)
                                   .OrderBy(x => x.Tags.Count)
                                   .Take(i_MaxResults);
                suggestedUsers = getFriendSuggestionsFromPhotos(i_LoggedInUser, sortedPhotosByTags, i_MaxResults);
            }
            return suggestedUsers;
        }

        public List<User> GetSuggestions2<T, TKey>(User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc)
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
                                    .Take(i_MaxResults);

            return getFriendSuggestionsFromPhotos(i_LoggedInUser, sortedPhotosByUpdateTime, i_MaxResults);
            
        }

        private List<User> getFriendSuggestionsFromPhotos(
            User i_LoggedInUser, IEnumerable<Photo> photos, int i_MaxResults)
        {
            var suggestedUsers = new List<User>();
            foreach (var photo in photos)
            {
                foreach (var tag in photo.Tags)
                {
                    if (!i_LoggedInUser.Friends.Contains(tag.User))
                    {
                        suggestedUsers.Add(tag.User);
                    }
                }
            }
            return suggestedUsers.Select(x => x).Take(i_MaxResults).ToList();
        }
    }
}
