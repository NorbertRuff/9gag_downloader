import tkinter

import customtkinter as ctk


class Header(ctk.CTkFrame):
    def __init__(self, *args, padding, **kwargs):
        super().__init__(*args, **kwargs)
        self.description_frame = ctk.CTkFrame(self)
        self.description_frame.pack(padx=padding, pady=padding, fill=tkinter.X)
        ctk.CTkLabel(self.description_frame, text="""
        This app will download all the gags you upvoted or saved on 9GAG.
        
        Request your 9GAG data from https://9gag.com/settings/privacy
        You will receive an email with a link to download your data in a html file.
        
        Select the folder where you want to save the gags and click on the Download button.
        This will create a folder named 'gags' in the selected folder and save the gags in it.
        
        Note: This app will only download the gags you upvoted or saved. It will not download the gags you commented on.
        Note: This app will not download the gags which are posts or albums. It will only download the gags which are images or videos.
        """, font=("Arial", 14)).pack(padx=padding, pady=padding)
