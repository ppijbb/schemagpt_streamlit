from streamlit_webrtc import RTCConfiguration
from pages.rtc.public_stun import public_stun_server_list


RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": public_stun_server_list
            },
        ]
    }
)