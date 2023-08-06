import pytest
from infra_operator import cli
from infra_operator.preprocess.mod import preprocess_file
from infra_operator.utils.load import load as yaml_load
from infra_operator.utils import config as Config


@pytest.mark.order(after="test_0_create.py::test_sm_create")
def test_sm_export():
    config = Config.parse_commandline_args([
        # "-w",
        # "n",
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/comb-1/sm.yaml",
        "export"
    ])
    result = cli.main(config)
    # expected = yaml_load(
    #     "aws/mainsite/dev/ap-northeast-1/ecs/bin-dev-infra-operator-tests-cluster/cluster.exported.yaml")
    # assert result == expected
