import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


###########################
# STEP 1 veri setini yukleyin.
##############################

employee = pd.read_csv('employee.csv')

employee.describe()

#Maas eksik olmustu. Buna bir de maas eklemek ıstersenız asagıdakı adımları takıp edebılırsınız. Yoksa dırekt STEP2'ye gecebılırsınız.
import numpy as np
maas = np.random.randint(30000, 100000, 300)
employee['Maas'] = maas


###############################################
# STEP 2 X ve Y'leri ayirma
############################################

X = employee.drop('Performans Notu', axis=1)
y = employee['Performans Notu']


###############################################
# STEP 3 olceklendirme
############################################


from sklearn.preprocessing import MinMaxScaler

sutun_adlari = X.columns

X = MinMaxScaler().fit_transform(X)

X = pd.DataFrame(X, columns=sutun_adlari)


###############################################
# STEP 4 veri setlerini ayirma
############################################
from sklearn.model_selection import train_test_split

# Eğitim ve test setlerine ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)



###############################################
# STEP 5 Tahmin yapip accuracy degerlerini elde etme
############################################
from sklearn.metrics import accuracy_score


# Logistic Regression Modeli
from sklearn.linear_model import LogisticRegression

# LOG REG nesnemizi cagiralim
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)   # Log reg'i kullanarak X_train ve y_train verisindeki oruntuleri ogren diyoruz
log_reg_pred = log_reg.predict(X_test) # Ogrendigin oruntuyu getir, ki bu model oluyor, ve su daha once gormedigin X_test veri setini kullanarak tahmin yap diyoruz.
log_reg_accuracy = accuracy_score(y_test, log_reg_pred) # Modelin gormedigi veri seti uzerindeki performansi


# Decision Tree Modeli
from sklearn.tree import DecisionTreeClassifier
dec_tree = DecisionTreeClassifier()
dec_tree.fit(X_train, y_train)
dec_tree_pred = dec_tree.predict(X_test)
dec_tree_accuracy = accuracy_score(y_test, dec_tree_pred)


# KNN Modeli
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)
knn_accuracy = accuracy_score(y_test, knn_pred)


# Sonuçları bir DataFrame'e dönüştür
sonuc = {
    "Logistic Regression": log_reg_accuracy,
    "Decision Tree": dec_tree_accuracy,
    "KNN": knn_accuracy
}

sonuc_df = pd.DataFrame(list(sonuc.items()), columns=["Model", "Accuracy"])
sonuc_df.sort_values(by='Accuracy', ascending=False)



# Modeli disa aktar
from joblib import dump
dump(dec_tree, 'decision_tree_model.joblib')

# Modeli okut
from joblib import load
dec_tree_loaded = load('decision_tree_model.joblib')
loaded_model_pred = dec_tree_loaded.predict(X_test)
