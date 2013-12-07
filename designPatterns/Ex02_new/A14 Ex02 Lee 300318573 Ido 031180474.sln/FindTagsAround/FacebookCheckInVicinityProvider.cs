
namespace FindTagsAround
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using FacebookWrapper.ObjectModel;

    /// <summary>
    public class FacebookCheckInVicinityProvider : ICheckInVicinityProvider
    {
        public List<Checkin> getAllUserFriendsRecentTags(
            User i_LoggedInUser, DateTime i_Oldest, string i_Sortby, int i_Max_count)
        {
            var aggregatedCheckins = new List<Checkin>();
            foreach (var friend in i_LoggedInUser.Friends)
            {
                foreach (var checkIn in friend.Checkins)
                {
                    if (checkIn.CreatedTime > i_Oldest)
                    {
                        aggregatedCheckins.Add(checkIn);
                    }
                }
            }
            if (i_Sortby == "CreatedTime")
            {
                return aggregatedCheckins.Select(x => x)
                    .OrderBy(x => x.CreatedTime)
                    .Take(i_Max_count)
                    .ToList();
            }
            else if (i_Sortby == "CommentsCount")
            {
                return aggregatedCheckins.Select(x => x)
                    .OrderBy(x => x.Comments.Count)
                    .Take(i_Max_count)
                    .ToList();
            }
            return aggregatedCheckins.ToList();//.ToDictionary<string, Checkin>(x => x.Id, x => x);
            
        }
    }
}
