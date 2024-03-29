from streamlit_webrtc import RTCConfiguration
from pages.rtc.public_stun import public_stun_server_list


RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": public_stun_server_list
            },
            # {
            #     "urls": "turn:openrelay.metered.ca:80",
            #     "username": "openrelayproject",
            #     "credential": "openrelayproject",
            # },
            # {
            #     "urls": "turn:openrelay.metered.ca:443",
            #     "username": "openrelayproject",
            #     "credential": "openrelayproject",
            # },
            # {
            #     "urls": "turn:openrelay.metered.ca:443?transport=tcp",
            #     "username": "openrelayproject",
            #     "credential": "openrelayproject",
            # },
            # {
            #     "urls": "turn:numb.viagenie.ca",
            #     "username": 'webrtc@live.com',
            #     "credential": 'muazkh'
            # },
            # {
            #     "urls": "turn:192.158.29.39:3478?transport=udp",
            #     "username": '28224511:1379330808',
            #     "credential": 'JZEOEt2V3Qb0y27GRntt2u2PAYA='
            # },
            # {
            #     "urls": "turn:192.158.29.39:3478?transport=tcp",
            #     "username": '28224511:1379330808',
            #     "credential": 'JZEOEt2V3Qb0y27GRntt2u2PAYA='
            # }
        ]
    }
)