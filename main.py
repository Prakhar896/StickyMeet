# Zoom Meeting ID and password saving system ***
import os, sys, subprocess
import tkinter as tk
from tkinter import filedialog, Text
import time
import json

print('Welcome to StickyMeet! What would you like to do today?')

meetings = {}
if os.path.isfile('meetings.txt'):
    meetings = json.load(open("meetings.txt"))
else:
    f = open("meetings.txt", "w")
    json.dump({ "sample": "sample" }, f)
    f.close()
    meetings = {}

settings = {}
if os.path.isfile('settings.txt'):
    settings = json.load(open("settings.txt"))
else:
    f = open("settings.txt", "w")
    json.dump({ "linkGeneratorEnabled": "false" }, f)
    f.close()
    settings = { "linkGeneratorEnabled": "false" }

try:
    if meetings['sample'] != None:
        meetings.pop('sample')
except:
    print('')

## Data Format:
## json
## Data Fields:
##  .type (Meeting type, for example z=Zoom Cloud Meetings, gm=Google Meet, t=Microsoft Teams, o=Others)
##  .id (Meeting ID)
##  .link [OPTIONAL]
##  .pwd [OPTIONAL]
##  .name

def printSpace():
    print(' ')
    
def validationCheck(givenString):
    if givenString == '':
        return False
    return True

def copy2clip(txt):
    if sys.platform == 'win32':
        cmd='echo '+txt.strip()+'|clip'
        return subprocess.check_call(cmd, shell=True)
    else:
        cmd='echo '+txt.strip()+'|pbcopy'
        return subprocess.check_call(cmd, shell=True)
    
def restartApp():
    if not ("idlelib" in sys.modules):
        printSpace()
        if sys.platform == 'win32':
            cmd = 'python main.py'
            subprocess.check_call(cmd, shell=True)
            exit()
        else:
            cmd = 'python3 main.py'
            subprocess.check_call(cmd, shell=True)
            exit()
    else:
        printSpace()
        print('Sorry, a critical system update required StickyMeet to restart but StickyMeet seems to be running on IDLE and hence cannot restart itself.')
        printSpace()
        print('You will have to manually start up StickyMeet. \nOn IDLE, click File > Open and select the `main.py` file. \nThen click Run > Run Module to start up StickyMeet.')
        time.sleep(4)
        print('Terminating app for manual restart...')
        exit()

printSpace()

def addMeeting():
    printSpace()
    print('Alright, a new meeting it is!')
    printSpace()
    
    name = input('What would you like to set this meeting\'s name as (the name acts like a label for you to recognise meetings, you CANNOT change this later): ')
    if not validationCheck(name):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
        return
    for meeting in meetings:
        if name == meeting:
            print('Sorry, this name has already been used. Please use a new name. Restarting add meeting...')
            addMeeting()
            return
    printSpace()
    
    meetingType = (input('Next up is the meeting platform. Enter \'z/zoom\' for Zoom Cloud Meetings, \'gm/meet\' for Google Meet, \'t/teams\' for Microsoft Teams or \'o\' for Others: ')).lower()
    if not validationCheck(meetingType):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
        return
    if meetingType == 'z' or meetingType == 'zoom':
        meetingType = 'Zoom Cloud Meetings'
    elif meetingType == 'gm' or meetingType == 'meet':
        meetingType = 'Google Meet'
    elif meetingType == 't' or meetingType == 'teams':
        meetingType = 'Microsoft Teams'
    elif meetingType == 'o':
        specificPlatform = input('You selected \'Others\'. Please enter the name of the platform: ')
        if not validationCheck(specificPlatform):
            print('Please enter data properly. Restarting add meeting...')
            addMeeting()
            return
        meetingType = specificPlatform
    else: 
        print('Sorry, an invalid meeting type was entered. Restarting add meeting...')
        addMeeting()
        return
    printSpace()
    
    meetingID = input('Cool. Next enter the meeting ID, this can be either all numerals, all letters or both: ')
    if not validationCheck(meetingID):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
        return
    printSpace()
    
    meetingPwd = input('Next up, enter the meeting\'s password (enter \'skip\' if meeting is not password-protected): ')
    if not validationCheck(meetingPwd):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
        return
    if meetingPwd == 'skip':
        meetingPwd = ''
    printSpace()
    
    meetingLink = ''
    if settings['linkGeneratorEnabled'] == 'true' and (meetingType == 'Zoom Cloud Meetings' or meetingType == 'Google Meet'):
        meetingLink = input('Next enter the meeting\'s link (enter \'skip\' if no viable link is available, or type \'auto\' for StickyMeet to generate it for you): ')
    else:
        meetingLink = input('Next enter the meeting\'s link (enter \'skip\' if no viable link is available): ')
    if not validationCheck(meetingLink):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
        return
    if meetingLink == 'skip':
        meetingLink = ''
    if meetingLink == 'auto':
        if meetingType == 'Zoom Cloud Meetings':
            meetingLink = 'https://us02web.zoom.us/j/' + meetingID.strip()
        elif meetingType == 'Google Meet':
            individualIDCodes = meetingID.split(' ')
            finalPath = '-'.join(individualIDCodes)
            meetingLink = 'https://meet.google.com/' + finalPath
    
    ## Creating JSON object with data given...
    setName = name
    meetings[setName] = { "type": meetingType, "id": meetingID, "pwd": meetingPwd, "link": meetingLink }
    json.dump(meetings, open("meetings.txt", 'w'))
    printSpace()
    print('Meeting added successfully!')
    
