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
            this.buttonSuggestedByCheckin = new System.Windows.Forms.Button();
            this.listBoxSuggestedByCheckin = new System.Windows.Forms.ListBox();
            this.buttonSuggestedByComment = new System.Windows.Forms.Button();
            this.listBoxSuggestedByEvent = new System.Windows.Forms.ListBox();
            this.SuspendLayout();
            // 
            // listBoxSuggestedByPhotos
            // 
            this.listBoxSuggestedByPhotos.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(224)))), ((int)(((byte)(192)))));
            this.listBoxSuggestedByPhotos.FormattingEnabled = true;
            this.listBoxSuggestedByPhotos.Location = new System.Drawing.Point(26, 80);
            this.listBoxSuggestedByPhotos.Name = "listBoxSuggestedByPhotos";
            this.listBoxSuggestedByPhotos.Size = new System.Drawing.Size(177, 160);
            this.listBoxSuggestedByPhotos.TabIndex = 1;
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
            // buttonSuggestedByCheckin
            // 
            this.buttonSuggestedByCheckin.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.buttonSuggestedByCheckin.Location = new System.Drawing.Point(228, 45);
            this.buttonSuggestedByCheckin.Name = "buttonSuggestedByCheckin";
            this.buttonSuggestedByCheckin.Size = new System.Drawing.Size(177, 23);
            this.buttonSuggestedByCheckin.TabIndex = 3;
            this.buttonSuggestedByCheckin.Text = "Suggest Friends By Checkin";
            this.buttonSuggestedByCheckin.UseVisualStyleBackColor = true;
            this.buttonSuggestedByCheckin.Click += new System.EventHandler(this.buttonSuggestedByCheckin_Click);
            // 
            // listBoxSuggestedByCheckin
            // 
            this.listBoxSuggestedByCheckin.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(224)))), ((int)(((byte)(192)))));
            this.listBoxSuggestedByCheckin.FormattingEnabled = true;
            this.listBoxSuggestedByCheckin.Location = new System.Drawing.Point(228, 80);
            this.listBoxSuggestedByCheckin.Name = "listBoxSuggestedByCheckin";
            this.listBoxSuggestedByCheckin.Size = new System.Drawing.Size(177, 160);
            this.listBoxSuggestedByCheckin.TabIndex = 4;
            // 
            // buttonSuggestedByComment
            // 
            this.buttonSuggestedByComment.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.buttonSuggestedByComment.Location = new System.Drawing.Point(426, 45);
            this.buttonSuggestedByComment.Name = "buttonSuggestedByComment";
            this.buttonSuggestedByComment.Size = new System.Drawing.Size(182, 23);
            this.buttonSuggestedByComment.TabIndex = 5;
            this.buttonSuggestedByComment.Text = "Suggest Friends By Event";
            this.buttonSuggestedByComment.UseVisualStyleBackColor = true;
            // 
            // listBoxSuggestedByEvent
            // 
            this.listBoxSuggestedByEvent.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(224)))), ((int)(((byte)(192)))));
            this.listBoxSuggestedByEvent.FormattingEnabled = true;
            this.listBoxSuggestedByEvent.Location = new System.Drawing.Point(426, 80);
            this.listBoxSuggestedByEvent.Name = "listBoxSuggestedByEvent";
            this.listBoxSuggestedByEvent.Size = new System.Drawing.Size(182, 160);
            this.listBoxSuggestedByEvent.TabIndex = 6;
            // 
            // SuggestFriendsForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(698, 457);
            this.Controls.Add(this.listBoxSuggestedByEvent);
            this.Controls.Add(this.buttonSuggestedByComment);
            this.Controls.Add(this.listBoxSuggestedByCheckin);
            this.Controls.Add(this.buttonSuggestedByCheckin);
            this.Controls.Add(this.buttonSuggestByPhotos);
            this.Controls.Add(this.listBoxSuggestedByPhotos);
            this.Name = "SuggestFriendsForm";
            this.Text = "SuggestFriendsForm";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.ListBox listBoxSuggestedByPhotos;
        private System.Windows.Forms.Button buttonSuggestByPhotos;
        private System.Windows.Forms.Button buttonSuggestedByCheckin;
        private System.Windows.Forms.ListBox listBoxSuggestedByCheckin;
        private System.Windows.Forms.Button buttonSuggestedByComment;
        private System.Windows.Forms.ListBox listBoxSuggestedByEvent;
    }
}