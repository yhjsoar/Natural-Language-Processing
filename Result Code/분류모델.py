# -*- coding: utf-8 -*-
"""분류모델.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jk2xOc-iJHTz-mEd8-HTM5p25xKPv1kU
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import urllib.request
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer
import numpy as np
import json
from bs4 import BeautifulSoup
import os
import gensim
from sklearn.model_selection import train_test_split

urllib.request.urlretrieve("https://drive.google.com/uc?export=download&id=1T_DZdHJkBcbUwt3CA5FqumlT3AuJjgls", filename="all_data.txt")

"""# 데이터 분석"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

train_data = pd.read_table("all_data.txt")

train_data.head()

# 파일 크기
print("파일 크기: ")
for file in os.listdir("./"):
  if 'txt' in file and 'zip' not in file:
    print(file.ljust(30) + str(round(os.path.getsize(file)/1000000, 2))+'MB')

# 데이터 개수
print("\n전체 학습 데이터의 개수: {}\n".format(len(train_data)))

# 각 문장의 문자 길이 분포
train_length = train_data['sentence'].apply(len)
train_length.head()

# 그래프에 대한 이미지 
# figsize: (가로,세로) 형태의 튜블로 입력
plt.figure(figsize=(12, 5))

# 히스토그램 선언
# bins: 히스토그램 값에 대한 버킷 범위
# range: x축 값의 범위
# alpha: 그래프 색상 투명도
# color: 그래프 색상
# label: 그래프에 대한 라벨
plt.hist(train_length, bins=200, alpha=0.5, color='r', label='word')
plt.yscale('log', nonposy='clip')

# 그래프 제목
plt.title('Log-Histogram of length or sentence')

# 그래프 x 축 라벨
plt.xlabel('Length of sentence')

# 그래프 y 축 라벨
plt.ylabel('Number of sentence')

print('문장 길이 최댓값: {}'.format(np.max(train_length)))
print('문장 길이 최솟값: {}'.format(np.min(train_length)))
print('문장 길이 평균값: {}'.format(np.mean(train_length)))
print('문장 길이 표준편차: {}'.format(np.std(train_length)))
print('문장 길이 중간값: {}'.format(np.median(train_length)))

# 사분위에 대한 경우는 0-100 스케일로 돼 있음
print('문장 길이 제1사분위: {}'.format(np.percentile(train_length, 25)))
print('문장 길이 제3사분위: {}'.format(np.percentile(train_length, 75)))

plt.figure(figsize=(12, 5))
# 박스 플롯 생성
# 첫 번째 인자: 여러 분포에 대한 데이터 리스트를 입력
# labels: 입력한 데이터에 대한 라벨
# showmeans: 평균을 마크함

plt.boxplot(train_length, labels=['counts'], showmeans=True)

!pip install wordcloud

from wordcloud import WordCloud
cloud = WordCloud(width=800, height = 600).generate("".join(train_data['sentence']))
plt.figure(figsize=(20,15))
plt.imshow(cloud)
plt.axis('off')

fig, axe = plt.subplots(ncols=1)
fig.set_size_inches(6, 3)
sns.countplot(train_data['emotion'])

"""# 데이터 전처리"""

train_data = pd.read_table("all_data.txt")

nltk.download('stopwords') # 불용어
stop_words = set(stopwords.words('english'))

def preprocessing(sentence, remove_stopwords=True):
  # 불용어 제거는 옵션으로 선택 가능하다.

  # 1. 영어가 아닌 특수문자를 공백(" ")으로 바꾸기
  sentence_text = re.sub("[^a-zA-Z]", " ", sentence)

  # 2. 대문자를 소문자로 바꾸고 공백 단위로 텍스트를 나눠서 리스트로 만든다
  words = sentence_text.lower().split()

  if remove_stopwords:
    # 3. 불용어 제거

    # 영어 불용어 불러오기
    stops = set(stopwords.words('english'))
    # 불용어가 아닌 단어로 이뤄진 새로운 리스트 생성
    words = [w for w in words if not w in stop_words]
    # 4. 단어 리스트를 공백을 넣어서 하나의 글로 합친다
    clean_sentence = ' '.join(words)

  else: #불용어를 제거하지 않을 때
    clean_sentence = ' '.join(words)

  return clean_sentence



