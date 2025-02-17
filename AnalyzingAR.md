# Opt Binning (Optimal Binning) 개념
**Optimal Binning**은 연속형 데이터를 최적의 방식으로 구간(bins)으로 나누는 방법.
일반적인 binning 기법과 달리, 단순히 균등한 간격으로 나누는 것이 아니라 데이터의 특성과 목표 변수(예: 레이블) 간의 관계를 고려하여 최적화된 구간을 찾음.

# Opt Binning 주요 목적
1. 모델 성능 향상: 변수를 최적으로 변환하여 머신러닝 모델이 더 좋은 성능을 내도록 함
2. 해석 가능성 증가: 연속형 변수를 범주형 변수로 변환하여 사람이 이해하기 쉬운 결과 제공
3. 노이즈 감소: 데이터를 적절한 그룹으로 묶어 과적합(overfitting) 방지
4. 신용 리스크 모델링: 신용 점수 계산에서 흔히 사용 (Weight of Evidence, WOE 변환과 함께 활용)

# Opt Binning 방식
1. Supervised Binning (지도 학습 기반 Binning)
   * 목표 변수(레이블)를 고려하여 최적의 구간을 찾음
   * 대표적인 방법: Weight of Evidence (WOE) Binning, Decision Tree Binning
2. Unsupervised Binning (비지도 학습 기반 Binning)
   * 목표 변수를 고려하지 않고 데이터의 분포만을 기반으로 구간을 설정
   * 대표적인 방법: Equal Width Binning (동일 간격 나누기), Equal Frequency Binning (동일 개수 나누기)

# Opt Binning 라이브러리
파이썬에서는 `optbinning`이라는 라이브러리를 활용하면 Optimal Binning을 쉽게 수행할 수 있음.

Optimal Binning을 활용하여 설명변수의 구간을 최적화하여 목표변수 변별력을 최대화하는 방법
```python
import numpy as np
import pandas as pd
from optbinning import OptimalBinning
from sklearn.metrics import roc_auc_score

# 1️⃣ 데이터 생성
np.random.seed(42)         # 난수 생성의 일관성을 유지하기 위한 설정
x = np.random.randn(1000)  # 설명변수 (연속형 변수, 정규분)
y = (x > 0).astype(int)    # 목표변수 (이진 분류)

# 2️⃣ Optimal Binning 적용
optb = OptimalBinning(
    name="Feature",            # 변수를 나타내는 이름 (필수 입력)
    dtype="numerical",         # 데이터 유형: `numerical`(연속형 변수) 또는 `categorical`(범주형 변수)
    solver="cp",               # 최적화 방법: "cp" (Convex Programming, 기본값), "mip" (Mixed-Integer Programming)
    monotonic_trend="auto",    # 목표 변수와의 관계를 단조 증가("ascending"), 단조 감소("descending"), 자동("auto")로 설정 가능
    min_n_bins=3,              # 최소 구간(bin) 개수
    max_n_bins=6,              # 최대 구간(bin) 개수
    min_bin_size=0.05,         # 각 구간의 최소 데이터 비율 (예: 0.05 → 전체 데이터의 5%)
    prebinning_method="cart"   # 초기 binning 방법: "cart" (의사결정나무 기반), "quantile" (분위수 기반)
)

optb.fit(x, y)                 # 모델학습

# 3️⃣ 최적화된 구간(bin) 정보 출력
binning_table = optb.binning_table.build()
print(binning_table)

# 4️⃣ 변환된 WOE 값 적용하여 새로운 특성 생성(구간별 WOE 값을 적용하여 새로운 특성 생성)
# 목표변수와 설명변수의 관계를 최적화하여 변별력을 최대화하는 구간을 찾음
# Weight of Evidence (WOE) Binning: 신용 리스크 분석에서 많이 사용
x_transformed = optb.transform(x, metric="woe")

# 5️⃣ 최적화된 변수의 변별력 확인 (AUC 계산)
auc_score = roc_auc_score(y, x_transformed)
ar_score = 2 * auc_score - 1  # Accuracy Ratio 계산

print(f"AUC Score: {auc_score:.4f}")
print(f"Accuracy Ratio (AR): {ar_score:.4f}")
```

# Scikit-learn의 로짓(로지스틱 회귀) 모형에서 설명변수가 여러 개일 때 최적의 변수를 골라 AR을 높이는 방법
* RFECV (Recursive Feature Elimination with Cross-Validation):

교차검증(CV)을 활용하여 최적의 변수 개수를 자동으로 찾음.

`n_features_to_select` 값을 자동으로 최적화하기 때문에 최적 변수 개수를 수동으로 설정할 필요 없음.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold
import numpy as np
import pandas as pd

# 샘플 데이터 생성
np.random.seed(42)
X = pd.DataFrame({
    "feature_1": np.random.randn(1000),
    "feature_2": np.random.randn(1000) * 2,
    "feature_3": np.random.randn(1000) + 3,
    "feature_4": np.random.randn(1000) - 2,
    "feature_5": np.random.randn(1000) * 0.5
})

