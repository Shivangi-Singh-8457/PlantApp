
from itertools import count
from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request
import MySQLdb

db = MySQLdb.connect("localhost", "root", "", "project",8111)
import json
import os
import base64
from flask_cors import CORS,cross_origin
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)
SERVER = "http://localhost:5000/"

#global BASE_DIRECTORY
BASE_DIRECTORY = "./IMAGES/"
#generating sql commands
def create_sql_comand(keys,value):
    str1="select leaf_division from leaf where "
    for index in range(0,len(keys)-1):
        str1=str1+f"{keys[index]}='{value[index]}' and "
    str1=str1+f"{keys[len(keys)-1]}='{value[len(keys)-1]}'"
    return str1

#getting images path from contained folder
def getFileNames(folderNames):
    IMAGES_PATH = './/static/dataset/'
    answer = {}
    fileName = []
    for folder in folderNames:
        allfiles = os.listdir(IMAGES_PATH+folder)     
        for file in allfiles:
            fileName.append(SERVER + IMAGES_PATH + folder + "/" + file)
        answer[folder] = fileName
        fileName = []  
    return answer

def insert_sql_comand(keys,value):
    str1="insert into temp ("
    str1=str1+"leaf_division , "
    for index in range(0,len(keys)-1):
        str1=str1+f"{keys[index]} , "
    str1=str1+f"{keys[len(keys)-1]}"
    str1=str1+")values("    
    str1=str1+f"'{output}' , "
    for index in range(0,len(keys)-1):
        str1=str1+f"'{value[index]}' , "
    str1=str1+f"'{value[len(keys)-1]}'"
    str1=str1+");"    
    return str1
#recive client server call

@app.route("/predict", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def calc():
    data = request.get_json()
    keys=[]
    value=[]
    
    for arr in data:
         keys.append(arr)
         value.append(data[arr])
    

    command = create_sql_comand(keys,value)
    print(command)
    curs = db.cursor()  #create a curser to database for  data extraction
    try:
        curs.execute(command)
        folder=curs.fetchall() #insert extracted data to folder variable
        intersection_folder=[]
        print(folder)
        for foll in folder:
            intersection_folder.append(foll[0])
        filenames=getFileNames(intersection_folder)
        return json.dumps(filenames) #dump data from server to client
    except:
        print( "Error: unable to fetch items")
        return json.dumps({})   #dump data from server to client

        
@app.route("/adddata", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def send():
 
   data = request.get_json()
   print(data)
   print(type(data))
   keys1=[]
   value1=[]
    
   for arr in data:
        keys1.append(arr)
        value1.append(data[arr])
    
   command = insert_sql_comand(keys1,value1)
   mycursor = db.cursor()  #create a curser to database for  data extraction
   print(command)
   try:
        mycursor.execute(command)
        db.commit()
        folder=mycursor.rowcount() #insert extracted data to folder variable
        db.close()
        print(folder)
        return json.dumps("plz upload image now your response is added to database")
   except:     
           print( "Error: unable to fetch items")
           return json.dumps("")   #dump data from server to client
@app.route("/imagedata", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def image():
   data = request.get_data()
   base64EncodedStr = base64.b64encode(data)
   global cnt
   #global output
   cnt=cnt+1
   with open(BASE_DIRECTORY + output + "/img_"+ str(cnt) +".png", "wb") as fh:
        fh.write(base64.decodebytes(base64EncodedStr))
    
   try:
        
        return json.dumps("Thank you for your contribution.")
   except:     
           print( "Error: unable to fetch items")
           return json.dumps({})   #dump data from server to client
@app.route("/imagename", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def imagename():
   data = request.get_data()
   global output
   global cnt
   cnt=0
   output = data.decode()
   print(output)
   if(os.path.isdir(BASE_DIRECTORY + output)):
    cnt=len(os.listdir(BASE_DIRECTORY + output))
    #cnt=len([path for path in os.listdir(BASE_DIRECTORY + output)if os.path.isfile(os.path.join(BASE_DIRECTORY + output,path))])
   else:
    os.mkdir(BASE_DIRECTORY + output)
   try:
        return json.dumps()
   except:     
           print()
           return json.dumps({})   #dump data from server to client
@app.route("/register", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def signup():
    data = request.get_json()
    command = "insert into users values("+f"'{data[0]}' , '{data[1]}', '{data[2]}'"+")"
    mycursor = db.cursor()  
    print(command)
    try:
        mycursor.execute(command)
        db.commit()
        
        return json.dumps("You are successfully registered")
    except:     
           print( "Error: unable to register")
           return json.dumps("")
@app.route("/login", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def signin():
    data = request.get_json()
    print(data)
    command = "select password from users where user_id="+f"'{data[0]}'" 
    mycursor = db.cursor()  
    print(command)
    global session
    session=[]
    login_flag=False
    try:
        mycursor.execute(command)
        result=mycursor.fetchone()
        print(result)
        if result[0]==data[1]:
            login_flag=True
            print(login_flag)
            return json.dumps("You are successfully logged in.")
        else:
            return json.dumps("Bad request")
    except:     
           print( "Error: unable to check")
           return json.dumps("")
app.run(debug=True)