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

def delete_pycache():

    try: 
        #get path of where the files are extracted. 
        #current_dir = os.path.abspath(os.getcwd())
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

    except Exception as e:
        customtkinter.CTkLabel(root, text="Exception when deleting PyCache folder: " + e , fg_color="red", font=("Roboto", 12)).pack()
        root.update_idletasks()
        base_path = os.path.abspath(".") #if error 

    pycache_path = os.path.join(base_path, 'env', 'Lib' ,'site-packages', '__pycache__')

    print("Other PATH: " + pycache_path)

    
    if os.path.exists(pycache_path): 
        shutil.rmtree(pycache_path)
        customtkinter.CTkLabel(root, text="Deleted Pycache" , fg_color="green", font=("Roboto", 12)).pack()
        root.update_idletasks()
        print(f"Deleted __pycache__ at: {pycache_path}")
    else: 
        print("__pycache__ folder not found.")
    
#call the function to remove cache folder. Issues happen if this folder does not get deleted. 
#delete_pycache()



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("themes/violet.json")


root.title('Youtube Video Downloader')
root.iconbitmap('Images/YouTubeDownloader.ico')
root.geometry('1000x800')

# where to save 
SAVE_YOUTUBE_VIDEO = os.path.join(os.path.expanduser("~"), "Desktop\YouTubeDownloads\YouTubeVideos")
SAVE_YOUTUBE_PLAYLIST = os.path.join(os.path.expanduser("~"), "Desktop\YouTubeDownloads\YoutubePlaylist\\")


#Video Downloader. 
def DownloadVideo(link, resolution):

    #check if po token is needed. 
    if po_button_checkbox.get() == "on":
        youtube_video = YouTube(link, use_po_token=True, po_token_verifier=po_token_verifier)
    else: 
        youtube_video = YouTube(link)

    #Get video for highest Resolution.
    if resolution == "Highest Resolution Possible":
        
        try:

            
            youtube_video = youtube_video.streams.get_highest_resolution()
            youtube_video.download(output_path=SAVE_YOUTUBE_VIDEO)
            show_button_for_confirmed_download()#Shows that the video is downloaded.
             
        except Exception as e: 
            errorOccuredSimplifyException(e)
            

    elif(resolution == "Lowest Resolution Possible"): 
        try:

            youtube_video = youtube_video.streams.get_lowest_resolution()
            youtube_video.download(output_path=SAVE_YOUTUBE_VIDEO)
            show_button_for_confirmed_download()#Shows that the video is downloaded.
             
        except Exception as e: 
            errorOccuredSimplifyException(e)

#Playlist Downloader. 
def DownloadVideoPlaylist(link, resolution): 

    #Set Counter and once flag: 
    currentLoop = 0
    flagErrorOnce = True

    #get playlist URL prior to loops.
    pl = Playlist(link)

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

                #check if PoToken is needed. 
                if po_button_checkbox.get() == "on":
                    youtube_playlist = YouTube(playlist_url, use_po_token=True, po_token_verifier=po_token_verifier)
                else:
                    youtube_playlist = YouTube(playlist_url)

                video_title = youtube_playlist.title
                playlist = youtube_playlist.streams.get_highest_resolution() 
                playlist.download(output_path=SAVE_YOUTUBE_PLAYLIST + pl.title)


            except Exception as e:
                if(flagErrorOnce == True):
                    customtkinter.CTkLabel(root, text="\n\nVideos Unable to download from playlist: \n", underline=True, font=("Roboto", 20)).pack()
                    flagErrorOnce == False
                failed_video_download_in_playlist(video_title, e)



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
                playlist.download(output_path=SAVE_YOUTUBE_PLAYLIST + pl.title)
                

            except Exception as e:
                if(flagErrorOnce == True):
                    customtkinter.CTkLabel(root, text="\n\nVideos Unable to download from playlist: \n", underline=True, font=("Roboto", 20)).pack()
                    flagErrorOnce == False
                failed_video_download_in_playlist(video_title, e)

    
    hide_progress_bar_on_screen()

    if(flagErrorOnce == True):
        show_button_for_confirmed_download_playlist_no_errors()
    


def failed_video_download_in_playlist(url_error, exception): 

    download_failed_frame = customtkinter.CTkFrame(root, fg_color="transparent")
    download_failed_frame.pack(padx=10)

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

    

    value = "&list="
    if value in link: 
        DownloadVideoPlaylist(link, resolution)
    else: 
        DownloadVideo(link, resolution)


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

warningMessage = customtkinter.CTkLabel(root, text="\n\n\n\nNOTE: By default your download can be found at: ~/Desktop/YouTubeDownloads"
                                        + "\n\nUpon your first attempt to download a video or playlist, it will create a folder for each."
                                        + "\n\nSingle Video Downloads - ~/Desktop/YouTubeDownloads/YouTubeVideos"
                                        + "\n\nPlaylist Downloads - ~/Desktop/YouTubeDownloads/YoutubePlaylist"
                                        
                                         , font=("Roboto", 18),
                                           fg_color="transparent" )
warningMessage.pack(padx=20)





#Shows text which state that the download was confirmed. 
##############################################################################################
label_show_download_confirm = customtkinter.CTkLabel(root, text="Youtube Video downloaded successfully.", fg_color="green",font=("Roboto", 24))
label_show_download_issue = customtkinter.CTkLabel(root, text="No errors yet...", fg_color="red", font=("Roboto", 18) )
label_show_download_confirm_no_erros_from_playlist = customtkinter.CTkLabel(root, text="Youtube PlayList downloaded successfully.", fg_color="green",font=("Roboto", 24))
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

