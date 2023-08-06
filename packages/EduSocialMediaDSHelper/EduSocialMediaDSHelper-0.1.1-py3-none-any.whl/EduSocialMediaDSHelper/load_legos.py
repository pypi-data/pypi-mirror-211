# %%
import pandas as pd
import pkg_resources
# %%
def load_data():

    resource_package = __name__  

    sets_resource_path = '/'.join(('legos', 'sets.csv'))
    sets_file_path = pkg_resources.resource_filename(resource_package, sets_resource_path)

    ccounts_resource_path = '/'.join(('legos', 'color_counts.csv'))
    ccounts_file_path = pkg_resources.resource_filename(resource_package, ccounts_resource_path)

    df_sets = pd.read_csv(sets_file_path)
    df_color_counts = pd.read_csv(ccounts_file_path)
    d_color_palette = dict(zip(
        df_color_counts.color_name
        , '#' + df_color_counts.rgb
        ))
    return df_sets, df_color_counts, d_color_palette