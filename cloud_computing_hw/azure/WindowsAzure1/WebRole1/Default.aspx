<%@ Page Title="Home Page" Language="C#" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="WebRole1._Default" %>

<asp:Content runat="server" ID="FeaturedContent" ContentPlaceHolderID="FeaturedContent">
    <form id="form1">
        <h5>Upload data file</h5>
        <asp:FileUpload id="DataFileUploadControl" runat="server" />
        <h5>Upload executable file</h5>
        <asp:FileUpload id="ExecFileUploadControl" runat="server" />
        <h5>The excecutable will be run with the data as the argument</h5>
        <asp:Button runat="server" id="DataUploadButton" text="Upload" onclick="DataUploadButton_Click" />
        <br />
        <asp:Label runat="server" id="Label1" text="Upload status: " />
    </form>
    <br /><br />
    <asp:Repeater ID="ResultsRepeater" runat="server"> 
        <ItemTemplate> 
            <%# DataBinder.Eval(Container.DataItem, "result") %>
        </ItemTemplate> 
        <SeparatorTemplate>
            <br>
        </SeparatorTemplate> 
    </asp:Repeater>

    
</asp:Content>

