#!/usr/bin/env python3

""" James' Terrible implementation of a CLI for playing with regex challenges """

import json
from json.decoder import JSONDecodeError
import re

import sys
import click


def display_challenge(filename: str, data: dict) -> None:
    """ displays the challenge data """
    print(f"{filename} by {data.get('creator', 'Unknown')}")
    print("#"*50)
    print("Input: ")
    print("#"*50)
    print(data.get("input"))
    print("#"*50)

    print("Expected Matches: ")
    print("#"*50)
    print(data.get("matches"))
    print("#"*50)

def parse_challenge(filepath: str, regex: re.Pattern):
    """ do the parsing things"""
    # with open(f"./challenges/{filename}", encoding="utf8") as file_handle:
    try:
        challenge_data = json.load(filepath)

    except JSONDecodeError as json_error:
        print(f"Failed to load {filepath}: {json_error}")
    display_challenge(filepath.name, challenge_data)

    if challenge_data.get("matches"):
        result = regex.findall(challenge_data.get("input"))
        if result:
            print("Found matches:")
            print(result)
            print("#"*50)
        if result != challenge_data.get("matches"):
            print("Sorry, you didn't succeed.")
        else:
            print("Success!")
    if challenge_data.get("groups"):
        result = regex.groups(challenge_data.get("input"))
        if result:
            print("Found groups:")
            print(result)
            print("#"*50)
        if result != challenge_data.get("groups"):
            print("Sorry, you didn't succeed.")


    # print(json.dumps(challenge, indent=4, ensure_ascii=False))

@click.group()
def cli():
    """ cli """

@cli.command()
@click.argument("filename",
    type=click.File(),
    )
@click.argument("regex")
def challenge(regex: str, filename: str):
    """ cli for the challenge parser"""

    try:
        pattern = re.compile(regex)
    except re.error as re_error:
        print(f"Failed to compile regex '{regex}': {re_error}", file=sys.stderr)
        sys.exit(1)


    parse_challenge(filename, pattern)

if __name__ == '__main__':
    cli()
