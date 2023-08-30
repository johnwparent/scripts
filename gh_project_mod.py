import argparse
import json
import os
import pathlib
import requests
import sys



def get_project_token(project_name, token):
    header = {"Authorization": f"Bearer {token}"}
    url = "https://api.github.com/graphql"
    data = {"query": '{ organization(login: "SPACK") { projectV2(number: 7){ id } } }'}
    rsp = requests.post(url, json.dumps(data), headers=header)
    if rsp.ok:
        return rsp.json()["data"]["organization"]["projectV2"]["id"]
    raise RuntimeError(f"Request response: {rsp.status_code}, error: {rsp.text}")


def make_project_issues(files_to_mirror: "list[str]", token: str):
    header = {"Authorization": f"Bearer {token}"}
    url = "https://api.github.com/graphql"
    proj_token = get_project_token("SPACK", token)
    for file in files_to_mirror:
        data = {
            "query": f"mutation {{addProjectV2DraftIssue(input: {{projectId: \"PVT_kwDOAYWyWc4AUtNH\" title: \"{file}\" body: \"Module\"}}) {{projectItem {{id}}}}}}"
            }
        rsp = requests.post(url, json.dumps(data), headers=header)
        if not rsp.ok or "errors" in rsp.text:
            raise RuntimeError(f"invalid return: {rsp.text}")

def get_files(dir: pathlib.Path):
    root = dir.stem
    components = [x.name for x in dir.iterdir() if x.suffix == ".py"]
    return ["/".join([root, comp]) for comp in components]

def mirror(dir: pathlib.Path, token: str):
    files_to_mirror = get_files(dir)
    make_project_issues(files_to_mirror, token)

def main():
    args = argparse.ArgumentParser()
    args.add_argument(
        "-d",
        "--dir",
        action="store",
        type=pathlib.Path,
        dest="dir",
        help="directory to mirror files from"
    )
    args.add_argument(
        "--token",
        action="store",
        dest="token",
        help="path to file containing GH PAT"
    )
    nmspc = args.parse_args(sys.argv[1:])
    token = ''
    with open(nmspc.token, "r") as f:
        token = f.read().strip('\n')
    mirror(nmspc.dir, token)
if __name__ == "__main__":
    main()