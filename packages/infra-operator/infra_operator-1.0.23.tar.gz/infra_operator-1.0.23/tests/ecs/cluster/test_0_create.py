import pytest
from infra_operator import cli
from infra_operator.utils import config as Config


@pytest.mark.order(0)
def test_ecs_create():
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/cluster.yaml",
        "create"
    ])
    cli.main(config)
    config = Config.parse_commandline_args([
        "-n",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/cluster.yaml",
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/cluster.update.yaml",
        "create"
    ])
    cli.main(config)
