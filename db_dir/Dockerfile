FROM postgres

# Install dependencies
RUN apt-get update
RUN apt-get install -y nfs-common
RUN apt-get install rpcbind

# Copy the shell script into the image
COPY db_init.sh /docker-entrypoint-initdb.d/init-user-db.sh
