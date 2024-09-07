import streamlit as st
import socketio
from threading import Lock
import os
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_bolt.adapter.socket_mode import SocketModeHandler

oauth_settings = OAuthSettings(
    client_id=st.secrets["SLACK_CLIENT_ID"],
    client_secret=st.secrets["SLACK_CLIENT_SECRET"],
    scopes=["channels:read", "groups:read", "chat:write"],
    user_scopes=["user:read"],
    installation_store=FileInstallationStore(base_dir="./data/installations"),
    state_store=FileOAuthStateStore(expiration_seconds=100, base_dir="./data/states")
)

app = App(
    signing_secret=st.secrets["SLACK_SIGNING_SECRET"],
    token=os.environ["SLACK_BOT_TOKEN"],
    oauth_settings=oauth_settings
)


if 'sio' not in st.session_state:
    st.session_state['sio'] = socketio.Client()
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

if 'current_text' not in st.session_state:
    st.session_state['current_text'] = ''


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
    

@st.session_state.sio.on('text_update')
def on_text_update(data):
    print(data)
    st.session_state['current_text'] = data['text']

# Display the current text
st.text(st.session_state['current_text'])

if st.button('Disconnect'):
    st.session_state['sio'].disconnect()
    st.write('Disconnected from server')
st.markdown(
    f"""
<a href="https://slack.com/oauth/v2/authorize?client_id={st.secrets["SLACK_CLIENT_ID"]}&scope=chat:write,chat:write.customize&user_scope=chat:write"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
""", unsafe_allow_html=True
)