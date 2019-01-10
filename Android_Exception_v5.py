import os.path
import datetime
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import zipfile
from collections import Counter
from jira import JIRA
import re
import ssl
import sys
import colorama
import sys
import os, colorama
from colorama import Fore,Style,Back
colorama.init()
os.system("mode con: cols=100 lines=50")



def createfolder():
    
    path = '\\\\10.0.16.86\\Handset_QC\\QC\\Sachiin\\Exception_Db\\'
    #path = 'D:\\9.0\\Script\\Logs\\'
    date = datetime.now()
    subfolder =  os.listdir(path)
    #print(date)
    Folder = str(date)[:10]
    #print (Folder)
    if (Folder in subfolder):
    	datePath = os.path.join(path,Folder)
    	subDirectory = os.listdir(datePath)
    	if (Tester in subDirectory):
    		print("Please copy all logs in below path if not copied earlier")
    		logpath = os.path.join(path,Folder,Tester)
    		print(os.path.join(path,Folder,Tester))
    	else:
    		os.mkdir(os.path.join(path,Folder,Tester))
    		print("Please copy all logs in below path")
    		logpath = os.path.join(path,Folder,Tester)
    		print(os.path.join(path,Folder,Tester))
    else:
        os.mkdir(os.path.join(path,Folder))
        os.mkdir(os.path.join(path,Folder,Tester))
        print("Please copy all logs in below path")
        logpath = os.path.join(path,Folder,Tester)
        print(os.path.join(path,Folder,Tester))

    createfolder_rvalue = [Folder,logpath]
    return createfolder_rvalue;

def parseUserAgent(fpath):
    #print "-------------- Enter parseUserAgent() --------------"
    #print (fpath)
    #print (fpath)

    if fpath.endswith('cbPTT'):
        pass
    elif fpath.endswith('cbPTX'):
        pass
    elif fpath.endswith('Analysis'):
        pass
    elif fpath.endswith('Audio'):
        pass
    elif fpath.endswith('Images'):
        pass
    elif fpath.endswith('Videos'):
        pass
    elif fpath.endswith('File'):
        pass
    else:
        filepath_New = os.path.join(fpath, 'poc_app_logs.txt')
        with open(filepath_New) as LogFile:
            if 'User-Agent' in LogFile.read():
                #print 'Line found in poc_app_logs.txt File'
                LogFilePath = filepath_New
            else:
                pass
        filepath_Old = os.path.join(fpath, 'poc_app_logs_old.txt')
        old_path = os.listdir(fpath)
        if ('poc_app_logs_old.txt' in old_path):
            with open(filepath_Old) as LogFile:
                if 'User-Agent' in LogFile.read():
                    #print 'Line found in poc_app_logs_old.txt File'
                    LogFilePath = filepath_Old
                else:
                    pass
        #print 'FilePath = '+ filepath_Old
        with open(LogFilePath) as fopen:
            #print ("File Opened")
            for line in  fopen:
                # print line
                pattern = 'User-Agent'
                index = line.find(pattern)
                if (index != -1):
                    #print line
                    OSFind = line.find('Android')
                    if (OSFind != -1):
                        #print "OS=Android"
                        linearray = line.split(' ')
                        DeviceName = linearray[2]
                        OSVersion_Temp = linearray[3].split('/')
                        Platform = OSVersion_Temp[0]
                        OS_Version = OSVersion_Temp[1]
                        ClientType_Temp = linearray[4].split('-')
                        if (ClientType_Temp[0] == 'knpoc'):
                            ClientType = 'Standard'
                            #print ClientType
                        else:
                            ClientType = 'Radio'
                        PLTTag = linearray[5]
                        CDETag_Temp = ClientType_Temp[1].split('/')
                        CDETag = CDETag_Temp[0]
                        TagDetail = 'Kodiak_PoC_CDE_' + CDETag + '\n' + PLTTag
                            #print ClientType
                        #print ('DeviceName = '+DeviceName +','+ 'Platform = '+ Platform +','+ 'OS Version = '+ OS_Version)
                        UseragentInfo = [DeviceName, Platform, OS_Version, ClientType,TagDetail]
                    else:
                        linearray = line.split(' ')
                        DeviceName = linearray[2]
                        OSVersion_Temp = linearray[3].split('/')
                        Platform = OSVersion_Temp[0]
                        OS_Version = OSVersion_Temp[1]
                        ClientType_Temp = linearray[4].split('-')
                        if (ClientType_Temp[0] == 'knpoc'):
                            ClientType = 'Standard'
                            #print ClientType
                        else:
                            ClientType = 'Radio'
                        PLTTag = linearray[5]
                        CDETag_Temp = ClientType_Temp[1].split('/')
                        CDETag = CDETag_Temp[0]
                        TagDetail = 'Kodiak_PoC_CDE_' + CDETag + '\n' + PLTTag
                            #print ClientType
                        #print ('DeviceName = '+DeviceName +','+ 'Platform = '+ Platform +','+ 'OS Version = '+ OS_Version)
                        UseragentInfo = [DeviceName, Platform, OS_Version, ClientType,TagDetail]
            #print "User-Agent Info: "
            #print  UseragentInfo
            #print "-------------- Exit parseUserAgent() --------------"
            return UseragentInfo;

