// ------------------------------------------------------------------------

namespace FaceBookBackEnd
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using FacebookWrapper.ObjectModel;

    /// <summary>
    public interface IFriendSuggestionsProvider
    {
        List<User> GetSuggestions(string i_Source, User i_LoggedInUser, string i_sortBy, int i_MaxResults);
    }
}
