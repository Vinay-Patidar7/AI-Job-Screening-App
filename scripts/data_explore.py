import pandas as pd
import matplotlib.pyplot as plt

# Load job descriptions dataset
df = pd.read_csv("jobdescription.csv")

# Check dataset overview
print(df.head())
print(df.info())

# Skill frequency check
df['skills'].value_counts().plot(kind='barh')
plt.title("Most Required Skills in Job Descriptions")
plt.show()
