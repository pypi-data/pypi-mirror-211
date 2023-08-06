import srp as srp

srp_exp1a = '''
from numpy import median
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
import os
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
%matplotlib inline


for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

df = pd.read_csv('../input/covid19-patient-precondition-dataset/covid.csv')

df.drop(columns={'entry_date', 'date_died',
        'date_symptoms', 'id'}, axis=1, inplace=True)

df['covid_res'].replace([1, 2, 3], [1, 0, 2], inplace=True)
df['covid_res'].value_counts().to_frame()

df.rename(columns={'covid_res': 'Chance'}, inplace=True)
df.head()

Splitting the data into train and test

train = df[['sex', 'patient_type', 'intubed', 'pneumonia', 'age', 'pregnancy',
            'diabetes', 'copd', 'asthma', 'inmsupr', 'hypertension',
           'other_disease', 'cardiovascular', 'obesity', 'renal_chronic',
            'tobacco', 'contact_other_covid', 'icu']]

test = df['Chance']
train = train.values
test = np.array(test)

Splitting further into 8: 2 ratio

x_train, x_test, y_train, y_test = train_test_split(
    train, test, test_size=0.2, random_state=42, stratify=test)
acc = []


Training the model using different algorithms

KNN


print(“KNN Accuracy: ”)
for i in range(1, 25):

    neigh = KNeighborsClassifier(n_neighbors=i).fit(x_train, y_train)
    yhat = neigh.predict(x_test)
    KNN_score = metrics.accuracy_score(y_test, yhat)
    print("Train set Accuracy at {} is {}  ".format(
        i, metrics.accuracy_score(y_train, neigh.predict(x_train))))
    print("Test set Accuracy at {} is {}".format(i, KNN_score))

acc.append(0.6290)

Decision Tree

print(“Decision Tree Accuracy ”)
for i in range(1, 25):
    drugTree = DecisionTreeClassifier(criterion="entropy", max_depth=i)
    drugTree.fit(x_train, y_train)
    predTree = drugTree.predict(x_test)
    decisionTree_score = metrics.accuracy_score(y_test, predTree)
    print("DecisionTrees's Accuracy at {} is {}\n".format(
        i, metrics.accuracy_score(y_test, predTree)))
    acc.append(logReg_score)

Logistic Regression

LR = LogisticRegression(C=0.03, solver='liblinear')
LR.fit(x_train, y_train)
yhat = LR.predict(x_test)
yhat_prob = LR.predict_proba(x_test)
logReg_score = metrics.accuracy_score(y_test, yhat)
print("LogisticRegression's Accuracy:{0}".format(
    metrics.accuracy_score(y_test, yhat)))

SVM

clf = svm.SVC(kernel='rbf')
clf.fit(x_train, y_train)
yhat = clf.predict(x_test)
svm_score = metrics.accuracy_score(y_test, yhat)
print("SVM's Accuracy:{0}".format(metrics.accuracy_score(y_test, yhat)))
acc.append(svm_score)

Random Forest Classifier

Random_forest = RandomForestClassifier(n_estimators=50)
Random_forest.fit(x_train, y_train)
randomForest_predict = Random_forest.predict(x_test)
randomForest_score = metrics.accuracy_score(y_test, randomForest_predict)
print("Random Forest Score :", randomForest_score)
acc.append(randomForest_score)

Gradient Boosting


gbk = GradientBoostingClassifier(
    random_state=100, n_estimators=150, min_samples_split=100, max_depth=6)
gbk.fit(x_train, y_train)
gbk_predict = gbk.predict(x_test)
gbk_score = gbk.score(x_test, y_test)
#print("Gradient Boosting Prediction :",gbk_predict)
print("Gradient Boosting Score :", gbk_score)

acc.append(gbk_score)
algo_name = ['KNN', 'Decision Tree', 'Logistic Regression',
             'SVM', 'Random Forest', 'Gradient Boosting']
acc = np.array(acc)

Conclusion

plt.figure(figsize=(10, 8))
sns.barplot(y=acc*100, x=algo_name, estimator=median, palette="Blues_d")
plt.xlabel('Accuracy', size=30)
plt.xticks(rotation=45)
plt.ylabel('Algorithm Name', size=30)
'''


srp_exp1b = '''
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels
import statsmodels.api as sm
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
df = pd.read_csv(r'/kaggle/input/salary-dataset-simple-linear-regression/Salary_dataset.csv')
df.head()
srp_X = df['YearsExperience']
y = df['Salary']

Create Train and Test Datasets:
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.7,test_size = 0.3, random_state = 100)
print('The shape of X_train is ', X_train.shape)
print('The shape of X_test is ', X_test.shape)
print('The shape of y_train is ', y_train.shape)
print('The shape of y_test is ', y_test.shape)

Adding Constant Variable to the Model 
X_train_sm = sm.add_constant(X_train)
X_train_sm.head()
Fitting the Model
lr = sm.OLS(y_train, X_train_sm)   # This creates a Linear Regression Object
lr_model = lr.fit()
lr_model.params

Predictions on Data Set : 
X_test_sm = sm.add_constant(X_test)
X_test_sm.head()
y_test_pred = lr_model.predict(X_test_sm)
y_test_pred.head()
'''

srp_exp2a = '''
import os
os.environ['HADOOP_HOME'] = 'C:\BigDataLocalSetup\hadoop'
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
spark = SparkSession.builder.appName('SoilTypeClassification').getOrCreate()
train_data = spark.read.csv('train.csv', header=True, inferSchema=True)
test_data = spark.read.csv('test.csv', header=True, inferSchema=True)
train_data
assembler = VectorAssembler(inputCols=train_data.columns[:-1], outputCol='features')
train_data = assembler.transform(train_data)
test_data = assembler.transform(test_data)
train_set, validation_set = train_data.randomSplit([0.8, 0.2], seed=13)
classifier = RandomForestClassifier(labelCol='Cover_Type', featuresCol='features')
model = classifier.fit(train_set)
predictions = model.transform(validation_set)
evaluator = MulticlassClassificationEvaluator(labelCol='Cover_Type', predictionCol='prediction', metricName='accuracy')
accuracy = evaluator.evaluate(predictions)
print('Accuracy on validation set:', accuracy)
test_predictions = model.transform(test_data)
import pandas as pd
pandas_df = test_predictions.select('Id', 'prediction').toPandas()
pandas_df.to_csv('Submission.csv', header=True, index=False)
'''

