# flask, django 主要兩個架網站的伺服器套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('E2lN4iNosxsyq22IXjdPST30pprLUR9Mw9evBC857n5uMbJN+h7Hog6HqgY9GlDtUuISniCJnuTtlPRZlcmJjzhSBeLXUIJOrGlRNOlg3MCt7/ExrGATUzaFTbxr2cQuDJkgi+opPI4ipWMVGveQAAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3a26d7c9e408a678896c5e2aa2e6639b')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，您說什麼'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return
    
    if ['snoopy', 'Snoopy', '史努比'] in msg:
        r = '這個爛東西~'
        sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002772'
        )
        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return

    if msg in ['hi', 'Hi', '哈囉']:
        r = 'hi'
    elif msg =='你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '你想訂位，是嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()