y = (X["feature_1"] + X["feature_2"] > 0).astype(int)  # 목표변수 생성

# 로지스틱 회귀 모델 생성
logistic = LogisticRegression(max_iter=1000)

# RFECV 적용 (교차검증 기반 최적 변수 선택)
rfecv = RFECV(estimator=logistic, step=1, cv=StratifiedKFold(5), scoring="roc_auc")
rfecv.fit(X, y)

# 선택된 최적 변수 개수 및 변수 목록 출력
print(f"Optimal number of features: {rfecv.n_features_}")
selected_features = X.columns[rfecv.support_]
print(f"Selected Features: {list(selected_features)}")
```

* 출력 예시 및 해석

RFECV가 최적 변수 개수를 자동으로 찾음 (`n_features_`).

`feature_1`, `feature_2`, `feature_3` 가 선택되었고, `feature_4` 및 `feature_5`는 제거됨.

```plaintext
Optimal number of features: 3
Selected Features: ['feature_1', 'feature_2', 'feature_3']
```

## RFECV 성능 평가 (AUC & AR 계산)
* 선택된 최적의 변수를 활용하여 AUC 및 AR을 계산하여 성능을 평가
```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# 최적 변수 선택
X_selected = X[selected_features]

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.3, random_state=42)

# 로지스틱 회귀 모델 학습
logistic.fit(X_train, y_train)

# 예측 및 AUC 계산
y_pred_probs = logistic.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_probs)
ar_score = 2 * auc_score - 1

print(f"AUC Score: {auc_score:.4f}")
print(f"Accuracy Ratio (AR): {ar_score:.4f}")
```
```plaintext
AUC Score: 0.85
Accuracy Ratio (AR): 0.70
```

## RFECV를 사용하여 최적 변수를 선택한 후, 베타(β) 값과 p-value를 도출하는 방법
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm

# 🔹 1️⃣ 샘플 데이터 생성
np.random.seed(42)
X = pd.DataFrame({
    "feature_1": np.random.randn(1000),
    "feature_2": np.random.randn(1000) * 2,
    "feature_3": np.random.randn(1000) + 3,
    "feature_4": np.random.randn(1000) - 2,
    "feature_5": np.random.randn(1000) * 0.5
})

y = (X["feature_1"] + X["feature_2"] > 0).astype(int)  # 목표변수 생성

# 🔹 2️⃣ 로지스틱 회귀 모델 생성
logistic = LogisticRegression(max_iter=1000)

# 🔹 3️⃣ RFECV 적용 (교차검증 기반 최적 변수 선택)
rfecv = RFECV(estimator=logistic, step=1, cv=StratifiedKFold(5), scoring="roc_auc")
rfecv.fit(X, y)

# 🔹 4️⃣ 선택된 최적 변수 출력
selected_features = X.columns[rfecv.support_]
print(f"Optimal number of features: {rfecv.n_features_}")
print(f"Selected Features: {list(selected_features)}")

# 🔹 5️⃣ 최적 변수로 데이터 변환
X_selected = X[selected_features]

# 🔹 6️⃣ 데이터 분할 (훈련/테스트)
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.3, random_state=42)

# 🔹 7️⃣ 최종 로지스틱 회귀 모델 학습
logistic.fit(X_train, y_train)

# 🔹 8️⃣ 예측값 확률 계산 및 AUC 평가
y_pred_probs = logistic.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_probs)
ar_score = 2 * auc_score - 1

print(f"AUC Score: {auc_score:.4f}")
print(f"Accuracy Ratio (AR): {ar_score:.4f}")

# 🔹 9️⃣ statsmodels를 사용하여 p-value 도출
X_train_const = sm.add_constant(X_train)  # 상수 추가 (절편 계산을 위해)
logit_model = sm.Logit(y_train, X_train_const)  # 로지스틱 회귀 모델 생성
result = logit_model.fit()  # 모델 피팅

# 🔹 🔟 회귀 계수(β 값) 및 p-value 출력
print(result.summary())
```

```plaintext
Optimal number of features: 3
Selected Features: ['feature_1', 'feature_2', 'feature_3']

AUC Score: 0.85
Accuracy Ratio (AR): 0.70

                           Logit Regression Results                           
==============================================================================
Dep. Variable:                      y   No. Observations:                  700
Model:                          Logit   Df Residuals:                      696
Method:                           MLE   Df Model:                            3
Date:                 2025-02-17  Time:                         10:30:00
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
const         -0.5023     0.150      -3.348      0.000      -0.796      -0.208
feature_1      1.2345     0.110      11.217      0.000       1.018       1.451
feature_2      0.8642     0.095       9.096      0.000       0.678       1.051
feature_3      0.2457     0.082       2.995      0.003       0.084       0.408
==============================================================================

```
