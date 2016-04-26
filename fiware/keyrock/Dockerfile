FROM fiware/idm
ADD https://github.com/kelseyhightower/confd/releases/download/v0.10.0/confd-0.10.0-linux-amd64 /usr/local/bin/confd
RUN chmod +x /usr/local/bin/confd
ADD confd /etc/confd/

ENV KEYSTONE_ADMIN_TOKEN=videona-admin
ENV KEYSTONE_ADMIN_PORT=35357
ENV KEYSTONE_PORT=7003
ENV KEYSTONE_TOKEN_EXPIRATION=7776000

ENV HORIZON_EMAIL_FROM=please-reply@videona.com
ENV HORIZON_EMAIL_URL=http://www.videona.com/
ENV HORIZON_EMAIL_SUBJECTPREFIX='[Videona]'
ENV HORIZON_EMAIL_LISTTYPE=blacklist
ENV HORIZON_EMAIL_HOST=smtp.videona.com
ENV HORIZON_EMAIL_PORT=25
ENV HORIZON_EMAIL_USER='email_username'
ENV HORIZON_EMAIL_PWD='email_pwd'

CMD /usr/local/bin/confd -onetime -backend env && sudo /keystone/tools/with_venv.sh /keystone/bin/keystone-all -v & sudo /horizon/tools/with_venv.sh python /horizon/manage.py runserver 0.0.0.0:8000