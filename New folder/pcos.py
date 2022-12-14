# -*- coding: utf-8 -*-
"""pcos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QB8B-9F37bp-8xi6A1KCV-iAk8Im67hR
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df_inf=pd.read_csv("PCOS_infertility (1).csv")
df_noinf= pd.read_excel('PCOS_data_without_infertility (4).xlsx', sheet_name="Full_new")

"""DATA CLEANING"""

#joining the two tables and deleting the repeating coloums
df=pd.merge(df_noinf,df_inf, on='Patient File No.',suffixes={'','_y'},how='left')
df=df.drop(['Unnamed: 44', 'Sl. No_y', 'PCOS (Y/N)_y', '  I   beta-HCG(mIU/mL)_y','II    beta-HCG(mIU/mL)_y', 'AMH(ng/mL)_y'], axis=1)
df.head()

df.info()

df.dtypes

#converting the string values into numeric values
df["AMH(ng/mL)"] = pd.to_numeric(df["AMH(ng/mL)"], errors='coerce')
df["II    beta-HCG(mIU/mL)"] = pd.to_numeric(df["II    beta-HCG(mIU/mL)"], errors='coerce')

#filling up the null values with median values
df['Marraige Status (Yrs)'].fillna(df['Marraige Status (Yrs)'].median(),inplace=True)
df['II    beta-HCG(mIU/mL)'].fillna(df['II    beta-HCG(mIU/mL)'].median(),inplace=True)
df['AMH(ng/mL)'].fillna(df['AMH(ng/mL)'].median(),inplace=True)
df['Fast food (Y/N)'].fillna(df['Fast food (Y/N)'].median(),inplace=True)

#clearing up the extra space in column names
df.columns = [col.strip() for col in df.columns]

#heat map of various factors

corrmat = df.corr()
plt.subplots(figsize=(18,18))
sns.heatmap(corrmat,cmap='Pastel1_r', square=True);

# dependence of various factors
corrmat["PCOS (Y/N)"].sort_values(ascending=False)

#having a look at major contributors to pcos
plt.figure(figsize=(12,12))
k = 12 #number of variables with positive corr for heatmap
l = 3 #number of variables with negative corr for heatmap
cols_p = corrmat.nlargest(k, "PCOS (Y/N)")["PCOS (Y/N)"].index 
cols_n = corrmat.nsmallest(l, "PCOS (Y/N)")["PCOS (Y/N)"].index
cols = cols_p.append(cols_n) 

cm = np.corrcoef(df[cols].values.T)
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True,cmap="Pastel1_r", annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()

# patterns of length in menstrual cycle
#length of menstrual phase in pcos vs normal

color=['red','orange']
fig=sns.lmplot(data=df,x="Age (yrs)",y="Cycle length(days)", hue="PCOS (Y/N)",palette=color)

"""this plot shows that people without pcos have have consistant length of menstrual cycle whereas for the people with pcos, the length increases with age"""

#relation of BMI with pcos
color=['red','orange']
fig=sns.lmplot(data=df,x="Age (yrs)",y="BMI", hue="PCOS (Y/N)",palette=color)

"""From the above graph we can infer that people without pcos have constant bmi whereas bmi is increasing with age for the people who have pcos."""

#analysing the irregularity in menstrual cycle 
# 4 indicates irregular periods
# 2 indicates regular periods

fig=sns.lmplot(data=df,x="Age (yrs)",y="Cycle(R/I)", hue="PCOS (Y/N)",palette=color)

"""The mensural cycle becomes more regular for normal cases with age. Whereas, for PCOS the irregularity increases with age."""

#relation of pcos with number of follicles in each ovary
sns.lmplot(data =df,x='Follicle No. (R)',y='Follicle No. (L)', hue="PCOS (Y/N)",palette=color)

"""we can see that for a person without pcos has the number of follicles in each ovary is somewhat equal but for the pcos patients the number is not equal"""

df.dtypes

features = ["Follicle No. (L)","Follicle No. (R)"]
for i in features:
    sns.swarmplot(x=df["PCOS (Y/N)"], y=df[i], color="black", alpha=0.5 )
    sns.boxenplot(x=df["PCOS (Y/N)"], y=df[i], palette=color)
    plt.show()

sns.swarmplot(x=df["PCOS (Y/N)"], y=df["Endometrium (mm)"], color="black", alpha=0.5 )
sns.boxenplot(x=df["PCOS (Y/N)"], y=df["Endometrium (mm)"], palette=color)
plt.show()