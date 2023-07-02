# case-cointop

## Installation

Create a virtualenv using your prefered venv manager, then run `pdm install`

Note, you can simply run pdm install if you have a default python interpreter >= 3.10

Once all the packages have been installed start the application by using

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
