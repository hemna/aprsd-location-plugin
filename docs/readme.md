# APRSD location plugin

[![PyPI](https://img.shields.io/pypi/v/aprsd-location-plugin.svg)](https://pypi.org/project/aprsd-location-plugin/)
[![Status](https://img.shields.io/pypi/status/aprsd-location-plugin.svg)](https://pypi.org/project/aprsd-location-plugin/)
[![Python Version](https://img.shields.io/pypi/pyversions/aprsd-location-plugin)](https://pypi.org/project/aprsd-location-plugin)
[![License](https://img.shields.io/pypi/l/aprsd-location-plugin)](https://opensource.org/licenses/Apache%20Software%20License%202.0)

[![Read the Docs](https://img.shields.io/readthedocs/aprsd-location-plugin/latest.svg?label=Read%20the%20Docs)](https://aprsd-location-plugin.readthedocs.io/)
[![Tests](https://github.com/hemna/aprsd-location-plugin/workflows/Tests/badge.svg)](https://github.com/hemna/aprsd-location-plugin/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/hemna/aprsd-location-plugin/branch/main/graph/badge.svg)](https://codecov.io/gh/hemna/aprsd-location-plugin)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Features

* Query the last known GPS location of any APRS callsign
* Reverse geocode GPS coordinates to human-readable locations
* Support for multiple geocoding services (Nominatim, Google, Bing, etc.)
* Free US Government geocoder option for US locations
* Automatic altitude and time-since-last-beacon information
* Works with any callsign or defaults to the calling station

## Requirements

* APRSD server (version 3.4.4 or higher)
* aprs.fi API key (free at https://aprs.fi/api/info)
* Python 3.8 or higher
* geopy library (automatically installed)
* oslo_config library (automatically installed)

**Optional (for commercial geocoders):**
* API keys for Google, Bing, HERE, OpenCage, TomTom, Azure Maps, Baidu, What3Words, or Woosmap

## Installation

You can install *APRSD location plugin* via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):

```console
$ pip install aprsd-location-plugin
```

Or install from source:

```console
$ git clone https://github.com/hemna/aprsd-location-plugin.git
$ cd aprsd-location-plugin
$ pip install -e .
```

## Configuration

The plugin requires configuration in your APRSD configuration file. Add the following section:

```ini
[aprsd_location_plugin]
enabled = True
geopy_geocoder = Nominatim
user_agent = APRSD

# Optional: API keys for commercial geocoders
# google_api_key = your-google-api-key
# bing_api_key = your-bing-api-key
# here_api_key = your-here-api-key
# opencage_api_key = your-opencage-api-key
# tomtom_api_key = your-tomtom-api-key
# azuremaps_subscription_key = your-azure-key
# baidu_api_key = your-baidu-key
# what3words_api_key = your-what3words-key
# woosmap_api_key = your-woosmap-key

# For ArcGIS geocoder (requires username and password)
# arcgis_username = your-username
# arcgis_password = your-password
```

### Configuration Options

* `enabled` (boolean, default: False)
  Enable or disable the location plugin. Must be set to `True` for the plugin to work.

* `geopy_geocoder` (string, default: "Nominatim")
  The geocoding service to use. Available options:

  * `Nominatim` - Free OpenStreetMap geocoder (no API key required, rate limited)
  * `USGov` - Free US Government geocoder (US locations only, no API key required)
  * `GoogleV3` - Google Geocoding API (requires API key)
  * `Bing` - Bing Maps API (requires API key)
  * `HERE` - HERE Geocoding API (requires API key)
  * `OpenCage` - OpenCage Geocoding API (requires API key)
  * `TomTom` - TomTom Geocoding API (requires API key)
  * `AzureMaps` - Azure Maps API (requires subscription key)
  * `Baidu` - Baidu Maps API (requires API key)
  * `What3Words` - What3Words API (requires API key)
  * `Woosmap` - Woosmap Geocoding API (requires API key)
  * `ArcGIS` - ArcGIS Geocoding API (requires username and password)

* `user_agent` (string, default: "APRSD")
  User agent string sent to geocoding services. For Nominatim, you should use a unique identifier for your application.

* **API Key Options**
  Set the appropriate API key option based on your chosen geocoder. Only the key for the selected geocoder is required.

## Usage

The Location Plugin responds to APRS message commands to retrieve the last known GPS location of a callsign.

### Command Syntax

The plugin recognizes the following commands:

* `l` - Get location of the calling station
* `l` (with trailing space) - Get location of the calling station
* `location` - Get location of the calling station
* `l CALLSIGN` - Get location of a specific callsign
* `location CALLSIGN` - Get location of a specific callsign

### Example Interactions

#### Example 1: Query your own location

Send an APRS message to your APRSD server:

```
l
```

Response:

```
K1ABC: Appomattox, VA 1250' 37.35,-78.82 2.3h ago
```

This shows:
* Callsign: K1ABC
* Location: Appomattox, VA (county and state for US locations)
* Altitude: 1250 feet
* Coordinates: 37.35°N, 78.82°W
* Time since last beacon: 2.3 hours ago

#### Example 2: Query another station's location

Send an APRS message:

```
l N0CALL
```

Response:

```
N0CALL: Denver, CO 5280' 39.74,-104.99 0.5h ago
```

#### Example 3: Using the full command

Send an APRS message:

```
location W1AW
```

Response:

```
W1AW: Newington, CT 150' 41.70,-72.73 1.2h ago
```

#### Example 4: International location

For non-US locations, the format may vary:

```
VE3ABC: Toronto, ON 500' 43.65,-79.38 0.8h ago
```

#### Example 5: Station with no recent location

If a callsign has no recent APRS data:

```
Failed to fetch aprs.fi location
```

#### Example 6: Location with unknown reverse geocode

If reverse geocoding fails but GPS coordinates are available:

```
K1ABC: Unknown Location 0' 37.35,-78.82 2.3h ago
```

### How It Works

1. User sends an APRS message with the command `l` or `location` (optionally with a callsign)
2. Plugin queries aprs.fi API to get the last known GPS coordinates for the callsign
3. Plugin uses the configured geocoding service to reverse geocode the coordinates
4. Plugin formats and returns a human-readable location response

The response includes:
* The callsign queried
* Human-readable location (county/state for US, or country for international)
* Altitude in feet
* GPS coordinates (latitude, longitude)
* Time elapsed since the last APRS beacon

### Enabling the Plugin

To enable the plugin in APRSD, add it to your enabled plugins list in the APRSD configuration:

```ini
[aprsd]
enabled_plugins = aprsd.plugins.location.LocationPlugin
```

Or use the entry point name:

```ini
[aprsd]
enabled_plugins = location
```

The plugin will automatically be discovered if installed and configured properly.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide](contributing).

## License

Distributed under the terms of the [Apache Software License 2.0 license](https://opensource.org/licenses/Apache%20Software%20License%202.0),
*APRSD location plugin* is free and open source software.

## Issues

If you encounter any problems,
please [file an issue](https://github.com/hemna/aprsd-location-plugin/issues) along with a detailed description.

## Credits

This project was generated from [@hemna](https://github.com/hemna)'s [APRSD Plugin Python Cookiecutter](https://github.com/hemna/cookiecutter-aprsd-plugin) template.
