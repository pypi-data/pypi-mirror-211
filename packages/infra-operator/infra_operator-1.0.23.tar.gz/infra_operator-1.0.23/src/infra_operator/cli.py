# fmt: off
from copy import deepcopy
import os
import glob

from infra_operator.utils.mod import ensure_path

pkg_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.insert(0, pkg_dir)
import json
import oyaml as yaml
from infra_operator.utils import config as Config
from infra_operator.utils.load import load as yaml_load
from infra_operator.utils.dump import dump as yaml_dump
import infra_operator.layout.mod as layout
from infra_operator.diff.mod import diff, obj_to_yaml
from infra_operator.operators.mod import dict_replace_mapping, remove_fields, render_str
from infra_operator.preprocess.mod import build_reverse_ref_map, expand_expression, get_variables, parse_expression, preprocess, preprocess_file, resolve_ref_and_operators
from infra_operator.read.mod import get_arn_from_resource, get_name, get_resource
from infra_operator.export.mod import export, export_ref
from infra_operator.create.mod import create
from infra_operator.update.mod import update
from infra_operator.validate.mod import validate
from infra_operator.delete.mod import delete
from infra_operator.plugins.wea_notify import release_notify_wea

# fmt: on


def render_wrap(kind, content, info, filename):
    info["kind"] = content["kind"]
    info["ctrl"] = content["apiVersion"].split(".")[0]
    _, _, info["filename"] = render_str(os.path.basename(filename), info)
    destination_filename = layout.format_2(info)
    ensure_path(destination_filename)
    yaml_dump(content, open(destination_filename, "w"))
    return (filename, destination_filename, kind, content)


def apply_wrap(kind, content, info, current, filename):
    if content.get("pipelineConfig", {}).get("no-apply"):
        print(f"this file does not allow apply.\n{filename}")
        return

    if current and current.get('status') not in ['INACTIVE', 'DRAINING']:
        before = export(kind, current, info)
        res = update_wrap(kind, content, info, current, filename)

        if ("TaskDefinition" in kind):
            account_name = "-".join([info.get('project', ''),
                                    info.get('env', '')])
            release_notify_wea(info.get('name'), {},
                               account_name, info.get('ecs_cluster'))

        after_resource = get_resource(content, kind, info)
        after = export(kind, after_resource, info)
        diff_wrap(kind, before, info, after, filename)
        return res
    else:
        return create_wrap(kind, content, info)


def create_wrap(kind, content, info):
    name = get_name(content, kind, info)
    print("not exists {}, {}, {}".format(kind, info.get('region'), name))
    print(f"creating...")
    res = create(kind, content, info)
    print("✅ created")
    return res


def update_wrap(kind, content, info, current, line):
    arn = get_arn_from_resource(current)
    name = get_name(content, kind, info)
    print("exists {}, {}, {}".format(kind, info.get('region'), name))
    print(arn)
    print("updating...")
    res = update(kind, content, info, current, line)
    print("✅ updated")
    return res


def delete_wrap(kind, content, info, current):
    arn = get_arn_from_resource(current)
    name = get_name(content, kind, info)
    print("exists {}, {}, {}".format(kind, info.get('region'), name))
    print(arn)
    print("deleting...")
    res = delete(kind, content, info, current)
    print("✅ deleted")
    return res


def diff_wrap(kind, before, info, after, line):
    name = get_name(before, kind, info)
    drop_fields = ["ETag"]
    for field in drop_fields:
        if field in before:
            del before[field]
        if field in after:
            del after[field]
    diffs = diff(after, before)
    print(line)
    if len(diffs):
        print("<details><summary>See Changes</summary>")
        print()
        print("```diff")
        sys.stdout.writelines(diffs)
        print("```")
        print("</details>")
    else:
        print("⚪ no changes: {}, {}, {}".format(kind, info.get('region'),
                                                name))
    return diffs


def validate_wrap(kind, content, info):
    name = get_name(content, kind, info)
    print("validating {}, {}, {} ...".format(
        kind, info.get("organization", info.get("region")), name))
    res = validate(kind, content, info)
    print("✅ validated")
    return res


