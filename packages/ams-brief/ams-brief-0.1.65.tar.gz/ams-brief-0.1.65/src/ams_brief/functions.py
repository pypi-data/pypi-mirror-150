from datetime import date
from pathlib import Path


def get_project_number(projectpath: Path) -> str:
    return projectpath.stem[3:7]


def get_client_and_project(projectpath: Path) -> str:
    return projectpath.stem[8:15]


def get_date() -> str:
    return date.today().strftime('%Y%m%d')
