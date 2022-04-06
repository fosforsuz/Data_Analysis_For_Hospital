import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 8)

# Read csv files
general = pd.read_csv('general.csv')
prenatal = pd.read_csv('prenatal.csv')
sports = pd.read_csv('sports.csv')

# make same the all column names
prenatal.columns = general.columns
sports.columns = general.columns

# Merge 3 dataframe
df = pd.concat([general, prenatal, sports], ignore_index=True)

# Drop the Unnamed: 0 column
df.drop(columns="Unnamed: 0", inplace=True)
df.dropna(axis=0, how='all', inplace=True)

# Replace on Sex, man -> m, woman -> f
df["gender"].replace({"man": "m", "male": "m", "woman": "f", "female": "f"}, inplace=True)

# in Prenatal hospital people's sex is woman so do all f
df.loc[(df.hospital == 'prenatal') & df.gender.isna(), 'gender'] = 'f'

# fill values to 0 in cols_nan
cols_nan = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
df[cols_nan] = df[cols_nan].fillna(0)

# Answer the questions:
# 1. Which hospital has the highest number of patients?
max_patient = df.hospital.value_counts().idxmax()
print(f"Which hospital has the highest number of patients?\n{max_patient}")

# 2. What share of the patients in the general hospital suffers from stomach-related issues?
# Round the result to the third decimal place.
general_patient_count = len(df.diagnosis[df.hospital == 'general'])
diagnosis_stomach_count = len(df.diagnosis[(df.hospital == 'general') & (df.diagnosis == 'stomach')])
stomach_share = round(diagnosis_stomach_count / general_patient_count, 3)
print(f'What share of the patients in the general hospital suffers from stomach-related issues?\n {stomach_share}')

# 3. What share of the patients in the sports hospital suffers from dislocation-related issues?
# Round the result to the third decimal place.
sports_patient_count = len(df.diagnosis[df.hospital == 'sports'])
dislocation_count = len(df.diagnosis[(df.hospital == "sports") & (df.diagnosis == "dislocation")])
dislocation_share = round(dislocation_count / sports_patient_count, 3)
print(f'What share of the patients in the sports hospital suffers from dislocation-related issues? {dislocation_share}')

# 4. What is the difference in the median ages of the patients in the general and sports hospitals?
general_median_age = df.age[df.hospital == 'general'].median()
sports_median_age = df.age[df.hospital == 'sports'].median()
print(f'What is the difference in the median ages of the patients in the general and sports hospitals?\n {int(general_median_age - sports_median_age)}')

# 5. After data processing at the previous stages, the blood_test column has three values:
# t= a blood test was taken, f= a blood test wasn't taken, and 0= there is no information.
# In which hospital the blood test was taken the most often (there is the biggest number of
# t in the blood_test column among all the hospitals)? How many blood tests were taken?
hospital = df.hospital[df.blood_test == 't'].value_counts().idxmax()
max_t = df.hospital[df.blood_test == 't'].value_counts().max()
print(f'In which hospital the blood test was taken the most often ?\n{hospital}\nHow many blood tests were taken?\n {max_t} blood tests')

# What is the most common age of a patient among all hospitals?
# Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80
df.plot(y='age', kind='hist')
plt.show()

# What is the most common diagnosis among patients in all hospitals? Create a pie chart

df.groupby('diagnosis').size().plot(kind='pie', title="Most Common Diagnosis", ylabel='Diagnosis')
plt.show()

# Build a violin plot of height distribution by hospitals. Try to answer the questions.
# What is the main reason for the gap in values?
# Why there are two peaks, which correspond to the relatively small and big values?
sns.violinplot(data=df, x='hospital', y='height')
plt.show()

print(f'The answer to the 1st question: 15 - 35')
print(f'The answer to the 2nd question: pregnancy')
print(f'The answer to the 3rd question: It\'s because The main reason for the gap in values is because the average height of Males and Females from sports hospital is roughly 4x more than general and prenatal. The two different types peaks refer to the distribution of the height from each hospital. A horizontal peak (general and prenatal) means the heights are distributed very closely to the mean while a vertical peak means there is more variation in height.')
