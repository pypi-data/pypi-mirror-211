from komora_syncer.config import LoggingConfig
from komora_syncer.models.Synchronizer import Synchronizer

import os
import sys
import click
import traceback

from logging.config import fileConfig as logging_fileConfig
import logging
logger = logging.getLogger(__name__)


def setup_logger():
    try:
        log_conf = LoggingConfig()
        logging_fileConfig(log_conf._config, disable_existing_loggers=False)
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.critical("Exiting")
        sys.exit()
    except Exception as e:
        raise e


@click.group()
def cli():
    pass


SYNC_OPTIONS = ['all', 'organizations', 'regions', 'sites', 'devices']
@cli.command()
@click.option('--sync', '-s', type=click.Choice(SYNC_OPTIONS), multiple=True, default=['all'], help="what should be synced")
@click.option('--configs', '-c', type=click.Path(), multiple=False, help="path to folder with configurations")
@click.option('--site', '-t', type=click.STRING, help="Name of site to deploy")
def synchronize(sync, configs, site):
    """
    Synchronize data between Netbox and Komora
    """

    # set custom configs folder path
    if configs:
        os.environ["CONFIG_FOLDER_PATH"] = os.path.abspath(configs)
    setup_logger()

    synchronizer = Synchronizer()
    
    if site and 'sites' not in sync:
        logger.critical("Site option '--site' is only available with sites 'synchronize --sync sites' synchronization")
        logger.critical("Exiting")
        return

    if site and 'sites' in sync:
        try:
            # Syncs Sites / Site, Location
            synchronizer.sync_sites(site_name=site)
            return
        except Exception as e:
            logger.error(f"Unable to synchronize site '{site}' - {e}")
            logger.debug(f"{e}\n{traceback.format_exc()}")
            logger.critical("Exiting")
            return

    if 'all' in sync or 'organizations' in sync:
        try:
            # Syncs Organizations / Tenants
            synchronizer.sync_organizations()
        except Exception as e:
            logger.error(f"Unable to synchronize organizations")
            logger.debug(f"{e}\n{traceback.format_exc()}")
            logger.critical("Exiting")
            return

    if 'all' in sync or 'regions' in sync:
        try:
            # Syncs Regions, Disctricts and Municipalities / Regions
            synchronizer.sync_regions()
        except Exception as e:
            logger.error(f"Unable to synchronize regions")
            logger.debug(f"{e}\n{traceback.format_exc()}")
            logger.critical("Exiting")
            return

    if 'all' in sync or 'sites' in sync:
        try:
            # Syncs Sites / Site, Location
            synchronizer.sync_sites()
        except Exception as e:
            logger.error(f"Unable to synchronize sites")
            logger.debug(f"{e}\n{traceback.format_exc()}")
            logger.critical("Exiting")
            return

    if 'all' in sync or 'devices' in sync:
        try:
            synchronizer.sync_devices()
        except Exception as e:
            logger.error(f"Unable to synchronize devices")
            logger.debug(f"{e}\n{traceback.format_exc()}")
            logger.critical("Exiting")
            return


if __name__ == "__main__":
    # Display CLI
    cli()
