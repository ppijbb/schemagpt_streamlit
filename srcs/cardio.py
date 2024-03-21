import os
import sys
from urllib.parse import unquote, quote
import pickle
import math
import numpy as np
import joblib


def get_heq_data():
    return (pickle.load(open(f"{os.getcwd()}/pages/models/KSModel", 'rb')),
            pickle.load(open(f"{os.getcwd()}/pages/models/VotingEnsembleModel", 'rb')))


def get_scale_data():
    return pickle.load(open(os.getcwd()+"/pages/models/16Model", 'rb'))


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


heq_data = get_heq_data()
scale_data = get_scale_data()

# from joblib import dump
#
# # 모델 저장
# dump(heq_data[0], 'heq1.joblib')
# dump(heq_data[1], 'heq2.joblib')
# dump(scale_data[1], 'scale2.joblib')
# heq_data[1].estimators_[1].save_model("clf.json")  # XGBoost
# heq_data[1].estimators_[1] = None
# print(heq_data[1])
# import pickle
#
# with open("file", "wb") as f:
#     pickle.dump(heq_data[1], f)

def heq(args):
    # args[-1] = args[-1][0]
    # KS 모델 동작에 필요한 데이터 파일에서 읽어옴
    value_data, Voting = heq_data
    knn_model, svm_model, coef, intercept, minmax_scaler, \
        standard_scaler, pca, value_bins, data_mean, branch, directions = value_data
    # with open('python/TabnetClassifierModel','rb') as f:
    #     TNC = pickle.load(f)
    a = coef[0]
    b = coef[1]
    c = coef[2]
    d = intercept
    data_mean = data_mean.tolist()
    branch = tuple(branch)
    cont_branch = list(branch)
    # Web 입력 처리

    processed_values = []
    for index, arg in enumerate(args):
        decoded = arg
        if index > 11:
            value_index = cont_branch[index - 12]
            if float(arg) > value_bins[index - 12][11]:
                value_grade = 12
            else:
                value_grade = np.histogram(float(arg), bins=value_bins[index - 12])[0].argmax() + 1
            args[index] = value_grade
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
    inarg = np.array(args[1:]).astype('int64')
    x = minmax_scaler.transform([inarg])
    num = knn_model.predict(x)
    result = round(knn_model.predict_proba(x)[0][1], 2)
    vx = inarg.reshape(1, -1)
    try:
        # num2 = TNC.predict(vx)
        num2 = num
    except:
        num2 = num
    # print(num, num2, Voting.predict(vx),  # voting
    #       Voting.estimators_[0].predict(vx),  # LightGBM
    #       Voting.estimators_[1].predict(vx),  # XGBoost
    #       Voting.estimators_[2].predict(vx),  # GradientBoost
    #       Voting.estimators_[3].predict(vx))  # CatBoost

    x = [np.append(x, num2)]
    feature = pca.transform(x)
    check = svm_model.predict(feature)
    input_dist = distance(a, feature[0, 0], b, feature[0, 1], c, feature[0, 2], d)
    cluster_result = level(standard_scaler.transform([[input_dist]]))

    if (num2 * check) == 1 and cluster_result == 1:
        risk_lv = '고위험군'
    elif (num2 * check) == 1 and cluster_result == 0:
        risk_lv = '위험군'
    elif (num2 * check) == 0 and cluster_result == 0:
        risk_lv = '일반인'
    elif (num2 * check) == 0 and cluster_result == 1:
        risk_lv = '건강인'
    else:
        risk_lv = '오류'

    return {
        "val_check1": int(num[0]),
        "val_check2": int(num2[0]),
        "risk_lv": risk_lv,
        "other_mean": data_mean,
        "processed_values": processed_values,
        "cont_value_branch": cont_branch,
        "directions": directions
    }


def scale_severity(args):
    # 입력 데이터 처리
    CatC, CatM, coef, intercept, pca, D_mean, SCALER = scale_data
    a = coef[0]
    b = coef[1]
    c = coef[2]
    d = intercept
    inarg = np.array(args[1:]).astype('int64')
    x = [inarg]
    num = CatC.predict(x)
    result = round(CatC.predict_proba(x)[0][1], 2)
    vx = inarg.reshape(1, -1)

    num2 = CatM.predict(vx).ravel()
    score = int(np.sum(inarg))
    if score < 16:
        num2[0] = 0
    elif 15 < score < 21:
        num2[0] = 1
    elif 20 < score < 25:
        num2[0] = 2
    elif score > 24:
        num2[0] = 3
    x = [np.append(x, num)]
    feature = pca.transform(x)
    input_dist = distance(a, feature[0, 0], b, feature[0, 1], c, feature[0, 2], d)
    cluster_result = level(SCALER[num[0]].transform([[input_dist]]))

    if num == 1 and cluster_result == 1:
        risk_lv = '고위험군'
    elif num == 1 and cluster_result == 0:
        risk_lv = '위험군'
    elif num == 0 and cluster_result == 0:
        risk_lv = '일반인'
    elif num == 0 and cluster_result == 1:
        risk_lv = '건강인'
    else:
        risk_lv = '오류'

    return {
        "val_check1": int(num[0]),
        "val_check2": int(num2[0]),
        "risk_score": score,
        "risk_lv": risk_lv,
        "other_mean": D_mean.tolist()
    }
