import pytest
from infra_operator import cli
from infra_operator.utils import config as Config


@pytest.mark.order(21000)
def test_ecs_delete():
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/cluster.yaml",
        "delete"
    ])
    cli.main(config)
