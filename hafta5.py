# Eger daha once hicbir kutuphaneyi yuklemediyseniz:
# 1 - requirements.txt isimli bir belge olusturunuz.
# 2 - requirements.txt icine gerekli kutuphaneleri not ediniz. Bunlar:
# pandas
# numpy
# openpyxl
# scipy
# ipywidgets
# 3 - Terminal'e pip install -r requirements.txt yaziniz ve enter'e basarak komutu calistiriniz. Kutuphanelerin yuklendigini goreceksiniz.


import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, f_oneway, mannwhitneyu, kruskal, pearsonr, chi2_contingency, spearmanr


######################################################
# Parametrik testler icin varsayimlar
######################################################
# Normallik - shapiro
# Varyans homojenligi - levene



######################################################
# Grup karsilastirmasi parametrik & non-parametrik testler
######################################################

# Parametrik & iki grup ise 't testi' - ttest_ind
# Parametrik & iki+ grup ise 'Anova' - f_oneway

# Parametrik degil & iki grup ise 'Mann–Whitney U test' - mannwhitneyu
# Parametrik degil & iki+ grup ise 'Kruskal Wallis' - kruskal


######################################################
# Degiskenler arasinda iliski parametrik & non-parametrik testler
######################################################

# Parametrik test 'Pearson korelasyon analizi' - pearsonr
# Parametrik degil & nominal veri 'Chi-Square (Ki-Kare)' - chi2_contingency
# Parametrik degil & ordinal veri 'Chi-Square (Ki-Kare)' - spearmanr



######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# İki grup ortalaması arasında istatistiksel karşılaştırma yapmak için AB Testi veya Bağımsız İki Örneklem T Testi kullanılır. Süreç genellikle şu adımları içerir:


### Varsayım Kontrolü ###
# Normallik Varsayımı: Her iki grubun dağılımının normal olup olmadığını kontrol ederiz. Bunu Shapiro-Wilk testi ile yapabiliriz.
# Varyans Homojenliği: Levene testi  kullanarak, iki grubun varyanslarının homojen olup olmadığını test ederiz.


### Hipotezin Uygulanması ###
# Varsayımlar Sağlanıyorsa: Normallik ve varyans homojenliği varsayımı sağlanıyorsa, bağımsız iki örneklem t testi (parametrik test) uygulanır.
# Varsayımlar Sağlanmıyorsa: Eğer normallik varsayımı sağlanmıyorsa, Mann-Whitney U testi (non-parametrik test) kullanılır. Varyans homojenliği sağlanmıyorsa, t testi fonksiyonuna 'equal_var=False' argümanı girilerek Welch'in t testi uygulanır.

### Notlar ###
# Eğer normallik varsayımı sağlanmıyorsa, direkt olarak Mann-Whitney U testine geçilir.
# Yalnizca varyans homojenliği sağlanmıyorsa, bağımsız iki örneklem t testinin 'equal_var' parametresi 'False' olarak ayarlanır.




#############################################################################################################################
# Uygulama 1: Sigara İçen ve İçmeyen Müşterilerin Ortalama Hesap Tutarları Arasındaki Farkın İstatistiksel Olarak İncelenmesi
#############################################################################################################################

### Is problemi ###
# Lokanta sahibi, işletmesini daha verimli hale getirmek amacıyla bir gözlemde bulunmuştur:
# Sigara içilen bölümdeki masalarda ödenen ortalama hesap, sigara içilmeyen bölüme göre daha yüksek gibi görünmektedir.
# İşletmeyi ikiye ayırarak sigara içen ve içmeyen müşterileri farklı alanlarda ağırlamaya başlamıştır.
# Ancak bu gözlemin gerçekten bir eğilim mi yoksa rastlantısal bir durum mu olduğundan emin olmak istemektedir.
# Sigara içilen bölümü genişletmek ciddi bir yatırım gerektirecektir; özellikle havalandırma sistemlerinin güçlendirilmesi gibi
# ek masrafları da beraberinde getirecektir. Bu nedenle, lokanta sahibi öncelikle bu farkın istatistiksel olarak anlamlı olup
# olmadığını araştırmaya karar verir. Bu amaçla yapılan istatistiksel testler, ödenen ortalama hesap tutarları arasındaki
# farkın tesadüfen oluşup oluşmadığını anlamak için kullanılacaktır. Eğer fark istatistiksel olarak anlamlıysa,
# sigara içilen alanı genişletmek için gereken yatırımı yapmaya daha rahat karar verebilecektir.


