# Mailsort is a gmail sorting application created in Python 
# Created by https://github.com/Splintaz/
import imaplib
import getpass
import re
import email
import os 
from pathlib import Path
import shutil

def partition():
    stage = str(mailboxes[choose_mailbox-1])
    stage2 = stage.partition("/")
    stage3 = stage2[2].replace('"', "") # 3 PARTITIONS!
    stage4 = stage3.replace("'", "")
    stage5 = stage4.replace(" ", "")
    M.select(stage5)
    read_mailbox()
    
def read_mailbox():
    global checker
    global mail_content
    attachment = input("What do you wish to do with the emails that have attachments? [downloadall/skipall/manual] ")
    try:
        os.chdir("C:/")
    except:
        exit("Seems like you don't have a C drive!")
    try:
        os.mkdir("mailsort")
    except FileExistsError:
        pass
    try:
        status, data = M.search(None, "ALL")
        mail_ids = []
        for block in data:
            mail_ids += block.split()
        for i in mail_ids:
            status, data = M.fetch(i, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])
                    mail_from = message["from"]
                    mail_subject = message["subject"]
                    if message.is_multipart():
                        mail_content = ""
                        for part in message.get_payload():
                            content_disposition = str(part.get("Content-Disposition"))
                            if part.get_content_type() == "text/plain":
                                mail_content += part.get_payload(decode=True).decode()
                                print(f"From: {mail_from}")
                                print(f"Subject: {mail_subject}")
                                print(f"Content: {mail_content}")
                            fileName = part.get_filename()
                            if bool(fileName):
                                if attachment == "manual":
                                    checker = True
                                    download_attachment = input(f"Do you wish to download '{fileName}' from '{mail_from}'? [Y/N] ")
                                    if download_attachment == "Y":
                                        filePath = os.path.join('mailsort/', fileName)
                                        if not os.path.isfile(filePath):
                                            fp = open(filePath, 'wb')
                                            fp.write(part.get_payload(decode=True))
                                            fp.close()
                                        print(f"Downloaded {fileName} from '{mail_from}' with the subject '{mail_subject}'")
                                    else:
                                        print(f"Skipping '{fileName}'")
                                elif attachment == "downloadall":
                                    checker = True
                                    filePath = os.path.join('mailsort/', fileName)
                                    if not os.path.isfile(filePath):
                                        fp = open(filePath, 'wb')
                                        fp.write(part.get_payload(decode=True))
                                        fp.close()
                                    print(f"Downloaded {fileName} from '{mail_from}' with the subject '{mail_subject}'")
                                else:
                                    checker = False
                                    print("Skipping all emails with attachments in the sorting!")
                                    break
                    else:
                        mail_content = message.get_payload()
    except:
        print("Could not read mailbox!")

