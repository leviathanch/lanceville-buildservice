# Lanceville ASIC buildservice
This web application is the build service of my company.
We run it on AWS and help you easily designing ASICs with a few clicks and no manual labour.

## Deployment
* Everytime you change something related to styles you have to run "./manage.py collectstatic" in order to make sure, that it's being rendered correctly.
* You also need a PostGresSQL database server
* All passwords are stored in a file called "secrets.py" which is not managed in GIT

## Requirements
* django-simple-menu
* django-recaptcha
* django-registration-redux
