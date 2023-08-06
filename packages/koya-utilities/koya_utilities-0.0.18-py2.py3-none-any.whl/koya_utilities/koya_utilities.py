from IPython.display import display_javascript, display_html, display
from df2gspread import gspread2df as g2d
from bcpandas import SqlCreds, to_sql
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime

import pandas as pd
import awswrangler as wr
import boto3
import numpy as np
import smtplib, ssl
import gspread
import itertools
import smtplib
import email.message
import tempfile
import json
import uuid
import io
import os



def get_stats(df, verbose=False):
    l = []
    for col in df.columns:
        if verbose:
            print(col)

        s = float(len(df))

        nn = float(df[col].count())
        nn_pct = nn / s

        try:
            unique = len(df[col].unique())
            unique_pct = round(unique / s, 2)
        except Exception as e:
            unique = None
            unique_pct = None
            print(str(e))


        null = pd.isnull(df[col]).sum()
        null_pct = round(null / s, 2)

        vc = df[col].value_counts()
        if len(vc) > 0:
            mf = pd.DataFrame(df[col].value_counts()).iloc[0, 0]
        else:
            mf = 0

        if nn != 0:
            mf_pct = round(mf / nn, 2)
        else:
            mf_pct = 0.0

        if unique is not None:
            binary = len("{0:b}".format(unique))
        else:
            binary=None

        l.append([col, nn, nn_pct, unique, unique_pct, binary, null, null_pct, mf, mf_pct])
    d = pd.DataFrame(l, columns=['col', 'not_null', 'not_null_pct', 'unique_values', 'unique_pct', 'binary', 'null',
                                 'null_pct', 'most_frequent', 'mf_pct'])
    return d

def value_counts_pct(se_col):
    vc = se_col.value_counts(dropna=False).to_frame()
    vc_pct = (se_col.value_counts(dropna=False) / float(len(se_col))).to_frame()
    vc_pct = vc_pct.applymap(lambda x: str(100 * round(x, 2)) + '%')
    df = pd.concat([vc, vc_pct], axis=1)
    df.columns = [se_col.name, se_col.name + '_pct']
    return df

def get_general_changes(df1, df2, key, verbose=False):
    inner_keys = list(set(df2[key]).intersection(df1[key]))
    inner_columns = list(set(df2.columns).intersection(df1.columns))

    if verbose:
        print(inner_columns)
        print(len(inner_keys), len(df1), len(df2))

    q1 = (df1[df1[key].isin(inner_keys)]
          .drop_duplicates(subset=key)
          .sort_values(by=key)
          [inner_columns]
          .set_index(key)
          .fillna('NaN_f')
          .applymap(lambda x: float(x) if type(x) == int or (type(x) == str and x.isnumeric()) else x)
          .applymap(lambda x: str(x))
          )

    q2 = (df2[df2[key].isin(inner_keys)]
          .drop_duplicates(subset=key)
          .sort_values(by=key)
          [inner_columns]
          .set_index(key)
          .fillna('NaN_f')
          .applymap(lambda x: float(x) if type(x) == int or (type(x) == str and x.isnumeric()) else x)
          .applymap(lambda x: str(x))
          )

    inner_columns.remove(key)
    comp = pd.DataFrame()
    for col in inner_columns:
        comp[col] = q1[col] == q2[col]

    aux = comp.T.copy(deep=True)
    l = []
    for col in aux:
        idx = list(aux[aux[col] == False].index)
        l.append([col, idx])

    aux = pd.merge(q1.reset_index(), q2.reset_index(), on=key, suffixes=('_CURRENT', '_NEW'))
    aux = aux[sorted(aux.columns)]

    changes = pd.DataFrame(l, columns=[key, 'changes'])
    changes['changes'] = changes['changes'].apply(lambda x: str(x))
    changes = pd.merge(changes, aux, on=key)

    return changes