def viewMeetings():
    printSpace()
    count = 0
    for meeting in meetings:
        try:
            print('Meeting Number: {}'.format(count))
            printSpace()
            print('\tName: {}'.format(meeting))
            printSpace()
            print('\tPlatform: {}'.format(meetings[meeting]['type']))
            printSpace()
            print('\tID: {}'.format(meetings[meeting]['id']))
            printSpace()
            if meetings[meeting]['pwd'] != '':
                print('\tPassword: {}'.format(meetings[meeting]['pwd']))
                printSpace()
            if meetings[meeting]['link'] != '':
                print('\tLink: {}'.format(meetings[meeting]['link']))
                printSpace()
            count += 1
        except:
            print("Error in loading data from database.")
    
def viewMeetingsGUI():
    #Tkinter window setup
    root = tk.Tk()
    
    canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
    canvas.pack()

    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    
    global guiViewMeetingsCount
    guiViewMeetingsCount = 0
    
    def getMeetingName():
        targetMeeting = ''
        identifierCount = 0
        for meeting in meetings:
            if identifierCount == guiViewMeetingsCount:
                targetMeeting = meeting
            identifierCount += 1
        return targetMeeting
    
    def packData():
        #Obtain target data
        targetMeeting = getMeetingName()
        
        #Make labels with data
        meetingNumberLabel = tk.Label(frame, text='Meeting Number: {}'.format(guiViewMeetingsCount), bg="white")
        meetingNameLabel = tk.Label(frame, text="Name: {}".format(targetMeeting), bg="white")
        meetingIDLabel = tk.Label(frame, text="ID: {}".format(meetings[targetMeeting]['id']), bg="white")
        if meetings[targetMeeting]['pwd'] != '':
            meetingPwdLabel = tk.Label(frame, text="Password: {}".format(meetings[targetMeeting]['pwd']), bg="white")
        if meetings[targetMeeting]['link'] != '':
            meetingLinkLabel = tk.Label(frame, text="Link: {}".format(meetings[targetMeeting]['link']), bg="white")
        
        #Pack labels
        meetingNumberLabel.pack()
        meetingNameLabel.pack()
        meetingIDLabel.pack()
        if meetings[targetMeeting]['pwd'] != '':
            meetingPwdLabel.pack()
        if meetings[targetMeeting]['link'] != '':
            meetingLinkLabel.pack()
        
    packData()
    
    def moveToNextMeeting():
        global guiViewMeetingsCount
        global nextMeeting
        guiViewMeetingsCount = guiViewMeetingsCount + 1
        if guiViewMeetingsCount >= len(meetings):
            guiViewMeetingsCount = 0
        for widget in frame.winfo_children():
            widget.destroy()
        packData()
        
        for widget in root.winfo_children():
            if str(type(widget)) == "<class 'tkinter.Button'>":
                widget.destroy()
                
        nextMeeting = tk.Button(root, text="Next Meeting", padx=10, pady=5, bg="#263D42", command=moveToNextMeeting)
        nextMeeting.pack()
        
        def copyIDToClip():
            meetingid = meetings[getMeetingName()]['id']
            copy2clip(meetingid)
    
        copyID = tk.Button(root, text="Copy ID", padx=10, pady=5, bg="#263D42", command=copyIDToClip)
        copyID.pack()
    
        def copyPwdToClip():
            meetingpwd = meetings[getMeetingName()]['pwd']
            copy2clip(meetingpwd)
    
        if meetings[getMeetingName()]['pwd'] != '':
            copyPwd = tk.Button(root, text="Copy Password", padx=10, pady=5, bg="#263D42", command=copyPwdToClip)
            copyPwd.pack()
    
        def copyLinkToClip():
            meetinglink = meetings[getMeetingName()]['link']
            copy2clip(meetinglink)
    
        if meetings[getMeetingName()]['link'] != '':
            copyLink = tk.Button(root, text="Copy Link", padx=10, pady=5, bg="#263D42", command=copyLinkToClip)
            copyLink.pack()
    
    global nextMeeting
    nextMeeting = tk.Button(root, text="Next Meeting", padx=10, pady=5, bg="#263D42", command=moveToNextMeeting)
    nextMeeting.pack()
    
    # i dont know wth is happenning rn what am i even doing
    # it works but i dont knoow why
    
    def copyIDToClip():
        meetingid = meetings[getMeetingName()]['id']
        copy2clip(meetingid)
    
    copyID = tk.Button(root, text="Copy ID", padx=10, pady=5, bg="#263D42", command=copyIDToClip)
    copyID.pack()
    
    def copyPwdToClip():
        meetingpwd = meetings[getMeetingName()]['pwd']
        copy2clip(meetingpwd)
    
    if meetings[getMeetingName()]['pwd'] != '':
        copyPwd = tk.Button(root, text="Copy Password", padx=10, pady=5, bg="#263D42", command=copyPwdToClip)
        copyPwd.pack()
    
    def copyLinkToClip():
        meetinglink = meetings[getMeetingName()]['link']
        copy2clip(meetinglink)
    
    if meetings[getMeetingName()]['link'] != '':
        copyLink = tk.Button(root, text="Copy Link", padx=10, pady=5, bg="#263D42", command=copyLinkToClip)
        copyLink.pack()
    
    root.mainloop()
    
