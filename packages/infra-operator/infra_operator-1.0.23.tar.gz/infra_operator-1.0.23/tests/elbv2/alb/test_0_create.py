import pytest
from infra_operator import cli
from infra_operator.utils import config as Config


@pytest.mark.order(100)
def test_alb_create():
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/alb.yaml",
        "create"
    ])
    cli.main(config)
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/alb.update.yaml",
        "create"
    ])
    cli.main(config)
