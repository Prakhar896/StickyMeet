# StickyMeet
A console application (with a tad bit of GUI) that allows you to easily save your meetings so you don't have to go hunting again.

## Activator

<img src="https://github.com/Prakhar896/ActivatorDocs/blob/main/activatorLogo.png?raw=true" alt="Activator Logo" width="350px">

[Activator](https://github.com/Prakhar896/ActivatorDocs) is a product activation service that activates copies. It also provides users a unified dashboard to manage all of your activated copies across several products that conform to Activator's DRM (Digital Rights Management) process. StickyMeet is one of these products.

### How It Works

Any copy of StickyMeet will first need to be activated with Activator. You do not have to do anything on your part; upon boot, if not activated, StickyMeet will locate the latest Activator server and will activate itself. A `licensekey.txt` file will be downloaded that will contain the license key for the copy. This file will be used to verify the copy's authenticity.

**DO NOT** delete the `licensekey.txt` file. If you do, the copy will be deactivated and will need to be activated again.

Every 14 days, the copy will automatically trigger a license key verification request (KVR) to ensure that the copy is still activated. If the copy is not activated, it will be deactivated and will need to be activated again. (Run the copy code again.)

### What I Can Do With Activator

During copy activation, the activation script generates unique identifiers for the computer it is being run on (called HSN) and for the copy itself (called CSN).

These identifiers are submitted to Activator servers. If an account with the same HSN is found, the CSN is added to the account. If no account is found, a new account is created with the HSN and CSN.

> NOTE: None of your private computer information is divulged in the activation process.

Then, you can log in to Activator using the link provided in the `licensekey.txt` file. You will be able to see all of your activated copies and their CSNs. You can also manage your account, link other HSN accounts as aliases and much more.

> For more information about Activator, see its [documentation](https://github.com/Prakhar896/ActivatorDocs)


## Usage
Downloading and using StickyMeet is a breeze!

Here are the steps to getting StickyMeet on your computer:

1) Click [here](http://gg.gg/StickyMeetDownload) to download a zip file of StickyMeet. 
2) Click and expand the StickyMeet zip file and you should see a folder named `StickyMeet-1.1`

### Usage with IDLE
3) Download and install the latest Python [here](https://python.org)
4) Open up an app called IDLE and click File > Open and select the `main.py` file inside the `StickyMeet-1.1` folder.
5) Click Run > Run Module to run the file.
6) Follow the instructions and start using StickyMeet! Type in `help` for help on using StickyMeet.

### Usage with Terminal/Command Prompt
3) On macOS, open up an app named Terminal, or, if on Windows, open up Command Prompt.
4) Considering the location for file downlaods in your browser is the default, cd (change directory) into the folder using `cd Downloads/StickyMeet-1.1`
5) Type in `python3 main.py` to run the `main.py` file and you can start using StickyMeet from your OS's shell!

## Frequently-Answered Questions
Q. Where is my meetings data stored? Is it safe to trust StickyMeet with confidential meeting information?

Ans: Yes, it is completely safe to store your meeting information with StickyMeet as all meeting data is locally stored on your computer.

Q. There is an error with StickyMeet, it is not showing information properly. What should I do?

Ans: If you come across this situation, please type in `system-reset` on the main action command (the one where it shows you the multiple functions you can type in). This will delete and re-write your data files (NOTE: This means that all existing meeting information will be deleted) so that StickyMeet starts on a fresh page. If an error occurs in doing this, please re-download StickyMeet.

Q. Does using the GUI (visual) version of the view meetings function cause GPU lags or cause a lot of resources to be used?

Ans: The GUI version was designed to be of low-intensity on your system's GPU and hence you will experience a little to nothing difference on your computer's processing speeds so do not worry.

Copyright © 2021 Prakhar Trivedi
