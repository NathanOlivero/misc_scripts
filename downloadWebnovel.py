from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import requests, sys, os, bs4, threading, math, time, re
from os import walk

################################################################################
# function definitions
################################################################################
def printDownloadProgress(printStatement):
    downloadProgress_Lbl.insert(INSERT, str(printStatement))
    downloadProgress_Lbl.update()

def setDownloadFolderPath(*args):
    downloadFolderPath.set(filedialog.askdirectory())

################## downloadWebnovelChapters ####################################
def downloadWebnovelChapters(webnovelURL, webnovelChaptersFolderPath, startChapterNum, endChapterNum, finalChapterFlag):
    for currentChapterNum in range(startChapterNum, (endChapterNum+1)):
        # Download the page.
        if (finalChapterFlag==True) and (currentChapterNum==endChapterNum):
            currentChapterURL = webnovelURL + "/chapter-" + str(currentChapterNum) + "-end"
        else:
            currentChapterURL = webnovelURL + "/chapter-" + str(currentChapterNum)
        print("Downloading page: " + currentChapterURL)
        res = requests.get(currentChapterURL)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        # Find the webnovel chapter text.
        novelTextElement = soup.find_all('div', attrs={"class":"reading-content"})
        if novelTextElement == []:
            print("NOTICE: Could not get " + currentChapterURL + " text")
        # elif novelTextElement[0].get_text().encode() == b'\n': #Empty page
        #     print("NOTICE: " + currentChapterURL + " does not exist")
        else:
            chapterTextFile = open(os.path.join(webnovelChaptersFolderPath, os.path.basename(currentChapterURL)), 'w',encoding='utf-8') # Individual chapter file
            try:
                for textItem in novelTextElement:
                    chapterTextFile.write(textItem.text)
            finally:
                chapterTextFile.close()
# END downloadWebnovelChapters

########################## downloadWebnovel ####################################
def downloadWebnovel(webnovelURL, downloadFolderPath):
    webnovelTitle = os.path.basename(webnovelURL.rstrip('/'))
    webnovelFolderPath = downloadFolderPath + "\\" + webnovelTitle
    webnovelChaptersFolderPath = webnovelFolderPath + "\\Chapters"

    # Check if valid webnovel URL
    try:
        res = requests.get(webnovelURL)
        res.raise_for_status()
        printDownloadProgress("Starting download for " + webnovelTitle + "\n")
    except requests.HTTPError as exception:
        printDownloadProgress(exception)
        print(exception)
    except requests.exceptions.MissingSchema as exception:
        printDownloadProgress(exception)
        print(exception)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    novelChapterLinks = soup.find_all('li', attrs={"class":"wp-manga-chapter"})
    if novelChapterLinks == []:
        printDownloadProgress(("\nERROR: Could not find \"" + os.path.basename(webnovelURL.rstrip('/')) + "\". Please use a valid URL."))
        print("\nERROR: Could not find " + os.path.basename(webnovelURL.rstrip('/')) + "\nPlease use a valid URL.")
        return
    else: # Determine total number of chapters
        firstChapterLink = novelChapterLinks[-1].find('a')['href']
        firstChapterNumStr = os.path.basename(firstChapterLink.rstrip('/'))
        firstChapterNum = int(''.join(filter(str.isdigit, firstChapterNumStr)))

        lastChapterLink = novelChapterLinks[0].find('a')['href']
        lastChapterNumStr = os.path.basename(lastChapterLink.rstrip('/'))
        lastChapterNum = int(''.join(filter(str.isdigit, lastChapterNumStr)))

    # Create folders
    os.makedirs(webnovelFolderPath, exist_ok=True) # store compiled novel in folder
    os.makedirs(webnovelChaptersFolderPath, exist_ok=True) # store individual chapters in folder

    # Create and Start Threads
    threadList = []
    NUM_OF_THREADS = 4
    numWebRequestPerThread = math.ceil(lastChapterNum/NUM_OF_THREADS)
    finalChapterFlag = False
    for i in range(firstChapterNum,lastChapterNum,numWebRequestPerThread):
        startChapterNum = i
        endChapterNum = (i + numWebRequestPerThread)
        if endChapterNum > lastChapterNum:
            endChapterNum = lastChapterNum
            finalChapterFlag = True
        threadItem = threading.Thread(target=downloadWebnovelChapters, args=(webnovelURL, webnovelChaptersFolderPath, startChapterNum, endChapterNum, finalChapterFlag), daemon=True)
        threadList.append(threadItem)
        threadItem.start()

    printDownloadProgress("\nDownloading")
    # Wait for all download Threads to end
    for threadItem in threadList:
        while threadItem.is_alive():
            time.sleep(2)
            printDownloadProgress('.')
        threadItem.join()

    # Consolidate all chapters into one file
    chapterFileNames = []
    for (_, _, filenames) in walk(webnovelChaptersFolderPath):
        chapterFileNames.extend(filenames)
    # Sort filenames in ascending numerical order
    chapterFileNames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    webnovelCombinedFileName = "all-chapters-combined"
    webnovelCombinedTextFile = open(os.path.join(webnovelFolderPath, webnovelCombinedFileName), 'a',encoding='utf-8')
    for chapterFileName in chapterFileNames:
        try:
            chapterTextFile = open(os.path.join(webnovelChaptersFolderPath, os.path.basename(chapterFileName)), 'r',encoding='utf-8')
            chapterText = chapterTextFile.read()
            webnovelCombinedTextFile.write(chapterText)
        finally:
            chapterTextFile.close()
    webnovelCombinedTextFile.close()

    printDownloadProgress('\nDownload Complete.')
