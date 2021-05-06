#GEO locator online
GEO locator online is a program in Python that can read a given set of IPs, perform Geo IP and RDAP lookups, and return the data back to the user via command line or .json file.

##How to use it
- Open the console
- Go to the main folder from the app (you should see 2 folders, files and tools, and the main.py file)
- Type `python main.py`
- You are going to see a menu wil multiple options. Choose the one that you need.

###Menu options
* Load file with IP Address:
    The core function for this app, you can upload a file with IP Address on it, no need to only have that, can be mixed with text. 
    This information is used to get data like city name, language, etc. 
    It uses two sources:
    - https://app.ipapi.co/: Used to take bulk data, tha app can send multiple IP address at the same time, using a free session, so it have a limit about how many ip address it can track.
    - https://freegeoip.app/: When ipapi reaches the limit GEO locator uses freegeoip to get info one by one, this one have more capacity for free users
    Once the information is loaded from this sites it stores the data inside a sqlite database for fast searches. It detects if an IP Address already is stored to save time and resources.
    File can be upload with a custom file or for test purposes you can use the demo file that we include.
* Look for specific IP information:
    Ask for an IP Address that its already stored on the system and shows in the console the information about it. 
* Look for all IP Address information stored on cache:
    Shows the information about all the IPs stored on the database via console. 
* Export info as file .json:
    Saves the information about all the IPs stored on the database in a .json file for external uses and better visualization.
* Dump cache:
    Clean the database. WARNING: No rollback, be careful when using this one
* Exit:
    Closes the connection to the database and the GEO locator.
 
    
There is some stuff that can be optimize, here is the primary TODO stuff that i suggest to upgrade if the project continues on develop:
- Insert via console new ip address
- Remove individual IP Address
- Ask or make an automatic system about when the incoming information should be update and not ignore
- Implement Click library for more user comfort
- Buy a licence so we can send infinite ip address to ipapi, this will improve the speed of the app
- Make threads for store information, should be more quick to store information if we manage multiple threads for this one
- Better exception managing
- Include pytest (Super important!)

Any question don't hesitate in ask