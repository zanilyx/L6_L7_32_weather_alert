import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert


# ---------- wind_alert (boundaries: 38/39, 61/62, 88/89) ----------
@pytest.mark.parametrize("speed, expected", [
    (10, "none"), (38, "none"),
    (39, "advisory"), (61, "advisory"),
    (62, "watch"), (88, "watch"),
    (89, "warning"), (150, "warning"),
])
def test_wind_alert(speed, expected):
    assert wind_alert(speed) == expected


# ---------- rain_alert (boundaries: 9.9/10, 49.9/50) ----------
@pytest.mark.parametrize("mm, saturated, expected", [
    (50, True, "warning"), (50, False, "watch"),
    (49.9, True, "watch"), (49.9, False, "advisory"),
    (10, True, "watch"), (10, False, "advisory"),
    (9.9, True, "none"), (0, False, "none"),
])
def test_rain_alert(mm, saturated, expected):
    assert rain_alert(mm, saturated) == expected


# ---------- heat_alert ----------
# humidity <= 40 -> no humidity adjustment (False branch)
@pytest.mark.parametrize("temp, humidity, expected", [
    (40, 40, "watch"),      # humidity exactly 40 -> no adjustment
    (30, 20, "none"),
    (35, 10, "advisory"),
    (45, 0, "warning"),
])
def test_heat_low_humidity(temp, humidity, expected):
    assert heat_alert(temp, humidity) == expected

# humidity > 40 -> adjustment applied (True branch)
@pytest.mark.parametrize("temp, humidity, expected", [
    (39, 100, "warning"),   # 39 + 6.0 = 45.0
    (34, 100, "watch"),     # 34 + 6.0 = 40.0
    (30, 90, "advisory"),   # 30 + 5.0 = 35.0
    (20, 50, "none"),       # 20 + 1.0 = 21.0
])
def test_heat_high_humidity(temp, humidity, expected):
    assert heat_alert(temp, humidity) == expected


# ---------- overall_alert ----------
def test_no_alerts():
    assert overall_alert([]) == "none"

def test_overall_picks_worst():
    assert overall_alert(["advisory", "warning", "watch"]) == "warning"

def test_overall_worst_first_then_lower():
    assert overall_alert(["warning", "none", "advisory"]) == "warning"

def test_overall_all_none():
    assert overall_alert(["none", "none"]) == "none"

def test_overall_unknown_alert():
    with pytest.raises(ValueError):
        overall_alert(["advisory", "tornado"])
