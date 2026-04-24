## 2.2.0 (2026-04-23)

### Fix

- **DataBridgesShape**: make a fresh call to _setup_configuration_and_authentication() instead of using cached result
- add end_date and other optional parameters on get_prices(). Add start_date as replacement to survey_date (backward compatibile)

## v2.1.0 (2025-10-13)

### Fix

- Ensure country_is03 is truly optional in get_household_surveys_list
- failed example on MFI data
- examples in docstrings'
- consolidate iso3code to adm0 code conversion for all methods
- consolidate examples and country_code for get_commodit_list, get_makrets_list() and get_nearby_markets()
- improve handling of Data Bridges API key

### Perf

- Cache country codes_mapping to avoid multiple file reads

## v2.0.0 (2025-10-08)

### BREAKING CHANGE

- All class methods require country_iso3 (instead of mix of country_code, country_iso3 and adm0code)

### Feat

- merge conflits, fix documentation example and consolidate country parameters to country_iso3

## v0.4.0 (2025-10-08)

### Fix

- failed example on MFI data
- examples in docstrings'
- consolidate iso3code to adm0 code conversion for all methods
- consolidate examples and country_code for get_commodit_list, get_makrets_list() and get_nearby_markets()
- improve handling of Data Bridges API key
- handle DATA_BRIDGES_API if doesn't exist in config file
- indentation in .github/workflow
- update python-package.yml
- typo in python-package.yml

## v1.0.0 (2024-11-29)

### Feat

- add RPME endpoints
- IncubationApi Household Surveys endpoints

### Fix

- get_household_questionnaire and get_choice_list functions to retrieve correct information

## v0.1.0 (2024-06-18)
