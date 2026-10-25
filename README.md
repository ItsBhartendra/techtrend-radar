# TechTrend Radar
An ML project that finds rising IT skills and roles, predicts salaries,
and recommends what to learn next, using public job-market data.

Status: in progress (MSc CS, DSC102 Machine Learning).

## Data
Stack Overflow Annual Developer Survey (selected years), licensed under
ODbL 1.0. Credit: Stack Overflow. Raw files are not stored in this repo;
notebooks download them from the official archive:
https://github.com/StackExchange/Survey

Limitation: survey respondents are a self-selected sample of developers,
not the whole IT industry.

## Progress
- [x] Data exploration (Stack Overflow Developer Survey, 2019/2021/2023/2025)
- [x] Cleaning, scaling (Min-Max, standardisation), PCA, feature selection
      (correlation filter, chi-square)

## Progress
- [x] DSC102 Practical 2: bias-variance trade-off (synthetic data), effect of
      many features and PCA, polynomial trend fitting on survey data

## Limitations (so far)
- Survey respondents are a self-selected sample; question wording and
  respondent mix change across years.
- Trend outlooks are based on only 7 yearly points and are rough guides,
  not forecasts to rely on.
- Some preprocessing choices (top countries/skills, salary median) were
  computed before the train/test split, a minor leakage.