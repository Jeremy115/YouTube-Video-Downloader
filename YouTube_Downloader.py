import json
from typing import Tuple
from  pytubefix import YouTube,Playlist
from tkinter import *
from pytubefix.cli import on_progress
import customtkinter
import os
import sys
import shutil
import sys


#GUI init   
root = customtkinter.CTk()


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("themes/violet.json")


root.title('Youtube Video Downloader')
root.iconbitmap('Images/YouTubeDownloader.ico')
root.geometry('1200x900')

# where to save 
SAVE_YOUTUBE_VIDEO = os.path.join(os.path.expanduser("~"), "Desktop\YouTubeDownloads\YouTubeVideos")
SAVE_YOUTUBE_PLAYLIST = os.path.join(os.path.expanduser("~"), "Desktop\YouTubeDownloads\YoutubePlaylist\\")
FILE_NAME = 'savedFileLocation/savedFolderLocations.txt'


def loadCustomVideoPath(): 
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file: 
            settings = json.load(file)
            return{
                "video_Path": settings['video_Path'] or SAVE_YOUTUBE_VIDEO,
                "playlist_Path": settings["playlist_Path"] or SAVE_YOUTUBE_PLAYLIST
            }
    else: 
        return{"video_Path": SAVE_YOUTUBE_VIDEO, "playlist_Path": SAVE_YOUTUBE_PLAYLIST}



#Video Downloader. 
def DownloadVideo(link, resolution):

    #check if po token is on. 
    if po_button_checkbox.get() == "on":
        youtube_video = YouTube(link, use_po_token=True, po_token_verifier=po_token_verifier)
    else: 
        youtube_video = YouTube(link)


    savedFilePath = loadCustomVideoPath()

    #Get video for highest Resolution.
    if resolution == "Highest Resolution Possible":
        
        try:

            
            youtube_video = youtube_video.streams.get_highest_resolution()
            print(savedFilePath["video_Path"])
            youtube_video.download(output_path=savedFilePath["video_Path"])
            show_button_for_confirmed_download()#Shows that the video is downloaded.
             
        except Exception as e: 
            errorOccuredSimplifyException(e)
            

    elif(resolution == "Lowest Resolution Possible"): 
        try:

            youtube_video = youtube_video.streams.get_lowest_resolution()
            youtube_video.download(output_path=savedFilePath["video_Path"])
            show_button_for_confirmed_download()#Shows that the video is downloaded.
             
        except Exception as e: 
            errorOccuredSimplifyException(e)

#Playlist Downloader. 
def DownloadVideoPlaylist(link, resolution): 

    #Set Counter and once flag: 
    currentLoop = 0
    flagErrorOnce = True
    video_title = ""
    #get playlist URL prior to loops.
    pl = Playlist(link)

    #Load settings.
    savedFilePath = loadCustomVideoPath()

    #Show Progress bar.
    show_progress_bar_on_screen()


    
    #User chose high res. 
    if(resolution == "Highest Resolution Possible"):
        #loop through each video in playlist and download them.  
        for playlist_url in pl.video_urls:

            try:

                currentLoop += 1

                playlist_progress_bar.set(currentLoop / len(pl.video_urls)) 
                root.update_idletasks()

                #check if PoToken is on 
                if po_button_checkbox.get() == "on":
                    youtube_playlist = YouTube(playlist_url, use_po_token=True, po_token_verifier=po_token_verifier)
                else:
                    youtube_playlist = YouTube(playlist_url)

                video_title = youtube_playlist.title
                playlist = youtube_playlist.streams.get_highest_resolution() 
                playlist.download(output_path=savedFilePath["playlist_Path"] + pl.title)


            except Exception as e:
                if flagErrorOnce == True:
                    customtkinter.CTkLabel(root, text="\n\nVideos Unable to download from playlist: \n", underline=True, font=("Roboto", 20)).pack()
                    flagErrorOnce = False
                failed_video_download_in_playlist(str(video_title), e)



    #User chose low res. 
    elif(resolution == "Lowest Resolution Possible"):
        #loop through each video in playlist and download them.     
        for playlist_url in pl.video_urls:

            try: 

                currentLoop += 1
                
                playlist_progress_bar.set(currentLoop / len(pl.video_urls)) 
                root.update_idletasks()

                #check POtoken is to be used. 
                if po_button_checkbox.get() == "on":
                    youtube_playlist = YouTube(playlist_url, use_po_token=True, po_token_verifier=po_token_verifier)
                else:
                    youtube_playlist = YouTube(playlist_url)

                video_title = youtube_playlist.title
                playlist = youtube_playlist.streams.get_lowest_resolution() 
                playlist.download(output_path=savedFilePath["playlist_Path"] + pl.title)
                

            except Exception as e:
                if flagErrorOnce == True:
                    customtkinter.CTkLabel(root, text="\n\nVideos Unable to download from playlist: \n", underline=True, font=("Roboto", 20)).pack()
                    flagErrorOnce = False
                failed_video_download_in_playlist(str(video_title), e)

    
    hide_progress_bar_on_screen()

    if(flagErrorOnce == True):
        show_button_for_confirmed_download_playlist_no_errors()
    


