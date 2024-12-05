from typing import Union, List
import torch
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import VotingClassifier, StackingClassifier, BaggingClassifier
from transformers import pipeline, PreTrainedModel
from transformers.pipelines import Pipeline
from skorch import NeuralNetBinaryClassifier
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline as sklearn_pipeline
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, mean_absolute_error, mean_squared_error, r2_score, roc_auc_score
import pandas as pd
import numpy as np
from torch import nn
from torchvision import models
import sys
sys.setrecursionlimit(10**7)
sys.set_int_max_str_digits(0)


class TabularSelector(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X[0]
        return X[:, :-1]

class TabularModel(BaseEstimator):
    def __init__(self):
        super(TabularModel, self).__init__()
        self._estimator_type = "classifier"
        self.model = ExtraTreesClassifier(
            n_estimators=750,
            class_weight={0: 0.574090, 1: 3.874269},
            criterion="entropy")

    def predict(self, X, y=None):
        X = X[:, :65]
        return self.model.predict(X)

    def predict_proba(self, X, y=None):
        X = X[:, :65]
        return self.model.predict_proba(X)

    def fit(self, X, y=None):
        X = X[:, :65]
        return self.model.fit(X, y)


class ImageSelector(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        data = X[-1]
        data = data.reshape(len(X[-1]), -1)
        return data

class VisionModel(nn.Module):
    def __init__(self):
        super(VisionModel, self).__init__()
        self.model = models.vgg16(weights='VGG16_Weights.DEFAULT')
        self.model.classifier = nn.Sequential(
            nn.Linear(7*7*512, 256),
            nn.ReLU(),
            nn.Linear(256,64),
            nn.ReLU(),
            nn.Linear(64,2),)
        self.model.load_state_dict(torch.load("/home/snubh104/dev/JSH/vgg16_binary_classifier.pth"))

    def forward(self, X):
        logit = self.model(X)
        output = torch.argmax(logit, dim=1).float()
        return output.requires_grad_()


class ImageModel(BaseEstimator):
    def __init__(self,):
        super(ImageModel, self).__init__()
        self._estimator_type = "classifier"
        model = VisionModel()
        self.model = NeuralNetBinaryClassifier(
            module=model,
            max_epochs=4,
            optimizer=torch.optim.Adam)

    def transform(self, X, y=None):
        batch_size = len(X)
        # img = X.reshape(batch_size, 224, 224)
        img = torch.from_numpy(X.astype(np.float32)).unsqueeze(1)
        return img.expand(batch_size, 3, 224, 224)

    def predict(self, X, y=None):
        X = self.transform(X[1])
        # self.model.eval()
        return self.model.predict(X)

    def predict_proba(self, X, y=None):
        X = self.transform(X[1])
        # self.model.eval()
        return self.model.predict_proba(X)

    def fit(self, X, y=None):
        img = X[1]
        X = self.transform(img)
        y = torch.from_numpy(y.astype(np.float32))
        # self.model.train()
        return self.model.fit(X, y)
    
    import numpy as np
    

class CustomVotingClassifier(VotingClassifier):

    def predict(self, X):
        """Predict class labels for X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        maj : array-like of shape (n_samples,)
            Predicted class labels.
        """
        # check_is_fitted(self)
        if self.voting == "soft":
            maj = np.argmax(self.predict_proba(X), axis=1)

        else:  # 'hard' voting
            predictions = self._predict(X).tolist()
            print(predictions)
            for i, prediction in enumerate(predictions): # Text label to index
                predictions[i] = np.array([np.where(self.classes_==yhat)[0] for yhat in prediction])
            maj = np.apply_along_axis(
                lambda x: np.argmax(np.bincount(x, weights=self._weights_not_none)),
                axis=1,
                arr=predictions,
            )

        maj = self.le_.inverse_transform(maj)

        return maj

class LMTextClassifier(BaseEstimator, ClassifierMixin):
    def __init__(
        self, 
        model: Union[str, PreTrainedModel, Pipeline], 
        label_classes: List, 
        device:str, **kwargs
        ):
        """
        Transformers 파이프라인을 Scikit-learn 분류기로 래핑.

        Args:
            model_path: 모델의 경로 또는 이름 (Transformers 파이프라인).
            kwargs: 파이프라인 초기화에 필요한 추가 인자.
        """
        if isinstance(model, Pipeline):
            self.model = model
        else:
            self.model = pipeline(task="text-classification", model=model, device=device, **kwargs)
        self.label_classes = label_classes  # 클래스 레이블 (fit 메서드에서 설정)
        self._is_fitted = True
        self.device = device

    def __sklearn_is_fitted__(self):
        """
        Check fitted status and return a Boolean value.
        """
        return hasattr(self, "_is_fitted") and self._is_fitted
    
    def process_time_wrapper(func: callable):
        import time
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            print(f"Processing time: {time.time() - start}")
            return result
        return wrapper
    
    @torch.inference_mode
    def fit(self, X=None, y=None):
        """
        분류기 학습 (실제 학습은 필요 없음).

        Args:
            X: 학습 데이터 (텍스트 목록).
            y: 학습 레이블 (사용되지 않음).
        """
        # 파이프라인을 사용하여 클래스 레이블 설정
        self.classes_ = self.label_classes
        return self

    @process_time_wrapper
    @torch.inference_mode
    def predict_proba(self, X: List[str]):
        """
        입력 텍스트에 대한 클래스별 확률 예측.

        Args:
            X: 텍스트 목록.

        Returns:
            각 샘플에 대한 클래스별 확률 (numpy 배열).
        """
        result = []
        for label_dict in self.model(X, return_all_scores=True):
            result += [[data['score'] for data in label_dict]]
        return np.array(result)

    @torch.inference_mode
    def predict(self, X: List[str]):
        """
        입력 텍스트에 대한 클래스 예측.

        Args:
            X: 텍스트 목록.

        Returns:
            각 샘플에 대한 예측 클래스 레이블 (numpy 배열).
        """
        probs = self.predict_proba(X)
        return np.array([self.label_classes[np.argmax(prob)] for prob in probs])
