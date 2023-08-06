from infra_operator import cli
from infra_operator.utils import config as Config


def test_sm_create():
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/sm.yaml",
        "create"
    ])
    cli.main(config)
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/sm.update.yaml",
        "create"
    ])
    cli.main(config)