def tagDetail(fpath,platform):
    #print "-------------Enter tagDetail()-------------"
    #print (fpath)
    #print (platform)
    #print "Inside tagDetail function"
    for dirName, subdirList, fileList in os.walk(fpath):
        #print('Found directory: %s' % dirName)
        for fname in fileList:
            # print('\t%s' % fname)
            if (platform == 'iOS'):
                if fname.lower().startswith('poc_ui_logs.txt'):
                    # print (fname)
                    filepath = os.path.join(dirName, fname)
                    #print 'FilePath = '+ filepath
                    fopen = open (filepath,'r')
                    #print ("File Opened")
                    for line in fopen:
                        patternCDE = 'CDE Tag'
                        patternPLT = 'PLT Tag'
                        patternUI = 'UI Tag'
                        indexCDE = line.find(patternCDE)
                        indexPLT = line.find(patternPLT)
                        indexUI = line.find(patternUI)
                        if (indexCDE != -1):
                            linearray = line.split(' ')
                            CDETag = 'Kodiak_PoC_CDE_'+linearray[2]
                            #print 'CDE Tag - '+CDETag
                        if (indexPLT != -1):
                            linearray = line.split(' ')
                            PLTTag = linearray[2]
                            #print 'PLT Tag - '+PLTTag
                        if (indexUI != -1):
                            linearray = line.split(' ')
                            UITag = linearray[2]
                            #print 'UI Tag - '+UITag
            else:
                 if fname.lower().startswith('poc_ui_logs.txt'):
                    # print (fname)
                    filepath = os.path.join(dirName, fname)
                    #print 'FilePath = '+ filepath
                    fopen = open (filepath,'r')
                    #print ("File Opened")
                    for line in fopen:
                        patternCDE = 'CDE Tag'
                        patternPLT = 'PLT Tag'
                        patternUI = 'UI Tag'
                        indexCDE = line.find(patternCDE)
                        indexPLT = line.find(patternPLT)
                        indexUI = line.find(patternUI)
                        if (indexCDE != -1):
                            linearray = line.split(' ')
                            CDETag = 'Kodiak_PoC_CDE_'+linearray[4]
                            #print 'CDE Tag - '+CDETag
                        if (indexPLT != -1):
                            linearray = line.split(' ')
                            PLTTag = linearray[4]
                            #print 'PLT Tag - '+PLTTag
                        if (indexUI != -1):
                            linearray = line.split(' ')
                            UITag = linearray[4]
                            #print 'UI Tag - '+UITag           
    
    tagDetail_rvalue = CDETag + PLTTag +UITag
    #print tagDetail_rvalue
    #print "------------- Exit tagDetail() -------------"
    return tagDetail_rvalue

