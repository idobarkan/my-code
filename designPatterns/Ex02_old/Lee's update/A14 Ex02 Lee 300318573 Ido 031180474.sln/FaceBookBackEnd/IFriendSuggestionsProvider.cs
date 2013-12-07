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
        List<User> GetSuggestions(eRecommendationSource i_Source, User i_LoggedInUser, eRecommendationSortKey i_sortBy, int i_MaxResults);
        List<User> GetSuggestions2<T, TKey>(eRecommendationSource i_Source, User i_LoggedInUser, int i_MaxResults, Func<T, TKey> i_OrderByFunc);
    }
}
