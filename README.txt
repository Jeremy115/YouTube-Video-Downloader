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


Settings> Update and Security> Windows Security> Virus & threat protection
> under Virus and threat protection settings -> Manage settings  -> under exclusions(scroll down) -> ADD OR REMOVE EXCLUSIONs




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





