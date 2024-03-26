import os
import sys
import streamlit as st
from srcs.cardio import heq, scale_severity
import streamlit.components.v1 as components


@st.cache_resource
def add_static_js():
    js_dir = f"{os.getcwd()}/static/css"
    js_file_list = [dir_ for dir_ in os.listdir(js_dir) if dir_.endswith("2.css")]

    js_data = ""

    for js in js_file_list:
        with open(f"{js_dir}/{js}", "r") as f:
            js_data += f'<style>\n{f.read()}\n</style>\n'
    return js_data


if __name__ == "__main__":
    st.title('🫀 Cardio')
    with st.sidebar:
        st.page_link("pages/cardio.py", )
        st.page_link("pages/dep_peptide.py", )
        st.page_link("pages/facial.py", )
    form_con = st.expander(label="측정하기", expanded=True)
    result_con = st.expander(label="점수보기", expanded=False)
    with form_con:
        tab1, tab2, tab3 = st.tabs(["기본 평가", "세부 평가", "테스트"])

        st.session_state.gn3 = 0
        with tab1:
            st.title("🔎 문진 평가")

            with st.form("문진"):
                st.write("영양, 일상 생활에서의 습관에서 심혈관 질환 위험성 평가")

                short_general_3 = st.radio(
                        label="자신의 건강은 어떻다고 생각하십니까?",
                        options=[0, 1, 2, 3],
                        index=st.session_state.gn3,
                        captions=["아주 건강하다", "건강하다", "조금 나쁜 편이다", "무척 나쁘다"],
                        horizontal=True)
                short_pattern_4 = st.radio(
                        label="최근 1개월 동안, 아침까지 피로가 남고, 일에 기력이 솟지 않으셨습니까?",
                        options=[0, 1, 2, 3],
                        captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                        horizontal=True)
                short_pattern_1 = st.radio(
                        label="최근 1개월 동안, 무기력감(모든 일이 귀찮고 하기 싫음)을 느끼셨습니까?",
                        options=[0, 1, 2, 3],
                        captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                        horizontal=True)
                short_pattern_5 = st.radio(
                        label="평소에 술을 얼마나 자주 마십니까?",
                        options=[0, 1, 2, 3],
                        captions=["전혀 마시지 않음", "한 달에 1~4번", "일주일에 2~3번", "일주일에 4번 이상"],
                        horizontal=True)
                short_pattern_5_1 = st.radio(
                        label="한 번에 술을 얼마나 마십니까?",
                        options=[0, 1, 2, 3],
                        captions=["0~2잔", "3~6잔", "7~9잔", "10잔 이상"],
                        horizontal=True)
                short_pattern_2 = st.radio(
                        label="최근 1개월 동안, 사소한 일에 매우 신경질적이었습니까?",
                        options=[0, 1, 2, 3],
                        captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                        horizontal=True)
                short_pattern_3 = st.radio(
                        label="지난 1주일~1개월 동안 최소 10분 이상 계속 숨이 차거나 심장이 "
                              "약간 빠르게 뛰는 중간 정도의 강도의 스포츠, 운동, 여가 활동을 하셨습니까?\n\n"
                              "예) 빠르게 걷기, 조깅, 골프, 필라테스, 등산-낮은 산, 자전거 타기 등",
                        options=[0, 1, 2, 3],
                        captions=["충분히 하고 있다", "어느 정도 하고 있다", "가끔 한다", "전혀 하지 않는다"],
                        horizontal=True)
                short_pattern_6 = st.radio(
                        label="최근 1개월 동안, 매우 긴장하거나 불안한 상태셨습니까?",
                        options=[0, 1, 2, 3],
                        captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                        horizontal=True)
                short_pattern_7 = st.radio(
                        label="최근 1개월 동안, 남의 시선을 똑바로 볼수 없으셨습니까?",
                        options=[0, 1, 2, 3],
                        captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                        horizontal=True)
                short_general_1 = st.radio(
                        label="매일 규칙적으로 운동을 하십니까?",
                        options=[0, 1, 2, 3],
                        captions=["충분히 하고 있다", "어느정도 하고 있다", "가끔 한다", "전혀 하지 않는다"],
                        horizontal=True)
                short_general_2 = st.radio(
                        label="매일 보조제를 복용하십니까?",
                        options=[0, 1, 2, 3],
                        captions=["먹지 않는다", "가끔 먹는다", "규칙적이지 않지만 자주 먹는다", "매일 먹는다"],
                        horizontal=True)
                short_pattern_8 = st.radio(
                        label="최근 1개월 동안, 남 앞에 얼굴을 내미는 것이 두려우셨습니까?",
                        options=[0, 1, 2, 3],
                        captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                        horizontal=True)
                short_nutrition_1 = st.radio(
                        label="견과류는 얼마나 자주 드십니까?\n\n"
                              "예)호두 1.5개, 땅콩 8개, 아몬드 7개 등\n\n"
                              "Vit E(mg) : 13.531(mg) < 정상  (추정)\n\n",
                        options=[0, 1, 2, 3],
                        captions=["하루 5회 이상", "하루 3~4회", "하루 1~2회", "일주일 3회 이하"],
                        horizontal=True)
                short_nutrition_3 = st.radio(
                        label="과일은 얼마나 자주 드십니까?\n\n"
                              "예)사과 1/3개, 귤 1개, 바나나 1/2개, 딸기 7개 등\n\n"
                              "VitB2(mg) : 1.293(mg) < 정상  (추정)\n\n",
                        options=[0, 1, 2, 3],
                        captions=["하루 2회 이상", "하루 1~2회", "일주일에 4~6회", "일주일 3회 이하"],
                        horizontal=True)
                short_nutrition_6 = st.radio(
                        label="우유 및 유제품은 얼마나 자주 드십니까?\n\n"
                              "예) 우유, 두유 1컵(200mL), 슬라이스 치즈 1.5장 등\n\n"
                              "동물성 단백질(g) :24.602(g) < 정상  (추정)\n\n",
                        options=[0, 1, 2, 3],
                        captions=["하루 2회 이상", "하루 1~2회", "일주일에 4~6회", "일주일 3회 이하"],
                        horizontal=True)
                short_nutrition_9 = st.radio(
                        label="육류나 생선류는 일주일에 어느 정도 드십니까?\n\n"
                              "예) 소, 돼지 ,닭고기 등 순살코기 40g(탁구공 크기), 등푸른 생선(소) 1토막 등\n\n"
                              "Protein(g) : 67.220(g) < 정상  (추정)\n\n",
                        options=[0, 1, 2, 3],
                        captions=["7회 이상", "4~6회", "2~3회", "1회 이하"],
                        horizontal=True)

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                if submitted:
                    del tab1
                    form_data = {
                        "user": "test",
                        "g_자신의 건강": short_general_3,
                        "p_피로": short_pattern_4,
                        "p_무기력": short_pattern_1,
                        "p_음주 횟수": short_pattern_5,
                        "p_음주량": short_pattern_5_1,
                        "p_신경질": short_pattern_2,
                        "p_중강도 신체활동": short_pattern_3,
                        "p_불안": short_pattern_6,
                        "p_시선 어려움": short_pattern_7,
                        "g_규칙적 운동": short_general_1,
                        "g_보조제 복용": short_general_2,
                        "p_대면 어려움": short_pattern_8,
                        "n_Vit E": short_nutrition_1,
                        "n_Vit B2": short_nutrition_3,
                        "n_동물성 단백질": short_nutrition_6,
                        "n_Protein": short_nutrition_9
                    }
                    with result_con:
                        _, con, _ = st.columns([0.1, 0.8, 0.1])
                        scale_severity(form_data, con)
        labels = ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parents = ["",    "Eve",  "Eve", "Seth", "Seth", "Eve",   "Eve",  "Awan",  "Eve"],
        values = [10,        14,      12,    10,      2,     6,       6,       4,     4],
        with tab2:
            st.title("🔎 세부 평가")
            with st.form("세부 평가지"):
                st.write("Inside the form")
                row1 = st.columns([1, 1, 1, 1])
                with row1[0]:
                    st.write("일반 정보")
                    general_1 = st.radio(
                            label="★ 규칙적 운동 여부",
                            options=[0, 1, 2, 3],
                            captions=["충분히 하고 있다", "어느정도 하고 있다", "가끔 한다", "전혀 하지 않는다"],
                            horizontal=True)
                    general_2 = st.radio(
                            label="★ 보조제 복용 유무 ",
                            options=[0, 1, 2, 3],
                            captions=["먹지 않는다", "가끔 먹는다", "규칙적이지 않지만 자주 먹는다", "매일 먹는다"],
                            horizontal=True)
                    general_6 = st.radio(
                            label="★ 자신의 건강 ",
                            options=[0, 1, 2, 3],
                            captions=["무척 나쁘다", "조금 나쁘다", "건강한 편이다", "매우 건강하다"],
                            horizontal=True)
                    general_12 = st.slider(
                            label="수축기 혈압 2차\n\n"
                                  "수축기 120, 140이하 고혈압 전단계",
                            min_value=70, max_value=190, value=110)
                    general_13 = st.slider(
                            label="이완기 혈압 1차\n\n"
                                  "이완기 80, 90이하 고혈압 전단계",
                            min_value=20, max_value=110, value=60)
                    general_14 = st.slider(
                            label="수축기 혈압 1차\n\n"
                                  "수축기 120, 140이하 고혈압 전단계",
                            min_value=70, max_value=190, value=110)
                    general_24 = st.slider(
                            label="비만진단 - 복부지방률\n\n"
                                  "표준범위 남자/여자: 0.75-0.85/0.7-0.8\n\n"
                                  "비만 0.9/0.85 이상\n\n",
                            min_value=0.2, max_value=1.0, value=0.3, step=0.001)
                with row1[1]:
                    st.write("혈액 정보")
                    blood_16 = st.slider(
                            label="HDL 콜레스테롤\n\n"
                                  "참고치\n\n"
                                  "-정상 : >40 mg/dL",
                            min_value=20.0, max_value=120.0, value=50.0, step=0.001)
                    blood_17 = st.slider(
                            label="LDL 콜레스테롤\n\n"
                                  "참고치\n\n"
                                  "-정상 : < 130 mg/dL",
                            min_value=20.0, max_value=250.0, value=50.0, step=0.001)
                    blood_18 = st.slider(
                            label="LDL-c 콜레스테롤\n\n"
                                  "참고치\n\n"
                                  "-정상 : < 130 mg/dL",
                            min_value=20.0, max_value=250.0, value=50.0, step=0.001)
                    blood_19 = st.slider(
                            label="적혈구용적치(Hct)\n\n"
                                  "참고치\n\n"
                                  "-정상(남자) : 39-50 %\n\n"
                                  "-정상(여자) : 36-47 %",
                            min_value=20.0, max_value=70.0, value=30.0, step=0.001)
                    blood_20 = st.slider(
                            label="Cholesterol\n\n"
                                  "참고치\n\n"
                                  "-정상 : 200 mg/dL 미만",
                            min_value=20.0, max_value=400.0, value=200.0, step=0.001)
                    blood_23 = st.slider(
                            label="헤모글로빈(HGB)\n\n"
                                  "참고치\n\n"
                                  "-정상(남자) : 13.0-17.1 g/dL\n\n"
                                  "-정상(여자) : 11.2-15.0 g/dL",
                            min_value=5.0, max_value=25.0, value=11.0, step=0.001)
                    blood_26 = st.slider(
                            label="적혈구수(RBC)\n\n"
                                  "참고치\n\n"
                                  "-정상(남자) : 440-560 만개/mm3\n\n"
                                  " -정상(여자) : 400-520 만개/mm3",
                            min_value=2.0, max_value=7.0, value=4.0, step=0.001)
                    blood_27 = st.slider(
                            label="단핵구(MONO)\n\n"
                                  "참고치\n\n"
                                  "-정상 : 0-9 %",
                            min_value=0.2, max_value=12.0, value=10.0, step=0.001)
                    blood_33 = st.slider(
                            label="백혈구수(WBC)\n\n"
                                  "참고치\n\n"
                                  "-정상 : 4.5-9.1 천개/mm3",
                            min_value=0.0, max_value=12.0, value=10.0, step=0.001)
                with row1[2]:
                    st.write("영양 정보")
                    nutrition_15 = st.slider(
                            label="★ Vit E(mg)\n\n"
                                  "참고치\n\n"
                                  "-정상(추정) : 13.531(mg) 이상 ",
                            min_value=0.0, max_value=40.0, value=10.0, step=0.001)
                    nutrition_21 = st.slider(
                            label="회분(g)\n\n"
                                  "참고치\n\n"
                                  "-정상(추정) : 17.334(g) 이상 ",
                            min_value=0.0, max_value=40.0, value=10.0, step=0.001)
                    nutrition_22 = st.slider(
                            label="식물성 Fe(mg)\n\n"
                                  "참고치\n\n"
                                  "-정상(추정) : 14.310(mg) 미만 ",
                            min_value=0.0, max_value=40.0, value=10.0, step=0.001)
                    nutrition_25 = st.slider(
                            label="Mo(ug)\n\n"
                                  "참고치\n\n"
                                  "-정상(추정) : 2.572(ug) 이상 ",
                            min_value=0.0, max_value=13.0, value=5.0, step=0.001)
                    nutrition_28 = st.slider(
                            label="★ VitB2(mg)\n\n"
                                  "참고치\n\n"
                                  "-정상(추정) : 1.293(mg) 이상 ",
                            min_value=0.0, max_value=5.0, value=3.0, step=0.001)
                    nutrition_29 = st.slider(
                            label="★ 동물성 단백질(g)\n\n"
                                  "참고치\n\n"
                                  "-정상(추정) : 24.602(g) 이상 ",
                            min_value=0.0, max_value=110.0, value=30.0, step=0.001)
                    nutrition_30 = st.slider(
                            label="Cu(ug)\n\n"
                                  "참고치\n\n"
                                  "-정상(추정) : 688.324(ug) 미만 ",
                            min_value=50.0, max_value=2000.0, value=40.0, step=0.001)
                    nutrition_31 = st.slider(
                            label="Vit C(mg)\n\n"
                                  "참고치\n\n"
                                  "-정상(추정) : 74.102(mg) 미만 ",
                            min_value=50.0, max_value=330.0, value=70.0, step=0.001)
                    nutrition_32 = st.slider(
                            label="★ Protein(g)\n\n"
                                  "참고치\n\n"
                                  "-정상(추정) : 5.332(g) 이상 ",
                            min_value=0.0, max_value=150.0, value=70.0, step=0.001)
                with row1[3]:
                    st.write("생활 정보")
                    pattern_3 = st.radio(
                            label="★ 스트레스 무기력감",
                            options=[0, 1, 2, 3],
                            captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                            horizontal=True)
                    pattern_4 = st.radio(
                            label="★ 스트레스 신경질",
                            options=[0, 1, 2, 3],
                            captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                            horizontal=True)
                    pattern_5 = st.radio(
                            label="★ 여가_중강도 신체활동 여부",
                            options=[0, 1, ],
                            captions=["한다", "안한다",],
                            horizontal=True)
                    pattern_7 = st.radio(
                            label="★ 스트레스 피로",
                            options=[0, 1, 2, 3],
                            captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                            horizontal=True)
                    pattern_8 = st.radio(
                            label="★ 음주 여부 및 음주량",
                            options=[0, 1, 2, 3, 4],
                            captions=["전혀 없음", "한 달에 1번", "한 달에 2~4번", "일주일에 2~3번", "일주일에 4번 이상"],
                            horizontal=True)
                    pattern_9 = st.radio(
                            label="★ 스트레스 긴장,불안",
                            options=[0, 1, 2, 3],
                            captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                            horizontal=True)
                    pattern_10 = st.radio(
                            label="★ 스트레스 대면어려움",
                            options=[0, 1, 2, 3],
                            captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                            horizontal=True)
                    pattern_11 = st.radio(
                            label="★ 스트레스_시선어려움",
                            options=[0, 1, 2, 3],
                            captions=["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                            horizontal=True)

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                if submitted:
                    form_data = {
                        "user": "test",
                        "g_규칙적 운동": general_1, "g_보조제 복용": general_2, "p_무기력": pattern_3, "p_산경질": pattern_4,
                        "p_중강도 신체활동": pattern_5, "g_자신의 건강": general_6, "p_피로": pattern_7, "p_음주": pattern_8,
                        "p_긴장/불안": pattern_9, "p_대면 어려움": pattern_10, "p_시선 어려움": pattern_11,
                        "g_수축기 혈압 2차": general_12, "g_이완기 혈압 1차": general_13, "g_수축기 혈압 1차": general_14,
                        "n_Vit E": nutrition_15, "b_HDL": blood_16, "b_LDL": blood_17,
                        "b_LDL-c": blood_18, "b_적혈구용적치": blood_19, "b_콜레스테롤": blood_20, "n_회분": nutrition_21,
                        "n_철분(식물성)": nutrition_22, "b_헤모글로빈": blood_23, "g_복부지방률": general_24, "n_Mo": nutrition_25,
                        "b_적혈구수": blood_26, "b_단핵구": blood_27, "n_Vit B2": nutrition_28, "n_동물성 단백질": nutrition_29,
                        "n_Cu": nutrition_30, "n_Vit C": nutrition_31, "n_Protein": nutrition_32, "b_백혈구수": blood_33
                    }
                    with result_con:
                        _, con, _ = st.columns([0.1, 0.8, 0.1])
                        heq(form_data, con)

        with tab3:
            with (open(os.getcwd()+"/static/views/index.html", "r") as f):
                html_obj = f'{f.read()}'
                # html_obj = html_obj.replace("text/javascript", "applcation/javascript")
                # html_obj = html_obj.replace("text/css", "text/html")
                # st.markdown(add_static_js(), unsafe_allow_html=True)
                main_component = components.html(html_obj, scrolling=True, height=700)
