from flask import Flask, request
import json
from datetime import date
import os.path
'''
Elijah Bajec Dickinson 
'''
app = Flask(__name__)


@app.route('/network_test')
def test():
    return 'Connection successful!'

@app.route('/recieve_tutor_request', methods = ['POST'])
def update_file():

    if (not os.path.isdir('tutor_requests')):
        os.mkdir('tutor_requests')

    body = (str)(request.data.decode('utf-8'))
    data = {}
    data = json.loads(body)
    filepath = 'tutor_requests/' +data['user'] +'/'

    if(not os.path.isdir(filepath)): 
        os.mkdir(filepath)
    
    #this is to identify multiple requests submitted on the same day
    #appends to end of filename
    request_num = 0

    while True: 
        filename =  str(date.today()) + '-' + str(request_num) + '.txt'

        if (os.path.isfile(filepath + filename)):
            request_num += 1
        else:
            data.pop('user')
            with open(filepath + filename, 'x') as f:
                f.write(json.dumps(data))   

            return 'Tutor request recieved!'

@app.route('/read_tutor_requests',methods = ['POST'])
def get_tutor_requests_data():

    body = (str)(request.data.decode('utf-8'))
    data = json.loads(body)

    dir = 'tutor_requests/' + data['username'] +'/'

    requestList = []

    if os.path.isdir(dir):
        for filename in os.listdir(dir):
            fullpath = os.path.join(dir, filename)

            if os.path.isfile(fullpath):
                f = open(fullpath,'r')
                requestList.append(f.read())

    return json.dumps(requestList)
    


@app.route('/login',methods = ['POST'])
def login():
    body = (str)(request.data.decode('utf-8'))
    data = json.loads(body)

    username = data['username']
    password = data['password']

    response =  {'passwordCheck':True, 'usernameCheck':True}

    return json.dumps(response)
          
@app.route('/load/<string:file>')
def get_calendar_data(file):

    path = 'readable/' + file

    if os.path.isfile(path):
        f = open('readable/' + file,'r')
        return f.read()
    
    return 'The file you are looking for does not exist.'



if __name__ ==  '__main__':
    app.run(host='0.0.0.0', port=5000)


