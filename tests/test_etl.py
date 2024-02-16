'''
testing functions from etl_utils
'''
from datetime import datetime
import pandas as pd
from src.etl_utils import keep_most_recent_recipes

def test_keep_most_recent_recipes():
    'test keep_most_recent_recipes'
    df = pd.DataFrame({
        'Month':['January','January','February','February'],
        'Year' : ['2022','2022','2021','2021'],
        'Day': [1,20,5,6],
        'Url' : ['url1','url1','url2','url2'],
        'Weekday': [1,2,3,2]
    })
    df = keep_most_recent_recipes(df).sort_values(by='Url').reset_index(drop=True)
    expected_df = pd.DataFrame({
        'Url':['url1','url2'],
        'date': [datetime.strptime('2022-01-20', '%Y-%m-%d'),
        datetime.strptime('2021-02-06', '%Y-%m-%d')]
    })
    assert df.equals(expected_df)
