#hlm2_music_changer dirtools
#directory management helper functions

#returns either a string of the currently in-place music .wad file
#or None if there is no custom music currently in place
def getActiveWadName():
    from os import path
    filepath = getActiveWadStorageFileName(fullPath=True)

    if not path.exists(filepath):
        return None
    else:
        with open(filepath, "r") as inFile:
            activeName = inFile.read()
        
        if '\n' in activeName:
            activeName = activeName[:activeName.index('\n')]
        
        #verify that the name refers to a file actually in the list of music wad files
        #only return name if it is a real .wad file
        if activeName in getMusicWadList():
            return activeName
        else:
            return None

#stores the active wad name in a file for later retrieval with getActiveWadName
#pass wadName of None if active wad is the original music
#raises ValueError if wadName is not a valid wad name or None
def setActiveWadName(wadName):
    filepath = getActiveWadStorageFileName(fullPath=True)

    #if wadName is None, store an empty file to indicate original music
    if wadName == None:
        with open(filepath, "w"):
            #do nothing, creating an empty file
            pass
    
    elif wadName in getMusicWadList():
        with open(filepath, "w") as outFile:
            outFile.write(wadName)
    
    else:
        raise ValueError(f"Could not store \"{wadName}\" as active wad name because that file doesn't exist")
    

    

#returns a list of music wad names
#these music wads must be located in the music wad directory (as returned by dirtools.getMusicWadDirectory)
def getMusicWadList():
    from os import listdir, path

    musicWadDir = getMusicWadDirectory()

    #get a list of the contents of the music directory
    musicWadContents = listdir(musicWadDir)

    #iterate through musicWadContents (which may contain files and directories)
    #to get a list of files ending with the '.wad' extention
    wadFileNames = []
    for filename in musicWadContents:
        if filename.endswith(".wad"):
            if path.isfile(path.join(musicWadDir, filename)):
                wadFileNames.append(filename)

    return wadFileNames

#opens a filesystem viewer window at the specified directory
#(e.g. opens File Explorer on Windows, Finder on OS X, etc)
#developed + tested on Windows 10, tested once on Ubuntu
#all other platforms *should* work but your results may vary
def openDirectoryWindow(directoryPath):
    from platform import system
    from subprocess import Popen #used on linux and os x


    systemname = system()
    if systemname == "Windows":
        from os import startfile
        startfile(directoryPath)

    elif systemname == "Linux":
        Popen(["xdg-open", directoryPath])

    elif systemname == "Darwin": #OS X
        Popen(["open", directoryPath])
    else:
        raise NotImplementedError(f"openDirectoryWindow not implemented for platform {systemname}")
        

#returns the active wad storage filename as a string
#if fullPath is true, returns the full path the file within the data directory
#if fullPath is false (the default), returns only the filename
def getActiveWadStorageFileName(fullPath = False):
    name = "activewad.txt"

    if not fullPath:
        return name
    else:
        from os import path
        return path.join(getConfigDirectory(), name)

#returns the music wad file name as a string
#music wads MUST be renamed to this in order to work
#if fullPath is true, returns the full path the file within the game directory
#if fullPath is false (the default), returns only the filename
def getMusicFileName(fullPath = False):
    name = "hlm2_music_desktop.wad"

    if not fullPath:
        return name
    else:
        from os import path
        return path.join(getGameDirectory(), name)

#returns the filename used for the backup music file
#if fullPath is true, returns the full path the file within the data directory
#if fullPath is false (the default), returns only the filename
def getBackupFileName(fullPath = False):
    name = "BACKUP_hlm2_music_desktop.wad"

    if not fullPath:
        return name
    else:
        from os import path
        return path.join(getDataDirectory(), name)


#returns an AppDirs object containing directories used by this application
def getAppDirs():
    from appdirs import AppDirs
    return AppDirs("hlm2_music_changer", "generic-user1")


#returns the configuration directory as a string
#ensures this directory exists and creates it if it does not
def getConfigDirectory():
    from os import path, makedirs
    configDir = getAppDirs().user_config_dir

    if not path.exists(configDir):
        makedirs(configDir)

    return configDir

#returns the data directory as a string
#ensures this directory exists and creates it if it does not
def getDataDirectory():
    from os import path, makedirs

    dataDir = getAppDirs().user_data_dir

    if not path.exists(dataDir):
        makedirs(dataDir)

    return dataDir

#returns the music wad directory as a string
#ensures this directory exists and creates it if it does not
def getMusicWadDirectory():
    from os import path, makedirs

    musicModDir = path.join(getDataDirectory(), "music_wads")
    if not path.exists(musicModDir):
        makedirs(musicModDir)

    return musicModDir

#returns True if provided directory contains an instance of the game
#returns False if provided directory does not contain the game 
def validateGameDir(gameDir:str) -> bool:
    from os import path
    #get the filepath of the data wad file
    dataWadFilePath = path.join(gameDir, "hlm2_data_desktop.wad")

    #check if the data wad file exists and return result
    return path.exists(dataWadFilePath)

#checks for a stored game directory
#if none is found, prompts user to input game directory, then validates and stores their input
#in either case, returns the game directory
def getGameDirectory():
    from os import path

    #get the path of the file used to store the game directory path
    gameDirStorageFilePath = path.join(getConfigDirectory(), "gamedir.txt")

    if path.exists(gameDirStorageFilePath):
        with open(gameDirStorageFilePath, "r") as inFile:
            gamedir = inFile.read()
            if '\n' in gamedir:
                gamedir = gamedir[:gamedir.index('\n')]

        #if stored gamedir passes validation, return it
        if validateGameDir(gamedir):
            return gamedir

        #if gamedir fails validation, proceed as though there was no gamedir file    
    
    print("Game directory unknown.")
    while True:
        gamedir = input("Please input the path to your Hotline Miami 2 game installation: ")
        if validateGameDir(gamedir):
            #store new gamedir
            with open(gameDirStorageFilePath, "w") as outFile:
                outFile.write(gamedir)

            return gamedir
        
        #if gamedir fails validation, print message and prompt again
        print(f"Hotline Miami 2 was not found at provided path \"{gamedir}\"")