def removeMeeting():
    printSpace()
    meetingIdentifier = input('Enter the name of the meeting (case-sensitive) or enter the meeting number: ')
    if meetingIdentifier.isdigit():
        try:
            meetingNumber = int(meetingIdentifier)
            count = 0
            for meeting in meetings:
                if count == meetingNumber:
                    meetings.pop(meeting)
                    json.dump(meetings, open("meetings.txt", 'w'))
                    printSpace()
                    print('Meeting deleted successfully!')
                    break
                count += 1
        except:
            print('Sorry, failed to remove meeting')
    else:
        try:
            meetings.pop(meetingIdentifier)
            json.dump(meetings, open("meetings.txt", 'w'))
            printSpace()
            print('Meeting deleted successfully!')
        except:
            print('Sorry, failed to remove meeting')
            
def userHelp():
    printSpace()
    print('Fret not, I have got you covered! I am the StickyMeet helper and I will explain all features of StickyMeet throughly!')
    printSpace()
    print("""
        Hey there! StickyMeet is an application designed for you to easily save your meeting information so you do not have to go hunting for your next meeting's information again!
        All data in StickyMeet is stored locally and remains even after you exit the application!
          
        First up, the 'add' function launches up an interactive method for you to easily save your meeting.
            (1) The function will ask you for the label of the meeting (also called the meeting name) for you to easily recognize which meeting is what.
            (2) Next it will ask the Meeting's ID, which you can find out via the steps below:
                    Zoom: Your meeting host should send you the meeting's ID in the message. If he/she only gives you a link, the ID can be found at the end of the link. For example:
                        https://us02web.zoom.us/j/234414332 has the meeting ID 234 4143 32
                    Google Meet: You can find the meeting ID at the end of the link. For example:
                             https://meet.google.com/yvh-wkpf-dpe has the ID yvh wkpf dpe
                    Microsoft Teams: Your meeting host should provide you the ID.
            (3) Next it will ask the password, so enter it in, if there is one. If the meeting is not password-protected simply type 'skip'.
            (4) Next it will ask for the link, which is optional as well. If you wish to save it, enter the link, if not type 'skip'.
          
        And done! You have just added a new meeting!
          
        Next up, the 'view' or 'view -v' function allows you to easily view all of your meetings in a neat manner.
        There is two ways you can view your saved meetings: 1) Via text in the console, 2) Via a Graphical User Interface (GUI) which is a visual window.
            (1) Typing 'view' will cycle through all of your meeting information and show it to you one-by-one. Do note that every meeting has a number.
            (2) Typing 'view -v' will open up a visual window with which you can view your saved meetings easily. You can even copy certain information with the buttons located at the bottom of the window.
              You can go to the next meeting simply by pressing the 'Next Meeting' button!
              
        Next up, the 'remove' function easily allows you to remove a meeting with either the meeting name or the meeting number as an input.
        If you know the number of the meeting, for example 0, you can simply type '0' and the meeting with the 0th number will be removed!
        Of course, you can find out the meeting number by using the 'view' function.
        Or you can remove a meeting with its name. Simply type in the name of the meeting and StickyMeet will delete it. Do note that this is case-sensitive.
        
        Next up, the 'edit' function easily allows you to edit specifc information of a meeting. Here are the steps to editing a meeting:
            (1) First, StickyMeet will ask you to enter the name or number of the meeting you want to edit. Note that the name is case-sensitive and has to be the exact of what you put in.
            (2) Second, enter the name of the element you want to edit. They include 'id', 'password', 'platform' and 'link'. All these valid names are also shown in the prompt.
            (3) Third, it will ask you to enter the new value of the element. Hit enter and you are done!
        
        Next up, the 'settings' function opens up the User Settings manager.
        As of now, only one setting (link-generation) is available for you to change according to your preference.
        When you type 'settings' on the main screen, you can type 'view' on the following prompt to view the state of all current settings.
        Settings and explanation list:
            (1) link-generation: This setting, when turned on, allows you to have an option to let StickyMeet generate a meeting's link for you based on the ID you have provided when making a new meeting.
                                When making a new meeting and asked for the link, if you said that the meeting platform is either Zoom Cloud Meetings or Google Meet, StickyMeet gives you an option to type 'auto' in the prompt
                                to let StickyMeet generate the link for you automatically based on the platform and ID. For example, the ID 'jvh see asg' and the platform 'Google Meet' would generate the link 'https://meet.google.com/jvh-see-asg'.
                            
                                Changing this setting:
                                    (1) Open up the User Settings manager by typing 'settings' on the main screen.
                                    (2) Type in 'link-generation'
                                    (3) If you wish to enable it, type in 'enable', if not, type in 'disable'
                                    Done!

        Next up, is the 'help' function. You already know this one! This simply prints a thorough explanation on the features of StickyMeet.
        
        Lastly, the 'exit' function simply closes the application.
        
        Hope you now have a clearter understanding of StickyMeet!!!
          """)
    
