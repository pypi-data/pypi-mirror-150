
#main method; runs interactive prompt
def main():

    #before doing anything else, create a backup of the music file
    try:
        createMusicBackup()
    #if backup already exists, a FileExistsError is raised
    except FileExistsError:
        #ignore error silently; no need to re-create backup
        pass

    interactiveMenu()

#returns a dict used as the menuOptions in interactiveMenu
def getInteractiveMenuOptions():
    from hlm2_music_changer.dirtools import getMusicWadList
    
    #always start with 0 being the original music
    menuOptions = {"0": "Original Hotline Miami 2 Soundtrack"}

    #add one numeric option for each music mod
    for index, filename in enumerate(getMusicWadList()):
        #NOTE: keys assigned are string type, not int
        #also the index is offset by 1, because 0 is taken
        menuOptions[str(index + 1)] = filename

    #add special options
    menuOptions["r"] = "Refresh music .wad list"
    menuOptions["o"] = "Open music .wad directory"
    menuOptions["q"] = "Quit"
    menuOptions["?"] = "Display help"
    

    return menuOptions

#method that provides user with options and prompts to select an option
#a main menu of sorts
#loops infinitely until quit command (q) is entered
def interactiveMenu():
    from hlm2_music_changer.dirtools import openDirectoryWindow, getMusicWadDirectory, getBackupFileName, getActiveWadName, setActiveWadName
    from os import path
    while True:
        #print blank line for seperation
        print()

        #get menu options
        menuOptions = getInteractiveMenuOptions()

        #get the active wad name
        activeWadName = getActiveWadName()
        
        #None indicates that no mod is selected
        #if the active wad name is None, use the description of the original soundtrack wad
        if activeWadName is None:
            activeWadName = menuOptions["0"]

        
        #get the largest command width in chars
        #this is used to draw evenly spaced column seperators
        maxCommandWidth = max(map(len, menuOptions.keys()))

        #add 2 to the max command width to account for parens
        maxCommandWidth += 2

        #print the menu options
        for command, description in menuOptions.items():
            #highlight the option with parens if it is currently selected
            if activeWadName == description:
                command = f"({command})"
            
            print(f"{command:<{maxCommandWidth}} :  {description}")
        
        #print newline for seperation
        print()

        userSelection = input("Choose an option from the menu: ").lower()
        
        #if user selection contains spaces, cut it down to the first term before the space
        if " " in userSelection:
            newSelection = userSelection[:userSelection.index(" ")]
            print(f"Warning: input being shortened from \"{userSelection}\" to \"{newSelection}\"")
            userSelection = newSelection

        if "(" in userSelection or ")" in userSelection:
            print("Note that parentheses indicate which music .wad file is currently selected, and don't need to be typed when selecting an option")
            continue

        #skip doing anything if command is not a valid option
        if userSelection not in menuOptions.keys():
            print(f"Unknown menu option \"{userSelection}\"")
            continue
        
        #handle special options
        if userSelection == "q":
            print("Quitting...")
            break

        elif userSelection == "?":
            print(getHelpText())

        elif userSelection == "o":
            print("Opening music .wad directory. Remember to refresh music .wad list with \"r\" after adding or removing music .wad files")
            openDirectoryWindow(getMusicWadDirectory())

        elif userSelection == "r":
            print("Refreshing music .wad list...")
            continue

        elif userSelection == "0":
            print("Restoring original music...")
            try:
                applyMusicWad(getBackupFileName(fullPath=True))
            except PermissionError:
                #permission errors can happen if the file is currently in use (such as if the game is running)
                print("Could not access music .wad file; this is most often because the game is currently running.")
            else:
                setActiveWadName(None)

        else:
            selectedFileName = menuOptions[userSelection]
            print(f"Applying \"{selectedFileName}\"...")
            try:
                applyMusicWad(path.join(getMusicWadDirectory(), selectedFileName))
            except PermissionError:
                #permission errors can happen if the file is currently in use (such as if the game is running)
                print("Could not access music .wad file; this is most often because the game is currently running.")
            else:
                setActiveWadName(selectedFileName)

    
#return help text as a string
def getHelpText():
    helpText = """Hotline Miami 2 Music Changer (hlm2mc)
A tool to help manage custom music mods for Hotline Miami 2: Wrong Number

Hotline Miami 2 stores its music data in a file named "hlm2_music_desktop.wad"
Custom music mods are typically distributed as a .wad file (such as "custom_music.wad")
This program allows you to store several custom music .wad files, then select one from a list and apply it to your game.
It also automatically backs up the original music .wad file, allowing you to restore the original music at any time.

To add a custom music .wad file, simply place it in the music_wads directory (which can be opened from the main menu by selecting "o").
Note that the file must end with the extention ".wad" or it will not be detected.

The currently selected music .wad is indicated on the main menu by its option being in parentheses (such as "(0)").
To apply a different mod, type its corresponding number and press enter.
"""
    return helpText

#given the filepath of a music wad file, copies that file into the game
#raises ValueError if path is not to a wad file
#raises FileNotFoundError if wad file is not found
def applyMusicWad(wadFilePath:str):
    from os import path, remove
    from shutil import copy
    from hlm2_music_changer.dirtools import getMusicFileName

    #ensure wad file path ends with the .wad extention
    if not wadFilePath.endswith(".wad"):
        raise ValueError(f"File path \"{wadFilePath}\" is not a .wad file!")
    
    #ensure file exists
    if not path.exists(wadFilePath):
        raise FileNotFoundError(f"Wad file \"{wadFilePath}\" does not exist!")

    #ensure a backup file exists
    try:
        createMusicBackup()
    except FileExistsError:
        pass

    #remove the original music wad file
    musicFileName = getMusicFileName(fullPath=True)
    remove(musicFileName)

    #copy the new music wad file
    copy(wadFilePath, musicFileName)


#creates a backup of the original music wad 
#this file is called 'hlm2_original_music.wad' and is stored in the data directory (not the music mod directory)
#raises FileExistsError if hlm2_original_music.wad already exists
#raises FileNotFoundError if music wad file is not found in game directory
def createMusicBackup():
    from os import path
    from shutil import copy
    from hlm2_music_changer.dirtools import getMusicFileName, getBackupFileName

    #raise FileExistsError if backup already exists
    backupPath = getBackupFileName(fullPath=True)
    if path.exists(backupPath):
        raise FileExistsError(f"Cannot create backup at \"{backupPath}\" because it already exists!")

    #raise FileNotFoundError if original music wad can't be found
    originalPath = getMusicFileName(fullPath=True)
    if not path.exists(originalPath):
        raise FileNotFoundError(f"Original music file \"{originalPath}\" does not exist!")
    
    #if the original exists and the backup doesn't, create the backup
    copy(originalPath, backupPath)

if __name__ == "__main__":
    main()