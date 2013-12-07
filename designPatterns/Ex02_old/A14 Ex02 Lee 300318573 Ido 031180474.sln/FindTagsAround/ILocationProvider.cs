
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
    public interface ILocationProvider
    {
        Coordinate GetLocationCoordinates(string i_googleMapsReference);
        List<GoogleMapsReference> GetLocationSuggestions(string userInput);
    }
}
