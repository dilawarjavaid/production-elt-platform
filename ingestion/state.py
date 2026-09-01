import hashlib
import json
from pathlib import Path


STATE_FILE = Path("data/.ingestion_state.json")


def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def load_state():
    if not STATE_FILE.exists():
        return {}

    with open(STATE_FILE, "r") as file:
        return json.load(file)


def save_state(state):
    STATE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(STATE_FILE, "w") as file:
        json.dump(
            state,
            file,
            indent=4
        )


def already_processed(dataset_name, file_hash):
    state = load_state()

    previous_hash = state.get(dataset_name)

    return previous_hash == file_hash


def mark_processed(dataset_name, file_hash):
    state = load_state()

    state[dataset_name] = file_hash

    save_state(state)