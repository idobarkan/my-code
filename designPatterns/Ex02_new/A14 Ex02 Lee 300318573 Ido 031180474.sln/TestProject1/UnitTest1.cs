using System;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using FindTagsAround;
using FaceBookBackEnd;
using FacebookWrapper.ObjectModel;

namespace TestProject1
{
    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void TestGoogleMapsLocationProvider()
        {
            var locationPrvdr = new GoogleMapsLocationProvider();
            Assert.IsTrue(locationPrvdr.GetLocationSuggestions("hanadiv 79").Count > 1);
            var myHomeAddressSuggestions = locationPrvdr.GetLocationSuggestions("hanadiv 79, Pardes Hanna");
            Assert.IsTrue(myHomeAddressSuggestions.Count == 1);
            var res3 = locationPrvdr.GetLocationSuggestions("lkahfea34r3rfmj!");
            Assert.IsTrue(locationPrvdr.GetLocationSuggestions("lkahfea34r3rfmj!").Count == 0);
            var myHomeCoordinates = locationPrvdr.GetLocationCoordinates(myHomeAddressSuggestions[0].Reference);
            Assert.IsTrue(myHomeCoordinates.Latitude > 0);
            Assert.IsTrue(myHomeCoordinates.Longtitude > 0);
        }

        [TestMethod]
        public void distanceComputer()
        {
            var distanceComputer = new GeographicalDistanceComputer();
            // should be around 1500 meter apart
            var addr1Coordinates = new Coordinate(32.4652928, 34.9826545);
            var addr2Coordinates = new Coordinate(32.4770009, 34.9756979);
            Assert.IsFalse(distanceComputer.IsNear(addr1Coordinates, 1000, addr2Coordinates));
            Assert.IsTrue(distanceComputer.IsNear(addr1Coordinates, 2000, addr2Coordinates));
        }

        [TestMethod]
        public void TestgetAllUserFriendsRecentTags()
        {
            // --- run only in DEBUG since the login is interactive ---
            var fbVicinityProv = new FacebookCheckInVicinityProvider();
            var fbBackend = new FacebookBackend();
            var user = fbBackend.LogIn();
            var longTimeAgo = DateTime.MinValue;
            var recentTags = fbVicinityProv.getAllUserFriendsRecentTags(user, longTimeAgo, "CreatedTime", 5);
            Assert.IsTrue(recentTags.Count > 10);
        }

        [TestMethod]
        public void TestUsersSuggestions()
        {
            // --- run only in DEBUG since the login is interactive ---
            var fbBackend = new FacebookBackend();
            var user = fbBackend.LogIn();
            var recentTags = fbBackend.GetSuggestions<Checkin, int>(
                eRecommendationSource.Checkins,
                user, 
                10, 
                (Checkin c) => c.Comments.Count);
        }
    }
}
