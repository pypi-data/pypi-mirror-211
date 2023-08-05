import lightcon
import pytest
from lightcon.eth_motor_board import EthMotorBoard
import os

force_skip_hw_tests = True

is_azure = os.getenv("AZURE_EXTENSION_DIR") is not None

if not is_azure:
    print("Running on a local machine.")
else :
    print("Running on Azure!")

skip_hw_tests = is_azure or force_skip_hw_tests


@pytest.fixture(scope="module")
def ip_address():
    return '10.1.1.0'

@pytest.fixture(scope="module")
@pytest.mark.skipif(skip_hw_tests == True, reason = "Hardware tests disabled")
def emb(ip_address):
    try:
        return EthMotorBoard(ip_address)
    except RuntimeError:
        assert False, "Cannot connect to motor board at {:}".format(ip_address)

    return None

@pytest.mark.skipif(skip_hw_tests == True, reason = "Hardware tests disabled")
def test_set_motor_parameters(emb):
    result = emb.setup_motor(0, 'Sanyo Denki SH2141-5541.json', True)
    assert result == True

    result = emb.setup_motor(0, '8HS11-0204S.json', True)
    assert result == True

    from lightcon.common.motor_parameters import motor_parameters
    result = emb.setup_motor_dict(motor_index = 0, motor_cfg = motor_parameters['8HS11-0204S.json'], verbose=True)
    assert result == True

def test_motor_parameters():
    from lightcon.common.motor_parameters import motor_parameters
    print('Available motor configurations:')
    print(motor_parameters.keys())
    assert True