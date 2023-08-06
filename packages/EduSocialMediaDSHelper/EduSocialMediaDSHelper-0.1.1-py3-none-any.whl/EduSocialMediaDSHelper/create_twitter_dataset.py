# %%
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 500)
import string

# %%
df = pd.read_csv('twitter_human_bots_dataset.csv', low_memory=False)
df.head()

# %%
df['created_at'] = pd.to_datetime(df['created_at'])
df['hour_created'] = pd.to_datetime(df['created_at']).dt.hour
df['avg_favourites_per_day'] = df.favourites_count / df.account_age_days
df['avg_statuses_per_day'] = df.statuses_count / df.account_age_days
df['avg_friends_per_day'] = df.friends_count / df.account_age_days
df['avg_followers_per_day'] = df.followers_count / df.account_age_days
df['has_profile_background'] = df.profile_background_image_url.isna()
df['has_profile_description'] = df.description.isna()
df['has_profile_image'] = df.profile_image_url.isna()
df['screen_name_length'] = df.screen_name.apply(len)
df['screen_name_capital_count'] = df.screen_name.fillna('').apply(lambda x: sum(1 for c in x if c.isupper()))
df['screen_name_punct_count'] = df.screen_name.fillna('').apply(lambda x: sum([1 for c in x if c in string.punctuation]))
df['description_length'] = df.description.fillna('').apply(len)
df['description_capital_count'] = df.description.fillna('').apply(lambda x: sum(1 for c in x if c.isupper()))
df['description_punct_count'] = df.description.fillna('').apply(lambda x: sum([1 for c in x if c in string.punctuation]))
df['description_at_count'] = df.description.fillna('').apply(lambda x: sum([1 for c in x if c == '@']))
df['description_link_count'] = df.description.fillna('').apply(lambda x: x.count('http'))
df['description_hash_count'] = df.description.fillna('').apply(lambda x: x.count('#'))
df.drop(columns=['Unnamed: 0', 'description', 'profile_background_image_url', 'profile_image_url', 'screen_name'], inplace=True)
df.head()

# %%
df.to_csv('twitter_bot_detection.csv', index=False)
# %%
