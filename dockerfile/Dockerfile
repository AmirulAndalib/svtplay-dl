# using edge to get ffmpeg-4.x
FROM alpine:latest
LABEL maintainer="j@i19.se"

COPY dist/*.whl .

RUN set -xe \
    && apk add --no-cache \
	    ca-certificates \
	    python3 \
        py3-pip \
        py3-cryptography \
        ffmpeg \
    && python3 -m pip install --break-system-packages *.whl \
    && rm -f *.whl

WORKDIR /data

ENTRYPOINT ["python3", "/usr/bin/svtplay-dl"]
CMD ["--help"]
