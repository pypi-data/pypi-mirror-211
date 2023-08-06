import time
import pytest
from infra_operator import cli
from infra_operator.utils import config as Config


@pytest.mark.order(21000)
def test_ec2_delete():
    time.sleep(10)
    config = Config.parse_commandline_args([
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ec2/infra-operator-tests/instance.yaml",
        "delete"
    ])
    cli.main(config)
