import json
import urllib
from urllib.parse import unquote as decode
from flask import Flask, request, make_response
import requests 
from functions.get_news import get_ntut, get_ntou, get_tmu, get_ntpu
from functions.logs import logs_red, logs_green, logs_yellow, logs_blue

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
    except:
        content = {
            "code": 406,
            "status": "NOT_ACCEPTABLE",
            "message": "No given data",
        }
        return content, 406
    else:
        print(str(data))
        responseId = data['responseId']
        logs_blue('responseId: ' + responseId)
        intent = data['queryResult']['intent']['displayName']
        get_news = {}
        mess = ''
        mess_detail_display = '\n'
        mess_detail_voice = '\n'

        if intent == 'NTPU':
            mess += '這裡是「北大」的最新三則通知：'
            mess_detail_voice += mess + '<break time=\"250ms\" />'
            get_news = get_ntpu()
            for i in range(3):
                mess_detail_display += str(i+1) + '. ' + get_news[i]['title'] + '\n'
                mess_detail_voice += str(i+1) + '. ' + get_news[i]['title'] + '<break time=\"250ms\" />\n'

        elif intent == 'NTUT':
            mess += '這裡是「北科」的最新三則通知：'
            mess_detail_voice += mess + '<break time=\"250ms\" />'
            get_news = get_ntut()
            for i in range(3):
                mess_detail_display += str(i+1) + '. ' + get_news[i]['title'] + '\n'
                mess_detail_voice += str(i+1) + '. ' + get_news[i]['title'] + '<break time=\"250ms\" />\n'

        elif intent == 'TMU':
            mess += '這裡是「北醫」的最新三則通知：'
            mess_detail_voice += mess + '<break time=\"250ms\" />'
            get_news = get_tmu()
            for i in range(3):
                mess_detail_display += str(i+1) + '. ' + get_news[i]['title'] + '\n'
                mess_detail_voice += str(i+1) + '. ' + get_news[i]['title'] + '<break time=\"250ms\" />\n'

        elif intent == 'NTOU':
            mess += '這裡是「海大」的最新三則通知：'
            mess_detail_voice += mess + '<break time=\"250ms\" />'
            get_news = get_ntou()
            for i in range(3):
                mess_detail_display += str(i+1) + '. ' + get_news[i]['title'] + '\n'
                mess_detail_voice += str(i+1) + '. ' + get_news[i]['title'] + '<break time=\"250ms\" />\n'
        else:
            return 403

        if(check_WEB_BROWSER(data)):
            content = get_response_screen(get_news, mess)
        else:
            mess_detail_display = mess + mess_detail_display
            mess_detail_display += '您可以使用有螢幕之裝置查看更多！'
            mess_detail_voice += '您可以使用有螢幕之裝置查看更多！'
            content = get_response_voice(mess_detail_display, mess_detail_voice)
        return content, 200

@app.route('/ntou', methods=['GET'])
def ntou_test():
    return str(get_ntou())
    
@app.route('/ntut', methods=['GET'])
def ntut_test():
    return str(get_ntut())

@app.route('/tmu', methods=['GET'])
def tmu_test():
    return str(get_tmu())

@app.route('/ntpu', methods=['GET'])
def ntpu_test():
    return str(get_ntpu())

def get_response_screen(json_data, simpleMess):
    logs_green('Screen')
    response = {
        "payload": {
            "google": {
                "expectUserResponse": True,
                "richResponse": {
                    "items": [{
                        "simpleResponse": {
                            "textToSpeech": simpleMess
                        }
                    },{
                        "carouselBrowse": {
                        "items": [
                            {
                                "title": "第一則通知",
                                "openUrlAction": {
                                    "url": json_data[0]['link']
                                },
                                "description": json_data[0]['title'],
                                "footer": json_data[0]['published']
                            },
                            {
                                "title": "第二則通知",
                                "openUrlAction": {
                                    "url": json_data[1]['link']
                                },
                                "description": json_data[1]['title'],
                                "footer": json_data[1]['published']
                            },
                            {
                                "title": "第三則通知",
                                "openUrlAction": {
                                    "url": json_data[2]['link']
                                },
                                "description": json_data[2]['title'],
                                "footer": json_data[2]['published']
                            }
                        ]}
                    }]
                }
            }
        }
    }
    return response

def get_response_voice(mess_detail_display,mess_detail_voice):
    logs_green('Voice')
    response = {
        "payload": {
            "google": {
                "expectUserResponse": True,
                "richResponse": {
                    "items": [{
                        "simpleResponse": {
                            "textToSpeech": '<speak>' + mess_detail_voice + '</speak>',
                            "displayText": mess_detail_display
                        }
                    }]
                }
            }
        }
    }
    return response

def check_WEB_BROWSER(check_data):
    item = check_data['originalDetectIntentRequest']['payload']['surface']['capabilities']
    flag = False
    for data in item:
        if data['name'] == 'actions.capability.WEB_BROWSER':
            flag = True
    return flag

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)