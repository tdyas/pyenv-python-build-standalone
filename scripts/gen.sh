#!/bin/sh

dir="$(dirname $0)"
if [ ! -d "${dir:=.}/.venv" ]; then
  python3.13 -m venv "${dir}/.venv"
  "${dir}/.venv/bin/pip" install -r "${dir}/requirements.txt"
fi

exec "${dir}/.venv/bin/python3" "${dir}/generate_defs.py" "$@"
