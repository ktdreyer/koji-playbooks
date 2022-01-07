#!/bin/bash
set -eux

# Reset the Koji database to an empty state.
# Useful for starting over when applying large configurations.

systemctl stop httpd

sudo -u postgres psql -c 'DROP DATABASE IF EXISTS koji;'
sudo -u postgres psql -c 'DROP USER IF EXISTS koji;'
sudo -u postgres psql -c 'CREATE DATABASE koji;'
sudo -u postgres psql -c "CREATE USER koji WITH ENCRYPTED PASSWORD 'koji';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE koji TO koji;"

psql -q koji koji < /usr/share/doc/koji/docs/schema.sql

psql -U koji -c "INSERT INTO users (name, status, usertype) VALUES ('kdreyer', 0, 0);"
psql -U koji -c "INSERT INTO user_perms (user_id, perm_id, creator_id) VALUES (1, 1, 1);"

systemctl start httpd