def changeSetting():
    printSpace()
    print('Welcome to the User Settings manager!')
    print('Here you can change different settings of the app as you like.')
    printSpace()
    print('Available Settings include: \n\t\'link-generation\': System which allows you to easily generate a link with the ID you have provided when adding a meeting for select meeting platforms.')
    print('Type \'help\' on the main run for more information about settings.')
    printSpace()
    settingName = input('Please enter the setting you would like to change (case-sensitive) or type \'view\' to view current state of all settings: ')
    if settingName == 'link-generation':
        printSpace()
        newStatus = input('Please type \'enable\' to enable or \'disable\' to disable this setting: ')
        if newStatus == 'enable':
            settings['linkGeneratorEnabled'] = 'true'
            json.dump(settings, open('settings.txt', 'w'))
            printSpace()
            print('Setting updated successfully!')
        elif newStatus == 'disable':
            settings['linkGeneratorEnabled'] = 'false'
            json.dump(settings, open('settings.txt', 'w'))
            printSpace()
            print('Setting updated successfully!')
        else:
            print('Sorry, invalid status entered. Failed to update setting. Restarting settings manager...')
            changeSetting()
    elif settingName == 'view':
        printSpace()
        for setting in settings:
            if setting == 'linkGeneratorEnabled':
                currentStatus = settings[setting]
                if currentStatus == 'true':
                    currentStatus = 'Enabled'
                else:
                    currentStatus = 'Disabled'
                print('\tlink-generation: ' + currentStatus)
    elif settingName == 'exit':
        print('Exiting User Settings Manager...')
        return
    
