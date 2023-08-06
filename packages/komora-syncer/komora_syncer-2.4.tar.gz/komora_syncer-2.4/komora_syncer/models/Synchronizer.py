from komora_syncer.models.komora.KomoraApi import KomoraApi
from komora_syncer.models.netbox.NbSite import NbSite
from komora_syncer.models.netbox.NbRegion import NbRegion
from komora_syncer.models.netbox.NbTenant import NbTenant
from komora_syncer.models.netbox.NbDevice import NbDevice

from komora_syncer.connections.NetboxConnection import NetboxConnection

import logging
logger = logging.getLogger(__name__)


class Synchronizer:
    def __init__(self):
        self.komora_api = KomoraApi()

        # Lists of komora sites
        self.sites = []

        # All location data from komora - RUIAN
        self.regions_all = []
        self.districs_all = []
        self.municipalities_all = []

        # Locations assigned to Sites in komora (will be created in Netbox)
        self.regions_assigned = []
        self.districts_assigned = []
        self.municipalities_assigned = []

    # pull all Regions and sites from komora
    def __prepare_all_regions(self):
        if not self.regions_all:
            self.regions_all = self.komora_api.get_regions()
        if not self.municipalities_all:
            self.municipalities_all = self.komora_api.get_municipalities()
        if not self.districs_all:
            self.districs_all = self.komora_api.get_districts()
        if not self.sites:
            self.sites = self.komora_api.get_sites()

    # Fill the assigned locations only
    def __prepare_assigned_regions(self):
        if not self.regions_all or not self.municipalities_all or not self.districs_all or not self.sites:
            self.__prepare_all_regions()

        # municipalities sets on sites - site.address exists
        municipalities_on_sites = [[site.address.municipalityName,
                                    site.address.districtName] for site in self.sites if site.address]
        self.municipalities_assigned = [muni for muni in self.municipalities_all if [
            muni.name, muni.districtName] in municipalities_on_sites]

        # get districts from step aboce
        districts_on_assigned_municipalities = set(
            municipality.districtName for municipality in self.municipalities_assigned)
        self.districts_assigned = [
            dis for dis in self.districs_all if dis.name in districts_on_assigned_municipalities]

        # get regions from step above
        regions_on_assigned_districts = set(
            district.regionName for district in self.districts_assigned)
        self.regions_assigned = [
            reg for reg in self.regions_all if reg.name in regions_on_assigned_districts]

        # get sites where address from ruian does not exists
        #   but region is assigned - foreign regions for example
        sites_without_address_with_region = [[site.regionId, site.regionName] for site in self.sites if not site.address and site.regionId]
        # get regions from sites without address and append them
        self.regions_assigned.extend([reg for reg in self.regions_all if [reg.id, reg.name] in sites_without_address_with_region])

    def sync_regions(self):
        if not self.regions_assigned or not self.municipalities_assigned or not self.districts_assigned or not self.sites:
            self.__prepare_assigned_regions()

        logger.info("Synchronizing regions")
        # sync regions
        for reg in self.regions_assigned:
            nb_region = NbRegion(reg, 'region')
            nb_region.synchronize()

        # sync Districts
        for dis in self.districts_assigned:
            nb_region = NbRegion(dis, 'district')
            nb_region.synchronize()

        # sync Municipatilies
        for muni in self.municipalities_assigned:
            nb_region = NbRegion(muni, 'municipality')
            nb_region.synchronize()

    def sync_sites(self, site_name=None):
        try:
            if not self.sites:
                self.sites = self.komora_api.get_sites()
        except Exception as e:
            raise e

        # If a site name is specified, synchronize only that site
        if site_name:
            logger.info("Synchronizing site: {}".format(site_name))
            
            found_sites = [site for site in self.sites if site.name == site_name]
            if len(found_sites) == 0:
                raise ValueError(f"No object found with name '{site_name}'")
            elif len(found_sites) > 1:
                raise ValueError(f"Multiple objects found with name '{site_name}'")
            else:
                nb_site = NbSite(found_sites[0])
                nb_site.synchronize()
        else:
            logger.info("Synchronizing sites")
            for site in self.sites:
                nb_site = NbSite(site)
                nb_site.synchronize()

    def sync_organizations(self):
        organizations = self.komora_api.get_organizations()

        logger.info("Synchronizing organizations")
        for organization in organizations:
            nb_tenant = NbTenant(organization)
            nb_tenant.synchronize()

    def sync_devices(self):
        try:
            logger.info("Posting devices")
            post_devices = NbDevice.get_nb_devices_data()
            self.komora_api.post_devices(post_devices)
        except Exception as e:
            raise e

        try:
            devices = self.komora_api.get_devices()
        except Exception as e:
            raise e

        logger.info("Synchronizing devices")
        for dev in devices:
            nb_dev = NbDevice(dev)
            nb_dev.synchronize()

        # TODO: Make method
        # Get all komora_id from devices at Komora system
        komora_ids = [dev.id for dev in devices]

        pynetbox = NetboxConnection()
        pynetbox.open()

        # filter devices, which are not stored in KOMORA
        devices_not_in_komora = pynetbox.connection.dcim.devices.filter(
            cf_komora_id__n=komora_ids)

        # Unset komora link to those devices
        devs_to_update = []
        for dev in devices_not_in_komora:
            dev.custom_fields["komora_id"] = None
            dev.custom_fields["komora_url"] = None
            devs_to_update.append(dev)

        # Update netbox DB
        try:
            if pynetbox.connection.dcim.devices.update(devs_to_update):
                logger.info(f"Devices links to Komora successfully unset")
            else:
                logger.info(f"No device found for unsetting links to Komora")
        except Exception as e:
            raise e
