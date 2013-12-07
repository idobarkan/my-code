namespace BasicFacebookFeatures.WithSingltonAppSettings
{
    partial class FacebookForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pictureBoxFriend = new System.Windows.Forms.PictureBox();
            this.picture_smallPictureBox = new System.Windows.Forms.PictureBox();
            this.listBoxFriends = new System.Windows.Forms.ListBox();
            this.buttonLogin = new System.Windows.Forms.Button();
            this.listBoxEvents = new System.Windows.Forms.ListBox();
            this.label3 = new System.Windows.Forms.Label();
            this.textBoxStatus = new System.Windows.Forms.TextBox();
            this.buttonSetStatus = new System.Windows.Forms.Button();
            this.listBoxNewsFeed = new System.Windows.Forms.ListBox();
            this.pictureBoxEvent = new System.Windows.Forms.PictureBox();
            this.linkFriends = new System.Windows.Forms.LinkLabel();
            this.labelEvents = new System.Windows.Forms.LinkLabel();
            this.linkNewsFeed = new System.Windows.Forms.LinkLabel();
            this.listBoxCheckinByPlace = new System.Windows.Forms.ListBox();
            this.insertLocationLbl = new System.Windows.Forms.Label();
            this.textBoxLocation = new System.Windows.Forms.TextBox();
            this.ButtonMyLocation = new System.Windows.Forms.Button();
            this.dateTimePickerUser = new System.Windows.Forms.DateTimePicker();
            this.textBoxDistance = new System.Windows.Forms.TextBox();
            this.chooseDateLbl = new System.Windows.Forms.Label();
            this.chooseDistanceLbl = new System.Windows.Forms.Label();
            this.listBoxAddressSuggestion = new System.Windows.Forms.ListBox();
            this.linkLabelComments = new System.Windows.Forms.LinkLabel();
            this.linkLabelLikes = new System.Windows.Forms.LinkLabel();
            this.listBoxViewCheckinComments = new System.Windows.Forms.ListBox();
            this.listBoxViewCheckinLikes = new System.Windows.Forms.ListBox();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxFriend)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.picture_smallPictureBox)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxEvent)).BeginInit();
            this.SuspendLayout();
            // 
            // pictureBoxFriend
            // 
            this.pictureBoxFriend.Location = new System.Drawing.Point(127, 248);
            this.pictureBoxFriend.Name = "pictureBoxFriend";
            this.pictureBoxFriend.Size = new System.Drawing.Size(137, 173);
            this.pictureBoxFriend.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBoxFriend.TabIndex = 42;
            this.pictureBoxFriend.TabStop = false;
            // 
            // picture_smallPictureBox
            // 
            this.picture_smallPictureBox.Location = new System.Drawing.Point(12, 57);
            this.picture_smallPictureBox.Name = "picture_smallPictureBox";
            this.picture_smallPictureBox.Size = new System.Drawing.Size(200, 156);
            this.picture_smallPictureBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.picture_smallPictureBox.TabIndex = 41;
            this.picture_smallPictureBox.TabStop = false;
            // 
            // listBoxFriends
            // 
            this.listBoxFriends.FormattingEnabled = true;
            this.listBoxFriends.Location = new System.Drawing.Point(12, 248);
            this.listBoxFriends.Name = "listBoxFriends";
            this.listBoxFriends.Size = new System.Drawing.Size(200, 173);
            this.listBoxFriends.TabIndex = 37;
            this.listBoxFriends.SelectedIndexChanged += new System.EventHandler(this.listBoxFriends_SelectedIndexChanged);
            // 
            // buttonLogin
            // 
            this.buttonLogin.Location = new System.Drawing.Point(12, 12);
            this.buttonLogin.Name = "buttonLogin";
            this.buttonLogin.Size = new System.Drawing.Size(75, 23);
            this.buttonLogin.TabIndex = 36;
            this.buttonLogin.Text = "Login";
            this.buttonLogin.UseVisualStyleBackColor = true;
            this.buttonLogin.Click += new System.EventHandler(this.buttonLogin_Click);
            // 
            // listBoxEvents
            // 
            this.listBoxEvents.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.listBoxEvents.DisplayMember = "name";
            this.listBoxEvents.FormattingEnabled = true;
            this.listBoxEvents.Location = new System.Drawing.Point(270, 249);
            this.listBoxEvents.Name = "listBoxEvents";
            this.listBoxEvents.Size = new System.Drawing.Size(552, 173);
            this.listBoxEvents.TabIndex = 40;
            this.listBoxEvents.SelectedIndexChanged += new System.EventHandler(this.listBoxEvents_SelectedIndexChanged);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(219, 17);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(64, 13);
            this.label3.TabIndex = 44;
            this.label3.Text = "Post Status:";
            // 
            // textBoxStatus
            // 
            this.textBoxStatus.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.textBoxStatus.Location = new System.Drawing.Point(289, 14);
            this.textBoxStatus.Name = "textBoxStatus";
            this.textBoxStatus.Size = new System.Drawing.Size(632, 20);
            this.textBoxStatus.TabIndex = 45;
            // 
            // buttonSetStatus
            // 
            this.buttonSetStatus.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonSetStatus.Location = new System.Drawing.Point(927, 12);
            this.buttonSetStatus.Name = "buttonSetStatus";
            this.buttonSetStatus.Size = new System.Drawing.Size(75, 23);
            this.buttonSetStatus.TabIndex = 46;
            this.buttonSetStatus.Text = "Post";
            this.buttonSetStatus.UseVisualStyleBackColor = true;
            this.buttonSetStatus.Click += new System.EventHandler(this.buttonSetStatus_Click);
            // 
            // listBoxNewsFeed
            // 
            this.listBoxNewsFeed.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.listBoxNewsFeed.DisplayMember = "name";
            this.listBoxNewsFeed.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listBoxNewsFeed.FormattingEnabled = true;
            this.listBoxNewsFeed.ItemHeight = 19;
            this.listBoxNewsFeed.Location = new System.Drawing.Point(222, 57);
            this.listBoxNewsFeed.Name = "listBoxNewsFeed";
            this.listBoxNewsFeed.Size = new System.Drawing.Size(539, 156);
            this.listBoxNewsFeed.TabIndex = 40;
            // 
            // pictureBoxEvent
            // 
            this.pictureBoxEvent.Location = new System.Drawing.Point(670, 248);
            this.pictureBoxEvent.Name = "pictureBoxEvent";
            this.pictureBoxEvent.Size = new System.Drawing.Size(160, 173);
            this.pictureBoxEvent.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBoxEvent.TabIndex = 42;
            this.pictureBoxEvent.TabStop = false;
            // 
            // linkFriends
            // 
            this.linkFriends.AutoSize = true;
            this.linkFriends.LinkArea = new System.Windows.Forms.LinkArea(0, 13);
            this.linkFriends.Location = new System.Drawing.Point(12, 216);
            this.linkFriends.Name = "linkFriends";
            this.linkFriends.Size = new System.Drawing.Size(185, 30);
            this.linkFriends.TabIndex = 47;
            this.linkFriends.TabStop = true;
            this.linkFriends.Text = "Fetch Friends \r\n(Click on a friend to view it\'s picture)";
            this.linkFriends.UseCompatibleTextRendering = true;
            this.linkFriends.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkFriends_LinkClicked);
            // 
            // labelEvents
            // 
            this.labelEvents.AutoSize = true;
            this.labelEvents.LinkArea = new System.Windows.Forms.LinkArea(0, 13);
            this.labelEvents.Location = new System.Drawing.Point(284, 216);
            this.labelEvents.Name = "labelEvents";
            this.labelEvents.Size = new System.Drawing.Size(190, 30);
            this.labelEvents.TabIndex = 48;
            this.labelEvents.TabStop = true;
            this.labelEvents.Text = "Fetch Events \r\n(Click on an event to view it\'s picture)";
            this.labelEvents.UseCompatibleTextRendering = true;
            this.labelEvents.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.labelEvents_LinkClicked);
            // 
            // linkNewsFeed
            // 
            this.linkNewsFeed.AutoSize = true;
            this.linkNewsFeed.Location = new System.Drawing.Point(219, 41);
            this.linkNewsFeed.Name = "linkNewsFeed";
            this.linkNewsFeed.Size = new System.Drawing.Size(91, 13);
            this.linkNewsFeed.TabIndex = 49;
            this.linkNewsFeed.TabStop = true;
            this.linkNewsFeed.Text = "Fetch News Feed";
            this.linkNewsFeed.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkNewsFeed_LinkClicked);
            // 
            // listBoxCheckinByPlace
            // 
            this.listBoxCheckinByPlace.BackColor = System.Drawing.Color.Orange;
            this.listBoxCheckinByPlace.FormattingEnabled = true;
            this.listBoxCheckinByPlace.Location = new System.Drawing.Point(5, 553);
            this.listBoxCheckinByPlace.Name = "listBoxCheckinByPlace";
            this.listBoxCheckinByPlace.Size = new System.Drawing.Size(412, 147);
            this.listBoxCheckinByPlace.TabIndex = 51;
            this.listBoxCheckinByPlace.Visible = false;
            this.listBoxCheckinByPlace.SelectedIndexChanged += new System.EventHandler(this.listBoxCheckinByPlace_SelectedIndexChanged);
            // 
            // insertLocationLbl
            // 
            this.insertLocationLbl.AutoSize = true;
            this.insertLocationLbl.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.insertLocationLbl.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.insertLocationLbl.Location = new System.Drawing.Point(9, 446);
            this.insertLocationLbl.Name = "insertLocationLbl";
            this.insertLocationLbl.Size = new System.Drawing.Size(92, 13);
            this.insertLocationLbl.TabIndex = 53;
            this.insertLocationLbl.Text = "Insert location:";
            // 
            // textBoxLocation
            // 
            this.textBoxLocation.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.textBoxLocation.Location = new System.Drawing.Point(127, 446);
            this.textBoxLocation.Name = "textBoxLocation";
            this.textBoxLocation.Size = new System.Drawing.Size(185, 20);
            this.textBoxLocation.TabIndex = 54;
            this.textBoxLocation.Text = "location";
            // 
            // ButtonMyLocation
            // 
            this.ButtonMyLocation.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(192)))), ((int)(((byte)(128)))));
            this.ButtonMyLocation.Font = new System.Drawing.Font("Microsoft Sans Serif", 15.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.ButtonMyLocation.ForeColor = System.Drawing.SystemColors.InactiveCaptionText;
            this.ButtonMyLocation.Location = new System.Drawing.Point(338, 446);
            this.ButtonMyLocation.Name = "ButtonMyLocation";
            this.ButtonMyLocation.Size = new System.Drawing.Size(79, 80);
            this.ButtonMyLocation.TabIndex = 55;
            this.ButtonMyLocation.Text = "Gooo";
            this.ButtonMyLocation.UseVisualStyleBackColor = false;
            this.ButtonMyLocation.Click += new System.EventHandler(this.ButtonMyLocation_Click);
            // 
            // dateTimePickerUser
            // 
            this.dateTimePickerUser.Location = new System.Drawing.Point(107, 472);
            this.dateTimePickerUser.Name = "dateTimePickerUser";
            this.dateTimePickerUser.Size = new System.Drawing.Size(200, 20);
            this.dateTimePickerUser.TabIndex = 56;
            // 
            // textBoxDistance
            // 
            this.textBoxDistance.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.textBoxDistance.Location = new System.Drawing.Point(210, 501);
            this.textBoxDistance.Name = "textBoxDistance";
            this.textBoxDistance.Size = new System.Drawing.Size(100, 20);
            this.textBoxDistance.TabIndex = 57;
            this.textBoxDistance.Text = "2000";
            // 
            // chooseDateLbl
            // 
            this.chooseDateLbl.AutoSize = true;
            this.chooseDateLbl.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.chooseDateLbl.Location = new System.Drawing.Point(12, 472);
            this.chooseDateLbl.Name = "chooseDateLbl";
            this.chooseDateLbl.Size = new System.Drawing.Size(78, 13);
            this.chooseDateLbl.TabIndex = 58;
            this.chooseDateLbl.Text = "Choose date";
            // 
            // chooseDistanceLbl
            // 
            this.chooseDistanceLbl.AutoSize = true;
            this.chooseDistanceLbl.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.chooseDistanceLbl.Location = new System.Drawing.Point(9, 501);
            this.chooseDistanceLbl.Name = "chooseDistanceLbl";
            this.chooseDistanceLbl.Size = new System.Drawing.Size(169, 13);
            this.chooseDistanceLbl.TabIndex = 59;
            this.chooseDistanceLbl.Text = "Choose distance: (in Meters)";
            // 
            // listBoxAddressSuggestion
            // 
            this.listBoxAddressSuggestion.BackColor = System.Drawing.Color.Orange;
            this.listBoxAddressSuggestion.ForeColor = System.Drawing.Color.Black;
            this.listBoxAddressSuggestion.FormattingEnabled = true;
            this.listBoxAddressSuggestion.Location = new System.Drawing.Point(5, 527);
            this.listBoxAddressSuggestion.Name = "listBoxAddressSuggestion";
            this.listBoxAddressSuggestion.Size = new System.Drawing.Size(412, 121);
            this.listBoxAddressSuggestion.TabIndex = 60;
            this.listBoxAddressSuggestion.Visible = false;
            this.listBoxAddressSuggestion.SelectedIndexChanged += new System.EventHandler(this.listBoxAddressSuggestion_SelectedIndexChanged);
            // 
            // linkLabelComments
            // 
            this.linkLabelComments.AutoSize = true;
            this.linkLabelComments.Location = new System.Drawing.Point(423, 513);
            this.linkLabelComments.Name = "linkLabelComments";
            this.linkLabelComments.Size = new System.Drawing.Size(123, 13);
            this.linkLabelComments.TabIndex = 61;
            this.linkLabelComments.TabStop = true;
            this.linkLabelComments.Text = "View checkin Comments";
            this.linkLabelComments.Visible = false;
            this.linkLabelComments.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelComments_LinkClicked);
            // 
            // linkLabelLikes
            // 
            this.linkLabelLikes.AutoSize = true;
            this.linkLabelLikes.Location = new System.Drawing.Point(787, 508);
            this.linkLabelLikes.Name = "linkLabelLikes";
            this.linkLabelLikes.Size = new System.Drawing.Size(100, 13);
            this.linkLabelLikes.TabIndex = 62;
            this.linkLabelLikes.TabStop = true;
            this.linkLabelLikes.Text = "View Checkin Likes";
            this.linkLabelLikes.Visible = false;
            this.linkLabelLikes.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelLikes_LinkClicked);
            // 
            // listBoxViewCheckinComments
            // 
            this.listBoxViewCheckinComments.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(255)))), ((int)(((byte)(192)))));
            this.listBoxViewCheckinComments.FormattingEnabled = true;
            this.listBoxViewCheckinComments.Location = new System.Drawing.Point(423, 532);
            this.listBoxViewCheckinComments.Name = "listBoxViewCheckinComments";
            this.listBoxViewCheckinComments.Size = new System.Drawing.Size(338, 121);
            this.listBoxViewCheckinComments.TabIndex = 63;
            this.listBoxViewCheckinComments.Visible = false;
            this.listBoxViewCheckinComments.SelectedIndexChanged += new System.EventHandler(this.listBoxViewCheckinComments_SelectedIndexChanged);
            // 
            // listBoxViewCheckinLikes
            // 
            this.listBoxViewCheckinLikes.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(255)))), ((int)(((byte)(192)))));
            this.listBoxViewCheckinLikes.FormattingEnabled = true;
            this.listBoxViewCheckinLikes.Location = new System.Drawing.Point(790, 532);
            this.listBoxViewCheckinLikes.Name = "listBoxViewCheckinLikes";
            this.listBoxViewCheckinLikes.Size = new System.Drawing.Size(212, 121);
            this.listBoxViewCheckinLikes.TabIndex = 64;
            this.listBoxViewCheckinLikes.Visible = false;
            this.listBoxViewCheckinLikes.SelectedIndexChanged += new System.EventHandler(this.listBoxViewCheckinLikes_SelectedIndexChanged);
            // 
            // FacebookForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1014, 649);
            this.Controls.Add(this.listBoxViewCheckinLikes);
            this.Controls.Add(this.listBoxViewCheckinComments);
            this.Controls.Add(this.linkLabelLikes);
            this.Controls.Add(this.linkLabelComments);
            this.Controls.Add(this.listBoxAddressSuggestion);
            this.Controls.Add(this.chooseDistanceLbl);
            this.Controls.Add(this.chooseDateLbl);
            this.Controls.Add(this.textBoxDistance);
            this.Controls.Add(this.dateTimePickerUser);
            this.Controls.Add(this.ButtonMyLocation);
            this.Controls.Add(this.textBoxLocation);
            this.Controls.Add(this.insertLocationLbl);
            this.Controls.Add(this.listBoxCheckinByPlace);
            this.Controls.Add(this.linkNewsFeed);
            this.Controls.Add(this.labelEvents);
            this.Controls.Add(this.linkFriends);
            this.Controls.Add(this.buttonSetStatus);
            this.Controls.Add(this.textBoxStatus);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.pictureBoxEvent);
            this.Controls.Add(this.pictureBoxFriend);
            this.Controls.Add(this.picture_smallPictureBox);
            this.Controls.Add(this.listBoxNewsFeed);
            this.Controls.Add(this.listBoxEvents);
            this.Controls.Add(this.listBoxFriends);
            this.Controls.Add(this.buttonLogin);
            this.Name = "FacebookForm";
            this.Text = "Welcom to Facebook";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxFriend)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.picture_smallPictureBox)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxEvent)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureBoxFriend;
        private System.Windows.Forms.PictureBox picture_smallPictureBox;
        private System.Windows.Forms.ListBox listBoxFriends;
        private System.Windows.Forms.Button buttonLogin;
        private System.Windows.Forms.ListBox listBoxEvents;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox textBoxStatus;
        private System.Windows.Forms.Button buttonSetStatus;
        private System.Windows.Forms.ListBox listBoxNewsFeed;
        private System.Windows.Forms.PictureBox pictureBoxEvent;
        private System.Windows.Forms.LinkLabel linkFriends;
        private System.Windows.Forms.LinkLabel labelEvents;
        private System.Windows.Forms.LinkLabel linkNewsFeed;
        private System.Windows.Forms.ListBox listBoxCheckinByPlace;
        private System.Windows.Forms.Label insertLocationLbl;
        private System.Windows.Forms.TextBox textBoxLocation;
        private System.Windows.Forms.Button ButtonMyLocation;
        private System.Windows.Forms.DateTimePicker dateTimePickerUser;
        private System.Windows.Forms.TextBox textBoxDistance;
        private System.Windows.Forms.Label chooseDateLbl;
        private System.Windows.Forms.Label chooseDistanceLbl;
        private System.Windows.Forms.ListBox listBoxAddressSuggestion;
        private System.Windows.Forms.LinkLabel linkLabelComments;
        private System.Windows.Forms.LinkLabel linkLabelLikes;
        private System.Windows.Forms.ListBox listBoxViewCheckinComments;
        private System.Windows.Forms.ListBox listBoxViewCheckinLikes;
    }
}

