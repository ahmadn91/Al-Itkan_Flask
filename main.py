from flask import Flask,render_template,jsonify,request
import datetime as dt
import xmlrpc.client 
# if this didnt work , open terminal and write "python3 -m pip install xmlrpc.client"

# python3 -m pip install flask
#to start server, go to main dir,"python3 main.py"

from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

class Rec_Api():

    def __init__(self):
        self.username ="admin" 
        self.password ="admin"
        self.db ="Al-Itkan" 
        self.url ="http://localhost:8069" 
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

"""
@app.route("/home",methods=["GET","POST"])
def home():

    return render_template("home.html")
"""

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
            if len(files) > 0:
                data["photo"] =str.encode(files["photo"]).decode('ascii')
                data["national_id"] =str.encode(files["national_id"]).decode('ascii')
                data["citizenship_cert"] =str.encode(files["citizenship_cert"]).decode('ascii')
                data["accomodation_id"] =str.encode(files["accomodation_id"]).decode('ascii')
                data["uni_degree"] =str.encode(files["uni_degree"]).decode('ascii')
                data["medical"] =str.encode(files["medical"]).decode('ascii')
                data["no_crim_req"] =str.encode(files["no_crim_req"]).decode('ascii')
                data["letter_rec_1"] =str.encode(files["letter_rec_1"]).decode('ascii')
                data["letter_rec_2"] =str.encode(files["letter_rec_2"]).decode('ascii')
            print(data)
            initial = obj.search_record(domain=[["partner_phone","=",data["partner_phone"]]])
            if initial != []:
                print ("Phone No. Already exists")
                return "Phone No. Already exists"
            else:
                try:
                    res=obj.create_record(fields=data)
                    s_res=obj.search_record(domain=[["name","=",data["name"]]])
                    if s_res != []:
                        print("A new record has been created successfully" + ", Record ID is :" + str(res) + "," + str(s_res)) 
                        return "A new record has been created successfully"
                    else:
                        print("Data sent successfully, but for some reason, record was not created" + res)
                        return "Data sent successfully, but for some reason, record was not created"
                except Exception as s:
                    print(s)
                    return s
    else:
        return "Nominal"

@app.route("/api/get")
def get_jobs():
    if request.method == "GET":
        jobs = {"Engineer":{
            "description":"system engineer",
            "dead_line":"2021"
        },"accountant":{
            "description":"accountant",
            "dead_line":"2022"
        },"techncican":{
            "description":"accountant",
            "dead_line":"2022"
        }
        }
        return jsonify(jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True) #localIP:5000, so the api call url should be "192.168.x.x:5000/api"
