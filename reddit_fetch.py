#!/usr/bin/env python3
import os.path
import urllib.request
import json
import praw

#seting up praw usage
user_agent = "Script by xHFHope"
r=praw.Reddit(user_agent=user_agent)
user_name = input('Username: ')
user = r.get_redditor(user_name)


#Validating chars of, looping, and modifying filename input as necessary
validChars = set('^&\'@{}[],$=!-\#()%.+~_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
valid = False
while not valid:
    filename = input('Desired filename: ')
    valid = True
    for c in filename:
        if not c in validChars:
            print('Invalid symbol or character used in filename.')
            valid = False
        if valid:
            if filename[len(filename)-4] == '.':
                if not filename[len(filename)-3] == 't' and filename[len(filename)-2] == 'x' and filename[len(filename)-1] == 't':                                                    
                    valid = False
                    print('Invalid filename. Must have txt extension or no extension')
            else:
                filename+='.txt'
        

#Retrieving valid input for type of comments to retrieve
while True:
    print('\n1: Top     2:New     3:Hot')    
    cType = input('Please enter 1, 2, or 3: ')
    if cType == '1':
        cType = 'top'
        break
    if cType =='2':
        cType = 'new'
        break
    if cType == '3':
        cType = 'hot'
        break
    print('Invalid input.')

#Retrieving valid input for quantity of comments to retrieve
while True:
    desiredFetchCount = input('\nHow many comments would you like to fetch from ' + cType + ' (1-1000): ')
    if desiredFetchCount.isdigit():
        if int(desiredFetchCount) > 0 and int(desiredFetchCount) <= 1000:
            break
    print('Invalid input.')

#Setting up a bool to indicate whether or not we are working with a new or an existing file
aNewFile = not os.path.isfile(filename)
if aNewFile:
    print('File not found. Making new txt file...')
else:
    print('File found.')


#Creating a new file OR reading all the contents from an existing file
if not aNewFile:
    print('Reading data from file.')
    fo = open(filename, 'r+', encoding="utf-8-sig")
    myData=fo.readlines()
    print('Done.')
else:    
    fo = open(filename, 'a+', encoding="utf-8-sig")
    print('Successfully created.')

#Number of comments written
count = 0

#Number of fetched comments that already existed in the file
matchedCount=0

#praw comment fetch happens here
comments=user.get_comments(limit=int(desiredFetchCount), sort=cType)

#ID comparison and output
print('Done.\nWriting comments to file as necessary... (be patient!)')
try:
    for i in comments:
        idstr = i.id + '\n'
        if aNewFile:
            fo.write(i.id + '\n')
            fo.write(i.body + '\n' + '\n')
            count+=1
        elif not idstr in myData: #ensure that comment id does not exist in file already
            fo.write(i.id + '\n')
            fo.write(i.body + '\n' + '\n')
            count+=1
        else:
            matchedCount+=1 


    print('Success- ' + str(matchedCount) + ' comments were already in file. Wrote ' + str(count) + ' new entries into ' + filename + '.')

except praw.errors.NotFound:
    print('Username not found.')
    
fo.close()

