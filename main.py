from flask import Flask,render_template,jsonify,request

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
        content = request.get_json()
        data=content["data"]
        files = content["files"]
        obj = Rec_Api()
        #search_result = obj.search_record(limit=1,domain=[[["email_from","=",data["email_from"],["partner_phone","=",data["partner_phone"]]]]])
        # if search_result !=0:
        #     #return jsonify({status:"Information already exists"},headers=headers)
        #     print(search_result,type(search_result))
        #     print("Not done")
        #     return "already exists"
        # else:
        files["photo"] = str.encode(files["photo"]).decode('ascii')
        print(files["photo"],type(files["photo"]))
        #fieldss={**data,**files}
        obj.create_record(fields={"name":"ahmed","photo":files["photo"]})
        #return jsonify({status:"Application Created successfully"},headers=headers)
        print("done")
        return "Done"
    else:
        pass

"""

@app.route("/test",methods=["GET","POST"])

def test():
    if request.method == "POST":
        return request

    return render_template("test.html")
"""
    

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True) #localIP:5000, so the api call url should be "192.168.x.x:5000/api"