def failed_video_download_in_playlist(url_error, exception): 

    if url_error == "":
        url_error = "Unable To get video URL."

    download_failed_frame = customtkinter.CTkFrame(root, fg_color="transparent")
    download_failed_frame.pack(pady=10)

    download_failed_Label1 = customtkinter.CTkLabel(download_failed_frame, text=url_error , fg_color="red", font=("Roboto", 16))
    download_failed_Label1.grid(row=0, column=0)

    download_failed_Label2 = customtkinter.CTkLabel(download_failed_frame, text=errorOccuredInPLaylistDownload(exception), font=("Roboto", 16))
    download_failed_Label2.grid(row=0, column=1)

    root.update_idletasks()



def downloadClicked(): 

    hide_button_for_unconfirmed_download()
    url_label.configure(text=link_from_user.get())#gets URL
    resolution_output_label.configure(text=resolution_From_User.get())#gets resolution.

    link = url_label.cget("text")
    resolution = resolution_output_label.cget("text")

    #Testing link and resolution for code from user input. Here is where I ended for the night.
    print("Link entered: " + link)
    print("Resolution entered: "+ resolution)

    
    if "&list=" in link or "?list=" in link: 
        DownloadVideoPlaylist(link, resolution)
    elif "?v=" in link: 
        DownloadVideo(link, resolution)
    elif link == "": 
        quit
    else:
        video_or_playlist_not_found()



def errorOccuredInPLaylistDownload(e):
    error_message = f" - Error: {str(e)}"

    if"detected as a bot." in str(e).lower():
        error_message = " - Bot detection."

    return error_message + "\n"


def errorOccuredSimplifyException(e):
    error_message = f"Error: {str(e)}"

    if "detected as a bot." in str(e).lower():
        error_message = "Bot detection detected. Try again in a minute."
            
    show_button_for_unconfirmed_download(error_message)

def po_token_verifier() -> Tuple[str, str]:

    token = "MnRxh5aCq8sMYnG_GUJ0rBoldr0Qiyyls5SYew-Gk-t4uaFfTQ6yXdPCY8qZFDEwQLYpxyqrSDZbVNUfTbQOHDGd2ZxNA_wASZuFFUm0TEGTKtEItUEM78-GfGpcwXSpxztcWyiJXqRvmRb2FFuC1diYqZl4uw=="
    visitorData = "CgtJcEJvZmJ6bjg4cyipxcW8BjIKCgJVUxIEGgAgXg%3D%3D"

    return visitorData, token



#URL Text box
#########################################################################################
frame_URL = customtkinter.CTkFrame(root, fg_color="transparent")
frame_URL.pack(pady=10)




#shows YouTube Video URL message in front of textbox/entry(entry meaning user input)
text_URLMessage = customtkinter.CTkLabel(frame_URL, text="Youtube Video URL:", font=("Roboto", 24), fg_color="transparent" )
text_URLMessage.grid(row=0, column=0)

#holds URL 
url_label = customtkinter.CTkLabel(root, text="", font=("Roboto", 24))
url_label.pack_forget()

#Gets url from user. 
link_from_user = customtkinter.CTkEntry(frame_URL, 
                                        placeholder_text="Enter URL",
                                        height=50,
                                        width=500,
                                        font=("Roboto", 18),
                                        corner_radius=50,
                                        border_color="black",
                                        border_width=1)