def editMeeting():
    printSpace()
    meetingIdentifier = input('Please enter the name (case-sensitive) or the number of the meeting you would like to edit: ')
    printSpace()
    if meetingIdentifier.isdigit():
        try:
            meetingNumber = int(meetingIdentifier)
            count = 0
            for meeting in meetings:
                if count == meetingNumber:
                    # Found meeting with meeting number
                    elementToEdit = input("Please type in either 'id', 'password', 'platform' or 'link' to edit the specific information: ")
                    printSpace()
                    if elementToEdit == 'id':
                        newInfo = input('Please enter the new ID: ')
                        printSpace()
                        try:
                            meetings[meeting]['id'] = newInfo
                            json.dump(meetings, open("meetings.txt", "w"))
                            print('Meeting information updated successfully!')
                            return
                        except:
                            print('Sorry, failed to edit the meeting.')
                    elif elementToEdit == 'password':
                        newInfo = input('Please enter the new password: ')
                        printSpace()
                        try:
                            meetings[meeting]['pwd'] = newInfo
                            json.dump(meetings, open("meetings.txt", "w"))
                            print('Meeting information updated successfully!')
                            return
                        except:
                            print('Sorry, failed to edit the meeting.')
                    elif elementToEdit == 'platform':
                        # get new platform
                        newInfo = (input('Please enter the meeting platform. Enter \'z/zoom\' for Zoom Cloud Meetings, \'gm/meet\' for Google Meet, \'t/teams\' for Microsoft Teams or \'o\' for Others: ')).lower()
                        if not validationCheck(newInfo):
                            print('Please enter data properly. Restarting edit meeting...')
                            editMeeting()
                            return
                        if newInfo == 'z' or newInfo == 'zoom':
                            newInfo = 'Zoom Cloud Meetings'
                        elif newInfo == 'gm' or newInfo == 'meet':
                            newInfo = 'Google Meet'
                        elif newInfo == 't' or newInfo == 'teams':
                            newInfo = 'Microsoft Teams'
                        elif newInfo == 'o':
                            specificPlatform = input('You selected \'Others\'. Please enter the name of the platform: ')
                            if not validationCheck(specificPlatform):
                                print('Please enter data properly. Restarting edit meeting...')
                                editMeeting()
                                return
                            newInfo = specificPlatform
                        else: 
                            print('Sorry, an invalid meeting type was entered. Restarting edit meeting...')
                            editMeeting()
                            return
                        printSpace()
            
                        # update database
                        try:
                            meetings[meeting]['type'] = newInfo
                            json.dump(meetings, open("meetings.txt", "w"))
                            print('Meeting information updated successfully!')
                            return
                        except:
                            print('Sorry, failed to edit the meeting.')
                    elif elementToEdit == 'link':
                        if settings['linkGeneratorEnabled'] == 'true' and (meetings[meeting]['type'] == 'Zoom Cloud Meetings' or meetings[meeting]['type'] == 'Google Meet'):
                            newInfo = input('Please enter the new link (or type \'auto\' for StickyMeet to generate it for you): ')
                            if newInfo == 'auto':
                                if meetings[meeting]['type'] == 'Zoom Cloud Meetings':
                                    newInfo = 'https://us02web.zoom.us/j/' + meetings[meeting]['id'].strip()
                                elif meetings[meeting]['type'] == 'Google Meet':
                                    individualIDCodes = meetings[meeting]['id'].split(' ')
                                    finalPath = '-'.join(individualIDCodes)
                                    newInfo = 'https://meet.google.com/' + finalPath
                        else:
                            newInfo = input('Please enter the new link: ')
                            
                        printSpace()
                        try:
                            meetings[meeting]['link'] = newInfo
                            json.dump(meetings, open("meetings.txt", "w"))
                            print('Meeting information updated successfully!')
                            return
                        except:
                            print('Sorry, failed to edit the meeting.')
                    else:
                        print('Sorry, invalid element typed. Restarting edit meeting...')
                        editMeeting()
                        return
                    break
                count += 1
            print('Sorry, meeting could not be found with given meeting number. Please try again')
            return
        except:
            print('Sorry, failed to edit or find meeting.')
    else:
        try:
            targetMeeting = meetings[meetingIdentifier]
        except:
            print('Sorry, could not identify meeting with name. Please try again.')
            editMeeting()
            return
        elementToEdit = input("Please type in either 'id', 'password', 'platform' or 'link' to edit the specific information: ")
        printSpace()
        if elementToEdit == 'id':
            newInfo = input('Please enter the new ID: ')
            printSpace()
            try:
                meetings[meetingIdentifier]['id'] = newInfo
                json.dump(meetings, open("meetings.txt", "w"))
                print('Meeting information updated successfully!')
            except:
                print('Sorry, failed to edit the meeting.')
        elif elementToEdit == 'password':
            newInfo = input('Please enter the new password: ')
            printSpace()
            try:
                meetings[meetingIdentifier]['pwd'] = newInfo
                json.dump(meetings, open("meetings.txt", "w"))
                print('Meeting information updated successfully!')
            except:
                print('Sorry, failed to edit the meeting.')
        elif elementToEdit == 'platform':
            # get new platform
            newInfo = (input('Next up is the meeting platform. Enter \'z/zoom\' for Zoom Cloud Meetings, \'gm/meet\' for Google Meet, \'t/teams\' for Microsoft Teams or \'o\' for Others: ')).lower()
            if not validationCheck(newInfo):
                print('Please enter data properly. Restarting edit meeting...')
                editMeeting()
                return
            if newInfo == 'z' or newInfo == 'zoom':
                newInfo = 'Zoom Cloud Meetings'
            elif newInfo == 'gm' or newInfo == 'meet':
                newInfo = 'Google Meet'
            elif newInfo == 't' or newInfo == 'teams':
                newInfo = 'Microsoft Teams'
            elif newInfo == 'o':
                specificPlatform = input('You selected \'Others\'. Please enter the name of the platform: ')
                if not validationCheck(specificPlatform):
                    print('Please enter data properly. Restarting edit meeting...')
                    editMeeting()
                    return
                newInfo = specificPlatform
            else: 
                print('Sorry, an invalid meeting type was entered. Restarting edit meeting...')
                editMeeting()
                return
            printSpace()
            
            # update database
            try:
                meetings[meetingIdentifier]['type'] = newInfo
                json.dump(meetings, open("meetings.txt", "w"))
                print('Meeting information updated successfully!')
            except:
                print('Sorry, failed to edit the meeting.')
        elif elementToEdit == 'link':
            newInfo = ''
            if settings['linkGeneratorEnabled'] == 'true' and (targetMeeting['type'] == 'Zoom Cloud Meetings' or targetMeeting['type'] == 'Google Meet'):
                newInfo = input('Please enter the new link (or type \'auto\' for StickyMeet to generate it for you): ')
                if newInfo == 'auto':
                    if targetMeeting['type'] == 'Zoom Cloud Meetings':
                        newInfo = 'https://us02web.zoom.us/j/' + targetMeeting['id'].strip()
                    elif targetMeeting['type'] == 'Google Meet':
                        individualIDCodes = targetMeeting['id'].split(' ')
                        finalPath = '-'.join(individualIDCodes)
                        newInfo = 'https://meet.google.com/' + finalPath
            else:
                newInfo = input('Please enter the new link: ')
            printSpace()
            try:
                meetings[meetingIdentifier]['link'] = newInfo
                json.dump(meetings, open("meetings.txt", "w"))
                print('Meeting information updated successfully!')
            except:
                print('Sorry, failed to edit the meeting.')
        else:
            print('Sorry, invalid element typed. Restarting edit meeting...')
            editMeeting()
            return
    
