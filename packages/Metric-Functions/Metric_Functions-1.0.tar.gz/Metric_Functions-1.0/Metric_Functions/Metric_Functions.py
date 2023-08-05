#!/usr/bin/env python
# coding: utf-8

# Created on 07/28/2021
#
# @author: Chao LI
#
# Description:
# The monitoring and evaluation of the impact of TPS look-fors
#
# how do we link Teacher PD to Look-fors,
#
# how do we link Look-fors to Reading Fluency Growth
#
# how do we link Reading Fluency to MAP 3 windows
#
# -Does simple regression/correlation good enough?  or do we need more robust research?
#
# -Do we need/want to use other algorithms?
#
# NOTE:
#
# we need to balance time and value; we need relative confident answers as a quick win.
# - need to change this one to py file for modular use.  But need to remember update

# In[1]:


import pandas as pd
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
import pingouin as pg
from factor_analyzer.factor_analyzer import calculate_kmo
from itertools import cycle
import numpy as np
from numpy import nan
import random
from scipy import stats
import seaborn as sb
from scipy.stats import pearsonr
from scipy.stats import chi2_contingency
import statsmodels.api as sm


# # Reading Fluency data

# ## Binalize Data Prepare function

# In[ ]:


def binalize_test_item(df):
    '''
    This function binalize the performance level to 0 or 1 for each test item
    and each test item's binaral score; and use the overal proficiency score to indicate if the
    student is majority_proficient
    INPUT:
    df - the cleaned, test item 1/0 binalized RF data

    OUTPUT:
    df - with 2 extra columns: proficient_level with proficient score of the student;
                            proficient_majority with the majority proficient score 1/0 of the student
    '''

    df_trim = df

    df_trim = df_trim.replace('Approaching Expectation', 0)
    df_trim = df_trim.replace('Below Expectation', 0)
    df_trim = df_trim.replace('Exceeds Expectation', 1)
    df_trim = df_trim.replace('Meets Expectation', 1)
    # what does "no score" means?
    df_trim = df_trim.replace('No Score', 0)

    #how to distinguish no expectation from not-taking?--give it a number which would not mix with others
    df_trim = df_trim.replace('No Expectation', 2)

    df_trim.loc[df_trim['ProgressMonitoringAccuracyScore'] >= 0.5,
                'ProgressMonitoringAccuracyScore'] = 1
    df_trim.loc[df_trim['ProgressMonitoringAccuracyScore'] < 0.5,
                'ProgressMonitoringAccuracyScore'] = 0
    df_trim['ProgressMonitoringComprehension'] = df_trim[
        'ProgressMonitoringComprehensionCorrect'] / df_trim[
            'ProgressMonitoringComprehensionAttempted']
    df_trim.loc[df_trim['ProgressMonitoringComprehension'] >= 0.5,
                'ProgressMonitoringComprehension'] = 1
    df_trim.loc[df_trim['ProgressMonitoringComprehension'] < 0.5,
                'ProgressMonitoringComprehension'] = 0
    df_trim = df_trim.drop([
        'ProgressMonitoringComprehensionCorrect',
        'ProgressMonitoringComprehensionAttempted'
    ],
                           axis=1)
    df_trim["Grade"].replace({"K": 0}, inplace=True)
    df_trim['Grade'] = pd.to_numeric(df_trim['Grade'], errors='coerce')

    return df_trim


# ## get_proficient_level Function

# In[ ]:


routed_items = [
    'ListeningComprehensionPerformanceLevel', 'PictureVocabPerformanceLevel'
]

foundational_begin = [
    'PictureVocabPerformanceLevel', 'PhonologicalAwarenessPerformanceLevel',
    'PhonicsWordRecognitionPerformanceLevel',
    'ListeningComprehensionPerformanceLevel', 'PrintConceptPerformanceLevel'
]

foundational_items_1to5 = [
    'PictureVocabPerformanceLevel', 'PhonologicalAwarenessPerformanceLevel',
    'PhonicsWordRecognitionPerformanceLevel',
    'ListeningComprehensionPerformanceLevel',
    'SentenceReadingFluencyPerformanceLevel'
]

# SentenceReadingFluencyPerformanceLevel is not expected, but some K took it and exceeded it.
foundational_items_k = [
    'PictureVocabPerformanceLevel', 'PhonologicalAwarenessPerformanceLevel',
    'PhonicsWordRecognitionPerformanceLevel',
    'ListeningComprehensionPerformanceLevel'
]
# same as oral_items_begin
oral_items_1to5 = [
    'OralReadingRatePerformanceLevel', 'OralReadingAccuracyPerformanceLevel',
    'LiteralComprehensionPerformanceLevel',
    'SentenceReadingFluencyPerformanceLevel'
]

# did not see not expected for K for SentenceReadingFluencyPerformanceLevel, but some K took it and exceeded--NEED CHECK
oral_items_k = [
    'OralReadingRatePerformanceLevel', 'OralReadingAccuracyPerformanceLevel',
    'LiteralComprehensionPerformanceLevel'
]
progress_items = [
    'ProgressMonitoringAccuracyScore', 'ProgressMonitoringComprehension'
]


# In[ ]:


def get_proficient_level(df):
    '''
    This function calculate the overal proficieny score of each student based upon his test type
    and each test item's binaral score; and use the overal proficiency score to indicate if the
    student is majority_proficient
    INPUT:
    df - the cleaned, test item 1/0 binalized RF data

    OUTPUT:
    df - with 2 extra columns: proficient_level with proficient score of the student;
                            proficient_majority with the majority proficient score 1/0 of the student
    '''

    # create new columns for proficient_level and for proficient_majority

    df['proficient_level'] = np.nan
    df['proficient_majority'] = np.nan

    # calculate proficient_level of Routed testers
    mask_routed = ((df['ResultType'] == 'Oral Reading') &
                   ((df['ListeningComprehensionPerformanceLevel'].notnull()) |
                    (df['PictureVocabPerformanceLevel'].notnull())))

    # change test type indicator for later use
    df.loc[mask_routed, 'ResultType'] = 'Routed'

    df.loc[mask_routed,
           'proficient_level'] = (df[routed_items].sum(axis=1)) / 2

    # calculate proficient_level of Foundational testers Grade 1-5 without "No Expectation", not beginners
    df.loc[((df['ResultType'] == 'Foundational Skills') &
            (df['AssignedTestType'] != 'Foundational Skills Beginner') &
            (df['SentenceReadingFluencyPerformanceLevel'] != 2)),
           'proficient_level'] = (df[foundational_items_1to5].sum(axis=1)) / 5

    # calculate proficient_level of Foundational testers Grade k with "No Expectation", not beginners
    df.loc[((df['ResultType'] == 'Foundational Skills') &
            (df['AssignedTestType'] != 'Foundational Skills Beginner') &
            (df['SentenceReadingFluencyPerformanceLevel'] == 2)),
           'proficient_level'] = (df[foundational_items_k].sum(axis=1)) / 4

    # calculate proficient_level of Foundational beginners testers
    df.loc[((df['ResultType'] == 'Foundational Skills') &
            (df['AssignedTestType'] == 'Foundational Skills Beginner')),
           'proficient_level'] = (df[foundational_begin].sum(axis=1)) / 5

    # calculate proficient_level of Oral-one-track testers Grade 1-5 without "No Expectation"
    mask_oral = ((df['ResultType'] == 'Oral Reading') &
                 (df['ListeningComprehensionPerformanceLevel'].isnull()) &
                 (df['PictureVocabPerformanceLevel'].isnull()))

    df.loc[(mask_oral & (df['SentenceReadingFluencyPerformanceLevel'] != 2)),
           'proficient_level'] = (df[oral_items_1to5].sum(axis=1)) / 4

    # calculate proficient_level of Oral-one-track testers Grade k with "No Expectation"
    df.loc[(mask_oral & (df['SentenceReadingFluencyPerformanceLevel'] == 2)),
           'proficient_level'] = (df[oral_items_k].sum(axis=1)) / 3

    # calculate proficient_level of Progress Monitoring testers
    df.loc[(df['ResultType'] == 'Progress Monitoring'),
           'proficient_level'] = (df[progress_items].sum(axis=1)) / 2

    df.loc[df['proficient_level'] >= 0.5, 'proficient_majority'] = 1
    df.loc[df['proficient_level'] < 0.5, 'proficient_majority'] = 0
    return df

