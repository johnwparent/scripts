import sys, os, distutils
import argparse
import cv2
import glob

def mult(ims):
    for im in ims:
        for x in range(50):
            ims.append(im.copy())

def rotate(ims):
    rot_range = ["-45","50"]
    pass

def bright(ims):
    bright_range = ["-50","100"]
    pass

def crop(ims):
    width_height_range = [90,70,90,70]
    pass

def flip(ims):
    flip_direction = "vertical"
    pass

im_types = [".jpg", ".png"]

def read_ims_in(direc, recursive=False):
    jpg_files = glob.glob(direc+"*"+im_types[0])
    png_files = glob.glob(direc+"*"+im_types[1])
    ims = []
    for pth in jpg_files:
        ims.append(cv2.imread(pth))
    for pth in png_files:
        ims.append(cv2.imread(pth))
    return ims

def write_ims_out(direc, ims):
    for im in ims:
        pth, ext = os.path.splitext(direc)
        cv2.imwrite(pth+hash(im)+ext,im)

def main():
    args = argparse.ArgumentParser()
    args.add(
        "--include-dir",
        "-I",
        dest="I",
        action="store",
        default=os.getcwd(),
        required=False,
    )
    args.add_argument(
        "--aug",
        "-a",
        dest="aug_type",
        action="append",
        default=["mult"],
        type=list,
        required=False,
        choices=["mult","bright","crop","rotate","flip"]
    )
    args.add_argument(
        "--output-dir",
        "-o",
        dest="output_dir",
        action="store",
        required=False,
        default=os.getcwd(),
    )
    args.add_argument(
        "--recursive",
        "-R",
        dest="recursive",
        action="store",
        required=False,
        default=False,
        type=lambda x: bool(distutils.util.strtobool(x))
    )
    opts = args.parse_args(sys.argv[1:])
    initial_ims = read_ims_in(opts.I, recursive=opts.recursive)
    for mut in opts.arg_type:
        new_ims = locals()[mut]

if __name__ == '__main__':
    main()