def ExceptionInfo_To_ghseet(data):
    global new
    global existing
    #print '----------- Enter ExceptionInfo_To_ghseet() -------------- '
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    wb = client.open("Overnight_IdleLog_Analysis")
    sheet = wb.worksheet('Exception')


    # read col values
    value_col_excep_list = sheet.col_values(4)
    value_col_stack_list = sheet.col_values(5)
    value_col_prid_list = sheet.col_values(9)
    #print value_col_prid_list
    exception_line = data[3]
    stack_line = data[4]
    open_state = ['ENGINEERING ASSIGNED','ENGINEERING SUPPORT']
    raise_state = ['Closed','TESTER ASSIGNED','TEST INPUT REQUIRED']
    row = data
    index = 2
    col = 0
    flag = 0 
    for i in value_col_stack_list:
        if (data[4] == i):
            if (data[3] == value_col_excep_list[col]):
                flag = 1
                existing = existing + 1
                #print value_col_prid_list[col]
                if (value_col_prid_list[col] == ''):
                    value_col_prid_list[col] = 'Nill'
                    #print 'nnniilllll'
                jiira_stat_return_data = JIIRA_STATUS(value_col_prid_list[col], stack_line)
                jira_return_data = str(jiira_stat_return_data[1])
                jira_id = str(jiira_stat_return_data[0])
                #print jira_return_data
                if (jira_return_data in open_state):
                    value_col_prid_list[col] = jira_id
                    sheet.update_cell(col+1, 9,value_col_prid_list[col])
                    print ('---------------------------------------------')
                    print Fore.WHITE+Back.GREEN+'Existing PR: ' +jira_id , ' PR status is::' +jira_return_data ,'No need to raise PR'+Style.RESET_ALL 
                    print ('---------------------------------------------')
                elif(jira_return_data in raise_state):
                    value_col_prid_list[col] = jira_id
                    sheet.update_cell(col+1, 9,value_col_prid_list[col])
                    print ('---------------------------------------------')
                    print Fore.WHITE+Back.RED+'PR Status is:: ' +jira_return_data , 'Please check and reopen the Existing PR::' +value_col_prid_list[col]
                    print 'For below Exception::' +exception_line + Style.RESET_ALL
                    print ('---------------------------------------------')
                elif(jira_return_data == '-8'):
                    print ('---------------------------------------------')
                    print Fore.WHITE+Back.RED+ 'You have to raise PR for the below exception as somebody didnot raise it after observing : ' + exception_line + Style.RESET_ALL
                    print ('---------------------------------------------')
                else:
                    value_col_prid_list[col] = jira_id
                    #print value_col_prid_list[col]
                    #sheet.insert_row(row, index)
                    sheet.update_cell(col+1, 9,value_col_prid_list[col])
                    print Fore.WHITE+Back.GREEN +'PR id added to the sheet' + Style.RESET_ALL

            else:
                #print '--------Inside For Loop -----'
                jira_return_data = JIIRA(stack_line)
                if (jira_return_data != -1):
                    pr_id = str(jira_return_data[0])
                    pr_status = str(jira_return_data[1])
                    #data[8] = pr_id
                    value_col_prid_list[col] = pr_id
                    sheet.insert_row(row, index)
                    sheet.update_cell(col+1, 9,value_col_prid_list[col])
                    print Fore.WHITE+Back.GREEN +'Existing PR in JIRA:' +pr_id , 'for the below Exception:' +exception_line
                    if(pr_status in open_state):
                        print 'No need to raise PR. PR status is::' +pr_status + Style.RESET_ALL
                        print ('---------------------------------------------')
                    else:
                        print Fore.WHITE+Back.RED+'Please Verify tag details and Reopen the PR::' +pr_id + Style.RESET_ALL
                else:
                    new = new +1
                    sheet.insert_row(row, index)
                    print ('---------------------------------------------')
                    print ('You have to raise PR for the below exception as the Stack is different : ' + exception_line)
                    print ('---------------------------------------------')
                #sheet.insert_row(row, index)
                #JIRA(value_col_excep_list[col])
                #new = new +1
                #print ('You Got A New Exception from this device logs, please raise in JIRA.')
                #print ('---------------------------------------------')
                flag = 1
        else:
            col = col + 1
    if (flag == 0):
        #print '------- Outside For Loop--------'
        #print value_col_excep_list
        jira_return_data = JIIRA(stack_line)
        #print jira_return_data
        if (jira_return_data != -1):
            pr_id = str(jira_return_data[0])
            pr_status = str(jira_return_data[1])
            #data[8] = pr_id
            sheet.insert_row(row, index)
            print Fore.WHITE+Back.GREEN +'Existing PR in JIRA:' +pr_id , 'for the below Exception:' +exception_line
            if(pr_status in open_state):
                print 'No need to raise PR.PR status is::' +pr_status + Style.RESET_ALL
                print ('---------------------------------------------')
            else:
                print Fore.WHITE+Back.RED+'Please check and reopen the Existing PR::' +pr_id , 'PR State is :' +pr_status+ Style.RESET_ALL
        else:
            new = new +1
            sheet.insert_row(row, index)
            print ('---------------------------------------------')
            print Fore.WHITE+Back.RED+'You have to raise PR for the below exception: ' + exception_line+ Style.RESET_ALL
            print ('---------------------------------------------')

    NewExisting_rvalue = [new,existing]
    #print NewExisting_rvalue
    #print (")))))))))))))))))))))))))))))))))")
    #print '----------- Exit ExceptionInfo_To_ghseet() -------------- '
    return NewExisting_rvalue

        
