import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
df_inf=pd.read_csv(r"C:\Users\Arya Sunil\Downloads\New folder\PCOS_infertility.csv")
df_noinf= pd.read_excel(r'C:\Users\Arya Sunil\Downloads\New folder\PCOS_data_without_infertility (5).xlsx', sheet_name="Full_new")
df=pd.merge(df_noinf,df_inf, on='Patient File No.',suffixes={'','_y'},how='left')
df=df.drop(['Unnamed: 44', 'Sl. No_y', 'PCOS (Y/N)_y', '  I   beta-HCG(mIU/mL)_y','II    beta-HCG(mIU/mL)_y', 'AMH(ng/mL)_y'], axis=1)
df["AMH(ng/mL)"] = pd.to_numeric(df["AMH(ng/mL)"], errors='coerce')
df["II    beta-HCG(mIU/mL)"] = pd.to_numeric(df["II    beta-HCG(mIU/mL)"], errors='coerce')
df['Marraige Status (Yrs)'].fillna(df['Marraige Status (Yrs)'].median(),inplace=True)
df['II    beta-HCG(mIU/mL)'].fillna(df['II    beta-HCG(mIU/mL)'].median(),inplace=True)
df['AMH(ng/mL)'].fillna(df['AMH(ng/mL)'].median(),inplace=True)
df['Fast food (Y/N)'].fillna(df['Fast food (Y/N)'].median(),inplace=True)
df.columns = [col.strip() for col in df.columns]

#heat map of various factors
corrmat = df.corr()
plt.subplots(figsize=(18,18))
figh1=sns.heatmap(corrmat,cmap='Pastel1_r', square=True);

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
figh2 = sns.heatmap(cm, cbar=True,cmap="Pastel1_r", annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)

# patterns of length in menstrual cycle
#length of menstrual phase in pcos vs normal
color=['red','orange']
fig1=sns.lmplot(data=df,x="Age (yrs)",y="Cycle length(days)", hue="PCOS (Y/N)",palette=color)

#relation of BMI with pcos
color=['red','orange']
fig2=sns.lmplot(data=df,x="Age (yrs)",y="BMI", hue="PCOS (Y/N)",palette=color)

#analysing the irregularity in menstrual cycle 
# 4 indicates irregular periods
# 2 indicates regular periods
fig3=sns.lmplot(data=df,x="Age (yrs)",y="Cycle(R/I)", hue="PCOS (Y/N)",palette=color)

#relation of pcos with number of follicles in each ovary
fig4=sns.lmplot(data =df,x='Follicle No. (R)',y='Follicle No. (L)', hue="PCOS (Y/N)",palette=color)
plt.show()
