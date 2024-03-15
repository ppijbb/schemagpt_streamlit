import sys
from urllib.parse import unquote, quote
import pickle
import math
import numpy as np


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


def heq(args):
    args[-1] = args[-1][0]
    # KS 모델 동작에 필요한 데이터 파일에서 읽어옴
    with open('python/KSModel', 'rb') as f:
        knn_model, svm_model, coef, intercept, minmax_scaler, \
            standard_scaler, pca, value_bins, data_mean, branch, directions = pickle.load(f)
    with open('python/VotingEnsembleModel', 'rb') as f:
        Voting = pickle.load(f)
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

    for index, arg in enumerate(args):
        decoded = unquote(arg)
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
            encoded = quote(to_web)
            print(encoded)
        else:
            encoded = quote(decoded)
            print(encoded)
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
    print(num, num2, Voting.predict(vx),  # voting
          Voting.estimators_[0].predict(vx),  # LightGBM
          Voting.estimators_[1].predict(vx),  # XGBoost
          Voting.estimators_[2].predict(vx),  # GradientBoost
          Voting.estimators_[3].predict(vx))  # CatBoost

    x = [np.append(x, num2)]
    feature = pca.transform(x)
    check = svm_model.predict(feature)
    input_dist = distance(a, feature[0, 0], b, feature[0, 1], c, feature[0, 2], d)
    cluster_result = level(standard_scaler.transform([[input_dist]]))

    if (num2 * check) == 1 and cluster_result == 1:
        print(quote('고위험군'))
    elif (num2 * check) == 1 and cluster_result == 0:
        print(quote('위험군'))
    elif (num2 * check) == 0 and cluster_result == 0:
        print(quote('일반인'))
    elif (num2 * check) == 0 and cluster_result == 1:
        print(quote('건강인'))
    else:
        print(quote('오류'))
    print(str(data_mean))
    print(cont_branch)
    print(directions)
    sys.stdout.flush()


def scale_severity(args):
    with open('python/16Model', 'rb') as f:
        CatC, CatM, coef, intercept, pca, D_mean, SCALER = pickle.load(f)
        a = coef[0]
        b = coef[1]
        c = coef[2]
        d = intercept
        data_mean = D_mean.tolist()

    for index, arg in enumerate(args):
        decoded = unquote(arg)
        encoded = quote(decoded)
        print(encoded)

    # 입력 데이터 처리
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
    print(num[0], int(num2[0]), score)  # CatBoost

    x = [np.append(x, num)]
    feature = pca.transform(x)
    input_dist = distance(a, feature[0, 0], b, feature[0, 1], c, feature[0, 2], d)
    cluster_result = level(SCALER[num[0]].transform([[input_dist]]))

    if num == 1 and cluster_result == 1:
        print(quote('고위험군'))
    elif num == 1 and cluster_result == 0:
        print(quote('위험군'))
    elif num == 0 and cluster_result == 0:
        print(quote('일반인'))
    elif num == 0 and cluster_result == 1:
        print(quote('건강인'))
    else:
        print(quote('오류'))
    print(str(data_mean))
    sys.stdout.flush()