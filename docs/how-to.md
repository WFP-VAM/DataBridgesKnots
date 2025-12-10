# User Guide

## Quick start

### Python

Run the following example to extract commodity data:
```python

from data_bridges_knots import DataBridgesShapes

CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

# COMMODITY DATA
commodity_units_list = client.get_commodity_units_list(country_iso3="TZA", commodity_unit_name="Kg", page=1, format='json')

```

### R

```R
library(reticulate)

# Import the Python module through reticulate
data_bridges_knots <- import("data_bridges_knots")

# Point to our virtual environment's Python
use_python(".venv/bin/python")

# Create client instance
config_path <- "data_bridges_api_config.yaml"
client <- data_bridges_knots$DataBridgesShapes(config_path)

# COMMODITY DATA
# Get commodity unit list for Tanzania
commodity_units <- client$get_commodity_units_list(
  country_code = "TZA",
  commodity_unit_name = "Kg",
  page = 1L,
  format = "json"
)
```
Examples on how to use the package  are  in the [examples](https://github.com/WFP-VAM/DataBridgesKnots/tree/main/examples) folder and in the [API Reference document](https://wfp-vam.github.io/DataBridgesKnots/reference/)


## Getting variable and choice labels

DataBridgesKnots come with some helper functions to make the datasets more human-readable. 
 

::: data_bridges_knots.labels.get_variable_labels

::: data_bridges_knots.labels.get_choice_labels

::: data_bridges_knots.labels.map_value_labels
