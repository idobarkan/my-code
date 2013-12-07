using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace FindTagsAround
{
    public class GoogleMapsReference
    {
        public string Reference
        {
            get;
            private set;
        }

        public string Description
        {
            get;
            private set;
        }

        public GoogleMapsReference(string i_description, string i_reference)
        {
            Description = i_description;
            Reference = i_reference;
        }
    }
}
