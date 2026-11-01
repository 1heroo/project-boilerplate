#!/usr/bin/env bash
# Generates every combination of the template options and checks each project:
# ruff, pytest, entry point imports, no leftovers of disabled modules, no unrendered Jinja.
# Usage: scripts/check_template.sh [workdir]   (needs uv and poetry)
set -u
TPL="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${1:-$(mktemp -d)}"
CC="uvx cookiecutter --no-input -f"

echo "workdir: $WORK"
$CC -o "$WORK/base" "$TPL" project_name=base >/dev/null
(cd "$WORK/base/base" && poetry install --no-root >/dev/null) || { echo 'poetry install failed'; exit 1; }
VENV="$WORK/base/base/.venv/bin"

fail=0
for k in true false; do for t in true false; do for m in true false; do for e in true false; do for a in true false; do
  slug="k${k:0:1}-t${t:0:1}-m${m:0:1}-e${e:0:1}-a${a:0:1}"
  if ! $CC -o "$WORK/m" "$TPL" project_name="$slug" use_kafka=$k use_taskiq=$t use_metrics=$m \
      include_example=$e include_admin_stub=$a >/dev/null 2>&1; then
    echo "$slug FAIL: generate"; fail=1; continue
  fi
  cd "$WORK/m/$slug" || exit 1
  errs=""
  "$VENV/ruff" check -q src tests >/dev/null 2>&1 || errs="$errs ruff"
  "$VENV/pytest" -q -p no:cacheprovider >/dev/null 2>&1 || errs="$errs pytest"
  mods="src.main"
  [ $k = true ] && mods="$mods,src.broker"
  [ $t = true ] && mods="$mods,src._taskiq,src._scheduler"
  [ $m = true ] && mods="$mods,src.metrics"
  "$VENV/python" -c "import importlib; [importlib.import_module(x) for x in '$mods'.split(',')]" >/dev/null 2>&1 \
    || errs="$errs import"
  "$VENV/python" -c "import json; json.load(open('src/config/logger/logging.json'))" 2>/dev/null || errs="$errs bad-json"
  [ $k = false ] && grep -rIqiE 'faststream|kafka' src pyproject.toml docker-compose.dev.yml Makefile configs && errs="$errs kafka-leftover"
  [ $t = false ] && grep -rIqiE 'taskiq|redis|ITaskQueue' src tests pyproject.toml docker-compose.dev.yml Makefile configs && errs="$errs taskiq-leftover"
  [ $m = false ] && grep -rIqiE 'prometheus|metrics_middleware' src pyproject.toml Makefile configs && errs="$errs metrics-leftover"
  [ $e = false ] && grep -rIqE '\bItem\b|items\.|/items' src tests && errs="$errs example-leftover"
  grep -rIqE '\{\{|\{%' . --exclude-dir=.venv && errs="$errs unrendered"
  if [ -n "$errs" ]; then echo "$slug FAIL:$errs"; fail=1; else echo "$slug ok"; fi
done; done; done; done; done
exit $fail
