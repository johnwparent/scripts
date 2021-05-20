import os, sys
import yaml
import argparse

# Basically we want to inspect the repo, possibly certain folders only
# check if there's a difference in these direcs via git
# and if there is a new file, or renamed file, etc, we modify the wrapper
# in a corresponding fashion

class Manager(object):
    def __init__(self):
        super().__init__(self)


class WrapperGenerator(object):
    def __init__(self,conf, wrapper = None):
        super().__init__(self)
        self._load(conf)
        if wrapper:
            self.load_wrapper(wrapper)
    def _load(self, conf):
        with open(conf, "r+") as c:
            conf_obj = yaml.safe_load(c)

    def load_wrapper(self, wrapper_yaml):
        pass

    def compute_dir_diff(self):
        pass


    def generate(self):
        pass


def main():
    ar = argparse.ArgumentParser()
    ar.add_argument(
        "--wrapper",
        "-w",
        action="store",
        dest="wrapper_dir",
        required=True
    )
    ar.add_argument(
        "--name",
        "-n",
        required=True,
        dest="name",
        action="store"
    )
    ar.add_argument(
        "--working-dir",
        "-I",
        action="store",
        required=True,
        dest="i"
    )
    opts = ar.parse_args(sys.argv[1:])
    sys.path.append(opts.wrapper_dir)
    templ = "namespaces:\n    kwiver:\n      arrows:\n        core:\n          classes:\n            {}:\n"
    base_key = "files"
    base_dir = "arrows/serialize/json/{}.h"
    with open(os.path.join(opts.wrapper_dir,opts.name),'r+') as yml:
        yml_obj = yaml.safe_load(yml)
        for f in os.scandir(opts.i):
            if f.is_file():
                ext = os.path.splitext(f.name)[1]
                if ext == ".h":
                    name = os.path.splitext(f.name)[0]
                    new_dict = yaml.safe_load(templ.format(name))
                    yml_obj[base_key][base_dir.format(name)] = new_dict

        yaml.safe_dump(yml_obj,yml)





if __name__ == '__main__':
    main()