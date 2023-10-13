# Proton VPN Network Manager WireGuard

Adds the WireGuard protocol to the Proton VPN v4 application. This was put together quickly for fun, is unstable, and **should not be actually used**. WireGuard configurations generated during run-time are written to stdout and log file with the private key visible, so that is an even bigger reason to not use this. 

Relies on the unofficial [WireGuard NetworkManager plugin](https://github.com/max-moser/network-manager-wireguard); if you are receiving "Connection failed" errors in a connection retry loop, you will need to rebuild the plugin with [this patch](https://github.com/max-moser/network-manager-wireguard/issues/62#issuecomment-1500081392) (no need to copy it afterward; just `sudo make install`).