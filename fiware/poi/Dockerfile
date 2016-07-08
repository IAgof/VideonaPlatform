FROM ariokkon/fiware_poi_dataprovider

ADD etc/init.d/mongodb /etc/init.d/mongodb
RUN chmod +x /etc/init.d/mongodb

CMD service postgresql start && service mongodb start && /usr/sbin/apache2ctl -D FOREGROUND