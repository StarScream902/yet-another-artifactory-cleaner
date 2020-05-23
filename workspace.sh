#!/usr/bin/env sh

x=$1

if [[ -e venv/bin/activate ]]; then
  source venv/bin/activate
else
  python3 -m venv venv
  source venv/bin/activate
fi

case $x in
  "build")
    pip install -r ./requirements.txt
  ;;
  "run")
    python ./main.py
  ;;
esac
