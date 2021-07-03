# Ideas:
# Mean Subject Grade
# Discord Chat Bot
# Hangman
# Typing Test
# Zoom Meeting ID and password saving system ***
import os, sys, subprocess
import tkinter as tk
from tkinter import filedialog, Text
import time
import json

print('Welcome to StickyMeet! What would you like to do today?')

meetings = []
if os.path.isfile('meetings.txt'):
    meetings = json.load(open("meetings.txt"))
else:
    f = open("meetings.txt", "w")
    json.dump({ "sample": "sample" }, f)
    f.close()
    meetings = []

settings = []
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
    print('No sample in database')

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

printSpace()

def addMeeting():
    printSpace()
    print('Alright, a new meeting it is!')
    printSpace()
    
    name = input('What would you like to set this meeting\'s name as (the name acts like a label for you to recognise meetings): ')
    if not validationCheck(name):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
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
    if meetingType == 'z' or meetingType == 'zoom':
        meetingType = 'Zoom Cloud Meetings'
    elif meetingType == 'gm' or meetingType == 'meet':
        meetingType = 'Google Meet'
    elif meetingType == 't' or meetingType == 'teams':
        meetingType = 'Microsoft Teams'
    elif meetingType == 'o':
        meetingType = 'Others'
    else: 
        print('Sorry, an invalid meeting type was entered. Restarting add meeting...')
        addMeeting()
    printSpace()
    
    meetingID = input('Cool. Next enter the meeting ID, this can be either all numerals, all letters or both: ')
    if not validationCheck(meetingID):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
    printSpace()
    
    meetingPwd = input('Next up, enter the meeting\'s password (enter \'skip\' if meeting is not password-protected): ')
    if not validationCheck(meetingPwd):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
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
    meetings[name] = { "type": meetingType, "id": meetingID, "pwd": meetingPwd, "link": meetingLink }
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

def mainRun():
    print('You can always type \'exit\' to exit the application!')
    printSpace()
    startingAction = input('Type \'view\' to view your saved meetings or \'view -v\' to view them in a GUI Window, \n\'add\' for adding a new meeting, \n\'remove\' for removing a meeting,\n\'settings\' for changing or viewing User Settings,\n\'help\' for help: ')
    if startingAction != 'view' and startingAction != 'add' and startingAction != 'remove' and startingAction != 'view -v' and startingAction != 'exit' and startingAction != 'help' and startingAction != 'settings':
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
    elif startingAction == 'exit':
        print('Byeeeee!')
        exit()

mainRun()
 
 
 ## Ideas:
 ## Meeting link generator with ID fitting into prefix url
 ## GUI format of viewing meetings that has copy to clipboard - done
 ## Next function in tkinter window - done


# Todos:
# Make check for same meeting names - done
# 