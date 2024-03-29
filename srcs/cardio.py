import os
import sys
import math
import numpy as np
import pandas as pd
import streamlit as st
from srcs.st_cache import get_heq_data, get_scale_data
import plotly.graph_objects as go
from plotly.subplots import make_subplots


heq_data = get_heq_data()
scale_data = get_scale_data()


def distance(a, x, b, y, c, z, d):
    up = abs(a * x + b * y + c * z + d)
    down = math.sqrt(a ** 2 + b ** 2 + c ** 2)
    return up / down


def level(x):
    if x > 0:
        result = 1
    else:
        result = 0
    return result


def make_grade(indexer, x):
    if x < 0:
        indexer = (np.array(indexer) * -1 + 13).tolist()
        indexer.sort()
        x += 13
        if indexer[0] > x:
            return " 건강", x, indexer
        elif indexer[0] <= x and indexer[1] > x:
            return " 일반", x, indexer
        elif indexer[1] <= x and indexer[2] > x:
            return " 주의", x, indexer
        elif indexer[2] <= x:
            return " 관심필요", x, indexer
    else:
        if indexer[0] > x:
            return " 건강"
        elif indexer[0] <= x and indexer[1] > x:
            return " 일반"
        elif indexer[1] <= x and indexer[2] > x:
            return " 주의"
        elif indexer[2] <= x:
            return " 관심필요"


def make_gauge(user_level, risk_lv):
    return go.Indicator(
            mode="gauge+number", # "gauge+number+delta"
            value=3-np.argmax(user_level)+0.5,
            domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]},
            title={'text': f"분석 결과", 'font': {'size': 24}},
            # delta={'reference': 4, 'increasing': {'color': "RebeccaPurple"}},
            number={"suffix": f"단계: {risk_lv}", "valueformat": ".0", 'font': {'size': 30, 'color': 'black'}},
            gauge={
                'axis': {
                    'range': [0, 4],
                    'tickvals': [0, 1, 2, 3, 4],
                    'ticktext': ["건강", "일반", "주의", "위험", "고위험"],
                    'tickwidth': 1,
                    'tickcolor': "darkblue",
                    'tickformatstops': [
                        {'templateitemname': '건강', 'value': '건강'},
                        {'templateitemname': '일반', 'value': '일반'},
                        {'templateitemname': '위험', 'value': '위험'},
                        {'templateitemname': '고위험', 'value': '고위험'},
                    ]
                },
                'bar': {
                    'color': "darkblue",
                    'thickness': 0,
                    'line': {
                        'width': 0,
                    }
                },
                # 'bgcolor': "white",
                'borderwidth': 1,
                'bordercolor': "gray",
                'steps': [
                    {'name': '건강',   'range': [0, 1], 'color': 'royalblue', },
                    {'name': '일반',   'range': [1, 2], 'color': 'lightcyan', },
                    {'name': '위험',   'range': [2, 3], 'color': 'lightsalmon', },
                    {'name': '고위험', 'range': [3, 4], 'color': 'tomato', }],
                'threshold': {
                    'thickness': 0.7,
                    'value': (3 - np.argmax(user_level)) + 0.5,
                    'line': {
                        'color': 'black',
                        'width': 4
                    }
                }
            })


