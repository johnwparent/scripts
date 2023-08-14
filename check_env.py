import argparse
import os
import subprocess
import sys

def call_test():
    return subprocess.call(["nmake", "/NOLOGO", "release", "/Fmakefile.vc"])

def process(file_name):
    with open(file_name, "r") as f:
        for line in f.readlines():
            env_var, val = line.split("=")
            print(f"trying: {env_var}:{val}")
            os.environ.pop(env_var)
            os.environ[env_var] = val
            ret = call_test()
            if ret == 0:
                print(f"Env var we need to set correctly: {env_var}")
                return


def main():
    a = argparse.ArgumentParser()
    a.add_argument(
        "file",
        action="store",
        help="env file to compare against active env"
    )
    nmspc = a.parse_args(sys.argv[1:])
    process(nmspc.file)

if __name__ == "__main__":
    main()