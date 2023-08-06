import pytest
from infra_operator import cli
from infra_operator.utils import config as Config


@pytest.mark.order(20000)
def test_role_delete():
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/exec.role.yaml",
        "delete"
    ])
    cli.main(config)
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/task.role.yaml",
        "delete"
    ])
    cli.main(config)