clean_train_sentence = []
for sentence in train_data['sentence']:
  clean_train_sentence.append(preprocessing(sentence, remove_stopwords=True))

clean_train_sentence[0]

print(train_data['sentence'][0])
print(clean_train_sentence[0])

clean_train_df = pd.DataFrame({
    'sentence':clean_train_sentence,
    'emotion':train_data['emotion']
})

tokenizer = Tokenizer()
tokenizer.fit_on_texts(clean_train_sentence)
text_sequences = tokenizer.texts_to_sequences(clean_train_sentence)

print(text_sequences[0])

word_vocab = tokenizer.word_index
word_vocab["<PAD>"] = 0
print(word_vocab)

data_configs = {}

data_configs['vocab'] = word_vocab
data_configs['vocab_size'] = len(word_vocab)+1

MAX_SEQUENCE_LENGTH = 174
train_inputs = pad_sequences(text_sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post')

print('Shape of train data: ', train_inputs.shape)

train_labels = np.array(train_data['emotion'])
print('Shape of label tensor:', train_labels.shape)

DATA_PATH = "./data/"
TRAIN_INPUT_DATA = 'train_input.npy'
TRAIN_LABEL_DATA = 'train_label.npy'
TRAIN_CLEAN_DATA = 'train_clean.csv'
DATA_CONFIGS = 'data_configs.json'

if not os.path.exists(DATA_PATH):
  os.makedirs(DATA_PATH)

# 전처리된 데이터를 넘파이 형태로 저장
np.save(open(DATA_PATH+TRAIN_INPUT_DATA, 'wb'), train_inputs)
np.save(open(DATA_PATH+TRAIN_LABEL_DATA, 'wb'), train_labels)

# 정제된 텍스트를 csv 형태로 저장
clean_train_df.to_csv(DATA_PATH+TRAIN_CLEAN_DATA, index=False)

# 데이터 사전을 JSON 형태로 저장
json.dump(data_configs, open(DATA_PATH + DATA_CONFIGS, 'w'), ensure_ascii=False)

"""# countvectorizer

### Embedding
"""

DATA_PATH = "./data/"
TRAIN_CLEAN_DATA = 'train_clean.csv'

train_data = pd.read_csv(DATA_PATH + TRAIN_CLEAN_DATA)

sentence_cv = list(train_data['sentence'])
y_cv = np.array(train_data['emotion'])

from sklearn.feature_extraction.text import CountVectorizer

vectorizer_cv = CountVectorizer(analyzer="word", max_features=5000)

train_data_features_cv = vectorizer_cv.fit_transform(sentence_cv)

print(vectorizer_cv)

print(train_data_features_cv)

"""### training"""

TEST_SIZE = 0.2
RANDOM_SEED = 42

train_input, eval_input, train_label, eval_label = train_test_split(train_data_features_cv, y_cv, test_size = TEST_SIZE, random_state=RANDOM_SEED)

# random forest

from sklearn.ensemble import RandomForestClassifier

forest_cv = RandomForestClassifier(n_estimators = 100)

forest_cv.fit(train_input, train_label)

# logistic regression

from sklearn.linear_model import LogisticRegression

lgs_cv = LogisticRegression(class_weight='balanced')
lgs_cv.fit(train_input, train_label)

print("Accuracy cv forest  : %f"%forest_cv.score(eval_input, eval_label))
print("Accuracy cv logistic: %f"%lgs_cv.score(eval_input, eval_label))

"""### testing """

urllib.request.urlretrieve("https://drive.google.com/uc?export=download&id=1WBrsz_bimuRZCBEv149hL-PoTi00tHwi", filename="black_cat.txt")

test_data = pd.read_table('black_cat.txt')

print(test_data)

test_sentences = list(test_data['sentence'])
real_emotion = list(test_data['emotion'])

test_data_features = vectorizer_cv.transform(test_sentences)

result_forest = forest_cv.predict(test_data_features)
result_lgs = lgs_cv.predict(test_data_features)

output_forest = pd.DataFrame(data = {"expected":result_forest, "real": real_emotion, "sentence": test_sentences})
output_lgs = pd.DataFrame(data = {"expected":result_lgs, "real": real_emotion, "sentence": test_sentences})

print("forest:")
print(output_forest)
print("\nlgs:")
print(output_lgs)

# output.to_csv("BlackCat_Expect.csv", index=False, quoting=3)

"""# tfidfvectorizer

### Embedding
"""

from sklearn.feature_extraction.text import TfidfVectorizer

DATA_PATH = "./data/"
TRAIN_CLEAN_DATA = 'train_clean.csv'

train_data = pd.read_csv(DATA_PATH + TRAIN_CLEAN_DATA)

sentence_tf = list(train_data['sentence'])
y_tf = np.array(train_data['emotion'])

vectorizer_t = TfidfVectorizer(min_df = 0.0, analyzer="char", sublinear_tf=True, ngram_range=(1,3), max_features=5000)

train_data_features_tf = vectorizer_t.fit_transform(sentence_tf)

"""### training"""

TEST_SIZE = 0.2
RANDOM_SEED = 42

train_input, eval_input, train_label, eval_label = train_test_split(train_data_features_tf, y_tf, test_size = TEST_SIZE, random_state=RANDOM_SEED)

# random forest

from sklearn.ensemble import RandomForestClassifier

forest_tf = RandomForestClassifier(n_estimators = 100)

forest_tf.fit(train_input, train_label)

# logistic regression

from sklearn.linear_model import LogisticRegression

lgs_tf = LogisticRegression(class_weight='balanced')
lgs_tf.fit(train_input, train_label)

print("Accuracy tf forest  : %f"%forest_tf.score(eval_input, eval_label))
print("Accuracy tf logistic: %f"%lgs_tf.score(eval_input, eval_label))

"""### testing"""

test_sentences = list(test_data['sentence'])
real_emotion = list(test_data['emotion'])

test_data_features = vectorizer_t.transform(test_sentences)

result_forest = forest_tf.predict(test_data_features)
result_lgs = lgs_tf.predict(test_data_features)

output_forest = pd.DataFrame(data = {"expected":result_forest, "real": real_emotion, "sentence": test_sentences})
output_lgs = pd.DataFrame(data = {"expected":result_lgs, "real": real_emotion, "sentence": test_sentences})

print("forest:")
print(output_forest)
print("\nlgs:")
print(output_lgs)

# output.to_csv("BlackCat_Expect.csv", index=False, quoting=3)

"""# word2vec - CBOW

### Embedding
"""

DATA_PATH = "./data/"
TRAIN_CLEAN_DATA = 'train_clean.csv'

train_data = pd.read_csv(DATA_PATH + TRAIN_CLEAN_DATA)

sentence = list(train_data['sentence'])
emotion = list(train_data['emotion'])

sentences = []
for st in sentence:
  sentences.append(st.split())

# 학습 시 필요한 하이퍼파라미터
num_features = 300        # 워드 벡터 특징값 수
min_word_count = 10       # 단어에 대한 최소 빈도 수
num_workers = 4           # 프로세스 개수
context = 10              # 컨텍스트 윈도 크기
downsampling = 1e-3       # 다운 샘플링 비율

from gensim.models import word2vec

w2v_cbow_model = word2vec.Word2Vec(sentences, workers = num_workers, size = num_features, min_count = min_word_count, window = context, sample = downsampling, sg = 0)

"""### training"""

def get_features(words, model, num_features):
  # 출력 벡터 초기화
  feature_vector = np.zeros((num_features), dtype=np.float32)

  num_words = 0
  # 어휘 사전 준비
  index2word_set = set(model.wv.index2word)

  for w in words:
    if w in index2word_set:
      num_words += 1
      # 사전에 해당하는 단어에 대해 단어 벡터를 더함
      feature_vector = np.add(feature_vector, model[w])

  # 문장의 단어 수 만큼 나누어 단어 벡터의 평균값을 문장 벡터로 함
  feature_vector = np.divide(feature_vector, num_words)
  return feature_vector

def get_dataset(sentence, model, num_features):
  dataset = list()
  for st in sentence:
    dataset.append(get_features(st, model, num_features))

  sentenceFeatureVecs = np.stack(dataset)

  return sentenceFeatureVecs

test_data_vecs_cbow = get_dataset(sentences, w2v_cbow_model, num_features)

from sklearn.model_selection import train_test_split

X_cbow = test_data_vecs_cbow
y_cbow = np.array(emotion)

del_list = list()
cnt = 0

for i in range(X_cbow.shape[0]):
  x_ = X_cbow[i]
  y_ = y_cbow[i]
  if np.any(np.isnan(x_)):
    cnt += 1
    del_list.append(i)

print(del_list)

for i in range(cnt):
  X_cbow = np.delete(X_cbow, del_list[cnt-i-1], 0)
  y_cbow = np.delete(y_cbow, del_list[cnt-i-1], 0)

print(np.any(np.isnan(X_cbow)))

RANDOM_SEED = 42
TEST_SPLIT = 0.2

X_cbow_train, X_cbow_eval, y_cbow_train, y_cbow_eval = train_test_split(X_cbow, y_cbow, test_size=TEST_SPLIT, random_state=RANDOM_SEED)

from sklearn.linear_model import LogisticRegression

lgs_cbow = LogisticRegression(class_weight='balanced')
lgs_cbow.fit(X_cbow_train, y_cbow_train)

from sklearn.ensemble import RandomForestClassifier

forest_cbow = RandomForestClassifier(n_estimators = 100)

forest_cbow.fit(X_cbow_train, y_cbow_train)

print("Accuracy cbow logistic: %f"%lgs_cbow.score(X_cbow_eval, y_cbow_eval))
print("Accuracy cbow forest  : %f"%forest_cbow.score(X_cbow_eval, y_cbow_eval))

"""### testing"""

test_sentences = list(test_data['sentence'])
real_emotion = list(test_data['emotion'])

test_data_features = get_dataset(test_sentences, w2v_cbow_model, num_features)

result_forest = forest_cbow.predict(test_data_features)
result_lgs = lgs_cbow.predict(test_data_features)

output_forest = pd.DataFrame(data = {"expected":result_forest, "real": real_emotion, "sentence": test_sentences})
output_lgs = pd.DataFrame(data = {"expected":result_lgs, "real": real_emotion, "sentence": test_sentences})

print("forest:")
print(output_forest)
print("\nlgs:")
print(output_lgs)

# output.to_csv("BlackCat_Expect.csv", index=False, quoting=3)

"""# word2vec - skip gram

### Embedding
"""

DATA_PATH = "./data/"
TRAIN_CLEAN_DATA = 'train_clean.csv'

train_data = pd.read_csv(DATA_PATH + TRAIN_CLEAN_DATA)

sentence = list(train_data['sentence'])
emotion = list(train_data['emotion'])

sentences = []
for st in sentence:
  sentences.append(st.split())

# 학습 시 필요한 하이퍼파라미터
num_features = 300        # 워드 벡터 특징값 수
min_word_count = 10       # 단어에 대한 최소 빈도 수
num_workers = 4           # 프로세스 개수
context = 10              # 컨텍스트 윈도 크기
downsampling = 1e-3       # 다운 샘플링 비율

from gensim.models import word2vec

w2v_sg_model = word2vec.Word2Vec(sentences, workers = num_workers, size = num_features, min_count = min_word_count, window = context, sample = downsampling, sg = 1)

"""### training"""

def get_features(words, model, num_features):
  # 출력 벡터 초기화
  feature_vector = np.zeros((num_features), dtype=np.float32)

  num_words = 0
  # 어휘 사전 준비
  index2word_set = set(model.wv.index2word)

  for w in words:
    if w in index2word_set:
      num_words += 1
      # 사전에 해당하는 단어에 대해 단어 벡터를 더함
      feature_vector = np.add(feature_vector, model[w])

  # 문장의 단어 수 만큼 나누어 단어 벡터의 평균값을 문장 벡터로 함
  feature_vector = np.divide(feature_vector, num_words)
  return feature_vector

def get_dataset(sentence, model, num_features):
  dataset = list()
  for st in sentence:
    dataset.append(get_features(st, model, num_features))

  sentenceFeatureVecs = np.stack(dataset)

  return sentenceFeatureVecs

test_data_vecs_sg = get_dataset(sentences, w2v_sg_model, num_features)

from sklearn.model_selection import train_test_split

X_sg = test_data_vecs_sg
y_sg = np.array(emotion)

del_list = list()
cnt = 0

for i in range(X_sg.shape[0]):
  x_ = X_sg[i]
  y_ = y_sg[i]
  if np.any(np.isnan(x_)):
    cnt += 1
    del_list.append(i)

for i in range(cnt):
  X_sg = np.delete(X_sg, del_list[cnt-i-1], 0)
  y_sg = np.delete(y_sg, del_list[cnt-i-1], 0)

print(np.any(np.isnan(X_sg)))

RANDOM_SEED = 42
TEST_SPLIT = 0.2

X_sg_train, X_sg_eval, y_sg_train, y_sg_eval = train_test_split(X_sg, y_sg, test_size=TEST_SPLIT, random_state=RANDOM_SEED)

from sklearn.linear_model import LogisticRegression

lgs_sg = LogisticRegression(class_weight='balanced')
lgs_sg.fit(X_sg_train, y_sg_train)

from sklearn.ensemble import RandomForestClassifier

forest_sg = RandomForestClassifier(n_estimators = 100)
forest_sg.fit(X_sg_train, y_sg_train)

print("Accuracy sg logistic: %f"%lgs_sg.score(X_sg_eval, y_sg_eval))
print("Accuracy sg forest  : %f"%forest_sg.score(X_sg_eval, y_sg_eval))

"""### testing"""

test_sentences = list(test_data['sentence'])
real_emotion = list(test_data['emotion'])

test_data_features = get_dataset(test_sentences, w2v_sg_model, num_features)

result_forest = forest_sg.predict(test_data_features)
result_lgs = lgs_sg.predict(test_data_features)

output_forest = pd.DataFrame(data = {"expected":result_forest, "real": real_emotion, "sentence": test_sentences})
output_lgs = pd.DataFrame(data = {"expected":result_lgs, "real": real_emotion, "sentence": test_sentences})

print("forest:")
print(output_forest)
print("\nlgs:")
print(output_lgs)

# output.to_csv("BlackCat_Expect.csv", index=False, quoting=3)

"""# pretrained word2vec

### Embedding
"""

# 현재 위치에 구글의 사전 훈련된 Word2Vec을 다운로드
!wget "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"

word2vec_eng = gensim.models.KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin.gz", binary=True)

"""### training"""

sentence = list(train_data['sentence'])
emotion = list(train_data['emotion'])

sentences = []
for st in sentence:
  sentences.append(st.split())

def get_features_pre(words, model, num_features, i2ws):
  # 출력 벡터 초기화
  feature_vector = np.zeros((num_features), dtype=np.float32)

  num_words = 0

  for w in words:
    if w in i2ws:
      num_words += 1
      # 사전에 해당하는 단어에 대해 단어 벡터를 더함
      feature_vector = np.add(feature_vector, model[w])

  # 문장의 단어 수 만큼 나누어 단어 벡터의 평균값을 문장 벡터로 함
  feature_vector = np.divide(feature_vector, num_words)
  return feature_vector

def get_dataset_pre(sentence, model, num_features):
  dataset = list()

  # 어휘 사전 준비
  index2word_set = set(model.wv.index2word)

  for st in sentence:
    dataset.append(get_features_pre(st, model, num_features, index2word_set))

  sentenceFeatureVecs = np.stack(dataset)

  return sentenceFeatureVecs

test_data_vecs_pretrained = get_dataset_pre(sentences, word2vec_eng, 300)

from sklearn.model_selection import train_test_split

X_pt = test_data_vecs_pretrained
y_pt = np.array(emotion)

print(np.any(np.isnan(X_pt)))
print(np.all(np.isfinite(X_pt)))

RANDOM_SEED = 42
TEST_SPLIT = 0.2

X_pt_train, X_pt_eval, y_pt_train, y_pt_eval = train_test_split(X_pt, y_pt, test_size=TEST_SPLIT, random_state=RANDOM_SEED)

from sklearn.linear_model import LogisticRegression

lgs_pt = LogisticRegression(class_weight='balanced')
lgs_pt.fit(X_pt_train, y_pt_train)

from sklearn.ensemble import RandomForestClassifier

forest_pt = RandomForestClassifier(n_estimators = 100)
forest_pt.fit(X_pt_train, y_pt_train)

print("Accuracy pt logistic: %f"%lgs_pt.score(X_pt_eval, y_pt_eval))
print("Accuracy pt forest  : %f"%forest_pt.score(X_pt_eval, y_pt_eval))

"""### testing"""

test_sentences = list(test_data['sentence'])
real_emotion = list(test_data['emotion'])

test_data_features = get_dataset_pre(test_sentences, word2vec_eng, 300)

result_forest = forest_pt.predict(test_data_features)
result_lgs = lgs_pt.predict(test_data_features)

output_forest = pd.DataFrame(data = {"expected":result_forest, "real": real_emotion, "sentence": test_sentences})
output_lgs = pd.DataFrame(data = {"expected":result_lgs, "real": real_emotion, "sentence": test_sentences})

print("forest:")
print(output_forest)
print("\nlgs:")
print(output_lgs)

# output.to_csv("BlackCat_Expect.csv", index=False, quoting=3)

"""# pretrained + emotion"""

# 현재 위치에 구글의 사전 훈련된 Word2Vec을 다운로드
!wget "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"

word2vec_eng_expand = gensim.models.KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin.gz", binary=True)

DATA_PATH = "./data/"
TRAIN_CLEAN_DATA = 'train_clean.csv'

train_data = pd.read_csv(DATA_PATH + TRAIN_CLEAN_DATA)

sentence = list(train_data['sentence'])
emotion = list(train_data['emotion'])

sentences = []
for st in sentence:
  sentences.append(st.split())

# 학습 시 필요한 하이퍼파라미터
num_features = 300        # 워드 벡터 특징값 수
min_word_count = 10       # 단어에 대한 최소 빈도 수
num_workers = 4           # 프로세스 개수
context = 10              # 컨텍스트 윈도 크기
downsampling = 1e-3       # 다운 샘플링 비율

from gensim.models import word2vec

# KeyedVectors do not support further training

"""# CBOW setting """

print (1e-3)

from gensim.models import word2vec
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from itertools import product

def get_features(words, model, num_features):
  # 출력 벡터 초기화
  feature_vector = np.zeros((num_features), dtype=np.float32)

  num_words = 0
  # 어휘 사전 준비
  index2word_set = set(model.wv.index2word)

  for w in words:
    if w in index2word_set:
      num_words += 1
      # 사전에 해당하는 단어에 대해 단어 벡터를 더함
      feature_vector = np.add(feature_vector, model[w])

  # 문장의 단어 수 만큼 나누어 단어 벡터의 평균값을 문장 벡터로 함
  feature_vector = np.divide(feature_vector, num_words)
  return feature_vector

def get_dataset(sentence, model, num_features):
  dataset = list()
  for st in sentence:
    dataset.append(get_features(st, model, num_features))

  sentenceFeatureVecs = np.stack(dataset)

  return sentenceFeatureVecs


DATA_PATH = "./data/"
TRAIN_CLEAN_DATA = 'train_clean.csv'

train_data = pd.read_csv(DATA_PATH + TRAIN_CLEAN_DATA)

sentence = list(train_data['sentence'])
emotion = list(train_data['emotion'])

sentences = []
for st in sentence:
  sentences.append(st.split())

max_forest = [[100, 1, 1, 1, 1e-1], [0, 0, 0, 0, 0]]
max_lgs = [[100, 1, 1, 1, 1e-1], [0, 0, 0, 0, 0]]
max_two = [[100, 1, 1, 1, 1e-1], [0, 0, 0, 0, 0]]
max_cat = [[100, 1, 1, 1, 1e-1], [0, 0, 0, 0, 0]]
max_all = [[100, 1, 1, 1, 1e-1], [0, 0, 0, 0, 0]]
 
# 학습 시 필요한 하이퍼파라미터
num_features = 300        # 워드 벡터 특징값 수
min_word_count = 10       # 단어에 대한 최소 빈도 수
num_workers = 4           # 프로세스 개수
context = 10              # 컨텍스트 윈도 크기
downsampling = 1e-3       # 다운 샘플링 비율

items = [[100, 200, 300, 400, 500], 
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
         [1e-1, 1e-2, 1e-3, 1e-4]]

parameter_list = list(product(*items))

urllib.request.urlretrieve("https://drive.google.com/uc?export=download&id=1WBrsz_bimuRZCBEv149hL-PoTi00tHwi", filename="black_cat.txt")
test_data = pd.read_table('black_cat.txt')

test_sentences = list(test_data['sentence'])
real_emotion = list(test_data['emotion'])

parameter_list = parameter_list[14960:]

for p in parameter_list:
  w2v_cbow_model = word2vec.Word2Vec(sentences, workers = p[2], size = p[0], min_count = p[1], window = p[3], sample = p[4], sg = 0)
  test_data_vecs_cbow = get_dataset(sentences, w2v_cbow_model, p[0])

  print(p)

  X_cbow = test_data_vecs_cbow
  y_cbow = np.array(emotion)

  del_list = list()
  cnt = 0

  for i in range(X_cbow.shape[0]):
    x_ = X_cbow[i]
    y_ = y_cbow[i]
    if np.any(np.isnan(x_)):
      cnt += 1
      del_list.append(i)

  for i in range(cnt):
    X_cbow = np.delete(X_cbow, del_list[cnt-i-1], 0)
    y_cbow = np.delete(y_cbow, del_list[cnt-i-1], 0)

  RANDOM_SEED = 42
  TEST_SPLIT = 0.2

  X_cbow_train, X_cbow_eval, y_cbow_train, y_cbow_eval = train_test_split(X_cbow, y_cbow, test_size=TEST_SPLIT, random_state=RANDOM_SEED)

  lgs_cbow = LogisticRegression(class_weight='balanced')
  lgs_cbow.fit(X_cbow_train, y_cbow_train)

  forest_cbow = RandomForestClassifier(n_estimators = 100)
  forest_cbow.fit(X_cbow_train, y_cbow_train)

  score_lgs = lgs_cbow.score(X_cbow_eval, y_cbow_eval)
  score_forest = forest_cbow.score(X_cbow_eval, y_cbow_eval)
  print("Accuracy cbow logistic: %f"%score_lgs)
  print("Accuracy cbow forest  : %f"%score_forest)

  test_data_features = get_dataset(test_sentences, w2v_cbow_model, p[0])
  result_forest = forest_cbow.predict(test_data_features)
  result_lgs = lgs_cbow.predict(test_data_features)

  forest_cnt = 0
  lgs_cnt = 0
  for i in range(5):
    if result_forest[i] == real_emotion[i]:
      forest_cnt += 1
    if result_lgs[i] == real_emotion[i]:
      lgs_cnt += 1

  print("forest: "+str(forest_cnt) + ", lgs: "+str(lgs_cnt))

  if max_forest[1][0] < score_forest :
    max_forest[0] = p
    max_forest[1][0] = score_forest
  
  if max_lgs[1][0] < score_lgs:
    max_lgs[0] = p
    max_lgs[1][0] = score_lgs

  if max_two[1][0]*2 < score_lgs + score_forest:
    max_two[0] = p
    max_two[1][0] = (score_lgs + score_forest)/2

  if max_cat[1][0] < forest_cnt + lgs_cnt:
    max_cat[0] = p
    max_cat[1][0] = forest_cnt + lgs_cnt
  
  if max_all[1][0] * 3 < (forest_cnt + lgs_cnt)/10 + score_forest + score_lgs:
    max_all[0] = p
    max_cat[1][0] = ((forest_cnt + lgs_cnt)/10 + score_forest + score_lgs)/3

print("max forest")
print(max_forest[0])
print(max_forest[1][0])
print("max lgs")
print(max_lgs[0])
print(max_lgs[1][0])
print("max two")
print(max_two[0])
print(max_two[1][0])
print("max cat")
print(max_cat[0])
print(max_cat[1][0])
print("max all")
print(max_all[0])
print(max_all[1][0])