// -----------------------------------------------------------------------
// <copyright file="Coordinate.cs" company="">
// TODO: Update copyright text.
// </copyright>
// -----------------------------------------------------------------------

namespace FindTagsAround
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;

    /// <summary>
    /// TODO: Update summary.
    /// </summary>
    public class Coordinate
    {
        public double Longtitude
        {
            get;
            private set;
        }

        public double Latitude
        {
            get;
            private set;
        }

        public Coordinate(double i_lattitude, double i_longtitude)
        {
            Latitude = i_lattitude;
            Longtitude = i_longtitude;
        }
    }
}
