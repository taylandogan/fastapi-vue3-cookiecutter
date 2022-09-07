# fastapi-vue3-cookiecutter
A cookiecutter template that generates a fastapi-vue3 project.
Optionally you might add a PostgreSQL or a Redis database.

### How to use it

Go to the directory where you want to create your project and run:

```bash
pip install cookiecutter
cookiecutter https://github.com/taylandogan/fastapi-vue3-cookiecutter
```

### Generate passwords

You will be asked to provide passwords and secret keys for several components. Open another terminal and run:

```bash
openssl rand -hex 32
```


### Input variables

The input variables, with their default values (some auto generated) are:

* `project_name`: The name of the project
* `project_slug`: The development friendly name of the project. By default, based on the project name
* `secret_key`: Backend server secret key. Use the method above to generate it.