
namespace FindTagsAround
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;

    public class GeographicalDistanceComputer : IDistanceComputer
    {
        public bool IsNear(Coordinate i_Center, double i_RadiusMeters, Coordinate i_TagLocation)
        {
            var d = distanceMeters(
                i_Center.Latitude, 
                i_Center.Longtitude,
                i_TagLocation.Latitude, 
                i_TagLocation.Longtitude);
            return d < i_RadiusMeters;
        }

        private double distanceMeters(double lat1, double lon1, double lat2, double lon2)
        {
            var R = 6371; // km
            var dLat = deg2rad(lat2 - lat1);
            var dLon = deg2rad(lon2 - lon1);
            var lat1rad = deg2rad(lat1);
            var lat2rad = deg2rad(lat2);

            var a = Math.Sin(dLat / 2) * Math.Sin(dLat / 2) +
                    Math.Sin(dLon / 2) * Math.Sin(dLon / 2) * Math.Cos(lat1rad) * Math.Cos(lat2rad);
            var c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));
            return R * c * 1000;
        }

        private double deg2rad(double I_Deg) 
        {
            return (I_Deg * Math.PI / 180.0);
        }
    }
}