def heq(args, st_layout):
    # args[-1] = args[-1][0]
    # KS 모델 동작에 필요한 데이터 파일에서 읽어옴
    value_data, Voting = heq_data
    knn_model, svm_model, coef, intercept, minmax_scaler, \
        standard_scaler, pca, value_bins, data_mean, branch, directions = value_data

    a = coef[0]
    b = coef[1]
    c = coef[2]
    d = intercept
    data_mean = data_mean.tolist()
    branch = tuple(branch)
    cont_branch = list(branch)
    # Web 입력 처리

    processed_values = []
    for index, (key, value) in enumerate(args.items()):
        decoded = value
        if index > 11:
            value_index = cont_branch[index - 12]
            if float(value) > value_bins[index - 12][11]:
                value_grade = 12
            else:
                value_grade = np.histogram(float(value), bins=value_bins[index - 12])[0].argmax() + 1
            args[key] = int(value_grade)
            to_web = '%d 단계' % value_grade
            if directions[index - 1] > 0:
                to_web += make_grade(value_index, value_grade)
            else:
                mg_text, mg_value, mg_indexer = make_grade(value_index, -1 * value_grade)
                to_web += mg_text
                cont_branch[index - 12] = mg_indexer
            encoded = to_web
        else:
            encoded = decoded

        processed_values += [encoded]
    # 입력 데이터 처리
    inarg = np.array(list(args.values())[1:]).astype('int64')
    x = minmax_scaler.transform([inarg])
    num = knn_model.predict(x)
    result = round(knn_model.predict_proba(x)[0][1], 2)
    vx = inarg.reshape(1, -1)
    try:
        # num2 = TNC.predict(vx)
        num2 = num
    except:
        num2 = num
    print(num, num2,
          Voting.predict(vx),  # voting
          Voting.estimators_[0].predict(vx),  # LightGBM
          Voting.estimators_[1].predict(vx),  # XGBoost
          Voting.estimators_[2].predict(vx),  # GradientBoost
          Voting.estimators_[3].predict(vx))  # CatBoost

    x = [np.append(x, num2)]
    feature = pca.transform(x)
    check = svm_model.predict(feature)
    input_dist = distance(a, feature[0, 0], b, feature[0, 1], c, feature[0, 2], d)
    cluster_result = level(standard_scaler.transform([[input_dist]]))
    user_level = [0, 0, 0, 0]
    if (num2 * check) == 1 and cluster_result == 1:
        user_level[0] = 0.1
        risk_lv = '고위험군'
    elif (num2 * check) == 1 and cluster_result == 0:
        user_level[1] = 0.1
        risk_lv = '위험군'
    elif (num2 * check) == 0 and cluster_result == 0:
        user_level[2] = 0.1
        risk_lv = '일반인'
    elif (num2 * check) == 0 and cluster_result == 1:
        user_level[3] = 0.1
        risk_lv = '건강인'
    else:
        risk_lv = '오류'
    result = {
        "val_check1": int(num[0]),
        "val_check2": int(num2[0]),
        "risk_lv": risk_lv,
        "other_mean": dict(zip(list(args.keys())[1:], data_mean)),
        "processed_values": processed_values,
        "cont_value_branch": cont_branch,
        "directions": directions
    }

    gen_data = {k.split("_")[1]: float(v) for k, v in args.items() if k.startswith("g")}
    gen_mean_data = {k.split("_")[1]: float(v) for k, v in result["other_mean"].items() if k.startswith("g")}
    nut_data = {k.split("_")[1]: float(v) for k, v in args.items() if k.startswith("n")}
    nut_mean_data = {k.split("_")[1]: float(v) for k, v in result["other_mean"].items() if k.startswith("n")}
    blo_data = {k.split("_")[1]: float(v) for k, v in args.items() if k.startswith("b")}
    blo_mean_data = {k.split("_")[1]: float(v) for k, v in result["other_mean"].items() if k.startswith("b")}
    pat_data = {k.split("_")[1]: float(v) for k, v in args.items() if k.startswith("p")}
    pat_mean_data = {k.split("_")[1]: float(v) for k, v in result["other_mean"].items() if k.startswith("p")}

    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.5, 0.5],
        row_heights=[0.5, 0.5],
        vertical_spacing=0.1,
        horizontal_spacing=0.4,
        subplot_titles=("영양 분석", "혈액 분석", "기본 분석", "패턴 분석"),
        # shared_yaxes=True
        specs=[[{"type": "polar", "t": 0.1}, {"type": "polar", "t": 0.1}],
               [{"type": "bar", }, {"type": "bar", }]],
        )
    for draw_data, title in zip([nut_data, nut_mean_data],
                                ["사용자 데이터", "정상군 평균"],):
        fig.add_traces(data=[
            go.Scatterpolargl(
                r=list(draw_data.values()),
                showlegend=False,
                theta=list(draw_data.keys()),
                fill="toself",
                name=title
            )],
            rows=1, cols=1
        )
    for draw_data, title in zip([blo_data, blo_mean_data],
                                ["사용자 데이터", "정상군 평균"],):
        fig.add_traces(data=[
            go.Scatterpolargl(
                r=list(draw_data.values()),
                showlegend=False,
                theta=list(draw_data.keys()),
                fill="toself",
                name=title
            )],
            rows=1, cols=2
        )

    for draw_data, title in zip([gen_data, gen_mean_data],
                                ["사용자 데이터", "정상군 평균"]):
        fig.add_traces(
            data=[go.Bar(
                y=list(draw_data.keys()),
                x=list(draw_data.values()),
                orientation='h',
                showlegend=False,
                name=title
            )],
            rows=2, cols=1
        )

    for draw_data, title in zip([pat_data, pat_mean_data],
                                ["사용자 데이터", "정상군 평균"]):
        fig.add_traces(
            data=[go.Bar(
                y=list(draw_data.keys()),
                x=list(draw_data.values()),
                orientation='h',
                showlegend=False,
                name=title
            )],
            rows=2, cols=2
        )

    pie = go.Figure(make_gauge(user_level, risk_lv))
    pie.update_layout(font={'color': "darkblue", 'family': "Arial"},
                      margin={
                          "l": 50, "r": 50, "t": 0, "b": 0, "pad": 0
                      })
    # st.write(risk_lv)
    fig.update_layout(margin={
        "l": 50, "r": 50, "t": 0, "b": 0, "pad": 0
    })
    with st_layout.container(border=True):
        st.plotly_chart(pie, theme="streamlit", use_container_width=True)
    with st_layout.container(border=True):
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    # st_layout.write(args)
    # st_layout.write(result)
    return result