def sort():
    global checker
    global mail_content
    try:
        attachsort = input("Do you wish to include attachment emails for the sorting? [Y/N] ")
        if attachsort == "Y":
            if checker == True:
                print("Including attachments")
            else:
                print("Skipping attachment emails because you didn't download any!")
        else:
            print("Skipping attachments")
        while True:
            try:
                folder = int(input("How many folders do you wish to create? "))
                folder_number = 1
                subfolder = int(input("How many subfolders do you wish to create for each of the folders? "))
                subfolder_number = 1
                try:
                    os.chdir("C:/")
                except:
                    exit("Seems like you don't have a C drive!")
                try:
                    os.mkdir("mailsort")
                except FileExistsError:
                    pass
                for folder in range(folder):
                    try:
                        name = "folder_" + str(folder_number)
                        folder_number += 1
                        os.mkdir("mailsort/" + name)
                        print(f"Folder {name} created!")
                    except FileExistsError:
                        print(f"File {name} already exists!")
                    for folder in range(subfolder):
                        try:
                            subname = "subfolder_" + str(subfolder_number)
                            subfolder_number += 1
                            os.mkdir("mailsort/" + name + "/" + subname)
                            print(f"Subfolder {subname} for {name} created!")
                        except FileExistsError:
                            print(f"Subfolder {name} already exists for {folder}!")
                break
            except ValueError:
                print("Only numbers are allowed!")
        status, data = M.search(None, "ALL")
        number_text = 0
        number_html = 0
        mail_ids = []
        for block in data:
            mail_ids += block.split()
        for i in mail_ids:
            status, data = M.fetch(i, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])
                    mail_from = message["from"]
                    mail_subject = message["subject"]
                    if message.is_multipart():
                        mail_content = ""
                        for part in message.get_payload():
                            content_disposition = str(part.get("Content-Disposition"))
                            fileName = part.get_filename()
                            if checker == True:
                                if part.get_content_type() == "text/plain":
                                    mail_content += part.get_payload(decode=True).decode()
                                    text_file = open(f"C:/mailsort/{number_text}.txt", "w")
                                    n = text_file.write(mail_content)
                                    text_file.close()
                                    number_text += 1
                                elif part.get_content_type() == "text/html":
                                    mail_content += part.get_payload(decode=True).decode()
                                    text_file = open(f"C:/mailsort/{number_html}.html", "w")
                                    n = text_file.write(mail_content)
                                    text_file.close()
                                    number_html += 1
                            else:
                                if bool(fileName):
                                    print(f"Skipped an attachment email!")
                                    pass
        print("Welcome to Mailsort")
        print(f"We counted {len(list(os.walk('C:/mailsort')))-1} folders")
        if len(list(os.walk('C:/mailsort')))-1 == 0:
            exit("No folders found, exiting!")
        while True:
            user = input("Windows user profile: ")
            try:
                os.chdir(f"C:/Users/{user}/Downloads/mailsort")
                break
            except:
                print("Invalid username")
        regex_number = 1
        for i in range(len(list(os.walk("C:/mailsort")))-1):
                    regex_folder = input(f"Sort folder {regex_number} by string: ")
                    f = open(f"C:/Users/{user}/Downloads/mailsort-main/extensions.txt")
                    lines = f.read().splitlines()
                    number = 0
                    print(f"Available extensions: {lines}")
                    type = input(f"File extension for folder {regex_number}: ")
                    while True:
                        try:
                            if lines[number] == type:
                                if lines[number] != "":
                                    print("Found extension")
                                    break
                                else:
                                    exit("Extension field can not be empty!")
                            else:
                                number += 1
                        except IndexError:
                            exit("Did not find extension!")
                    txt_folder = Path("C:/mailsort").rglob(f"{type}")
                    files = [x for x in txt_folder]
                    switchcontent = 0
                    for name in files:
                        f = open(name, "r")
                        content = f.readlines()
                        print(f"File: {name}")
                        f.close()
                        while True:
                            try:
                                if re.match(str(regex_folder), str(content[switchcontent])):
                                    print("Match")
                                    os.chdir("C:/mailsort")
                                    try:
                                        shutil.move(f"{name}", f"C:\mailsort/folder_{regex_number}")
                                    except:
                                        pass
                                    break
                                else:
                                    print("No match")
                                    switchcontent += 1
                            except IndexError:
                                print("End of content")
                                switchcontent = 0
                                break
                    regex_number += 1
        type2 = type.replace("*", "")
        while True:
            for i in os.listdir("C:/mailsort/"):
                if i.endswith(f"{type2}"):
                    txtunsorted = input(f"Found {type2} file that remained unsorted, where do you wish to put them? [folder/subfolder/deleteall] ")
                    os.chdir("C:/mailsort/")
                    if txtunsorted == "folder":
                        whichfolder = input("Folder number? ")
                        shutil.move(f"{i}", f"C:/mailsort/folder_{whichfolder}")
                        print("Done!")
                        break
                    elif txtunsorted == "subfolder":
                        whichfolder = input("Folder number? ")
                        whichsubfolder = input("Subfolder number? ")
                        shutil.move(f"{i}", f"C:/mailsort/folder_{whichfolder}/subfolder_{whichsubfolder}")
                        print("Done!")
                        break
                    elif txtunsorted == "deleteall":
                        os.chdir("C:/mailsort")
                        path = '.'
                        files = os.listdir(path)
                        for filename in files:
                            if filename.endswith(f"{type2}"):
                                os.remove(f"{filename}")
                                print(f"Deleted {filename}")
    except NameError:
        exit("You need to select a mailbox before sorting!")

try:
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    gmail = input("Gmail: ")
    if re.match(regex, gmail):
        M.login(gmail, getpass.getpass())
        print("Login successful")
        rv, mailboxes = M.list()
        number = 0
        while True:
            try:
                number += 1
                mailboxes[number]
            except IndexError:
                break
        print(f"Found {number} mailboxes")
        iterate = 0
        while True:
            try:
                print(f"{iterate+1}. " + str(mailboxes[number-number+iterate]))
                iterate += 1
            except IndexError:
                break
        while True:
            try:
                choose_mailbox = int(input(f"Which mailbox do you wish to select? (1-{iterate}) "))
                while True:
                    if choose_mailbox == int(iterate-iterate+1):
                        confirm_mailbox = input(f"Are you sure you wish to select {mailboxes[0]}? [Y/N] ")
                        if confirm_mailbox == "Y":
                            M.select("INBOX") 
                            read_mailbox()
                            break
                        else:
                            break
                    elif choose_mailbox == int(iterate-iterate+2):
                        confirm_mailbox = input(f"Are you sure you wish to select {mailboxes[1]}? [Y/N] ")
                        if confirm_mailbox == "Y":
                            exit("That mailbox does not exist by default!")
                        else:
                            break
                    elif choose_mailbox == int(iterate-iterate+3):
                        confirm_mailbox = input(f"Are you sure you wish to select {mailboxes[2]}? [Y/N] ")
                        if confirm_mailbox == "Y":
                            M.select('"[Gmail]/All Mail"') 
                            read_mailbox()
                            break
                        else:
                            break
                    else:
                        if choose_mailbox > iterate:
                            exit("That mailbox is either empty or does not exist!")
                        else:
                            if choose_mailbox == int(6):
                                exit("Sent mail is broken, sorry!")
                            else:
                                confirm_mailbox = input(f"Are you sure you wish to select {mailboxes[choose_mailbox-1]}? [Y/N] ")
                                if confirm_mailbox == "Y":
                                    partition()
                                    break
                                else:
                                    break
                break
            except (IndexError, ValueError) as error:
                    print("That mailbox is either empty or does not exist!")
    else:
        exit("Login failed, incorrect email format!")
except imaplib.IMAP4.error:
    exit("Login failed, either your password is incorrect or you didn't enable less secure apps!")

sort()