#link_from_user.pack(pady=40)
link_from_user.grid(row=0, column=1, padx=20)
#########################################################################################






#Resolution Box
########################################################################################

frame_Resolution_Box = customtkinter.CTkFrame(root, fg_color="transparent")
frame_Resolution_Box.pack(pady=10)

text_Resolution_Box = customtkinter.CTkLabel(frame_Resolution_Box, text="Resolution:", font=("Roboto", 24), fg_color="transparent" )
text_Resolution_Box.grid(row=0, column=0)


resolutionOptions = ["Highest Resolution Possible","Lowest Resolution Possible"]

resolution_From_User = customtkinter.CTkComboBox(frame_Resolution_Box, 
                                            values=resolutionOptions,
                                            #command=downloadClicked,
                                            height=50,
                                            width=375,
                                            font=("Roboto", 18),
                                            corner_radius=50,
                                            border_color="black",
                                            border_width=1, 
                                            button_hover_color="purple", 
                                            dropdown_font=("Roboto", 18))
resolution_From_User.grid(row=0, column=1, padx=20)

resolution_output_label = customtkinter.CTkLabel(root, text="", font=("Roboto", 18))
resolution_output_label.pack_forget()
########################################################################################

frame = customtkinter.CTkFrame(root, fg_color="transparent")
frame.pack(pady=10)


#Download button
##########################################################################################    
download_button = customtkinter.CTkButton(frame, 
                        text="Download", 
                        command=downloadClicked, #runs a function. 
                        height=50,
                        width=100,
                        font=("Roboto", 24),
                        #fg_color=
                        #hover_color=
                        corner_radius=50,
                        border_color="black",
                        border_width=1
                        )
#download_button.pack(pady=90)
download_button.grid(row=0, column=0, padx=20)
############################################################################################

#Clear button. 
############################################################################################
def clearURL():
    link_from_user.delete(0, END)


clear_button = customtkinter.CTkButton(frame, 
                                        text="Clear", 
                                        command=clearURL, 
                                        height=50,
                                        width=100,
                                        font=("Roboto", 24),
                                        #fg_color=
                                        #hover_color=
                                        corner_radius=50,
                                        border_color="black",
                                        border_width=1)
#clear_button.pack(pady=90)
clear_button.grid(row=0, column=1, padx=20)
############################################################################################

#CheckBox for use po_token
############################################################################################
usePO_button = customtkinter.StringVar(value="on")
po_button_checkbox = customtkinter.CTkCheckBox(frame, text="Use PO Token", 
                                               variable=usePO_button, 
                                               onvalue="on", 
                                               offvalue="off", 
                                               font=("Roboto", 24))
po_button_checkbox.grid(row=0, column=2, padx=20)



############################################################################################
warningMessageText = customtkinter.CTkLabel(root, text=
                                            "\n\nTurning off Po Token will be faster but unreliable at times."
                                            + "\n\nIf the program freezes with the PO token on, it's still downloading — just give it time."
                                            ,font=("Roboto", 18)
                                            ,fg_color="transparent"
                                            )
warningMessageText.pack(padx=20)


warningMessage = customtkinter.CTkLabel(root, text=
                                         "\n\nSingle Video Downloads - " + str(loadCustomVideoPath()["video_Path"])
                                        + "\n\nPlaylist Downloads - " + str(loadCustomVideoPath()["playlist_Path"])
                                        , font=("Roboto", 22),
                                        fg_color="transparent" )
