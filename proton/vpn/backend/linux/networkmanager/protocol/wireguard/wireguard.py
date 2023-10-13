from concurrent.futures import Future
import os

from getpass import getuser

from proton.vpn import logging
from proton.vpn.backend.linux.networkmanager.core.nmclient import NM
from proton.vpn.backend.linux.networkmanager.core import LinuxNetworkManager
from proton.vpn.connection.vpnconfiguration import VPNConfiguration

logger = logging.getLogger(__name__)

class WireGuard(LinuxNetworkManager):
    """Base class for the backends implementing the WireGuard protocol."""
    virtual_device_name = "proton0"
    protocol = "wireguard"
    connection = None
    _use_certificate = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__vpn_settings = None
        self.__connection_settings = None
        logger.warning("UNOFFICIAL/COMMUNTIY MODULE!")
        logger.warning("This module is community-made and not officially provided by Proton, and as such, might interfere with the intended behavior of the application.")
        if not self._wireguard_plugin_present(): # Prevent loader from seeing module in such cases?
            logger.critical("Missing NetworkManager wireguard plugin. This will cause NotImplementedError.")

    def _wireguard_plugin_present(self) -> bool:
        vpn_plugin_list = NM.VpnPluginInfo.list_load()
        if any(plugin.props.name == 'wireguard' for plugin in vpn_plugin_list):
            return True
        return False

    def _configure_connection(self, vpnconfig):
        """Configure imported vpn connection.

            :param vpnconfig: vpn configuration object.
            :type vpnconfig: VPNConfiguration

        It also uses vpnserver, vpncredentials and settings for the following reasons:
            - vpnserver is used to fetch domain, servername (optional)
            - vpncredentials is used to fetch username/password for non-certificate
              based connections
            - settings is used to fetch dns settings
        """
        self.connection = self._import_vpn_config(vpnconfig)

        self.__vpn_settings = self.connection.get_setting_vpn()
        self.__connection_settings = self.connection.get_setting_connection()

        self._unique_id = self.__connection_settings.get_uuid()

        self.__make_vpn_user_owned()
        self.__configure_dns()
        self.__set_custom_connection_id()


    def __make_vpn_user_owned(self):
        # returns NM.SettingConnection
        # https://lazka.github.io/pgi-docs/NM-1.0/classes/SettingConnection.html#NM.SettingConnection

        self.__connection_settings.add_permission(
            "user",
            getuser(),
            None
        )

    def __configure_dns(self):
        """Apply dns configurations to ProtonVPN connection."""

        ipv4_config = self.connection.get_setting_ip4_config()
        ipv6_config = self.connection.get_setting_ip6_config()

        ipv4_config.props.dns_priority = -1500
        ipv6_config.props.dns_priority = -1500

        try:
            if len(self._settings.dns_custom_ips) == 0:
                return
        except AttributeError:
            return

        ipv4_config.props.ignore_auto_dns = True
        ipv6_config.props.ignore_auto_dns = True

        ipv4_config.props.dns = self._settings.dns_custom_ips

    def __set_custom_connection_id(self):
        self.__connection_settings.props.id = self._get_servername()

    def _setup(self) -> Future:
        vpnconfig = VPNConfiguration.from_factory(self.protocol)
        self._vpnserver.wg_public_key_x25519 = self._vpnserver.x25519pk # "Workaround" -> AttributeError: 'VPNServer' object has no attribute 'wg_public_key_x25519'
        vpnconfig = vpnconfig(self._vpnserver, self._vpncredentials, self._settings)
        vpnconfig.use_certificate = self._use_certificate

        self._configure_connection(vpnconfig)
        return self.nm_client.add_connection_async(self.connection)
    
    @classmethod
    def _get_priority(cls):
        return 2

    @classmethod
    def _validate(cls):
        return True