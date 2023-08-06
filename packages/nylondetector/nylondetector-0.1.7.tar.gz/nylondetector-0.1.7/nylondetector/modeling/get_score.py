import os
import sys
import itertools
sys.path.append('../preprocess')

import joblib
import pickle
import numpy as np
import pandas as pd
from konlpy.tag import Komoran
from datetime import datetime as dt
from sklearn.pipeline import Pipeline
from gensim.sklearn_api import D2VTransformer

from text_handling import do_text_ma
from text_handling import make_ngram
from text_handling import text_preproc
from siu_data_preproc import trim_by_length
from siu_data_preproc import transform_date
from siu_data_preproc import extract_hashtags
from siu_data_preproc import hsptl_prsnl_split
from d2v_input_transformer_2 import D2VInputTransformer


def change_date(date: int, form_from='%Y%m%d', form_to='%Y.%m.%d.'):
    """
    :param date: 특정 date
    :param form_from: date의 이전 포맷
    :param form_to: 바뀔 포맷
    """
    return dt.strptime(str(date), form_from).strftime(form_to)


def load_files_df(data_dir: str, keyword_list: list, crawl_date: int):
    """
    :param data_dir: data가 담긴 위치
    :param keyword_list: keyword가 담긴 list
    :param crawl_date: scaper를 실행한 기준 날짜 (ex: 20220408)
    """
    # 1. Make file paths
    file_paths = []
    for keyword in keyword_list:
        keyword = keyword.replace('"', '')
        temp = [os.listdir(f'{data_dir}/{x}/contents') for x in os.listdir(data_dir) if keyword in x]
        temp = [x for x in list(itertools.chain.from_iterable(temp)) if 'rdbl' in x]

        file_paths += temp

    file_paths = [f"{data_dir}/{fn.split('_')[2]}/contents/{fn}" for fn in file_paths]
    file_paths = [x for x in file_paths if change_date(crawl_date, form_to='%Y-%m-%d') in x]
    
    for i, file_path in enumerate(file_paths):
        if i==0:
            df = pd.read_csv(file_path, index_col=0)
        else:
            df_tmp = pd.read_csv(file_path, index_col=0)
            df = pd.concat([df, df_tmp], axis=0)

    # filter NAs and useless veterinary hospitals
    df = df.loc[~df['content'].isna()]
    df = df.loc[df['content'].map(lambda x: '동물병원' not in x)]

    return df.reset_index(drop=True)


def cleanse_df(df: pd.DataFrame, trims: list, crawl_date: int, date_crit: int):
    """
    :param df: load_files_df()의 결과
    :param trims: [trim_low, trim_upp], float
    :param crawl_date: scaper를 실행한 기준 날짜 (ex: 20220408)
    :param date_crit: filtering할 yyyymm, (ex: 202109)

    """
    # 0. Change date format
    crawl_date = change_date(crawl_date)
    date_crit = change_date(date_crit, '%Y%m', '%Y.%m.')
    
    # 1. Cleansing
    df = text_preproc(df, ['name', 'title', 'content'], kor_only=True)

    # 2. Trimming
    df = trim_by_length(df, trims[0], trims[-1])

    # 3. Change date and filter by dates
    df['date'] = transform_date(df['date'], crawl_date)

    date_filter = df['date'].map(lambda x: x[:7] > date_crit)
    df = df.loc[date_filter]

    # 4. Extract hashtags, Split to hospitals and personals
    df['#s'] = extract_hashtags(df['content'], '.*(안과|병원|의원)$')

    hsptl_words = ['병원', '의원', '안과', '공식블로그', '공식']
    excpt_words = ['동물']
    df_hsptl, df_prsnl = hsptl_prsnl_split(df, hsptl_words, excpt_words)

    return df_hsptl, df_prsnl


def make_morph_series(text_col: pd.Series, is_save=True):
    """
    :param text_col: text가 들어있는 dataframe의 column
    :param is_save: save pickle file or not
    """
    tagger = Komoran()
    pos_list = ('NNG', 'NNP', 'NP', 'VV', 'VA')
    stopwords = []

    X_ma = do_text_ma(text_col, tagger, pos_list, stopwords, is_morph='y')

    if is_save:
        save_date = '-'.join(str(dt.today()).split(' '))[:16]
        with open(f'X_ma_{save_date}.pkl', 'wb') as f:
            pickle.dump(X_ma, f)

    return X_ma


