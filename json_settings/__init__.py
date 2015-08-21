import json
import logging
import os
import sys


def json_patch(path):
    logging.warn("Attempting to load local settings from %r" % (path,))
    try:
        d = json.load(open(path))
    except IOError:
        logging.exception("Unable to open json settings in %r" % (path,))
        raise SystemExit(-1)
    except ValueError:
        logging.exception("Unable to parse json settings in %r" % (path,))
        raise SystemExit(-1)
    for k, v in d.items():
        globals()[k] = v


def patch_settings(json_settings_file):
    env_settings = os.environ.get('JSON_SETTINGS', None)
    if env_settings is None:
        # We only use the default if it exists
        env_settings = os.path.join(sys.prefix, "etc", json_settings_file)
        if not os.path.exists(env_settings):
            return
    json_patch(env_settings)
    if "VAR_DIRECTORY" not in globals():
        globals()["VAR_DIRECTORY"] = os.path.join(sys.prefix, "var")
    if "STATIC_ROOT" not in globals():
        globals()["STATIC_ROOT"] = os.path.join(
            globals()["VAR_DIRECTORY"], "static")
    if "MEDIA_ROOT" not in globals():
        globals()["MEDIA_ROOT"] = os.path.join(
            globals()["VAR_DIRECTORY"], "media")
