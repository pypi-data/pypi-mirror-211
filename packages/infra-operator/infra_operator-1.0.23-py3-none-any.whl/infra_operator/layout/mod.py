#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import json
import oyaml as yaml

from infra_operator.utils.load import load as yaml_load


def load_layout(filename):
    abspath = os.path.realpath(filename)
    cwd = os.getcwd()
    folder = os.path.dirname(abspath)
    while True:
        layout_path = os.path.join(folder, "layout.yaml")
        if os.path.exists(layout_path):
            return yaml_load(layout_path)
        if folder == cwd or folder == "/":
            break
        folder = os.path.dirname(folder)


def parse(filename, recursive=False):
    layouts = load_layout(filename)["layouts"]
    segments = filename.strip().replace("/.trash/", "/").split(os.sep)
    for layout in layouts:
        seg_defs = layout["path"].split("/")
        if len(seg_defs) == len(segments) or "<recursive>" in seg_defs:
            matched = True
            info = {}
            for i, seg_def, seg in zip(range(len(segments)), seg_defs, segments):
                if seg_def == "<recursive>" and recursive:
                    return parse("/".join(segments[i:]))
                result = re.match("\$\{([^\s\}]+)\}", seg_def)
                if result:
                    name = result.groups()[0]
                    info[name] = seg
                else:
                    if seg_def == seg:
                        continue
                    else:
                        matched = False
                        break
            for key, val in layout["require"].items():
                if info.get(key) != val:
                    matched = False
                    break
            if matched:
                return info
    raise Exception(f"failed to match any layout with filename: {filename}")


def replace(seg_def, info):
    result = re.match("\$\{([^\s\}]+)\}", seg_def)
    if result:
        name = result.groups()[0]
        return info[name]
    else:
        return seg_def


def format_2(info):
    layouts = load_layout(os.path.join(os.getcwd(), "layout.yaml"))["layouts"]
    for layout in layouts:
        matched = True
        seg_defs = layout["path"].split("/")
        for key, val in layout["require"].items():
            if info.get(key) != val:
                matched = False
                break
        if matched:
            pathes = [replace(seg_def, info) for seg_def in seg_defs]
            path = "/".join(pathes)
            return path
    raise Exception(f"didn't find matched layout for info: {info}")


def format(info, root_filename):
    layouts = load_layout(root_filename)["layouts"]
    for layout in layouts:
        matched = True
        seg_defs = layout["path"].split("/")
        for seg_def in seg_defs:
            result = re.match("\$\{([^\s\}]+)\}", seg_def)
            if result:
                name = result.groups()[0]
                if name not in info:
                    matched = False
                    break
        for key, val in layout["require"].items():
            if info.get(key) != val:
                matched = False
                break
        if matched:
            pathes = [replace(seg_def, info) for seg_def in seg_defs]
            path = "/".join(pathes)
            return path
    raise Exception(f"didn't find matched layout for info: {info}")


def main():
    files = [parse(line) for line in sys.stdin]
    res = json.dumps(files)
    print(res)


if __name__ == "__main__":
    main()