srp_exp2b = '''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from pyspark.sql import Window
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as Fsum
from pyspark.sql.functions import col
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, ArrayType, FloatType, DoubleType, Row, DateType, StringType
from pyspark.ml.feature import Normalizer, StandardScaler
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from sklearn.utils import resample
spark = SparkSession \
    .builder \
    .appName("Sparkify_1") \
    .getOrCreate()
path = "sparkify.json"
df = spark.read.json(path)
df.printSchema()
df.take(1)
df.select("userId").dropDuplicates().count()
df_clean = df.dropna(how='any', subset=['userId', 'sessionId'])
df_clean = df_clean.filter(df_clean['userId'] != '')
get_date = udf(lambda x: datetime.datetime.fromtimestamp(
    x / 1000.0).strftime("%Y-%m-%d"))
df_clean = df_clean.withColumn(
    "registration_date", get_date(df_clean.registration))
get_hour = udf(lambda x: datetime.datetime.fromtimestamp(
    x / 1000.0).strftime("%H"))
df_clean = df_clean.withColumn("hour", get_hour(df_clean.ts))
get_location = udf(lambda x: x[-2:])
df_clean = df_clean.withColumn(
    "location_state", get_location(df_clean.location))
df_clean.createOrReplaceTempView('user_log_table')
churn = spark.sql(
    'SELECT DISTINCT userId, 1 as churn FROM user_log_table WHERE Page = "Cancellation Confirmation"')
no_churn = spark.sql('SELECT DISTINCT userId, 0 as churn FROM user_log_table \
                      WHERE userId NOT IN (SELECT DISTINCT userId FROM user_log_table WHERE Page = "Cancellation Confirmation")')
churn_combined = churn.union(no_churn)
churn_combined.createOrReplaceTempView('churn_nochurn')
churn_combined = spark.sql('SELECT * FROM churn_nochurn ORDER BY RAND()')
churn_combined.count()
churn_df = df_clean.join(churn_combined, on='userId')
churn_df.select(['userId', 'churn']).dropDuplicates().show(20)
churn_df.select('page').dropDuplicates().show()
song_per_user = churn_df \
    .select("userId", "song")\
    .groupby("userId")\
    .count()\
    .withColumnRenamed("count", "song_per_user")
song_per_user.describe().show()
gender_num = churn_df\
    .select('userId', 'gender')\
    .dropDuplicates() \
    .replace(['M', 'F'], ['0', '1'], 'gender')\
    .select('userId', col('gender').cast('int'))\
    .withColumnRenamed('gender', 'gender_num')
gender_num.describe().show()
thumbs_up = churn_df \
    .select('userID', 'page') \
    .where(churn_df.page == 'Thumbs Up') \
    .groupBy('userID') \
    .count() \
    .withColumnRenamed('count', 'thumbs_up')
thumbs_up.describe().show()
thumbs_down = churn_df \
    .select('userID', 'page') \
    .where(churn_df.page == 'Thumbs Down') \
    .groupBy('userID') \
    .count() \
    .withColumnRenamed('count', 'thumbs_down')
thumbs_down.describe().show()
listening_time = churn_df \
    .select('userId', 'length') \
    .groupby(['userId']) \
    .sum() \
    .withColumnRenamed('sum(length)', 'listening_time')
listening_time.describe().show()
level_num = churn_df\
    .select('userId', 'level')\
    .replace(['free', 'paid'], ['0', '1'], 'level')\
    .select('userId', col('level').cast('int'))\
    .withColumnRenamed('level', 'level_num')
level_num.describe().show()
label = churn_df \
    .select('userId', col('churn').alias('label')) \
    .dropDuplicates()
label.describe().show()
data = song_per_user.join(gender_num, 'userID', 'outer') \
    .join(thumbs_up, 'userID', 'outer') \
    .join(thumbs_down, 'userID', 'outer') \
    .join(listening_time, 'userID', 'outer') \
    .join(level_num, 'userID', 'outer') \
    .join(label, 'userID', 'outer') \
    .drop('userID') \
    .fillna(0)
data.show(5)
cols = ['song_per_user', 'gender_num', 'thumbs_up',
        'thumbs_down', 'level_num', 'listening_time']
assembler = VectorAssembler(inputCols=cols, outputCol="NumFeatures")
data = assembler.transform(data)
scaler = StandardScaler(inputCol="NumFeatures",
                        outputCol="features", withStd=True)
scalerModel = scaler.fit(data)
data = scalerModel.transform(data)
rest, validation = data.randomSplit([0.8, 0.2], seed=42)
lr = LogisticRegression(maxIter=10, regParam=0.0, elasticNetParam=0)
f_score = MulticlassClassificationEvaluator(metricName='f1')
lr_train = lr.fit(rest)
lr_test = lr_train.transform(validation)
evaluator = MulticlassClassificationEvaluator(predictionCol='prediction')
print('Accuracy:')
print(evaluator.evaluate(lr_test, {evaluator.metricName: 'accuracy'}))
print('F-1 score:')
print(evaluator.evaluate(lr_test, {evaluator.metricName: 'f1'}))
rf = RandomForestClassifier()
f_score = MulticlassClassificationEvaluator(metricName='f1')

rf_train = rf.fit(rest)
rf_test = rf_train.transform(validation)
evaluator = MulticlassClassificationEvaluator(predictionCol='prediction')
print('Accuracy:')
print(evaluator.evaluate(rf_test, {evaluator.metricName: 'accuracy'}))
print('F-1 score:')
print(evaluator.evaluate(rf_test, {evaluator.metricName: 'f1'}))
gb = GBTClassifier()
f_score = MulticlassClassificationEvaluator(metricName='f1')
gb_train = gb.fit(rest)
gb_test = gb_train.transform(validation)
evaluator = MulticlassClassificationEvaluator(predictionCol='prediction')
print('Accuracy')
print(evaluator.evaluate(gb_test, {evaluator.metricName: 'accuracy'}))
print('F-1 score')
print(evaluator.evaluate(gb_test, {evaluator.metricName: 'f1'}))
train, test = data.randomSplit([0.7, 0.3], seed=42)
gb_tuned = GBTClassifier()
paramGrid = ParamGridBuilder()\
    .addGrid(gb_tuned.maxIter, [5, 10])\
    .addGrid(gb_tuned.maxDepth, [4, 12]) \
    .build()
crossval_gbt = CrossValidator(estimator=gb_tuned,
                              evaluator=f_score,
                              estimatorParamMaps=paramGrid,
                              numFolds=3)
gb_train = gb_tuned.fit(train)
gb_test = gb_train.transform(test)
evaluator = MulticlassClassificationEvaluator(predictionCol='prediction')
print('Gradient Boosting Results')
print('Accuracy')
print(evaluator.evaluate(gb_test, {evaluator.metricName: 'accuracy'}))
print('F-1 score')
print(evaluator.evaluate(gb_test, {evaluator.metricName: 'f1'}))
gb_train.featureImportances
importances = [0.2823, 0.0366, 0.2839, 0.2563, 0.0191, 0.1219]
features = ['song_per_user', 'gender_num', 'thumbs_up',
            'thumbs_down', 'level_num', 'listening_time']
feat = np.arange(len(features))
plt.barh(feat, importances, align='center', alpha=0.5)
plt.yticks(feat, features)
plt.xlabel('Importance Score')
plt.title('Feature Importances')
'''

srp_exp3a = '''
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
# Load the dataset
data = pd.read_csv('car_prices.csv')
# Drop irrelevant columns
columns_to_drop = ['column1', 'column2', ...]  # Specify the columns to drop
data = data.drop(columns=columns_to_drop)
# Handle missing values
data = data.dropna()  # Drop rows with missing values
# Alternatively, you can fill missing values with mean, median, or mode:
# data['column'] = data['column'].fillna(data['column'].mean())
# Encode categorical variables
categorical_columns = ['make', 'model', ...]  # Specify the categorical columns
label_encoder = LabelEncoder()
for column in categorical_columns:
    data[column] = label_encoder.fit_transform(data[column])
# Normalize numerical variables
numerical_columns = ['price', 'mileage', ...]  # Specify the numerical columns
scaler = MinMaxScaler()
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])
# Save preprocessed data
data.to_csv('preprocessed_car_prices.csv', index=False)

'''

srp_exp3b = '''
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
# Load the dataset
data = pd.read_csv('Sales.csv')
# Drop irrelevant columns
columns_to_drop = ['column1', 'column2', ...]  # Specify the columns to drop
data = data.drop(columns=columns_to_drop)
# Handle missing values
data = data.dropna()  # Drop rows with missing values
# Alternatively, you can fill missing values with mean, median, or mode:
# data['column'] = data['column'].fillna(data['column'].mean())
# Encode categorical variables
categorical_columns = ['make', 'model', ...]  # Specify the categorical columns
label_encoder = LabelEncoder()
for column in categorical_columns:
    data[column] = label_encoder.fit_transform(data[column])
# Normalize numerical variables
numerical_columns = ['price', 'mileage', ...]  # Specify the numerical columns
scaler = MinMaxScaler()
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])
# Save preprocessed data
data.to_csv('preprocessed_car_prices.csv', index=False)

'''


srp_exp4a = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt     # is a collection of command style functions that make 
import seaborn as sns

df_train= pd.read_csv(r'D:\5th_semester\MiniProject2A\Projectworking\dataset\Train.csv')
df_test= pd.read_csv(r'D:\5th_semester\MiniProject2A\Projectworking\dataset\Test.csv')
df_train.head()  # displays the first five rows of the dataframe by default
df_train.shape  

df_train['Item_Weight'].describe()  #seeing all the central tendenies of the dataset
df_train.describe()  

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()

df_train['item_fat_content']= le.fit_transform(df_train['item_fat_content'])
df_train['item_type']= le.fit_transform(df_train['item_type'])
df_train['outlet_size']= le.fit_transform(df_train['outlet_size'])
df_train['outlet_location_type']= le.fit_transform(df_train['outlet_location_type'])
df_train['outlet_type']= le.fit_transform(df_train['outlet_type'])



X=df_train.drop('item_outlet_sales',axis=1)
Y=df_train['item_outlet_sales']

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, random_state=101, test_size=0.2)
from sklearn.preprocessing import StandardScaler
sc= StandardScaler()
X_train_std= sc.fit_transform(X_train)  # learning how the data is in X train and then transforming
X_test_std= sc.transform(X_test)
X_train_std

from xgboost import XGBRegressor
xg= XGBRegressor()

xg.fit(X_train_std, Y_train)

from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV

# define models and parameters
model = RandomForestRegressor()
n_estimators = [10, 100, 1000]
max_depth=range(1,31)
min_samples_leaf=np.linspace(0.1, 1.0)
max_features=["auto", "sqrt", "log2"]
min_samples_split=np.linspace(0.1, 1.0, 10)

# define grid search
grid = dict(n_estimators=n_estimators)


grid_search_forest = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, 
                           scoring='r2',error_score=0,verbose=2,cv=2)

grid_search_forest.fit(X_train_std, Y_train)

# summarize results
print(f"Best: {grid_search_forest.best_score_:.3f} using {grid_search_forest.best_params_}")
means = grid_search_forest.cv_results_['mean_test_score']
stds = grid_search_forest.cv_results_['std_test_score']
params = grid_search_forest.cv_results_['params']

for mean, stdev, param in zip(means, stds, params):
    print(f"{mean:.3f} ({stdev:.3f}) with: {param}")

'''


srp_exp4b = '''
# Installation of required libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression  
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier 
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import GradientBoostingClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score, GridSearchCV

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=FutureWarning) 
warnings.filterwarnings("ignore", category=UserWarning) 

%config InlineBackend.figure_format = 'retina'

# to display all columns and rows:
pd.set_option('display.max_columns', None); pd.set_option('display.max_rows', None);


# Reading the dataset

churn_url = “Churn-Prediction-using-Machine-Learning/churn.csv at main · ahmetcankaraoglan/Churn-Prediction-using-Machine-Learning · GitHub”
from urllib.request import urlretrieve
urlretrieve(churn_url,”churn.csv”)
df = pd.read_csv("../input/predicting-churn-for-bank-customers/Churn_Modelling.csv", index_col=0)
df.columns = map(str.lower, df.columns)

df.head()

df.shape()

df.info()

df.groupby("gender").agg({"age": "mean"})

df.nunique()