########################################
# AŞAMA 1: Veriyi Python ortamında okuma
########################################


df = pd.read_excel('lokanta.xlsx')

##############################################################################
# AŞAMA 2: Hedef grupların (sigara içen vs. içmeyen) ortalamasını bakma
##############################################################################

# Bir hafta boyunca restoranımızı ziyaret eden müşterilerin, sigara içenler ve içmeyenler olmak üzere,
# ödedikleri ortalama hesap miktarlarını inceliyoruz. Bu bize hangi grubun daha fazla hesap ödediğine dair ilksel bir bilgi verecek.



df.groupby('Sigara_icen').agg({'Toplam_hesap': 'mean'})



# groupby().agg() birlikte kullanilan fonksiyonlardir.
# Gruplama: df.groupby('Sigara_icen') kısmı, veri tablosundaki müşterileri sigara içen ve içmeyen olarak ikiye ayırır. Buradaki amacımız, sigara içen müşterilerin verilerini bir yanda, içmeyenlerin verilerini diğer yanda toplamak.
# Ortalama Hesaplama: agg({'Toplam_hesap':'mean'}) kısmı ise, her iki gruptaki müşterilerin ödediği toplam hesap miktarlarının ortalamasını hesaplar. Burada 'agg' kısmı, gruplanmış veriler üzerinde bazı hesaplamalar yapmamızı sağlar ve 'mean' ile bu hesaplamanın ortalamayı bulmak olduğunu belirtiriz.


############################
# AŞAMA 3: Parametrik mi Parametrik değil mi (Varsayım Kontrolü)
############################

# Normallik Varsayımı
# Varyans Homojenliği

############################
# AŞAMA 3.1 :Normallik Varsayımı (shapiro)
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.

# Python'a bildirdigimiz method. Sadece shapiro'da iki grubu ayri ayri karsilastiriyoruz.

# Alternatif 1
shapiro(df.loc[df['Sigara_icen']== 'Evet', 'Toplam_hesap'])
shapiro(df.query("Sigara_icen == 'Evet'")['Toplam_hesap'])
# ShapiroResult(statistic=0.9896612167358398, pvalue=0.6855236887931824)

# Alternatif 2
shapiro(df.loc[df['Sigara_icen']== 'Hayır', 'Toplam_hesap'])
shapiro(df.query("Sigara_icen == 'Hayır'")['Toplam_hesap'])
# ShapiroResult(statistic=0.9955608248710632, pvalue=0.9312676787376404)

# Eğer p-değeri 0.05'ten küçükse, null hipotezi (H0) reddedilir.
# Eğer p-değeri 0.05'ten büyük veya eşitse, null hipotezi (H0) reddedilemez.


############################
# AŞAMA 3.2 : Varyans Homojenliği Varsayımı (levene)
# Normallik varsayimi saglanmiyorsa direkt Non-parametrik teste gecilmelidir.
############################

# H0: Grupların varyansları homojendir.
# H1: Grupların varyansları homojen değildir.



# Alternatif 1
levene(df.loc[df['Sigara_icen']== 'Evet', 'Toplam_hesap'],
       df.loc[df['Sigara_icen']== 'Hayır', 'Toplam_hesap'])
# LeveneResult(statistic=0.0013257623078349091, pvalue=0.9709846445282896)

