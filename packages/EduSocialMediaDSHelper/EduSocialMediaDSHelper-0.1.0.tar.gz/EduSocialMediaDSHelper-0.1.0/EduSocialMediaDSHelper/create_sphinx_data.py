# %%
import numpy as np
import pandas as pd
np.random.seed(42)


# %%
n = 10000

d_material = {
    'clay': 0.1
    , 'sandstone': 0.15
    , 'porcelain': 0.2
    , 'gold': 0.05
    , 'iron': 0.1
    , 'copper': 0.15
    , 'bronze': 0.25
    }
d_condition = {
    'poor': 0.25
    , 'fair': 0.35
    , 'good': 0.3
    , 'excellent': 0.1
}
d_paint_coloring = {
    'absent': 0.60
    , 'mostly blue': 0.04
    , 'mostly green': 0.05
    , 'mostly red': 0.01
    , 'various': 0.30
}
d_posture = {
    'crouched': 0.25
    , 'pouncing': 0.15
    , 'standing': 0.15
    , 'laying': 0.40
    , 'other': 0.05
}
d_markings = {
    'plain': 0.3
    , 'light': 0.2
    , 'medium': 0.4
    , 'heavy': 0.1
}

a_id = np.arange(1, n+1)

a_material = np.random.choice(list(d_material.keys()), size=n, p=list(d_material.values()))
a_condition = np.random.choice(list(d_condition.keys()), size=n, p=list(d_condition.values()))
a_paint_coloring = np.random.choice(list(d_paint_coloring.keys()), size=n, p=list(d_paint_coloring.values()))
a_posture = np.random.choice(list(d_posture.keys()), size=n, p=list(d_posture.values()))
a_markings = np.random.choice(list(d_markings.keys()), size=n, p=list(d_markings.values()))
a_headdress_present = np.random.choice(['Y', 'N'], size=n, p=[0.7, 0.3])
a_has_wings = np.random.choice([True, False], size=n, p=[0.15, 0.85])
a_has_tail = np.random.choice([True, False], size=n, p=[0.40, 0.60])

a_paw_digits = np.random.choice([2, 3, 4, 5], size=n, p=[0.2, 0.1, 0.4, 0.3])

a_length_cm_1 = np.random.normal(loc=(6*2.54), scale=1.0, size=5000)
a_length_cm_2 = np.random.normal(loc=(15*2.54), scale=2.0, size=3000)
a_length_cm_3 = np.random.normal(loc=(30*2.54), scale=3.0, size=1500)
a_length_cm_4 = np.random.normal(loc=(90*2.54), scale=4.0, size=500)
a_length = np.concatenate([a_length_cm_1, a_length_cm_2, a_length_cm_3, a_length_cm_4])

df_sphinx = pd.DataFrame({
    'id':a_id
    , 'material':a_material
    , 'condition':a_condition
    , 'paint_coloring':a_paint_coloring
    , 'posture':a_posture
    , 'markings':a_markings
    , 'headdress_present':a_headdress_present
    , 'has_wings':a_has_wings
    , 'has_tail':a_has_tail
    , 'number_paw_digits':a_paw_digits
    , 'length_cm':a_length

})

df_sphinx.head()

# %%
def get_width(length):
    l_fracs = [0.3, 0.4, 0.5]
    frac = np.random.choice(l_fracs)
    return length * frac

df_sphinx['width_cm'] = df_sphinx.length_cm.apply(get_width)

def get_height(width):
    l_fracs = [0.80, 0.9, 1.05, 1.1, 1.2, 1.3, 1.4, 1.5]
    frac = np.random.choice(l_fracs)
    return width * frac

df_sphinx['height_cm'] = df_sphinx.width_cm.apply(get_height)

df_sphinx.head()

# %%
d_density_g_cm3 = {
    'clay': 2.65
    , 'sandstone': 2.3
    , 'porcelain': 2.403
    , 'gold': 19.32
    , 'iron': 7.874
    , 'copper': 8.96
    , 'bronze': 8.73
}

def get_density(material):
    mat_density = d_density_g_cm3[material]
    this_density = np.random.normal(size=1, loc=mat_density, scale=0.1 * mat_density)[0]
    return this_density

df_sphinx['density_g_cm3'] = df_sphinx.material.apply(get_density)
df_sphinx.sample(5)

# %%
df_sphinx['age_years'] = (4500 - (4500 * np.random.beta(a=20, b=2, size=n))).round()
df_sphinx['age_years'] = df_sphinx.age_years.astype('int')
df_sphinx.age_years.describe()

# %%
df_sphinx.sample(10)

# %%
df_sphinx.iloc[327, 5] = np.nan

# %%
df_sphinx.query('markings != markings')

# %%
df_sphinx.to_csv('df_sphinx.csv', index=False)
