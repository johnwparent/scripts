import sys
import os

def get_name(file):
    return os.path.basename(os.path.split(file)[0])


def run_git(*args):
    return os.popen("git {}".format(" ".join(args))).read()


def get_modified_files():
    return run_git("diff", "--name-only").split('\n')


def git_add(file):
    run_git("add", file)


def git_commit(msg):
    run_git("commit", "-m{}".format(msg))


if __name__ == '__main__':
    for file in get_modified_files():
        f_name = get_name(file)
        commit_msg = '"update {name}"'.format(name=f_name)
        git_add(file)
        git_commit(commit_msg)
        