# Alternatif 2
levene(df.query("Sigara_icen == 'Evet'")['Toplam_hesap'],
       df.query("Sigara_icen == 'Hayır'")['Toplam_hesap'])
# LeveneResult(statistic=0.0013257623078349091, pvalue=0.9709846445282896)

# Eğer p-değeri 0.05'ten küçükse, null hipotezi (H0) reddedilir.
# Eğer p-değeri 0.05'ten büyük veya eşitse, null hipotezi (H0) reddedilemez.


############################
# AŞAMA 4 : Nihai Test
# Normallik varsayimi ve Varyans homojenligi varsayimi birlikte saglandigi durumda: (2 grup karsilastirmasi icin t testi, 2+ grup karsilastirmasi icin ANOVA)
############################

# H0: Sigara içen ve içmeyen müşterilerin ödediği ortalama toplam hesap miktarları arasında istatistiksel olarak anlamlı bir fark yoktur.
# H1: Sigara içen ve içmeyen müşterilerin ödediği ortalama toplam hesap miktarları arasında istatistiksel olarak anlamlı bir fark vardır.

# Alternatif 1
ttest_ind(df.loc[df['Sigara_icen']== 'Evet', 'Toplam_hesap'],
          df.loc[df['Sigara_icen']== 'Hayır', 'Toplam_hesap'],
          equal_var=True)
# TtestResult(statistic=1.5310836731464508, pvalue=0.12705485801677924, df=242.0)

# Alternatif 1
ttest_ind(df.query("Sigara_icen == 'Evet'")['Toplam_hesap'],
          df.query("Sigara_icen == 'Hayır'")['Toplam_hesap'],
          equal_var=True)
# TtestResult(statistic=1.5310836731464508, pvalue=0.12705485801677924, df=242.0)

# p-value < 0.05 ise HO RET.
# p-value > 0.05 ise H0 REDDEDILEMEZ.


############################
# AŞAMA 4.1 : Nihai Test (Normallik varsayiminin saglandigi fakat varyans homojenliginin saglanmadigi durum)
# Normallik varsayimi ve Varyans homojenligi varsayimi birlikte saglandigi durumda: (2 grup karsilastirmasi icin t testi, 2+ grup karsilastirmasi icin ANOVA)
############################

# H0: Sigara içen ve içmeyen müşterilerin ödediği ortalama toplam hesap miktarları arasında istatistiksel olarak anlamlı bir fark yoktur.
# H1: Sigara içen ve içmeyen müşterilerin ödediği ortalama toplam hesap miktarları arasında istatistiksel olarak anlamlı bir fark vardır.

# Alternatif 1
ttest_ind(df.loc[df['Sigara_icen']== 'Evet', 'Toplam_hesap'],
          df.loc[df['Sigara_icen']== 'Hayır', 'Toplam_hesap'],
          equal_var=False)

# Alternatif 1
ttest_ind(df.query("Sigara_icen == 'Evet'")['Toplam_hesap'],
          df.query("Sigara_icen == 'Hayır'")['Toplam_hesap'],
          equal_var=False)

############################
# AŞAMA 4.2 Nihai Test (Varsayımlar sağlanmıyorsa mannwhitneyu testi - non-parametrik test)
############################

mannwhitneyu(df.loc[df['Sigara_icen']== 'Evet', 'Toplam_hesap'],
            df.loc[df['Sigara_icen']== 'Hayır', 'Toplam_hesap'])



#############################################################################################################################
# Uygulama 2: Spor Salonu Üyelik Paketleri Testi
#############################################################################################################################

