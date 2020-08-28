from flask import Flask,render_template,jsonify
from flask import request
import xmlrpc.client #if this didnt work , open terminal and write "python3 -m pip install xmlrpc.client"

# python3 -m pip install flask
#to start server, go to main dir,"python3 main.py"

app = Flask(__name__)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

class Rec_Api():

    def __init__(self):
        self.username ="" 
        self.password =""
        self.db ="" 
        self.url ="" 
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url)) 
        self.uid = 0

    
    def authenticate(self):
        try:
            self.uid = self.common.authenticate(self.db,self.username,self.password,{})
            return ("Logged in successfuly, user id :"+ str(self.uid))
        except Exception as s:
            return self.exception_format(s)
    
    def create_record(self,fields,module="hr.applicant",op_type="create"):

        try:
                res  = self.models.execute_kw(self.db, self.uid, self.password,
                    module, op_type, [fields])
                return res

        except Exception as s:
                return self.exception_format(s)


    def search_Record(self,domain,module="hr.applicatn",op_type="search",limit=1):
        
            try :
                res=self.models.execute_kw(self.db, self.uid, self.password,
                     module, op_type, [domain], {'limit': limit})
                return res

            except Exception as s:
                return self.exception_format(s)

"""
@app.route("/home",methods=["GET","POST"])
def home():

    return render_template("home.html")
"""

@app.route("/api",methods=["GET","POST"])
def api_req():
    if request.method == "POST":
        content = request.get_json()
        obj = Rec_Api()
        search_result = obj.search_record(limit=1,domain=[[["email_from","=",content["email_from"],["partner_phone","=",content["partner_phone"]]]]])
        if search_result:
            return jsonify({status=Information already exists},headers=headers)
        else:
            obj.create_record(fields=contents)
            return jsonify({status=Application Create successfully},headers=headers)
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
