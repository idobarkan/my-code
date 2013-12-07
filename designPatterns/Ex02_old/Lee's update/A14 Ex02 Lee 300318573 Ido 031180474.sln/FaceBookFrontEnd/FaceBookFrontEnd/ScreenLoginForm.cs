using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using FacebookWrapper.ObjectModel;
using FacebookWrapper;
using FaceBookBackEnd;
using FindTagsAround;
using FaceBookFrontEnd;
using BasicFacebookFeatures.WithSingltonAppSettings;

namespace FaceBookFrontEnd
{
    public partial class ScreenLoginForm : Form
    {
        private User m_LoggedInUser;
        private FacebookBackend m_FacebookEnd;

        public ScreenLoginForm()
        {
            InitializeComponent();
            m_FacebookEnd = new FacebookBackend();
        }

        private void buttonLogin_Click(object sender, EventArgs e)
        {
            Cursor.Current = Cursors.WaitCursor;
            m_LoggedInUser = m_FacebookEnd.LogIn();
            if (m_LoggedInUser != null)
            {
                this.Hide();
                
                FacebookForm facebook = new FacebookForm(m_LoggedInUser, m_FacebookEnd);
                facebook.ShowDialog();
            }
            this.Close();
        }
    }
}