### Is problemi ###
# Bir spor salonu sahibi, üyelerinin spor salonu deneyimlerini iyileştirmek için iki farklı üyelik paketini test
# etmeye karar veriyor: "Standart Paket" ve "Premium Paket". Standart Paket, temel spor salonu hizmetlerini sunarken,
# Premium Paket ek olarak kişisel antrenman seansları ve özel grup derslerini içeriyor. Üyeler, bu iki paketten birini
# seçerek salonu kullanmaya başlıyorlar. Salon sahibi, hangi paketin üyelerin spor salonundaki genel memnuniyet ve
# katılım sıklığı üzerinde daha etkili olduğunu belirlemek istiyor. Eğer Premium Paketin üyeler üzerinde olumlu bir
# etkisi istatistiksel olarak anlamlıysa, bu pakete daha fazla yatırım yapmayı ve pazarlamayı artırmayı düşünebilir.

# Veri Seti Özellikleri

# Üye ID: Her üyeye özgü bir tanımlayıcı.
# Üyelik Paketi: "Standart" veya "Premium".
# Memnuniyet Puanı: Üyenin genel memnuniyetini yansıtan puan, 1'den 5'e kadar.
# Katılım Sıklığı: Aylık spor salonu ziyaret sayısı.
# Yaş Grubu: Üyenin yaş grubu (örn. "18-25", "26-35", "36-45" gibi).


########################################
# AŞAMA 1: Veriyi Python ortamında okuma
########################################

df = pd.read_excel('spor_salonu_uyelik_veriseti.xlsx')


##############################################################################
# AŞAMA 2: Hedef grupların (Standart Uyelik & Premium Uyelik) ortalamasını bakma
##############################################################################

# Bir hafta boyunca restoranımızı ziyaret eden müşterilerin, sigara içenler ve içmeyenler olmak üzere,
# ödedikleri ortalama hesap miktarlarını inceliyoruz. Bu bize hangi grubun daha fazla hesap ödediğine dair ilksel bir bilgi verecek.

df.groupby('Uyelik_Paketi').agg({'Memnuniyet_Puani': 'mean'})

df.groupby('Uyelik_Paketi').agg({'Katilim_Sikligi': 'mean'})


############################
# AŞAMA 3: Parametrik mi Parametrik değil mi (Varsayım Kontrolü)
############################

# Normallik Varsayımı
# Varyans Homojenliği

############################
# AŞAMA 3.1 :Normallik Varsayımı (shapiro)
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.

# Alternatif 1
shapiro(df.loc[df['Uyelik_Paketi']== 'Standart', 'Memnuniyet_Puani'])
shapiro(df.query("Uyelik_Paketi == 'Standart'")['Memnuniyet_Puani'])
# ShapiroResult(statistic=0.8791409134864807, pvalue=1.6694144733264693e-07)

# Alternatif 2
shapiro(df.loc[df['Uyelik_Paketi']== 'Premium', 'Memnuniyet_Puani'])
shapiro(df.query("Uyelik_Paketi == 'Premium'")['Memnuniyet_Puani'])
# ShapiroResult(statistic=0.8791409134864807, pvalue=1.6694144733264693e-07)

# Eğer p-değeri 0.05'ten küçükse, null hipotezi (H0) reddedilir.
# Eğer p-değeri 0.05'ten büyük veya eşitse, null hipotezi (H0) reddedilemez.

# Eğer normallik varsayımı sağlanmıyorsa, direkt olarak Mann-Whitney U testine geçilir.

############################
# AŞAMA 4 Nihai Test (Varsayımlar sağlanmıyorsa mannwhitneyu testi - non-parametrik test)
############################

# H0: Standart uyelik paketi ve premium uyelik paketi bulunanlarin memnuniyet puanlari arasında istatistiksel olarak anlamlı bir fark yoktur.
# H1: Standart uyelik paketi ve premium uyelik paketi bulunanlarin memnuniyet puanlari arasında istatistiksel olarak anlamlı bir fark vardir.

mannwhitneyu(df.loc[df['Uyelik_Paketi']== 'Standart', 'Memnuniyet_Puani'],
            df.loc[df['Uyelik_Paketi']== 'Premium', 'Memnuniyet_Puani'])

# p-value < 0.05 ise HO RET.
# p-value > 0.05 ise H0 REDDEDILEMEZ.
