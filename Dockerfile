#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM debian:stable
MAINTAINER James Milner<james.milner@geovation.uk>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
# ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

#RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list
# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
# Add PostgreSQL's repository. It contains the most recent stable release
#     of PostgreSQL, ``9.5``.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get -y update
RUN apt-get -y install ca-certificates rpl pwgen

#-------------Application Specific Stuff ----------------------------------------------------

# We add postgis as well to prevent build errors (that we dont see on local builds)
# on docker hub e.g.
# The following packages have unmet dependencies:
# postgresql-9.3-postgis-2.1 : Depends: libgdal1h (>= 1.9.0) but it is not going to be installed
#                              Recommends: postgis but it is not going to be installed
RUN apt-get install -y postgresql-9.5-postgis-2.2 netcat

# Open port 5432 so linked containers can see them
EXPOSE 5432

# Run any additional tasks here that are too tedious to put in
# this dockerfile directly.
ADD postgis/setup.sh /postgis/setup.sh
RUN chmod 0755 postgis/setup.sh
RUN postgis/setup.sh

# We will run any commands in this when the container starts
ADD postgis/start-postgis.sh /postgis/start-postgis.sh
RUN chmod 0755 /postgis/start-postgis.sh

CMD /postgis/start-postgis.sh

### Tiler specific Code
ADD ./tiler/tiler-scripts /tiler-scripts
RUN chmod +x -R /tiler-scripts
RUN export DB_PORT=5432
RUN export DB_USER=docker
RUN export DB_DATABASE=data 
RUN export DB_PASSWORD=docker

### GDAL Specific Code
RUN apt-get install gdal-bin


# ADD . /usr/local/src/gdal-docker/
# RUN apt-get update -y && \
#     apt-get install -y make && \
#     make -C /usr/local/src/gdal-docker install clean && \
#     apt-get purge -y make

# # Externally accessible data is by default put in /data
# WORKDIR /data
# VOLUME ["/data"]

# # Execute the gdal utilities as nobody, not root
# USER nobody

# # Output version and capabilities by default.
# CMD gdalinfo --version && gdalinfo --formats && ogrinfo --formats