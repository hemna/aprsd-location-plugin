.. highlight:: shell

========
Usage
========

The Location Plugin responds to APRS message commands to retrieve the last known GPS location of a callsign.

Command Syntax
==============

The plugin recognizes the following commands:

* ``l`` - Get location of the calling station
* ``l`` (with trailing space) - Get location of the calling station
* ``location`` - Get location of the calling station
* ``l CALLSIGN`` - Get location of a specific callsign
* ``location CALLSIGN`` - Get location of a specific callsign

Example Interactions
====================

Example 1: Query your own location
-----------------------------------

Send an APRS message to your APRSD server:

::

   l

Response:

.. code-block:: text

   K1ABC: Appomattox, VA 1250' 37.35,-78.82 2.3h ago

This shows:
* Callsign: K1ABC
* Location: Appomattox, VA (county and state for US locations)
* Altitude: 1250 feet
* Coordinates: 37.35°N, 78.82°W
* Time since last beacon: 2.3 hours ago

Example 2: Query another station's location
--------------------------------------------

Send an APRS message:

::

   l N0CALL

Response:

.. code-block:: text

   N0CALL: Denver, CO 5280' 39.74,-104.99 0.5h ago

Example 3: Using the full command
----------------------------------

Send an APRS message:

::

   location W1AW

Response:

.. code-block:: text

   W1AW: Newington, CT 150' 41.70,-72.73 1.2h ago

Example 4: International location
-----------------------------------

For non-US locations, the format may vary:

.. code-block:: text

   VE3ABC: Toronto, ON 500' 43.65,-79.38 0.8h ago

Example 5: Station with no recent location
------------------------------------------

If a callsign has no recent APRS data:

::

   Failed to fetch aprs.fi location

Example 6: Location with unknown reverse geocode
-------------------------------------------------

If reverse geocoding fails but GPS coordinates are available:

.. code-block:: text

   K1ABC: Unknown Location 0' 37.35,-78.82 2.3h ago

How It Works
============

1. User sends an APRS message with the command ``l`` or ``location`` (optionally with a callsign)
2. Plugin queries aprs.fi API to get the last known GPS coordinates for the callsign
3. Plugin uses the configured geocoding service to reverse geocode the coordinates
4. Plugin formats and returns a human-readable location response

The response includes:
* The callsign queried
* Human-readable location (county/state for US, or country for international)
* Altitude in feet
* GPS coordinates (latitude, longitude)
* Time elapsed since the last APRS beacon

Configuration
=============

The plugin requires configuration in your APRSD configuration file. Add the following section:

.. code-block:: ini

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

Configuration Options
---------------------

enabled
~~~~~~~

* Type: boolean
* Default: False
* Description: Enable or disable the location plugin. Must be set to ``True`` for the plugin to work.

geopy_geocoder
~~~~~~~~~~~~~~

* Type: string
* Default: "Nominatim"
* Choices: ArcGIS, AzureMaps, Baidu, Bing, GoogleV3, HERE, Nominatim, OpenCage, TomTom, USGov, What3Words, Woosmap
* Description: The geocoding service to use.

  * ``Nominatim`` - Free OpenStreetMap geocoder (no API key required, rate limited)
  * ``USGov`` - Free US Government geocoder (US locations only, no API key required)
  * ``GoogleV3`` - Google Geocoding API (requires API key)
  * ``Bing`` - Bing Maps API (requires API key)
  * ``HERE`` - HERE Geocoding API (requires API key)
  * ``OpenCage`` - OpenCage Geocoding API (requires API key)
  * ``TomTom`` - TomTom Geocoding API (requires API key)
  * ``AzureMaps`` - Azure Maps API (requires subscription key)
  * ``Baidu`` - Baidu Maps API (requires API key)
  * ``What3Words`` - What3Words API (requires API key)
  * ``Woosmap`` - Woosmap Geocoding API (requires API key)
  * ``ArcGIS`` - ArcGIS Geocoding API (requires username and password)

user_agent
~~~~~~~~~~

* Type: string
* Default: "APRSD"
* Description: User agent string sent to geocoding services. For Nominatim, you should use a unique identifier for your application.

API Key Options
~~~~~~~~~~~~~~~

Set the appropriate API key option based on your chosen geocoder. Only the key for the selected geocoder is required:

* ``google_api_key`` - For GoogleV3 geocoder
* ``bing_api_key`` - For Bing geocoder
* ``here_api_key`` - For HERE geocoder
* ``opencage_api_key`` - For OpenCage geocoder
* ``tomtom_api_key`` - For TomTom geocoder
* ``azuremaps_subscription_key`` - For AzureMaps geocoder
* ``baidu_api_key`` - For Baidu geocoder
* ``what3words_api_key`` - For What3Words geocoder
* ``woosmap_api_key`` - For Woosmap geocoder
* ``arcgis_username`` and ``arcgis_password`` - For ArcGIS geocoder

Enabling the Plugin
===================

To enable the plugin in APRSD, add it to your enabled plugins list in the APRSD configuration:

.. code-block:: ini

   [aprsd]
   enabled_plugins = aprsd.plugins.location.LocationPlugin

Or use the entry point name:

.. code-block:: ini

   [aprsd]
   enabled_plugins = location

The plugin will automatically be discovered if installed and configured properly.

Prerequisites
=============

* APRSD server (version 3.4.4 or higher)
* aprs.fi API key (free at https://aprs.fi/api/info)
* The API key must be configured in your APRSD config under ``[aprs_fi]`` section:

.. code-block:: ini

   [aprs_fi]
   apiKey = your-aprs-fi-api-key

Troubleshooting
===============

Plugin not responding
---------------------

* Verify the plugin is enabled in both ``[aprsd_location_plugin]`` and ``[aprsd]`` sections
* Check that your aprs.fi API key is configured correctly
* Ensure the plugin is installed: ``pip list | grep aprsd-location-plugin``

"Failed to fetch aprs.fi location"
-----------------------------------

* The callsign may not have any recent APRS data
* Check that your aprs.fi API key is valid
* Verify the callsign exists and has transmitted recently

"Unknown Location"
------------------

* The reverse geocoding service may have failed
* Try switching to a different geocoder (e.g., from Nominatim to USGov for US locations)
* Check API key if using a commercial geocoder
* Verify network connectivity to the geocoding service

Rate limiting (Nominatim)
--------------------------

* Nominatim has rate limits for free usage
* Consider using a commercial geocoder for higher volume
* Or use the USGov geocoder for US locations (no rate limits)
