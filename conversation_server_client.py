import requests
import json
import logging
import traceback

class ConversationServerClient:
    
    def __init__(self,conversation_server_ip, conversation_server_port,response_callback):
        self.conversation_server_ip = conversation_server_ip
        self.conversation_server_port = str(conversation_server_port)
        self.response_callback = response_callback
        
    def respondTo(self,  text):
        payload = {
            "sender": "User",
            "message": "\"" + text + "\""
        }
        headers = {'content-type': 'application/json'}
        
        raw_response = "nothing"
        try:
            r = requests.post("http://" +self.conversation_server_ip+ ":"+self.conversation_server_port+"/webhooks/rest/webhook", json=payload, headers=headers)
            raw_response = r.text
            self.response_callback(str(json.loads(r.text)[0]['text']))
            print("Response to " + text + " from Conversation Server: " + str(json.loads(r.text)[0]['text']))
        except Exception: 
            # traceback.print_exc()
            logging.error("Failed to connect to conversation server or process JSON response")
            logging.error("Raw response: " + raw_response)
            self.response_callback("Oh, I ran into an error. I cannot respond now, sorry.")