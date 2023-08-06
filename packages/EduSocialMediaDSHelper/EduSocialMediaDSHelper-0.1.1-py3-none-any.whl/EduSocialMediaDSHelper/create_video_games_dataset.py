# %%
import numpy as np
import pandas as pd

# %%
df = pd.read_csv('Managerial_and_Decision_Economics_2013_Video_Games_Dataset.csv'
                 , encoding = 'ISO-8859-1')
df.head()

# %%
l_cols = [
    'Console'
    , 'Title'
    , 'US Sales (millions)'
    , 'YearReleased'
    , 'Publisher'
    , 'Genre'
    , 'Sequel'
    , 'Re-release'
    , 'Usedprice'
    , 'Review Score'
    , 'RatingE'
    , 'RatingT'
    , 'RatingM'
    , 'MaxPlayers'
    , 'Online'
    , 'Handheld'
    , 'LtdEdition'
    , 'Multiplatform'
]
df = df[l_cols]

# %%
l_common_genres = df.Genre.value_counts()[0:5].index.to_list()
df['Is_Common_Genre'] = df.Genre.apply(lambda x: True if x in l_common_genres else False)


# %%
s_log_sales_ign = (np.log(df['US Sales (millions)']) + 80)
s_ign = (s_log_sales_ign + (np.random.choice([1,-1], size=len(df)) * s_log_sales_ign * np.random.normal(loc=0.05, scale=0.025, size=len(df)))).round()
df['IGN Review Score'] = s_ign
s_ign.describe()


# %%
df.to_csv('video_game_sales.csv', index=False)

# %%
