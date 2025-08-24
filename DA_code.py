import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno


df = pd.read_csv('DA_CP box_office_data(2000-2024).csv')

df.head()
df.info()
df.describe()

msno.matrix(df)
plt.show()

df.hist(figsize=(12, 10))
plt.tight_layout()
plt.show()

#Data Cleaning and Preprocessing
df = df.dropna(subset=['Budget', 'Box Office'])
df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Profit'] = df['Box Office'] - df['Budget']
df['Release Year'] = df['Release Date'].dt.year

sns.lineplot(data=df, x='Release Year', y='Box Office')
plt.title('Box Office Revenue Over Years')
plt.show()

sns.boxplot(data=df, x='Genre', y='Profit')
plt.xticks(rotation=90)
plt.title('Profit Distribution by Genre')
plt.show()

corr_matrix = df.corr(numeric_only=True)
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

