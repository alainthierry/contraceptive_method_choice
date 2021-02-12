# -*- coding: utf-8 -*-
"""contraceptive_method_choice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14Wab6GFhA08hhVtMUbpyjZAWahDGHB8C

# Dataset Description
<p>This dataset is a subset of the 1987 National Indonesia Contraceptive Prevalence Survey. The samples are married women who were either not pregnant or do not know if they were at the time of interview. The problem is to predict the current contraceptive method choice<strong>(no use, long-term methods, or short-term methods)</strong> of a woman based on her demographic and socio-economic characteristics.
<a href="https://archive.ics.uci.edu/ml/datasets/Contraceptive+Method+Choice" target="_blank" >cmc</a></p>

#### Inclusion of needed packages and libraries
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from pandas.plotting import scatter_matrix
from scipy.stats import pearsonr
from scipy.stats import shapiro, normaltest, chi2_contingency
ALPHA = 0.05

sns.set()
sns.set_theme()
plt.style.use('classic')
plt.rcParams.update({ "font.family": "serif",})

"""#### <b> Note that LR is for LogisticRegression </b>

### Dataset Uploading
"""

headers = ['wife_age', 'wife_education', 'husband_education', 'number_children_ever_born',
           'wife_religion', 'wife_working', 'husband_occupation', 'standard_living',
           'media_exposure', 'contraceptive_method_used']
filename = "/content/cmc.data"
df = pd.read_csv(filename, names=headers)

"""### Data Preprocessing"""

headers[:7]

print(f'Dataset info : \n {df.info()} \n Dataset Variables data types : \n {df.dtypes}')

print(f'Contains no values : \n {df.isnull().sum()} \n Contains NaN : \n {df.isna().sum()}')

df.shape

df.head(7)

df['contraceptive_method_used'].value_counts()
sns.histplot(df['contraceptive_method_used'])
plt.show()

"""The dataset contains 10 variables with 1473 observations in which there 9 predictors and 1 target (contraceptive_method_choice). All observations are integers and the dataset contains no missing values. The target has two types of value 1 (no-use), 2 (short-term) and 3 (long-term).This is a prediction by classifying if the woman's contraceptive method choice doesn't exist(no-use) ,is short-term method usage and long-term method. The observations per class are 629 for no-use, 511 for short-term method and 333 for long-term method.<b> So, the contraceptive_method_choice class is unbalanced.</b>

---

#### Descriptive Statistics
"""

df.describe()

"""The wife age ranges between 16 and 49. The average is around 32 years old. The standard deviation is around 8, so the observations of the wife_age variable are not too scattered. <b>We'll need to standardize predictors(to put them in a same range of values)</b>"""

correlations = df.corr(method='pearson')
correlations.style.background_gradient()

