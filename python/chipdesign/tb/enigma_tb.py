# tb/enigma_tb.py
import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.clock import Clock

CLK_PERIOD_NS = 10


async def press_key(dut, val):
    """Pulse confirm with din=val and wait for valid."""
    dut.din.value = val
    dut.confirm.value = 1
    await RisingEdge(dut.clk)
    dut.confirm.value = 0

    # wait a few cycles for 'valid'
    for _ in range(5):
        await RisingEdge(dut.clk)
        if dut.valid.value:
            return int(dut.dout.value)
    assert False, "valid did not assert within 5 cycles"


@cocotb.test()
async def basic_enigma_smoke(dut):
    # Clock
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_NS, units="ns").start())

    # Defaults
    dut.ena.value = 1
    dut.din.value = 0
    dut.confirm.value = 0
    dut.reset_btn.value = 0

    # Reset
    dut.rst_n.value = 0
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)

    # Tap the front-panel reset_btn -> should load R=12, M=11, L=25
    dut.reset_btn.value = 1
    await RisingEdge(dut.clk)
    dut.reset_btn.value = 0
    await RisingEdge(dut.clk)

    # Check internal positions (hierarchical peek is fine with Icarus)
    pos_r = int(dut.pos_r.value)
    pos_m = int(dut.pos_m.value)
    pos_l = int(dut.pos_l.value)
    assert (pos_r, pos_m, pos_l) == (
        12,
        11,
        25,
    ), f"bad defaults: {(pos_r, pos_m, pos_l)}"

    # Press a few keys, ensure valid+bounded outputs and rotor stepping
    before_r = pos_r
    out0 = await press_key(dut, 0)  # 'A' -> 0
    assert 0 <= out0 < 26

    await RisingEdge(dut.clk)  # positions updated when we latched the key
    pos_r1 = int(dut.pos_r.value)
    assert pos_r1 == ((before_r + 1) % 26), "right rotor did not step"

    # More random-ish presses
    for v in [25, 13, 7, 4, 19]:
        o = await press_key(dut, v)
        assert 0 <= o < 26

    # Sanity: valid deasserts next cycle
    await RisingEdge(dut.clk)
    assert not dut.valid.value
