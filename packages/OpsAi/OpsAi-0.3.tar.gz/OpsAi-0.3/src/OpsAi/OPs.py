import requests
import json


class Ai:
    def __init__(self, query):
        self.query = query

    def chat(self):
        query = self.query
        headers = {
            'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
            'Connection': 'keep-alive',
            'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
            'Accept': '*/*',
            'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-GB,en;q=0.9'
        }

        data = {
            'data': {
                'message': query,
            }
        }
        url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'
        response = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            result = response.json()["result"]["choices"][0]["text"]
            return result
        except:
            return None

    def En(self):
        query = self.query
        headers = {
            'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
            'Connection': 'keep-alive',
            'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
            'Accept': '*/*',
            'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-GB,en;q=0.9'
        }

        data = {
            'data': {
                'message': "Translate into English only : \n " + query,
            }
        }
        url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'
        response = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            result = response.json()["result"]["choices"][0]["text"]
            return result
        except:
            return None

    def Ar(self):
        query = self.query
        headers = {
            'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
            'Connection': 'keep-alive',
            'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
            'Accept': '*/*',
            'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-GB,en;q=0.9'
        }

        data = {
            'data': {
                'message': "Translate into Arabic only : \n " + query,
            }
        }
        url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'
        response = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            result = response.json()["result"]["choices"][0]["text"]
            return result
        except:
            return None

    def explain(self):
        query = self.query
        headers = {
            'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
            'Connection': 'keep-alive',
            'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
            'Accept': '*/*',
            'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-GB,en;q=0.9'
        }

        data = {
            'data': {
                'message': " Explain and analyze the code only, and if I ask you about any other question, tell me that I could not find the codes Just : \n " + query,
            }
            # Explain and analysis the code only and do not answer any other question, just tell him I did not find the code
        }
        url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'
        response = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            result = response.json()["result"]["choices"][0]["text"]
            return result
        except:
            return None

    def code(self):
        query = self.query
        headers = {
            'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
            'Connection': 'keep-alive',
            'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
            'Accept': '*/*',
            'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-GB,en;q=0.9'
        }

        data = {
            'data': {
                'message': " You and your guest are to write the code only Do not answer any questions other than writing code  : \n  " + query,
            }
            # Explain and analysis the code only and do not answer any other question, just tell him I did not find the code ???
        }
        url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'
        response = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            result = response.json()["result"]["choices"][0]["text"]
            return result
        except:
            return None

    def revision_ar(self):
        query = self.query
        headers = {
            'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
            'Connection': 'keep-alive',
            'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
            'Accept': '*/*',
            'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-GB,en;q=0.9'
        }

        data = {
            'data': {
                'message': "صحح لي باللغة العربية هذي الجملة من الاخطاء نحوية و الاملائية : \n " + query,
            }
        }
        url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'
        response = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            result = response.json()["result"]["choices"][0]["text"]
            return result
        except:
            return None

    def revision_En(self):
        query = self.query
        headers = {
            'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
            'Connection': 'keep-alive',
            'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
            'Accept': '*/*',
            'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-GB,en;q=0.9'
        }

        data = {
            'data': {
                'message': "Just correct the mistakes in the English words only : \n " + query,
            }
        }
        url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'
        response = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            result = response.json()["result"]["choices"][0]["text"]
            return result
        except:
            return None