# # LF & RF

# ## Get session majority_proficient percentage
def get_class_prf_perc(df):
    '''
    This function calculate percentage of students who made RF majority proficient
    over all tested students per class session.

    INPUT:
    df - df_fluency_prf_sum_w2: schoolid, sectionid, ResultType, StudentID_count, proficient_majority_sum

    OUTPUT:
    _CLASS_PRF_PERC - a 2 layer dictionary: schoolid over sectionid over percentage

    denominator:sum(Foundational count + Oral count + Progress count + Routed count)*3
        --all testers theoretical chances of "being proficient at each of the 3 levels"
    numerator: sum(Foundational proficient + Oral count +Progress count + Routed proficient
                +Oral proficient + Progress count + Progress proficient)
        --testers' real count of "being proficient" at each level. e.g. a Oral tester being proficient
        at the Oral test means he is proficient with both Foundational and Oral
    '''
    CLASS_RANGE = df.groupby('schoolid')['sectionid'].agg(
    list).to_dict()

    _CLASS_PRF_PERC = {}

    for school, classrooms in CLASS_RANGE.items():
        _CLASS_PRF_PERC[school] = {}

        for classroom in classrooms:
            _CLASS_PRF_PERC[school][classroom] = []
            df_3types_de = df
            df_grade_class = df_3types_de[
                (df_3types_de['schoolid'] == school)
                & (df_3types_de['sectionid'] == classroom)]

            denominator = (df_grade_class['StudentID_count'].sum()) * 3

            numerator_f = df_grade_class[
                df_grade_class['ResultType'] ==
                'Foundational Skills']['proficient_majority_sum']
            if numerator_f.empty:
                numerator_f = 0
            else:
                numerator_f = numerator_f.values[0]

            numerator_o = (
                (df_grade_class[df_grade_class['ResultType'] == 'Oral Reading']
                 ['StudentID_count']) +
                (df_grade_class[df_grade_class['ResultType'] == 'Oral Reading']
                 ['proficient_majority_sum']))

            if numerator_o.empty:
                numerator_o = 0
            else:
                numerator_o = numerator_o.values[0]

            numerator_p = (
                (df_grade_class[df_grade_class['ResultType'] ==
                                'Progress Monitoring']['StudentID_count']) * 2
                + (df_grade_class[df_grade_class['ResultType'] ==
                                  'Progress Monitoring']
                   ['proficient_majority_sum']))

            if numerator_p.empty:
                numerator_p = 0
            else:
                numerator_p = numerator_p.values[0]

            numerator_r = df_grade_class[df_grade_class['ResultType'] ==
                                         'Routed']['proficient_majority_sum']

            if numerator_r.empty:
                numerator_r = 0
            else:
                numerator_r = numerator_r.values[0]

            numerator = numerator_f + numerator_o + numerator_p + numerator_r

            _CLASS_PRF_PERC[school][classroom] = numerator / denominator

    return _CLASS_PRF_PERC

# ## Binalize Data Prepare function
def observer_ttest(df, look_for_indicator, group_type):
    '''
    This function do t-test between schoolleader observation results vs. district  observation results
    to see if these 2 groups are significantly different.

    INPUT:
    df - the dataframe with observation results: answer, observation_id
    look_for_indicator - which look_for id to test
    group_type - how to treat the 2 groups of data
        ind: treat 2 groups as independent/unrelated groups, so use ttest_ind function
        join: treat 2 groups as related groups and therefore find the merger with same sections
        both: treat 2 groups as related groups and find the very merge of both same sections and same dates of observations

    OUTPUT:
    Ttest_relResult - statistic and pvalue
    '''
    df_lookfor_test = df[df['look_for'] == look_for_indicator].drop(
        ['school_id', 'observation_id', 'look_for'], axis=1)
    df_lookfor_test_sl = df_lookfor_test[df_lookfor_test['observer_role'] ==
                                         1].drop(['observer_role'], axis=1)
    df_lookfor_test_dis = df_lookfor_test[df_lookfor_test['observer_role'] ==
                                          0].drop(['observer_role'], axis=1)

    if group_type == 'ind':
        df_lookfor_test_sl = df_lookfor_test_sl['answer']
        df_lookfor_test_dis = df_lookfor_test_dis['answer']
        return stats.ttest_ind(df_lookfor_test_sl, df_lookfor_test_dis)
    elif group_type == 'join':
        section_list_dis = df_lookfor_test_dis['section_id'].unique().tolist()
        df_lookfor_test_sl = df_lookfor_test_sl[
            df_lookfor_test_sl['section_id'].isin(
                section_list_dis)].reset_index(drop=True)['answer']
        df_lookfor_test_dis = df_lookfor_test_dis['answer']

        #usually sl observations are more than district observation
        df_lookfor_test_sl_sample = df_lookfor_test_sl.sample(
            n=(len(df_lookfor_test_dis.index)))

        return stats.ttest_rel(df_lookfor_test_sl_sample, df_lookfor_test_dis)
    else:
        df_lookfor_test_both = pd.merge(df_lookfor_test_dis,
                                        df_lookfor_test_sl,
                                        how='inner',
                                        on=['section_id', 'date'
                                            ]).drop(['date', 'section_id'],
                                                    axis=1)
        return stats.ttest_rel(df_lookfor_test_both['answer_x'],
                               df_lookfor_test_both['answer_y'])

