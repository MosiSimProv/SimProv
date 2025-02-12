import json
from pathlib import Path

import pytest


@pytest.fixture()
def error_rules_path():
    path = Path(__file__) / "../resources/error-rules.py"
    return path.resolve()


@pytest.fixture()
def real_rules_path():
    path = Path(__file__) / "../resources/real-rules.py"
    return path.resolve()


@pytest.fixture()
def specs_path():
    path = Path(__file__) / "../resources/specs.yaml"
    return path.resolve()

@pytest.fixture()
def real_specs_path():
    path = Path(__file__) / "../resources/real-specs.yaml"
    return path.resolve()

@pytest.fixture()
def real_event():
    return {
        "type": "FileChange-Event",
        "file_path": "~/fooo/bar/bak/study/models/simulation-model.py"
    }


@pytest.fixture()
def demo_event():
    return {
        "type": "DEMO EVENT",
        "file_path": "~/fooo/bar/bak/study/models/simulation-model.py"
    }


@pytest.fixture()
def conflict_event():
    return {"type": "CONFLICT"}


@pytest.fixture()
def unknown_event():
    return {"type": "NOTHING"}


@pytest.fixture()
def complex_event():
    path = Path(__file__) / "../resources/complex-event.json"
    event_from_json = json.load(open(path.resolve()))
    return event_from_json
