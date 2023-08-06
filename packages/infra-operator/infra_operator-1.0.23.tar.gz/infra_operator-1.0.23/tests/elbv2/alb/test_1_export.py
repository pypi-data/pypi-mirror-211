import pytest
from infra_operator import cli
from infra_operator.preprocess.mod import preprocess_file
from infra_operator.utils.load import load as yaml_load
from infra_operator.utils import config as Config


@pytest.mark.order(10000)
def test_alb_export():
    config = Config.parse_commandline_args([
        "-w",
        "n",
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/alb.yaml",
        "export"
    ])
    result = cli.main(config)
    kind, info, expected = preprocess_file(
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/alb.exported.yaml", {}, enable_ref_file=True, wait_for_ref=False)
    assert result == expected
