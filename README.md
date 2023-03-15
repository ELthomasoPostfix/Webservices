# Introduction

This repo contains the code for the web services assignment for the course Distributed Systems (INFORMAT 1500WETDIS) at the University of Antwerp in the academic year of 2022-2023. The author is Thomas Gueutal (s0195095).

# Running the project

The following sections describe how to run the project on **linux**. It is not guaranteed to work on windows. Feel free to skip the [installation section](#intallation) as and go straight to the [startup section](#startup) as the startup script runs the installation step automatically anyways. The installation section is only present for the sake of completeness.

## Intallation

Before running the API and web interface, the necessary project setup must be done. This includes setting up the python virtual environment and installing all dependencies. This step can be completed by simply calling the installscript

```sh
./install.sh
```
in the project root.

## Startup

To run the API and web interface, simply call the run script

```sh
./run.sh
```

# Accreditation

Any significant sources used in writing this project, that wouldn't be immediately obvious from reading its requirements and or source code, receive credit in this section.

## Version control

The `.gitignore` file was taken, and then possibly adapted, from [this github repo](https://github.com/tiangolo/fastapi/blob/master/.gitignore), which provides a template file for the FastAPI api web framework.