def scale_severity(args, st_layout):
    # 입력 데이터 처리
    CatC, CatM, coef, intercept, pca, D_mean, SCALER = scale_data
    a = coef[0]
    b = coef[1]
    c = coef[2]
    d = intercept

    values = list(args.values())

    inarg = np.array(values[1:]).astype('int64')
    x = [inarg]
    num = CatC.predict(x)
    result = round(CatC.predict_proba(x)[0][1], 2)
    vx = inarg.reshape(1, -1)

    num2 = CatM.predict(vx).ravel()
    user_level = [0, 0, 0, 0]
    score = int(np.sum(inarg))
    if score < 16:
        user_level[3] = 0.1
        num2[0] = 0
        risk_lv = '건강인'
    elif 15 < score < 21:
        user_level[2] = 0.1
        num2[0] = 1
        risk_lv = '일반인'
    elif 20 < score < 25:
        num2[0] = 2
        user_level[1] = 0.1
        risk_lv = '위험군'
    elif score > 24:
        user_level[0] = 0.1
        num2[0] = 3
        risk_lv = '고위험군'
    x = [np.append(x, num)]
    feature = pca.transform(x)
    input_dist = distance(a, feature[0, 0], b, feature[0, 1], c, feature[0, 2], d)
    cluster_result = level(SCALER[num[0]].transform([[input_dist]]))
    
    if (num[0] == 1 and cluster_result == 1):
        ai_risk_lv = '고위험군'
    elif (num[0] == 1 and cluster_result == 0):
        ai_risk_lv = '위험군'
    elif (num[0] == 0 and cluster_result == 0):
        ai_risk_lv = '일반인'
    elif (num[0] == 0 and cluster_result == 1):
        ai_risk_lv = '건강인'
    else:
        ai_risk_lv = '오류'

    result = {
        "val_check1": int(num[0]),
        "val_check2": int(num2[0]),
        "risk_score": score,
        "risk_lv": risk_lv,
        "other_mean": dict(zip([k.split("_")[1] for k in args.keys() if k != "user"], D_mean))
    }
    label = [f"총점",]
    generals = ["일반", "자신의 건강", "규칙적 운동", "보조제 복용",]
    nutritions = ["영양", "Vit E", "Vit B2", "동물성 단백질", "Protein",]
    patterns = ["패턴", "피로", "무기력", "음주 횟수", "음주량", "신경질", "중강도 신체활동", "불안", "시선 어려움", "대면 어려움"]
    gen_score = [args[f'g_{g}'] for g in generals[1:]]
    nut_score = [args[f'n_{n}'] for n in nutritions[1:]]
    pat_score = [args[f'p_{p}'] for p in patterns[1:]]
    fig = go.Figure(
        go.Sunburst(
            name="결과",
            labels=label + generals + nutritions + patterns,
            parents=[""] +
                    label + ["일반"] * len(generals[1:]) +
                    label + ["영양"] * len(nutritions[1:]) +
                    label + ["패턴"] * len(patterns[1:]),
            values=[score,] +
                   [sum(gen_score)] + gen_score +
                   [sum(nut_score)] + nut_score +
                   [sum(pat_score)] + pat_score,
            branchvalues='total',
            insidetextorientation='radial'
        ),
    )
    polar = go.Figure()
    for draw_data, title in zip([{k.split("_")[1] : v for k, v in args.items() if k != "user"}, result["other_mean"]],
                                ["사용자 데이터", "정상군 평균"],):
        polar.add_traces(data=[
            go.Scatterpolargl(
                r=list(draw_data.values()),
                showlegend=False,
                theta=list(draw_data.keys()),
                fill="toself",
                name=title
            )],
        )
    # fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    pie = go.Figure(make_gauge(user_level, risk_lv))
    pie.update_layout(font={'color': "darkblue", 'family': "Arial"},
                      margin={"l": 0, "r": 0, "t": 0, "b": 0,})
    with st_layout.container(border=True):
        st.plotly_chart(pie, theme="streamlit", use_container_width=True,)
    with st_layout.container(border=True):
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, height=400)
    with st_layout.container(border=True):
        st.plotly_chart(polar, theme="streamlit", use_container_width=True, height=400)
    
    return result