def make_embedded_vec(X_ma: pd.Series, ngram_names: list, ngram_ns: list, is_save=True):
    """
    :param X_ma: make_morph_input()의 결과
    :param ngram_names: input으로 들어갈 dataframe의 column 중 ngram들에 대한 column name list,
                        1gram에 해당하는 이름부터 오름차순으로 기재

    :param ngram_ns: 어떠한 ngram들이 존재하는지에 대한 numeric list,
                     ngram_names에 해당하는 ngram_n이 순서대로 들어가야함
    :param is_save: save pickle file or not
    """
    with open('best_params_d2v.pkl', 'rb') as f:
        best_params_d2v = pickle.load(f)

    # set best parameter, and make embedded vector via them
    pipeline_d2v_final = Pipeline([
        ('preproc', D2VInputTransformer(ngram_names, ngram_ns, '1_2_3')),
        ('embed', D2VTransformer())
    ])
    pipeline_d2v_final.set_params(**best_params_d2v)

    doc_embedded_vec = pipeline_d2v_final.fit_transform(X_ma)
    if is_save:
        save_date = '-'.join(str(dt.today()).split(' '))[:16]
        with open(f'doc_embedded_vec_{save_date}.pkl', 'wb') as f:
            pickle.dump(doc_embedded_vec, f)

    return doc_embedded_vec


def make_embedded_df(doc_embedded_vec: np.ndarray, is_save=True):
    """
    :param doc_embedded_vec: make_embedded_vec()의 결과
    :param is_save: save pickle file or not
    """
    doc_embedded_df = pd.DataFrame(doc_embedded_vec)
    doc_embedded_df.columns = ['embed_{}'.format(x) for x in range(doc_embedded_df.shape[1])]

    if is_save:
        save_date = '-'.join(str(dt.today()).split(' '))[:16]
        with open(f'doc_embedded_df_{save_date}.pkl', 'wb') as f:
            pickle.dump(doc_embedded_df, f)

    return doc_embedded_df


def make_input_df(df_hsptl: pd.DataFrame, X_ma: pd.Series):
    """
    :param df_hsptl: cleanse_df()의 결과
    :param X_ma: make_morph_input()의 결과
    """
    # make keyword count dataframe, as robust as possible
    X_ngram = X_ma.map(lambda x: make_ngram(x, 2))
    keyword_cnt_df = pd.concat([df_hsptl['content'].map(lambda x: x.count('실손')).rename('실손'),
                                df_hsptl['content'].map(lambda x: x.count('실비')).rename('실비'),
                                df_hsptl['content'].map(lambda x: x.count('할인')).rename('할인'),
                                df_hsptl['content'].map(lambda x: x.count('혜택')).rename('혜택'),
                                X_ngram.map(lambda x: x.count('실_손')).rename('실_손')], axis=1)

    # make d2v dataframe
    ngram_names = ['content_1gram_1', 'content_2gram', 'content_3gram']
    ngram_ns = [1,2,3]
    doc_embedded_vec = make_embedded_vec(X_ma, ngram_names, ngram_ns)
    doc_embedded_df = make_embedded_df(doc_embedded_vec)
    doc_embedded_df.index = df_hsptl.index

    input_df = pd.concat([keyword_cnt_df, doc_embedded_df], axis=1)
    return input_df


def get_scored_df(df_hsptl: pd.DataFrame, input_df: pd.DataFrame, model_path: str):
    """
    :param df_hsptl: cleanse_df()의 결과
    :param input_df: make_input_df()의 결과
    :param model_path: 학습시킨 모델의 path (ex: 'siu_clf_ver2.sav')
    """
    best_model_clf = joblib.load(model_path)

    label = best_model_clf.predict(input_df)
    score = [x[1] for x in best_model_clf.predict_proba(input_df)]
    
    scored_df = df_hsptl
    scored_df['label'] = label
    scored_df['score'] = score
    
    return scored_df

