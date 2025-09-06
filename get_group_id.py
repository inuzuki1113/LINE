import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "UXbkRhFPsKjNCkwGOvbF8pctURapd3sv2aHfn2jyJL6nikPPRVJSDzQoB8Crw1rTA/Gil9KM4R2CNhZsm/jHhlCef5zZwma/SSCknzKXHhDBePqpHzxoxrcSYpv2K8KN7xrA7cLAjOQ8kL74yrWGEwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "3dbf05dbaded06a1819b3b4dbeea62a8"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.type == "group":
        group_id = event.source.group_id
        print("Group ID:", group_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"Group ID取得しました: {group_id}")
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

