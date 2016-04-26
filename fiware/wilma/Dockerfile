FROM ging/fiware-pep-proxy
ADD https://github.com/kelseyhightower/confd/releases/download/v0.10.0/confd-0.10.0-linux-amd64 /usr/local/bin/confd
RUN chmod +x /usr/local/bin/confd

ADD certs /opt/certs
ENV CERT_FILE=/opt/certs/server.crt
ENV KEY_FILE=/opt/certs/server.key

ENV KEYSTONE_HOST=http://localhost
ENV KEYSTONE_PORT=7003
ENV APP_HOST=api.web
ENV APP_PORT=7002
ENV IDM_USER=idm_user
ENV IDM_PASSWORD=idm

ENV WILMA_HTTP_PORT=7010
ENV WILMA_HTTPS_PORT=7443
ENV WILMA_ACOUNT-HOST=http://auth.videona.com
ENV PUBLIC_PATH_1='/login'
ENV PUBLIC_PATH_2='/signup'

ADD confd /etc/confd/

#RUN /usr/local/bin/confd -onetime -backend env
CMD /usr/local/bin/confd -onetime -backend env && sudo node server.js