def output_wrap(folder, expr_str, refed_files):
    print(f"output {expr_str}")
    expr = parse_expression(folder, expr_str)
    result = expand_expression(expr, refed_files)
    print("✅ outputed")
    return result


def export_wrap(kind, current, info, line):
    name = get_name(current, kind, info)
    print("exporting {}, {}, {} ...".format(
        kind, info.get("organization", info.get("region")), name))
    current = export(kind, current, info)
    if Config.config.write:
        os.makedirs(os.path.dirname(line), exist_ok=True)
        with open(line, "w") as f:
            yaml_dump(current, f)
        print(f"✅ exported: {line}")
    return current


def get_relative_path(filename, line):
    return os.path.join(os.path.relpath(os.path.dirname(filename), os.path.dirname(
        os.path.dirname(line))), os.path.basename(filename))


def export_ref_recursive(all_refs, id_to_filename, kind, current, info, root_filename, write_file=True, depth=100):
    info = deepcopy(info)
    refs, root = export_ref(kind, current, info)
    if depth < 1:
        return root
    for id, v in refs.items():
        if id not in all_refs:
            kind, content, info = v
            new_root_id_to_filename = {}
            current = get_resource(content, kind, info)
            name = get_name({"metadata": current}, kind, {})
            refed_filename = info.get("refed_filename")
            if name:
                refed_filename = name
            info["name"] = refed_filename
            info["filename"] = f"{refed_filename}.yaml"
            filename = layout.format(info, root_filename)
            ref_str = info.get("ref_template", "$file({})").format(
                get_relative_path(filename, root_filename))
            id_to_filename[id] = ref_str
            all_refs[id] = ref_str
            export_ref_recursive(all_refs, new_root_id_to_filename,
                                 kind, current, info, filename, write_file, depth-1)
        else:
            id_to_filename[id] = all_refs[id]
    root = dict_replace_mapping(root, id_to_filename)
    if write_file:
        os.makedirs(os.path.dirname(root_filename), exist_ok=True)
        with open(root_filename, "w") as f:
            yaml_dump(root, f)
            print(f"✅ exported: {root_filename}")
    return root


def export_ref_wrap(kind, current, info, line):
    name = get_name(current, kind, info)
    print("exporting {}, {}, {} ...".format(
        kind, info.get("organization", info.get("region")), name))

    all_refs = {}
    id_to_filename = {}
    root = export_ref_recursive(
        all_refs, id_to_filename, kind, current, info, line, True, 100)
    return root


def add_to_extra(ref_files):
    with open(".extra-files", "a") as f:
        f.writelines(ref_files)
        f.write("\n")
    return ref_files


def ref_hook(kind, refed_by):
    switch = {
        "TaskDefinition": [
            lambda args: list(
                filter(lambda one: one.endswith("service.yaml"), args)),
            add_to_extra
        ]
    }
    if kind not in switch:
        return
    steps = switch[kind]
    args = refed_by
    print(
        f"trigger file refed me: {json.dumps(refed_by, default=str, indent=4)}"
    )
    for step in steps:
        args = step(args)


def get_resource_by_file(filename):
    folder = os.path.dirname(filename)
    wait_for_ref = False
    kind, info, content = preprocess_file(filename, True, wait_for_ref)
    current = get_resource(content, kind, info)
    return current


emojis = {"create": "🏗️ ",
          "delete": "🗑️ ",
          "validate": "🔍",
          "export": "🖨️ ",
          "export-ref": "🖨️ ",
          "diff": "📝",
          }


def validate_args(filename, values):
    return preprocess_file(filename, values.get("input", {}), enable_ref_file=True, wait_for_ref=False)


def output_refed_files(folder, values, values_filename):
    refed_files = {}
    for key, val in values["output"].items():
        expr = parse_expression(folder, val)
        if expr["func"] == "FileReference":
            refed_files[expr["file"]] = None
    for filename, _ in refed_files.items():
        kind, current, info, _ = export_args(filename, values, values_filename)
        refed_files[filename] = current
    return refed_files


def render_args(filename, values, values_filename):
    values = yaml_load(values_filename, True)
    kind, info, content = preprocess_file(
        filename, values, enable_ref_file=False, wait_for_ref=True)
    return kind, content, values, filename


