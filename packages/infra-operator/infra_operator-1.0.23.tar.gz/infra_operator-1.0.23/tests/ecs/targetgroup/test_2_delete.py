import pytest
from infra_operator import cli
from infra_operator.utils import config as Config


@pytest.mark.order(21000)
def test_tg_delete():
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/targetGroup.yaml",
        "delete"
    ])
    cli.main(config)
