import os
from os import path
from time import sleep
import docker


def _get_postgres_docker_data_path():
    if 'LOCALIZATION_API_POSTGRES_DOCKER_DATA_PATH' not in os.environ:
        raise Exception("LOCALIZATION_API_POSTGRES_DOCKER_DATA_PATH needs to be set in os envs!")
    postgres_docker_data_path = os.getenv('LOCALIZATION_API_POSTGRES_DOCKER_DATA_PATH')
    if not path.exists(postgres_docker_data_path) or not path.isdir(postgres_docker_data_path):
        raise Exception("LOCALIZATION_API_POSTGRES_DOCKER_DATA_PATH does not exists or is not a directory!")
    return postgres_docker_data_path


def _create_postgres_docker_container(client, name, postgres_password):
    docker_container = client.containers.run("postgres:13.0", environment={
            'POSTGRES_PASSWORD': postgres_password,
            'PGDATA': '/var/lib/postgresql/data'
        },
        name=name,
        ports={'5432': '5432'},
        volumes={_get_postgres_docker_data_path(): {'bind': '/var/lib/postgresql/data', 'mode': 'rw'}},
        remove=True,
        detach=True
    )
    postgres_is_running = False
    while not postgres_is_running:
        print('Waiting for docker postgres to start...')
        logs = docker_container.logs().decode('utf-8')
        if 'database system is ready to accept connections' in logs:
            postgres_is_running = True
        sleep(3)
    return docker_container


def get_postgres_docker_container(postgres_password):
    name = 'localizationapi-postgres'
    client = docker.from_env()
    if name in map(lambda c: c.name, client.containers.list()) and client.containers.get(name).status == 'running':
        return client.containers.get(name)
    return _create_postgres_docker_container(client, name, postgres_password)
