import math

from hypothesis import example, given, strategies as st

from irrigation_scheduler import moisture_average, parse_zone, water_needed


ARBITRARY_INPUT = st.one_of(st.text(), st.none(), st.integers(), st.binary())
NONNEGATIVE_NUMBER = st.integers(min_value=0, max_value=10**9)


@given(ARBITRARY_INPUT)
def test_parse_zone_no_crash(s):
    result = parse_zone(s)
    if result is not None:
        name, area = result
        assert name and name == name.strip()
        assert math.isfinite(area) and area >= 0


@given(ARBITRARY_INPUT)
def test_moisture_average_no_crash(s):
    result = moisture_average(s)
    if result is not None:
        assert isinstance(result, int) and 0 <= result <= 100


@given(ARBITRARY_INPUT)
def test_water_needed_no_crash(s):
    result = water_needed(s)
    if result is not None:
        assert math.isfinite(result) and result >= 0


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1), NONNEGATIVE_NUMBER)
def test_parse_zone_accepts_valid_input(name, area):
    assert parse_zone(f" {name} : {area} ") == (name.title(), float(area))


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=40))
def test_moisture_average_preserves_floor(readings):
    csv = ", ".join(map(str, readings))
    assert moisture_average(csv) == sum(readings) // len(readings)


@given(NONNEGATIVE_NUMBER, NONNEGATIVE_NUMBER)
def test_water_needed_preserves_formula(area, rain):
    assert water_needed(f"{area}|{rain}") == max(area * 5 - rain, 0)


@given(st.integers(max_value=-1))
@example(-1)
def test_parse_zone_rejects_negative_area(area):
    assert parse_zone(f"north:{area}") is None


@given(st.one_of(st.integers(max_value=-1), st.integers(min_value=101)))
@example(101)
def test_moisture_average_rejects_out_of_range_readings(reading):
    assert moisture_average(f"40,{reading},50") is None


@given(st.integers(max_value=-1), st.booleans())
@example(-1, False)
def test_water_needed_rejects_negative_fields(negative, in_area):
    text = f"{negative}|8" if in_area else f"120|{negative}"
    assert water_needed(text) is None


@given(st.sampled_from(["north:NaN", "north:inf", ":120", "north:1:2"]))
def test_parse_zone_rejects_bad_fields(text):
    assert parse_zone(text) is None


@given(st.sampled_from(["", "40,,50", "40,wet", "40,35.5"]))
def test_moisture_average_rejects_bad_fields(text):
    assert moisture_average(text) is None


@given(st.sampled_from(["NaN|8", "120|inf", "1e308|0", "120||8"]))
def test_water_needed_rejects_bad_fields(text):
    assert water_needed(text) is None
