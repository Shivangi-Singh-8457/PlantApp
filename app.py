from flask import Flask, render_template, request
import MySQLdb
db = MySQLdb.connect("localhost", "root", "", "project",8111)
from flask import Flask
from flask_mail import Mail, Message
import json
import glob
import os
import base64
import random
from flask_cors import CORS,cross_origin
app = Flask(__name__)
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shivangi_52111104@nitkkr.ac.in'
app.config['MAIL_PASSWORD'] = 'Shivangi@4321'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)
SERVER = "http://localhost:5000/"

#global BASE_DIRECTORY
#BASE_DIRECTORY = "./IMAGES/"
BASE_DIRECTORY = ".//static/temp_images/"
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
   msg = Message('Hello', sender = 'shivangi_52111104@nitkkr.ac.in', recipients = [user_email])
   msg.body = "This email is from Plantopedia.\nyour OTP is "+otp 
   mail.send(msg)

def generate_otp():
    global otp
    otp=random.randint(1000,9999)
    print(str(otp))
    sendMail(str(otp)) 
    print("sentmail_1")
    return

def imagelist(fol_id):
    mycursor=db.cursor()
    command="select img_index from temp_images where folder_id="+f"{fol_id}"
    try:
        mycursor.execute(command)
        result=mycursor.fetchall()
        # db.close()
        print(result)
        arr=[]
        for it in result:
            arr.append(it[0])
        print(arr) 
        return arr    
    except:     
           print( "Error: unable to fetch")
           return arr    

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
        #db.commit()
        mycursor.execute("select max(folder_id) from temp")
        result=mycursor.fetchone()
        print(result)
        #cursor=db.cursor(prepared=True)
        query="insert into temp_images(folder_id,img_index) values(%s,%s)"
        for i in range(startIndex, lastIndex+1):
            print(i)
            tuple=(result,i)
            mycursor.execute(query,tuple)
        print("done")    
        db.commit()    
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
    #cnt=len(os.listdir(BASE_DIRECTORY + output))
    list_of_files=glob.glob(BASE_DIRECTORY + output + "/*")
    latest_file=max(list_of_files,key=os.path.getctime)
    print(latest_file)
    basename=os.path.basename(latest_file)
    print(basename)
    filename=os.path.splitext(basename)[0]
    print(filename)
    cnt=int(filename.split("_")[1])
    print(cnt)
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
        print(result)
        print(type(result))
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
        return_image={}
        for folder in return_folder:
            return_image[folder[0]]=imagelist(folder[0])
        print(return_image)     
        return json.dumps([return_folder,return_image])
    except:     
           print( "Error: unable to check")
           return json.dumps("")  

