FROM python:3.8.5-slim as build

RUN apt-get update && \
    apt-get -y install build-essential
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

FROM python:3.8.5-slim
COPY --from=build /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY run.py /app/
RUN adduser --gecos '' --disabled-password --shell /bin/false webhook \
 && chown -R webhook:webhook /app
USER webhook
WORKDIR /app
EXPOSE 5000
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "run:APP" ]