def JIIRA(data):
    options = {
    'server': 'https://jira.kodiakptt.com'}
    jira = JIRA(options , basic_auth=('psachin', 'Whitecollar!11'))
    #issue = jira.search_issues("project = INT", "summary", "Channel")
    #jql_str = Exception'
    #data = ''.join(data)
    #print data
    data = data.replace('\t', '')
    if ("'" in data):
        #print 'inside if'
        data = str(data.replace("'", " "))
    else:
        pass
    string2 = "project='INT' AND description~ '"+data+"'"
    #print string2
    query = jira.search_issues(string2)
        
    #print query
    if(len(query) == 0):
        #print ('No Exisiting PR found in JIRA for the Exception.')
        return -1
    else:
        pr_state = str(query[0].fields.status)
        jira_data = [query[0].key,pr_state]
        #print jira_data
        return jira_data


def JIIRA_STATUS(data,data2):
    options = {
    'server': 'https://jira.kodiakptt.com'}
    jira = JIRA(options , basic_auth=('psachin', 'Whitecollar!11'))
    #print data
    #print data2
    if (data != 'Nill'):
        issue = jira.issue(data)
        #print issue.fields.status
        id_status = [data, issue.fields.status]
        #print id_status
        return id_status
    else:
        data2 = str(data2.replace('\t', ''))
        if ("'" in data2):
            #print 'inside if'
            data2 = str(data2.replace("'", " "))
        string3 = "project='INT' AND description~ '"+data2+"'"
        query = jira.search_issues(string3)
        #print query
        if (len(query) == 0):
            return_data = ['-8','-8']
            return return_data
        else:
            #issue = jira.issue(data)
            return_data =[str(query[0].key), str(query[0].fields.status)]
            #print return_data
            return return_data


       #print(i.key)

