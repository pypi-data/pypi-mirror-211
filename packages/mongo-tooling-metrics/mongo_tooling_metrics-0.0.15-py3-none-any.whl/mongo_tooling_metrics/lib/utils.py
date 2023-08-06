import os

MONGOD_INTENRAL_DISTRO_FILEPATH = '/etc/mongodb-distro-name'
SUPPORTED_VIRTUAL_WORKSTATION_NAMES = set(
    ["ubuntu2204-workstation-graviton", "ubuntu2204-workstation", "ubuntu1804-workstation"])


def _is_virtual_workstation() -> bool:
    """Detect whether this is a MongoDB internal virtual workstation."""
    try:
        with open(MONGOD_INTENRAL_DISTRO_FILEPATH, 'r') as file:
            return file.read().strip() in SUPPORTED_VIRTUAL_WORKSTATION_NAMES
    except Exception as _:
        return False


TOOLING_METRICS_OPT_OUT = "TOOLING_METRICS_OPT_OUT"


def _has_metrics_opt_out() -> bool:
    """Check whether the opt out environment variable is set."""
    return os.environ.get(TOOLING_METRICS_OPT_OUT, None) == '1'


def should_collect_internal_metrics() -> bool:
    """Check whether we should collect internal metrics for this host."""
    return _is_virtual_workstation() and not _has_metrics_opt_out()
