﻿namespace BasicFacebookFeatures.WithSingltonAppSettings
{
    partial class FacebookForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        private System.Windows.Forms.ErrorProvider distanceErrorProvider;
        private System.Windows.Forms.ErrorProvider nameErrorProvider;
        private System.Windows.Forms.ErrorProvider favoriteColorErrorProvider;
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
            this.listBoxEvents = new System.Windows.Forms.ListBox();
            this.label3 = new System.Windows.Forms.Label();
            this.textBoxStatus = new System.Windows.Forms.TextBox();
            this.buttonSetStatus = new System.Windows.Forms.Button();
            this.listBoxNewsFeed = new System.Windows.Forms.ListBox();
            this.pictureBoxEvent = new System.Windows.Forms.PictureBox();
            this.linkFriends = new System.Windows.Forms.LinkLabel();
            this.labelEvents = new System.Windows.Forms.LinkLabel();
            this.linkNewsFeed = new System.Windows.Forms.LinkLabel();
            this.FindFriendsCheckin = new System.Windows.Forms.Button();
            this.listBoxCheckins = new System.Windows.Forms.ListBox();
            this.linkLabelCheckins = new System.Windows.Forms.LinkLabel();
            this.buttonSuggestFriends = new System.Windows.Forms.Button();
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
            // listBoxEvents
            // 
            this.listBoxEvents.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.listBoxEvents.DisplayMember = "name";
            this.listBoxEvents.FormattingEnabled = true;
            this.listBoxEvents.Location = new System.Drawing.Point(270, 249);
            this.listBoxEvents.Name = "listBoxEvents";
            this.listBoxEvents.Size = new System.Drawing.Size(560, 173);
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
            this.textBoxStatus.Size = new System.Drawing.Size(925, 20);
            this.textBoxStatus.TabIndex = 45;
            // 
            // buttonSetStatus
            // 
            this.buttonSetStatus.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonSetStatus.Location = new System.Drawing.Point(1220, 12);
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
            this.listBoxNewsFeed.Size = new System.Drawing.Size(832, 156);
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
            // FindFriendsCheckin
            // 
            this.FindFriendsCheckin.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(224)))), ((int)(((byte)(224)))), ((int)(((byte)(224)))));
            this.FindFriendsCheckin.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.FindFriendsCheckin.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(192)))), ((int)(((byte)(64)))), ((int)(((byte)(0)))));
            this.FindFriendsCheckin.Location = new System.Drawing.Point(270, 449);
            this.FindFriendsCheckin.Name = "FindFriendsCheckin";
            this.FindFriendsCheckin.Size = new System.Drawing.Size(185, 23);
            this.FindFriendsCheckin.TabIndex = 50;
            this.FindFriendsCheckin.Text = "FInd friends by checkin";
            this.FindFriendsCheckin.UseVisualStyleBackColor = false;
            this.FindFriendsCheckin.Click += new System.EventHandler(this.FindFriendsCheckin_Click);
            // 
            // listBoxCheckins
            // 
            this.listBoxCheckins.FormattingEnabled = true;
            this.listBoxCheckins.Location = new System.Drawing.Point(12, 449);
            this.listBoxCheckins.Name = "listBoxCheckins";
            this.listBoxCheckins.Size = new System.Drawing.Size(252, 160);
            this.listBoxCheckins.TabIndex = 51;
            // 
            // linkLabelCheckins
            // 
            this.linkLabelCheckins.AutoSize = true;
            this.linkLabelCheckins.Location = new System.Drawing.Point(12, 433);
            this.linkLabelCheckins.Name = "linkLabelCheckins";
            this.linkLabelCheckins.Size = new System.Drawing.Size(81, 13);
            this.linkLabelCheckins.TabIndex = 52;
            this.linkLabelCheckins.TabStop = true;
            this.linkLabelCheckins.Text = "Fetch Checkins";
            this.linkLabelCheckins.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelCheckins_LinkClicked);
            // 
            // buttonSuggestFriends
            // 
            this.buttonSuggestFriends.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.buttonSuggestFriends.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(192)))), ((int)(((byte)(64)))), ((int)(((byte)(0)))));
            this.buttonSuggestFriends.Location = new System.Drawing.Point(270, 478);
            this.buttonSuggestFriends.Name = "buttonSuggestFriends";
            this.buttonSuggestFriends.Size = new System.Drawing.Size(185, 23);
            this.buttonSuggestFriends.TabIndex = 53;
            this.buttonSuggestFriends.Text = "Suggest Friends";
            this.buttonSuggestFriends.UseVisualStyleBackColor = true;
            this.buttonSuggestFriends.Click += new System.EventHandler(this.buttonSuggestFriends_Click);
            // 
            // FacebookForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1307, 649);
            this.Controls.Add(this.buttonSuggestFriends);
            this.Controls.Add(this.linkLabelCheckins);
            this.Controls.Add(this.listBoxCheckins);
            this.Controls.Add(this.FindFriendsCheckin);
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
        private System.Windows.Forms.ListBox listBoxEvents;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox textBoxStatus;
        private System.Windows.Forms.Button buttonSetStatus;
        private System.Windows.Forms.ListBox listBoxNewsFeed;
        private System.Windows.Forms.PictureBox pictureBoxEvent;
        private System.Windows.Forms.LinkLabel linkFriends;
        private System.Windows.Forms.LinkLabel labelEvents;
        private System.Windows.Forms.LinkLabel linkNewsFeed;
        private System.Windows.Forms.Button FindFriendsCheckin;
        private System.Windows.Forms.ListBox listBoxCheckins;
        private System.Windows.Forms.LinkLabel linkLabelCheckins;
        private System.Windows.Forms.Button buttonSuggestFriends;
    }
}

