import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kaush\.pyenv\pyenv-win\versions\3.11.3\Lib\site-packages\Tesseract-OCR\tesseract.exe'
from ast import Name
import json
import cv2
import numpy as np
import sys
import re
import os
from PIL import Image
import ftfy
import io
import string
import re
import psycopg2
import UI
# from datetime import datetime
# import pytz

# def gettimestamp():
#     IST = pytz.timezone('Asia/Kolkata')
#     return datetime.now(IST)

def adhaar_read_data(text):
    res=text.split()
    #print(res)
    name = None
    dob = None
    adh = None
    sex = None
    nameline = []
    dobline = []
    text0 = []
    text1 = []
    text2 = []
    lines = text.split('\n')
    #print('lines = ',lines)
    for lin in lines:
        s = lin.strip()
        #s = lin.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    if 'female' in text.lower():
        sex = "FEMALE"
    else:
        sex = "MALE"
    
    text1 = list(filter(None, text1))
    text0 = text1[:]

    #print(text1)
    #print(text0)
    
    try:

        # Cleaning first names
        name = text0[0]
        name = name.rstrip()
        name = name.lstrip()
        #name = name.replace("8", "B")
        #name = name.replace("0", "D")
        #name = name.replace("6", "G")
        #name = name.replace("1", "I")
        name = re.sub('[^a-zA-Z] +', ' ', name)

        # Cleaning DOB
        dob = text0[1][-10:]
        dob = dob.rstrip()
        dob = dob.lstrip()
        '''dob = dob.replace('l', '/')
        dob = dob.replace('L', '/')
        dob = dob.replace('I', '/')
        dob = dob.replace('i', '/')
        dob = dob.replace('|', '/')
        dob = dob.replace('\"', '/1')
        dob = dob.replace(":","")'''
        dob = dob.replace(" ", "")

        # Cleaning Adhaar number details
        aadhar_number=''

        for word in res:
            if len(word) >= 4 and word.isdigit() and len(aadhar_number)<=10:
                aadhar_number=aadhar_number  + word + ' '
        if len(aadhar_number)>=12:
            print("Aadhar number : "+ aadhar_number)
            #print(name)
        else:
            print("Aadhar number not read")
        adh=aadhar_number

        

    except:
        pass

    data = {}
    data['Name'] = name
    data['Date of Birth'] = dob
    data['Adhaar Number'] = adh
    data['Sex'] = sex
    data['ID Type'] = "Adhaar"
    return data

def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split( )
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno+1:]
            return textlist
    return textlist

# path = "C:\Users\kaush\myfile.txt"
# img = cv2.imread("20201112_215316.jpg")
img = cv2.imread(UI.filename)
# img = cv2.resize(img, None, fx=200, fy=200,interpolation=cv2.INTER_CUBIC)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# var = cv2.Laplacian(img, cv2.CV_64F).var()
# if var < 50:
#     print("Image is Too Blurry....")
#     k= input('Press Enter to Exit.')
#     exit(1)
    
filename = UI.filename
text = pytesseract.image_to_string(Image.open(filename), lang = 'eng')

text_output = open('output.txt', 'w', encoding='utf-8')

text_output.write(text)
text_output.close()

file = open('output.txt', 'r', encoding='utf-8')
text = file.read()

text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)

data = adhaar_read_data(text)
ano  = data['Adhaar Number']


# print(data)

try:
    to_unicode = str
except NameError:
    to_unicode = bytes
with io.open('info.json', 'w', encoding='utf-8') as outfile:
    data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(data))   


with open('info.json', encoding = 'utf-8') as data:
    data_loaded = json.load(data)


file1 = open('output.txt', 'r')
Lines  = file1.readlines()
sex = "MALE"
index = -1
for line in Lines :
  index=index +1
  if "DOB" in line :
    ind = line.find("DOB")
    dob = line[ind + 4:].strip()
    print("Date of birth : ", dob)
    i = 1
    s = Lines[index-i].strip()
    
    while(any(c.isalpha() for c in s) == 0):
      i = i + 1
      s = Lines[index-i].strip()
    name = ''  
    for j in range (0, len(Lines[index-i])):
      name = Lines[index-i].strip()
    print('Name : ' , name)

  if "Female" in line or "FEMALE" in line:
    sex = "FEMALE"
print("Sex : ", sex)

input_val = ()
conn = psycopg2.connect(
    host="localhost",
    database="ID details",
    user="postgres",
    password="Kaushik2002@"
)
cur = conn.cursor()
#cur.execute("CREATE TABLE IF NOT EXISTS person (id SERIAL PRIMARY KEY, name VARCHAR(255), dob DATE, gender VARCHAR(10), aadhar VARCHAR(16))")
cur.execute("INSERT INTO person (name, dob, gender, aadhar) VALUES (%s, %s, %s, %s)", (name, dob, sex, ano))
conn.commit()
cur.close()
conn.close()