def get_difference_stats(df1,df2,key
                         ,match_columns=True
                         ,only_difference=False
                         ,match_ids=True
                         ,drop_null=False
                         ,type_comparison='difference'):
    
    df1=df1.copy(deep=True)
    df2=df2.copy(deep=True)
    
    if match_ids:
        common = set(df1[key]).intersection(df2[key])
        df1 = df1[df1[key].isin(common)]
        df2 = df2[df2[key].isin(common)]
    else:
        diff = list(set(df1[key])-set(df2[key]))
        diff+= list(set(df2[key])-set(df1[key]))
    
        if len(diff)>0:
            raise ValueError('keys do not match: lenght')
        
    if df1[key].duplicated().sum()>0:
        raise ValueError('duplicated key in df1')
        
    if df2[key].duplicated().sum()>0:
        raise ValueError('duplicated key in df2')
        
    
    if match_columns:
        columns = set(df1.columns).intersection(df2.columns)
        df1 = df1[columns]
        df2 = df2[columns]
    else:
        diff = list(set(df1.columns)-set(df2.columns))
        diff+= list(set(df2.columns)-set(df1.columns))

        if len(diff)>0:
            raise ValueError('columns do not match: lenght')
    
    df1=df1.set_index(key).sort_index()
    df2=df2.set_index(key).sort_index()
    
    aux=pd.merge(df1,df2,on=key,suffixes=('_df1','_df2'))
    
    d={}
    for col in df1.columns:
        if col!=key:
            
            if drop_null!=False:
                not_null = aux.copy(deep=True)
                
                if drop_null=='left':
                    not_null = not_null.dropna(subset=f'{col}_df1')
                elif drop_null == 'right':
                    not_null = not_null.dropna(subset=f'{col}_df2')
                elif drop_null==True:
                    not_null = not_null.dropna(subset=f'{col}_df1')
                    not_null = not_null.dropna(subset=f'{col}_df2')
                    
                series1 = not_null[f'{col}_df1'].copy(deep=True)
                series2 = not_null[f'{col}_df2'].copy(deep=True)

                    
            else:
                series1 = aux[f'{col}_df1'].copy(deep=True)
                series2 = aux[f'{col}_df2'].copy(deep=True)
                
            series1=series1.fillna('NaN')
            series2=series2.fillna('NaN')


            if type_comparison=='difference':
                diff=(series1!=series2).sum()
            else:
                diff=(series1==series2).sum()
            
            if pd.isnull(diff) or diff==0:
                pct = 0
            else:
                pct = round(diff/len(series1),2)*100
                
            
            
            if not only_difference:
                d[col] = (diff,pct)
            elif diff!=0:
                d[col] = (diff,pct)
    return d

def create_natural_key(cols_natutal_key,x):
    key=''
    for col in cols_natutal_key:
        key+=f'[{col}]_{x[col]}__'
    key=key.strip('__')
    return key

def get_natural_key(df,subset_cols=None):
    
    df=df.copy(deep=True)

    if subset_cols is None:
        subset_cols=df.columns

    results=[]
    for i in range(1,len(subset_cols)+1):
        combinations = list(itertools.combinations(subset_cols,i))
        for combination in combinations:
            combination = list(combination)
            df[combination] = df[combination].fillna('NaN_f').astype(str)
            df['key'] = df[combination].apply(lambda x: "**".join(x),axis=1)
            dups = df['key'].duplicated().sum()
            results.append([combination,dups])
    results=pd.DataFrame(results,columns=['combinations','duplicates'])
    results['n_members'] = results['combinations'].apply(lambda x:len(x))
    return results

def get_dup_iso(dup,key):
    '''
    This function helps to isolate the columns that have different values where the unified key is the same
    '''
    cols=list(dup.columns)
    cols.remove(key)
    dd={}
    for value in dup[key].unique():
        d={}
        d['report']=[]
        sub=dup[dup[key]==value].fillna('')
        for col in cols:
            #print(col)
            s=set(sub[col])
            if len(s)>1:
                d[col]=[list(s)]
                l=d['report']
                l.append(col)
                d['report']=l
            else:
                d[col]=''
        d['report']=','.join(d['report']).strip().strip(',')
        dd[value]=d
    dup_iso = pd.DataFrame(dd).T
    return dup_iso


def send_email_to(body='generic email message'
                  , project_name=None
                  , subject='Email from dev'
                  , email_from='mendesdev20@gmail.com'
                  , email_to='andre@getkoya.ai'
                  , token='epetgpoiulvfcagc'):

    
    try:
        msg = email.message.Message()
        msg["Subject"] = subject
        msg["From"] = email_from
        msg["To"] = email_to
        password = token

        msg.add_header("Content-Type", "text/html")
        msg.set_payload(f"{project_name} - " + body)

        s = smtplib.SMTP("smtp.gmail.com: 587")
        s.starttls()

        # login credentials for sending email
        s.login(msg["From"], password)
        s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))

        return 0

    except Exception as e:
        print(e)
        return 1

#displays JSON data in an easily and readable format
class RenderJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid), raw=True)
        display_javascript("""
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
        document.getElementById('%s').appendChild(renderjson(%s))
        });
        """ % (self.uuid, self.json_str), raw=True)


def check_quality(df_normalized, airtable_params, check_quality=False, test_level='outter', verbose=True):
    if check_quality:
        baseId = airtable_params['baseId']
        apiKey = airtable_params['apikey']
        tableName = airtable_params['tableName']
        token = airtable_params['token']

        fields = get_fields_types(baseId, token, tableName)
        koya_template_fields = list(fields.keys())
        koya_template_df = pd.DataFrame(columns=koya_template_fields)

        result = test_columns(koya_template_df.columns, df_normalized.columns, test_level=test_level, verbose=verbose)
        return result
    
