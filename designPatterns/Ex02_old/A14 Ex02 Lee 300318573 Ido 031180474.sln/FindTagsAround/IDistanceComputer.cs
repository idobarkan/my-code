// -----------------------------------------------------------------------
// <copyright file="IDistaceComputer.cs" company="">
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
    public interface IDistanceComputer
    {
        bool IsNear(Coordinate i_Center, double i_RadiusMeters, Coordinate i_TagLocation);
    }
}