# The distribution of the dependent variable in the dataset is plotted as pie and columns graphs.
f,ax=plt.subplots(1,2,figsize=(18,8))
srp_df['exited'].value_counts().plot.pie(explode=[0,0.1],autopct='%1.1f%%',ax=ax[0],shadow=True)
ax[0].set_title('dağılım')
ax[0].set_ylabel('')
sns.countplot('exited',data=df,ax=ax[1])
ax[1].set_title('exited')
plt.show()


# Plotted the categorical variables on the basis of the graph of the column according to the dependent variable.
fig, axarr = plt.subplots(2, 2, figsize=(20, 12))
sns.countplot(x='geography', hue = 'exited',data = df, ax=axarr[0][0])
sns.countplot(x='gender', hue = 'exited',data = df, ax=axarr[0][1])
sns.countplot(x='hascrcard', hue = 'exited',data = df, ax=axarr[1][0])
sns.countplot(x='isactivemember', hue = 'exited',data = df, ax=axarr[1][1])


# Boxplot graph for outlier observation analysis
fig, axarr = plt.subplots(3, 2, figsize=(20, 12))
sns.boxplot(y='creditscore',x = 'exited', hue = 'exited',data = df, ax=axarr[0][0])
sns.boxplot(y='age',x = 'exited', hue = 'exited',data = df , ax=axarr[0][1])
sns.boxplot(y='tenure',x = 'exited', hue = 'exited',data = df, ax=axarr[1][0])
sns.boxplot(y='balance',x = 'exited', hue = 'exited',data = df, ax=axarr[1][1])
sns.boxplot(y='numofproducts',x = 'exited', hue = 'exited',data = df, ax=axarr[2][0])
sns.boxplot(y='estimatedsalary',x = 'exited', hue = 'exited',data = df, ax=axarr[2][1])

# Missing Observation Analysis
df.isnull().sum()


# Train-Test Separation
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.20, random_state=12345)

from imblearn.combine import SMOTETomek

smk = SMOTETomek()
# Oversample training  data
X_train, y_train = smk.fit_sample(X_train, y_train)

# Oversample validation data
X_test, y_test = smk.fit_sample(X_test, y_test)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

models = []
models.append(('LR', LogisticRegression(random_state = 12345)))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier(random_state = 12345)))
models.append(('RF', RandomForestClassifier(random_state = 12345)))
models.append(('SVM', SVC(gamma='auto', random_state = 12345)))
models.append(('XGB', GradientBoostingClassifier(random_state = 12345)))
models.append(("LightGBM", LGBMClassifier(random_state = 12345)))
models.append(("CatBoost", CatBoostClassifier(random_state = 12345, verbose = False)))

# evaluate each model in turn
results = []
names = []
for name, model in models:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        msg = "%s: (%f)" % (name, accuracy)
print(msg)


models2 = []
models2.append(('CART', DecisionTreeClassifier( random_state = 12345)))
models2.append(('RF', RandomForestClassifier( random_state = 12345)))
models2.append(('XGB', GradientBoostingClassifier( random_state = 12345)))
models2.append(("LightGBM", LGBMClassifier( random_state = 12345)))
models2.append(("CatBoost", CatBoostClassifier(random_state = 12345, verbose = False)))

models2 = []
models2.append(('CART', DecisionTreeClassifier( random_state = 12345)))
models2.append(('RF', RandomForestClassifier( random_state = 12345)))
models2.append(('XGB', GradientBoostingClassifier( random_state = 12345)))
models2.append(("LightGBM", LGBMClassifier( random_state = 12345)))
models2.append(("CatBoost", CatBoostClassifier(random_state = 12345, verbose = False)))



from matplotlib import rc,rcParams
def plot_confusion_matrix(cm, classes,title='Confusion matrix', cmap=plt.cm.Blues):

    plt.rcParams.update({'font.size': 19})
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title,fontdict={'size':'16'})
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45,fontsize=12,color="blue")
    plt.yticks(tick_marks, classes,fontsize=12,color="blue")
    rc('font', weight='bold')
    fmt = '.1f'
    thresh = cm.max()
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="red")

    plt.ylabel('True label',fontdict={'size':'16'})
    plt.xlabel('Predicted label',fontdict={'size':'16'})
    plt.tight_layout()

import itertools
plot_confusion_matrix(confusion_matrix(y_test, y_pred=y_pred), classes=['Non Churn','Churn'],title='Confusion matrix


tn, fp, fn, tp = cm_xgb.ravel()
print("True Negatives: ",tn)
print("False Positives: ",fp)
print("False Negatives: ",fn)
print("True Positives: ",tp)



FP_predicts_indexes = [] 
TP_predicts_indexes=[]
FN_predict_indexes =[]
TN_predicts_indexes  = []
for index, row in df_pred.iterrows():
    if row['y_test'] == 0 and row['y_pred'] == 1:
        FP_predicts_indexes.append(row.name)
    elif row['y_test'] == 1 and row['y_pred'] == 1:
        TP_predicts_indexes.append(row.name)
    elif row['y_test'] == 0 and row['y_pred'] == 0:
        TN_predicts_indexes.append(row.name)
    elif row['y_test'] == 1 and row['y_pred'] == 0:
        FN_predict_indexes.append(row.name) 


df_pred.loc[TN_predicts_indexes,"prediction_result"] = "TN"
df_pred.loc[TP_predicts_indexes,"prediction_result"] = "TP"
df_pred.loc[FP_predicts_indexes,"prediction_result"] = "FP"
df_pred.loc[FN_predict_indexes,"prediction_result"] = "FN"
df_pred.head()


df_pred[df_pred["prediction_result"] == "FP"].head()

df_pred[df_pred["prediction_result"] == "FN"].head()

'''

srp_exp5a = '''
import pandas as pd
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
%matplotlib inline
np.random.seed(2)
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, mean_squared_error
import itertools

from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
from keras.models import *
from keras.layers import *
from keras.optimizers import RMSprop, Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.applications import vgg16, inception_v3, resnet50
from tensorflow.keras import backend
sns.set(style='white', context='notebook', palette='deep')
def add_one_to_one_correlation_line(ax, min_factor=1, max_factor=1, **plot_kwargs):
    lim_min, lim_max = pd.DataFrame([ax.get_ylim(), ax.get_xlim()]).agg({0: 'min', 1: 'max'})
    lim_min *= min_factor
    lim_max *= max_factor
    plot_kwargs_internal = dict(color='grey', ls='--')
    plot_kwargs_internal.update(plot_kwargs)
    ax.plot([lim_min, lim_max], [lim_min, lim_max], **plot_kwargs_internal)
    ax.set_ylim([lim_min, lim_max])
    ax.set_xlim([lim_min, lim_max])
# Load the data
df = pd.read_csv("../input/crowd-counting/labels.csv")
# Map each id to its appropriate file name
df['image_name'] = df['id'].map('seq_{:06d}.jpg'.format)
df.describe()
df['count'].hist(bins=30);
# Setup some constants
size = 224
batch_size = 64
# ImageDataGenerator - with defined augmentaions
datagen = ImageDataGenerator(
    rescale=1./255,  # Rescale the pixels to [0,1]. This seems to work well with pretrained models.
    featurewise_center=False,  # set input mean to 0 over the dataset
    samplewise_center=False,  # set each sample mean to 0
    featurewise_std_normalization=False,  # divide inputs by std of the dataset
    samplewise_std_normalization=False,  # divide each input by its std
    zca_whitening=False,  # apply ZCA whitening
#     rotation_range=20,  # randomly rotate images in the range (degrees, 0 to 180)
#     zoom_range = 0.2, # Randomly zoom image 
#     width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
#     height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
    horizontal_flip=False,  # randomly flip images
    vertical_flip=False,
    validation_split=0.2,  # 20% of data randomly assigned to validation
    # This one is important:
    preprocessing_function=resnet50.preprocess_input,  # Whenever working with a pretrained model, it is said to be essential to use its provided preprocess
)
flow_params = dict(
    dataframe=df,
    directory='../input/crowd-counting/frames/frames',
    x_col="image_name",
    y_col="count",
    weight_col=None,
    target_size=(size, size),
    color_mode='rgb',
    class_mode="raw",
    batch_size=batch_size,
    shuffle=True,
    seed=0,
)
# The dataset is split to training and validation sets at this point
train_generator = datagen.flow_from_dataframe(
    subset='training',
    **flow_params    
)
valid_generator = datagen.flow_from_dataframe(
    subset='validation',
    **flow_params
)
batch = next(train_generator)
fig, axes = plt.subplots(4, 4, figsize=(14, 14))
axes = axes.flatten()
for i in range(16):
    ax = axes[i]
    ax.imshow(batch[0][i])
    ax.axis('off')
    ax.set_title(batch[1][i])
plt.tight_layout()
plt.show()
base_model = resnet50.ResNet50(
    weights='imagenet',  # Load the pretrained weights, trained on the ImageNet dataset.
    include_top=False,  # We don't include the fully-connected layer at the top of the network - we need to modify the top.
    input_shape=(size, size, 3),  # 224x224 was the original size ResNet was trained on, so I decided to use this.
    pooling='avg',  # A global average pooling layer will be added after the last convolutional block.
)
# base_model.summary()
# Here we change the top (the last parts) of the network.
x = base_model.output  # Since we used pooling='avg', the output is of the pooling layer
x = Dense(1024, activation='relu')(x)  # We add a single fully-connected layer
predictions = Dense(1, activation='linear')(x)  # This is the new output layer - notice only 1 output, this will correspond to the number of people in the image
model = Model(inputs=base_model.input, outputs=predictions)
k = -7
for layer in model.layers[:k]:
    layer.trainable = False
print('Trainable:')
for layer in model.layers[k:]:
    print(layer.name)
    layer.trainable = True
model.summary()
# Define the optimizer - this function will iteratively improve parameters in order to minimise the loss. 
# The Adam optimization algorithm is an extension to stochastic gradient descent, which is usually more effective and fast.
optimizer = Adam(
    # The most important parameter is the learning rate - controls the amount that the weights are updated during eache round of training.
    learning_rate=0.001,
    # Additional parameters to play with:
#     beta_1=0.9,
#     beta_2=0.999,
#     epsilon=1e-07,
)
# Compile the model
model.compile(
    optimizer=optimizer, 
    loss="mean_squared_error",  # This is a classic regression score - the lower the better
    metrics=['mean_absolute_error', 'mean_squared_error']
)
# Set a learning rate annealer - to have a decreasing learning rate during the training to reach efficiently the global minimum of the loss function. 
# The LR is decreased dynamically when the score is not improved. This keeps the advantage of the fast computation time with a high LR at the start.
learning_rate_reduction = ReduceLROnPlateau(
    monitor='val_mean_squared_error',  # Track the score on the validation set
    patience=3,  # Number of epochs in which no improvement is seen.
    verbose=1, 
    factor=0.2,  # Factor by which the LR is multiplied.
    min_lr=0.000001  # Don't go below this value for LR.
)
# Fit the model
history = model.fit_generator(
    generator=train_generator,
    epochs=50,  # 50 epochs seems to have reached the minimal loss for this setup
    validation_data=valid_generator,
    verbose=2, 
    callbacks=[learning_rate_reduction],
)
print('\nDone.')
# Plot the loss and accuracy curves for training and validation 
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.plot(history.history['loss'], color='b', label="Training loss")
ax.plot(history.history['val_loss'], color='r', label="Validation loss",axes =ax)
ax.set_ylim(top=np.max(history.history['val_loss'])*1.2, bottom=0)
legend = ax.legend(loc='best', shadow=True)
# Predict on entire validation set, to be able to review the predictions manually
valid_generator.reset()
all_labels = []
all_pred = []
for i in range(len(valid_generator)):
    x = next(valid_generator)
    pred_i = model.predict(x[0])[:,0]
    labels_i = x[1]
    all_labels.append(labels_i)
    all_pred.append(pred_i)
#     print(np.shape(pred_i), np.shape(labels_i))
cat_labels = np.concatenate(all_labels)
cat_pred = np.concatenate(all_pred)
df_predictions = pd.DataFrame({'True values': cat_labels, 'Predicted values': cat_pred})
ax = df_predictions.plot.scatter('True values', 'Predicted values', alpha=0.5, s=14, figsize=(9,9))
ax.grid(axis='both')
add_one_to_one_correlation_line(ax)
ax.set_title('Validation')
plt.show()
mse = mean_squared_error(*df_predictions.T.values)
pearson_r = sc.stats.pearsonr(*df_predictions.T.values)[0]

print(f'MSE: {mse:.1f}\nPearson r: {pearson_r:.1f}')

'''


srp_exp5b = '''
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1./255,
                                      zoom_range=0.2,
                                      width_shift_range=0.2,
                                      height_shift_range=0.2,
                                      validation_split=0.2
                                      )
