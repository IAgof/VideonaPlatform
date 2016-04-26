FROM python:2.7-onbuild

COPY dev_requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r dev_requirements.txt

ENTRYPOINT ["py.test"]