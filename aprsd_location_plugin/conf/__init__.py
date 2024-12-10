from oslo_config import cfg

from aprsd_location_plugin.conf import main


CONF = cfg.CONF
main.register_opts(CONF)
