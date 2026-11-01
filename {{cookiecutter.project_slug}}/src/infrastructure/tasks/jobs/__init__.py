"""Importing this package registers every task (and its schedule label) on the broker."""
{%- if cookiecutter.include_example %}
import src.infrastructure.tasks.jobs.items  # noqa: F401
{%- endif %}