# ## district observation vs. SL chi-square
def observer_chisquare(df, look_for_indicator, group_type):
    '''
    This function do chi-square test between schoolleader observation results vs. district  observation results
    to see if these 2 groups are significantly different.

    INPUT:
    df - the dataframe with observation results: answer, observation_id
    look_for_indicator - which look_for id to test
    group_type - how to treat the 2 groups of data
        ind: treat 2 groups as independent/unrelated groups, so use ttest_ind function
        join: treat 2 groups as related groups and therefore find the merger with same sections
        both: treat 2 groups as related groups and find the very merge of both same sections and same dates of observations

    OUTPUT:
    chi2_contingency - statistic, pvalue and degree of freedom
    '''
    df_lookfor_test = df[df['look_for'] == look_for_indicator].drop(
        ['school_id', 'look_for'], axis=1)
    df_lookfor_test_sl = df_lookfor_test[df_lookfor_test['observer_role'] == 1]
    df_lookfor_test_dis = df_lookfor_test[df_lookfor_test['observer_role'] ==
                                          0]

    if group_type == 'ind':
        chisqt = pd.crosstab(df_lookfor_test.observer_role,
                             df_lookfor_test.answer)

    elif group_type == 'join':
        section_list_dis = df_lookfor_test[df_lookfor_test['observer_role'] ==
                                           0]['section_id'].unique().tolist()
        df_lookfor_test = df_lookfor_test[df_lookfor_test['section_id'].isin(
            section_list_dis)]
        chisqt = pd.crosstab(df_lookfor_test.observer_role,
                             df_lookfor_test.answer)

    else:
        df_lookfor_test_both = pd.merge(df_lookfor_test_dis,
                                        df_lookfor_test_sl,
                                        how='inner',
                                        on=['section_id', 'date'
                                            ]).drop(['date', 'section_id'],
                                                    axis=1)

        observation_list = df_lookfor_test_both['observation_id_x'].unique(
        ).tolist()
        observation_list_b = df_lookfor_test_both['observation_id_y'].unique(
        ).tolist()
        observation_list.extend(observation_list_b)

        df_lookfor_test = df_lookfor_test[
            df_lookfor_test['observation_id'].isin(observation_list)]

        chisqt = pd.crosstab(df_lookfor_test.observer_role,
                             df_lookfor_test.answer)

    value = np.array([chisqt.iloc[0][0:3].values, chisqt.iloc[1][0:3].values])

    return chi2_contingency(value)[0:3], chisqt

# ## district observation vs. SL logistic regression
def observer_logistic(df, look_for_indicator, group_type):
    '''
    This function do Single-variate logistic regression test between schoolleader observation results vs. district  observation results
    to see if these 2 groups are significantly different.

    INPUT:
    df - the dataframe with observation results: answer, observation_id
    look_for_indicator - which look_for id to test
    group_type - how to treat the 2 groups of data
        ind: treat 2 groups as independent/unrelated groups, so use ttest_ind function
        join: treat 2 groups as related groups and therefore find the merger with same sections
        both: treat 2 groups as related groups and find the very merge of both same sections and same dates of observations

    OUTPUT:
    summary2 - logistic regression report
    '''
    df_lookfor_test = df[df['look_for'] == look_for_indicator].drop(
        ['school_id', 'look_for'], axis=1)
    df_lookfor_test_sl = df_lookfor_test[df_lookfor_test['observer_role'] == 1]
    df_lookfor_test_dis = df_lookfor_test[df_lookfor_test['observer_role'] ==
                                          0]

    if group_type == 'join':
        section_list_dis = df_lookfor_test[df_lookfor_test['observer_role'] ==
                                           0]['section_id'].unique().tolist()
        df_lookfor_test = df_lookfor_test[df_lookfor_test['section_id'].isin(
            section_list_dis)]

    elif group_type == 'both':
        df_lookfor_test_both = pd.merge(df_lookfor_test_dis,
                                        df_lookfor_test_sl,
                                        how='inner',
                                        on=['section_id', 'date'
                                            ]).drop(['date', 'section_id'],
                                                    axis=1)

        observation_list = df_lookfor_test_both['observation_id_x'].unique(
        ).tolist()
        observation_list_b = df_lookfor_test_both['observation_id_y'].unique(
        ).tolist()
        observation_list.extend(observation_list_b)

        df_lookfor_test = df_lookfor_test[
            df_lookfor_test['observation_id'].isin(observation_list)]

    else:
        df_lookfor_test = df_lookfor_test

    X = df_lookfor_test.observer_role.to_numpy()
    X = X.reshape(-1, 1)
    Y = df_lookfor_test.answer

    #lr = LogisticRegression()

    #result = lr.fit(X, Y)
    logit_model = sm.Logit(Y, X)
    result = logit_model.fit()

    return result.summary2()

# # RF & MAP

# ## Get_fraction function

# In[ ]:


def get_fraction(df):
    '''
    This function calculate the fraction and transform performancelevel to scores of each test item based upon test type

    INPUT:
    df - the cleaned, test item RF data without binalization

    OUTPUT:
    df - with 2 extra columns: proficient_level with proficient score of the student;
                            proficient_majority with the majority proficient score 1/0 of the student
    '''

    # calculate fractions
    df['Print'] = df['PrintConceptCorrect'] / df['PrintConceptAttempted']
    df['Listening'] = df['ListeningComprehensionCorrect'] / df[
        'ListeningComprehensionAttempted']
    df['Picture'] = df['PictureVocabCorrect'] / df['PictureVocabAttempted']
    df['SentenceReading'] = df['SentenceReadingFluencyCorrect'] / df[
        'SentenceReadingFluencyAttempted']
    df['ProgressMonitoringComprehension'] = df[
        'ProgressMonitoringComprehensionCorrect'] / df[
            'ProgressMonitoringComprehensionAttempted']

    #replace the performancelevel with scores--MAY THINK ABOUT THE NUMBER PICK
    df = df.replace('Approaching Expectation', 0)
    df = df.replace('Below Expectation', -1)
    df = df.replace('Exceeds Expectation', 2)
    df = df.replace('Meets Expectation', 1)
    df = df.replace('No Score', np.nan)
    #under OralReadingWCPM, there is a 170+
    df = df.replace('170+', 170)

    #do not need to deal with 'No Expectation' since it is not in LiteralComprehensionPerformanceLevel

    #drop unused columns
    df = df.drop([
        'PrintConceptCorrect', 'PrintConceptAttempted',
        'ListeningComprehensionCorrect', 'ListeningComprehensionAttempted',
        'PictureVocabCorrect', 'PictureVocabAttempted',
        'SentenceReadingFluencyCorrect', 'SentenceReadingFluencyAttempted',
        'ProgressMonitoringComprehensionCorrect',
        'ProgressMonitoringComprehensionAttempted'
    ],
                 axis=1)

    # Found Routed testers
    mask_routed = ((df['ResultType'] == 'Oral Reading') &
                   ((df['Listening'].notnull()) | (df['Picture'].notnull())))

    # change test type indicator for later use
    df.loc[mask_routed, 'ResultType'] = 'Routed'

    # change foundational beginner testers test type indicator for later use
    df.loc[df['AssignedTestType'] == 'Foundational Skills Beginner',
           'ResultType'] = 'Foundational Beginner'

    # do not need to deal with Foundational K testers or Oral_k testers since they just have NA for their No expectation scores

    return df


# ## pvalue Function

# In[ ]:


def calculate_pvalues(df, col):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
    return pvalues.loc[:, col]


# ## Item correlation function_outdated

# In[ ]:


