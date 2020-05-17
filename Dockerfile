FROM eddi16/alpython

RUN apk add --update-cache curl

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./Speedtest /app/Speedtest
COPY ./main.py /app/main.py
RUN pip3 install -r requirements.txt

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.9/supercronic-linux-arm \
    SUPERCRONIC=supercronic-linux-arm \
    SUPERCRONIC_SHA1SUM=47481c3341bc3a1ae91a728e0cc63c8e6d3791ad

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

 CMD ["supercronic", "./speedtest.cron"]