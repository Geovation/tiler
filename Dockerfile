#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM debian:jessie
MAINTAINER James Milner<james.milner@geovation.uk>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
# USER root
#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
# ADD config/71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

#RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list
# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
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

# Run any additional tasks here that are too tedious to put in
# this dockerfile directly.
ADD postgis/setup.sh /postgis/setup.sh
RUN chmod 0755 postgis/setup.sh
RUN postgis/setup.sh

# We will run any commands in this when the container starts
ADD postgis/start-postgis.sh /postgis/start-postgis.sh
RUN chmod 0755 /postgis/start-postgis.sh

### GDAL Specific Code
RUN apt-get install gdal-bin

### Python
RUN apt-get install -y python-pip libpq-dev python-dev
RUN pip install psycopg2 geojson nose coverage shapely mapbox-vector-tile

### Tippecanoe! 
RUN apt-get -y install sudo git build-essential libsqlite3-dev zlib1g-dev \
    && cd / \
    && git clone https://github.com/mapbox/tippecanoe.git tippecanoe \
    && cd tippecanoe \
    #  && git checkout tags/$TIPPECANOE_RELEASE \
    && cd /tippecanoe \
    && make \
    && make install \
    && cd / \
 #   && rm -rf tippecanoe \

### Config
ENV DB_HOST localhost
ENV DB_PORT 5432
ENV DB_USER docker
ENV DB_NAME gis 
ENV DB_PASSWORD docker

# Open port 5432 so linked containers can see them
EXPOSE 5432

# # Run the database in the background
# RUN /postgis/start-postgis.sh

### Tiler 
ADD tiler.sh /bin/tiler 
RUN chmod 755 /bin/tiler
ENTRYPOINT ["tiler"]
