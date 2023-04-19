# Webservices

This repo contains the code for the web services assignment for the course Distributed Systems (INFORMAT 1500WETDIS) at the University of Antwerp in the academic year of 2022-2023. The author is Thomas Gueutal (s0195095).

To skip to running the project, refer to [this section](#running-the-project).

The following major sections relate directly to the project's required features and deliverables:
* [Run the project](#running-the-project)
* [RESTful Design Considerations](#restful-design-considerations)
* [Documentation](#documentation)

Note that the role of the manual deliverable is filled by the [RESTful Design Considerations](#restful-design-considerations) section as wel as the [Documentation](#documentation) section.

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
</ol>

## Submission

Following project submission, a small 5-minute demo of the solution is scheduled per student.

The following are additional notes on project submission

<ul>
  <li>Make sure no files are missing</li>
  <li>Late submissions will automatically have points deducted for tardiness.</li>
  <li>Make sure that your submission has the following format and upload it via Blackboard! 
    <br><b>DS-Assignment1-Snumber-Lastname.zip</b>
  </li>
</ul>

# Running the project

<b>TL;DR</b>: Call the [run script](run.sh) from the project root to run both the frontend application and the backend API.

The following sections describe how to run the project on **linux**. It is not guaranteed to work on windows. Feel free to skip the [installation section](#intallation) and go straight to the [startup section](#startup) as the startup script runs the installation step automatically anyways. The installation section is only present for the sake of completeness.

## Intallation

Before running the API and web interface, the necessary project setup must be done. As python, [Flask](https://flask.palletsprojects.com/en/2.2.x/) and [Vue3](https://vuejs.org/guide/introduction.html) with [Vite](https://vitejs.dev/) as build took are used, this includes setting up the python virtual environment, installing all python dependencies and installing the node dependencies. This step can be completed by simply calling the [install script](install.sh) **from the project root**.

```sh
./install.sh
```


## Startup

To run the backend API and frontend application, simply call the [run script](run.sh) **from the project root**. This script considers the existence of a `venv/` folder in the project root to be proof the the installation having happened already. However, it should prompt the user to ask if reinstallation is desired anyways.

```sh
./run.sh
```

# RESTful Design Considerations

This section elaborates on the design considerations relating to the RESTfulness of the Webservices API, which functions as a TMDB aggregator/proxy.

Note that any mention of the *Webservices API* refers to the API we are required to write as part of the assignment; it refers to the API detailed in the assignment pdf.

For each resource and collection, the supported CRUD http methods are listed, since they provide additional insight into purpose of each resource and collection, though of course REST does not necessarily equate http.

## Movies Collection

The movies collection represents the collection of all Movie resources. Its implementation is warranted to adhere to the RESTful principle of "hackable up the tree". Its sole purpose is to be a parent/collection of single movie resources. In doing so, it allows the intuitive specification of the subject movie for following, more specialised resources.

The corresponding endpoint is `/api/movies/`. The CRUD http operations are supported as follows:

* ~~POST~~: Method Not Allowed
* GET: gets the list of all movies
* ~~PUT~~: Method Not Allowed
* ~~DELETE~~: Method Not Allowed

## Popular Movies Collection

The popular movies collection represents the collection of all popular Movie resources. It constitutes project requirement 1: get x popular movies. By treating the collection of popular movies as a resource in and of itself, we can avoid adding it as subfunctionality to the `/api/movies/` endpoint. This allows it to adhere to the RESTful principle of "hackable up the tree" and prevents unnecessary query parameters for `/api/movies/`.

The corresponding endpoint is `/api/movies/popular?amount=x`. The `amount` parameter purely facilitates the popularx functionality. The CRUD http operations are supported as follows:

* ~~POST~~: Method Not Allowed
* GET: gets the first x popular movies
* ~~PUT~~: Method Not Allowed
* ~~DELETE~~: Method Not Allowed

## Average Score Plot Resource

An average score plot resource represents a barplot of the average scores of the specified movies. The plot itself is transparently treated as a resource, though the corresponding backend queries the quickchart API.

The corresponding endpoint is `/api/movies/average-score-plot?ids=ids_csv` where `ids_csv` is a comma separated list of movie ids. The `ids` parameter purely facilitates the plotting functionality. The CRUD http operations are supported as follows:

* ~~POST~~: Method Not Allowed
* GET: gets the first x popular movies
* ~~PUT~~: Method Not Allowed
* ~~DELETE~~: Method Not Allowed

## Movie Resource

The Movie resource, which represents a single TMDB movie, is also not required by the project specification. Similarly to the movies collection, it organically enables access to more specialised resources, through a logical, hackable path.

The corresponding endpoint is `/api/movies/{mov_id}`. The CRUD http operations are supported as follows:

* ~~POST~~: Method Not Allowed
* GET: gets a barplot of the average scores of the specified movies
* ~~PUT~~: Method Not Allowed
* ~~DELETE~~: Method Not Allowed

## Likes Collection

The likes collection is just that, a collection of all Like resources. However, a single Like resource consits of a single status boolean. Thus, to make the likes collection as complete and simple as possible, it manifests as a list of the TMDB ids of all liked movies in the API response. It is the set of all TMDB movie ids that, at the moment of querying, are marked as `liked` in the API backend.

Similarly to the movies collection, the likes collection provides a hackable structure to further like/un-like functionality. It also makes for an easy way to verify the required like/un-like project functionality.

The corresponding endpoint is `/api/likes/`. The CRUD http operations are supported as follows:

* ~~POST~~: Method Not Allowed
* GET: gets the list of all movie ids currently marked as `liked`
* ~~PUT~~: Method Not Allowed
* ~~DELETE~~: Method Not Allowed

## Like Resource

The like resource represents a `(movie_id, liked)` pair, where `movie_id` is a TMDB movie id and `liked` a boolean denoting whether the movie is currently marked as liked.

The corresponding endpoint is `/api/likes/<int:mov_id>`. The CRUD http operations are supported as follows:

* ~~POST~~: Method Not Allowed
* GET: gets the `(movie_id, liked)` pair corresponding to the `mov_id` url parameter
* PUT: set the `liked` property of the `(movie_id, liked)` pair corresponding to `mov_id` to `true`
* DELETE: set the `liked` property of the `(movie_id, liked)` pair corresponding to `mov_id` to `false`

The reasoning behind supporting the PUT method and not the POST method is that this simple application does not make use of, or keeps track of _any_ users. This implies that the `liked` state of a movie, though it is a resource in the API implementation, acts like property of a movie that is shared between *all* consumers of the Webservices API. In that sense, it is more intuitive for this property to default to `false` for all movies and it being immediately open to updating with PUT, than for a like to first need to be created using POST.

Another possible implementation for the like functionality would have been the addition of a `/api/movies/<mov_id>/like` route. Such a format treats the `/like` postfix more like an action than a resource, making it practical but ultimately not quite RESTful. 

A last option would have been a `/api/movies/<mov_id>?like=t/f` style extension of the [movie resource](#movie-resource). But, this somewhat goes against the REST principles of "Few operations, many URI" in that it foregoes an extra URI in favor of including that functionality into an existing one and also goes against "Query arguments are only for parameters" as the like functionality is implementable without the parameter in this case. It can be argued that adding `?like=t/f` to the URL changes the resource that is being communicated with from a movie resource to a like resource. In the end, it comes down to the fact that the API implementation treats a like as a separate resource, because this makes the api more modular and extensible and because REST prefers resources over applications.

# Documentation

The description of the Webservices API structure, parameters and API use is provided in the form of autogenerated apispec documentation. This documentation is generated using the `flask-apispec` python module, and is available at the http://localhost:5000/api/swagger/ and http://localhost:5000/api/swagger-ui/ endpoints once the project is running successfully; it is available after completing the [run the project section](#running-the-project).

Alternatively, the in-code comments are also quite extensive and may serve as backup documentation.

# Encountered Technical Difficulties

This section documents any technical difficulties and implementational struggles I encountered while working on this assignment. It is purely for my own benefit and to ease future review of this project's code.

## HTTP vs HTTPS

Currently, the flask app doesn't seem to support the use of HTTPS. This is likely some or the other configuration error, but not of much consequence to the project. Just **remember to use HTTP for now** in all api requests, to be safe.

## Flask RESTful

View the flask-restful python package's latest documentation [here](https://flask-restful.readthedocs.io/en/latest/). These docs may differ from the used version, specified in the [`requirements.txt`](requirements.txt) file.

### reqparse module

The [reqparse module](https://flask-restful.readthedocs.io/en/latest/api.html#module-reqparse) offers [parsing of the request arguments](https://flask-restful.readthedocs.io/en/latest/quickstart.html#argument-parsing) amongst other things. The minimal code to use it follows:

```py
from flask_restful import reqparse
parser = reqparse.RequestParser()
args = parser.parse_args() # The request arguments
```

To add optional parameters that don't raise an exception due to absence, set the `required` flag.

```py
parser.add_argument("requiredArg", required=False,
    help="A required argument")
```

To specify which fields of the flask.Request the parser should search for the arguments, specify the `locations` argument.

```py
parser.add_argument("optionalQueryArg", location=('args',),
    help="An optional query string argument, found in flask.request.args")
```

Setting the `locations` argument solves the following error response:

```
{
    "message": "Did not attempt to load JSON data because the request Content-Type was not 'application/json'."
}
```

## Flask CORS

At first I tried to simply make the frontend work using the file protocol, e.g. `file://path/to/index.html`. Any fetches threw CORS errors however, so I decided to simply run a separate http server to provide the frontend application instead.

As a first attempt, I tried to utilize python3's SimpleHTTPServer module to run an https server, because calls over http failed for one reason or the other. The following python script was used in the attempt:

```py
from http.server import HTTPServer,SimpleHTTPRequestHandler
import ssl

httpd = HTTPServer(('localhost', 1443), SimpleHTTPRequestHandler)
# Since version 3.10: SSLContext without protocol argument is deprecated. 
# sslctx = ssl.SSLContext()
sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
sslctx.check_hostname = False # If set to True, only the hostname that matches the certificate will be accepted
sslctx.load_cert_chain(certfile='./generated/server.pem', keyfile="./generated/key.pem")
httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
```

The certificate used above was generated during the install script

```sh
# Generate ssl cert. for the simple https server to work
echo "[Install] Generate ssl certificate";
mkdir Web/generated
openssl req -new -x509 -keyout Web/generated/key.pem -out Web/generated/server.pem -days 365 -nodes  \
-subj "/C=BE/ST=Antwerpen/L=Antwerpen/O=UAntwerpen/OU=Student-DS/CN=Thomas-Gueutal/emailAddress=Thomas.Gueutal@student.uantwerpen.be" \
> /dev/null
```

However, this attempt was abandoned because the certificate was not signed by a trusted authority, making browsers like chrome flag and reject to visit the frontend pages.

Thus, I created a [vuejs](https://vuejs.org/guide/introduction.html) project based on vite, which provides a builtin development http server by default, to serve the frontend instead.

The frontend and backend api components are standalone, so without CORS enabled any frontend fetches to the backend fail. CORS is simply implemented using the flask-cors package in this project.

## Python Decorators

To elegantly handle unexpected exceptions and common input requirements, I chose to make use of decorators. These can be wrapped around the http methods to semi-explicitly describe the error-behavior of the relevant endpoints. Decorators that take parameters and still examine and pass down the wrapped function's parameters gave me some trouble, but the following links helped in finding the solution: [SO answer](https://stackoverflow.com/questions/5929107/decorators-with-parameters), [sitepoint article](https://www.sitepoint.com/understanding-python-decorators/)

# Secrets and Configuration

The configuration of the Flask app is done as conveniently as possible. All secrets are simply stored in the [configuration file](API/config.py). Safety precautions, such as an [instance directory](https://flask.palletsprojects.com/en/2.2.x/config/#instance-folders), are foregone in favor of simplicity.

# Accreditation

Any significant sources used in writing this project, that wouldn't be immediately obvious from reading its requirements, [dependencies](requirements.txt) and or source code, receive credit in this section.

## Version control

The `.gitignore` file was generated with [this website](https://www.toptal.com/developers/gitignore), which allows gitignore file generation based on used technologies, and then possibly adapted.

## TMDB

Though this dependency is already explicitly stated often, it bears mentioning that the [TMDB API terms of use](https://www.themoviedb.org/documentation/api/terms-of-use) requires any user or product to feature the TMDB logo and credit notice, as written in section `1.A.2` and the section "What are the attribution requirements?" [here](https://www.themoviedb.org/documentation/api). The frontend application satisfies this requirement by accrediting TMDB at the bottom of every page.