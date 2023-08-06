import pytest
from infra_operator import cli
from infra_operator.utils import config as Config


@pytest.mark.order(0)
def test_ec2_create():
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ec2/infra-operator-tests/instance.yaml",
        "create"
    ])
    cli.main(config)
    # config = Config.parse_commandline_args([
    #     "-t",
    #     "aws/mainsite/dev/ap-northeast-1/ec2/infra-operator-tests/instance.update.yaml",
    #     "create"
    # ])
    # cli.main(config)
