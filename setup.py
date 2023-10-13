#!/usr/bin/env python

from setuptools import setup, find_namespace_packages

setup(
    name="proton-vpn-network-manager-wireguard",
    version="0.0.1",
    description="Wireguard protocol for Proton VPN Linux",
    author="Weilbyte",
    author_email="me@weilbyte.dev",
    url="https://github.com/Weilbyte/python-proton-vpn-network-manager-wireguard",
    packages=find_namespace_packages(include=['proton.vpn.backend.linux.networkmanager.protocol.wireguard']),
    include_package_data=True,
    install_requires=["proton-core", "proton-vpn-network-manager"],
    extras_require={
        "development": ["wheel", "flake8", "pylint"]
    },
    entry_points={
        "proton_loader_linuxnetworkmanager": [
            "wireguard = proton.vpn.backend.linux.networkmanager.protocol.wireguard:WireGuard"
        ]
    },
    python_requires=">=3.8",
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