def proficiency_corr_testitem(df_RF, df_map, test_type):
    '''
      INPUT
      df_RF - pandas dataframe of Reading Fluency, may separate in different types
      df_map - pandas dataframe of MAP
      test_type - 'Foundational Skills', 'Oral Reading', 'Progress Monitoring', 'Routed','all'

      OUTPUT
      correlation - A matrix holding the correlation coefficiencies between columns

      pvalue - P value for the correlations
      cannot do all since all will drop all na rows.
      '''

    if test_type == 'Foundational Skills':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Foundational Skills')].drop(
            [
                'ProgressMonitoringAccuracyScore',
                'ProgressMonitoringComprehension', 'ProgressMonitoringWCPM',
                'OralReadingWCPM', 'OralReadingAccuracyScore', 'Print',
                'LiteralComprehensionPerformanceLevel', 'AssignedTestType',
                'ResultType'
            ],
            axis=1)

    if test_type == 'Foundational Beginner':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Foundational Beginner')].drop(
            [
                'ProgressMonitoringAccuracyScore',
                'ProgressMonitoringComprehension', 'ProgressMonitoringWCPM',
                'OralReadingWCPM', 'OralReadingAccuracyScore',
                'SentenceReading', 'LiteralComprehensionPerformanceLevel',
                'AssignedTestType', 'ResultType'
            ],
            axis=1)

    if test_type == 'Oral Reading':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Oral Reading')].drop([
            'ProgressMonitoringAccuracyScore',
            'ProgressMonitoringComprehension', 'ProgressMonitoringWCPM',
            'PhonologicalAwarenessZPDLevel', 'PhonicsWordRecognitionZPDLevel',
            'Listening', 'Picture', 'Print', 'AssignedTestType', 'ResultType'
        ],
                                                                    axis=1)

    if test_type == 'Progress Monitoring':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Progress Monitoring')].drop(
            [
                'PhonologicalAwarenessZPDLevel',
                'PhonicsWordRecognitionZPDLevel', 'Listening', 'Picture',
                'SentenceReading', 'OralReadingWCPM', 'Print',
                'OralReadingAccuracyScore',
                'LiteralComprehensionPerformanceLevel', 'AssignedTestType',
                'ResultType'
            ],
            axis=1)

    if test_type == 'Routed':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Routed')].drop([
            'PhonologicalAwarenessZPDLevel', 'PhonicsWordRecognitionZPDLevel',
            'ProgressMonitoringAccuracyScore', 'Print',
            'ProgressMonitoringComprehension', 'ProgressMonitoringWCPM',
            'AssignedTestType', 'ResultType'
        ],
                                                              axis=1)

    #merge in testpercentile--currently, random merge in the top RF if sester has multiple RF scores--NEED UPDATE
    df_mp = pd.merge(df_map[['student_number', 'testpercentile', 'grade']],
                     df_RF,
                     how='inner',
                     left_on='student_number',
                     right_on='StudentID')

    #drop unused column
    df_map_corr = df_mp.drop(['StudentID', 'student_number'], axis=1)

    #calculate correlation
    correlation = df_map_corr.corr().testpercentile
    #calculate pvalue
    pvalue = calculate_pvalues(df_map_corr, "testpercentile")

    return correlation, pvalue


# ## Item correlation function-upgrade

# In[ ]:


def testitem_corr_map(df_RF, df_map, test_type, map_corr):
    '''
      This function calculate the correlation scores between Reading_Fluency test items/scores to MAP static: testpercentile
      or MAP dynamic: progress

      INPUT
      df_RF - pandas dataframe of Reading Fluency, may separate in different types
      df_map - pandas dataframe of MAP
      test_type - 'Foundational Skills', 'Oral Reading', 'Progress Monitoring', 'Routed','all'
      map_corr - 'testpercentile', map_rit_progress', 'map_pro_progress', 'map_qtile_progress',
      'map_mgrowth_progress','map_growth_progress', 'map_goal_rit_progress'

      OUTPUT
      correlation - A matrix holding the correlation coefficiencies between columns

      pvalue - P value for the correlations
      cannot do all since all will drop all na rows.
      '''

    if test_type == 'Foundational Skills':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Foundational Skills')].drop(
            [
                'ProgressMonitoringAccuracyScore',
                'ProgressMonitoringComprehension', 'ProgressMonitoringWCPM',
                'OralReadingWCPM', 'OralReadingAccuracyScore', 'Print',
                'LiteralComprehensionPerformanceLevel', 'AssignedTestType',
                'ResultType'
            ],
            axis=1)

    if test_type == 'Foundational Beginner':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Foundational Beginner')].drop(
            [
                'ProgressMonitoringAccuracyScore',
                'ProgressMonitoringComprehension', 'ProgressMonitoringWCPM',
                'OralReadingWCPM', 'OralReadingAccuracyScore',
                'SentenceReading', 'LiteralComprehensionPerformanceLevel',
                'AssignedTestType', 'ResultType'
            ],
            axis=1)

    if test_type == 'Oral Reading':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Oral Reading')].drop([
            'ProgressMonitoringAccuracyScore',
            'ProgressMonitoringComprehension', 'ProgressMonitoringWCPM',
            'PhonologicalAwarenessZPDLevel', 'PhonicsWordRecognitionZPDLevel',
            'Listening', 'Picture', 'Print', 'AssignedTestType', 'ResultType'
        ],
                                                                    axis=1)

    if test_type == 'Progress Monitoring':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Progress Monitoring')].drop(
            [
                'PhonologicalAwarenessZPDLevel',
                'PhonicsWordRecognitionZPDLevel', 'Listening', 'Picture',
                'SentenceReading', 'OralReadingWCPM', 'Print',
                'OralReadingAccuracyScore',
                'LiteralComprehensionPerformanceLevel', 'AssignedTestType',
                'ResultType'
            ],
            axis=1)

    if test_type == 'Routed':
        # calculate personal overal majority_proficient score
        df_RF = df_RF[(df_RF['ResultType'] == 'Routed')].drop([
            'PhonologicalAwarenessZPDLevel', 'PhonicsWordRecognitionZPDLevel',
            'ProgressMonitoringAccuracyScore', 'Print',
            'ProgressMonitoringComprehension', 'ProgressMonitoringWCPM',
            'AssignedTestType', 'ResultType'
        ],
                                                              axis=1)

    #merge in testpercentile--currently, random merge in the top RF if sester has multiple RF scores--NEED UPDAT
    df_mp = pd.merge(df_map[['student_number', map_corr, 'grade_level']],
                     df_RF,
                     how='inner',
                     left_on='student_number',
                     right_on='StudentID')

    #drop unused column
    df_map_corr = df_mp.drop(['StudentID', 'student_number'], axis=1)

    #calculate correlation
    correlation = df_map_corr.corr()[map_corr]
    #calculate pvalue
    pvalue = calculate_pvalues(df_map_corr, map_corr)

    return correlation, pvalue


# ## proficient_score Function

# In[ ]:


