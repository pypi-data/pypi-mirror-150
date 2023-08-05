"""
Sprint-related functions.
"""

import os
import re
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jira import JIRA


def get_current_sprint():
    """
    Returns an object representating the current sprint.
    """

    load_dotenv()

    username = os.getenv("JIRA_USERNAME")
    password = os.getenv("JIRA_PASSWORD")
    project_prefix = os.getenv("PROJECT_PREFIX")
    project_name = os.getenv("PROJECT_NAME")

    jira = JIRA("https://tasks.opencraft.com", auth=(username, password))

    issues_in_current_sprint = jira.search_issues(
        f"project={project_name} AND SPRINT not in closedSprints() "
        "AND sprint not in futureSprints()"
    )

    # pylint: disable=C0209
    sprint_regex = r"{prefix}\.\d{{3}}".format(prefix=project_prefix)
    sprint_field = issues_in_current_sprint[0].fields.customfield_10005[0]
    sprint_string = re.findall(sprint_regex, sprint_field)[0]

    return Sprint(sprint_string)


def get_previous_sprint():
    """
    Returns an object representating the previous sprint.
    """

    current_sprint = get_current_sprint()
    return Sprint(
        f"{current_sprint.sprint_code}.{current_sprint.sprint_number - 1}"
    )


def get_next_sprint():
    """
    Returns an object representating the next sprint.
    """

    current_sprint = get_current_sprint()
    return Sprint(
        f"{current_sprint.sprint_code}.{current_sprint.sprint_number + 1}"
    )


class Sprint:
    """
    This class represents a two-week sprint.
    """

    def __init__(self, sprint_string):
        sprint_code, sprint_number = sprint_string.split(".")
        self.sprint_code = sprint_code
        self.sprint_number = int(sprint_number)

    @property
    def start_datetime(self):
        """
        Returns a datetime object repredenting the date when has sprint started
        or will start.
        """

        # I need this constants to know exactly what is
        # "thursday of second week of current sprint".
        sprint_239_number = 239
        sprint_239_start_datetime = datetime(
            year=2021,
            month=1,
            day=26,
            hour=0,
            minute=0,
            second=0,
            tzinfo=timezone.utc,
        )

        sprint_numbers_diff = self.sprint_number - sprint_239_number
        start_datetime = sprint_239_start_datetime + timedelta(
            days=sprint_numbers_diff * 14
        )

        return start_datetime

    @property
    def end_datetime(self):
        """
        Returns a datetime object repredenting the date when has sprint ended
        or will end.
        """

        days_in_sprint = 14
        return self.start_datetime + timedelta(days=days_in_sprint)

    def __repr__(self):
        return f"<Sprint {self.sprint_code}.{self.sprint_number}>"