def step(arr):
	#print '------------- Enter function step() ---------'
	global flag
	global matchcount
	fpath = arr[0]
	TName = arr[1]
	DateFolder = arr[2]
	TagDetail = arr[3]
	LogPath = arr[4]
	#print ' --- Inside Else ---'
        for dirName, subdirList, fileList in os.walk(fpath):
            for fname in fileList:
                if fname.lower().startswith('poc_ui_logs.txt'):
                    fname = os.path.join(fpath,'poc_ui_logs.txt')
                    #flist = os.listdir(fpath)
                    #if ("poc_ui_logs.txt" in flist):
                    with open(fname) as fp:
                        line = fp.readline()
                        while line:
                            index = line.find('Exception')
                            if (index != -1):
                                x = line.find('[')
                                timestamp = line[x+1 : x+19]
                                x = line.rfind(']')
                                exception = line[x+1 : ]
                                temp = line
                                line = fp.readline()
                                if (line[0] == "["):
                                    pass
                                elif (line[0] == "\n"):
                                    pass
                                else:
                                    # TO DO  - write to gsheet
                                    stack = line
                                    #print line
                                    if("JavaBridge" in temp):
                                        #print 'rrrrrrrrrrrrrrrr'
                                        while (line.find('JavaBridge') == -1):
                                            #print line
                                            if (stack == line):
                                                pass
                                            else:
                                                #print 'else'
                                                stack = stack  + line
                                            line = fp.readline()
                                    else:
                                        while (line.find('HTML5LOG') == -1):
                                            if (stack == line):
                                                pass
                                            else:
                                                stack = stack  + line
                                            line = fp.readline()
                                    #print newstr
                                    Module = 'UI'
                                    Exception_Data = [TName,DateFolder,Module,exception,stack,timestamp,TagDetail,LogPath]
                                    #print Exception_Data
                                    matchcount = ExceptionInfo_To_ghseet(Exception_Data)
                                    #print ("----------------------------")
                            line = fp.readline()
                if fname.lower().startswith('poc_ui_logs_old.txt'):
                    fname = os.path.join(fpath,'poc_ui_logs_old.txt')
                    #flist = os.listdir(fpath)
                    #if ("poc_ui_logs.txt" in flist):
                    with open(fname) as fp:
                        line = fp.readline()
                        while line:
                            index = line.find('Exception')
                            if (index != -1):
                                x = line.find('[')
                                timestamp = line[x+1 : x+19]
                                x = line.rfind(']')
                                exception = line[x+1 : ]
                                temp = line
                                line = fp.readline()
                                if (line[0] == "["):
                                    pass
                                elif (line[0] == "\n"):
                                    pass
                                else:
                                    # TO DO  - write to gsheet
                                    stack = line
                                    if("JavaBridge" in temp):
                                        while (line.find('JavaBridge') == -1):
                                            if (stack == line):
                                                pass
                                            else:
                                                stack = stack  + line
                                            line = fp.readline()
                                    else:
                                        while (line.find('HTML5LOG') == -1):
                                            if (stack == line):
                                                pass
                                            else:
                                                stack = stack  + line
                                            line = fp.readline()
                                    #print newstr
                                    Module = 'UI'
                                    Exception_Data = [TName,DateFolder,Module,exception,stack,timestamp,TagDetail,LogPath]
                                    #print Exception_Data
                                    matchcount = ExceptionInfo_To_ghseet(Exception_Data)
                                    #print ("----------------------------")
                            line = fp.readline()
                if fname.lower().endswith('.zip'):
                    pass
                    # fpathz = os.path.join(fpath, fname)
                    # print fpathz
                    # zfile = zipfile.ZipFile(fpathz)
                    # for filename in ['poc_ui_logs_old.txt']:
                    #     with zfile.open(filename) as fp:
                    #         line = fp.readline()
                    #         while line:
                    #             index = line.find('Exception')
                    #             if (index != -1):
                    #                 x = line.find('[')
                    #                 timestamp = line[x+1 : x+19]
                    #                 x = line.find('E')
                    #                 exception = line[x : ]
                    #                 temp = line
                    #                 line = fp.readline()
                    #                 if (line[0] == "["):
                    #                     pass
                    #                 elif (line[0] == "\n"):
                    #                     pass
                    #                 else:
                    #                     # TO DO  - write to gsheet
                    #                     stack = line
                    #                     while (line.find('JavaBridge') == -1):
                    #                         #line = fp.readline()
                    #                         if (stack == line):
                    #                             pass
                    #                         else:
                    #                             stack = stack  + line
                    #                         line = fp.readline()
                    #                     #print newstr
                    #                     Module = 'UI'
                    #                     Exception_Data = [TName,DateFolder,Module,exception,stack,timestamp,TagDetail,LogPath]
                    #                     #print Exception_Data
                    #                     matchcount = ExceptionInfo_To_ghseet(Exception_Data)
                    #             line = fp.readline()
                else:
                    pass
                if fname.lower().startswith('poc_plt_logs.txt'):
                    fname = os.path.join(fpath,'poc_plt_logs.txt')
                    with open(fname) as fp:
                        line = fp.readline()
                        while line:
                            index = line.find('Exception')
                            if (index != -1):
                                x = line.find('[')
                                timestamp = line[x+1 : x+19]
                                x = line.rfind(']')
                                exception = line[x+1 : ]
                                temp = line
                                line = fp.readline()
                                if (line[0] == "["):
                                    pass
                                elif (line[0] == "\n"):
                                    pass
                                else:
                                    # TO DO  - write to gsheet
                                    stack = line
                                    while (line.find('[') == -1):
                                        #line = fp.readline()
                                        if (stack == line):
                                            pass
                                        else:
                                            stack = stack  + line
                                        line = fp.readline()
                                    #print newstr
                                    Module = 'PLT'
                                    Exception_Data = [TName,DateFolder,Module,exception,stack,timestamp,TagDetail,LogPath]
                                    #print Exception_Data
                                    matchcount = ExceptionInfo_To_ghseet(Exception_Data)
                                    #print ('returnnnnnnnnnnnnnnnnn')
                                    #Write_data[0]
                            line = fp.readline()
                else:
                    NoException = 1
                    pass
                if fname.lower().startswith('poc_plt_logs_old.txt'):
                    fname = os.path.join(fpath,'poc_plt_logs_old.txt')
                    with open(fname) as fp:
                        line = fp.readline()
                        while line:
                            index = line.find('Exception')
                            if (index != -1):
                                x = line.find('[')
                                timestamp = line[x+1 : x+19]
                                x = line.rfind(']')
                                exception = line[x+1 : ]
                                #print exception
                                temp = line
                                line = fp.readline()
                                if (line[0] == "["):
                                    pass
                                elif (line[0] == "\n"):
                                    pass
                                else:
                                    # TO DO  - write to gsheet
                                    stack = line
                                    while (line.find('[') == -1):
                                        #line = fp.readline()
                                        if (stack == line):
                                            pass
                                        else:
                                            stack = stack  + line
                                        line = fp.readline()
                                    #print newstr
                                    Module = 'PLT'
                                    Exception_Data = [TName,DateFolder,Module,exception,stack,timestamp,TagDetail,LogPath]
                                    #print Exception_Data
                                    matchcount = ExceptionInfo_To_ghseet(Exception_Data)
                                    #print ('returnnnnnnnnnnnnnnnnn')
                                    #Write_data[0]
                            line = fp.readline()
                else:
                    NoException = 1
                    pass

        #print '----------- Exit step() -------------- '

