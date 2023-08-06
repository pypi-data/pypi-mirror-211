import pytest
from infra_operator import cli
from infra_operator.utils import config as Config


@pytest.mark.order(21000)
def test_mesh_delete():
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/appmesh/infra-operator-tests-mesh/mesh.yaml",
        "delete"
    ])
    cli.main(config)
