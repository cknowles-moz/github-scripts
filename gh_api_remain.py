#!/usr/bin/env python
"""
Check remaining API calls, and time of next reset
"""

from datetime import datetime

from github3 import login

from github_scripts import utils


def parse_args():
    """
    Parse the args - need either the username adn token, or the config to exist
    return the parsed args.
    """
    parser = utils.GH_ArgParser(
        description="Print out the remaining API limits, and the time of the reset"
    )
    args = parser.parse_args()
    return args


def get_limits(gh_sess, type_of_limit):
    """
    Return the search limit and the date for refresh
    :param: gh_sess - an initialized Github session
    :param: type_of_limit - string, either 'core' or 'search'
    Return [limitremaining(int), date(timestamp)]
    """
    if type_of_limit not in ["core", "search"]:
        raise Exception("Type of rate must be 'core' or 'search'")
    rates = gh_sess.rate_limit()["resources"][type_of_limit]
    return [rates["remaining"], rates["reset"]]


def main():
    """
    Check the remaining rate for the user, printing out the levels, as well as time of next reset
    """
    args = parse_args()
    gh_sess = login(token=args.token)
    api_limit, api_timestamp = get_limits(gh_sess, "core")
    refreshtime = datetime.fromtimestamp(api_timestamp)
    print(f"Remaining limits: {api_limit}, which will reset at {refreshtime}")
    search_limit, search_timestamp = get_limits(gh_sess, "search")
    refreshtime = datetime.fromtimestamp(search_timestamp)
    print(f"Remaining search limits: {search_limit}, which will reset at {refreshtime}")


if __name__ == "__main__":
    main()
