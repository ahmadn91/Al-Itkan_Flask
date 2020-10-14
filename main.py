from flask import Flask,render_template,jsonify,request
import datetime as dt
import xmlrpc.client
import json
from datetime import datetime
from random import randint
#import base64
# if this didnt work , open terminal and write "python3 -m pip install xmlrpc.client"

# python3 -m pip install flask
#to start server, go to main dir,"python3 main.py"



from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

class Rec_Api():

    def __init__(self):
        self.username ="apibot" 
        self.password ="ArxTuOpp_11@3"
        self.db ="ItkanIP" 
        self.url ="https://erp.alitkan.com" 
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url)) 
        

    
    def authenticate(self):
        try:
            self.uid = self.common.authenticate(self.db,self.username,self.password,{})
            #return ("Logged in successfuly, user id :"+ str(self.uid))
            return self.uid
        except Exception as s:
            return s
    
    def create_record(self,fields,module="hr.applicant",op_type="create"):

        try:
                res  = self.models.execute_kw(self.db, self.authenticate(), self.password,
                    module, op_type, [fields])
                return res

        except Exception as s:
                return s


    def search_record(self,domain,module="hr.applicant",op_type="search",limit=1):
        
            try :
                res=self.models.execute_kw(self.db, self.authenticate(), self.password,
                     module, op_type, [domain], {'limit': limit})
                return res

            except Exception as s:
                return s
    def search_and_read(self,domain,fields,module="hr.job",op_type="search_read",limit=0):
        
            try :
                res=self.models.execute_kw(self.db, self.authenticate(), self.password,
                     module, op_type, [domain], {'limit': limit,'fields':fields})
                return res

            except Exception as s:
                return s

    

"""
@app.route("/home",methods=["GET","POST"])
def home():

    return render_template("home.html")
"""




def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)







@app.route("/api",methods=["GET","POST"])
def api_req():
    if request.method == "POST":

        obj=Rec_Api()
        if not obj.authenticate():
            print("Authentication Failed, There is an issue with credentials")
            return "Authentication Failed, There is an issue with credentials"
        else:
            content = request.get_json()
            data=content["data"]
            files=content["files"]
            
            




            if files.get("photo"):
                data["photo"] =str.encode(files["photo"]).decode('ascii')

            if files.get("national_id"):
                data["national_id"] =str.encode(files["national_id"]).decode('ascii')

            if files.get("citizenship_cert"):
                data["citizenship_cert"] =str.encode(files["citizenship_cert"]).decode('ascii')

            if files.get("accomodation_id"):
                data["accomodation_id"] =str.encode(files["accomodation_id"]).decode('ascii')

            if files.get("uni_degree"):
                data["uni_degree"] =str.encode(files["uni_degree"]).decode('ascii')

            if files.get("medical"):
                data["medical"] =str.encode(files["medical"]).decode('ascii')

            if files.get("no_crim_req"):
                data["no_crim_req"] =str.encode(files["no_crim_req"]).decode('ascii')

            if files.get("letter_rec_1"):
                data["letter_rec_1"] =str.encode(files["letter_rec_1"]).decode('ascii')

            if files.get("letter_rec_2"):
                data["letter_rec_2"] =str.encode(files["letter_rec_2"]).decode('ascii')

            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d-%H:%M:%S")
    
            strData = json.dumps(data, indent=4)

#            initial = obj.search_record(domain=[["partner_phone","=",data["partner_phone"]]])
#            if initial != []:
#                print ("Phone No. Already exists")
#                return "Phone No. Already exists"
#            else:
            try:
                ref=str(random_with_N_digits(8))
                data["external_ref"] = ref

                res=obj.create_record(fields=data)
                s_res=obj.search_record(domain=[["name","=",data["name"]]])
                if s_res != []:
                    success_massage = "A new record has been created successfully" + ", Record ID is :" + str(res) + "," + str(s_res)
                    with open("/tmp/flask_logs_%s" % (date_time), "w") as logFile:
                        logFile.write(success_massage + "\n\n" + strData)
                    print(success_massage)
                    return ref
                else:

                    failure_massage = "Data sent successfully, but for some reason, record was not created" + str(res)
                    with open("/tmp/flask_logs_%s" % (date_time), "w") as logFile:
                        logFile.write(failure_massage + "\n\n" + strData)
                    print(failure_massage)
                    return "Data sent successfully, but for some reason, record was not created"

            except Exception as s:
                exception_massage = "error Exception message :) => " + str(s)
                with open("/tmp/flask_logs_%s" % (date_time), "w") as logFile:
                    logFile.write(exception_massage + "\n\n" + strData)
                print(exception_massage)
                return str(s)
    else:
        return "Nominal"

@app.route("/api/get")
def get_jobs():
    if request.method == "GET":
        obj=Rec_Api()
        obj.authenticate()
        data = obj.search_and_read([[1,'=',1]],["name", "description", "opening_date", 'state', "card_image", "city"])
        print (data)
        return jsonify(data)

@app.route("/api/check",methods=["POST"])
def get_check():
    if request.method == "POST":
        obj=Rec_Api()
        content = request.get_json()
        external_ref = content["ref"]
        if len(external_ref) == 8:
            response = obj.search_and_read([["external_ref","=",external_ref]],["stage_id"],limit=1,module="hr.applicant")
            if response:
                response = {"id":response[0]["stage_id"][0],"msg":response[0]["stage_id"][1]}

                return jsonify(response)
            else:
                res={"id":"empty","msg":"Sorry, There is no such application in the system"}
                return jsonify(res)
        else:
            res={"id":"empty","msg":"Wrong Format, Please enter the 8 digits application refernce number "}
            return res

#added today
@app.route("/api/helpdesk",methods=["POST"])
def helpdesk():
    if request.method == "POST":
        content = request.get_json()
        data=content["data"]
        obj=Rec_Api()
        if content["files"]:
            data["uploaded_file"] = str.encode(content["files"]["Attachment"]).decode('ascii')
        if not obj.authenticate():
            print("Authentication Failed, There is an issue with credentials")
            return jsonify({"created": False, 
                "message": "Authentication Failed, There is an issue with credentials"})
        else:
            try:
                res=obj.create_record(fields=data,module="helpdesk.ticket")
                #s_res=obj.search_record(module="helpdesk.ticket",domain=[["partner_email","=",data["partner_name"]]],limit=1)
                if res:
                    success_message = "A new record has been created successfully" + "record ID is :" + str(res)
                    print(success_message) 
                    return jsonify({"created": True,
                        "message":"created successfully"})
                    
                else:

                    failure_massage = "Data sent successfully, but for some reason, record was not created" + str(res)
                    
                    print(failure_massage)
                    return jsonify({"created": False,
                        "message":"Not created Successfully"})

            except Exception as s:
                exception_massage = "error Exception message :) => " + str(s)
                print(exception_massage)
                return str(s)
            
    else:
        return "Nominal"

#end of added today


            

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True) #localIP:5000, so the api call url should be "192.168.x.x:5000/api"