train_data = datagen.flow_from_directory('../input/diabetic-retinopathy-224x224-gaussian-filtered/gaussian_filtered_images/gaussian_filtered_images',
                                                     target_size=(224,224),
                                                     batch_size=32,
                                                     class_mode = 'categorical',
                                                     subset = 'training')

valid_data = datagen.flow_from_directory('../input/diabetic-retinopathy-224x224-gaussian-filtered/gaussian_filtered_images/gaussian_filtered_images',
                                                     target_size=(224,224),
                                                     batch_size=32,
                                                     class_mode = 'categorical',
                                                     subset = 'validation')

!pip install -q efficientnet

import efficientnet.tfkeras as efn

def lr_rate(epoch,lr):
    if epoch<10:
        lr=0.0001
        return lr
    elif epoch<=15:
        lr=0.0005
        return lr
    elif epoch<=30:
        lr=0.0001
        return lr
    else:
        lr=lr*(epoch/(1+epoch))
        return lr
lr_callback=tf.keras.callbacks.LearningRateScheduler(lr_rate)
model = tf.keras.Sequential([
        efn.EfficientNetB0(
            input_shape=(224,224, 3),
            weights='imagenet',
            include_top=False
        ),tf.keras.layers.Flatten(),tf.keras.layers.Dense(5, activation='softmax')
    ])
    
model.compile(optimizer="Adam",loss='categorical_crossentropy',metrics=['acc'])


history=model.fit_generator(train_data,validation_data = valid_data,callbacks=[lr_callback],epochs=40,verbose=1)

import matplotlib.pyplot as plt

def display_training_curves(training, validation, title, subplot):
    
    if subplot%10==1: # set up the subplots on the first call
        plt.subplots(figsize=(10,10), facecolor='#F0F0F0')
        plt.tight_layout()
    ax = plt.subplot(subplot)
    ax.set_facecolor('#F8F8F8')
    ax.plot(training)
    ax.plot(validation)
    ax.set_title('model '+ title)
    ax.set_ylabel(title)
    #ax.set_ylim(0.28,1.05)
    ax.set_xlabel('epoch')
    ax.legend(['train', 'valid.'])

display_training_curves(
    history.history['loss'], 
    history.history['val_loss'], 
    'loss', 211)
display_training_curves(
    history.history['acc'], 
    history.history['val_acc'], 
    'accuracy', 212)
'''


srp_exp6a = '''
import os
import re
import smtplib
from email.mime.text import MIMEText

# Define suspicious activity patterns
suspicious_patterns = [
    r"Unauthorized access attempt",
    r"Excessive failed login attempts",
    # Add more patterns as needed
]

def collect_system_data():
    # Implement data collection logic here
    log_entries = []
    command = 'wevtutil qe Security /q:"*[System[(EventID=4624 or EventID=4625)]]"'
    output = os.popen(command).read()
    log_entries = output.split('\n')
    print(log_entries)
    return log_entries

# Analyze system data for suspicious activities
def analyze_system_data(log_entries):
    suspicious_activities = []
    for entry in log_entries:
        for pattern in suspicious_patterns:
            if re.search(pattern, entry):
                suspicious_activities.append(entry)
                break
    return suspicious_activities

# Send email alert
def send_email_alert(suspicious_activities):
    from_address = 'your_email@example.com'
    to_address = 'recipient@example.com'
    subject = 'Suspicious Activities Detected'
    body = '\n'.join(suspicious_activities)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    # Configure your SMTP server and credentials
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    username = 'your_email@example.com'
    password = 'your_password'

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        print("Email alert sent successfully.")
    except Exception as e:
        print("Failed to send email alert:", str(e))

# Main program execution
if __name__ == "__main__":
    # Collect system data
    system_data = collect_system_data()

    # Analyze system data for suspicious activities
    suspicious_activities = analyze_system_data(system_data)

    if suspicious_activities:
        # Send email alert
        send_email_alert(suspicious_activities)
    else:
        print("No suspicious activities found.")

'''

srp_exp6b = '''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import confusion_matrix, recall_score, f1_score, precision_score
from pandas import DataFrame
# Building a function that performs full partitioning
def train_val_test_split(df, rstate=42, shuffle=True, stratify=None):
    strat = df[stratify] if stratify else None
    train_set, test_set = train_test_split(
        df, test_size=0.4, random_state=rstate, shuffle=shuffle, stratify=strat)
    strat = test_set[stratify] if stratify else None
    val_set, test_set = train_test_split(
        test_set, test_size=0.5, random_state=rstate, shuffle=shuffle, stratify=strat)
    return (train_set, val_set, test_set)
def remove_labels(df, label_name):
    X = df.drop(label_name, axis=1)
    y = df[label_name].copy()
    return (X, y)
def evaluate_result(y_pred, y, y_prep_pred, y_prep, metric):
    print(metric.__name__, "WITHOUT preparation:", metric(y_pred, y, average='weighted'))
    print(metric.__name__, "WITH preparation:", metric(y_prep_pred, y_prep, average='weighted'))
df = pd.read_csv('TotalFeatures-ISCXFlowMeter.csv')
df.head(10)
df.info()
df['calss'].value_counts()
# We copy the data set and transform the output variable to numeric to calculate correlations
X = df.copy()
X['calss'] = X['calss'].factorize()[0]
# Calculate Correlations
corr_matrix = X.corr()
corr_matrix["calss"].sort_values(ascending=False)
X.corr()
# It is possible to value staying with those that have the highest correlation
corr_matrix[corr_matrix["calss"] > 0.05]
# Now dividing the dataset
train_set, val_set, test_set = train_val_test_split(X)
X_train, y_train = remove_labels(train_set, 'calss')
X_val, y_val = remove_labels(val_set, 'calss')
X_test, y_test = remove_labels(test_set, 'calss')
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
scaler = RobustScaler()
X_test_scaled = scaler.fit_transform(X_test)
scaler = RobustScaler()
X_val_scaled = scaler.fit_transform(X_val)
# Transformación a un DataFrame de Pandas
X_train_scaled = DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
X_train_scaled.head(10)
X_train_scaled.describe()
from sklearn.tree import DecisionTreeClassifier

