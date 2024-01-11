# İlgili kütüphaneleri içe aktarıyoruz.
import pandas as pd

# Pandas ayarlarını yapılandırıyoruz: Tüm sütunları göster ve genişliği artır.
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Scikit-learn kütüphanelerini içe aktarıyoruz.
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error as mae
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


# 'emlak_data1.xlsx' ve 'emlak_data2.xlsx' Excel dosyalarını okuyoruz.
df = pd.read_excel('emlak_data1.xlsx')
df1 = pd.read_excel('emlak_data2.xlsx')

# İki veri çerçevesini 'Port_no' sütunu üzerinden birleştiriyoruz ve 'emre' adında yeni bir veri çerçevesi oluşturuyoruz.
emre = pd.merge(df, df1, on='Port_no')

# 'Port_no' sütununu kaldırıyoruz. Yalnizca veri setlerini birlestirmek icin ihtiyac duyuyorduk.
emre.drop('Port_no', axis=1, inplace=True)

# Bağımsız (x) ve bağımlı (y) değişkenleri belirliyoruz.
X = emre[['OrtGel', 'Bina_Yasi', 'OrtOda', 'Ort_Y', 'Nufus', 'Ort_Hane', 'Enlem', 'Boylam']]
y = emre['Fiyat']

# Bağımsız değişkenleri Min-Max ölçeklendirme ile normalize ediyoruz.
sutun_adlari = X.columns
X = MinMaxScaler().fit_transform(X)
X = pd.DataFrame(X, columns=sutun_adlari)

##############
## Model 1 ##
##############
# Scikit-learn ile bir lineer regresyon modeli oluşturuyoruz ve tahminler yaparak ortalama mutlak hata hesaplıyoruz.
model = LinearRegression()
model.fit(X, y)
predictions = model.predict(X)
mae_without_validation = mae(y, predictions)

# Modelin katsayılarını ve hangi değişkenlere ait olduğunu gösteren bir veri çerçevesi oluşturuyoruz.
model1 = pd.DataFrame({'Coef_model1': model.coef_}, index=sutun_adlari)
model1.loc['mae_without_validation'] = mae_without_validation

##############
## Model 2 ##
##############
# Veriyi eğitim ve test alt kümelerine böleriz.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Modeli eğitiriz ve test verileri üzerinde tahminler yaparak ortalama mutlak hata hesaplarız.
model.fit(X_train, y_train)
predictions1 = model.predict(X_test)
mae_with_validation = mae(y_test, predictions1)

# Modelin katsayılarını ve intercept değerini alıp bir veri çerçevesi oluşturuyoruz.
model2 = pd.DataFrame({'Coef_model2': model.coef_}, index=sutun_adlari)
model2.loc['mae_with_validation'] = mae_with_validation

## Model 1 & Model 2 - Karsilastirma ##
# İki modelin sonuçlarını birleştirerek bir sonuç veri çerçevesi oluşturuyoruz.
model_son = pd.concat([model1, model2], axis=1)

##########################
## STATSMODELS ILE TAHMIN ##
##########################
# Statsmodels kütüphanesini içe aktarıyoruz.
import statsmodels.api as sm
# Statsmodels ile bağımsız değişkenleri ekleyerek OLS ile bir lineer regresyon modeli oluşturuyoruz ve özet bilgilerini gösteriyoruz.
X = sm.add_constant(X)
reg_model = sm.OLS(y, X).fit()
reg_model.summary()








#################
## ALISTIRMA 1 ##
#################

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error as mae
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# 'reG_veri' isimli veri setini okuyun:

# Bağımsız ve bağımlı değişkenleri belirleyin: 'X' ve 'y' değişkenlerini oluşturun.

# Bağımsız (X) değişkenleri Min-Max ölçeklendirme ile normalize edin.

# Veriyi eğitim ve test alt kümelerine bölun: Test verisi oranını %40 olarak ayarlayın.

# Scikit-learn ile bir lineer regresyon modeli oluşturun, eğitin ve tahminler yapın.

# Eğitim verileri üzerinde tahminler yaparak ortalama mutlak hata (MAE) hesaplayın.

# Modelin katsayılarını ve MAE değerini içeren bir veri çerçevesi oluşturun.

# Test verileri üzerinde tahminler yaparak test hatasını hesaplayın.

# Modelin test hatası ile birlikte katsayılarını içeren bir veri çerçevesi oluşturun.


# İpuçular:
# - MinMaxScaler sınıfını kullanarak bağımsız değişkenleri normalize edebilirsiniz.
# - train_test_split fonksiyonu ile veriyi bölebilir ve egitim verisini elde edebilirsiniz.
# - LinearRegression sınıfını kullanarak bir lineer regresyon modeli oluşturabilirsiniz.
# - mean_absolute_error fonksiyonu ile ortalama mutlak hata hesaplayabilirsiniz.
# - Veri setindeki bagimli degisken (y) Fiyat degiskenidir.

# Veri analizi ve modelleme adımlarını sırayla uygulayın.

# Sonuçları yazdırın.


##################
## Alistirma  2 ##
##################

# 'reG_veri' isimli veri setini kullanarak Statsmodels ile bir lineer regresyon modeli oluşturun ve model sonuçlarını bir world belgesine kopyalayip yorumlayiniz.





