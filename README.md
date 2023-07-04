# case-cointop

## Installation

Create a virtualenv using your prefered venv manager, then run `pdm install`

Note, you can simply run pdm install if you have a default python interpreter >= 3.10

Before starting the server copy the `.env.example` to `.env` and replace the
`<YOUR_API_KEY>` by your coinapi key.

Once all the packages have been installed make the migrations with

```shell
pdm run manage.py migrate
```

And finally start the application with

```shell
pdm run server
```

Then you can go to `http://127.0.0.1:8000` and play with it

### Manage Users

User management is only available to superusers.

To create a new superuser, run the following command:

```shell
pdm run manage.py createsuperuser
```

And follow the steps


## Install Cronjobs

To install the pre-configured cronjobs, run
```shell
pdm run manage.py crontab add
```
