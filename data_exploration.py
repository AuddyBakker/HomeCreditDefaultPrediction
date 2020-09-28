# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 08:19:23 2020
"""

import sqlite3 as sql
import csv
import pandas as pd
import numpy as np


def clean_data(train="data/HomeCreditDefault/application_train.csv", 
               ccb="data/HomeCreditDefault/credit_card_balance.csv"):
    
    # Select only columns we will use for training data
    app_train = pd.read_csv(train)
    df = app_train[['SK_ID_CURR', 'TARGET', 'NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 
               'FLAG_OWN_REALTY', 'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 
               'AMT_ANNUITY', 'AMT_GOODS_PRICE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 
               'OWN_CAR_AGE']].copy()
    df.to_csv('data/HomeCreditDefault/application_train_cleaned.csv', index=False)
    
    # Select only columns we will use for bureau data
    df_cc_balance = pd.read_csv(ccb)
    df_b = df_cc_balance[['SK_ID_CURR', 'SK_ID_PREV', 'AMT_BALANCE', 'AMT_CREDIT_LIMIT_ACTUAL']].copy()
    df_b.to_csv('data/HomeCreditDefault/credit_card_balance_cleaned.csv', index=False)


# Problems 1, 2, and 4
def bad_debt_db(db_file="data/HomeCreditDefault/bad_debt.db", 
               ccb="data/HomeCreditDefault/credit_card_balance_cleaned.csv", 
               train="data/HomeCreditDefault/application_train_cleaned.csv"):

    """
    Parameters:
        db_file (str): The name of the database file.
        
        bureau (str): The name of a csv file containing all client's previous 
            credits provided by other financial institutions that were reported 
            to Credit Bureau (for clients who have a loan in our sample).

        bureau_balance (str): The name of a csv file containing Monthly balances 
            of previous credits in Credit Bureau
            
        train (str): The name of a csv file containing Static data for all 
            applications. One row represents one loan in our data sample.
    """
    try:
        #Connect to the database (and create it if it doesn't exist)
        with sql.connect(db_file) as conn:
            cur = conn.cursor()  # Get the cursor.
            #add the following tables to the database with the specied column names and types.
            cur.execute("""CREATE TABLE IF NOT EXISTS ApplicationTrain (SK_ID_CURR INTEGER,
                                                                       Target INTEGER,
                                                                       Contract_Type TEXT,
                                                                       Gender TEXT,
                                                                       Car_Owner TEXT,
                                                                       Realty_Owner TEXT,
                                                                       Num_Child INTEGER,
                                                                       Total_Income INTEGER,
                                                                       Total_Credit INTEGER,
                                                                       Total_Annuity INTEGER,
                                                                       Price_of_Goods INTEGER,
                                                                       Income_Type TEXT,
                                                                       Education TEXT,
                                                                       Car_Age INTEGER)""")
            
            cur.execute("""CREATE TABLE IF NOT EXISTS CreditCardBalance (SK_ID_CURR INTEGER, 
                                                                      SK_ID_PREV INTEGER,
                                                                      prev_month_bal INTEGER,
                                                                      cred_limit INTEGER)""")
            

            with open(train, 'r') as infile:
                rows = list(csv.reader(infile))
                cur.executemany("INSERT INTO ApplicationTrain VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);", rows)
            with open(ccb, 'r') as infile:
                rows = list(csv.reader(infile))
                cur.executemany("INSERT INTO CreditCardBalance VALUES(?,?,?,?);", rows)


        #commit database
        conn.commit()
    finally:
        #close database
        conn.close()
        

def join_tables(db_file="data/HomeCreditDefault/bad_debt.db"):
    try:
        #Connect to the database (and create it if it doesn't exist)
        with sql.connect(db_file) as conn:

            cur = conn.cursor()  # Get the cursor.
            data = cur.execute("""SELECT AT.SK_ID_CURR, AT.TARGET, AT.Contract_Type, AT.Gender, 
                               AT.Car_Owner, AT.Realty_Owner, AT.Num_Child, AT.Total_Income, 
                               AT.Total_Credit, AT.Total_Annuity, AT.Price_of_Goods, AT.Income_Type, 
                               AT.Education, AT.Car_Age, CB.prev_month_bal, CB.cred_limit 
                               FROM ApplicationTrain AS AT LEFT JOIN CreditCardBalance AS CB 
                               ON AT.SK_ID_CURR == CB.SK_ID_CURR 
                               ORDER BY AT.SK_ID_CURR;""").fetchall()
        
            # commit database
            conn.commit()
    finally:
        #close database
        conn.close()
        
    return data, type(data), np.shape(data)
    
    
'''
            data = cur.execute("""SELECT AT.SK_ID_CURR, AT.TARGET, AT.Contract_Type, AT.Gender, 
                               AT.Car_Owner, AT.Realty_Owner, AT.Num_Child, AT.Total_Income, 
                               AT.Total_Credit, AT.Total_Annuity, AT.Price_of_Goods, AT.Income_Type, 
                               AT.Education, AT.Car_Age, B.SK_ID_BUREAU, B.Credit_Active, 
                               B.Days_Credit, B.Days_Credit_Overdue, B.Days_Credit_End, 
                               B.Amt_Credit_Sum, B.Credit_Type 
                               FROM ApplicationTrain AS AT INNER JOIN Bureau AS B 
                               ON AT.SK_ID_CURR == B.SK_ID_CURR 
                               ORDER BY AT.SK_ID_CURR;""").fetchall()
'''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    