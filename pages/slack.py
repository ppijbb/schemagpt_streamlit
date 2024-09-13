import streamlit as st
import socketio
import asyncio
import logging
import requests
from threading import Lock
import os
from slack_bolt import App
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler


# oauth_settings = AsyncOAuthSettings(
#     client_id=st.secrets["SLACK_CLIENT_ID"],
#     client_secret=st.secrets["SLACK_CLIENT_SECRET"],
#     scopes=["channels:read", "groups:read", "chat:write"],
#     user_scopes=["user:read"],
#     installation_store=FileInstallationStore(base_dir="./data/installations"),
#     state_store=FileOAuthStateStore(expiration_seconds=100, base_dir="./data/states")
# )

app = AsyncApp(
    signing_secret=st.secrets["SLACK_SIGNING_SECRET"],
    token=os.environ["SLACK_BOT_TOKEN"],
    # oauth_settings=oauth_settings
)
SLACK_BOT_ENDPOINT = f"https://slack.com/api/chat.postMessage?token={st.secrets['SLACK_BOT_TOKEN']}&channel=%s&text=%s"
SLACK_EVENT_ENDPOINT = "https://slack.com/api/events.listen"

async def sock():
    app.client.apps_connections_open(app_token=os.environ["SLACK_APP_TOKEN"])
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_BOT_TOKEN"])
    await handler.start_async()

if 'current_text' not in st.session_state:
    st.session_state['current_text'] = ''
    
@app.command("/hello-bolt")
async def hello(body, ack):
    logging.warn(body["user_id"])
    ack(f"Hi <@{body['user_id']}>!")

@app.event({
    "type": "message",
    "subtype": "message_changed"
})
async def log_message_change(logger, event):
    user, text = event["user"], event["text"]
    logger.info(f"The user {user} changed the message to {text}")

@app.event("app_mention")
async def handle_mentions(event, client, message, say):  # async function
    logging.warn("message ", message)
    st.session_state['current_text'] = message
    result = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+ os.environ["SLACK_APP_TOKEN"]},
        data={"channel": event["channel"],"text": "what's up"}
    )
    api_response = await client.reactions_add(
        channel=event["channel"],
        timestamp=event["ts"],
        name="eyes",
    )
    await say(text="What's up?", channel=event["channel"])

@app.message("hello")
async def message_hello(message, say):
    await say(f"Hey there <@{message['user']}>!")


if 'sio' not in st.session_state:
    st.session_state['sio'] = socketio.Client()
    # handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    # handler.start()
    asyncio.run(sock())


if __name__ == "__main__":
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

    if st.button('Disconnect'):
        st.session_state['sio'].disconnect()
        st.write('Disconnected from server')
    st.markdown(
        f"""
    <a href="https://slack.com/oauth/v2/authorize?client_id={st.secrets["SLACK_CLIENT_ID"]}&scope=chat:write,chat:write.customize&user_scope=chat:write"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
    <meta name="slack-app-id" content="A07LC0Q7324">
    """, unsafe_allow_html=True
    )