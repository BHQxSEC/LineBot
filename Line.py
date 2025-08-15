import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, MessageAction

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")

if not CHANNEL_SECRET or not CHANNEL_TOKEN:
    raise RuntimeError("Set LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN environment variables.")

line_bot_api = LineBotApi(CHANNEL_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():

    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400, "Invalid signature")
    return "OK", 200

rich_menu_to_create = RichMenu(
    size={"width": 2500, "height": 843},
    selected=True,
    name="เมนูหลัก",
    chat_bar_text="แตะที่นี่",
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
            action=MessageAction(label="1", text="Flag คือข้อมูลที่ใช้ยืนยันใน CTF")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=0, width=1250, height=843),
            action=MessageAction(label="2", text="อืม… ขอคิดก่อนนะ 🤔")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
            action=MessageAction(label="3", text="ก็ได้… แต่เป็นความลับนะ ████████████████████████")
        )
    ]
)

rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

with open("menu_image.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

line_bot_api.set_default_rich_menu(rich_menu_id)





@app.get("/")
def health():
    return "LINE bot up ✅", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