def get_proficient_score(df_RF, proficient_type):
    '''
      This function calculate Reading Fluency proficient_score for different testtypes,
      considering testtype scale. and for proficient_majority or all_proficient

      INPUT
      df_RF - pandas dataframe of Reading Fluency
      proficient_type - "proficient_majority" or "all_proficient"

      OUTPUT
      df - with 1 extra column: proficient_score per student; 0-1;
            no matter which test type the tester participated, weighted.

    '''

    df_RF['proficient_score'] = 0
    denominator = 4

    if proficient_type == 'proficient_majority':
        # calculate personal overal majority_proficient score
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Beginner'),
                  'proficient_score'] = df_RF['proficient_majority']
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Skills'),
                  'proficient_score'] = df_RF['proficient_majority'] + 1
        df_RF.loc[(df_RF['ResultType'] == 'Oral Reading'),
                  'proficient_score'] = df_RF['proficient_majority'] + 2
        df_RF.loc[(df_RF['ResultType'] == 'Progress Monitoring'),
                  'proficient_score'] = df_RF['proficient_majority'] + 3
        df_RF.loc[(df_RF['ResultType'] == 'Routed'),
                  'proficient_score'] = df_RF['proficient_majority'] + 1

        #calculate an interim proficient_score
        df_RF['proficient_score'] = (df_RF['proficient_score']) / denominator


    if proficient_type == 'all_proficient':
        #use proficient_level column to show if all_proficient
        df_RF.loc[df_RF['proficient_level'] < 1, 'proficient_level'] = 0

        # calculate personal overal all_proficient score; the presumption is if
        # go to next level, the previous level is all_proficient--may think about it
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Beginner'),
                  'proficient_score'] = df_RF['proficient_level']
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Skills'),
                  'proficient_score'] = df_RF['proficient_level'] + 1
        df_RF.loc[(df_RF['ResultType'] == 'Oral Reading'),
                  'proficient_score'] = df_RF['proficient_level'] + 2
        df_RF.loc[(df_RF['ResultType'] == 'Progress Monitoring'),
                  'proficient_score'] = df_RF['proficient_level'] + 3
        df_RF.loc[(df_RF['ResultType'] == 'Routed'),
                  'proficient_score'] = df_RF['proficient_level'] + 1

        #calculate an interim proficient_score
        df_RF['proficient_score'] = (df_RF['proficient_score']) / denominator

    return df_RF


# ## get_progress Function

# In[ ]:


def get_progress_score(df_RF_1, df_RF_2):
    '''
      This function is for testing dynamic state correlation.  It calculates the progress between 2 windows
      of RF by finding the difference of proficient_score, which is scaled based on testtype changes.

      INPUT
      df_RF_1 - pandas dataframe of Reading Fluency previous window
      df_RF_2 - pandas dataframe of Reading Fluency later window

      OUTPUT
      df - with 2 vars: 'StudentID', 'proficient_progress'
            "proficient_progress" is the difference the "proficient_score"
            or 2 RF df

    '''
    df_RF_1 = df_RF_1[['StudentID', 'proficient_score']].rename(
            columns={
                "proficient_score": "proficient_score_1",
            })
    df_RF_2 = df_RF_2[['StudentID', 'proficient_score']].rename(
            columns={
                "proficient_score": "proficient_score_2",
            })

    #find the testers who took both tests
    df_RF_both = pd.merge(df_RF_1,
                         df_RF_2,
                         how='inner',
                         on='StudentID')

    df_RF_both['rf_pro_progress'] = df_RF_both['proficient_score_2'] - df_RF_both['proficient_score_1']
    df_RF_both = df_RF_both.drop(['proficient_score_1', 'proficient_score_2'], axis=1)

    return df_RF_both


# ## get_item_progress Function

# In[1]:


def get_item_progress(df_RF_1, df_RF_2):
    '''
      This function calculates those RF of the same testtypes in 2 windows, the progress of each test items.

      INPUT
      df_RF_1 - pandas dataframe of Reading Fluency previous window with all the items
      df_RF_2 - pandas dataframe of Reading Fluency later window with all the items

      OUTPUT
      df - with 2 vars: 'StudentID', 'proficient_progress'
            "proficient_progress" is the difference the "proficient_score"
            or 2 RF df

    '''
    #find out the testers who took both tests and took the same test types
    df_RF_item_both = pd.merge(df_RF_1.drop(['AssignedTestType'], axis=1),
                               df_RF_2,
                               how='inner',
                               on=['StudentID', 'ResultType'])

    #find the progress made in each test item
    df_RF_item_both[
        'Print'] = df_RF_item_both['Print_y'] - df_RF_item_both['Print_x']
    df_RF_item_both['Listening'] = df_RF_item_both[
        'Listening_y'] - df_RF_item_both['Listening_x']
    df_RF_item_both['Picture'] = df_RF_item_both[
        'Picture_y'] - df_RF_item_both['Picture_x']
    df_RF_item_both['SentenceReading'] = df_RF_item_both[
        'SentenceReading_y'] - df_RF_item_both['SentenceReading_x']
    df_RF_item_both['ProgressMonitoringComprehension'] = df_RF_item_both[
        'ProgressMonitoringComprehension_y'] - df_RF_item_both[
            'ProgressMonitoringComprehension_x']
    df_RF_item_both['PhonologicalAwarenessZPDLevel'] = df_RF_item_both[
        'PhonologicalAwarenessZPDLevel_y'] - df_RF_item_both[
            'PhonologicalAwarenessZPDLevel_x']
    df_RF_item_both['PhonicsWordRecognitionZPDLevel'] = df_RF_item_both[
        'PhonicsWordRecognitionZPDLevel_y'] - df_RF_item_both[
            'PhonicsWordRecognitionZPDLevel_x']
    df_RF_item_both['OralReadingWCPM'] = df_RF_item_both[
        'OralReadingWCPM_y'] - df_RF_item_both['OralReadingWCPM_x']
    df_RF_item_both['OralReadingAccuracyScore'] = df_RF_item_both[
        'OralReadingAccuracyScore_y'] - df_RF_item_both[
            'OralReadingAccuracyScore_x']
    df_RF_item_both['LiteralComprehensionPerformanceLevel'] = df_RF_item_both[
        'LiteralComprehensionPerformanceLevel_y'] - df_RF_item_both[
            'LiteralComprehensionPerformanceLevel_x']
    df_RF_item_both['ProgressMonitoringWCPM'] = df_RF_item_both[
        'ProgressMonitoringWCPM_y'] - df_RF_item_both[
            'ProgressMonitoringWCPM_x']
    df_RF_item_both['ProgressMonitoringAccuracyScore'] = df_RF_item_both[
        'ProgressMonitoringAccuracyScore_y'] - df_RF_item_both[
            'ProgressMonitoringAccuracyScore_x']

    df_RF_item_both = df_RF_item_both.drop([
        'Print_y', 'Print_x', 'Listening_y', 'Listening_x', 'Picture_y',
        'Picture_x', 'SentenceReading_y', 'SentenceReading_x',
        'ProgressMonitoringComprehension_y',
        'ProgressMonitoringComprehension_x', 'PhonologicalAwarenessZPDLevel_y',
        'PhonologicalAwarenessZPDLevel_x', 'PhonicsWordRecognitionZPDLevel_y',
        'PhonicsWordRecognitionZPDLevel_x', 'OralReadingWCPM_y',
        'OralReadingWCPM_x', 'OralReadingAccuracyScore_y',
        'OralReadingAccuracyScore_x', 'LiteralComprehensionPerformanceLevel_y',
        'LiteralComprehensionPerformanceLevel_x', 'ProgressMonitoringWCPM_y',
        'ProgressMonitoringWCPM_x', 'ProgressMonitoringAccuracyScore_y', 'ProgressMonitoringAccuracyScore_x'
    ],
                                           axis=1)

    return df_RF_item_both