MAX_DEPTH = 20

# Model trained with the unscaled data set
clf_tree = DecisionTreeClassifier(max_depth=MAX_DEPTH, random_state=42)
clf_tree.fit(X_train, y_train)
# Model trained with the scaled dataset
clf_tree_scaled = DecisionTreeClassifier(max_depth=MAX_DEPTH, random_state=42)
clf_tree_scaled.fit(X_train_scaled, y_train)
# We predict with the training data set
y_train_pred = clf_tree.predict(X_train)
y_train_prep_pred = clf_tree_scaled.predict(X_train_scaled)
# We compare results between scaled and unscaled
evaluate_result(y_train_pred, y_train, y_train_prep_pred, y_train, f1_score)
# We predict with the validation data set
y_pred = clf_tree.predict(X_val)
y_prep_pred = clf_tree_scaled.predict(X_val_scaled)
# We compare results between scaled and unscaled
evaluate_result(y_pred, y_val, y_prep_pred, y_val, f1_score)
# We reduce the number of attributes in the dataset to better visualize it
X_train_reduced = X_train[['min_flowpktl', 'flow_fin']]
# We generate a model with the reduced data set
clf_tree_reduced = DecisionTreeClassifier(max_depth=2, random_state=42)
clf_tree_reduced.fit(X_train_reduced, y_train)
# We graphically represent the constructed decision limit
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
%matplotlib inline

def plot_decision_boundary(clf, X, y, plot_training=True, resolution=1000):
    mins = X.min(axis=0) - 1
    maxs = X.max(axis=0) + 1
    x1, x2 = np.meshgrid(np.linspace(mins[0], maxs[0], resolution),
                         np.linspace(mins[1], maxs[1], resolution))
    X_new = np.c_[x1.ravel(), x2.ravel()]
    y_pred = clf.predict(X_new).reshape(x1.shape)
    custom_cmap = ListedColormap(['#fafab0','#9898ff','#a0faa0'])
    plt.contourf(x1, x2, y_pred, alpha=0.3, cmap=custom_cmap)
    custom_cmap2 = ListedColormap(['#7d7d58','#4c4c7f','#507d50'])
    plt.contour(x1, x2, y_pred, cmap=custom_cmap2, alpha=0.8)
    if plot_training:
        plt.plot(X[:, 0][y==0], X[:, 1][y==0], "yo", label="normal")
        plt.plot(X[:, 0][y==1], X[:, 1][y==1], "bs", label="adware")
        plt.plot(X[:, 0][y==2], X[:, 1][y==2], "g^", label="malware")
        plt.axis([mins[0], maxs[0], mins[1], maxs[1]])               
    plt.xlabel('min_flowpktl', fontsize=14)
    plt.ylabel('flow_fin', fontsize=14, rotation=90)

plt.figure(figsize=(12, 6))
plot_decision_boundary(clf_tree_reduced, X_train_reduced.values, y_train)
plt.show()
# We paint the tree to compare it with the previous graphic representation
from graphviz import Source
srp_from sklearn.tree import export_graphviz
import os

srp_export_graphviz(
        clf_tree_reduced,
        out_file="android_malware.dot",
        feature_names=X_train_reduced.columns,
        class_names=["benign", "adware", "malware"],
        rounded=True,
        filled=True
    )

Source.from_file("android_malware.dot")

'''

srp_exp7a = '''
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
import os
from distutils.dir_util import copy_tree, remove_tree
from PIL import Image
from random import randint
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import matthews_corrcoef as MCC
from sklearn.metrics import balanced_accuracy_score as BAS
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow_addons as tfa
from keras.utils.vis_utils import plot_model
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import Conv2D, Flatten
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.preprocessing.image import ImageDataGenerator as IDG
from tensorflow.keras.layers import SeparableConv2D, BatchNormalization, MaxPool2D
base_dir = "Alzheimer_s Dataset/"
root_dir = "./"
test_dir = base_dir + "test/"
train_dir = base_dir + "train/"
work_dir = root_dir + "dataset/"
if os.path.exists(work_dir):
    remove_tree(work_dir)
os.mkdir(work_dir)
copy_tree(train_dir, work_dir)
copy_tree(test_dir, work_dir)
print("Working Directory Contents:", os.listdir(work_dir))
WORK_DIR = './dataset/'
CLASSES = [ 'NonDemented',
            'VeryMildDemented',
            'MildDemented',
            'ModerateDemented']
IMG_SIZE = 176
IMAGE_SIZE = [176, 176]
DIM = (IMG_SIZE, IMG_SIZE)
ZOOM = [.99, 1.01]
BRIGHT_RANGE = [0.8, 1.2]
HORZ_FLIP = True
FILL_MODE = "constant"
DATA_FORMAT = "channels_last"
work_dr = IDG(rescale = 1./255, brightness_range=BRIGHT_RANGE, zoom_range=ZOOM, data_format=DATA_FORMAT, fill_mode=FILL_MODE, horizontal_flip=HORZ_FLIP)
train_data_gen = work_dr.flow_from_directory(directory=WORK_DIR, target_size=DIM, batch_size=6500, shuffle=False)
train_data, train_labels = train_data_gen.next()
sm = SMOTE(random_state=42)
train_data, train_labels = sm.fit_resample(train_data.reshape(-1, IMG_SIZE * IMG_SIZE * 3), train_labels)
train_data = train_data.reshape(-1, IMG_SIZE, IMG_SIZE, 3)
train_data, test_data, train_labels, test_labels = train_test_split(train_data, train_labels, test_size = 0.2, random_state=42)
train_data, val_data, train_labels, val_labels = train_test_split(train_data, train_labels, test_size = 0.2, random_state=42)
def conv_block(filters, act='relu'):
    block = Sequential()
    block.add(Conv2D(filters, 3, activation=act, padding='same'))
    block.add(Conv2D(filters, 3, activation=act, padding='same'))
    block.add(BatchNormalization())
    block.add(MaxPool2D())
    return block
def dense_block(units, dropout_rate, act='relu'):    
    block = Sequential()
    block.add(Dense(units, activation=act))
    block.add(BatchNormalization())
    block.add(Dropout(dropout_rate))
    return block
def construct_model(act='relu'):
    model = Sequential([
        Input(shape=(*IMAGE_SIZE, 3)),
        Conv2D(16, 3, activation=act, padding='same'),
        Conv2D(16, 3, activation=act, padding='same'),
        MaxPool2D(),
        conv_block(32),
        conv_block(64),
        conv_block(128),
        Dropout(0.2),
        conv_block(256),
        Dropout(0.2),
        Flatten(),
        dense_block(512, 0.7),
        dense_block(128, 0.5),
        dense_block(64, 0.3),
        Dense(4, activation='softmax')        
    ], name = "cnn_model")
    return model
class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('val_acc') > 0.99:
            print("\nReached accuracy threshold! Terminating training.")
            self.model.stop_training = True
my_callback = MyCallback()
early_stopping = EarlyStopping(monitor='val_loss', patience=2)
model = construct_model()
METRICS = [tf.keras.metrics.CategoricalAccuracy(name='acc'),
           tf.keras.metrics.AUC(name='auc'), 
           tfa.metrics.F1Score(num_classes=4)]
CALLBACKS = [my_callback] 
model.compile(optimizer='adam',
              loss=tf.losses.CategoricalCrossentropy(),
              metrics=METRICS)
history = model.fit(train_data, train_labels, validation_data=(val_data, val_labels), callbacks=CALLBACKS, epochs=EPOCHS)
test_scores = model.evaluate(test_data, test_labels)
pred_labels = model.predict(test_data)
def roundoff(arr):
    arr[np.argwhere(arr != arr.max())] = 0
    arr[np.argwhere(arr == arr.max())] = 1
    return arr
for labels in pred_labels:
    labels = roundoff(labels)
pred_ls = np.argmax(pred_labels, axis=1)
test_ls = np.argmax(test_labels, axis=1)
conf_arr = confusion_matrix(test_ls, pred_ls)
print("Balanced Accuracy Score: {} %".format(round(BAS(test_ls, pred_ls) * 100, 2)))
print("Matthew's Correlation Coefficient: {} %".format(
    round(MCC(test_ls, pred_ls) * 100, 2)))'''


srp_exp7b = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')
import sklearn.neighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
df = pd.read_csv('../input/heart-disease prediction/Heart_Disease_Prediction.csv')
df.head()
df.describe()
df.shape()
df.isnull().values.any()
df[‘sex’].value_counts()
df[‘Heart Disease’].value_counts()
sns.countplot(x=’Heart Disease’,data=df)
df.corr()
#K-nearest neighbours
x=df.iloc[:,:-2]
y=df.iloc[:,-1]
x_train,x_test,y_train,y_test=train_test_split(x,y, random_state=0,test_size=0.35)
sc_x=StandardScaler()
x_train = sc_x.fit_transform(x_train)
x_test = sc_x.ransform(x_test)
import math
math.sqrt(len(y_test))
classifier = KNeighborsClassifier(n_neighbors = 9, p = 2, metric = 'euclidean')
classifier.fit(x_train,y_train)
y_pred=classifier.predict(x_test)
y_pred
cm=confusion_matrix(y_test,y_pred)
print(cm)
knn_acc_score=accuracy_score(y_test,y_pred)
print("Accuracy of KNN:",knn_acc_score*100)


#SVM
from sklearn import svm
clf = svm.SVC(kernel='rbf')
clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)
y_pred=clf.predict(x_test)
y_pred
cm=confusion_matrix(y_test,y_pred)
print(cm)
svm_acc_score=accuracy_score(y_test,y_pred)
print("Accuracy of SVM:",svm_acc_score*100)

#Random Forest Model
rf = RandomForestClassifier(n_estimators=500, random_state=12, max_depth=5)
rf.fit(x_train,y_train)
rf_predicted = rf.predict(x_test)
rf_conf_matrix = confusion_matrix(y_test, rf_predicted)
print("confusion matrix")
print(rf_conf_matrix)
rf_acc_score = accuracy_score(y_test, rf_predicted)
print("Accuracy of Random Forest:",rf_acc_score*100)

'''