def create_args(filename, values, values_filename):
    values_folder = os.path.dirname(values_filename)
    input_variables = resolve_ref_and_operators(
        values_folder, values.get("input", {}))
    kind, info, content = preprocess_file(
        filename, input_variables, enable_ref_file=True, wait_for_ref=True)
    current = get_resource(content, kind, info)
    return kind, content, info, current, filename


def export_args(filename, values, values_filename):
    values_folder = os.path.dirname(values_filename)
    input_variables = resolve_ref_and_operators(
        values_folder, values.get("input", {}))
    kind, info, content = preprocess_file(
        filename, input_variables, enable_ref_file=True, wait_for_ref=False)
    current = get_resource(content, kind, info)
    if not current:
        raise Exception(
            f"could not found resources corresponding to {filename}")
    return kind, current, info, filename


def export_ref_args(filename, values, values_file):
    kind, info, content = preprocess_file(
        filename, values.get("input", {}), enable_ref_file=True, wait_for_ref=False)
    current = get_resource(content, kind, info)
    if not current:
        raise Exception(
            f"could not found resources corresponding to {filename}")
    return kind, current, info, filename


def diff_args(filename, values):
    folder = os.path.dirname(filename)
    kind, info, content = preprocess_file(
        filename, values.get("input", {}), enable_ref_file=True, wait_for_ref=False)
    current = get_resource(content, kind, info)
    current_expanded = {}
    if current:
        all_refs = {}
        id_to_filename = {}
        current_crd = export_ref_recursive(
            all_refs, id_to_filename, kind, current, info, filename, False, 1)
        _, _, current_expanded = preprocess(
            current_crd, info, folder, enable_ref_file=True, wait_for_ref=False)
    return kind, current_expanded, info, content,  filename


def delete_args(filename, values, vlaues_file):
    kind, info, content = preprocess_file(
        filename, values.get("input", {}), enable_ref_file=True, wait_for_ref=False)
    current = get_resource(content, kind, info)
    if current:  # 存在, 删除
        need_diff = False
        return kind, content, info, current
    else:  # 不存在，反馈
        print("❌ not exists {}, {}, {}".format(kind, info['region'],
                                               info['name']))


def for_each_file(template_path, args_func, func, values, values_file):
    if os.path.isdir(template_path):
        for extension in ["**/*.yaml", "**/*.yml"]:
            glob_expr = os.path.join(template_path, extension)
            for filename in glob.glob(glob_expr, recursive=True):
                if filename != values_file:
                    args = args_func(filename, values, values_file or "")
                    func(*args)
    elif os.path.isfile(template_path):
        args = args_func(template_path, values, values_file or "")
        return func(*args)
    else:
        raise Exception(f"could not found {template_path}")


def for_each_output(template_path, refed_files_func, func, values, values_file):
    if not values.get("output"):
        raise Exception(
            f"values must provide the `output` field to generate output.")
    output = {}
    folder = os.path.dirname(values_file)
    refed_files = refed_files_func(folder, values, values_file)
    for key, val in values["output"].items():
        output[key] = func(folder, val, refed_files)
    output_filename = values_file.replace(
        ".yml", ".output.yml").replace(".yaml", ".output.yaml")
    with open(output_filename, "w") as f:
        yaml_dump(output, f)
    return output


def main(args):
    # global config
    config = args
    action = config.action
    template_path = config.template
    values_file = config.values
    switch = {
        "validate": (validate_wrap, validate_args, for_each_file),
        "output": (output_wrap, output_refed_files, for_each_output),
        "create": (apply_wrap, create_args, for_each_file),
        "render": (render_wrap, render_args, for_each_file),
        "export": (export_wrap, export_args, for_each_file),
        "export-ref": (export_ref_wrap, export_ref_args, for_each_file),
        "diff": (diff_wrap, diff_args, for_each_file),
        "delete": (delete_wrap, delete_args, for_each_file),
    }
    func, args_func, for_files = switch[action]
    if values_file and not os.path.isfile(values_file):
        raise Exception(f"could not found {values_file}")
    values = yaml_load(values_file) or {}
    return for_files(template_path, args_func, func, values, values_file)


if __name__ == "__main__":
    Config.parse_commandline_args()
    main(Config.config)
