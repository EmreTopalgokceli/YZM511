import pandas as pd
import numpy as np


num_rows = 100
num_columns = 5
column_names = [f'X{i}' for i in range(1, 5)] + ['Y']
data = np.random.rand(num_rows, num_columns)
df = pd.DataFrame(data, columns=column_names)


# Pandas ayarlarını yapılandırıyoruz: Tüm sütunları göster ve genişliği artır.
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 100)


X = df[[f'X{i}' for i in range(1, 5)]]
X = df[["X1", "X2"]]
y = df[['Y']]


# MinMax scaler

sutun_isim = X.columns
from sklearn.preprocessing import MinMaxScaler
X = MinMaxScaler().fit_transform(X)
X = pd.DataFrame(X, columns=sutun_isim)
X.describe()


##############
## Model 1 ##
##############
# Scikit-learn ile bir lineer regresyon modeli oluşturuyoruz ve tahminler yaparak ortalama mutlak hata hesaplıyoruz.
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error as mae

model = LinearRegression()
model.fit(X,y)
pred = model.predict(X)
mea_validasyonsuz = mae(y, pred)


model1 = pd.DataFrame({'Coef_model1': model.coef_}, index=sutun_isim)
model1.loc['mea_validasyonsuz'] = mea_validasyonsuz

##############
## Model 2 ##
##############
# Veriyi eğitim ve test alt kümelerine böleriz.
from sklearn.model_selection import train_test_split
# Veriyi eğitim ve test alt kümelerine böleriz.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.24)

model = LinearRegression()
model.fit(X_train,y_train)
pred1 = model.predict(X_test)
mea_validasyonlu= mae(y_test, pred1)

# Modelin katsayılarını ve intercept değerini alıp bir veri çerçevesi oluşturuyoruz.
model2 = pd.DataFrame({'model2k': model.coef_.flatten()}, index=sutun_isim)
model2.loc['mea_validasyonlu'] = mea_validasyonlu

model_son = pd.concat([model1, model2], axis=1)




##
import statsmodels.api as sm
X = sm.add_constant(X)
reg_2 = sm.OLS(y, X).fit()
reg_2.summary()







df['Y'] = (df['Y']>0.5).astype(int)

X = df[[f'X{i}' for i in range(1, 5)]]
y = df[['Y']]




sutun_isim = X.columns
from sklearn.preprocessing import MinMaxScaler
X = MinMaxScaler().fit_transform(X)
X = pd.DataFrame(X, columns=sutun_isim)
X.describe()


# Veriyi eğitim ve test alt kümelerine böleriz.
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.54)

def egitim_test_orani_belirleme(soyisim):
    import random
    deger= len(soyisim)
    random.seed(deger)
    egitim_test_orani = round(random.uniform(0.1, 0.8), 2)
    return egitim_test_orani



# Örnek kullanım:
soyisim = "Basak"
print(f"Sayın {soyisim}, egitim-test oranınız:", egitim_test_orani_belirleme(soyisim))

# Support Vector Machine Modeli kullanarak tahmin yapınız ve accuracy değerlerini elde ediniz.
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
smv = SVC()
smv.fit(X_train, y_train)
smv_pred = smv.predict(X_test)
smv_acc = accuracy_score(y_test, smv_pred)




# Support Vector Machine Modeli kullanarak tahmin yapınız ve accuracy değerlerini elde ediniz.
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

from sklearn.ensemble import GradientBoostingClassifier
gb = GradientBoostingClassifier()
gb.fit(X_train, y_train)
gb_pred = gb.predict(X_test)
gb_acc = accuracy_score(y_test, gb_pred)



from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)
dt_acc = accuracy_score(y_test, dt_pred)



sonuc = {
    'SVC':smv_acc,
    'RF':rf_acc,
    'GB':gb_acc,
    'DT':dt_acc
    }



sonuc_df = pd.DataFrame(list(sonuc.items()), columns=['Model_adi', 'Basari_orani'])

sonuc_df.sort_values(by='Model_adi', ascending=True, inplace=True)
sonuc_df = sonuc_df.sort_values(by='Model_adi', ascending=True)


# pip install joblib
from joblib import dump
dump('dt', 'DT_son_hafta.joblib')