@app.route("/folder_vote", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def folder_vote():
    data=request.get_json()
    mycursor = db.cursor() 
    global user
    command1="select vote, report from folder_reviewers where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
    try:
        mycursor.execute(command1)
        result=mycursor.fetchone()
        db.commit()
        print(result)
        print(type(result))
        command2=""
        command3=""
        if result is None:        
            if(data[1]=='u'):
                command2="insert into folder_reviewers values("+f"'{user}','{data[0]}',1,0)"
                command3="update temp set upvote=upvote+1 where folder_id="+f"'{data[0]}'"
                print("result is None")
            elif(data[1]=='d'):
                command2="insert into folder_reviewers values("+f"'{user}','{data[0]}',-1,0)"
                command3="update temp set downvote=downvote+1 where folder_id="+f"'{data[0]}'"
            elif(data[1]=='r'):
                command2="insert into folder_reviewers values("+f"'{user}','{data[0]}',0,1)"
                command3="update temp set report=report+1 where folder_id="+f"'{data[0]}'"    
        else:
            if result[1]==1 and data[1]=='r':
                if result[0]==0:
                    command2="delete from folder_reviewers where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
                    command3="update temp set report=report-1 where folder_id="+f"'{data[0]}'"
                elif result[0]==-1:
                    command2="update folder_reviewers set report=0 where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
                    command3="update temp set report=report-1 where folder_id="+f"'{data[0]}'"    
            elif result[0]==1 and data[1]=='r':
                command2="update folder_reviewers set vote=0, report=1 where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
                command3="update temp set upvote=upvote-1, report=report+1 where folder_id="+f"'{data[0]}'"
            elif result[0]==1 and data[1]=='u':
                command2="delete from folder_reviewers where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
                command3="update temp set upvote=upvote-1 where folder_id="+f"'{data[0]}'"
            elif result[0]==-1 and data[1]=='u':
                if result[1]==0:
                    command2="update folder_reviewers set vote=1 where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
                    command3="update temp set upvote=upvote+1, downvote=downvote-1 where folder_id="+f"'{data[0]}'"
            elif result[0]==-1 and data[1]=='d':
                if result[1]==0:
                    command2="delete from folder_reviewers where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
                    command3="update temp set downvote=downvote-1 where folder_id="+f"'{data[0]}'"
                elif result[1]==1:
                    command2="update folder_reviewers set vote=0 where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
                    command3="update temp set downvote=downvote-1 where folder_id="+f"'{data[0]}'"    
            elif result[0]==-1 and data[1]=='r':
                    command2="update folder_reviewers set report=1 where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
                    command3="update temp set report=report+1 where folder_id="+f"'{data[0]}'"
            elif result[0]==1 and data[1]=='d':
                command2="update folder_reviewers set vote=-1 where user_id="+f"'{user}'"+" and folder_id="+f"'{data[0]}'"
                command3="update temp set upvote=upvote-1, downvote=downvote+1 where folder_id="+f"'{data[0]}'"
        print(command2)
        print(command3)
        if(command2!=""):
            mycursor.execute(command2)
            db.commit()
        if(command3!=""):    
            mycursor.execute(command3) 
            db.commit()       
        return json.dumps("")        
    except:
        print( "Error: unable to change")
        return json.dumps("") 

@app.route("/image_vote", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def image_vote():
    data=request.get_json()
    mycursor = db.cursor() 
    global user
    command1="select vote, report from image_reviewers where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
    try:
        mycursor.execute(command1)
        result=mycursor.fetchone()
        db.commit()
        print(result)
        print(type(result))
        command2=""
        command3=""
        if result is None:        
            if(data[2]=='u'):
                command2="insert into image_reviewers values("+f"'{user}',{data[0]},{data[1]},1,0)"
                command3="update temp_images set upvote=upvote+1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
            elif(data[2]=='d'):
                command2="insert into image_reviewers values("+f"'{user}',{data[0]},{data[1]},-1,0)"
                command3="update temp_images set downvote=downvote+1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
            elif(data[2]=='r'):
                command2="insert into image_reviewers values("+f"'{user}',{data[0]},{data[1]},0,1)"
                command3="update temp_images set report=report+1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"    
        else:
            if result[1]==1 and data[2]=='r':
                if result[0]==0:
                    command2="delete from image_reviewers where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                    command3="update temp_images set report=report-1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                elif result[0]==-1:
                    command2="update image_reviewers set report=0 where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                    command3="update temp_images set report=report-1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"    
            elif result[0]==1 and data[2]=='r':
                command2="update image_reviewers set vote=0, report=1 where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                command3="update temp_images set upvote=upvote-1, report=report+1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
            elif result[0]==1 and data[2]=='u':
                command2="delete from image_reviewers where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                command3="update temp_images set upvote=upvote-1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
            elif result[0]==-1 and data[2]=='u':
                if result[1]==0:
                    command2="update image_reviewers set vote=1 where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                    command3="update temp_images set upvote=upvote+1, downvote=downvote-1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
            elif result[0]==-1 and data[2]=='d':
                if result[1]==0:
                    command2="delete from image_reviewers where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                    command3="update temp_images set downvote=downvote-1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                elif result[1]==1:
                    command2="update image_reviewers set vote=0 where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                    command3="update temp_images set downvote=downvote-1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"    
            elif result[0]==-1 and data[2]=='r':
                    command2="update image_reviewers set report=1 where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                    command3="update temp_images set report=report+1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
            elif result[0]==1 and data[2]=='d':
                command2="update image_reviewers set vote=-1 where user_id="+f"'{user}'"+" and folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
                command3="update temp_images set upvote=upvote-1, downvote=downvote+1 where folder_id="+f"{data[0]} and img_index="+f"{data[1]}"
        print(command2)
        print(command3)
        if(command2!=""):
            mycursor.execute(command2)
            db.commit()
        if(command3!=""):    
            mycursor.execute(command3) 
            db.commit()       
        return json.dumps("")        
    except:
        print( "Error: unable to change")
        return json.dumps("") 

@app.route("/save_comment", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def save_comment():
    data=request.get_json()
    command="insert into reviews values("+f"{data[0]},'{user}','{data[1]}',now())"
    mycursor=db.cursor()
    try:
        mycursor.execute(command)
        db.commit()
        return json.dumps("")
    except:
        print( "Error: unable to change")
        return json.dumps("")

@app.route("/get_comments", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def fetch_comment():
    data=request.get_data()
    fol_id=data.decode()
    command="select user_id, comment, date from reviews where folder_id="+str(fol_id)
    mycursor=db.cursor()
    try:
        mycursor.execute(command)
        comments=mycursor.fetchall()
        print(comments)
        return_comments=[]
        for i in comments:
            temp=[]
            for j in i:
                temp.append(j)
            return_comments.append(temp)  
        print(return_comments)      
        return json.dumps(return_comments)
    except:
        print( "Error: unable to fetch")
        return json.dumps("")          

app.run(debug=True)