# # Plots

# ## test files

def RF_testtype_map_test(df_RF, df_map, proficient_type, test_type=None):
    '''
      This function provide the test file used for plotting the scatterplot between Reading_Fluency scaled
      proficient_majority/proficient_majority general/testtype to MAP static: is_proficient

      INPUT
      df_RF - pandas dataframe of Reading Fluency, may separate in different types
      df_map - pandas dataframe of MAP
      proficient_type - "proficient_majority" or "all_proficient"
      test_type - 'Foundational Skills', 'Oral Reading', 'Progress Monitoring', 'Routed'

      OUTPUT
      test files
      '''

    df_RF['proficient_score'] = 0
    denominator = 4

    if proficient_type == 'proficient_majority':
        # calculate personal overal majority_proficient score
        # weighted higher level of test types as the same method of classroom overrall score.
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Beginner'),
                  'proficient_score'] = df_RF['proficient_majority']
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Skills'),
                  'proficient_score'] = df_RF['proficient_majority'] + 1
        df_RF.loc[(df_RF['ResultType'] == 'Oral Reading'),
                  'proficient_score'] = df_RF['proficient_majority'] + 2
        df_RF.loc[(df_RF['ResultType'] == 'Progress Monitoring'),
                  'proficient_score'] = df_RF['proficient_majority'] + 3
        df_RF.loc[(df_RF['ResultType'] == 'Routed'),
                  'proficient_score'] = df_RF['proficient_majority'] + 1

        #calculate an interim proficient_score
        df_RF['proficient_score'] = (df_RF['proficient_score']) / denominator

        #if test_type, then filter
        if test_type:
            df_RF = df_RF[(df_RF['ResultType'] == test_type)]

        #--merge kids took both RF and MAP
        df_mp = pd.merge(
            df_map[['student_number', 'is_proficient', 'grade_level']],
            df_RF[['StudentID', 'proficient_score']],
            how='inner',
            left_on='student_number',
            right_on='StudentID')

        df_mp = df_mp.rename(
            columns={
                "is_proficient": "map_proficient",
                "proficient_score": "rf_proficient_majority"
            })

        df_mp_corr = df_mp.drop(['StudentID', 'student_number'], axis=1)
        #plot = sb.scatterplot(x="rf_proficient_majority", y="map_proficient", data=df_mp_corr)

    if proficient_type == 'all_proficient':
        #use proficient_level column to show if all_proficient
        df_RF.loc[df_RF['proficient_level'] < 1, 'proficient_level'] = 0

        # calculate personal overal all_proficient score; the presumption is if
        # go to next level, the previous level is all_proficient--may think about it
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Beginner'),
                  'proficient_score'] = df_RF['proficient_level']
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Skills'),
                  'proficient_score'] = df_RF['proficient_level'] + 1
        df_RF.loc[(df_RF['ResultType'] == 'Oral Reading'),
                  'proficient_score'] = df_RF['proficient_level'] + 2
        df_RF.loc[(df_RF['ResultType'] == 'Progress Monitoring'),
                  'proficient_score'] = df_RF['proficient_level'] + 3
        df_RF.loc[(df_RF['ResultType'] == 'Routed'),
                  'proficient_score'] = df_RF['proficient_level'] + 1

        #calculate an interim proficient_score
        df_RF['proficient_score'] = (df_RF['proficient_score']) / denominator

        #if test_type, then filter
        if test_type:
            df_RF = df_RF[(df_RF['ResultType'] == test_type)]

        #--currently, random merge in the top RF if tester has multiple RF scores--NEED UPDATE
        df_mp = pd.merge(
            df_map[['student_number', 'is_proficient', 'grade_level']],
            df_RF[['StudentID', 'proficient_score']],
            how='inner',
            left_on='student_number',
            right_on='StudentID')

        df_mp = df_mp.rename(
            columns={
                "is_proficient": "map_proficient",
                "proficient_score": "rf_all_proficient"
            })

        df_mp_corr = df_mp.drop(['StudentID', 'student_number'], axis=1)
        #plot = sb.scatterplot(x="rf_all_proficient", y="map_proficient", data=df_mp_corr)

    return df_mp_corr

# ## RF majority_p & MAP proficient Scatter plot

# In[ ]:


