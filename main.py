from flask import *
from flask_ngrok import run_with_ngrok
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import speech_recognition as sr #
from pydub import AudioSegment
import requests
from pprint import pprint
import json
import openai
openai.api_key = '' 

#Messaging API settings/Channel access token
line_bot_api = LineBotApi('')#Channel access token

#Basic settings/Channel secret 
handler = WebhookHandler('')#你的Channel secret

app_id = ''
app_key = ''
auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
url = "https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/LiveBoard/KRTC?&%24format=JSON"

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return{
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }

class data():

    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')

        return{
            'authorization': 'Bearer '+access_token
        }

app = Flask(__name__)
run_with_ngrok(app)   
@app.route("/")
def home():
    return "<h1>test</h1>"

@app.route("/user/<username>")
def user(username):
    return "<h1>" + username + ",</h1>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
tdx_model=False
ai_model=False
#實際處理訊息的部份
@handler.add(MessageEvent)
def handle_message(event):
  global tdx_model
  global ai_model
  replyMsg= TextSendMessage(text="首頁模式")
  if(event.message.text=="結束"):
    tdx_model=False
    ai_model=False
    replyMsg= TextSendMessage(text="首頁模式")

  if(tdx_model):
    msg=""
    da=event.message.text
    LineID,StationName=da.split(" ")
    try:
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())
    except:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())

    data_js=json.loads(data_response.text)  
    for i in data_js:
      if(i["LineID"]==LineID and i["StationName"]["Zh_tw"]==StationName):
        print(f'{i["TripHeadSign"]}還有{i["EstimateTime"]}分鐘')
        msg+=(i["TripHeadSign"]+"還有"+str(i["EstimateTime"])+"分鐘\n")

    replyMsg= TextSendMessage(text=msg)      #回覆文字=收到的文字
  
  if(ai_model):
    messages = '' 
    msg = event.message.text
    messages = f'{messages}{msg}\n'   
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=msg,
        max_tokens=128,
        temperature=0.5
    )
    ai_msg = response['choices'][0]['text'].replace('\n','')
    print('ai > '+ai_msg)
    messages = f'{messages}\n{ai_msg}\n\n'  # 合併 AI 回應的話     
    replyMsg1=ai_msg #應聲蟲
    replyMsg=TextSendMessage(text=replyMsg1)#回覆文字=收到的文字

  if(event.message.text=="高捷"):
    tdx_model=True
    replyMsg= TextSendMessage(text="請輸入路線及站名e.g.,R 左營")
  if(event.message.text=="AI"):
    ai_model=True
    replyMsg= TextSendMessage(text="AI對話模式")

  line_bot_api.reply_message(
      event.reply_token,#回復訊息的密碼
      replyMsg
  )
  print(tdx_model)
app.run()