def performDataReset():
    printSpace()
    print('Initiating data reset...')
    printSpace()
    print('Deleting data files...')
    try:
        os.remove('meetings.txt')
        os.remove('settings.txt')
    except:
        print('An error occurred in deleting data files. System reload required. Terminating app...')
        exit()
    printSpace()
    print('Writing new data files...Please wait.')
    time.sleep(2)
    try:
        meetings = {}
        if os.path.isfile('meetings.txt'):
            meetings = json.load(open("meetings.txt"))
        else:
            f = open("meetings.txt", "w")
            json.dump({ "sample": "sample" }, f)
            f.close()
            meetings = {}
            
        settings = {}
        if os.path.isfile('settings.txt'):
            settings = json.load(open("settings.txt"))
        else:
            f = open("settings.txt", "w")
            json.dump({ "linkGeneratorEnabled": "false" }, f)
            f.close()
            settings = { "linkGeneratorEnabled": "false" }
    except:
        print('An error occurred in writing new data. System reload required. Terminating app...')
        exit()
    print('System data reset performed.')
    restartApp()
    
def rereadData():
    printSpace()
    print('Re-reading data from data files... please wait!')
    try:
        meetings = json.load(open("meetings.txt"))
        settings = json.load(open("settings.txt"))
    except:
        print('There was an error in re-reading from data files. Please restart StickyMeet.')
        exit()
    time.sleep(2)
    print('Data re-read successfully.')
    restartApp()
    
