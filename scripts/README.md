# README

1. Create a `config.yml` in the path of this file with the following structure:

    ```YML
    OLTP:
    drivername: postgresql
    user: root
    password: root
    host: localhost
    port: 5432
    database_name: OLTP_PROJECT
    OLAP:
    drivername: postgresql
    user: root
    password: root
    host: localhost
    port: 5432
    database_name: OLAP_PROJECT
    ```

    > Chage the `database_name` for yours.

2. Create a virtual python environment: `python -m venv -venv`.

3. Activate the created python virtual environment.

    - Windows: `.\.venv\Scripts\Activate.ps1`.

    - Linux: `source ./.venv/bin/activate`.

4. Install the requirements: `pip install -r .\requirements.txt`.

5. Run the main script: `python ./main.py`.
