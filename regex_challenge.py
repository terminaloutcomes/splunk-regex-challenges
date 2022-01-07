#!/usr/bin/env python3

""" James' Terrible implementation of a CLI for playing with regex challenges """

import json
from json.decoder import JSONDecodeError
import re
import os
import sys


import click
from loguru import logger

def load_challenge(file_object: click.File) -> dict:
    """ loads a challenge file"""
    try:
        return json.load(file_object)
    except JSONDecodeError as json_error:
        logger.error(f"Failed to load {file_object.name}: {json_error}")
    return {}


def display_challenge(filename: str, data: dict) -> None:
    """ displays the challenge data """
    print(f"{filename} by {data.get('creator', 'Unknown')}")
    print("#"*50)
    print("Input: ")
    print("#"*50)
    print(data.get("input"))
    print("#"*50)
    if data.get("matches"):
        print("Expected Matches: ")
        print(data.get("matches"))
        print("#"*50)
    if data.get("groups"):
        print("Expected Groups: ")
        print(data.get("groups"))
        print("#"*50)

#pylint: disable=too-many-branches
def run_pattern(challenge_data: dict, pattern: re.Pattern, show_text: bool=True):
    """ runs the patterns """

    results = {}

    if challenge_data.get("matches"):
        result = pattern.findall(challenge_data.get("input"))
        if result:
            results["matches"] = False
            if show_text:
                print("Found matches:")
                print(result)
                print("#"*50)
            if result == challenge_data.get("matches"):
                if show_text:
                    print("Success in matches!")
                results["matches"] = True
            elif show_text:
                print("Sorry, you didn't succeed.")
    if challenge_data.get("groups"):
        results["groups"] = False
        result = list(pattern.search(challenge_data.get("input")).groups())
        if result:
            if show_text:
                print("Found groups:")
                print(result)
                print("#"*50)
            if result == challenge_data.get("groups"):
                if show_text:
                    print("Success in groups!")
                results["groups"] = True
            elif show_text:
                print("Sorry, you didn't succeed in groups.")
        elif show_text:
            print("Sorry, you didn't succeed in groups.")
    return results

@click.group()
def cli():
    """ cli """

def compile_regex_or_quit(pattern: str) -> re.Pattern:
    """ compiles the regex """
    try:
        return re.compile(pattern)
    except re.error as re_error:
        logger.error(f"Failed to compile regex '{pattern}': {re_error}", file=sys.stderr)
        sys.exit(1)

@cli.command()
@click.argument("filename",
    type=click.File(),
    )
@click.argument("regex")
def challenge(filename: str, regex: str):
    """ Test yourself! """
    pattern = compile_regex_or_quit(regex)
    challenge_data = load_challenge(filename)

    display_challenge(filename.name, challenge_data)

    run_pattern(challenge_data, pattern)

@cli.command()
@click.argument("filename",
    type=click.File(),
    )
def test(filename: str):
    """ tests a file """
    challenge_data = load_challenge(filename)

    logger.info(f"🔰 Testing {filename.name}")
    fails = {}

    for field in ("input", "creator", "matches", "groups"):
        if not field in challenge_data:
            if "missing_fields" not in fails:
                fails["missing_fields"] = []
            fails["missing_fields"] = field

    if "example_solution" in challenge_data:
        logger.debug("   Found example solution")
        pattern = compile_regex_or_quit(challenge_data["example_solution"])
        results = run_pattern(challenge_data, pattern, show_text=False)
        for result in results: #pylint: disable=consider-using-dict-items
            if not results[result]:
                logger.error(f"[!] {result} failed with example regex {challenge_data['example_solution']}")
                if "failed_results" not in fails:
                    fails["failed_results"] = []
                fails["failed_results"].append(result)

    if fails:
        logger.error("❌ {} FAILED!", filename.name)
        logger.error(json.dumps(fails, indent=4, ensure_ascii=False))
        sys.exit(1)
    else:
        logger.info("✅ {} passes tests!", filename.name)


@cli.command(name="list")
def list_challenges():
    """ lists challenge files """
    print("The following challenges exist:")
    for filename in os.listdir("./challenges"):
        print(f"./challenges/{filename}")

if __name__ == '__main__':
    cli()
