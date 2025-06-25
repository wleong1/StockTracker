FROM bitnami/pgbouncer:latest

USER root

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y postgresql-client

USER 1001

CMD ["pgbouncer", "/etc/pgbouncer/pgbouncer.ini"]