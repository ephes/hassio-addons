ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh /
COPY sensors.py
COPY split_sensor_messages.py /
RUN chmod a+x /run.sh

# Install python + requirements
RUN \
    apk add --no-cache \
        bash \
        python3 \
    \
    && pip3 install \
        paho-mqtt

CMD [ "/run.sh" ]
