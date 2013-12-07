// -----------------------------------------------------------------------
// <copyright file="IAuthenticator.cs" company="">
// TODO: Update copyright text.
// </copyright>
// -----------------------------------------------------------------------

namespace FaceBookBackEnd
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using FacebookWrapper.ObjectModel;

    /// <summary>
    /// TODO: Update summary.
    /// </summary>
    public interface IAuthenticator
    {
        User LogIn();
    }
}
