#!/usr/bin/env python3

#this is the home for functions that interact directly with
#my google drive

#drive_setup connects to and authenticates with my drive

#drive_fill uploads the results from my webscrapers into
#their properly organized folders

#dl_items takes a file name as argument, searches the drive
#for that file, then does a check to see if it received the
#name of a folder or a file. if it was given a folder, it will
#download the entire contents of that folder as well as any
#subfolders and their contents as well. I need to rework
#the code to make it a little cleaner, but I felt it was more
#important to first get something that works, then make it
#work better

#as soon as I figure out a reasonable way to implement account
#switching, I will be a very happy coder

#temporary fix for the above, when invoking drive_setup you
#should pass in both the SCOPES you want it to be able to
#use as well as the directory where you want it to look for
#token.json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from datetime import date
import requests
import os
import io
import re

#edit the following with your own preferred default path
creds_path = os.path.expandvars('$HOME/Documents/config/python_user_modules/')

def drive_setup(SCOPES='https://www.googleapis.com/drive.metadata.readonly', token_dir=creds_path):
	print(creds_path)
	pwd = os.getcwd()
	os.chdir(creds_path)
	if not SCOPES:
		raise Exception("No scope")
	creds = None
	if os.path.exists(token_dir + 'token.json'):
		creds = Credentials.from_authorized_user_file(token_dir + 'token.json', SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(creds_path + 'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open(token_dir + 'token.json', 'w') as token:
			token.write(creds.to_json())
	os.chdir(pwd)
	return build('drive', 'v3', credentials = creds)

#generalize this function by giving it the ability to tell
#the difference between folders and files, creating
#subdirectories in the drive upload location accordingly
def drive_fill(DRIVE_DIR, DRIVE, FILESET=None, SUBDIR=None):
	print('from: ' + str(date.today()))
	if SUBDIR:
		DEST_META = {'name': SUBDIR, 'mimeType': "application/vnd.google-apps.folder", 'parents': [DRIVE_DIR['files'][0]['id']]}
		DEST = DRIVE.files().create(body=DEST_META, fields="id").execute()
		ID = DEST.get('id')
		DEST_META['name'] = str(date.today())
		DEST_META['parents'] = [ID]
	else:
		DEST_META = {'name': str(date.today()), 'mimeType': "application/vnd.google-apps.folder", 'parents': [DRIVE_DIR['files'][0]['id']]}
	DEST = DRIVE.files().create(body=DEST_META, fields="id").execute()
	ID = DEST.get('id')
	if FILESET == None:
		FILESET = os.listdir()
	for file in FILESET:
		for attempt in range(1, 10):
			try:
				print('upload: ' + file)
				META = {"name": os.path.basename(file), "parents": [ID]}
				DATA = MediaFileUpload(file)
				UPLOAD = DRIVE.files().create(body=META, media_body=DATA, fields='id').execute()
			except:
				continue
			else:
				break

def dl_items(drive, item):
	query_string = "name = '" + item +"'"
	src_dir = drive.files().list(q=query_string).execute()
	if not src_dir or not src_dir['files'][0]['id']:
		print(item + " not found")
		exit()
	if src_dir['files'][0]['mimeType'] == 'application/vnd.google-apps.folder':
		print('found folder')
		query_str = "'" + str(src_dir['files'][0]['id']) + "' in parents"
		children = drive.files().list(q=query_str).execute()
		fileset = children['files']
	else:
		print('found file')
		fileset = src_dir['files']
	print(fileset)
	for file in fileset:
		print(file)
		if file['mimeType'] == 'application/vnd.google-apps.folder':
			pwd = os.getcwd()
			if not os.path.exists(file['name']):
				os.mkdir(file['name'])
			os.chdir(file['name'])
			dl_items(drive, file['name'])
			os.chdir(pwd)
			continue
		dl_req = drive.files().get_media(fileId=file['id'])
		out_file = io.BytesIO()
		dl = MediaIoBaseDownload(out_file, dl_req)
		done = False
		while done == False:
			status, done = dl.next_chunk()
		with io.open(file['name'], 'wb') as out:
			out_file.seek(0)
			out.write(out_file.read())