srp_exp8 = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("zomato.csv")
df.head()
df.isnull().sum()
df.info()

# Preprocessing

df=df.drop(columns=['url','phone','address','name','location','rest_type','dish_liked','cuisines',
'reviews_list','menu_item','listed_in(city)'],axis=1)
df['online_order'].unique()
df['book_table'].unique()
df['listed_in(type)'].unique()
df['online_order'] = df['online_order'].map({'Yes':1, 'No':0})
df['book_table'] = df['book_table'].map({'Yes':1, 'No':0})
df['listed_in(type)'] = df['listed_in(type)'].map({'Buffet':0, 'Cafes':1, 'Delivery':2, 'Desserts':3, 'Dine-out':4,'Drinks & nightlife':5, 'Pubs and bars':6})
df.isnull().sum()
df['rate']
df['rate'].unique()
df[df['rate']=='-'].count()
df = df[(df['rate'] != 'NEW') & (df['rate'] != '-')]
df.shape
df.isnull().sum()

# Cleaning Ratings

df['rate'] = df['rate'].str.strip()  # Remove extra spaces from the string
srp_df['rate'] = df['rate'].str.split('/', expand=True)[0].astype(float)
df['rate'].unique()
df['approx_cost(for two people)'].unique()
df['approx_cost(for two people)'].dtype
df['approx_cost(for two people)'] = df['approx_cost(for two people)'].str.replace(",","")
# Convert the column to the integer data type
df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(float).astype(float)

df.isnull().sum()
df_mean = df.copy()
df_mode = df.copy()
df_knn = df.copy()
df_mean.isnull().sum()

# Approach 1: Handling missing values using Mean

mean_rate = df_mean['rate'].mean()
mean_rate
df_mean['rate'] = df_mean['rate'].fillna(mean_rate)
df_mean['rate']

mean_cost = df_mean['approx_cost(for two people)'].mean()
mean_cost

df_mean['approx_cost(for two people)'] = df_mean['approx_cost(for two people)'].fillna(mean_cost)
df_mean['approx_cost(for two people)']

# Approach 2: Handling missing values using Mode

mode_rate = df_mode['rate'].mode()[0]
mode_rate

df_mode['rate'].unique()
df_mode['rate'] = df_mode['rate'].fillna(mode_rate)
df_mode['rate']

mode_cost = df_mode['approx_cost(for two people)'].mode()[0]
mode_cost

df_mode['approx_cost(for two people)'] = df_mode['approx_cost(for two people)'].fillna(mode_cost)
df_mode['approx_cost(for two people)']
df_mode.isnull().sum()

# Approach 3 : Handling missing values using KNN Imputer

from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=2)
df_knn = imputer.fit_transform(df_knn)
df_knn
df_KNN = pd.DataFrame(data=df_knn,columns=df_mean.columns)
df_KNN.tail()
df_mean.tail()
df_mode.tail()

# Linear Regression

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

x = df_KNN.drop(columns=['rate'],axis=1)
y = df_KNN['rate']
X_train,X_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=0)
model = LinearRegression()
model.fit(X_train,y_train)
y_pred = model.predict(X_test)

MAE = mean_absolute_error(y_test,y_pred)
MSE = mean_squared_error(y_test, y_pred)
print(MAE)
print(MSE)

# Random forest regressor

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X_train,y_train)
y_pred = model.predict(X_test)
print(y_pred)
accuracy = model.score(X_test,y_test)
print(accuracy*100)

# Decision Tree Regressor

from sklearn.tree import DecisionTreeRegressor
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(y_pred)
accuracy = model.score(X_test,y_test)
print(accuracy*100)

# Gradient Boosting Regressor

from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(y_pred)
accuracy = model.score(X_test,y_test)
print(accuracy*100

'''

srp_exp9 = '''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import nltk

nltk.download('stopwords')
nltk.download('punkt')

# Load the Amazon dataset
data = pd.read_csv('/content/Reddit_Data.csv')

# Preprocessing
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess(text):
    if isinstance(text, str):  # Check if the text is a string
        tokens = word_tokenize(text.lower())
        tokens = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
        return ' '.join(tokens)
    else:
        return ''

data['processed_text'] = data['text'].apply(preprocess)

# Filter out rows with empty processed_text
data = data[data['processed_text'] != '']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['processed_text'], data['sentiment'], test_size=0.2, random_state=42)

# Feature extraction
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train the classifier 1
classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)
# Predict sentiment on test data
predictions = classifier.predict(X_test_vectorized)
# Evaluate the classifier
accuracy = (predictions == y_test).mean()
print('Accuracy:', accuracy*100)

# Train the classifier 2
classifier = SVC(kernel='linear')
classifier.fit(X_train_vectorized, y_train)
# Predict sentiment on test data
predictions = classifier.predict(X_test_vectorized)
# Evaluate the classifier
accuracy = (predictions == y_test).mean()
print('Accuracy:', accuracy)

'''


exp1 = bbn = '''# for creating Bayesian Belief Networks (BBN)
import pandas as pd
from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController
# the guest's intitial door selection is completely random
guest = BbnNode(Variable(0, 'guest', ['A', 'B', 'C']), [1.0/3, 1.0/3, 1.0/3])
# the door the prize is behind is also completely random
prize = BbnNode(Variable(1, 'prize', ['A', 'B', 'C']), [1.0/3, 1.0/3, 1.0/3])
# monty is dependent on both guest and prize
monty = BbnNode(Variable(2, 'monty', ['A', 'B', 'C']), [0, 0.5, 0.5,  # A, A
                                                        0, 0, 1,  # A, B
                                                        0, 1, 0,  # A, C
                                                        0, 0, 1,  # B, A
                                                        0.5, 0, 0.5,  # B, B
                                                        1, 0, 0,  # B, C
                                                        0, 1, 0,  # C, A
                                                        1, 0, 0,  # C, B
                                                        0.5, 0.5, 0  # C, C
                                                        ])

bbn = Bbn() \
    .add_node(guest) \
    .add_node(prize) \
    .add_node(monty) \
    .add_edge(Edge(guest, monty, EdgeType.DIRECTED)) \
    .add_edge(Edge(prize, monty, EdgeType.DIRECTED))

# Convert the BBN to a join tree
join_tree = InferenceController.apply(bbn)

# Define a function for printing marginal probabilities


def print_probs():
    for node in join_tree.get_bbn_nodes():
        potential = join_tree.get_bbn_potential(node)
        print("Node:", node)
        print("Values:")
        print(potential)
        print('----------------')


print_probs()
'''

exp2 = apprx = '''# Approx Inference
from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController

# create the nodes
a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
d = BbnNode(Variable(3, 'd', ['on', 'off']), [0.9, 0.1, 0.5, 0.5])
e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.3, 0.7, 0.6, 0.4])
f = BbnNode(Variable(5, 'f', ['on', 'off']), [
            0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.99, 0.01])
g = BbnNode(Variable(6, 'g', ['on', 'off']), [0.8, 0.2, 0.1, 0.9])
h = BbnNode(Variable(7, 'h', ['on', 'off']), [
            0.05, 0.95, 0.95, 0.05, 0.95, 0.05, 0.95, 0.05])

# create the network structure
bbn = Bbn() \
    .add_node(a) \
    .add_node(b) \
    .add_node(c) \
    .add_node(d) \
    .add_node(e) \
    .add_node(f) \
    .add_node(g) \
    .add_node(h) \
    .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
    .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
    .add_edge(Edge(b, d, EdgeType.DIRECTED)) \
    .add_edge(Edge(c, e, EdgeType.DIRECTED)) \
    .add_edge(Edge(d, f, EdgeType.DIRECTED)) \
    .add_edge(Edge(e, f, EdgeType.DIRECTED)) \
    .add_edge(Edge(c, g, EdgeType.DIRECTED)) \
    .add_edge(Edge(e, h, EdgeType.DIRECTED)) \
    .add_edge(Edge(g, h, EdgeType.DIRECTED))

# convert the BBN to a join tree
join_tree = InferenceController.apply(bbn)

# insert an observation evidence
ev = EvidenceBuilder() \
    .with_node(join_tree.get_bbn_node_by_name('a')) \
    .with_evidence('on', 1.0) \
    .build()
join_tree.set_observation(ev)

# print the posterior probabilities
for node, posteriors in join_tree.get_posteriors().items():
    p = ', '.join([f'{val}={prob:.5f}' for val, prob in posteriors.items()])
    print(f'{node} : {p}')
'''

exp3 = bayes = '''# bayes Params
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from bayes_opt import BayesianOptimization, UtilityFunction
import warnings
warnings.filterwarnings("ignore")

