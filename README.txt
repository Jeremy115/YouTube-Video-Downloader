If you want to make changes to the program with the current state you can. 
The license is MIT. You have full permission to do as you please with this code.  


A lot of the times YouTube will detect your request as a bot so may have to wait a while to download. 
Sometimes you can spam the download button and it will just eventually go through. 
I recommend downloading and not attempting to redownload the video as multple times it will be flagged and may have issues downloading other videos. 




Keep in mind that windows will see this as a virus since its not signed by windows when downloading one of the .rar or .zip folders.

In order to compile everything for non-power users, that is the solution since they wont have the dependencies installed. 


IF YOU WANT TO ALLOW WINDOWS TO INSTALL THE .rar OR .zip AND NOT FLAG IT HERE ARE THE INSTRUCTIONS: 

DO THIS AT YOUR OWN RISK.
ANYTIME YOU INSTALL SOMETHING ON THE ENTERENET IT IS A RISK!


  1. KEEP IN MIND TO TURN THIS BUTTON BACK ON SO DO NOT CLOSE THE WINDOW WHEN YOU GET HERE:
      Settings> Update and Security> Windows Security> Open Windows Security > 
      > Virus & threat protection > Virus & threat protection settings > TURN OFF REAL-TIME Protection. 

  2. Download the .rar or .zip folder located in /exeDownload/

  3. Make a folder somewhere on your computer like c:/YouTubeVideoDownloader or d:/YouTubeVideDownloader and put the .rar or .zip file in. 

  4. extract the .zip or .rar file 

  5. Go back to > Virus & threat protection settings > Exclusions (Add or remove exclusions) > Add an exclusion > file 
        Choose the file location of the newly create folder from step 3 \YouTube_Downloader
        go to the folder until you see these files: 

          _internal
          Images
          savedFileLocation
          themes
          YouTube_Downloader

        you want to choose the YouTube_Downloader file and click open at the bottom right. 


  6. TURN BACK ON REAL-TIME PROTECTION located Settings> Update and Security> Windows Security> Open Windows Security 
                > Virus & threat protection > Virus & threat protection settings > TURN ON REAL-TIME Protection.

  7. In the folder of the newly created file locate the YouTube_Downloader file(.exe) and right click it and create a shortcut and place that on your desktop for ease of access. 

  8. NOW you should be able to run the shortcut but windows may warn you about this file being a virus, while I have added nothing malicous own my ownm its your decision beyond this point. 
      TO Continue - Run anyway and now you can use the youtube downloader. You can choose file locations you wish to store the files in but default will be the desktop. 






If you are wanting to create your own exe with modifications:  

Activate environment. 
WINDOWS ONLY
source env\Scripts\activate
-Here you can add your own packages into the virtual environment. 



If you want want to extract everything into a exe. 

From the virtual environment run the auto-py-to-exe.
WARNING - if you do not use the Virtual environment then it will not work. So use the source env\Scripts\activate above. 

command: 
auto-py-to-exe



I recommend using the exeDownload folder to move everything to. 





