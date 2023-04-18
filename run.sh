#!/usr/bin/env bash

# Variables
PY_VENV_PATH='venv/';
SKIP_INSTALL='n';

echo "[Run] Install project";

if [ -d "$PY_VENV_PATH" ]
then
  echo "The venv/ directory already exists at project root. Skip the install step? (y/n)";
  read SKIP_INSTALL;
fi

if [ "$SKIP_INSTALL" = 'n' ]
then
  # Install project
  chmod +x ./install.sh;
  ./install.sh;
fi

echo "[Run] Start frontend application";

# Run API consumer
cd Webservices-consumer;
npm run dev &
cd ..;


echo "[Run] Start web server";

# Run project
flask --app API --debug run;


echo "[Run] Finished run script";

