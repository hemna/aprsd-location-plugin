from oslo_config import cfg

plugin_group = cfg.OptGroup(
    name="aprsd_location_plugin",
    title="APRSD Slack Plugin settings",
)

plugin_opts = [
    cfg.BoolOpt(
        "enabled",
        default=False,
        help="Enable the plugin?",
    ),
    cfg.StrOpt(
        "geopy_geocoder",
        choices=[
            "ArcGIS",
            "AzureMaps",
            "Baidu",
            "Bing",
            "GoogleV3",
            "HERE",
            "Nominatim",
            "OpenCage",
            "TomTom",
            "USGov",
            "What3Words",
            "Woosmap",
        ],
        default="Nominatim",
        help="The geopy geocoder to use.  Default is Nominatim."
        "See https://geopy.readthedocs.io/en/stable/#module-geopy.geocoders"
        "for more information.",
    ),
    cfg.StrOpt(
        "user_agent",
        default="APRSD",
        help="The user agent to use for the Nominatim geocoder."
        "See https://geopy.readthedocs.io/en/stable/#module-geopy.geocoders"
        "for more information.",
    ),
    cfg.StrOpt(
        "arcgis_username",
        default=None,
        help="The username to use for the ArcGIS geocoder."
        "See https://geopy.readthedocs.io/en/latest/#arcgis"
        "for more information."
        "Only used for the ArcGIS geocoder.",
    ),
    cfg.StrOpt(
        "arcgis_password",
        default=None,
        help="The password to use for the ArcGIS geocoder."
        "See https://geopy.readthedocs.io/en/latest/#arcgis"
        "for more information."
        "Only used for the ArcGIS geocoder.",
    ),
    cfg.StrOpt(
        "azuremaps_subscription_key",
        help="The subscription key to use for the AzureMaps geocoder."
        "See https://geopy.readthedocs.io/en/latest/#azuremaps"
        "for more information."
        "Only used for the AzureMaps geocoder.",
    ),
    cfg.StrOpt(
        "baidu_api_key",
        help="The API key to use for the Baidu geocoder."
        "See https://geopy.readthedocs.io/en/latest/#baidu"
        "for more information."
        "Only used for the Baidu geocoder.",
    ),
    cfg.StrOpt(
        "bing_api_key",
        help="The API key to use for the Bing geocoder."
        "See https://geopy.readthedocs.io/en/latest/#bing"
        "for more information."
        "Only used for the Bing geocoder.",
    ),
    cfg.StrOpt(
        "google_api_key",
        help="The API key to use for the Google geocoder."
        "See https://geopy.readthedocs.io/en/latest/#googlev3"
        "for more information."
        "Only used for the Google geocoder.",
    ),
    cfg.StrOpt(
        "here_api_key",
        help="The API key to use for the HERE geocoder."
        "See https://geopy.readthedocs.io/en/latest/#here"
        "for more information."
        "Only used for the HERE geocoder.",
    ),
    cfg.StrOpt(
        "opencage_api_key",
        help="The API key to use for the OpenCage geocoder."
        "See https://geopy.readthedocs.io/en/latest/#opencage"
        "for more information."
        "Only used for the OpenCage geocoder.",
    ),
    cfg.StrOpt(
        "tomtom_api_key",
        help="The API key to use for the TomTom geocoder."
        "See https://geopy.readthedocs.io/en/latest/#tomtom"
        "for more information."
        "Only used for the TomTom geocoder.",
    ),
    cfg.StrOpt(
        "what3words_api_key",
        help="The API key to use for the What3Words geocoder."
        "See https://geopy.readthedocs.io/en/latest/#what3words"
        "for more information."
        "Only used for the What3Words geocoder.",
    ),
    cfg.StrOpt(
        "woosmap_api_key",
        help="The API key to use for the Woosmap geocoder."
        "See https://geopy.readthedocs.io/en/latest/#woosmap"
        "for more information."
        "Only used for the Woosmap geocoder.",
    ),
]

ALL_OPTS = plugin_opts


def register_opts(cfg):
    cfg.register_group(plugin_group)
    cfg.register_opts(ALL_OPTS, group=plugin_group)


def list_opts():
    return {
        plugin_group.name: plugin_opts,
    }
