import pytest
from infra_operator import cli
from infra_operator.preprocess.mod import preprocess_file
from infra_operator.utils.load import load as yaml_load
from infra_operator.utils import config as Config


@pytest.mark.order(10000)
def test_role_export():
    config = Config.parse_commandline_args([
        "-w",
        "n",
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/exec.role.yaml",
        "export"
    ])
    result = cli.main(config)
    expected = yaml_load(
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/exec.role.exported.yaml")
    assert result == expected
    config = Config.parse_commandline_args([
        "-w",
        "n",
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/task.role.yaml",
        "export"
    ])
    result = cli.main(config)
    expected = yaml_load(
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/task.role.exported.yaml")
    assert result == expected