""" Correlation matrix plot """
plt.style.use('classic')
plt.rcParams.update({ "font.family": "serif",})
fig = plt.figure(figsize=(10, 5))
ax = plt.axes()
cax = ax.matshow(correlations, vmin=-1, vmax=1)
cbar = fig.colorbar(cax)
ticks = np.arange(0,10,1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_yticklabels(headers)
plt.show()

pearsonr(df['wife_education'], df['husband_education'])

plt.figure(figsize=(10, 4))
plt.rcParams.update({ "font.family": "serif", "font.size": 13})
sns.scatterplot(
    data=df, x="wife_education", y="husband_education", hue="contraceptive_method_used",
    palette = 'deep'
)
plt.legend()
plt.show()

stat, p = pearsonr(df['wife_education'], df['husband_education'])
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably independent')
else:
	print('Probably dependent')

"""This shows that the wife_education and the husband_eduction variables are moderately correlated. Others predictors than wife_education and husband_education are not correlated.<b>The correlation is given with a p-value under 0.001 though the scatter plot doesn't show that. The pearson test confirms that wife_education and husband_education are dependant</b> We can assume these other predictors are independant with the target."""

df.hist(bins=20, layout=(5, 5), sharex=False, figsize=(17, 15))
plt.show()

df.plot(kind='density', subplots=True, layout=(5, 5), sharex=False, figsize=(17, 15))
plt.show()

"""This above plots show that  the predictors number children_ever_born and wife_age except the others seem to have a certain normal distribution."""

df.plot(kind = 'box', subplots=True, layout=(5, 5), sharex=False, figsize=(17, 15))
plt.show()

"""The observations of wife_age predictors are well distributed, which is not the same case for others predictors.

#### Hypotheses Tests (Gaussianity)

H0: the sample has a Gaussian distribution.
    H1: the sample does not have a Gaussian distribution.

##### The Shapiro Test
"""

for predictor_name in headers:
  stat, p = shapiro(df[predictor_name])
  if p > ALPHA:
    print(f'{predictor_name} probably Gaussian')
  else:
    print(f'{predictor_name} probably not Gaussian')

"""##### The Normaltest Test"""

for predictor_name in headers:
  stat, p = normaltest(df[predictor_name])
  if p > ALPHA:
    print(f'{predictor_name} probably Gaussian')
  else:
    print(f'{predictor_name} probably not Gaussian')

"""<b>After these two hypotheses tests, we can confirm that no predictor is gaussian, has a normal distribution for a confidence interval of 95%.</b>

#### Hypotheses Tests (Independance)

H0: the two samples are independent.
    H1: there is a dependency between the samples.

##### The Chi-Squared Test
"""

for predictor_name in headers:
    table = pd.crosstab( df['contraceptive_method_used'], df[predictor_name] )
    stat, p, dof, expected = chi2_contingency(table)
    if p > ALPHA:
      pass
      print(f'contraceptive_method_used & {predictor_name} are probably independent')
    else:
      print(f'contraceptive_method_used & {predictor_name} are probably dependent')

for predictor_name1 in headers:
  for predictor_name2 in headers:
    table = pd.crosstab( df[predictor_name1], df[predictor_name2] )
    stat, p, dof, expected = chi2_contingency(table)
    # print('stat=%.3f, p=%.3f' % (stat, p))
    print(f'stat={np.round(stat, 3)}, p={np.round(p, 4)}')
    if p > ALPHA:
      pass
      print(f'{predictor_name1} & {predictor_name2} are probably independent')
    else:
      print(f'{predictor_name1} & {predictor_name2} are probably dependent')

"""##### All predictors except wife_working and the target (contraceptive_method_used) are dependant. Then, we can assume that most accurate variables for predicting contraceptive_method_used target are all the predictors except <b>wife_working</b> with a confidence interval of 95%.

#### Data Standardization
"""

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import(
    train_test_split, KFold, cross_val_score, RepeatedStratifiedKFold, GridSearchCV
)

from sklearn.linear_model import  LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import  SVC

from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, mean_absolute_error
)

X = df.drop('contraceptive_method_used', axis=1)
y = df["contraceptive_method_used"]
seed = 7

scaler = StandardScaler()
scaled_X = scaler.fit_transform(X)

"""##### Data Splitting"""

X_train, X_test, y_train, y_test = train_test_split(scaled_X, y, test_size=0.3, random_state=seed)

"""Algorithms to test """

models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

"""Printing training accuracy"""

results = []
names = []
for name, model in models:
  kfold = KFold(n_splits=10, random_state=seed, shuffle=True)
  cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
  results.append(cv_results)
  names.append(name)
  print(f"{name} accuracy ({cv_results.mean()}) std ({cv_results.std()})")

""" Plotting Comparison """   
plt.style.use('classic')
plt.rcParams.update({ "font.family": "serif",})
fig = plt.figure(figsize=(10, 4))
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.ylabel('Training Accuracy')
plt.show()

"""##### <b>The SVM (SVC) classifier has the largest training accuracy, but it's not good enough. Can we do better ?</b>

#### Parameters Tuning

###### Tuning LogisticRegression parameters (Regularization, max_iter)

###### <b> For penalty = l1 </b>
"""

max_iters = [1_000, 10_000, 100_000, 10000000]

for iter in max_iters:

  clf_l1_LR = LogisticRegression(penalty='l1', tol=0.01, solver='saga', max_iter=iter, multi_class='multinomial')
  kfold = KFold(n_splits=10, random_state=seed, shuffle=True)
  cv_results = cross_val_score(clf_l1_LR, X_train, y_train, cv=kfold, scoring='accuracy')
  print(f'Accuracy ({cv_results.mean()}), std ({cv_results.std()})')

"""###### <b> For penalty = l2 </b>"""

max_iters = [1_000, 10_000, 100_000, 10000000]

for iter in max_iters:

  clf_l2_LR = LogisticRegression(penalty='l2', tol=0.01, solver='newton-cg', max_iter=iter, multi_class='multinomial')
  kfold = KFold(n_splits=10, random_state=seed, shuffle=True)
  cv_results = cross_val_score(clf_l2_LR, X_train, y_train, cv=kfold, scoring='accuracy')
  print(f'Accuracy ({cv_results.mean()}), std ({cv_results.std()})')