warningMessage.pack(padx=20)


    
def input_Custom_File_locations():

    def set_Default_File_Path():

        # Use the default constants
        video_path = SAVE_YOUTUBE_VIDEO
        playlist_path = SAVE_YOUTUBE_PLAYLIST

        # Save the default settings
        save_settings(video_path, playlist_path)

        # Update the warning message in the root window
        update_video_download_Location()
        
        #Destroy the frame. 
        new_window.destroy()
        new_window.update()

    def save_settings(video_path, playlist_path):

        #Save user settings to the JSON file.
        #settingsNew = {"video_Path": video_path, "playlist_Path": playlist_path}
        settingsOld = loadCustomVideoPath()


        settingsNew = {
            "video_Path": video_path if video_path and video_path != settingsOld.get("video_Path") else settingsOld.get("video_Path"),
            "playlist_Path": playlist_path if playlist_path and playlist_path != settingsOld.get("playlist_Path") else settingsOld.get("playlist_Path")
        }

        
        with open(FILE_NAME, 'w') as file:
            json.dump(settingsNew, file)

    #Save. 
    def on_save():

        #Get new settings.
        video_path = video_entry.get()
        playlist_path = playlist_entry.get()

        #load old settings.
        settings = loadCustomVideoPath()


        # Ensure the playlist path ends with a backslash if not empty.
        if playlist_path and not playlist_path.endswith("\\"):
            playlist_path += "\\"

        #Check to see if left blank if so then leave default. 
        if video_path == "" and settings.get("video_Path") == "": 
            video_path = SAVE_YOUTUBE_VIDEO

        if playlist_path == "" and settings.get("playlist_Path") == "":
            playlist_path = SAVE_YOUTUBE_PLAYLIST
        
        #Check if video path exists on computer. 
        if not doesFilePathExists(video_path) and video_path != '':
            error_label.configure(text="Video Path does not exists. ", font=("Roboto", 24))

        #Check if playlist path exists on computer. 
        elif not doesFilePathExists(playlist_path) and playlist_path != '': 
            error_label.configure(text="Playlist Path does not exists.", font=("Roboto", 24))

        #If both playlist or video path exists then we are good. 
        else: 
            save_settings(video_path, playlist_path)
            update_video_download_Location()
            new_window.destroy()  
            new_window.update()

    #Cancel.
    def on_cancel():
        new_window.destroy()  # Close the save popup
        new_window.update()
    
    def doesFilePathExists(file_Path):
        if os.path.exists(file_Path):
            return True
        else:
            return False

    new_window = customtkinter.CTkToplevel(root)

    new_window.title("Change Download Folders")
    new_window.geometry("750x600")
    new_window.iconbitmap('Images/YouTubeDownloader.ico')
    
    #new_window.transient(root)
    new_window.grab_set() #prevents going back to main window. 

    #TOP MESSAGE 
    #####################################################################################################
    
    label_for_message = customtkinter.CTkLabel(new_window, text="\nChange Download Folder\n\n You need to copy the full file path to the desired download location.\n",font=("Roboto", 24))
    label_for_message.pack()

    # Label for error message
    error_label = customtkinter.CTkLabel(new_window, text="", text_color="red", font=("Roboto", 14))
    error_label.pack(pady=10)

    #Show Entrys for new file paths
    #####################################################################################################

    show_video_Path_frame = customtkinter.CTkFrame(new_window,fg_color="transparent")
    show_video_Path_frame.pack(padx=20, pady=20)



    #Entry and Label video_Path
    video_entry_label = customtkinter.CTkLabel(show_video_Path_frame, text="Video Path: ", font=("Roboto", 24))
    video_entry_label.grid(row=0, column=0,padx=10, pady=10)

    video_entry = customtkinter.CTkEntry(show_video_Path_frame, 
                                        font=("Roboto", 24),
                                        height=50,
                                        width=500,
                                        corner_radius=50,
                                        border_color="black",
                                        border_width=1)
    video_entry.grid(row=0, column=1, padx=10, pady=10)


    #Entry and Label video_playlist
    playlist_entry_label = customtkinter.CTkLabel(show_video_Path_frame, text="Playlist Path: ", font=("Roboto", 24))
    playlist_entry_label.grid(row=1, column=0, padx=10, pady=10)

    playlist_entry = customtkinter.CTkEntry(show_video_Path_frame, 
                                            font=("Roboto", 24),
                                            height=50,
                                            width=500,
                                            corner_radius=50,
                                            border_color="black",
                                            border_width=1)
    playlist_entry.grid(row=1, column=1, padx=10, pady=10)



    #Save and cancel buttons.
    #####################################################################################################
    save_cancel_button_frame = customtkinter.CTkFrame(new_window,fg_color="transparent")
    save_cancel_button_frame.pack(padx=20, pady=20)

    # Add the Save button inside the frame
    save_button = customtkinter.CTkButton(save_cancel_button_frame, 
                                            text="Save", 
                                            command=on_save,
                                            width=200, 
                                            height=50,
                                            font=("Roboto", 24), 
                                            corner_radius=50,
                                            border_color="black",
                                            border_width=1)
    save_button.grid(row=0, column=0, padx=20, pady=20)

    # Add the Cancel button inside the frame
    cancel_button = customtkinter.CTkButton(save_cancel_button_frame, 
                                            text="Cancel", 
                                            command=on_cancel, 
                                            width=200, 
                                            height=50,
                                            font=("Roboto", 24), 
                                            corner_radius=50,
                                            border_color="black",
                                            border_width=1)
    cancel_button.grid(row=0, column=1, padx=20, pady=20)

    #Change Back to Default file location
    default_button = customtkinter.CTkButton(save_cancel_button_frame, 
                                            text="Set Default", 
                                            command=set_Default_File_Path, 
                                            width=200, 
                                            height=50,
                                            font=("Roboto", 24), 
                                            corner_radius=50,
                                            border_color="black",
                                            border_width=1)
    default_button.grid(row=0, column=2, padx=20, pady=20)


