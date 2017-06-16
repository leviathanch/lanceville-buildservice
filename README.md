# Lanceville ASIC buildservice
This web application is the build service of my company.
We run it on AWS and help you easily designing ASICs with a few clicks and no manual labour.

## Deployment
* Everytime you change something related to styles you have to run "./manage.py collectstatic" in order to make sure, that it's being rendered correctly.
* Always run "./manage.py migrate --run-syncdb" after pulling
* You also need a PostGresSQL database server
* All passwords are stored in a file called "secrets.py" which is not managed in GIT

## Requirements
* django-simple-menu
* django-recaptcha
* django-registration-redux
* django-allauth
* django-betterforms
* django-tinymce
* django-formtools
* django-cms
* django-treebeard
* treebeard
* django-multisite
* django-suit
* django-tables2
* django-crispy-forms
* django-utils
* sshpubkeys
