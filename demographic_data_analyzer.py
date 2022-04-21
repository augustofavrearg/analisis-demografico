import pandas as pd


def calculate_demographic_data(print_data=True):
  # Read data from file
  df = pd.read_csv('adult.data.csv')

   
  
  race_count = df['race'].value_counts()

   # What is the average age of men?
  average_age_men = df.loc[df['sex'] == 'Male']['age'].mean().round(decimals=1)


  # What is the percentage of people who have a Bachelor's degree?
  bachelors_count = df.loc[df['education'] == 'Bachelors']['education'].count()
  total_count = df['education'].count()
  percentage_bachelors = (bachelors_count / total_count * 100).round(decimals=1)


  education_salary_df = pd.DataFrame(df.groupby(df['education'])['salary'].value_counts())
  education_salary_df = education_salary_df.rename(columns={"salary": "counts"})
  high_salary_df = education_salary_df.loc[(slice(None), '>50K'),:]

  higher_education = education_salary_df.loc[['Bachelors', 'Masters', 'Doctorate']].sum()
  lower_education = education_salary_df.sum() - higher_education

  higher_education_rich = high_salary_df.loc[['Bachelors', 'Masters', 'Doctorate']].sum()
  lower_education_rich = high_salary_df.sum() - higher_education_rich
  min_work_hours = df['hours-per-week'].min()

  hours_worked_salary_df = pd.DataFrame(df.groupby(df['hours-per-week'])['salary'].value_counts())
  hours_worked_salary_df = hours_worked_salary_df.rename(columns={"salary": "counts"})
  min_hours_worked_salary_df = hours_worked_salary_df.loc[min_work_hours, :]


  num_min_workers = min_hours_worked_salary_df.sum()

  rich_percentage = float((min_hours_worked_salary_df.loc['>50K'] / num_min_workers * 100).round(decimals=1))

  country_counts_df = pd.DataFrame(df.groupby(df['native-country'])['salary'].count())
  country_counts_df = country_counts_df.rename(columns={"salary": "counts"}).reset_index()
  country_rich_counts_df = pd.DataFrame(df.groupby(df['native-country'])['salary'].value_counts())
  country_rich_counts_df = country_rich_counts_df.loc[(slice(None), '>50K'), :]
  country_rich_counts_df = country_rich_counts_df.rename(columns={"salary": "rich-counts"})
  country_rich_counts_df = country_rich_counts_df.reset_index()[['native-country', 'rich-counts']]
  country_counts_df = country_counts_df.merge(country_rich_counts_df, on='native-country')
  country_counts_df['rich-percent'] = (country_counts_df['rich-counts'] / country_counts_df['counts'] * 100)
  country_counts_df['rich-percent'] = country_counts_df['rich-percent'].round(decimals=1)
  top_country = country_counts_df.sort_values('rich-percent', ascending=False).head(1)

  highest_earning_country = top_country.iloc[0]['native-country']
  highest_earning_country_percentage = top_country.iloc[0]['rich-percent']


  india_df = df.loc[df['native-country'] == 'India']
  india_df = india_df.loc[df['salary'] == '>50K']
  india_df = pd.DataFrame(india_df.groupby('native-country')['occupation'].value_counts())
  india_df = india_df.rename(columns={'occupation': 'counts'})
  india_df = india_df.reset_index().sort_values('counts', ascending=False).head(1)

  top_IN_occupation = india_df.iloc[0]['occupation']


# DO NOT MODIFY BELOW THIS LINE
  
  if print_data:
    print("Number of each race:\n", race_count)
    print("Average age of men:", average_age_men)
    print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
    print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
    print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
    print(f"Min work time: {min_work_hours} hours/week")
    print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
    print("Country with highest percentage of rich:", highest_earning_country)
    print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
    print("Top occupations in India:", top_IN_occupation)

  return {
    'race_count': race_count,
    'average_age_men': average_age_men,
    'percentage_bachelors': percentage_bachelors,
    'higher_education_rich': higher_education_rich,
    'lower_education_rich': lower_education_rich,
    'min_work_hours': min_work_hours,
    'rich_percentage': rich_percentage,
    'highest_earning_country': highest_earning_country,
    'highest_earning_country_percentage':highest_earning_country_percentage,
    'top_IN_occupation': top_IN_occupation
    }