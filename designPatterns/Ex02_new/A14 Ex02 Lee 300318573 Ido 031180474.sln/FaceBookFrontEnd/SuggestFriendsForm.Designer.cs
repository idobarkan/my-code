namespace FaceBookFrontEnd
{
    partial class SuggestFriendsForm
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
            this.listBoxSuggestedByPhotos = new System.Windows.Forms.ListBox();
            this.buttonSuggestByPhotos = new System.Windows.Forms.Button();
            this.buttonSuggestedByEvent = new System.Windows.Forms.Button();
            this.listBoxSuggestedByEvent = new System.Windows.Forms.ListBox();
            this.labelnumOfResult = new System.Windows.Forms.Label();
            this.textBoxMaxResults = new System.Windows.Forms.TextBox();
            this.pictureBoxFriendByPhoto = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            this.pictureBoxFriendByEvent = new System.Windows.Forms.PictureBox();
            this.label2 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxFriendByPhoto)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxFriendByEvent)).BeginInit();
            this.SuspendLayout();
            // 
            // listBoxSuggestedByPhotos
            // 
            this.listBoxSuggestedByPhotos.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(224)))), ((int)(((byte)(192)))));
            this.listBoxSuggestedByPhotos.FormattingEnabled = true;
            this.listBoxSuggestedByPhotos.Location = new System.Drawing.Point(26, 91);
            this.listBoxSuggestedByPhotos.Name = "listBoxSuggestedByPhotos";
            this.listBoxSuggestedByPhotos.Size = new System.Drawing.Size(177, 160);
            this.listBoxSuggestedByPhotos.TabIndex = 1;
            this.listBoxSuggestedByPhotos.SelectedIndexChanged += new System.EventHandler(this.listBoxSuggestedByPhotos_SelectedIndexChanged);
            // 
            // buttonSuggestByPhotos
            // 
            this.buttonSuggestByPhotos.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.buttonSuggestByPhotos.Location = new System.Drawing.Point(26, 45);
            this.buttonSuggestByPhotos.Name = "buttonSuggestByPhotos";
            this.buttonSuggestByPhotos.Size = new System.Drawing.Size(177, 23);
            this.buttonSuggestByPhotos.TabIndex = 2;
            this.buttonSuggestByPhotos.Text = "Suggest Friends by Photos";
            this.buttonSuggestByPhotos.UseVisualStyleBackColor = true;
            this.buttonSuggestByPhotos.Click += new System.EventHandler(this.buttonSuggestByPhotos_Click);
            // 
            // buttonSuggestedByEvent
            // 
            this.buttonSuggestedByEvent.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.buttonSuggestedByEvent.Location = new System.Drawing.Point(387, 45);
            this.buttonSuggestedByEvent.Name = "buttonSuggestedByEvent";
            this.buttonSuggestedByEvent.Size = new System.Drawing.Size(182, 23);
            this.buttonSuggestedByEvent.TabIndex = 5;
            this.buttonSuggestedByEvent.Text = "Suggest Friends By Events";
            this.buttonSuggestedByEvent.UseVisualStyleBackColor = true;
            this.buttonSuggestedByEvent.Click += new System.EventHandler(this.buttonSuggestedByEvent_Click);
            // 
            // listBoxSuggestedByEvent
            // 
            this.listBoxSuggestedByEvent.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(224)))), ((int)(((byte)(192)))));
            this.listBoxSuggestedByEvent.FormattingEnabled = true;
            this.listBoxSuggestedByEvent.Location = new System.Drawing.Point(387, 91);
            this.listBoxSuggestedByEvent.Name = "listBoxSuggestedByEvent";
            this.listBoxSuggestedByEvent.Size = new System.Drawing.Size(182, 160);
            this.listBoxSuggestedByEvent.TabIndex = 6;
            this.listBoxSuggestedByEvent.SelectedIndexChanged += new System.EventHandler(this.listBoxSuggestedByEvent_SelectedIndexChanged);
            // 
            // labelnumOfResult
            // 
            this.labelnumOfResult.AutoSize = true;
            this.labelnumOfResult.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.labelnumOfResult.Location = new System.Drawing.Point(23, 18);
            this.labelnumOfResult.Name = "labelnumOfResult";
            this.labelnumOfResult.Size = new System.Drawing.Size(208, 13);
            this.labelnumOfResult.TabIndex = 7;
            this.labelnumOfResult.Text = "Choose maximum number of results:\r\n";
            // 
            // textBoxMaxResults
            // 
            this.textBoxMaxResults.BackColor = System.Drawing.SystemColors.Info;
            this.textBoxMaxResults.Location = new System.Drawing.Point(237, 15);
            this.textBoxMaxResults.Name = "textBoxMaxResults";
            this.textBoxMaxResults.Size = new System.Drawing.Size(76, 20);
            this.textBoxMaxResults.TabIndex = 8;
            this.textBoxMaxResults.Text = "10";
            // 
            // pictureBoxFriendByPhoto
            // 
            this.pictureBoxFriendByPhoto.Location = new System.Drawing.Point(225, 88);
            this.pictureBoxFriendByPhoto.Name = "pictureBoxFriendByPhoto";
            this.pictureBoxFriendByPhoto.Size = new System.Drawing.Size(137, 173);
            this.pictureBoxFriendByPhoto.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBoxFriendByPhoto.TabIndex = 9;
            this.pictureBoxFriendByPhoto.TabStop = false;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(23, 71);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(161, 13);
            this.label1.TabIndex = 10;
            this.label1.Text = "(Click on an user to view picture)";
            // 
            // pictureBoxFriendByEvent
            // 
            this.pictureBoxFriendByEvent.Location = new System.Drawing.Point(590, 88);
            this.pictureBoxFriendByEvent.Name = "pictureBoxFriendByEvent";
            this.pictureBoxFriendByEvent.Size = new System.Drawing.Size(137, 173);
            this.pictureBoxFriendByEvent.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBoxFriendByEvent.TabIndex = 43;
            this.pictureBoxFriendByEvent.TabStop = false;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(384, 74);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(161, 13);
            this.label2.TabIndex = 44;
            this.label2.Text = "(Click on an user to view picture)";
            // 
            // SuggestFriendsForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(739, 343);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.pictureBoxFriendByEvent);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.pictureBoxFriendByPhoto);
            this.Controls.Add(this.textBoxMaxResults);
            this.Controls.Add(this.labelnumOfResult);
            this.Controls.Add(this.listBoxSuggestedByEvent);
            this.Controls.Add(this.buttonSuggestedByEvent);
            this.Controls.Add(this.buttonSuggestByPhotos);
            this.Controls.Add(this.listBoxSuggestedByPhotos);
            this.Name = "SuggestFriendsForm";
            this.Text = "SuggestFriendsForm";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxFriendByPhoto)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxFriendByEvent)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListBox listBoxSuggestedByPhotos;
        private System.Windows.Forms.Button buttonSuggestByPhotos;
        private System.Windows.Forms.Button buttonSuggestedByEvent;
        private System.Windows.Forms.ListBox listBoxSuggestedByEvent;
        private System.Windows.Forms.Label labelnumOfResult;
        private System.Windows.Forms.TextBox textBoxMaxResults;
        private System.Windows.Forms.PictureBox pictureBoxFriendByPhoto;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.PictureBox pictureBoxFriendByEvent;
        private System.Windows.Forms.Label label2;
    }
}