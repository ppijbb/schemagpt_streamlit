import streamlit as st


st.title('🧬 Dep Peptide App')
with st.sidebar:
    st.page_link("pages/cardio.py",)
    st.page_link("pages/dep_peptide.py",)
    st.page_link("pages/facial.py",)


col1, col2 = st.tabs(["기본 평가", "세부 평가"])

st.session_state.gn3 = 0
with col1:
    st.title("🔎 문진 평가")
    
    with st.form("문진"):
        st.write("영양, 일상 생활에서의 습관에서 심혈관 질환 위험성 평가")
        
        short_general_3 = st.radio(
                label="자신의 건강은 어떻다고 생각하십니까?",
                options=[0, 1, 2, 3],
                index=st.session_state.gn3,
                captions = ["아주 건강하다", "건강하다", "조금 나쁜 편이다", "무척 나쁘다"],
                horizontal=True)
        short_pattern_4 = st.radio(
                label="최근 1개월 동안, 아침까지 피로가 남고, 일에 기력이 솟지 않으셨습니까?",
                options=[0, 1, 2, 3],
                captions = ["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                horizontal=True)
        short_pattern_1 = st.radio(
                label="최근 1개월 동안, 무기력감(모든 일이 귀찮고 하기 싫음)을 느끼셨습니까?",
                options=[0, 1, 2, 3],
                captions = ["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                horizontal=True)        
        short_pattern_5 = st.radio(
                label="평소에 술을 얼마나 자주 마십니까?",
                options=[0, 1, 2, 3],
                captions = ["전혀 마시지 않음", "한 달에 1~4번", "일주일에 2~3번", "일주일에 4번 이상"],
                horizontal=True)
        short_pattern_5_1 = st.radio(
                label="한 번에 술을 얼마나 마십니까?",
                options=[0, 1, 2, 3],
                captions = ["0~2잔", "3~6잔", "7~9잔", "10잔 이상"],
                horizontal=True)
        short_pattern_2 = st.radio(
                label="최근 1개월 동안, 사소한 일에 매우 신경질적이었습니까?",
                options=[0, 1, 2, 3],
                captions = ["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                horizontal=True)
        short_pattern_3 = st.radio(
                label="지난 1주일~1개월 동안 최소 10분 이상 계속 숨이 차거나 심장이 "
                      "약간 빠르게 뛰는 중간 정도의 강도의 스포츠, 운동, 여가 활동을 하셨습니까?\n\n"
                      "예) 빠르게 걷기, 조깅, 골프, 필라테스, 등산-낮은 산, 자전거 타기 등",
                options=[0, 1, 2, 3],
                captions = ["충분히 하고 있다", "어느 정도 하고 있다", "가끔 한다", "전혀 하지 않는다"],
                horizontal=True)
        short_pattern_6 = st.radio(
                label="최근 1개월 동안, 매우 긴장하거나 불안한 상태셨습니까?",
                options=[0, 1, 2, 3],
                captions = ["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                horizontal=True)
        short_pattern_7 = st.radio(
                label="최근 1개월 동안, 남의 시선을 똑바로 볼수 없으셨습니까?",
                options=[0, 1, 2, 3],
                captions = ["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                horizontal=True)
        short_pattern_1 = st.radio(
                label="매일 규칙적으로 운동을 하십니까?",
                options=[0, 1, 2, 3],
                captions = ["충분히 하고 있다", "어느정도 하고 있다", "가끔 한다", "전혀 하지 않는다"],
                horizontal=True)
        short_pattern_2 = st.radio(
                label="매일 보조제를 복용하십니까?",
                options=[0, 1, 2, 3],
                captions = ["먹지 않는다", "가끔 먹는다", "규칙적이지 않지만 자주 먹는다", "매일 먹는다"],
                horizontal=True)
        short_pattern_8 = st.radio(
                label="최근 1개월 동안, 남 앞에 얼굴을 내미는 것이 두려우셨습니까?",
                options=[0, 1, 2, 3],
                captions = ["전혀 없었다", "가끔 느꼈다", "자주 느꼈다", "항상 느꼈다"],
                horizontal=True)
        short_nutrition_1 = st.radio(
                label="견과류는 얼마나 자주 드십니까?\n\n"
                      "예)호두 1.5개, 땅콩 8개, 아몬드 7개 등\n\n"
                      "Vit E(mg) : 13.531(mg) < 정상  (추정)\n\n",
                options=[0, 1, 2, 3],
                captions = ["하루 5회 이상", "하루 3~4회", "하루 1~2회", "일주일 3회 이하"],
                horizontal=True)
        short_nutrition_3 = st.radio(
                label="과일은 얼마나 자주 드십니까?\n\n"
                      "예)사과 1/3개, 귤 1개, 바나나 1/2개, 딸기 7개 등\n\n"
                      "VitB2(mg) : 1.293(mg) < 정상  (추정)\n\n",
                options=[0, 1, 2, 3],
                captions = ["하루 2회 이상", "하루 1~2회", "일주일에 4~6회", "일주일 3회 이하"],
                horizontal=True)
        short_nutrition_6 = st.radio(
                label="우유 및 유제품은 얼마나 자주 드십니까?\n\n"
                      "예) 우유, 두유 1컵(200mL), 슬라이스 치즈 1.5장 등\n\n"
                      "동물성 단백질(g) :24.602(g) < 정상  (추정)\n\n",
                options=[0, 1, 2, 3],
                captions = ["하루 2회 이상", "하루 1~2회", "일주일에 4~6회", "일주일 3회 이하"],
                horizontal=True)
        short_nutrition_9 = st.radio(
                label="육류나 생선류는 일주일에 어느 정도 드십니까?\n\n"
                      "예) 소, 돼지 ,닭고기 등 순살코기 40g(탁구공 크기), 등푸른 생선(소) 1토막 등\n\n"
                      "Protein(g) : 67.220(g) < 정상  (추정)\n\n",
                options=[0, 1, 2, 3],
                captions = ["7회 이상", "4~6회", "2~3회", "1회 이하"],
                horizontal=True)
        

        st.write(short_pattern_5_1.__dir__())

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            form_data = [
                short_general_3, short_pattern_4, short_pattern_1, short_pattern_5, 
                short_pattern_5_1, short_pattern_2, short_pattern_3, short_pattern_6,
                short_pattern_7, short_pattern_1, short_pattern_2, short_pattern_8,
                short_nutrition_1, short_nutrition_3, short_nutrition_6, short_nutrition_9
            ]
            st.write(form_data)
            st.write(sum(form_data))

with col2:
    st.title("🔎 세부 평가")
    with st.form("my_form"):
        st.write("Inside the form")
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)