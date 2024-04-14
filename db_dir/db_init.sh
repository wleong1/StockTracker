#!/bin/bash

# Creates an empty stocks database
psql -U postgres -c "CREATE DATABASE stocks;"

# Restore the data into the stocks database
pg_restore -U postgres -d stocks /nfs/db.dump
