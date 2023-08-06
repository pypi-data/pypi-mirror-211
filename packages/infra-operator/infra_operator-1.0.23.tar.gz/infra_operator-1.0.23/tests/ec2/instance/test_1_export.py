import pytest
from infra_operator import cli
from infra_operator.operators.mod import remove_nested_field
from infra_operator.preprocess.mod import preprocess_file
from infra_operator.utils.load import load as yaml_load
from infra_operator.utils import config as Config


@pytest.mark.order(10000)
def test_ec2_export():
    config = Config.parse_commandline_args([
        "-w",
        "n",
        "-t",
        "aws/mainsite/dev/ap-northeast-1/ec2/infra-operator-tests/instance.yaml",
        "export"
    ])
    result = cli.main(config)
    kind, info, expected = preprocess_file(
        "aws/mainsite/dev/ap-northeast-1/ec2/infra-operator-tests/instance.exported.yaml", {}, enable_ref_file=True, wait_for_ref=False)
    remover_1 = remove_nested_field(["metadata", "InstanceId"])
    remover_2 = remove_nested_field(
        ["spec", "BlockDeviceMappings", list, "Ebs", "VolumeId"])
    result = remover_2(remover_1(result))
    expected = remover_2(remover_1(expected))
    assert result == expected
