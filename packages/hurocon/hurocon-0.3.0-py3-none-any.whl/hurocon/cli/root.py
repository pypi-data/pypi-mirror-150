import click

from .. import meta


@click.group()
@click.version_option(meta.version)
def cli():
    """ Command line interface for Huawei LTE routers """
