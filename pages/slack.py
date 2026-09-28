import streamlit as st
import socketio
import asyncio
import logging
import requests
import threading
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from srcs.st_utils import missing_secrets


REQUIRED_SECRETS = ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "SLACK_CLIENT_ID"]
missing = missing_secrets(*REQUIRED_SECRETS)
if missing:
    st.set_page_config(page_title="slack bot",
                       page_icon="💬",
                       layout="wide",
                       initial_sidebar_state="auto",)
    st.title('Slack Bot test ground')
    st.info(f"이 데모는 Slack 앱 설정이 필요합니다 (누락: {', '.join(missing)}).")
    st.stop()

app = AsyncApp(
    token=st.secrets["SLACK_BOT_TOKEN"],
    oauth_settings=None
)
SLACK_BOT_ENDPOINT = f"https://slack.com/api/chat.postMessage?token={st.secrets['SLACK_BOT_TOKEN']}&channel=%s&text=%s"
SLACK_EVENT_ENDPOINT = "https://slack.com/api/events.listen"

async def sock():
    app.client.apps_connections_open(app_token=st.secrets["SLACK_APP_TOKEN"])
    handler = AsyncSocketModeHandler(app=app, app_token=st.secrets["SLACK_APP_TOKEN"])
    await handler.start_async()
    logging.warning("handler started")

if 'current_text' not in st.session_state:
    st.session_state['current_text'] = ''
    
@app.command(command="/hello-bolt")
async def hello(body, ack):
    logging.warning(body["user_id"])
    ack(f"Hi <@{body['user_id']}>!")

@app.event(event={"type": "message", "subtype": "message_changed"})
async def log_message_change(logger, event):
    user, text = event["user"], event["text"]
    logger.info(f"The user {user} changed the message to {text}")
    logging.warning(f"The user {user} changed the message to {text}")

CURRENT_TEXT_MAX_LEN = 10000


@app.event(event="app_mention")
async def handle_mentions(event, client, message, say):  # async function
    logging.warning("message ", message)
    if isinstance(message, str):
        text = message
    elif isinstance(message, dict):
        text = message.get("text", str(message))
    else:
        text = str(message)
    st.session_state["current_text"] = (
        text[:CURRENT_TEXT_MAX_LEN] if len(text) > CURRENT_TEXT_MAX_LEN else text
    )
    result = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + st.secrets["SLACK_APP_TOKEN"]},
        data={"channel": event["channel"],"text": "what's up"}
    )
    api_response = await client.reactions_add(
        channel=event["channel"],
        timestamp=event["ts"],
        name="eyes",
    )
    await say(text="What's up?", channel=event["channel"])

@app.message(keyword="hello")
async def message_hello(message, say):
    await say(text=f"Hey there <@{message['user']}>!")


if 'sio' not in st.session_state:
    st.session_state['sio'] = socketio.Client()
    threading.Thread(target=lambda: asyncio.run(sock()), daemon=True).start()


if __name__ == "__main__":
    st.set_page_config(page_title="slack bot",
                       page_icon="💬",
                       layout="wide",
                       initial_sidebar_state="auto",)
    app.start()
    st.title('Slack Bot test ground')
    st.markdown('''            
            ## 프로젝트 소개
            
                Slack Bot을 테스트하는 페이지
                socket 통신으로 봇 동작
                

            ## 개발 내용
            - 요청 처리하는 Slack bot

            ## 사용 기술
            <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
            <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
            ''', unsafe_allow_html=True)

    # Display the current text
    st.text("received text"+st.session_state['current_text'])

    if st.button("Disconnect"):
        if st.session_state.get("sio") is not None:
            st.session_state["sio"].disconnect()
            st.session_state.pop("sio", None)
        st.write("Disconnected from server")
    st.markdown(
        f"""
    <a href="https://slack.com/oauth/v2/authorize?client_id={st.secrets["SLACK_CLIENT_ID"]}&scope=chat:write,chat:write.customize&user_scope=chat:write"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
    <meta name="slack-app-id" content="A07LC0Q7324">
    """, unsafe_allow_html=True
    )
