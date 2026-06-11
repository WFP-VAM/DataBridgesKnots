# Roadmap for DataBridgesKnots

This document outlines the planned features and improvements for the `DataBridgesKnots` package, which provides a wrapper for the WFP Data Bridges API.

## 1.0.0 "Brilliant Bigfoot" (DataBridges API v5.0.0)

### New Features
- [X] Endpoints: CommoditiesApis
- [X] Endpoints: CurrencyApi
- [X] Endpoints: EconomicDataApi
- [X] Endpoints: MarketsApi
- [X] Endpoints: FoodSecurityApi
- [X] Endpoints: GorpApi
- [X] Endpoints: MarketPricesAPi
- [X] Endpoints: IncubationApi
- [X] Endpoints: RpmeApi
- [X] Endpoints: XlsFormsApi
- [X] Endpoints: SurveysApi

## 2.0.0 "Cheerful Chimera" (DataBridges API v6.0.0)

- [X] Fix optional dependencies for STATA
- [X] Update setup.py and pyproject.toml to include DataBridges API v6.0
- [X] R example files
- [X] Documentation: Enhance documentation and provide more usage examples
- [X] Automation: GitHub Actions linting and testing

# v3.0.0 "Delicate Dragon" (DataBridgesAPI v1.0.0 - new API)
- [X] Testing: Unit testing for implemented endpotns 

## v3.1.5
- [X] Refactor client.py into modules (e.g. `endpoints/household.py`)
- [X] Add get_commodity_list_get
- [X] Soft deprecation `DataBridgesShape`
- [X] Bug fixing: Market list JSON and CSV
- [X] Bug fixing: Markets GeoJSON response
- [X] Testing: Add tests for helper functions (labels)

# v4.0.0

- [X] Add parameters for `get_household_survey` FullData
- [X] Update endpoints to `v2`
- [ ] Deprecate `DataBridgesShape`
- [ ] Update documentation for v4.x
- [ ] Add tests for existing endpoints (integration + unit)

# Future releases

## Minors
- [ ] Add missing endpoints
  - [ ] RpmeApi
  - [ ] IpcchApi
  - [ ] GlobalOutlookApi
- [ ] STATA support
- [ ] Add helper functions to search surveys
- [ ] Add option to write to file / retrieve partial results (time-out)
- [ ] Add option to use polars

## Patch
- [ ] Add tests for additional endpoints
