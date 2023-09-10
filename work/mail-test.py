from flask import Flask, request
import requests, json

app = Flask(__name__)

@app.route("/info")
def get_info():
    response = requests.get('https://api.beget.com/api/mail/getMailboxList?login=vevmkycf&passwd=RI*5Xut4&input_format=json&output_format=json&input_data={%22domain%22:%22test8999.ru%22}')
    return response.json()

@app.route('/create')
def create_mail():
    username = request.args.get('username')
    password = request.args.get('password')
    input_data = {"domain":"test8999.ru","mailbox":f"{username}","mailbox_password":f"{password}"}
    params = {'login': 'vevmkycf', 
        'passwd': 'RI*5Xut4', 
        'input_format': 'json', 
        'output_format': 'json', 
        'input_data': [json.dumps(input_data)]
        }
    create_mail = requests.get('https://api.beget.com/api/mail/createMailbox', params=params)
    return create_mail.content

@app.route('/del')
def delete_mail():
    username = request.args.get('username')
    input_data = {"domain":"test8999.ru","mailbox":f"{username}"}
    params = {'login': 'vevmkycf', 
        'passwd': 'RI*5Xut4', 
        'input_format': 'json', 
        'output_format': 'json', 
        'input_data': [json.dumps(input_data)]
        }
    delete_mail = requests.get('https://api.beget.com/api/mail/dropMailbox', params=params)
    return delete_mail.content

if __name__ == "__main__":
    app.run(debug=True,port=5555,host='0.0.0.0')