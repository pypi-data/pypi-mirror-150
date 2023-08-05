import click
from huawei_lte_api.Client import Client

from .. import core
from .root import cli


@cli.group()
def sms():
    """ SMS commands """
    pass


@sms.command('send')
@click.option('-n', '--number', default='', help='Number that message will be sent to')
@click.option('-t', '--text', default='', help='Text of the message to be sent')
def sms_send(number: str, text: str):
    if len(number) == 0:
        number = input('Number: ')
    if len(text) == 0:
        text = input('Text: ')

    try:
        with core.HRC_Connection() as router_con:
            send_status = Client(router_con).sms.send_sms(
                [number],
                text
            )

        if send_status.lower() == 'ok':
            click.echo('SMS sent successfully to {}'.format(number))
        else:
            click.echo('SMS was not sent, reason: "{}"'.format(send_status))
    except Exception as e:
        click.echo('Execution failed, reason: "{}"'.format(e))