def errorHelp():
    printSpace()
    print("""
          ***DANGER FUNCTIONS***:
        Functions listed here are dangerous and should only be used if absolutely necessary.
        
        The 'system-reset' function deletes all of your current meetings data and restarts StickyMeet. 
        If you are running StickyMeet on IDLE you will have to manually start up StickyMeet after its done resetting and stopping itself. 
        Follow the intructions given after the reset to start up StickyMeet. If you are running StickyMeet on console, you do not have to worry,
        StickyMeet will restart after the system reset and you can continue using StickyMeet.
        This function should only be used if StickyMeet is resulting in constant errors.
        
        The 're-read' function re-reads the data files stored on your computer to update its database. After re-reading, StickyMeet will have to restart. 
        If you are running StickyMeet on IDLE you will have to manually start up StickyMeet after its done resetting and stopping itself.
        Follow the intructions given after the reset to start up StickyMeet.
        If you are running StickyMeet on CONSOLE, you do not have to worry, StickyMeet will restart after the system reset 
        and you can continue using StickyMeet. This function should only be used if StickyMeet is not able to show meetings properly or cannot add/remove/edit meetings.
          """)
    
def updateToHigherVersion():
    printSpace()
    print('Data store creation for newer version of StickyMeet process started...please wait!')
    printSpace()
    # dataCacheFolderPath = 'Desktop/DO NOT EDIT - StickyMeet data files'
    dataCacheFolderPath = ''
    
    ## Get proper path for Desktop corresponding to OS
    currentDirectory = os.getcwd()
    
    ### Get the trailing path and then add desktop to it
    pathInArrayForm = list(currentDirectory)
    slashesCount = 0
    hitTrailingPoint = False
    loopCount = 0
    for char in pathInArrayForm:
        if hitTrailingPoint:
            pathInArrayForm = pathInArrayForm[:loopCount]
            break
        else:
            if char == '/' or char == '\\':
                slashesCount += 1
                if slashesCount >= 3:
                    hitTrailingPoint = True
        loopCount += 1
    dataCacheFolderPath = ''.join(pathInArrayForm)
    if sys.platform == 'win32':
        dataCacheFolderPath += 'Desktop\DO NOT EDIT - StickyMeet data files'
    elif sys.platform == 'darwin':
        dataCacheFolderPath += 'Desktop/DO NOT EDIT - StickyMeet data files'
    else:
        print('unsupported OS')
        exit()
    
    # create directory with path if there is none
    try:
        readmePath = os.path.join(dataCacheFolderPath, 'README.txt')
        if not os.path.exists(dataCacheFolderPath):
            os.makedirs(dataCacheFolderPath)
        f = open(readmePath, "w")
        message = "PLEASE DO NOT DELETE THIS FOLDER. THIS FOLDER WAS AUTO-GENERATED BY STICKYMEET FOR THE USER TO IMPORT THEIR OLD DATA FROM WHEN THEY DOWNLOAD A NEWER VERSION OF STICKYMEET. DO NOT EDIT THE FOLDER/FILES' NAME OR CONTENT WITHIN SAID FILES OR STICKYMEET MAY FAIL TO IMPORT DATA."
        f.write(message)
    
        cacheMeetings = open(os.path.join(dataCacheFolderPath, 'meetings.txt'), "w")
        json.dump(meetings, cacheMeetings)
        
        print('Almost done...')
        time.sleep(2)
        
        cacheSettings = open(os.path.join(dataCacheFolderPath, 'settings.txt'), "w")
        json.dump(settings, cacheSettings)
        
        print('Finishing up...')
        time.sleep(2)
        print('Done! Version data store was made.')
    except:
        print('Sorry, there was an error in creating the folder and the files and the update cache could not be made.')
    
