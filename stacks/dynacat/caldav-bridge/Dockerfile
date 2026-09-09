FROM python:3.13.14-alpine3.23

WORKDIR /app
RUN apk add --no-cache tzdata
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY bridge.py /app/bridge.py

USER 65532:65532

CMD ["python", "-u", "/app/bridge.py"]
