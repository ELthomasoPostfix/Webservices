# Webservices

This repo contains the code for the web services assignment for the course Distributed Systems (INFORMAT 1500WETDIS) at the University of Antwerp in the academic year of 2022-2023. The author is Thomas Gueutal (s0195095).

# Project Specification

The goal of this project is to develop a RESTful API that acts as an aggregator for [the TMDB API](https://developers.themoviedb.org/3) and also adds some additional functionality, such as [plotting movie scores via another API](https://quickchart.io/documentation/). We must also provide a minimal web interface to test this API.

This section repeats the project requirements. This serves the double purpose of A) to thoroughly document the project and to allow in-code references to these requirements and deliverables and B) ensure I properly read and undestand the assignment.

The required features are:
<ol>
  <li>List the first x popular movies</li>
  <li>Given a movie, get the movies with exactly matching genres.</li>
  <li>Given a movie, get the movies with a similar runtime. (max 10 min diff)</li>
  <li>Given a movie, get the movies with overlapping first two actor(s)</li>
  <li>Given a set of movies, generate a barplot of average movie score</li>
  <li>’delete’ a movie: exclude movie from the API results, until API restart</li>
  <li>’like’ and ’un-like’ a movie</li>
</ol>

The minimally required deliverables for a passing grade are:
<ol>
  <li>Easy or automatic running of the web service and user interface, e.g. via a <b>run.sh</b> script</li>
  <li>Include an API manual with endpoint arguments, return value and description</li>
  <li>Include a design consideration section in the manual</li>
  <li>Include a used libraries section in the manual and make the project dependencies easily obtainable by
    <ol>
      <li>adding their source to the project</li>
      <li>providing an up-to-date <b>requirements.txt</b> file</li>
    </ol>
  </li>
  <li>Provide the API keys with the project source, with enough remaining quota to test the submitted solution</li>
  <li>Additional notes: make sure no files are missing</li>
</ol>

# Running the project

The following sections describe how to run the project on **linux**. It is not guaranteed to work on windows. Feel free to skip the [installation section](#intallation) and go straight to the [startup section](#startup) as the startup script runs the installation step automatically anyways. The installation section is only present for the sake of completeness.

## Intallation

Before running the API and web interface, the necessary project setup must be done. As python and [Flask](https://flask.palletsprojects.com/en/2.2.x/) are used, this includes setting up the python virtual environment and installing all dependencies. This step can be completed by simply calling the install script **in the project root**.

```sh
./install.sh
```


## Startup

To run the API and web interface, simply call the run script **in the project root**. This script considers the existence of a `venv/` folder in the project root to be proof the the installation having happened already. However, it should prompt the user to ask if reinstallation is desired anyways.

```sh
./run.sh
```

# Accreditation

Any significant sources used in writing this project, that wouldn't be immediately obvious from reading its requirements and or source code, receive credit in this section.

## Version control

The `.gitignore` file was generated with [this website](https://www.toptal.com/developers/gitignore), which allows gitignore file generation based on used technologies, and then possibly adapted.