FROM python:3.11
ENV PYTHONUNBUFFERED=1
RUN sed -i 's/providers = provider_sect/providers = provider_sect\n\
ssl_conf = ssl_sect\n\
\n\
[ssl_sect]\n\
system_default = system_default_sect\n\
\n\
[system_default_sect]\n\
Options = UnsafeLegacyRenegotiation/' /etc/ssl/openssl.cnf
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./db-microservices/delete-ms /code/delete-ms
ENV PYTHONPATH=/code:${PYTHONPATH}
CMD python3.11 ./delete-ms/consume_delete.py
