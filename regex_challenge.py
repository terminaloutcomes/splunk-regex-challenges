#!/usr/bin/env python3

""" James' Terrible implementation of a CLI for playing with regex challenges """

import json
from json.decoder import JSONDecodeError
import os
from pathlib import Path
import re
import sys
from typing import List, Optional

import click
from loguru import logger
from pydantic import BaseModel

class ChallengeFile(BaseModel):
    """ challenge file format """
    input: str
    matches: List[str] = []
    exclusions: List[str] = []
    groups: List[str] = []
    creator: Optional[str] = "Unknown regex master."
    example_solution: Optional[str]

    class Config:
        """ config """
        arbitrary_types_allowed = True

# {
#     "input" : "hello world",
#     "matches" : [
#         "hello"
#     ],
#     "groups" : [
#         "hello"
#     ],
#     "creator" : "@yaleman",
#     "example_solution" : "(^\\w+)"
# }

def load_challenge(file_object: click.File) -> ChallengeFile:
    """ loads a challenge file"""
    load_path = Path(file_object.name).expanduser().resolve()
    try:
        file_json = json.loads(load_path.open(encoding="utf-8").read())
        return ChallengeFile.parse_obj(file_json)
    except JSONDecodeError as json_error:
        logger.error(f"Failed to load {file_object.name}: {json_error}")
        sys.exit()

def display_challenge(filename: str, data: ChallengeFile) -> None:
    """ displays the challenge data """
    print(f"{filename} by {data.creator}")
    print("#"*50)
    print("Input: ")
    print("#"*50)
    print(data.input)
    print("#"*50)
    if data.matches:
        print("Expected Matches: ")
        print(data.matches)
        print("#"*50)
    print("#"*50)
    if data.exclusions:
        print("Things to exclude: ")
        print(data.exclusions)
        print("#"*50)
    if data.groups:
        print("Expected Groups: ")
        print(data.groups)
        print("#"*50)

class IncludedExclusions(Exception):
    """ raised when you included results that should have been excluded."""
class InvalidMatches(Exception):
    """ raised when you don't match the required matches """

#pylint: disable=too-many-branches
def run_pattern(
    challenge_data: ChallengeFile,
    pattern: re.Pattern,
    show_text: bool=True,
    ) -> bool:
    """ runs the pattern, returns bool if it succeeded or not """

    results = {
    }

    if challenge_data.matches:
        result = pattern.findall(challenge_data.input)
        if result is None or result != challenge_data.matches:
            raise InvalidMatches
    for exclusion in challenge_data.exclusions:
        if exclusion in result:
            logger.error("You matched {} which shouldn't be matched.", exclusion)
            raise IncludedExclusions(exclusion)
    if challenge_data.groups:
        results["groups"] = False
        search_result = pattern.search(challenge_data.input)

        if search_result is not None:
            result = list(search_result.groups())
            if show_text:
                print("Found groups:")
                print(result)
                print("#"*50)
            if result == challenge_data.groups:
                if show_text:
                    print("Success in groups!")
                results["groups"] = True
            elif show_text:
                print("Sorry, you didn't succeed in groups.")
                return False
        elif show_text:
            print("Sorry, you didn't succeed in groups.")
            return False
    return True

@click.group()
def cli() -> None:
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
def challenge(filename: click.File, regex: str) -> None:
    """ Test yourself! """
    pattern = compile_regex_or_quit(regex)
    challenge_data = load_challenge(filename)

    display_challenge(filename.name, challenge_data)

    run_pattern(challenge_data, pattern)

@cli.command()
@click.argument("filename",
    type=click.File(),
    )
def test(filename: click.File) -> None:
    """ tests a file """
    challenge_data = load_challenge(filename)

    logger.info(f"🔰 Testing {filename.name}")
    # fails: Dict[str, Any] = {}

    if not challenge_data.example_solution:
        logger.error("Couldn't find a solution in {}", filename.name)
        return

    logger.debug("   Found example solution:")
    logger.debug(challenge_data.example_solution)
    pattern = compile_regex_or_quit(challenge_data.example_solution)
    try:
        result = run_pattern(challenge_data, pattern, show_text=False)
    except InvalidMatches:
        logger.error("You didn't match the required strings.")
        result = False
    except IncludedExclusions:
        result = False

        # for result in results: #pylint: disable=consider-using-dict-items
        #     if not results[result]:
        #         logger.error(
        #             "[!] {} failed with example regex {}",
        #             result,
        #             challenge_data.example_solution,
        #             )
        #         if "failed_results" not in fails:
        #             fails["failed_results"] = []
        #         fails["failed_results"].append(result)

    if not result:
        logger.error("❌ {} FAILED!", filename.name)
        # logger.error(json.dumps(fails, indent=4, ensure_ascii=False))
        # sys.exit(1)
    else:
        logger.info("✅ {} passes tests!", filename.name)


@cli.command(name="list")
def list_challenges() -> None:
    """ lists challenge files """
    print("The following challenges exist:", file=sys.stderr)
    for filename in os.listdir("./challenges"):
        print(f"./challenges/{filename}")

if __name__ == '__main__':
    cli()
