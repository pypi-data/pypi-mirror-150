import click
import requests
import json
from git import Repo
import os
import sys 
@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


@click.group()
def apis():
    """Welcome to CodeCommenter 📣"""


@apis.command()
def predict():
    """Run prediction"""
    click.echo("Use this function to run a prediction!")

@apis.command()
def commit():
    """Commit current diffs and have CodeCommenter comment the commit for you"""
    # Git add -A
    # Get current difs
    # Get preds
    # Commit
    repo = Repo(os.getcwd())
    print(repo)
    diff = repo.git.diff()
    # print(repo.git.diff())     
    resp = requests.post('https://yl4zicglte.execute-api.us-east-1.amazonaws.com/predict/commit', json={"prompt": diff}) 
    # Then commit those
    print(resp.status_code)
    # resp = resp.json()
    click.echo(resp.text)


def predict():
    """Run prediction"""
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str, hide_input=True)
    if authenticate_warrant(username=username, password=password):
        click.echo("Successfully authenticated with Spikit!")
    else:
        click.echo("Invalid username and password. Login")


def main():
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("CVE")
    apis(prog_name="c2")
