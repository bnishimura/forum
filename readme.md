# Introduction
This is a generic forum made to exercise and deepen my django knowledge.
Secrets are hidden using the decouple package.

## Known negative traits
* User creation does not require emails so bots could nuke the server
> This choice was based on the fact that confirming emails can pose as a barrier for peers trying to use the project.

* No static files
> It is pretty ugly without any CSS and JS, but that has never been the focus.

* DB is SQLite
> Also arbitrary. This is a dummy project and there is no intent to make it scale so SQLite is good enough.

# Requirements
* Python 3.10
* Gunicorn 20.1.0
* Python-decouple 
