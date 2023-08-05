import pytest
import time
from lightcon.harpia import Harpia
from lightcon.eth_motor_board import EthMotorBoard

skip_test_harpia = True
skip_test_emb = True

def work_leprecan_provider(provider):
    reg = provider.GetRegister(0x1c0, 0x0001, 0)
    assert reg is not None

    provider.SetRegister(0x1c0, 0x0050, 0, 0x00010000)
    time.sleep(2)
    provider.SetRegister(0x1c0, 0x0050, 0, 0x00000000)

@pytest.mark.skipif(skip_test_harpia == True, reason="HARPIA hardware testing is disabled")
def test_harpia_can():
    harpia = Harpia('127.0.0.1')
    work_leprecan_provider(harpia.can)

@pytest.mark.skipif(skip_test_emb == True, reason="EthMotorBoard hardware testing is disabled")
def test_eth_motor_board_can():
    emb = EthMotorBoard('10.1.1.0')
    work_leprecan_provider(emb.can)
    