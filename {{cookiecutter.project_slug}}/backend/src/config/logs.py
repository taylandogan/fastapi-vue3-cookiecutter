import logging.config
from config.base import Settings


def configure(settings: Settings) -> None:
    debug = getattr(settings, "DEBUG", False)
    logging.config.dictConfig(
        # fmt: off
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "throttle_elastic_failures": {"()": "de.core.log.filters.ThrottleElasticFailures"},
            },
            "root": {
                "level": "DEBUG" if debug else "INFO",
                "handlers": ["console"]
            },
            "formatters": {
                "default": {"format": "[%(asctime)s] %(levelname)-8s %(name)-20s :: %(message)s", "use_colors": True},
                "access": {"use_colors": True}
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "loggers": {},
        }
        # fmt: on
    )
    logging.getLogger("aioredis").setLevel(logging.INFO)
