import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, First
from cocotb.clock import Clock
import random

# ---------- Python reference ----------
ROT3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"  # right = III
ROT1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"  # middle = I
ROT4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"  # left = IV
UKWB = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

NOTCH_I = "Q"  # 16
NOTCH_III = "V"  # 21
NOTCH_IV = "J"  # 9  (kun til info; bruges ikke i stepping her)


def i(c):
    return ord(c) - 65


def C(x):
    return chr(x + 65)


def fwd(layout, x):
    return i(layout[x])


def inv(layout, x):
    return layout.index(C(x))


def enigma_ref(text, start=(12, 11, 25)):
    # positions: (R,M,L) = (III, I, IV)
    pos_r, pos_m, pos_l = start
    out = []
    for ch in text:
        # stepping før routing (historisk korrekt)
        notch_r = pos_r == i(NOTCH_III)
        notch_m = pos_m == i(NOTCH_I)
        if notch_m:
            pos_l = (pos_l + 1) % 26
        if notch_r or notch_m:
            pos_m = (pos_m + 1) % 26
        pos_r = (pos_r + 1) % 26

        x = i(ch)
        x = (fwd(ROT3, (x + pos_r) % 26) - pos_r) % 26
        x = (fwd(ROT1, (x + pos_m) % 26) - pos_m) % 26
        x = (fwd(ROT4, (x + pos_l) % 26) - pos_l) % 26
        x = i(UKWB[x])
        x = (inv(ROT4, (x + pos_l) % 26) - pos_l) % 26
        x = (inv(ROT1, (x + pos_m) % 26) - pos_m) % 26
        x = (inv(ROT3, (x + pos_r) % 26) - pos_r) % 26
        out.append(C(x))
    return "".join(out)


# ---------- DUT helpers ----------
async def reset_dut(dut):
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)


async def press_reset_btn(dut):
    # ui_in[7] = reset_btn
    dut.ui_in.value = int(dut.ui_in.value) | (1 << 7)
    await RisingEdge(dut.clk)
    dut.ui_in.value = int(dut.ui_in.value) & ~(1 << 7)
    await RisingEdge(dut.clk)


async def send_letter(dut, code):
    """code: 0..25. Puls confirm på ui_in[5]. Returner (out_code)."""
    # læg data
    base = int(dut.ui_in.value) & ~0x1F
    dut.ui_in.value = base | (code & 0x1F)
    await RisingEdge(dut.clk)
    # confirm = 1
    dut.ui_in.value = int(dut.ui_in.value) | (1 << 5)
    await RisingEdge(dut.clk)
    # confirm = 0
    dut.ui_in.value = int(dut.ui_in.value) & ~(1 << 5)

    # vent på valid
    while True:
        await RisingEdge(dut.clk)
        if (int(dut.uo_out.value) >> 6) & 1:
            return int(dut.uo_out.value) & 0x1F


@cocotb.test()
async def test_simple_sequence(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)

    # Reset-knap sætter pos til (12,11,25)
    await press_reset_btn(dut)

    text = "HELLOWORLD"
    expected = enigma_ref(text, start=(12, 11, 25))
    got = ""
    for ch in text:
        code = ord(ch) - 65
        outc = await send_letter(dut, code)
        got += chr(outc + 65)

    assert got == expected, f"{got=} != {expected=}"


@cocotb.test()
async def test_reset_reproducible(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)

    seq = "ABCDEF"
    # første run
    await press_reset_btn(dut)
    out1 = ""
    for ch in seq:
        out1 += chr((await send_letter(dut, ord(ch) - 65)) + 65)

    # forstyr positions ved at sende et par tegn
    for ch in "XYZ":
        await send_letter(dut, ord(ch) - 65)

    # reset igen -> samme output for samme inputsekvens
    await press_reset_btn(dut)
    out2 = ""
    for ch in seq:
        out2 += chr((await send_letter(dut, ord(ch) - 65)) + 65)

    assert out1 == out2


@cocotb.test()
async def test_random_block_vs_ref(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)
    await press_reset_btn(dut)

    rng = random.Random(1234)
    block = "".join(chr(rng.randrange(26) + 65) for _ in range(50))
    exp = enigma_ref(block, start=(12, 11, 25))

    got = ""
    for ch in block:
        got += chr((await send_letter(dut, ord(ch) - 65)) + 65)

    assert got == exp


@cocotb.test()
async def test_ignore_invalid_codes(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)
    await press_reset_btn(dut)

    # læg en ulovlig kode 31 + confirm -> forvent ingen valid
    base = int(dut.ui_in.value) & ~0x1F
    dut.ui_in.value = base | 31
    await RisingEdge(dut.clk)
    dut.ui_in.value = int(dut.ui_in.value) | (1 << 5)
    await RisingEdge(dut.clk)
    dut.ui_in.value = int(dut.ui_in.value) & ~(1 << 5)

    # vent nogle cycles og tjek at valid ikke blev sat
    valid_seen = False
    for _ in range(10):
        await RisingEdge(dut.clk)
        if (int(dut.uo_out.value) >> 6) & 1:
            valid_seen = True
            break
    assert not valid_seen, "Invalid kode må ikke give valid"