def save_data_local(df, source, save_csv = False, save_json = False, json_object=None):
    '''
    Saves data to a local folder

    Args:
    df (pandas.DataFrame): Pandas dataframe
    source (str): Source
    json_object (optional): JSON object to be saved (default: None)
    save_csv (bool): Flag indicating whether to save the data as a CSV file (default: False)
    save_json (bool): Flag indicating whether to save the data as a JSON object (default: False)

    Returns:
        None
    ''' 
    print('saving to local folder')
    today = datetime.datetime.now().strftime('%m-%d-%Y')

    if save_csv:
        #df_normalized.to_csv(f'data/master_normalized_{source}_{today}.csv',index=False)
        df.to_csv(f'master_normalized_{source}_{today}.csv', index=False)
        print(f'master_normalized_{source}_{today}.csv successfully saved')
    
    if save_json:
        json_file_name = f'master_normalized_{source}_{today}.json'
        with open(json_file_name, 'w') as json_file:
            json.dump(json.loads(json_object), json_file)
            print(f'master_normalized_{source}_{today}.json successfully saved')
    
    elif save_json and json_object is None:
        print('Json Object is none')

def save_data_s3(df, source, client_project_name, stage, save_csv = False, save_json = False, 
                json_object=None, include_uuid=False, add_info=None):
    '''
    Saves data to a S3

    Args:
    df (pandas.DataFrame): Pandas dataframe
    source (str): Source
    today_s3: datetime in AWS S3 format
    json_object (optional): JSON object to be saved (default: None)
    save_csv (bool): Flag indicating whether to save the data as a CSV file (default: False)
    save_json (bool): Flag indicating whether to save the data as a JSON object (default: False)

    Returns:
        None
    ''' 
    print('saving to s3')

    today = datetime.datetime.now().strftime('%m-%d-%Y')
    today_s3 = datetime.datetime.now().strftime('%Y-%m-%d')

    filename = f'{source}_{today_s3}'

    if include_uuid:
        UUID = uuid.uuid1().hex
        filename = f'{filename}______{UUID}'

    if add_info:
        filename = f'{add_info}_{filename}'

    if save_csv:
        filename += '.csv'
        path = f"s3://{client_project_name}/{stage}/normalization/data/"
        wr.s3.to_csv(df=df, path=path + filename)
        print(f'{filename} successfully saved')

    if save_json:
        s3 = boto3.client('s3')
        s3.put_object(Bucket=client_project_name, Key=f'development/normalization/data/{source}_{today_s3}.json', Body=json_object)
        print(f'{filename}.json successfully saved')

def save_to_database(df, source, engine):
    '''
    Saves data to a database table

    Args:
        df (pandas.DataFrame): Pandas Dataframe
        source (str): Source
        engine: Database engine or connection object
    '''

    print('saving to database')
    df.to_sql(name=source, con=engine, if_exists='replace', index=False)

def save_data_drive(folder_id: str, df: pd.DataFrame, source:str, 
                    save_csv=False, save_json=False, json_object = None, auth = True):
    '''
    Saves data to Google Drive

    Args:
        Folder_id (str): ID of the folder in Google Drive
        df (pandas.DataFrame): Pandas dataframe
        source (str): Source
        json_object (optional): JSON object to be saved (default: None)
        save_csv (bool): Flag indicating whether to save the data as a CSV file (default: False)
        save_json (bool): Flag indicating whether to save the data as a JSON object (default: False)

    Returns:
        None
    '''
    print('saving to drive')
    today = datetime.datetime.now().strftime('%m-%d-%Y')
    csv_file_name = f'master_normalized_{source}_{today}.csv'
    json_file_name = f'master_normalized_{source}_{today}.json'

    if auth:
        gauth = GoogleAuth()
        gauth.DEFAULT_SETTINGS['client_config_file'] = os.getenv("CLIENT_SECRETS_PATH")
        gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    if save_csv:
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(csv_buffer.getvalue())
        csv_file = drive.CreateFile({'title': csv_file_name, 'parents': [{'id': folder_id}]})
        csv_file.SetContentFile(f.name)
        csv_file.Upload(param={'convert': True})
        os.remove(f.name)
        print(f'{csv_file_name} successfully saved')

    if save_json:
        json_buffer = io.BytesIO(json.dumps(json_object).encode())
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(json_buffer.getvalue())
        json_file = drive.CreateFile({'title': json_file_name, 'parents': [{'id': folder_id}]})
        json_file.SetContentFile(f.name)
        json_file.Upload(param={'convert': True})
        os.remove(f.name)
        print(f'{json_file_name} successfully saved')