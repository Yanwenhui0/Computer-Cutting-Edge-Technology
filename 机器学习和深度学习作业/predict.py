import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

data = pd.read_csv('abalone.csv', encoding='utf-8')
X=data.iloc[:, 0:8]
y=data['年龄']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
linreg = LinearRegression()
linreg.fit(X_train, y_train)
print("最佳拟合线的截距：" + str(linreg.intercept_))
print("回归系数：" + str(linreg.coef_))
y_pred = linreg.predict(X_test)
print("MSE：", metrics.mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(metrics.mean_squared_error(y_test, y_pred)))