change_default_dir = customtkinter.CTkButton(root, 
                                            text="Change Default Downloads Folder", 
                                            command=input_Custom_File_locations, 
                                            width=300, 
                                            height=50,
                                            font=("Roboto", 24), 
                                            corner_radius=50,
                                            border_color="black",
                                            border_width=1)
change_default_dir.pack(padx=20, pady=60)


#used in input_Custom_File_locations to show file locations have been updated. 
def update_video_download_Location():
    warningMessage.configure(
        text=
        "\n\nSingle Video Downloads - " + str(loadCustomVideoPath()["video_Path"]) 
        + "\n\nPlaylist Downloads - " + str(loadCustomVideoPath()["playlist_Path"]),
        font=("Roboto", 24),
        fg_color="transparent"
    )



#Shows text which state that the download was confirmed. 
##############################################################################################
label_show_download_confirm = customtkinter.CTkLabel(root, text="Youtube Video downloaded successfully.", fg_color="green",font=("Roboto", 24))
label_show_download_issue = customtkinter.CTkLabel(root, text="No errors yet...", fg_color="red", font=("Roboto", 18) )
label_show_download_confirm_no_erros_from_playlist = customtkinter.CTkLabel(root, text="Youtube PlayList downloaded successfully.", fg_color="green",font=("Roboto", 24))
no_Video_Found_Message = customtkinter.CTkLabel(root, text="This video does not exists. Program looks for &list=(Playlist) or ?v=(Video) in URL."
                                                + "\nIf you are trying to copy and paste from the share button on the playlist. IT WILL FAIL to find the playlist."
                                                + "\n\nIMPORTANT: You CAN use a URL from a video in the playlist if you want to the get the playlist.", fg_color="red", font=("Roboto", 18) )
playlist_progress_bar = customtkinter.CTkProgressBar(root, orientation="horizontal", width=300, height=30, mode="determinate")
playlist_progress_bar.pack_forget()
playlist_progress_bar.set(0)



#Download Good:
def show_button_for_confirmed_download():
    label_show_download_confirm.pack(pady=20)
    root.after(5000, hide_button_for_confirmed_download)
   
def hide_button_for_confirmed_download():
    label_show_download_confirm.pack_forget()

def show_button_for_confirmed_download_playlist_no_errors():
    label_show_download_confirm_no_erros_from_playlist.pack(pady=20)
    root.after(5000, hide_button_for_confirmed_download_playlist_no_errors)

def hide_button_for_confirmed_download_playlist_no_errors(): 
    label_show_download_confirm_no_erros_from_playlist.pack_forget()


#Issues Downloading:
def show_button_for_unconfirmed_download(error_message):
    label_show_download_issue.configure(text=error_message)
    label_show_download_issue.pack(pady=20)

def hide_button_for_unconfirmed_download():
    label_show_download_issue.pack_forget()

def video_or_playlist_not_found(): 
    
    no_Video_Found_Message.pack(pady=20)
    root.after(8000, no_Video_Found_Message.pack_forget)


#show progress bar and hide after:
def show_progress_bar_on_screen(): 
    playlist_progress_bar.set(0)
    playlist_progress_bar.pack(pady=20)
    root.update_idletasks()
    

def hide_progress_bar_on_screen():
    root.after(2000)
    playlist_progress_bar.pack_forget()
    root.update_idletasks()



##############################################################################################




#Main Loop. 
root.mainloop()

