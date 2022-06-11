import subprocess
import threading
import time
import requests
import json
import sys
import logging
from flask import Flask, request

def print_menu():       ## Your menu design here
    print(30 * "-" , "MENU CATALYST SCHOOL" , 30 * "-")
    print("1. Create did:prism")
    print("2. Resolve DID")
    print("3. Create out-of-band invitation")
    print("4. Receive out-of-band invitation")
    print("5. Send txt message")
    print("6. Send my prism:did")
    print("7. Exit")
    print(67 * "-")
    
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/webhook/topic/connections/', methods=['POST'])
def connections():
    if request.method == 'POST':
        # print("Data received from Webhook is: ", request.json)
        if "connection_id" in request.json and request.json["connection_id"]:
            global connection_id
            connection_id = request.json["connection_id"]
        if "state" in request.json and request.json["state"] == 'completed':
            print('Connection established')
        return "OK"
    
@app.route('/webhook/topic/basicmessages/', methods=['POST'])
def basicmessages():
    if request.method == 'POST':
        print("Message received: ", request.json["content"])
        return "OK"
@app.route('/webhook/topic/issue_credential_v2_0/', methods=['POST'])
def issue_credential():
    if request.method == 'POST':
        if request.json['state'] == "credential-received":
            print("Credential received: ", request.json)
        if request.json['state'] == "request-received":
            print("Credential request received")
        return "OK"

args = [
    "python3",
    "-m",
    "aries_cloudagent",
    "start",
    "--endpoint", "http://127.0.0.1:8020",
    "--label", "faber.agent",
    "--inbound-transport", "http", "0.0.0.0", "8020",
    "--outbound-transport", "http",
    "--admin", "0.0.0.0", "8021",
    "--admin-insecure-mode",
    "--preserve-exchange-records",
    "--auto-provision",
    "--no-ledger",
    "--trace-target", "log",
    "--trace-tag", "acapy.events",
    "--trace-label", "faber.agent.trace",
    "--auto-ping-connection",
    "--auto-respond-message",
    "--auto-accept-invites",
    "--auto-accept-requests",
    "--auto-respond-credential-proposal",
    "--auto-respond-credential-offer",
    "--auto-respond-credential-request",
    "--auto-store-credential",
    "--storage-type", "memory",
    "--wallet-local-did",
    "--wallet-type", "basic",
    "--wallet-storage-type", "basic",
    "--wallet-name", "faber.agent420699",
    "--wallet-key", "faber.agent420699",
    "--webhook-url", "http://localhost:8022/webhook",
    "--log-level", "debug",
    "--log-file", "./faber.log"
]

def acapy(args):
    global process
    process = subprocess.Popen(args)
    process.communicate()

acapy_thread = threading.Thread(target=lambda: acapy(args))
acapy_thread.daemon = True
acapy_thread.start()

webhook_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8022, debug=False, use_reloader=False))
webhook_thread.daemon = True
webhook_thread.start()
time.sleep(5)
loop=True
api_url = "http://localhost:8021"     
  
while loop:
    print_menu()
    choice = int(input("Enter your choice [1-7]: "))
     
    if choice==1:     # CREATE DID:PRISM
        print("Creating did:prism")
        resp = requests.post(api_url + "/wallet/did/create", json = {
                "method": "prism",
                "options": {
                "key_type": "secp256k1"
                }
            })
        did = resp.json()["result"]["did"]
        print("Faber DID: " + did)
        print("This DID is already posted to prism node and stored in wallet")
    elif choice==2:     # RESOLVE DID
        did_to_resolve = input("DID:")
        try:
            resp = requests.get(api_url + "/resolver/resolve/"+did_to_resolve)
            print("DID Document:",resp.json()['did_document'])
        except:
            print("DID not found")
    elif choice==3:     # CREATE OOB INVITATION
        resp = requests.post(api_url + "/out-of-band/create-invitation", json = {
                    "alias": "ToAlice",
                    "handshake_protocols": [
                    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0"],
                    "metadata": {},
                    "my_label": "Invitation to Alice",
                    "use_public_did": False
                }
            )
        print("Invitation:")
        print(resp.json()["invitation"])
    elif choice==4:     # RECEIVE OOB INVITATION
        invitation = input("Paste invitation here:").replace("\'", "\"")
        #print(json.loads(invitation))
        resp = requests.post(api_url + "/out-of-band/receive-invitation", json = json.loads(invitation))
        # print(resp.json())
    elif choice==5:     # # SEND TXT MSG
        txtmsg = input("Message: ")
        resp = requests.post(api_url + "/connections/" + connection_id + "/send-message", json = {
            "content": txtmsg 
        })
        # print(resp.json())
    elif choice==6:     # # SEND DID
        resp = requests.post(api_url + "/connections/" + connection_id + "/send-message", json = {
            "content": did 
        })
    elif choice==7:
        acapy_thread.join(1)
        if acapy_thread.is_alive():
             print('Stoping agent')
             process.terminate()
             acapy_thread.join()
        sys.exit()
        
    else:
        print("Wrong option selection.")