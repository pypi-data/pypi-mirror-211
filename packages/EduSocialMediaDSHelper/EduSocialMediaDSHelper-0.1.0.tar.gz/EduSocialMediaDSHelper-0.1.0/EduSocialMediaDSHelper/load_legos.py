# %%
import pandas as pd
# %%
def load_data():
    df_sets = pd.read_csv('legos/sets.csv')
    df_color_counts = pd.read_csv('legos/color_counts.csv')
    d_color_palette = dict(zip(
        df_color_counts.color_name
        , '#' + df_color_counts.rgb
        ))
    return df_sets, df_color_counts, d_color_palette