def RF_testtype_map_scplot(df_RF, df_map, proficient_type, test_type=None):
    '''
      This function plot the scatterplot between Reading_Fluency scaled proficient_majority/proficient_majority
      general/testtype to MAP static: is_proficient

      INPUT
      df_RF - pandas dataframe of Reading Fluency, may separate in different types
      df_map - pandas dataframe of MAP
      proficient_type - "proficient_majority" or "all_proficient"
      test_type - 'Foundational Skills', 'Oral Reading', 'Progress Monitoring', 'Routed'

      OUTPUT
      Scatterplot
      '''

    df_RF['proficient_score'] = 0
    denominator = 4

    if proficient_type == 'proficient_majority':
        # calculate personal overal majority_proficient score
        # weighted higher level of test types as the same method of classroom overrall score.
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Beginner'),
                  'proficient_score'] = df_RF['proficient_majority']
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Skills'),
                  'proficient_score'] = df_RF['proficient_majority'] + 1
        df_RF.loc[(df_RF['ResultType'] == 'Oral Reading'),
                  'proficient_score'] = df_RF['proficient_majority'] + 2
        df_RF.loc[(df_RF['ResultType'] == 'Progress Monitoring'),
                  'proficient_score'] = df_RF['proficient_majority'] + 3
        df_RF.loc[(df_RF['ResultType'] == 'Routed'),
                  'proficient_score'] = df_RF['proficient_majority'] + 1

        #calculate an interim proficient_score
        df_RF['proficient_score'] = (df_RF['proficient_score']) / denominator

        #if test_type, then filter
        if test_type:
            df_RF = df_RF[(df_RF['ResultType'] == test_type)]

        #--merge kids took both RF and MAP
        df_mp = pd.merge(df_map[['student_number', 'is_proficient', 'grade_level']],
                         df_RF[['StudentID', 'proficient_score']],
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

        df_mp = df_mp.rename(
            columns={
                "is_proficient": "map_proficient",
                "proficient_score": "rf_proficient_majority"
            })

        df_mp_corr = df_mp.drop(['StudentID', 'student_number'], axis=1)
        plot = sb.scatterplot(x="rf_proficient_majority", y="map_proficient", data=df_mp_corr)

    if proficient_type == 'all_proficient':
        #use proficient_level column to show if all_proficient
        df_RF.loc[df_RF['proficient_level'] < 1, 'proficient_level'] = 0

        # calculate personal overal all_proficient score; the presumption is if
        # go to next level, the previous level is all_proficient--may think about it
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Beginner'),
                  'proficient_score'] = df_RF['proficient_level']
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Skills'),
                  'proficient_score'] = df_RF['proficient_level'] + 1
        df_RF.loc[(df_RF['ResultType'] == 'Oral Reading'),
                  'proficient_score'] = df_RF['proficient_level'] + 2
        df_RF.loc[(df_RF['ResultType'] == 'Progress Monitoring'),
                  'proficient_score'] = df_RF['proficient_level'] + 3
        df_RF.loc[(df_RF['ResultType'] == 'Routed'),
                  'proficient_score'] = df_RF['proficient_level'] + 1

        #calculate an interim proficient_score
        df_RF['proficient_score'] = (df_RF['proficient_score']) / denominator

        #if test_type, then filter
        if test_type:
            df_RF = df_RF[(df_RF['ResultType'] == test_type)]

        #--currently, random merge in the top RF if tester has multiple RF scores--NEED UPDATE
        df_mp = pd.merge(df_map[['student_number', 'is_proficient', 'grade_level']],
                         df_RF[['StudentID', 'proficient_score']],
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

        df_mp = df_mp.rename(
            columns={
                "is_proficient": "map_proficient",
                "proficient_score": "rf_all_proficient"
            })

        df_mp_corr = df_mp.drop(['StudentID', 'student_number'], axis=1)
        plot = sb.scatterplot(x="rf_all_proficient", y="map_proficient", data=df_mp_corr)

    return plot


# ## RF proficient progress vs. MAP progress Scatter

# In[ ]:


def RF_progress_map_scplot(df_RF_both, df_map_both, corr_type):
    '''
      This function caculates the correlation on dynamic state between RF proficient_progress
      and several MAP progress

      INPUT
      df_RF_both - pandas dataframe of Reading Fluency with 'StudentID', 'proficient_progress'
      from get_progress_score function, which is the progress between 2 RF windows
      df_map - pandas dataframe of MAP with "map_pro_progress" and "map_qtile_progress"
      corr_type - "percentile", "proficient",'rit','map_mgrowth_progress','map_growth_progress'

      OUTPUT
      correlation - A matrix holding the correlation coefficiencies between columns
      pvalue - A matrix showing the Pvalue of correlation between columns
    '''
    #--currently, random merge in the top RF if sester has multiple RF scores--NEED UPDATE
    if corr_type == 'percentile':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_qtile_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    #--currently, random merge in the top RF if sester has multiple RF scores--NEED UPDATE
    if corr_type == 'proficient':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_pro_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    if corr_type == 'rit':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_rit_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    if corr_type == 'map_mgrowth_progress':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_mgrowth_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    if corr_type == 'map_growth_progress':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_growth_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    df_mp_corr = df_mp.drop(['StudentID', 'student_number'], axis=1)
    correlation = df_mp_corr.corr().rf_pro_progress
    pvalue = calculate_pvalues(df_mp_corr, "rf_pro_progress")

    plot = sb.scatterplot(x=df_mp_corr.iloc[:,1], y="rf_pro_progress", data=df_mp_corr)

    return plot

# ## RF majority_p & MAP proficient Scatter plot

# In[ ]:

def testdomain_corr_map_heat(df_RF, df_map, goal):
    '''
      This function do the heatmap plots show the correlation between RF test domains and MAP goal

      INPUT
      df_RF - pandas dataframe of Reading Fluency, with all test type info and all test domain;
              and is the progress between 2 windows
      df_map - pandas dataframe of MAP; with student_number, grade_level and map_goal_rit_progress
      goal -- which MAP goal to do the correlation

      OUTPUT
      correlation heat map - A matrix holding the correlation coefficiencies between columns

      '''

    if goal == 1:
        # need to tweak which test domain to correlate with which MAP goal
        df_RF = df_RF.drop(
            [
                'ProgressMonitoringAccuracyScore',
                'ProgressMonitoringComprehension', 'ProgressMonitoringWCPM',
                'OralReadingWCPM', 'OralReadingAccuracyScore',
                'Listening', 'Picture','LiteralComprehensionPerformanceLevel',
                'AssignedTestType', 'ResultType'
            ],
            axis=1)


    #merge in testpercentile
    df_mp = pd.merge(df_map,
                     df_RF,
                     how='inner',
                     left_on='student_number',
                     right_on='StudentID')

    #drop unused column
    df_map_corr = df_mp.drop(['StudentID', 'student_number'], axis=1)

    #calculate correlation
    sb.heatmap(df_map_corr.corr(), xticklabels=df_map_corr.corr().columns, yticklabels=df_map_corr.corr().columns, cmap='RdYlGn', center=0, annot=True)

    # Decorations
    plt.title('Correlation of MAP Goal & RF_test_domains', fontsize=22)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xticks(rotation=60)

    return plt.show()

# # Spearman RF_MAP

# - both used the same names as above, since it is updated, do not need to change name
# - or if want to see the grade_level Pearson correlation as well, may

# ## RF majority_p & MAP proficiency correlation

# UPGRADED

# In[2]:


def proficiency_testtype_corr_map(df_RF, df_map, proficient_type, test_type=None, spearman=False):
    '''
      This function calculate the correlation (Spearman or Pearson) scores between Reading_Fluency scaled proficient_majority/proficient_majority
      general/testtype to MAP static: is_proficient

      INPUT
      df_RF - pandas dataframe of Reading Fluency, may separate in different types, used vars include:
            "StudentID", ResultType", "proficient_majority"(0/1)
      df_map - pandas dataframe of MAP; used vars: 'student_number', 'is_proficient', 'grade_level'
      proficient_type - "proficient_majority" or "all_proficient"
      test_type - 'Foundational Skills', 'Oral Reading', 'Progress Monitoring', 'Routed'
      spearman - default is "Pearson", can toggle on "spearman"

      OUTPUT
      if pearson:
      correlation - A matrix holding the correlation coefficiencies between columns
      pvalue - A matrix showing the Pvalue of correlation between columns
      if spearman:
      correlation - holding both correlation coefficiencies and p-value
      '''

    df_RF['proficient_score'] = 0
    denominator = 4

    if proficient_type == 'proficient_majority':
        # calculate personal overal majority_proficient score
        # weighted higher level of test types as the same method of classroom overrall score.
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Beginner'),
                  'proficient_score'] = df_RF['proficient_majority']
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Skills'),
                  'proficient_score'] = df_RF['proficient_majority'] + 1
        df_RF.loc[(df_RF['ResultType'] == 'Oral Reading'),
                  'proficient_score'] = df_RF['proficient_majority'] + 2
        df_RF.loc[(df_RF['ResultType'] == 'Progress Monitoring'),
                  'proficient_score'] = df_RF['proficient_majority'] + 3
        df_RF.loc[(df_RF['ResultType'] == 'Routed'),
                  'proficient_score'] = df_RF['proficient_majority'] + 1

        #calculate an interim proficient_score
        df_RF['proficient_score'] = (df_RF['proficient_score']) / denominator

        #if test_type, then filter
        if test_type:
            df_RF = df_RF[(df_RF['ResultType'] == test_type)]

        #--currently, random merge in the top RF if sester has multiple RF scores--NEED UPDATE
        df_mp = pd.merge(df_map[['student_number', 'is_proficient', 'grade_level']],
                         df_RF[['StudentID', 'proficient_score']],
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

        df_mp = df_mp.rename(
            columns={
                "is_proficient": "map_proficient",
                "proficient_score": "rf_proficient_majority"
            })

    if proficient_type == 'all_proficient':
        #use proficient_level column to show if all_proficient
        df_RF.loc[df_RF['proficient_level'] < 1, 'proficient_level'] = 0

        # calculate personal overal all_proficient score; the presumption is if
        # go to next level, the previous level is all_proficient--may think about it
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Beginner'),
                  'proficient_score'] = df_RF['proficient_level']
        df_RF.loc[(df_RF['ResultType'] == 'Foundational Skills'),
                  'proficient_score'] = df_RF['proficient_level'] + 1
        df_RF.loc[(df_RF['ResultType'] == 'Oral Reading'),
                  'proficient_score'] = df_RF['proficient_level'] + 2
        df_RF.loc[(df_RF['ResultType'] == 'Progress Monitoring'),
                  'proficient_score'] = df_RF['proficient_level'] + 3
        df_RF.loc[(df_RF['ResultType'] == 'Routed'),
                  'proficient_score'] = df_RF['proficient_level'] + 1

        #calculate an interim proficient_score
        df_RF['proficient_score'] = (df_RF['proficient_score']) / denominator

        #if test_type, then filter
        if test_type:
            df_RF = df_RF[(df_RF['ResultType'] == test_type)]

        #--currently, random merge in the top RF if tester has multiple RF scores--NEED UPDATE
        df_mp = pd.merge(df_map[['student_number', 'is_proficient', 'grade_level']],
                         df_RF[['StudentID', 'proficient_score']],
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

        df_mp = df_mp.rename(
            columns={
                "is_proficient": "map_proficient",
                "proficient_score": "rf_all_proficient"
            })

    df_mp=df_mp.set_index('student_number')

    if spearman:
        df_mp_corr = df_mp.drop(['StudentID','grade_level'], axis=1)
        correlation = stats.spearmanr(df_mp_corr)
        return correlation
    else:
        df_mp_corr = df_mp.drop(['StudentID'], axis=1)
        correlation = df_mp_corr.corr().map_proficient
        pvalue = calculate_pvalues(df_mp_corr, "map_proficient")
        return correlation, pvalue


# ## RF proficient progress vs. MAP progress correlation

# OUTGRADED

# In[ ]:


def proficiency_progress_corr(df_RF_both, df_map_both, corr_type, spearman=False):
    '''
      This function caculates the correlation on dynamic state between RF proficient_progress
      and several MAP progress

      INPUT
      df_RF_both - pandas dataframe of Reading Fluency with 'StudentID', 'proficient_progress'
      from get_progress_score function, which is the progress between 2 RF windows
      df_map - pandas dataframe of MAP with 'student_number', 'grade_level', 'map_pro_progress',
              'map_rit_progress', 'map_mgrowth_progress', 'map_growth_progress'
      corr_type - "percentile", "proficient",'rit','map_mgrowth_progress','map_growth_progress'
      corr_method - default is Pearson, can toggle spearman

      OUTPUT
      correlation - A matrix holding the correlation coefficiencies between columns
      pvalue - A matrix showing the Pvalue of correlation between columns
      if spearman:
      correlation - holding both correlation coefficiencies and p-value
    '''
    #--currently, random merge in the top RF if sester has multiple RF scores--NEED UPDATE
    if corr_type == 'percentile':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_qtile_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    #--currently, random merge in the top RF if sester has multiple RF scores--NEED UPDATE
    if corr_type == 'proficient':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_pro_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    if corr_type == 'rit':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_rit_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    if corr_type == 'map_mgrowth_progress':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_mgrowth_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    if corr_type == 'map_growth_progress':
        df_mp = pd.merge(df_map_both[['student_number', 'grade_level', 'map_growth_progress']],
                         df_RF_both,
                         how='inner',
                         left_on='student_number',
                         right_on='StudentID')

    df_mp=df_mp.set_index('student_number')

    if spearman:
        df_mp_corr = df_mp.drop(['StudentID','grade_level'], axis=1)
        correlation = stats.spearmanr(df_mp_corr)
        return correlation
    else:
        df_mp_corr = df_mp.drop(['StudentID'], axis=1)
        correlation = df_mp_corr.corr().rf_pro_progress
        pvalue = calculate_pvalues(df_mp_corr, "rf_pro_progress")
        return correlation, pvalue

# # Test domain vs. Goal

# - testitem_corr_map can be used for domain vs. goal by test type

# ## test domain progress across test type
def get_item_progress_notype(df_RF_1, df_RF_2, domain):
    '''
      This function calculates those RF of the same test domains in 2 windows, the progress of the test domain.

      INPUT
      df_RF_1 - pandas dataframe of Reading Fluency previous window with all the items
      df_RF_2 - pandas dataframe of Reading Fluency later window with all the items

      OUTPUT
      df - with 2 vars: 'StudentID', the progress metric of the test domain

    '''
    df_RF_1 = df_RF_1[['StudentID', domain]]
    df_RF_2 = df_RF_2[['StudentID', domain]]

    df_RF_1 = df_RF_1.dropna(subset=[domain])
    df_RF_2 = df_RF_2.dropna(subset=[domain])

    #find out the testers who took both tests
    df_RF_item_both = pd.merge(df_RF_1, df_RF_2, how='inner', on='StudentID')

    #find the progress made in the test domain
    df_RF_item_both[domain] = df_RF_item_both['{}_y'.format(
        domain)] - df_RF_item_both['{}_x'.format(domain)]

    df_RF_item_both = df_RF_item_both.drop(
        ['{}_y'.format(domain), '{}_x'.format(domain)], axis=1)

    return df_RF_item_both

# ## Test domain across testtype vs. MAP goal
def testdomain_corr_mapgoal(df_RF, df_map, domain, goal):
    '''
      This function calculate the correlation scores between Reading_Fluency test domain progress to MAP goal progress

      INPUT
      df_RF - pandas dataframe of Reading Fluency, with a metric of test domain progress
      df_map - pandas dataframe of MAP with a metric of goal progress
      domain - 'PhonicsWordRecognitionZPDLevel'
      goal - 'map_goal_rit_progress'

      OUTPUT
      correlation - A matrix holding the correlation coefficiencies between columns

      pvalue - P value for the correlations
      '''
    #merge students who took 2 windows of 2 tests
    df_mp = pd.merge(df_map[['student_number', goal, 'grade_level']],
                     df_RF,
                     how='inner',
                     left_on='student_number',
                     right_on='StudentID')

    #drop unused column
    df_map_corr = df_mp.drop(['StudentID', 'student_number'], axis=1)

    #calculate correlation
    correlation = df_map_corr.corr()[goal]
    #calculate pvalue
    pvalue = calculate_pvalues(df_map_corr, goal)

    return correlation, pvalue