"""###### <b> For penalty = elasticnet </b>"""

max_iters = [1_000, 10_000, 100_000, 10000000]
l1_ratio = 0.5

for iter in max_iters:
  clf_en_LR = LogisticRegression(penalty='elasticnet', solver='saga',l1_ratio=0.5, tol=0.01, max_iter=iter, multi_class='multinomial')

  kfold = KFold(n_splits=10, random_state=seed, shuffle=True)
  cv_results = cross_val_score(clf_en_LR, X_train, y_train, cv=kfold, scoring='accuracy')
  print(f'Accuracy ({cv_results.mean()}), std ({cv_results.std()})')

"""##### No improvement, the training and test accuracy remain the same as in the default configuration.

##### ''' Prediction Accuracy, confusion_matrix in default configuration '''
"""

""" Prediction Accuracy, confusion_matrix in default configuration """
model = LogisticRegression()
fitted = model.fit(X_train, y_train)
y_hat = fitted.predict(X_test)

print(f"LogisticRegression\n Prediction Accuracy {accuracy_score(y_test, y_hat)} \n {confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

""" Prediction Accuracy, confusion_matrix in tuned configuration """

max_iters = [1_000, 10_000, 100_000, 10000000]

for iter in max_iters:
  model = LogisticRegression(penalty='l2', tol=0.01, solver='newton-cg', max_iter=iter, multi_class='multinomial')
  fitted = model.fit(X_train, y_train)
  y_hat = fitted.predict(X_test)
  print(f"Max_iterations : {iter}")
  print(f"{accuracy_score(y_test, y_hat)} \n {confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

"""##### No improvement, the training and test accuracy remain the same as in the default configuration.

###### <b>Tuning LDA parameters</b>
"""

model = LinearDiscriminantAnalysis()
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid = {'solver': ['svd', 'lsqr', 'eigen']}
search = GridSearchCV(model, grid, scoring='accuracy', cv=cv, n_jobs=-1)
results = search.fit(X_train, y_train)
print('Training Accuracy: %.3f' % results.best_score_)
print('Config: %s' % results.best_params_)

"""##### No improvement, the training and test accuracy remain the same as in the default configuration"""

model = LinearDiscriminantAnalysis(solver='lsqr')
fit = model.fit(X_train, y_train)
y_hat = fit.predict(X_test)

print(f"LDA Prediction Accuracy {accuracy_score(y_test, y_hat)} \n {confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

"""###### <b>The best LDA configuration is obtained with lsqr solver. The LDA does better than the LogisticRegression in both training and test accuracy</b>

###### <b>Tuning KNN parameters</b>
"""

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_params = {
    'n_neighbors': list(range(1, 10)),
    'weights' : ['uniform', 'distance'],
    'algorithm': ['ball_tree', 'kd_tree', 'brute', 'auto'],
    'metric' : ['euclidean', 'manhattan', 'minkowski'],
}

search = GridSearchCV(KNeighborsClassifier(n_jobs=-1), grid_params, scoring='accuracy', cv=cv, n_jobs=-1)
results = search.fit(X_train, y_train)
print('Mean Accuracy: %.3f' % results.best_score_)
print('Config: %s' % results.best_params_)

"""###### This is better than the default configuration of KNeighborsClassifier. The best configuration is <b>Config: {'algorithm': 'ball_tree', 'metric': 'manhattan', 'n_neighbors': 9, 'weights': 'uniform'}</b>
---


"""

model = KNeighborsClassifier(n_neighbors=9, weights='uniform',algorithm='ball_tree', metric='manhattan')
fit = model.fit(X_train, y_train)
y_hat = fit.predict(X_test)
print(f"KNN Prediction Accuracy {accuracy_score(y_test, y_hat)} \n Confusion Matrix \n {confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

"""##### Tuning CART DecisionTreeClassifier"""

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_params = {
    'criterion': ['entropy', 'gini'],
    'splitter' : ['best', 'random'],
}

search = GridSearchCV(DecisionTreeClassifier(), grid_params, scoring='accuracy', cv=cv, n_jobs=-1)
results = search.fit(X_train, y_train)
print('Mean Accuracy: %.3f' % results.best_score_)
print('Config: %s' % results.best_params_)

"""<b>The DecisionTreeClassifier does not do better than the default configuration</b>

###### Tuning  SVM (*SVC*) parameters
"""

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=seed)
param_grid = {'C': [0.1, 1, 10, 100, 1000, 10000, 100000],
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'decision_function_shape': ['ovo', 'ovr'],
              'kernel': ['linear', 'poly', 'rbf'] }
  
grid = GridSearchCV(SVC(shrinking=True), param_grid, scoring='accuracy', n_jobs=-1, refit=True,cv=cv, verbose=3) 
results = grid.fit(X_train, y_train) 

print('Mean Accuracy: %.3f' % results.best_score_)
print('Config: %s' % results.best_params_)

"""This is better than the default configuration of SVM SVC classifier. The <b>training accuracy is 0.554 when the training accuracy of the default configuration is 0.5372.</b>

###### SVM (SVC) Prediction Accuracy
"""

model = SVC(C=100, kernel='rbf', gamma=0.01, shrinking=True, probability=True)
fitted  = model.fit(X_train, y_train)

y_hat = fitted.predict(X_test)
print(f"SVM(SVC) Prediction Accuracy {accuracy_score(y_test, y_hat)} \n Confusion Matrix \n{confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

"""###### Prediction Accuray of all algorithms"""

models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA',  LinearDiscriminantAnalysis(solver='lsqr')))
models.append(('KNN', KNeighborsClassifier(n_neighbors=9,weights='uniform', algorithm='ball_tree', metric='manhattan')))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(C=100, kernel='rbf', gamma=0.01, shrinking=True, probability=True)))

results = []
names = []
for name, model in models:
   kfold = KFold(n_splits=3)
   cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
   results.append(cv_results)
   names.append(name)

   fitted  = model.fit(X_train, y_train)
   y_hat = fitted.predict(X_test)
   print(f"{name} Training TAccuracy ({name, cv_results.mean()}) STD ({cv_results.std()})")
   print(f"{name} Prediction Accuracy {accuracy_score(y_test, y_hat)} \n {confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

""" Plotting Comparison """   
plt.style.use('classic')
plt.rcParams.update({ "font.family": "serif",})
fig = plt.figure(figsize=(10, 4))
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
plt.ylabel('Training Accuracy')

ax.set_xticklabels(names)
plt.show()

"""##### The SVM (SVC) does <b>much better than all other tested algorithms with a training accuracy of 0.545 and 0.5497 as testing accuracy</b>". Can we do better again ?"""

from sklearn.neural_network import  MLPClassifier

fitted = model.fit(X_train, y_train)

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=seed)
kfold = KFold(n_splits=3)
cv_results = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')
print(cv_results.mean(), cv_results.std())

model = MLPClassifier(random_state=seed, hidden_layer_sizes=100, activation='tanh',
                      solver='lbfgs', alpha=0.0001,max_iter = 10000,
                      )
fitted = model.fit(X_train, y_train)

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=seed)
# kfold = KFold(n_splits=3)
cv_results = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')
print(cv_results.mean(), cv_results.std())

"""##### The neuronal network MLPClassifier is worse for both training and prediction accuracy"""

from sklearn.ensemble import(
    BaggingClassifier, RandomForestClassifier,ExtraTreesClassifier
)

ensembles = []
ensembles.append(('BCL', BaggingClassifier()))
ensembles.append(('RFCL', RandomForestClassifier()))
ensembles.append(('ETCL', ExtraTreesClassifier()))

results = []
names = []
for name, ensemble in ensembles:
    kfold = KFold(n_splits=3)
    
    cv_results = cross_val_score(ensemble, X_train, y_train, cv=kfold, scoring="accuracy")
    results.append(cv_results)
    names.append(name)
    print(f"{name} Training accuracy ({cv_results.mean()}) SDT ({cv_results.std()})")

""" Plotting Comparison """   
plt.style.use('seaborn-deep')
plt.rcParams.update({ "font.family": "serif",})
fig = plt.figure(figsize=(10, 4))
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

"""###### <b> The RandomForestClassifier performs better as the SVM (SVC) classifier<b>.

### <b>Feature Selection</b>
"""

X = df.drop('contraceptive_method_used', axis=1)
y = df["contraceptive_method_used"]
from sklearn.feature_selection import SelectKBest, chi2

"""###### Predictors Selection with <b>chi2</b>"""

best = SelectKBest(score_func=chi2, k=3)
X_NEW = best.fit_transform(X, y)

X_NEW_train, X_NEW_test, y_new_train, y_new_test = train_test_split(X_NEW, y, test_size=0.3,random_state=seed)

""" Adding Algorithms """
models = []
models.append(('LR', LogisticRegression(max_iter=1000)))
models.append(('LDA',  LinearDiscriminantAnalysis(solver='lsqr')))
models.append(('KNN', KNeighborsClassifier(n_neighbors=9,weights='uniform', algorithm='ball_tree', metric='manhattan')))
models.append(('SVM', SVC(C=100, kernel='rbf', gamma=0.01, shrinking=True, probability=True)))
models.append(('RFCL', RandomForestClassifier(criterion='entropy')))

""" Cross_validation """
results = []
names = []
for name, model in models:
   kfold = KFold(n_splits=3)

   cv_results = cross_val_score(model, X_NEW_train, y_new_train, cv=kfold, scoring='accuracy')
   results.append(cv_results)
   names.append(name)

   fitted  = model.fit(X_NEW_train, y_new_train)
   y_hat = fitted.predict(X_NEW_test)
   print(f"{name} Training TAccuracy ({name, cv_results.mean()}) STD ({cv_results.std()})")
   print(f"{name} Prediction Accuracy {accuracy_score(y_new_test, y_hat)} \n {confusion_matrix(y_new_test, y_hat)} \n {classification_report(y_new_test, y_hat)} ")

""" Cross_validation """
results = []
names = []
for name, model in models:
   kfold = KFold(n_splits=3)

   cv_results = cross_val_score(model, X_NEW_train, y_new_train, cv=kfold, scoring='accuracy')
   results.append(cv_results)
   names.append(name)

   fitted  = model.fit(X_NEW_train, y_new_train)
   y_hat = fitted.predict(X_NEW_test)
   print(f"{name} Training TAccuracy ({name, cv_results.mean()}) STD ({cv_results.std()})")
   print(f"{name} Prediction Accuracy {accuracy_score(y_new_test, y_hat)} \n {confusion_matrix(y_new_test, y_hat)} \n {classification_report(y_new_test, y_hat)} ")

""" Plot Algorithms Comparison """
""" Plotting Comparison """   
plt.style.use('classic')
plt.rcParams.update({ "font.family": "serif",})
fig = plt.figure(figsize=(10, 4))
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

"""<b>The SVM (SVC) remains much better than other algorithms for k predictors, k = 3.</b>

<b> Seek the best k fold </b>
"""

list_training_error = []
list_testing_error = []
data = df.values
X = data[:, :9]
y = data[:, 9]

kf = KFold(n_splits=20)

for train_index, test_index in kf.split(X):
  X_train, X_test = X[train_index], X[test_index]
  y_train, y_test = y[train_index], y[test_index]
  model = SVC(C=100, kernel='rbf', gamma=0.01, shrinking=True, probability=True)
  
  model.fit(X_train, y_train)
  y_train_data_pred = model.predict(X_train)
  y_test_data_pred = model.predict(X_test)

  fold_training_error = mean_absolute_error(y_train, y_train_data_pred) 
  fold_testing_error = mean_absolute_error(y_test, y_test_data_pred)

  list_training_error.append(fold_training_error)
  list_testing_error.append(fold_testing_error)

plt.figure(figsize=(12, 5))
plt.subplot(1,2,1)
plt.plot(range(1, kf.get_n_splits() + 1), np.array(list_training_error).ravel(), 'o-')
plt.xlabel('number of fold')
plt.ylabel('training error')
plt.title('Training error across folds')
plt.tight_layout()
plt.subplot(1,2,2)
plt.plot(range(1, kf.get_n_splits() + 1), np.array(list_testing_error).ravel(), 'o-')
plt.xlabel('number of fold')
plt.ylabel('testing error')
plt.title('Testing error across folds')
plt.tight_layout()
plt.show()

"""##### <b>It's k = 3 as used in the cross_validation of SVC Classifier.</b> Can we improve with PCA"""

from sklearn.decomposition import PCA

pca = PCA()
pca.fit(scaled_X)

exp_variance = pca.explained_variance_ratio_
fig, ax = plt.subplots()
ax.bar(range(pca.n_components_), exp_variance)
ax.set_xlabel('Principal Component #')

"""It's not clear to see where the elbow appears, but take 6 components of 85%."""

cum_exp_variance = np.cumsum(exp_variance)

fig, ax = plt.subplots()
ax.plot(cum_exp_variance)
ax.axhline(y=0.85, linestyle='--')

n_components = 6

pca = PCA(n_components, random_state=seed)
pca.fit(scaled_X)
pca_projection = pca.transform(scaled_X)

X_train_pca, X_test_pca, y_train_pca, y_test_pca = train_test_split(
    pca_projection, df['contraceptive_method_used'], random_state=seed,
)

model = SVC()
fitted  = model.fit(X_train_pca, y_train_pca)

cross_val_results = cross_val_score(model, X_train_pca, y_train_pca, scoring='accuracy', cv=KFold(n_splits=3))
print(cross_val_results.mean(), cross_val_results.std())

y_hat_pca = fitted.predict(X_test_pca)
print(f"PCA SVM(SVC) Prediction Accuracy {accuracy_score(y_test_pca, y_hat_pca)} \n Confusion Matrix \n{confusion_matrix(y_test_pca, y_hat_pca)} \n {classification_report(y_test_pca, y_hat_pca)} ")

"""<b>This is not better than the chi2 feature selection.</b> Let's balance the classes ?

###### <>With stratify arg<>
"""

X = df.drop('contraceptive_method_used', axis=1)
scaled_X = scaler.fit_transform(X)
y = df["contraceptive_method_used"]
X_bal_train, X_bal_test, y_bal_train, y_bal_test = train_test_split(scaled_X, y, test_size=0.2, random_state=seed,stratify=y)

model = SVC(C=100, kernel='rbf', gamma=0.01, shrinking=True, probability=True)
fitted  = model.fit(X_bal_train, y_bal_train)
cross_val_results = cross_val_score(model, X_bal_train, y_bal_train, scoring='accuracy', cv=KFold(n_splits=10))
print(f"SVM(SVC) \nTraining Accuracy ({cross_val_results.mean()}), STD ({cross_val_results.std()})")

y_hat_pca = fitted.predict(X_bal_test)
print(f"Prediction Accuracy {accuracy_score(y_bal_test, y_hat_pca)} \n Confusion Matrix \n{confusion_matrix(y_bal_test, y_hat_pca)} \n {classification_report(y_bal_test, y_hat_pca)} ")

"""###### <b> Balancing the data by sampling </b>"""

df_class_1 = df[df['contraceptive_method_used'] == 1]
df_class_2 = df[df['contraceptive_method_used'] == 2]
df_class_3 = df[df['contraceptive_method_used'] == 3]

df_class_2 = df_class_2.sample(df_class_1.shape[0], replace=True, random_state=seed)
df_class_3 = df_class_3.sample(df_class_1.shape[0], replace=True, random_state=seed)

data = pd.concat([df_class_1, df_class_2, df_class_3])
print(data['contraceptive_method_used'].value_counts())

"""<b>The classes are now well balanced</b>"""

X_train, X_test, y_train, y_test = train_test_split(
    scaler.fit_transform(data.drop('contraceptive_method_used', axis=1)), data['contraceptive_method_used'],
    test_size=0.3, random_state=seed, stratify=data['contraceptive_method_used']
)

model = SVC(C=100, kernel='rbf', gamma=0.01, shrinking=True, probability=True)

fitted  = model.fit(X_train, y_train)
cross_val_results = cross_val_score(model, X_train, y_train, scoring='accuracy', cv=KFold(n_splits=10))
print(f"SVM(SVC) \nTraining Accuracy ({cross_val_results.mean()}), STD ({cross_val_results.std()})")

y_hat = fitted.predict(X_test)
print(f"Prediction Accuracy {accuracy_score(y_test, y_hat)} \n Confusion Matrix \n{confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

"""<b>The SVM (SVC) does more much better than the unbalanced case.</b> Can we have better ?

<b>Chi2 Feature Selection after balancing classes</b>
"""

best = SelectKBest(score_func=chi2, k=7)
y = data['contraceptive_method_used']
X = data.drop('contraceptive_method_used', axis=1)
X_NEW = best.fit_transform(X, y)

X_NEW_train, X_NEW_test, y_new_train, y_new_test = train_test_split(
    X_NEW, y, test_size=0.3, random_state=seed, stratify=data['contraceptive_method_used'],
    )

""" Adding Algorithms """
models = []
models.append(('LR', LogisticRegression(max_iter=1000)))
models.append(('LDA',  LinearDiscriminantAnalysis(solver='lsqr')))
models.append(('KNN', KNeighborsClassifier(n_neighbors=9,weights='uniform', algorithm='ball_tree', metric='manhattan')))
models.append(('SVM', SVC(C=100, kernel='rbf', gamma=0.01, shrinking=True, probability=True)))
models.append(('RFCL', RandomForestClassifier()))

""" Cross_validation """
results = []
names = []
for name, model in models:
   kfold = RepeatedStratifiedKFold(n_splits=13, n_repeats=3, random_state=seed)

   cv_results = cross_val_score(model, X_NEW_train, y_new_train, cv=kfold, scoring='accuracy')
   results.append(cv_results)
   names.append(name)

   fitted  = model.fit(X_NEW_train, y_new_train)
   y_hat = fitted.predict(X_NEW_test)
   print(f"{name} Training Accuracy ({name, cv_results.mean()}) STD ({cv_results.std()})")
   print(f"{name} Prediction Accuracy {accuracy_score(y_new_test, y_hat)} \n {confusion_matrix(y_new_test, y_hat)} \n {classification_report(y_new_test, y_hat)} ")

""" Plot Algorithms Comparison """
""" Plotting Comparison """   
plt.style.use('classic')
plt.rcParams.update({ "font.family": "serif",})
fig = plt.figure(figsize=(10, 4))
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

"""###### <b> The RandomForestClassifier does much better than the SVC classifier as shown by the plot above</b>

#### Let's check again PCA
"""

pca = PCA()
pca.fit(scaler.fit_transform(data.drop('contraceptive_method_used', axis=1)))

exp_variance = pca.explained_variance_ratio_
fig, ax = plt.subplots()
ax.bar(range(pca.n_components_), exp_variance)
ax.set_xlabel('Principal Component #')

cum_exp_variance = np.cumsum(exp_variance)

fig, ax = plt.subplots()
ax.plot(cum_exp_variance)
ax.axhline(y=0.85, linestyle='--')
n_components = 6
pca = PCA(n_components, random_state=seed)
pca.fit(scaled_X)
pca_projection = pca.transform(scaled_X)

X_train_pca, X_test_pca, y_train_pca, y_test_pca = train_test_split(
    pca_projection, df['contraceptive_method_used'], random_state=seed,
)

model = SVC(C=100, kernel='rbf', gamma=0.01, shrinking=True, probability=True)
fitted  = model.fit(X_train_pca, y_train_pca)

cross_val_results = cross_val_score(model, X_train_pca, y_train_pca, scoring='accuracy', cv=KFold(n_splits=16))
print(cross_val_results.mean(), cross_val_results.std())

y_hat_pca = fitted.predict(X_test_pca)
print(f"PCA SVM(SVC) Prediction Accuracy {accuracy_score(y_test_pca, y_hat_pca)} \n Confusion Matrix \n{confusion_matrix(y_test_pca, y_hat_pca)} \n {classification_report(y_test_pca, y_hat_pca)} ")

"""<b>This is worse according to the previous algorithms. Then, by conclusion, the better model is obtained with k = 7 features(chi2 selection) with RandomForestClassifier.</b>"""

list_training_error = []
list_testing_error = []
values = data.values
X = values[:, :7]
y = values[:, 9]

kf = KFold(n_splits=20)

for train_index, test_index in kf.split(X):
  X_train, X_test = X[train_index], X[test_index]
  y_train, y_test = y[train_index], y[test_index]
  model = RandomForestClassifier()
  
  model.fit(X_train, y_train)
  y_train_data_pred = model.predict(X_train)
  y_test_data_pred = model.predict(X_test)

  fold_training_error = mean_absolute_error(y_train, y_train_data_pred) 
  fold_testing_error = mean_absolute_error(y_test, y_test_data_pred)

  list_training_error.append(fold_training_error)
  list_testing_error.append(fold_testing_error)

plt.figure(figsize=(12, 5))
plt.subplot(1,2,1)
plt.plot(range(1, kf.get_n_splits() + 1), np.array(list_training_error).ravel(), 'o-')
plt.xlabel('number of fold')
plt.ylabel('training error')
plt.title('Training error across folds')
plt.tight_layout()
plt.subplot(1,2,2)
plt.plot(range(1, kf.get_n_splits() + 1), np.array(list_testing_error).ravel(), 'o-')
plt.xlabel('number of fold')
plt.ylabel('testing error')
plt.title('Testing error across folds')
plt.tight_layout()
plt.show()

"""<b>The best kfold value is between 15 and 17 for cross validation</b>"""

best = SelectKBest(score_func=chi2, k=7)
y = data['contraceptive_method_used']
X = data.drop('contraceptive_method_used', axis=1)
X_NEW = best.fit_transform(X, y)

X_NEW_train, X_NEW_test, y_new_train, y_new_test = train_test_split(
    X_NEW, y, test_size=0.3, random_state=seed,
    )

model = RandomForestClassifier()
""" Cross_validation """

cv_results = cross_val_score(model, X_NEW_train, y_new_train, cv=KFold(n_splits=16), scoring='accuracy')
fitted  = model.fit(X_NEW_train, y_new_train)
y_hat = fitted.predict(X_NEW_test)

print(f"RFCL Training Accuracy ({cv_results.mean()}) STD ({cv_results.std()})")
print(f"RFCL Prediction Accuracy {accuracy_score(y_new_test, y_hat)} \n {confusion_matrix(y_new_test, y_hat)} \n {classification_report(y_new_test, y_hat)} ")

"""<b>The RFCL wins and the needed predictors are the seven obtained with chi2 for feature selection for predicting with an accuracy of 0.714 and the confusion matrix is much better than the one of the SVM (SVC) and other algorithms</b>.

#### Ensemble with balanced class ( Contraceptive_method_used ) and chi2 feature selection
"""

best = SelectKBest(score_func=chi2, k=7)
y = data['contraceptive_method_used']
X = data.drop('contraceptive_method_used', axis=1)
X_NEW = best.fit_transform(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_NEW, y, test_size=0.3, random_state=seed)

results = []
names = []
for name, ensemble in ensembles:
    kfold = KFold(n_splits=16)
    
    cv_results = cross_val_score(ensemble, X_train, y_train, cv=kfold, scoring="accuracy")
    results.append(cv_results)
    names.append(name)

    fitted  = ensemble.fit(X_train, y_train)
    y_hat = fitted.predict(X_test)

    print(f"{name} Error Test Rate {((y_hat != y_test).sum())/data.shape[0]*100}")
    print(f"{name} Training accuracy ({cv_results.mean()}) SDT ({cv_results.std()})")
    print(f"{name} Prediction Accuracy {accuracy_score(y_test, y_hat)} \n {confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

""" Plotting Comparison """   
plt.style.use('seaborn-deep')
plt.rcParams.update({ "font.family": "serif",})
fig = plt.figure(figsize=(10, 4))
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

"""#### <b>Conclusion : compare to other ensemble algorithms and SVM (SVC), RandomForestClassifier remains the best with 9% as test error rate, the best training and prediction accuracy and the confusion matrix.</b>

#### <b> Test the first 7 predictors of the balanced dataframe </b>
"""

df_balanced = data.values
X_balanced = df_balanced[:,:7]
y_balanced = df_balanced[:,9]
import pickle

X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.3, random_state=seed)

model = RandomForestClassifier()
""" Cross_validation """

cv_results = cross_val_score(model, X_train, y_train, cv=KFold(n_splits=16), scoring='accuracy')
model_rfcl = model.fit(X_train, y_train)
y_hat = model_rfcl.predict(X_test)

print(f"RFCL Training Accuracy ({cv_results.mean()}) STD ({cv_results.std()})")
print(f"RFCL Prediction Accuracy {accuracy_score(y_test, y_hat)} \n {confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

results = []
names = []
for name, ensemble in ensembles:
    kfold = KFold(n_splits=16)
    
    cv_results = cross_val_score(ensemble, X_train, y_train, cv=kfold, scoring="accuracy")
    results.append(cv_results)
    names.append(name)

    fitted  = ensemble.fit(X_train, y_train)
    y_hat = fitted.predict(X_test)

    print(f"{name} Error Test Rate {((y_hat != y_test).sum())/data.shape[0]*100}")
    print(f"{name} Training accuracy ({cv_results.mean()}) SDT ({cv_results.std()})")
    print(f"{name} Prediction Accuracy {accuracy_score(y_test, y_hat)} \n {confusion_matrix(y_test, y_hat)} \n {classification_report(y_test, y_hat)} ")

""" Plotting Comparison """   
plt.style.use('seaborn-deep')
plt.rcParams.update({ "font.family": "serif",})
fig = plt.figure(figsize=(10, 4))
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

"""###### <b>Finally : compare to other ensemble algorithms and SVM (SVC), RandomForestClassifier remains the best test error rate value between 8% and 9%, the best training and prediction accuracy and the confusion matrix with the first seven predictors of the balanced. These are the only variables that impact the woman's contraceptive method that she uses or will use</b>

#### <b>Save the model for reuse purposes</b>
"""

model_filename = 'finalized_model_rfcl.sav'
import joblib
joblib.dump(model_rfcl, model_filename)



