#!/bin/bash
# Stops and deletes existing containers if they exist
incus stop dns-serv --force 2>/dev/null || true
incus stop dns-client --force 2>/dev/null || true
incus delete dns-serv --force 2>/dev/null || true
incus delete dns-client --force 2>/dev/null || true

# Removes the network if it already exists
incus network rm dns-infra 2>/dev/null || true

# Creates the network and containers
incus network create dns-infra network=UPLINK ipv4.address=192.168.47.1/24 ipv4.nat=true ipv6.address=none ipv6.nat=false
incus init images:ubuntu/jammy/cloud dns-client -t c2-m6 --network dns-infra -d eth0,ipv4.address=192.168.47.50 -d root,size=320GiB
incus init images:ubuntu/jammy/cloud dns-serv -t c2-m6 --network dns-infra -d eth0,ipv4.address=192.168.47.101 -d root,size=320GiB

# Starts the containers
echo "========== Starting VMs =========="
incus start dns-serv
incus start dns-client

# Wait for network to initialize
sleep 5

# Setup dns-serv
echo "========== Setting up dns-serv (DNS Server) =========="
incus exec dns-serv -- /bin/bash -c "apt update && sleep 5 && DEBIAN_FRONTEND=noninteractive apt-get install -y net-tools bind9 bind9utils bind9-doc dnsutils tshark"

# Ensure bind9 directories exist
incus exec dns-serv -- /bin/bash -c "mkdir -p /etc/bind/zones"

# Enable and start bind9
incus exec dns-serv -- systemctl enable --now bind9

# Setup dns-client
echo "========== Setting up dns-client (DNS Client) =========="
incus exec dns-client -- /bin/bash -c "apt update && sleep 5"
incus exec dns-client -- bash -c "useradd -m -s /bin/bash 'ansible'"
incus exec dns-client -- usermod -aG sudo ansible
incus exec dns-client -- bash -c "echo ansible:ansible | chpasswd"

# Install nslookup (dnsutils) and tshark
incus exec dns-client -- /bin/bash -c "DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils tshark net-tools"

# Allow ansible user to run tshark without root privileges
incus exec dns-client -- /bin/bash -c "usermod -aG wireshark ansible"

# Push DNS configuration files
echo "========== Configuring DNS on ntp-make =========="
incus file push ../named.conf.options dns-serv/etc/bind/named.conf.options
incus file push ../named.conf.local dns-serv/etc/bind/named.conf.local
incus file push ../research.net dns-serv/etc/bind/zones/research.net
incus file push ../research.net.rev dns-serv/etc/bind/zones/research.net.rev
incus file push ../resolv.conf dns-serv/etc/resolv.conf

# Restart bind9 to apply changes
incus exec dns-serv -- systemctl restart bind9
incus exec dns-serv -- systemctl status bind9 --no-pager

# Set resolv.conf on ntp-client
echo "========== Applying resolv.conf to ntp-make =========="
incus file push ../resolv.conf dns-client/etc/resolv.conf

# Add login messages
incus exec dns-serv -- /bin/bash -c 'echo "reset; echo YOU ARE LOGGED IN AS ROOT IN dns-serv" >> /root/.bashrc'
incus exec dns-client -- /bin/bash -c 'echo "reset; echo YOU ARE LOGGED IN AS ROOT IN dns-client" >> /root/.bashrc'

echo "========== Setup complete! =========="