def mainRun():
    print('You can always type \'Control + C\' or \'exit\' (only on the main screen,\n denoted by -------) to exit the application!')
    printSpace()
    startingAction = input('Type \'view\' to view your saved meetings or \'view -v\' to view them in a GUI Window, \n\'add\' for adding a new meeting, \n\'remove\' for removing a meeting,\n\'edit\' to edit a meeting,\n\'settings\' for changing or viewing User Settings,\n\'help\' for help: ')
    validStartingActions = ['view', 'view -v', 'add', 'remove', 'exit', 'system-reset', 're-read', 'settings', 'help', 'version', 'edit', 'help error', 'update -l']
    if startingAction not in validStartingActions:
        print('Sorry, invalid action typed! Please try again!')
        printSpace()
        print('-------')
        mainRun()
    if startingAction == 'add':
        addMeeting()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'view':
        if len(meetings) == 0:
            print('Sorry! No meetings are saved to display! Add a meeting by typing \'add\'!')
            printSpace()
            mainRun()
        viewMeetings()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'view -v':
        if len(meetings) == 0:
            print('Sorry! No meetings are saved to display! Add a meeting by typing \'add\'!')
            printSpace()
            mainRun()
        viewMeetingsGUI()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'remove':
        removeMeeting()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'settings':
        changeSetting()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'help':
        userHelp()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'help error':
        errorHelp()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'edit':
        editMeeting()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'system-reset':
        performDataReset()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 're-read':
        rereadData()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'version':
        printSpace()
        print('StickyMeet Version 1.1 \n© Prakhar Trivedi 2021')
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'update -l':
        updateToHigherVersion()
        printSpace()
        print('-------')
        mainRun()
    elif startingAction == 'exit':
        print('Byeeeee!')
        exit()

mainRun()