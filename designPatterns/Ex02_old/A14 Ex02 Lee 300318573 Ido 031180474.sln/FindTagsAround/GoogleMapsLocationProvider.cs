// -----------------------------------------------------------------------
// <copyright file="GoogleMapsLocationProvider.cs" company="">
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
    using System.Net;
    using System.Xml.Linq;
    using System.Xml;
    using System.IO;
    /// <summary>
    /// TODO: Update summary.
    /// </summary>
    public class GoogleMapsLocationProvider : ILocationProvider
    {
        private string m_GoogleMapsKey = "AIzaSyBYpkC0V-CGuJX1pDC8Rr8nuF4ISACDjiE";

        public Coordinate GetLocationCoordinates(string i_LocationReference)
        {
            var responseStream = getLocationResponseStream(i_LocationReference);
            var result = getLocationFromResponseXml(responseStream);
            return result;
        }

        public List<GoogleMapsReference> GetLocationSuggestions(string userInput)
        {
            var responseStream = getSuggestionsResponseStream(userInput);
            var result = getSuggestionsFromResponseXml(responseStream);
            return result;
        }

        private Stream getLocationResponseStream(string i_LocationReference)
        {
            var requestUri = string.Format(
                "https://maps.googleapis.com/maps/api/place/details/xml?reference={0}&sensor=false&key={1}",
                Uri.EscapeDataString(i_LocationReference),
                m_GoogleMapsKey);

            return sendRequestAndGetResponseStream(requestUri);
        }

        private Stream sendRequestAndGetResponseStream(string requestUri)
        {
            var request = WebRequest.Create(requestUri);
            var response = request.GetResponse();
            return response.GetResponseStream();
        }

        private Stream getSuggestionsResponseStream(string userInput)
        {
            var requestUri = string.Format(
                "https://maps.googleapis.com/maps/api/place/autocomplete/xml?input={0}&language=en&sensor=false&key={1}",
                Uri.EscapeDataString(userInput),
                m_GoogleMapsKey);

            return sendRequestAndGetResponseStream(requestUri);
        }

        private List<GoogleMapsReference> getSuggestionsFromResponseXml(Stream xmlStream)
        {
            var xdoc = XDocument.Load(xmlStream);
            var result = new List<GoogleMapsReference>();
            foreach (var prediction in xdoc.Descendants("prediction"))
            {
                var reference = prediction.Descendants("reference").Select(x => x.Value).Single();
                var description = prediction.Descendants("description").Select(x => x.Value).Single();
                result.Add(new GoogleMapsReference(description, reference));
            }
            return result;
        }

        private Coordinate getLocationFromResponseXml(Stream xmlStream)
        {
            var xdoc = XDocument.Load(xmlStream);
            var result = new List<GoogleMapsReference>();
            XElement location = xdoc.Descendants("location").Select(x => x).Single();
            var lat = location.Descendants("lat").Select(x => x.Value).Single();
            var lng = location.Descendants("lng").Select(x => x.Value).Single();
            double parsedLat;
            double parsedLong;
            var latitudeParsed = Double.TryParse(lat, out parsedLat);
            var longtitudeParsed = Double.TryParse(lng, out parsedLong);
            if (!latitudeParsed || !longtitudeParsed)
            {
                throw new Exception("error in parsing geometry");
            }
            return new Coordinate(parsedLat, parsedLong);
        }
    }
}
