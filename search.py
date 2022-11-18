import os
import pathlib
import subprocess
from dataclasses import dataclass

from fastapi import FastAPI, Query


class Conf:
    git: str = os.environ["X_GIT_DIR"].strip()


conf = Conf()
app = FastAPI()


@app.post("/search/update-git")
async def post():
    subprocess.run("git pull origin master".split(), shell=False, cwd=conf.git)


@dataclass
class Match:
    filepath: str
    value: str

    def json(self):
        return {
            "filepath": self.filepath,
            "value": self.value,
        }


def grep(directory: str, keywords: list[str]) -> list[Match]:
    if len(keywords) == 0:
        return []

    cmd = f"git grep {keywords[0]} '{directory}/*.md'"
    for i in range(1, len(keywords)):
        cmd = f"{cmd} | grep '{keywords[i]}'"
    cmd = f"{cmd} | uniq"

    try:
        p = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=1, cwd=conf.git
        )
        if p.stderr:
            print(p.stderr)
        assert p.returncode == 0, f"Existed with {p.returncode}"
        matches: list[Match] = []
        for line in p.stdout.strip().split("\n"):
            fs = line.split(":", 1)
            if len(fs) != 2:
                continue
            filepath, value = fs
            filepath = str(pathlib.Path(filepath).with_suffix(""))
            m = Match(filepath, value)
            matches.append(m)
        return matches

    except Exception as err:
        print(err)
        return []


@app.get("/search/grep")
async def get(q: list[str] = Query(default=[])):
    ds = [
        "aiura",
        "taglibro",
        "memo",
        "paper",
    ]
    return {directory: [m.json() for m in grep(directory, q)] for directory in ds}
