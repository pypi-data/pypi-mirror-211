import pytest
from infra_operator import cli
from infra_operator.utils.load import load as yaml_load
from infra_operator.utils import config as Config


@pytest.mark.order(10000)
def test_appmesh_export():
    config = Config.parse_commandline_args([
        "-w",
        "n",
        "-t",
        "aws/mainsite/dev/ap-northeast-1/appmesh/infra-operator-tests-mesh/mesh.yaml",
        "export"
    ])
    result = cli.main(config)
    expected = yaml_load(
        "aws/mainsite/dev/ap-northeast-1/appmesh/infra-operator-tests-mesh/mesh.exported.yaml")
    assert result == expected
