import os
from platformdirs import user_config_dir
import yaml
import logging
import copy

log = logging.getLogger(__name__)


# This is to fill in the defaults so there's not too many variables
config = {
    "default_template": '',
    "default_input_file": 'reportbody.md',
    "default_output_file": 'report-preview.md',
    "format": '',
    "verbose": False,
    # The template mapper. This gives the locations of template files for each template.
    "templatemapper": {
    },
    # Additional template mapper files to link.
    "templatemappers": [
    ],
    # Files with additional
    "includes": {
    }
}

envvars = {
    'RR_TEMPLATE': "defaulttemplate",
    'RR_INPUT_FILE': 'default_input_file'
}

def get_config_from_file(file):
    try:
        with open(file, 'r') as vf:
            config = yaml.safe_load(vf)
            log.info(f"Processing file {file}")
            return config
    except:
        log.info(f"Could not open config file {file}")
        return {}

def get_config(arg_file = None):
    final_config = copy.copy(config)

    # Sort out environment variables
    for envvar in envvars.keys():
        var = os.getenv(envvar)
        if var != None:
            final_config[envvars[envvar]] = var
    
    for config_location in [user_config_dir('reportranger', 'Volkis') + '/config.yml', 'config.yml', arg_file]:
        if config_location:
            final_config.update(get_config_from_file(config_location))
    log.info(f"Final config: {final_config}")
    return final_config

