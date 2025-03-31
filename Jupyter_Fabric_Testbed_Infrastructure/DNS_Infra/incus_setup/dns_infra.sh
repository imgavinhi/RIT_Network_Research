#!/bin/bash
# Stops and deletes existing containers if they exist
incus stop ntp-make --force 2>/dev/null || true
incus stop ntp-client --force 2>/dev/null || true
incus delete ntp-make --force 2>/dev/null || true
incus delete ntp-client --force 2>/dev/null || true

# Removes the network if it already exists
incus network rm dns-infra 2>/dev/null || true

# Creates the network and containers
incus network create dns-infra network=UPLINK ipv4.address=192.168.47.1/24 ipv4.nat=true ipv6.address=none ipv6.nat=false
incus init images:ubuntu/jammy/cloud ntp-client -t c2-m6 --network dns-infra -d eth0,ipv4.address=192.168.47.50 -d root,size=320GiB
incus init images:ubuntu/jammy/cloud ntp-make -t c2-m6 --network dns-infra -d eth0,ipv4.address=192.168.47.101 -d root,size=320GiB

# Starts the containers
echo "========== Starting VMs =========="
incus start ntp-make
incus start ntp-client

# Wait for network to initialize
sleep 5

# Setup ntp-make (DNS Server)
echo "========== Setting up ntp-client (DNS Server) =========="
incus exec ntp-make -- /bin/bash -c "apt update && sleep 5 && DEBIAN_FRONTEND=noninteractive apt-get install -y net-tools bind9 bind9utils bind9-doc dnsutils tshark"

# Ensure bind9 directories exist
incus exec ntp-make -- /bin/bash -c "mkdir -p /etc/bind/zones"

# Enable and start bind9
incus exec ntp-make -- systemctl enable --now bind9

# Setup ntp-client (DNS Client)
echo "========== Setting up ntp-make (DNS Client) =========="
incus exec ntp-client -- /bin/bash -c "apt update && sleep 5"
incus exec ntp-client -- bash -c "useradd -m -s /bin/bash 'ansible'"
incus exec ntp-client -- usermod -aG sudo ansible
incus exec ntp-client -- bash -c "echo ansible:ansible | chpasswd"

# Install nslookup (dnsutils) and tshark
incus exec ntp-client -- /bin/bash -c "DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils tshark net-tools"

# Allow ansible user to run tshark without root privileges
incus exec ntp-client -- /bin/bash -c "usermod -aG wireshark ansible"

# Push DNS configuration files
echo "========== Configuring DNS on ntp-make =========="
incus file push ../named.conf.options ntp-make/etc/bind/named.conf.options
incus file push ../named.conf.local ntp-make/etc/bind/named.conf.local
incus file push ../research.net ntp-make/etc/bind/zones/research.net
incus file push ../research.net.rev ntp-make/etc/bind/zones/research.net.rev
incus file push ../resolv.conf ntp-make/etc/resolv.conf

# Restart bind9 to apply changes
incus exec ntp-make -- systemctl restart bind9
incus exec ntp-make -- systemctl status bind9 --no-pager

# Set resolv.conf on ntp-client
echo "========== Applying resolv.conf to ntp-make =========="
incus file push ../resolv.conf ntp-client/etc/resolv.conf

# Add login messages
incus exec ntp-make -- /bin/bash -c 'echo "reset; echo YOU ARE LOGGED IN AS ROOT IN ntp-make" >> /root/.bashrc'
incus exec ntp-client -- /bin/bash -c 'echo "reset; echo YOU ARE LOGGED IN AS ROOT IN ntp-client" >> /root/.bashrc'

echo "========== Setup complete! =========="

