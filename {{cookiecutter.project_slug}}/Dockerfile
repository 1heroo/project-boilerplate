FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ={{ cookiecutter.timezone }}

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoints/dev/*.sh && chown -R nobody:nogroup /app
USER nobody

EXPOSE 8000{% if cookiecutter.use_metrics %} 8002{% endif %}{% if cookiecutter.use_taskiq %} 8003{% endif %}