# Prepare the data.
cancer = load_breast_cancer()
X = cancer["data"]
y = cancer["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    stratify=y,
                                                    random_state=42)
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
# Define the black box function to optimize.


def black_box_function(C):
    # C: SVC hyper parameter to optimize for.
    model = SVC(C=C)
    model.fit(X_train_scaled, y_train)
    y_score = model.decision_function(X_test_scaled)
    f = roc_auc_score(y_test, y_score)
    return f


# Set range of C to optimize for.
# bayes_opt requires this to be a dictionary.
pbounds = {"C": [0.1, 10]}
# Create a BayesianOptimization optimizer,
# and optimize the given black_box_function.
optimizer = BayesianOptimization(f=black_box_function,
                                 pbounds=pbounds, verbose=2,
                                 random_state=4)
optimizer.maximize(init_points=5, n_iter=10)
print("Best result: {}; f(x) = {}.".format(
    optimizer.max["params"], optimizer.max["target"]))

'''

exp4 = hmm = '''# hmm
import numpy as np
import pandas as pd


class ProbabilityVector:
    def __init__(self, probabilities: dict):
        states = probabilities.keys()
        probs = probabilities.values()

        assert len(states) == len(
            probs), "The probabilities must match the states."
        assert len(states) == len(set(states)), "The states must be unique."
        assert abs(sum(probs) - 1.0) < 1e-12, "Probabilities must sum up to 1."
        assert len(list(filter(lambda x: 0 <= x <= 1, probs))) == len(probs), \
            "Probabilities must be numbers from [0, 1] interval."

        self.states = sorted(probabilities)
        self.values = np.array(list(map(lambda x:
                                        probabilities[x], self.states))).reshape(1, -1)

    @classmethod
    def initialize(cls, states: list):
        size = len(states)
        rand = np.random.rand(size) / (size**2) + 1 / size
        rand /= rand.sum(axis=0)
        return cls(dict(zip(states, rand)))

    # @classmethod
    # def from_numpy(cls, array: np.ndarray, state: list):
    #     return cls(dict(zip(states, list(array))))

    @property
    def dict(self):
        return {k: v for k, v in zip(self.states, list(self.values.flatten()))}

    @property
    def df(self):
        return pd.DataFrame(self.values, columns=self.states, index=['probability'])

    def __repr__(self):
        return "P({}) = {}.".format(self.states, self.values)

    def __eq__(self, other):
        if not isinstance(other, ProbabilityVector):
            raise NotImplementedError
        if (self.states == other.states) and (self.values == other.values).all():
            return True
        return False

    def __getitem__(self, state: str) -> float:
        if state not in self.states:
            raise ValueError(
                "Requesting unknown probability state from vector.")
        index = self.states.index(state)
        return float(self.values[0, index])

    def __mul__(self, other) -> np.ndarray:
        if isinstance(other, ProbabilityVector):
            return self.values * other.values
        elif isinstance(other, (int, float)):
            return self.values * other
        else:
            NotImplementedError

    def __rmul__(self, other) -> np.ndarray:
        return self.__mul__(other)

    def __matmul__(self, other) -> np.ndarray:
        if isinstance(other, ProbabilityMatrix):
            return self.values @ other.values

    def __truediv__(self, number) -> np.ndarray:
        if not isinstance(number, (int, float)):
            raise NotImplementedError
        x = self.values
        return x / number if number != 0 else x / (number + 1e-12)

    def argmax(self):
        index = self.values.argmax()
        return self.states[index]


class ProbabilityMatrix:
    def __init__(self, prob_vec_dict: dict):

        assert len(prob_vec_dict) > 1, \
            "The numebr of input probability vector must be greater than one."
        assert len(set([str(x.states) for x in prob_vec_dict.values()])) == 1, \
            "All internal states of all the vectors must be indentical."
        assert len(prob_vec_dict.keys()) == len(set(prob_vec_dict.keys())), \
            "All observables must be unique."

        self.states = sorted(prob_vec_dict)
        self.observables = prob_vec_dict[self.states[0]].states
        self.values = np.stack([prob_vec_dict[x].values
                                for x in self.states]).squeeze()

    @classmethod
    def initialize(cls, states: list, observables: list):
        size = len(states)
        rand = np.random.rand(size, len(observables)) \
            / (size**2) + 1 / size
        rand /= rand.sum(axis=1).reshape(-1, 1)
        aggr = [dict(zip(observables, rand[i, :])) for i in range(len(states))]
        pvec = [ProbabilityVector(x) for x in aggr]
        return cls(dict(zip(states, pvec)))

    @classmethod
    def from_numpy(cls, array:
                   np.ndarray,
                   states: list,
                   observables: list):
        p_vecs = [ProbabilityVector(dict(zip(observables, x)))
                  for x in array]
        return cls(dict(zip(states, p_vecs)))

    @property
    def dict(self):
        return self.df.to_dict()

    @property
    def df(self):
        return pd.DataFrame(self.values,
                            columns=self.observables, index=self.states)

    def __repr__(self):
        return "PM {} states: {} -> obs: {}.".format(
            self.values.shape, self.states, self.observables)

    def __getitem__(self, observable: str) -> np.ndarray:
        if observable not in self.observables:
            raise ValueError(
                "Requesting unknown probability observable from the matrix.")
        index = self.observables.index(observable)
        return self.values[:, index].reshape(-1, 1)


a1 = ProbabilityVector({'rain': 0.7, 'sun': 0.3})
a2 = ProbabilityVector({'sun': 0.1, 'rain': 0.9})
print(a1.df)
print(a2.df)

print("Comparison:", a1 == a2)
print("Element-wise multiplication:", a1 * a2)
print("Argmax:", a1.argmax())
print("Getitem:", a1['rain'])

'''

exp5 = em = '''# em

import numpy as np


# Note: X and mu are assumed to be column vector


def normPDF(x, mu, sigma):
    size = len(x)
    if size == len(mu) and (size, size) == sigma.shape:
        det = np.linalg.det(sigma)
        if det == 0:
            raise NameError("The covariance matrix can't be singular")
        norm_const = 1.0/(np.math.pow((2*np.pi), float(size)/2)
                          * np.math.pow(det, 1.0/2))
        x_mu = np.matrix(x - mu).T
        inv_ = np.linalg.inv(sigma)
        result = np.math.pow(np.math.e, -0.5 * (x_mu.T * inv_ * x_mu))
        return norm_const * result
    else:
        raise NameError("The dimensions of the input don't match")
        return -1


def initForwardBackward(X, K, d, N):
    # Initialize the state transition matrix, A. A is a KxK matrix where
    # element A_{jk} = p(Z_n = k | Z_{n-1} = j)
    # Therefore, the matrix will be row-wise normalized. IOW, Sum(Row) = 1
    # State transition probability is time independent.
    A = np.ones((K, K))
    A = A/np.sum(A, 1)[None].T

    # Initialize the marginal probability for the first hidden variable
    # It is a Kx1 vector
    PI = np.ones((K, 1))/K

    # Initialize Emission Probability. We assume Gaussian distribution
    # for emission. So we just need to keep the mean and covariance. These
    # parameters are different for different states.
    # Mu is dxK where kth column represents mu for kth state
    # SIGMA is a list of K matrices of shape dxd. Each element represent
    # covariance matrix for the corresponding state.
    # Given the current latent variable state, emission probability is
    # independent of time
    MU = np.random.rand(d, K)
    SIGMA = [np.eye(d) for i in range(K)]

    return A, PI, MU, SIGMA


def buildAlpha(X, PI, A, MU, SIGMA):
    # We build up Alpha here using dynamic programming. It is a KxN matrix
    # where the element ALPHA_{ij} represents the forward probability
    # for jth timestep (j = 1...N) and ith state. The columns of ALPHA are
    # normalized for preventing underflow problem as discussed in secion
    # 13.2.4 in Bishop's PRML book. So,sum(column) = 1
    # c_t is the normalizing costant
    N = np.size(X, 1)
    K = np.size(PI, 0)
    Alpha = np.zeros((K, N))
    c = np.zeros(N)

    # Base case: build the first column of ALPHA
    for i in range(K):
        Alpha[i, 0] = PI[i]*normPDF(X[:, 0], MU[:, i], SIGMA[i])
    c[0] = np.sum(Alpha[:, 0])
    Alpha[:, 0] = Alpha[:, 0]/c[0]

    # Build up the subsequent columns
    for t in range(1, N):
        for i in range(K):
            for j in range(K):
                Alpha[i, t] += Alpha[j, t-1]*A[j, i]  # sum part of recursion
            # product with emission prob
            Alpha[i, t] *= normPDF(X[:, t], MU[:, i], SIGMA[i])
        c[t] = np.sum(Alpha[:, t])
        Alpha[:, t] = Alpha[:, t]/c[t]   # for scaling factors
    return Alpha, c


def buildBeta(X, c, PI, A, MU, SIGMA):
    # Beta is KxN matrix where Beta_{ij} represents the backward probability
    # for jth timestamp and ith state. Columns of Beta are normalized using
    # the element of vector c.

    N = np.size(X, 1)
    K = np.size(PI, 0)
    Beta = np.zeros((K, N))

    # Base case: build the last column of Beta
    for i in range(K):
        Beta[i, N-1] = 1.

    # Build up the matrix backwards
    for t in range(N-2, -1, -1):
        for i in range(K):
            for j in range(K):
                Beta[i, t] += Beta[j, t+1]*A[i, j] * \
                    normPDF(X[:, t+1], MU[:, j], SIGMA[j])
        Beta[:, t] /= c[t+1]
    return Beta


