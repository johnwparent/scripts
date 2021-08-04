import os
import sys

rtf_header = """{{\\rtf1\\ansi\\deff0\\nouicompat
{{\\fonttbl{{\\f0\\fnil\\fcharset0 Courier New;}}}}
{{\\colortbl ;\\red0\\green0\\blue255;}}
{{\\*\\generator Riched20 10.0.19041}}\\viewkind4\\uc1
\\f0\\fs22\\lang1033
{}
}}
"""

def line_to_rtf(str):
    return str.replace("\n","\par")

def parse_license_to_rtf(file_path):
    contents = ""
    with open(file_path,"r+") as f:
        for line in f.readlines():
            contents+=line_to_rtf(line)
    return rtf_header.format(contents)

