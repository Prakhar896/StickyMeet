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
meetings = json.load(open("meetings.txt"))
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
    printSpace()
    
    meetingType = (input('Next up is the meeting platform. Enter \'z/zoom\' for Zoom Cloud Meetings, \'gm/meet\' for Google Meet, \'t/teams\' for Microsoft Teams or \'o\' for Others: ')).lower()
    if not validationCheck(name):
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
    if not validationCheck(name):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
    printSpace()
    
    meetingPwd = input('Next up, enter the meeting\'s password (enter \'skip\' if meeting is not password-protected): ')
    if not validationCheck(name):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
    if meetingPwd == 'skip':
        meetingPwd = ''
    printSpace()
    
    meetingLink = input('Next enter the meeting\'s link (enter \'skip\' if no viable link is available): ')
    if not validationCheck(name):
        print('Please enter data properly. Restarting add meeting...')
        addMeeting()
    if meetingLink == 'skip':
         meetingLink = ''
    
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
    

def mainRun():
    print('You can always type \'exit\' to exit the application!')
    printSpace()
    startingAction = input('Type \'view\' to view your saved meetings or \'view -v\' to view them in a GUI Window, \n\'add\' for adding a new meeting, \n\'remove\' for removing a meeting \n\'help\' for help: ')
    if startingAction != 'view' and startingAction != 'add' and startingAction != 'remove' and startingAction != 'view -v' and startingAction != 'exit':
        print('Sorry, invalid action typed! Please try again!')
        printSpace()
        mainRun()
    if startingAction == 'add':
        addMeeting()
        printSpace()
        mainRun()
    elif startingAction == 'view':
        viewMeetings()
        printSpace()
        mainRun()
    elif startingAction == 'view -v':
        viewMeetingsGUI()
        printSpace()
        mainRun()
    elif startingAction == 'remove':
        removeMeeting()
        printSpace()
        mainRun()
    elif startingAction == 'exit':
        print('Byeeeee!')
        exit()

mainRun()
 
 
 ## Ideas:
 ## Meeting link generator with ID fitting into prefix url
 ## GUI format of viewing meetings that has copy to clipboard
 ## Next function in tkinter window
