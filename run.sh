#!/usr/bin/env bash

echo "[Run] Start run script";


# Install project
chmod +x ./install.sh
./install.sh;

# Run project
cd API
uvicorn main:app --reload;


echo "[Run] Finished run script";

