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
