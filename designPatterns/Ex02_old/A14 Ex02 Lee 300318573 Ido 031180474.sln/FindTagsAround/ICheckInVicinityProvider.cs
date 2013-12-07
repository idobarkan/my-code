// -----------------------------------------------------------------------
// <copyright file="ITagVicinityProvider.cs" company="">
// TODO: Update copyright text.
// </copyright>
// -----------------------------------------------------------------------

namespace FindTagsAround
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using FacebookWrapper.ObjectModel;


    /// <summary>
    /// TODO: Update summary.
    /// </summary>
    public interface ICheckInVicinityProvider
    {
        Dictionary<string, Checkin> getAllUserFriendsRecentTags(User i_LoggedInUser, DateTime i_Oldest);
    }
}
