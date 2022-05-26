import matplotlib.pyplot as plt

import matplotlib as mpl

import pandas as pd
import scipy.stats  as test
import scikit_posthocs as sp
import pingouin as pg
import seaborn as sns



df = pd.read_csv('resultados.txt', delimiter= ';')



df['Cases'] = df['K'].astype('str') + df['PartirVars']

print(df)

df2 = df.pivot_table(index='Problema', columns = 'Cases',values='TTotal')

medias = df2.mean()

aver1 = [medias[0],medias[2],medias[4],medias[6],medias[8]]
aver2 = [medias[1],medias[3],medias[5],medias[7],medias[9]]

# plt.plot([5,10,15,20,25], aver1, [5,10,15,20,25], aver2,)

print(medias)


# sns.boxplot(data=df, x="Cases", y="TTotal", hue=df.Cases.tolist())
fig, ax = plt.subplots(1,1, figsize=(10,5))
part = [23.035425186157227 ,9.456007719039917, 8.742131471633911 ,10.28268098831176 ,11.558128356933594]

# ax.plot([5,10,15,20,25], aver1, marker='o')
ax.plot([5,10,15,20,25], part, marker='o')

ax.set_xlabel("K", fontsize=15)
ax.set_ylabel("sec.", fontsize=15)
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator([5,10,15,20,25]))





plt.show()
print(pg.friedman(data=df2))

t = sp.posthoc_conover_friedman(a=df2)

print(t)