while True:
    # Loop continue
    # Set the directory you want to start from
    #Filepath = raw_input("Enter path : ")
    print ('-----------------------------------------------------------')
    Tester = raw_input(Fore.MAGENTA +"ENTER YOUR NAME : "+ Style.RESET_ALL)
    print ('-----------------------------------------------------------')
    # User input for string to search
    print ('')
    exten = '.txt'
    matchcount = 0
    NoException = 0
    new = 0
    existing = 0
    Write_data = 0
    createFolder_Data = createfolder()
    date_data = createFolder_Data[0]
    FilePath= createFolder_Data[1]

    rootDir = FilePath
    print ('-----------------------------------------------------------')
    prompt = raw_input("Have you copied the logs?<y/n> : ")
    print ('-----------------------------------------------------------')
    if prompt.lower() == "y":
       #DeviceInfo = parseUserAgent(FilePath)
       print
       subFolderList = os.listdir(FilePath)
       for subdir in subFolderList:
        FilePath = os.path.join(rootDir,subdir)
        #print FilePath
        subsubFolderList = os.listdir(FilePath)
        #print subsubFolderList
        if ('PTT' in subsubFolderList):
            FilePath = os.path.join(FilePath,'PTT')
            #print FilePath
            for dirName,subDirName,fileList in os.walk(FilePath):
                dirpath = dirName
                #print dirName
                #print subDirName
                if (dirpath == rootDir):
                    pass
                elif dirName.endswith('Analysis'):
                	pass
                elif dirName.endswith('cbPTX'):
                	pass
                elif dirName.endswith('cbPTT'):
                	pass
                elif dirName.endswith('Audio'):
                    pass
                elif dirName.endswith('Images'):
                    pass
                elif dirName.endswith('Videos'):
                    pass
                elif dirName.endswith('File'):
                    pass
                else:
                    #print ('-------------------------')                    
                    #print ('Please Wait ...')
                    #print ('-------------------------')
                    DeviceInfo = parseUserAgent(dirName)
                    if DeviceInfo[1] == 'iOS':
                        print Fore.CYAN+'iOS not supported yet.'+ Style.RESET_ALL
                        ios = 1
                        break
                    print '***********************************************************************'
                    print (Fore.CYAN +'VALIDATING LOGS FOR DEVICE : ' + DeviceInfo[0] + Style.RESET_ALL)
                    print 'Please wait...'
                    print ('')
                    #TagInfo = tagDetail(dirName,DeviceInfo[1])
                    stepFunction_Data = [dirName, Tester, date_data,DeviceInfo[4],FilePath]
                    step(stepFunction_Data)
                    print '***********************************************************************'
        else:
            for dirName,subDirName,fileList in os.walk(FilePath):
                dirpath = dirName
                #print dirName
                #print subDirName
                if (dirpath == rootDir):
                    pass
                elif dirName.endswith('Analysis'):
                    pass
                elif dirName.endswith('cbPTX'):
                    pass
                elif dirName.endswith('cbPTT'):
                    pass
                elif dirName.endswith('Audio'):
                    pass
                elif dirName.endswith('Images'):
                    pass
                elif dirName.endswith('Videos'):
                    pass
                elif dirName.endswith('File'):
                    pass
                else:
                    #print ('---------------------------')
                    #print ('Please Wait ...')
                    #print ('---------------------------')
                    #pass
                    DeviceInfo = parseUserAgent(dirName)
                    if DeviceInfo[1] == 'iOS':
                        print Fore.CYAN+'iOS not supported yet.'+ Style.RESET_ALL
                        ios = 1
                        break
                    print '***********************************************************************'
                    print (Fore.CYAN + 'VALIDATING LOGS FOR DEVICE : ' + DeviceInfo[0] + Style.RESET_ALL)
                    print 'Please wait...'
                    print ('')
                    #TagInfo = tagDetail(dirName,DeviceInfo[1])
                    #print (TagInfo)
                    stepFunction_Data = [dirName, Tester, date_data,DeviceInfo[4],FilePath]
                    step(stepFunction_Data)
                    print '***********************************************************************'
    #print matchcount
    print ('')
    if (ios != 1):
        if ( matchcount == 0):
            print ('')
            print Fore.GREEN + 'NO EXCEPTION FOUND :) :) :)' + Style.RESET_ALL
            print ('')
        else:
            print ('------------------------------------------------------------------')
            print Fore.WHITE+Back.GREEN+'SEARCH RESULTS:                                                     '+ Style.RESET_ALL
            print 'New Exception observed     :  ' + str(matchcount[0])
            print 'Existing Exception observed:  ' + str(matchcount[1]) 
            print ('------------------------------------------------------------------')
            print ('')
            print ('------------------------------------------------------------------')
            print Fore.WHITE+Back.GREEN+ 'Please find the result updated in below GSheet' + Style.RESET_ALL
            print Fore.WHITE+Back.MAGENTA+'URL : https://tinyurl.com/y8p8bkg9'+ Style.RESET_ALL
            print ('------------------------------------------------------------------')
            print ('')
    user_input = raw_input('Do you want to quit ? [Y/N] :')
    if user_input.lower() == "y":
        break