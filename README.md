# TechTrend Radar
An ML project that finds rising IT skills and roles, predicts salaries,
and recommends what to learn next, using public job-market data.

Status: in progress (MSc CS, DSC102 Machine Learning).

## Data
Stack Overflow Annual Developer Survey (2019-2025), licensed under
ODbL 1.0. Credit: Stack Overflow. Raw files are not stored in this repo;
notebooks download them from the official archive:
https://github.com/StackExchange/Survey

## Progress
- [x] Data exploration (Stack Overflow Developer Survey, 2019-2025)
- [x] DSC102 Practical 1: cleaning, scaling (Min-Max, standardisation), PCA,
      feature selection (correlation filter, chi-square)
- [x] DSC102 Practical 2: bias-variance trade-off (synthetic data), effect of
      many features and PCA, polynomial trend fitting on survey data
  - Using the same 300 training sets for every polynomial degree, bias² falls
    and variance rises with degree; total error is lowest at moderate degrees.
  - Trend direction was checked with two measures (share of respondents, share
    of mentions): TypeScript, PowerShell and Python rise; Java, HTML/CSS,
    JavaScript, C# and PHP fall; C, C++ and SQL are roughly flat.
- [ ] DSC102 Practicals 3 and 5: salary prediction (in progress)
- [ ] Classification, SVM, neural network, clustering
- [ ] Streamlit app

## Limitations
- Survey respondents are a self-selected sample of developers, not the whole
  IT industry; question wording and respondent mix change across years.
- Several languages shift together between 2020/2021 and 2024/2025, which may
  reflect survey or respondent-mix changes rather than real skill changes.
- Answer options for shells changed across years (Bash/Shell/PowerShell
  combined in 2019-2020, separate in 2021-2022, "Bash/Shell (all shells)"
  from 2023), so Bash/Shell is excluded from trend analysis.
- Trend outlooks are based on only 7 yearly points and are rough guides,
  not forecasts to rely on.
- Some preprocessing choices (top countries/skills, salary median) were
  computed before the train/test split, a minor leakage.