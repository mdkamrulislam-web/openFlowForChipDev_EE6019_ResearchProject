import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_shift_register(dut):
    # 20 ns per clock cycle = 50 MHz, matching info.yaml and template config.
    # Drive inputs with clk low; sample 5 ns after its rising edge.
    dut.clk.value = 0
    dut.ena.value = 1
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    async def cycle(bit=0, enable=1, reset=False, unused=0):
        dut.clk.value = 0
        dut.ui_in.value = (unused & 0xFC) | (enable << 1) | bit
        dut.rst_n.value = int(not reset)
        await Timer(10, unit="ns")
        dut.clk.value = 1
        await Timer(5, unit="ns")
        result = int(dut.uo_out.value)
        assert int(dut.uio_oe.value) == 0, "Unused bidirectional pins must be inputs"
        assert int(dut.uio_out.value) == 0, "Unused output path must be zero"
        await Timer(5, unit="ns")
        return result

    dut._log.info("1. Reset clears the stored bits")
    assert await cycle(reset=True) == 0

    dut._log.info("2. Send 10110010; expect 0xB2 after eight shifts")
    expected = 0
    for bit in [1, 0, 1, 1, 0, 0, 1, 0]:
        expected = ((expected << 1) | bit) & 0xFF
        assert await cycle(bit) == expected
    assert expected == 0xB2

    dut._log.info("3. Disabled clock cycles hold 0xB2")
    for bit in [1, 0, 1]:
        assert await cycle(bit, enable=0) == 0xB2

    dut._log.info("4. A ninth shift drops the oldest bit: B2 -> 65")
    assert await cycle(1) == 0x65

    dut._log.info("5. Unused input pins do not change the function")
    dut.uio_in.value = 0xFF
    assert await cycle(0, unused=0xFC) == 0xCA

    dut._log.info("6. Reset wins even when shifting is enabled")
    assert await cycle(1, enable=1, reset=True) == 0

    dut._log.info("7. Reset also clears when shifting is disabled")
    assert await cycle(1) == 1
    assert await cycle(1, enable=0, reset=True) == 0

    dut._log.info("8. Repeated bits fill, then empty, all eight positions")
    expected = 0
    for bit in [1] * 10 + [0] * 10:
        expected = ((expected << 1) | bit) & 0xFF
        assert await cycle(bit) == expected
    assert expected == 0
    dut._log.info("PASS: reset, shift direction, hold, overflow and pin directions")
