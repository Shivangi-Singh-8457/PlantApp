
from itertools import count
from multiprocessing.sharedctypes import Value
from sqlite3 import SQLITE_CREATE_INDEX
from flask import Flask, render_template, request
import MySQLdb
db = MySQLdb.connect("localhost", "root", "", "project",8111)
from flask import Flask
from flask_mail import Mail, Message
import json
import os
import base64
import random
from flask_cors import CORS,cross_origin
app = Flask(__name__)
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_email'
app.config['MAIL_PASSWORD'] = 'email_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)
SERVER = "http://localhost:5000/"

#global BASE_DIRECTORY
BASE_DIRECTORY = "./IMAGES/"
global user
user=""
global login_flag
login_flag=False
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
    str1=str1+f"{keys[len(keys)-1]},"
    str1=str1+"start_index, last_index, user_id)values("    
    str1=str1+f"'{output}' , "
    for index in range(0,len(keys)-1):
        str1=str1+f"'{value[index]}' , "
    str1=str1+f"'{value[len(keys)-1]}',"
    str1=str1+f"'{startIndex}','{lastIndex}','{user}'"+");"    
    return str1

def sendMail(otp):
   global user_email 
   msg = Message('Hello', sender = 'your_email', recipients = [user_email])
   msg.body = "This email is from Plantopedia.\nyour OTP is "+otp 
   mail.send(msg)

def generate_otp():
    global otp
    otp=random.randint(1000,9999)
    print(str(otp))
    sendMail(str(otp)) 
    print("sentmail_1")
    return

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
    global login_flag
    print(login_flag)
    print(user)
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
        return json.dumps()
   except:     
           print( "Error: unable to fetch items")
           return json.dumps("")  #dump data from server to client

@app.route("/imagedata", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def image():
   data = request.get_data()
   base64EncodedStr = base64.b64encode(data)
   global cnt
   global output
   cnt=cnt+1
   with open(BASE_DIRECTORY + output + "/img_"+ str(cnt) +".png", "wb") as fh:
        fh.write(base64.decodebytes(base64EncodedStr))
    
   try:
        
        return json.dumps("Thank you for your contribution.")
   except:     
           print( "Error: unable to fetch items")
           return json.dumps({})

@app.route("/imagename", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def imagename():
   #data = request.get_data()
   data=request.get_json()
   global startIndex
   global lastIndex
   global output
   global cnt
   cnt=0
   #output = data.decode()
   output=data[0]
   print(output)
   if(os.path.isdir(BASE_DIRECTORY + output)):
    cnt=len(os.listdir(BASE_DIRECTORY + output))
   else:
    os.mkdir(BASE_DIRECTORY + output)
   startIndex=cnt+1 
   lastIndex=cnt + int(data[1])
   print(str(startIndex)+" start")
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
    global login_flag
    global user
    login_flag=True
    user=data[0]
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
    try:
        mycursor.execute(command)
        result=mycursor.fetchone()
        print(result)
        if result[0]==data[1]:
            global login_flag
            login_flag=True
            global user
            user=data[0]
            print(login_flag)
            print(user)
            return json.dumps(["You are successfully logged in.","true"])
        else:
            return json.dumps(["Bad request","false"])
    except:     
           print( "Error: unable to check")
           return json.dumps(["Register yourself","false"])

@app.route("/checklogin", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def check_signin():
    global login_flag
    print(login_flag)
    if login_flag:
        return "true"
    else:
        return "false"

@app.route("/logout", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)        
def signout():
    global login_flag
    login_flag=False
    print(login_flag)
    global user
    user=""
    print(user)
    return json.dumps("You are logged out.")

@app.route("/checkemail", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)  
def checkemail():
    data = request.get_data()
    global user_email
    user_email=data.decode()
    print(user_email)
    command="select user_id from users where user_id="+f"'{user_email}'"
    mycursor = db.cursor()  
    print(command)
    try:
        mycursor.execute(command)
        result=mycursor.fetchone()
        #db.commit()
        #db.close()
        if len(result)>0:
            generate_otp()
            print("sentmail_2")
            return "true"
        else:
            return "false"
    except:     
           print( "Error: unable to change")
           return json.dumps("") 
           
@app.route("/checkotp", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def checkotp():
    data=request.get_data()
    getotp=data.decode()
    global otp
    if(str(otp)==getotp):
        return "true"
    else:
        return "false"

@app.route("/resend", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def resend():
    generate_otp()
    return json.dumps("")

@app.route("/chngpswd", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def chngpswd():
    data=request.get_data()
    global user_email
    getpswd=data.decode()
    command = "update users set `password`="+f"'{getpswd}'"+ " where user_id="+f"'{user_email}'" 
    mycursor = db.cursor()  
    print(command)
    try:
        mycursor.execute(command)
        db.commit()
        return json.dumps("Password changed successfully.")
    except:     
           print( "Error: unable to change")
           return json.dumps("") 

@app.route("/folderlist", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def folderlist():
    command = "select folder_id, leaf_division, leaf_apices, leaf_bases, leaf_margin from temp order by leaf_division" 
    mycursor = db.cursor()  
    print(command)
       
    try:
        mycursor.execute(command)
        folders=mycursor.fetchall()
        print(folders)
        return_folder=[]
        for foll in folders:
            f1=[]
            for f in foll:
               f1.append(f) 
            return_folder.append(f1)
        print(return_folder)
        return json.dumps(return_folder)
    except:     
           print( "Error: unable to check")
           return json.dumps()           
app.run(debug=True)
