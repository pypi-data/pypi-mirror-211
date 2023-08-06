# %%
import pandas as pd

# %%
l_cols = [
    'age'
    ,'workclass'
    ,'fnlwgt'
    ,'education'
    ,'education_num'
    ,'marital_status'
    ,'occupation'
    ,'relationship'
    ,'race'
    ,'male_female'
    ,'capital_gain'
    ,'capital_loss'
    ,'hours_per_week'
    ,'native_country'
    ,'income_group'
    ]
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data', index_col=False, names=l_cols)
df.head()

# %%
df['fnlwgt'] = (df.fnlwgt / df.fnlwgt.min()).round()

# %%
df = df.loc[df.index.repeat(df.fnlwgt)].reset_index(drop=True)
print(len(df))
df.head()

# %%
df.drop(columns='fnlwgt', inplace=True)

# %%
df.to_csv('uci_census_data.csv', index=False)

# %%
ratio_fm = len(df.query('male_female == " Male"')) / len(df.query('male_female == " Female"')) 
df['fm'] = df.male_female.apply(lambda x: ratio_fm if x == " Female" else 1)
df = df.loc[df.index.repeat(df.fm)].reset_index(drop=True)
df.drop(columns=['fm'], inplace=True)
diff_fm = len(df.query('male_female == " Male"')) - len(df.query('male_female == " Female"'))
df_fsamp = df.query('male_female == " Female"').sample(diff_fm)
df = pd.concat([df, df_fsamp]).reset_index(drop=True)
print(len(df))

# %%
df.to_csv('uci_census_data_balanced.csv', index=False)

# %%
df.head()