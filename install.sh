#!/usr/bin/env bash

echo "[Install] Start installation script";


# Setup venv
python3 -m venv venv;
. venv/bin/activate;

# Install reqs
pip install -r requirements.txt;


echo "[Install] Finished installation script";