def Estep(trainSet, PI, A, MU, SIGMA):
    # The goal of E step is to evaluate Gamma(Z_{n}) and Xi(Z_{n-1},Z_{n})
    # First, create the forward and backward probability matrices
    Alpha, c = buildAlpha(trainSet, PI, A, MU, SIGMA)
    Beta = buildBeta(trainSet, c, PI, A, MU, SIGMA)

    # Dimension of Gamma is equal to Alpha and Beta where nth column represents
    # posterior density of nth latent variable. Each row represents a state
    # value of all the latent variables. IOW, (i,j)th element represents
    # p(Z_j = i | X,MU,SIGMA)
    Gamma = Alpha*Beta

    # Xi is a KxKx(N-1) matrix (N is the length of data seq)
    # Xi(:,:,t) = Xi(Z_{t-1},Z_{t})
    N = np.size(trainSet, 1)
    K = np.size(PI, 0)
    Xi = np.zeros((K, K, N))
    for t in range(1, N):
        Xi[:, :, t] = (1/c[t])*Alpha[:, t-1][None].T.dot(Beta[:, t][None])*A
        # Now columnwise multiply the emission prob
        for col in range(K):
            Xi[:, col, t] *= normPDF(trainSet[:, t], MU[:, col], SIGMA[col])

    return Gamma, Xi, c


def Mstep(X, Gamma, Xi):
    # Goal of M step is to calculate PI, A, MU, and SIGMA while treating
    # Gamma and Xi as constant
    K = np.size(Gamma, 0)
    d = np.size(X, 0)

    PI = (Gamma[:, 0]/np.sum(Gamma[:, 0]))[None].T
    tempSum = np.sum(Xi[:, :, 1:], axis=2)
    A = tempSum/np.sum(tempSum, axis=1)[None].T

    MU = np.zeros((d, K))
    GamSUM = np.sum(Gamma, axis=1)[None].T
    SIGMA = []
    for k in range(K):
        MU[:, k] = np.sum(Gamma[k, :]*X, axis=1)/GamSUM[k]
        X_MU = X - MU[:, k][None].T
        SIGMA.append(X_MU.dot(((X_MU*(Gamma[k, :][None])).T))/GamSUM[k])

    return PI, A, MU, SIGMA


def main():
    # Reading the data file
    input_file = open('points.dat')
    lines = input_file.readlines()
    allData = np.array([line.strip().split()
                       for line in lines]).astype(np.float)
    (m, n) = np.shape(allData)

    # Separating out dev and train set
    devSet = allData[np.math.ceil(m*0.9):, 0:].T
    trainSet = allData[:np.math.floor(m*0.9), 0:].T

    # Setting up total number of clusters which will be fixed
    K = 3

    # Initialization: Build a state transition matrix with uniform probability
    A, PI, MU, SIGMA = initForwardBackward(trainSet, K, n, m)

    # Temporary variables. X, Y mesh for plotting
    nx = np.arange(-4.0, 4.0, 0.1)
    ny = np.arange(-4.0, 4.0, 0.1)
    ax, ay = np.meshgrid(nx, ny)

    iter = 0
    prevll = -999999
    while (True):
        iter = iter + 1
        # E-Step
        Gamma, Xi, c = Estep(trainSet, PI, A, MU, SIGMA)

        # M-Step
        PI, A, MU, SIGMA = Mstep(trainSet, Gamma, Xi)

        # Calculate log likelihood. We use the c vector for log likelihood because
        # it already gives us p(X_1^N)
        ll_train = np.sum(np.log(c))
        Gamma_dev, Xi_dev, c_dev = Estep(devSet, PI, A, MU, SIGMA)
        ll_dev = np.sum(np.log(c_dev))
        if (iter > 50 or (ll_train - prevll) < 0.05):
            break
        print(abs(ll_train - prevll))
        prevll = ll_train


if __name__ == '__main__':
    main()

'''

exp6 = realworld = '''# realworld
import numpy as np
import gym
import random


def main():

    # create Taxi environment
    env = gym.make('Taxi-v3')

    # initialize q-table
    state_size = env.observation_space.n
    action_size = env.action_space.n
    qtable = np.zeros((state_size, action_size))

    # hyperparameters
    learning_rate = 0.9
    discount_rate = 0.8
    epsilon = 1.0
    decay_rate = 0.005

    # training variables
    num_episodes = 1000
    max_steps = 99  # per episode

    # training
    for episode in range(num_episodes):

        # reset the environment
        state = env.reset()
        done = False

        for s in range(max_steps):

            # exploration-exploitation tradeoff
            if random.uniform(0, 1) < epsilon:
                # explore
                action = env.action_space.sample()
            else:
                # exploit
                action = np.argmax(qtable[state, :])

            # take action and observe reward
            new_state, reward, done, info = env.step(action)

            # Q-learning algorithm
            qtable[state, action] = qtable[state, action] + learning_rate * \
                (reward + discount_rate *
                 np.max(qtable[new_state, :])-qtable[state, action])

            # Update to our new state
            state = new_state

            # if done, finish episode
            if done == True:
                break

        # Decrease epsilon
        epsilon = np.exp(-decay_rate*episode)

    print(f"Training completed over {num_episodes} episodes")
    input("Press Enter to watch trained agent...")

    # watch trained agent
    state = env.reset()
    done = False
    rewards = 0

    for s in range(max_steps):

        print(f"TRAINED AGENT")
        print("Step {}".format(s+1))

        action = np.argmax(qtable[state, :])
        new_state, reward, done, info = env.step(action)
        rewards += reward
        env.render()
        print(f"score: {rewards}")
        state = new_state

        if done == True:
            break

    env.close()


if __name__ == "__main__":
    main()

'''

exp7 = reinforcement = '''# reinforcement learning
import numpy as np
import gym
import random
from IPython.display import Image
import os

env = gym.make("FrozenLake-v0")
env.render()

action_size = env.action_space.n
print('Action Size - ', action_size)

state_size = env.observation_space.n
print('State Size - ', state_size)

qtable = np.zeros((state_size, action_size))
# print(qtable)

tuning_params = [2500, 5000, 10000, 15000, 25000, 50000, 70000]

for param in tuning_params:

    total_episodes = param        # Total episodes
    total_test_episodes = 100     # Total test episodes
    max_steps = 99                # Max steps per episode

    learning_rate = 0.7           # Learning rate
    gamma = 0.8                 # Discounting rate

    # Exploration parameters
    epsilon = 1.0                 # Exploration rate
    max_epsilon = 1.0             # Exploration probability at start
    min_epsilon = 0.01            # Minimum exploration probability
    decay_rate = 0.01             # Exponential decay rate for exploration prob

    rewards = []
    avg_epsilon = []
    print('*************************  Q-Learning  ********************************')
    # 2 For life or until learning is stopped
    for episode in range(total_episodes):
        # Reset the environment
        state = env.reset()
        step = 0
        done = False
        total_rewards = 0

        for step in range(max_steps):

            # 3. Choose an action a in the current world state (s)
            # First we randomize a number
            exp_exp_tradeoff = random.uniform(0, 1)

            # If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)
            if exp_exp_tradeoff > epsilon:
                action = np.argmax(qtable[state, :])

            # Else doing a random choice --> exploration
            else:
                action = env.action_space.sample()

            # Take the action (a) and observe the outcome state(s') and reward (r)
            new_state, reward, done, info = env.step(action)

            # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
            qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma *
                                                                             np.max(qtable[new_state, :]) - qtable[state, action])

            total_rewards += reward
            # Our new state is state
            state = new_state

            # If done : finish episode
            if done == True:
                break
            if (step == max_steps-1):
                #print('Max Step Reached for Episode - ', episode)
                #print('Epsilon value at Max Step - ', epsilon)
                avg_epsilon.append(epsilon)

        # Reduce epsilon (because we need less and less exploration)
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * \
            np.exp(-decay_rate*episode)
        rewards.append(total_rewards)

    print("Number of Training Episodes - " + str(total_episodes))
    print("Training Score over time: " + str(sum(rewards)/total_episodes))
    try:
        print("Average Epsilon value when max steps is reached: " +
              str(sum(avg_epsilon)/len(avg_epsilon)))
    except:
        print("Average Epsilon value is 0, since Max steps are not reached")

    print(qtable)
    print(" ")

    env.reset()
    rewards = []
    avg_steps = []

    print('*************************  Q-Testing  ********************************')

    for episode in range(total_test_episodes):
        state = env.reset()
        step = 0
        done = False
        total_rewards = 0

        for step in range(max_steps):

            # UNCOMMENT IT IF YOU WANT TO SEE OUR AGENT PLAYING
            # env.render()
            # Take the action (index) that have the maximum expected future reward given that state
            action = np.argmax(qtable[state, :])

            new_state, reward, done, info = env.step(action)

            total_rewards += reward

            if done:
                # env.render()
                print("Episode - " + str(episode) +
                      ",  Score - ", total_rewards)
                # avg_steps.append(step)
                break
            state = new_state
        avg_steps.append(step)
        rewards.append(total_rewards)

    env.close()

    print("Learning Rate value - " + str(learning_rate))
    print("Number of Test Episodes - " + str(total_test_episodes))
    print("Testing Score over time: " + str(sum(rewards)/total_test_episodes))
    print("Average num of Steps Per Episode: " +
          str(sum(avg_steps)/total_test_episodes))

'''
