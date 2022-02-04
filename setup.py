#!/usr/bin/env python

from setuptools import setup, find_namespace_packages

setup(
    name="python-protonvpn-network-manager-openvpn",
    version="0.0.0",
    description="Proton Technologies VPN connector for linux",
    author="Proton Technologies",
    author_email="contact@protonmail.com",
    url="https://github.com/ProtonVPN/pyhon-protonvpn-network-manager-openvpn",
    packages=find_namespace_packages(include=['proton.vpn.backend.linux.networkmanager.protocol.openvpn']),
    include_package_data=True,
    install_requires=["proton-core"],
    entry_points={
        "proton_loader_nm_protocol": [
            "openvpn_tcp = proton.vpn.backend.linux.networkmanager.protocol.openvpn:OpenVPNTCP",
            "openvpn_udp = proton.vpn.backend.linux.networkmanager.protocol.openvpn:OpenVPNUDP",
        ]
    },
    license="GPLv3",
    platforms="OS Independent",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Security",
    ]
)
