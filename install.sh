#!/usr/bin/env bash

echo "[Install] Setup python virtual env";

# Setup venv
python3 -m venv venv;
. venv/bin/activate;

echo "[Install] Install dependencies";

# Install reqs
pip install -r requirements.txt;


echo "[Install] Finished installation script";
