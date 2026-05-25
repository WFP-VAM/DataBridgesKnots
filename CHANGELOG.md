## v3.0.2 (2026-05-25)

### Fix

- change structure of tests to separate unit from integration testing

## v3.0.1 (2026-05-25)

### Fix

- change structure of tests to separate unit from integration testing
- remove broken redundant tag step from semver workflow

## v3.0.0 (2026-05-22)

### BREAKING CHANGE

- **client**: add default API version to `DataBridgesShape` initialization; rename `get_household_xslform_definition` → `get_household_xlsform_definition` (XLSForm typo fix)

### Feat

- **client**: rename auth params and procedure to align with new WFP API Portal (portal.api.wfp.org)

### Fix

- add mandatory `country_iso3` param to `get_market_geojson_list`, fix response as geoJSON
- `get_economic_indicator_list` response returned as DataFrame
- remove obsolete endpoints
- remove obsolete SCOPES from client
- remove unused deprecation warning

## 2.1.4 (2026-05-19)

### Fix

- tests for market_geojson
- add mandatory country_iso3 param to get_market_geojson_list, fix  response as geoJSON and add tests for it
- get_economic_indicator_list response as data_frame
- remove obsolete endpoints
- host in client
- remove obsolete SCOPES from client
- remove unused deprecation warning
- deprecation warning

## v2.1.3 (2026-05-19)

### Feat

- add RPME endpoints
- IncubationApi Household Surveys endpoints

### Fix

- rename label functions to more descriptive names
- import pandas in conftest
- tests work with API call
- pd.Dataframe output as long dataset, instead of wide
- get_column_labels now can return the output as pd.Dataframe
- get_column_label bug and tests
- **helpers**: add typing and better naming parameters to get_column_label and get_value_label functions
- **DataBridgesShape**: make a fresh call to _setup_configuration_and_authentication() instead of using cached result
- add end_date and other optional parameters on get_prices(). Add start_date as replacement to survey_date (backward compatibile)
- Ensure country_is03 is truly optional in get_household_surveys_list
- failed example on MFI data
- examples in docstrings'
- consolidate iso3code to adm0 code conversion for all methods
- consolidate examples and country_code for get_commodit_list, get_makrets_list() and get_nearby_markets()
- improve handling of Data Bridges API key
- handle DATA_BRIDGES_API if doesn't exist in config file
- indentation in .github/workflow
- update python-package.yml
- typo in python-package.yml
- get_household_questionnaire and get_choice_list functions to retrieve correct information

### Refactor

- move label functions under label.py and create basic tests

### Perf

- Cache country codes_mapping to avoid multiple file reads
