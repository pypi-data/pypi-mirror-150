import pandas as pd


## Load Data
DATA_DIR = ('https://gitlab.com/prosocialai/nlpia2/-/raw/main/.nlpia2-data')

true = pd.read_csv(DATA_DIR+'/fake-news-dataset-true-small.csv')
fake = pd.read_csv(DATA_DIR+'/fake-news-dataset-fake-small.csv')

true['label'] = 1
fake['label'] = 0

fake.drop(labels=['subject','date', 'text'],axis=1,inplace=True)
true.drop(labels=['subject','date', 'text'],axis=1,inplace=True)

df = pd.concat([fake,true])

data.head()

## Clean the text