## Setup development environment

`pip install -upgrade pip`

Create Virtual Environment:

`python -m venv venv`
`python3 -m venv --without-pip venv`

#### Activate previously created virtual environment

`source .venv/bin/activate` (Linux/macOS) 

or 

`.venv\Scripts\Activate.ps1` (Windows). 

You know the environment is activated when the command prompt shows **(.venv)** at the beginning.

#### Install required dependencies:

```
pip install -r /requirements/requirements.txt
pip install -r /requirements/requirements-test.txt
```

### Pre-commit

The package uses `pre-commit` to improve and ensure code quality. To install it, execute the following in your virtual
environment:

1. cd into the root of your GIT repository
2. `pip install pre-commit`
3. `pre-commit install`

This installs a git hook which runs pre-commit prior to committing anything to the GIT repository and **needs to be done
each time a repository gets cloned!**

If you want to do the pre-commit just in between, use the following command:

`pre-commit run --all-files`

### Testing

This package requires a working SQL Server for testing. In order to test against a docker image running an SQL Server,
run the following command:

```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=password!Password" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2017-latest
```

Then set the following env values to use it:

```bash
export SQL_PROTOCOL=mssql
export SQL_SERVER=localhost
export SQL_DB=master
export SQL_USER=sa
export SQL_PASS='password!Password'
export SQL_AUTHENTICATION=SqlPassword
```

In case you have issues connecting with the database due to the driver, make sure to set the following environment variable as well:

```bash
export ODBC_DRIVER = <driver name>
```

Where `<driver name>` is `SQL Server` on Windows and `ODBC Driver 17 for SQL Server` on Unix/MacOS.

----

### Generate the latest python package's version

---
**IMPORTANT NOTES:**

Before you start:
1. When regenerating the requirements files you **MUST** start from a freshly created virtual environment otherwise you might run into unwanted dependency issues.

2. Also make sure to base your virtual environment from the correct **python version**. This is especially important for
users already using python version 3.10... Dependencies should be calculated for python version 3.9.

3. DELETE the existing requirements.txt and requirements-test.txt files, otherwise dependencies will NOT be
updated! Be sure to re-add those files to GIT when you are done.
---

To generate the requirements files and even check version we need to install `pip-tools`:

```$bash
pip install pip-tools
```

Then run below commands to check changes:
```$bash
pip install pip-tools
cd requirements
pip-compile requirements.in
pip-compile --output-file requirements-test.txt requirements.in requirements-test.in
```


**IMPORTANT:**

Comment out the below package in **requirements.txt** and **requirements-test.txt**
as it is specific to windows:
```$bash
    #pywin32==303
    # via portalocker
```


