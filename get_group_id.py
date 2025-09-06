from flask import Flask, request, abort, render_template_string
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "UXbkRhFPsKjNCkwGOvbF8pctURapd3sv2aHfn2jyJL6nikPPRVJSDzQoB8Crw1rTA/Gil9KM4R2CNhZsm/jHhlCef5zZwma/SSCknzKXHhDBePqpHzxoxrcSYpv2K8KN7xrA7cLAjOQ8kL74yrWGEwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "3dbf05dbaded06a1819b3b4dbeea62a8"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 受信ログを保持する簡易リスト
logs = []

@app.route("/")
def index():
    # 最新10件を表示
    return render_template_string("""
        <h2>BOT ログ</h2>
        <ul>
        {% for log in logs[-10:] %}
            <li>{{ log }}</li>
        {% endfor %}
        </ul>
    """, logs=logs)

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
        log_msg = f"Group ID取得: {group_id}"
        logs.append(log_msg)  # リストに追加
        print(log_msg)  # コンソールにも出力
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"Group ID取得しました: {group_id}")
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)


