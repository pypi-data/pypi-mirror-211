# save this as app.py
import os
from flask import Flask
from flask import request
from infra_operator.diff.mod import diff, obj_to_yaml
from infra_operator.operators.mod import dict_replace_mapping, remove_fields
from infra_operator.preprocess.mod import build_reverse_ref_map, get_variables, preprocess, preprocess_file
from infra_operator.read.mod import get_arn_from_resource, get_name, get_resource
from infra_operator.export.mod import export, export_ref
from infra_operator.create.mod import create
from infra_operator.update.mod import update
from infra_operator.validate.mod import validate
from infra_operator.delete.mod import delete
app = Flask("infra-operator-server")
UPLOAD_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

{
    "variables": {
        "Creator": "XXX",
        "CommitId": "xxxxx"
    },
    "apply_files": [
        {
            "filename": "aws/mainsite/dev/ap-northeast-1/ecs/tk-dev-ecs-cluster/desmond-debug/alb.yaml",
            "content": "xxxxx"
        }
    ],
    "all_files": [
        {
            "filename": "aws/mainsite/dev/ap-northeast-1/ecs/tk-dev-ecs-cluster/desmond-debug/alb.yaml",
            "content": "xxxxx"
        }
    ]
}

# read from git, given git commit hash
# read from s3. contains all the files
# upload a zip contains all files
# post contains all file content


def apply(file, variables):
    pass


def setup_folder(variables, files):
    for file in files:
        filename = UPLOAD_FOLDER


@app.post("/aws/apply")
def apply():
    body = request.get_json()
    variables = body.get("variables", {})
    files = body["files"]
    setup_folder(variables, files)
    for file in files:
        apply(file, variables)


if __name__ == "__main__":
    app.run(debug=True)
