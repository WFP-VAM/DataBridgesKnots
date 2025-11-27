from typing import Dict, Optional

import json
from pathlib import Path

# Cache return value from _load_country_codes() into global variable
codes_mapping = None


def _load_country_codes() -> Dict[str, int]:
    """Load country codes mapping from JSON file.

    Returns:
        Dict[str, int]: Mapping of ISO3 codes to ADM0 codes

    Examples:
        >>> codes = _load_country_codes()
        >>> isinstance(codes, dict)
        True
    """
    global codes_mapping
    if codes_mapping is None:
        try:
            json_path = Path(__file__).parent / "country_list.json"
            with open(json_path, "r", encoding="utf-8") as f:
                country_list = json.load(f)

            codes_mapping = {
                country["iso3Alpha3"]: country["adm0Code"]
                for country in country_list
                if country.get("adm0Code") is not None
                and country.get("iso3Alpha3") is not None
            }
        except FileNotFoundError:
            raise FileNotFoundError(f"Country list file not found at {json_path}")

    return codes_mapping


def get_adm0_code(country_iso3: str) -> Optional[int]:
    """Get ADM0 code for a given ISO3 country code.

    Args:
        iso3 (str): ISO3 country code (e.g. 'AFG' for Afghanistan)

    Returns:
        Optional[int]: ADM0 code if found, None if not found

    Examples:
        >>> code = get_code("ETH")  # Ethiopia
        >>> isinstance(code, int)
        True
        >>> get_code("XXX") is None  # Invalid code
        True
    """

    if not isinstance(country_iso3, str):
        raise TypeError("iso3 must be a string")

    codes = _load_country_codes()
    return codes.get(country_iso3.upper())

