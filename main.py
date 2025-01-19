from  pytubefix import YouTube,Playlist
from tkinter import *
from pytubefix.cli import on_progress
import customtkinter
import os


#import env


#GUI CODE    
root = customtkinter.CTk()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("themes/violet.json")


root.title('Youtube Video Downloader')
root.iconbitmap('images')
root.geometry('1000x800')

# where to save 
SAVE_YOUTUBE_VIDEO = os.path.join(os.path.expanduser("~"), "Desktop\YouTubeDownloads\YouTubeVideos")
SAVE_YOUTUBE_PLAYLIST = os.path.join(os.path.expanduser("~"), "Desktop\YouTubeDownloads\YoutubePlaylist\\")





#Video Downloader. 
def DownloadVideo(link, resolution):


    #Get the youtube link 
    youtube_video = YouTube(link)

    #IDC anymore about this shit. fuck your optimization bitch
    if resolution == "Highest Resolution":
        
        try:

            youtube_video = youtube_video.streams.get_highest_resolution()
            youtube_video.download(output_path=SAVE_YOUTUBE_VIDEO)
            show_button_for_confirmed_download()#Shows that the video is downloaded.
             
        except Exception as e: 
            errorOccuredSimplifyException(e)
            

    elif(resolution == "Lowest Resolution"): 
        try:

            youtube_video = youtube_video.streams.get_lowest_resolution()
            youtube_video.download(output_path=SAVE_YOUTUBE_VIDEO)
            show_button_for_confirmed_download()#Shows that the video is downloaded.
             
        except Exception as e: 
            errorOccuredSimplifyException(e)




    """    
    elif resolution == "1080p": 
            
        try:

            youtube_video = youtube_video.streams.filter(res="1080p").first()
            youtube_video.download(output_path=SAVE_YOUTUBE_VIDEO)
            print("YouTube video has been downloaded in 1080p")

        except Exception as e: 
            print("Download Failed: " + e)
    elif resolution == "720p":


        youtube_video = youtube_video.streams.filter(res="720p").first()
        youtube_video.download(output_path=SAVE_YOUTUBE_VIDEO)
        print("YouTube video has been downloaded in 720p")
    elif resolution == "480p":


        youtube_video = youtube_video.streams.filter(res="480p").first()
        youtube_video.download(output_path=SAVE_YOUTUBE_VIDEO)
        print("YouTube video has been downloaded in 480p")
    else: 
        print("Resolution does not exist for this video: " + link)

    """




#Playlist Downloader. 
def DownloadVideoPlaylist(link, resolution): 

    print(link)
    print(resolution)

    i = 0
    try:
        pl = Playlist(link)
        for playlist_url in pl.video_urls:
            i = i + 1
            youtube_playlist = YouTube(playlist_url)
            playlist = youtube_playlist.streams.get_highest_resolution() #.filter(progressive=True, file_extension='mp4', res='720p').first()
            playlist.download(output_path=SAVE_YOUTUBE_PLAYLIST + pl.title)
            print(f'Video: {len(pl)} / ' + str(i))
            
        print("Youtube playlist has been downloaded")

    except Exception as e:
        print("Download Failed! \\n:" + e)


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


def errorOccuredSimplifyException(e):
    error_message = f"Error: {str(e)}"

    if "detected as a bot." in str(e).lower():
        error_message = "Bot detection detected. Try again in a minute."
            
    show_button_for_unconfirmed_download(error_message)

    


#UI STUFF BELOW. 





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
                                        font=("Roboto", 24),
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


resolutionOptions = ["Highest Resolution","Lowest Resolution"]

resolution_From_User = customtkinter.CTkComboBox(frame_Resolution_Box, 
                                            values=resolutionOptions,
                                            #command=downloadClicked,
                                            height=50,
                                            width=300,
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
download_button.grid(row=0, column=0)
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




warningMessage = customtkinter.CTkLabel(root, text="WARNING: If you download a playlist. It will take the highest possible resolution for" 
                                        + " each video.\n\nThe downloader is not stuck but give it time to download if "
                                        + "nothing happens after you click.\n\n\n\nYour download can be found at your Desktop/YouTubeDownloads"
                                        + "\nIt will create two folders once you download a video or playlist upon your first download."
                                        
                                         , font=("Roboto", 18),
                                           fg_color="transparent" )
warningMessage.pack(padx=20)







#Downloading in progress text.  
############################################################################################
#puts a placeholder on screen invisible till clicked. 
 



#Shows text which state that the download was confirmed. 
##############################################################################################
label_show_download_confirm = customtkinter.CTkLabel(root, text="Youtube Video downloaded successfully.", fg_color="green",font=("Roboto", 24))
label_show_download_issue = customtkinter.CTkLabel(root, text="No errors yet...", fg_color="red", font=("Roboto", 18) )

#Download Good
def show_button_for_confirmed_download():
    label_show_download_confirm.pack(pady=20)
    root.after(5000, hide_button_for_confirmed_download)
   
def hide_button_for_confirmed_download():
    label_show_download_confirm.pack_forget()


#Issue Downloading
def show_button_for_unconfirmed_download(error_message):
    label_show_download_issue.configure(text=error_message)
    label_show_download_issue.pack(pady=20)


def hide_button_for_unconfirmed_download():
    label_show_download_issue.pack_forget()

##############################################################################################
    

#Main Loop. 
root.mainloop()

