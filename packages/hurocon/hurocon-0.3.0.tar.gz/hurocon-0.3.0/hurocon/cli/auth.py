from getpass import getpass

import click
from huawei_lte_api.Client import Client

from .. import core
from .root import cli


@cli.group()
def auth():
    """ Router authentication """
    pass


@auth.command('login')
def auth_login():
    """ Safely configure all authentication related details for further interactions """
    print('Authentication Configurator\n')
    con_ip = input(
        '(leave empty to use "{}")\n'
        'Full address to router: '
        .format(core.LOCAL_CONFIG_DEFAULT['connection_address'])
    )
    uname = input('Username: ')
    passwd = getpass('Password: ')

    auth_cfg = core.AuthConfig()
    auth_cfg.username = uname
    auth_cfg.password = passwd
    auth_cfg.connection_address = con_ip if len(con_ip) > 0 else \
        core.LOCAL_CONFIG_DEFAULT['connection_address']

    auth_cfg.commit()

    print("\nAuthentication details successfully specified")


@auth.command('logout')
def auth_logout():
    """ Remove all authentication details """
    core.AuthConfig().reset()
    core.AuthConfig().commit()
    print("All authentication details removed")


@auth.command('test')
def auth_test_connection():
    """ Test connection to router with current auth details """
    try:
        with core.HRC_Connection() as router_con:
            Client(router_con)
    except Exception as e:
        msg = 'Auth failed, reason: "{}"'.format(e)
    else:
        msg = 'Successful Authentication'

    click.echo(msg)
