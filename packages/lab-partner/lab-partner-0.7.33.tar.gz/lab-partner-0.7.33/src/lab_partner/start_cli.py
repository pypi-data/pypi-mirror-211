#!/usr/bin/env python

import logging
import shlex
import os
import click
import sys
from .docker import (
    DockerDaemonInfo,
    RootlessDockerContainer,
    DockerRunBuilder,
    UnixUser
)


logging.basicConfig(level=logging.INFO)


if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


DISPLAY = os.environ['DISPLAY']
WORKSPACE = os.environ['LAB_WORKSPACE']
WORKSPACE_DATA = os.path.join(WORKSPACE, 'data')
NETWORK_NAME = 'lab'
ROOTLESS_DOCKER_NAME = 'lab-rootless-docker'


def version():
    return metadata.version('lab-partner')


def is_supported_platform() -> bool:
    """
    Check current platform is MacOS or Linux
    :return: True on MacOS or Linux
    """
    return sys.platform in ('darwin', 'linux')


@click.command()
def start_cli():
    cli_env = {}
    docker_daemon_info = DockerDaemonInfo.build()
    rootless = RootlessDockerContainer(ROOTLESS_DOCKER_NAME, docker_daemon_info)
    if not docker_daemon_info.is_rootless():
        rootless.start_rootless_container(WORKSPACE, NETWORK_NAME)
        cli_env['DOCKER_HOST'] = 'tcp://localhost:2375'

    user_info = UnixUser()
    cli_cmd = DockerRunBuilder(f'enclarify/lab-partner-cli:{version()}')
    cli_cmd.options() \
        .with_tty() \
        .with_env('DOCKER_HOST', f'tcp://{ROOTLESS_DOCKER_NAME}:2375') \
        .with_env('ENVIRONMENT', 'LOCAL') \
        .with_env('HOST_DOCKER_SOCKET', docker_daemon_info.docker_internal_socket()) \
        .with_env('LAB_WORKSPACE', os.environ.get('LAB_WORKSPACE')) \
        .with_env('LAB_WORKSPACE', WORKSPACE) \
        .with_env('LAB_WORKSPACE_DATA', WORKSPACE_DATA) \
        .with_env('LAB_NETWORK_NAME', NETWORK_NAME) \
        .with_env('LAB_VERSION', version()) \
        .with_bind_mount(user_info.home_subdir('.gitconfig'), '/opt/lab/home/.gitconfig') \
        .with_bind_mount(user_info.home_subdir('.vim'), '/opt/lab/home/.vim') \
        .with_bind_mount(user_info.home_subdir('.vimrc'), '/opt/lab/home/.vimrc') \
        .with_bind_mount(user_info.home_subdir('.aws'), '/opt/lab/home/.aws') \
        .with_bind_mount(user_info.home_subdir('.ssh'), '/opt/lab/home/.ssh') \
        .with_bind_mount(WORKSPACE, WORKSPACE) \
        .with_bind_mount(docker_daemon_info.docker_socket(), '/var/run/docker.sock', False) \
        .with_workdir(WORKSPACE)

    cmd = shlex.split(cli_cmd.build())
    os.execvpe(cmd[0], cmd, cli_env)


if __name__ == '__main__':
    start_cli()
