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
print(meetings)

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
        printSpace()
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
            
    


def mainRun():
    startingAction = input('Type \'view\' to view your saved meetings, \'add\' for adding a new meeting, \'remove\' for removing a meeting \'help\' for help: ')
    if startingAction != 'view' and startingAction != 'add' and startingAction != 'remove':
        print('Sorry, invalid action typed! Please try again!')
        printSpace()
        mainRun()
    if startingAction == 'add':
        addMeeting()
    elif startingAction == 'view':
        viewMeetings()

mainRun()
 
 
 ## Ideas:
 ## Meeting link generator with ID fitting into prefix url
 ## GUI format of viewing meetings that has copy to clipboard