# END downloadWebnovel

################################################################################
# END function definitions
################################################################################

root = Tk()
root.title("Download Webnovel")
root.bind('<Return>', printDownloadProgress)
rootWidth = 800
rootHeight = 300
screenWidth= root.winfo_screenwidth() # width of the screen
screenHeight = root.winfo_screenheight() # height of the screen
rootXCoordinate = (screenWidth/2) - (rootWidth/2)
rootYCoordinate = (screenHeight/2) - (rootHeight/2)
root.geometry('%dx%d+%d+%d' % (rootWidth, rootHeight, rootXCoordinate, rootYCoordinate))
root.minsize(rootWidth, rootHeight)

webnovelURL = StringVar()
webnovelURL.set("https://boxnovel.com/novel/omniscient-readers-viewpoint/")
downloadFolderPath = StringVar()
downloadFolderPath.set(os.path.join(os.path.expanduser('~'), 'downloads')) #Default download folder

# Add Widgets
mainFrame = ttk.Frame(root, padding=(3,3,3,12))
webnovelUrl_Lbl = ttk.Label(mainFrame, text="Webnovel URL:")
webnovelDownloadFolder_Lbl = ttk.Label(mainFrame, text="Download to Folder:")
downloadProgress_Lbl = Text(mainFrame, background="white", wrap="word", yscrollcommand=set())
webnovelUrl_Entry = ttk.Entry(mainFrame, textvariable=webnovelURL)
webnovelUrl_Entry.focus()
webnovelDownloadFolder_Entry = ttk.Entry(mainFrame, textvariable=downloadFolderPath)
download_Btn = ttk.Button(mainFrame, text="Download", command=lambda : downloadWebnovel(webnovelURL.get(), downloadFolderPath.get()))
webnovelDownloadFolder_Btn = ttk.Button(mainFrame, text="Select Folder", command=setDownloadFolderPath)

# Grid Specifications
mainFrame.grid(column=0, row=0, sticky=(N, S, E, W))
webnovelUrl_Lbl.grid(column=0, row=0, sticky=(N, W), pady=5, padx=5)
downloadProgress_Lbl.grid(column=0, row=2, columnspan=3, sticky=(N, S, E, W), pady=5, padx=5)
webnovelDownloadFolder_Lbl.grid(column=0, row=1, sticky=(N, S, E, W), pady=5, padx=5)
webnovelUrl_Entry.grid(column=1, row=0, sticky=(N, E, W), pady=5, padx=5)
webnovelDownloadFolder_Entry.grid(column=1, row=1, sticky=(N, E, W), pady=5, padx=5)
download_Btn.grid(column=2, row=0)
webnovelDownloadFolder_Btn.grid(column=2, row=1)

# Column and Row Configurations
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainFrame.columnconfigure(1, weight=1)
mainFrame.rowconfigure(2, weight=1)

root.mainloop()
