import streamlit as st
import streamlit.components.v1 as components
from streamlit_shap import st_shap

import numpy as np
import shap

from srcs.st_cache import get_or_create_eventloop, get_dep_scale_model
from srcs.st_style_md import hide_radio_value_md


def view():
    shap.plots.initjs()
    hide_radio_value_md()
    st.title('👩‍⚕️📝🙍‍♂️ Depression self-scoring inventory Analysis')
    st.markdown("")
    st.image("pages/image/dep_scale/output.png")


if __name__ == "__main__":
    st.set_page_config(page_title="depressive scale",
                       page_icon="👩‍⚕️",
                       layout="wide",
                       initial_sidebar_state="auto",)
    scale_xgb, explainer = get_dep_scale_model()
    view()
    with st.form("BDI"):
        bdi_1 = st.radio(
            label="슬픔",
            options=[0, 1, 2, 3],
            captions=["나는 슬프지 않다",
                      "나는 슬플 때가 자주 있다",
                      "나는 항상 슬프다",
                      "나는 너무 슬프고 불행해서 결딜 수가 없다"],
            key="bdi1",
            horizontal=False)
        bdi_2 = st.radio(
            label="비관주의",
            options=[0, 1, 2, 3],
            captions=["나는 미래에 대해 낙심하지 않는다",
                      "나는 이전에 비해 미래에 대한 희망이 줄었다",
                      "나는 내 앞날이 잘 풀릴 것이라고 기대하지 않는다",
                      "나는 미래가 희망이 없고 점점 더 나빠질 것 같은 느낌이 든다"],
            key="bdi2",
            horizontal=False)
        bdi_3 = st.radio(
            label="과거의 실패",
            options=[0, 1, 2, 3],
            captions=["나는 나 자신을 실패자라고 느끼지 않는다",
                      "나는 생각보다 많은 실패를 했다",
                      "돌이켜보면, 나는 너무 많은 실패를 했다",
                      "나는 인간으로서 완전히 실패한 것 같다"],
            key="bdi3",
            horizontal=False)
        bdi_4 = st.radio(
            label="즐거움 상실",
            options=[0, 1, 2, 3],
            captions=["나는 이전처럼 내가 좋아하는 일을 하면서 즐거움을 느낀다",
                      "나는 이전만큼 일을 즐기지 못하고 있다",
                      "나는 이전과 달리 일에서 즐거움을 거의 느끼지 못하고 있다",
                      "나는 이전과 달리 어떤 일에서도 즐거움을 느끼지 못하고 있다"],
            key="bdi4",
            horizontal=False)
        bdi_5 = st.radio(
            label="죄책감",
            options=[0, 1, 2, 3],
            captions=["나는 특별히 죄책감을 느끼지 않는다",
                      "나는 내가 했던 일이나 하지 못했던 일 떄문에 죄책감을 느낀다",
                      "나는 죄책감을 느낄 때가 자주 있다",
                      "나는 항상 죄책감을 느낀다"],
            key="bdi5",
            horizontal=False)
        bdi_6 = st.radio(
            label="벌 받는 느낌",
            options=[0, 1, 2, 3],
            captions=["나는 벌을 받고 있다고 느끼지 않는다",
                      "나는 벌을 받을지도 모른다는 느낌이 든다",
                      "나는 벌을 받을 것 같다",
                      "나는 지금 벌을 받고 있다는 느낌이 든다"],
            key="bdi6",
            horizontal=False)
        bdi_7 = st.radio(
            label="자기혐오",
            options=[0, 1, 2, 3],
            captions=["나는 나 자신에 대해 변함없이 같은 느낌이다",
                      "나는 나 자신에 대한 믿음이 없어졌다",
                      "나는 나 자신에 대해 실망하고 있다",
                      "나는 나 자신을 혐오한다"],
            key="bdi7",
            horizontal=False)
        bdi_8 = st.radio(
            label="자기비판",
            options=[0, 1, 2, 3],
            captions=["나는 이전에 비해 자신을 더 탓하거나 비난하지 않는다",
                      "나는 이전에 비해 나 자신을 더 많이 탓한다",
                      "내가 저지른 실수는 다 나의 잘못 때문이라고 생각한다",
                      "안 좋은 일이 벌어지면 다 나 때문인 것 같아 자신을 비난한다"],
            key="bdi8",
            horizontal=False)
        bdi_9 = st.radio(
            label="자살 사고 및 자살 소망",
            options=[0, 1, 2, 3],
            captions=["나는 자살같은 것은 생각하지 않는다",
                      "나는 자살을 생각해 본 적은 있지만, 행동으로 옮기지는 않을 것이다",
                      "나는 자살을 하고 싶다",
                      "나는 기회만 있으면 자살할 것이다"],
            key="bdi9",
            horizontal=False)
        bdi_10 = st.radio(
            label="울음",
            options=[0, 1, 2, 3],
            captions=["나는 이전보다 울음이 더 많아지지 않았다",
                      "나는 이전보다 울음이 더 많아졌다",
                      "나는 사소한 일에도 울음이 터져 나온다",
                      "나는 울고 싶어도 울 기력조차 없다"],
            key="bdi10",
            horizontal=False)
        bdi_11 = st.radio(
            label="초조",
            options=[0, 1, 2, 3],
            captions=["나는 이전보다 더 초조하거나 긴장되지 않는다",
                      "나는 이전보다 더 초조하고 긴장된다",
                      "나는 너무 초조해서 가만히 있기가 어렵다",
                      "나는 너무 초조해서 계속 움직이거나 뭐든 하고 있어야 한다"],
            key="bdi11",
            horizontal=False)
        bdi_12 = st.radio(
            label="흥미상실",
            options=[0, 1, 2, 3],
            captions=["나는 사람들이나 일에 대한 관심이 변하지 않았다",
                      "나는 사람들이나 일에 대한 관심이 이전에 비해 줄어들었다",
                      "나는 사람들이나 일에 대한 관심이 많이 줄어들었다",
                      "나는 어떤 것에도 관심을 갖기가 힘들다"],
            key="bdi12",
            horizontal=False)
        bdi_13 = st.radio(
            label="우유부단",
            options=[0, 1, 2, 3],
            captions=["나는 이전처럼 결정을 잘 내린다",
                      "나는 이전처럼 결정을 내리기가 힘들다",
                      "나는 이전처럼 결정을 내리는 것이 너무 힘들다",
                      "나는 어떤 결정도 내리기 힘들다"],
            key="bdi13",
            horizontal=False)
        bdi_14 = st.radio(
            label="무가치함",
            options=[0, 1, 2, 3],
            captions=["나는 내가 무가치한 사람이라고 느끼지 않는다",
                      "나는 내가 이전만큼 가치 있고 쓸모 있는 사람이라는 생각이 들지 않는다",
                      "나는 다른 사람들보다 무가치한 사람이라는 느낌이 든다",
                      "나는 완전히 무가치한 사람이라는 느낌이 든다"],
            key="bdi14",
            horizontal=False)
        bdi_15 = st.radio(
            label="기력상실",
            options=[0, 1, 2, 3],
            captions=["나는 이전에 비해 기력이 떨어지지 않았다",
                      "나는 이전보다 기력이 떨어졌다",
                      "나는 기력이 많이 떨어졌다",
                      "나는 기력이 없어 아무 일도 할 수가 없다"],
            key="bdi15",
            horizontal=False)
        bdi_16 = st.radio(
            label="수면 양상 변화",
            options=[0, 1, 2, 3],
            captions=["나는 수면 양상에 변화가 없다",
                      "나는 이전보다 잠이 약간 늘었다/줄었다",
                      "나는 이전보다 잠이 훨씬 늘었다/줄었다",
                      "나는 하루 종일 잠을 잔다/전보다 일찍 잠에 깨고 다시 잠들기 어렵다"],
            key="bdi16",
            horizontal=False)
        bdi_17 = st.radio(
            label="짜증",
            options=[0, 1, 2, 3],
            captions=["나는 이전에 비해 짜증이 심해지지 않는다",
                      "나는 이전에 비해 짜증이 약간 늘었다",
                      "나는 이전에 비해 짜증이 훨씬 심해졌다",
                      "나는 항상 짜증이 난다"],
            key="bdi17",
            horizontal=False)
        bdi_18 = st.radio(
            label="식욕 변화",
            options=[0, 1, 2, 3],
            captions=["나는 식욕에 변화가 없다",
                      "나는 이전에 비해 식욕이 약간 늘었다/줄었다",
                      "나는 이전에 비해 식욕이 많이 늘었다/줄었다",
                      "나는 식욕이 전혀없다/음식에 대한 욕구가 심해졌다"],
            key="bdi18",
            horizontal=False)
        bdi_19 = st.radio(
            label="주의 집중 어려움",
            options=[0, 1, 2, 3],
            captions=["나는 이전 처럼 집중을 잘 할 수 있다",
                      "나는 이전 처럼 집중을 잘 할 수 없다",
                      "나는 어떤 일에도 오래 집중하기가 어렵다",
                      "나는 어떤 일에도 전혀 집중할 수가 없다"],
            key="bdi19",
            horizontal=False)
        bdi_20 = st.radio(
            label="피로감",
            options=[0, 1, 2, 3],
            captions=["나는 평소보다 더 피곤하지 않다",
                      "나는 평소보다 더 쉽게 피곤해진다",
                      "나는 너무 피곤해서 이전에 해왔던 많은 일들을 하기 힘들다",
                      "나는 너무 피곤해서 이전에 해왔던 일들을 아무 것도 할 수 없다"],
            key="bdi20",
            horizontal=False)
        bdi_21 = st.radio(
            label="성에 대한 흥미상실",
            options=[0, 1, 2, 3],
            captions=["나는 성에 대한 관심이 별다른 변화 없이 유지되고 있다",
                      "나는 이전에 비해 성에 대한 관심이 줄었다",
                      "나는 최근 성에 대한 관심이 상당히 줄었다",
                      "나는 성에 대한 관심을 완전히 잃었다"],
            key="bdi21",
            horizontal=False)

        # Every form must have a submit button.
        submitted = st.form_submit_button("결과보기")
        if submitted:
            form_data = {
                "bdi1": bdi_1,
                "bdi2": bdi_2,
                "bdi3": bdi_3,
                "bdi4": bdi_4,
                "bdi5": bdi_5,
                "bdi6": bdi_6,
                "bdi7": bdi_7,
                "bdi8": bdi_8,
                "bdi9": bdi_9,
                "bdi10": bdi_10,
                "bdi11": bdi_11,
                "bdi12": bdi_12,
                "bdi13": bdi_13,
                "bdi14": bdi_14,
                "bdi15": bdi_15,
                "bdi16": bdi_16,
                "bdi17": bdi_17,
                "bdi18": bdi_18,
                "bdi19": bdi_19,
                "bdi20": bdi_20,
                "bdi21": bdi_21,
            }
            features = np.array([list(form_data.values()) + [sum(form_data.values())]])
            result = scale_xgb.predict(features)[0]
            shap_values = explainer(features, )
            print(shap_values.__dir__())
            print(type(shap_values.base_values))
            print(shap_values.values.shape)
            print(len(list(form_data.keys()) + ["sum"]))
            plot_component = shap.multioutput_decision_plot(base_values=shap_values.base_values.tolist(),
                                                            shap_values=shap_values.values.tolist(),
                                                            row_index=result,
                                                            highlight=[0],
                                                            feature_names=np.array([k for k in form_data.keys()] + ["sum"]),
                                                            show=True)
            print(type(plot_component))
            st_shap(plot_component)
