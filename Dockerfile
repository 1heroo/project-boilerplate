FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Asia/Bishkek

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoints/dev/*.sh && chown -R nobody:nogroup /app
USER nobody

EXPOSE 8000 8002 8003
