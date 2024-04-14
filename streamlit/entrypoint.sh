#!/bin/bash
mkdir /temp_data
chown -R postgres:postgres /temp_data
apt-get update
apt-get install -y nfs-common
python3 src/flask_endpoints.py
