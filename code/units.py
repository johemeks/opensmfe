"""Unit harmonization for OpenSmFe.

Plain-language note: this file converts every published number into one standard
(SI) unit per property, so values from different papers can sit side by side.
The original number and unit are always kept too. You do not need to open this
file; the conversion factors are listed in docs/CODEBOOK.md.

Rules
- Coercivity -> kA/m.  1 kOe = 79.5775 kA/m; 1 Oe = 0.0795775 kA/m;
  mu0*H in T -> kA/m multiply by 795.775; 1 MA/m = 1000 kA/m.
- Remanence / magnetization keep their BASIS:
  mass basis (emu/g, A m2/kg; numerically identical) -> A m2/kg
  volume basis (T, kG, G) -> T.  1 kG = 0.1 T.
  Mass-basis values are NOT converted to tesla, because that needs the sample
  density, which most papers do not report for powders or bonded magnets.
- (BH)max -> kJ/m3.  1 MGOe = 7.95775 kJ/m3.
- Curie temperature -> K.  C + 273.15.
"""

from math import pi

MU0 = 4 * pi * 1e-7

HC = {
    "koe": lambda v: v * 1000 / (4 * pi),
    "oe": lambda v: v / (4 * pi),
    "ka/m": lambda v: v,
    "a/m": lambda v: v / 1000,
    "ma/m": lambda v: v * 1000,
    "t": lambda v: v / MU0 / 1000,   # mu0*Hc quoted in tesla
}
MAG_MASS = {"emu/g": 1.0, "am2/kg": 1.0, "a m2/kg": 1.0, "a·m2/kg": 1.0}
MAG_VOL = {"t": 1.0, "kg": 0.1, "kgs": 0.1, "g": 1e-4, "gs": 1e-4}
BH = {"mgoe": 100 / (4 * pi), "kj/m3": 1.0}  # 1 MGOe = 100/(4 pi) kJ/m3 = 7.9577
TC = {"k": lambda v: v, "c": lambda v: v + 273.15, "°c": lambda v: v + 273.15}

COERCIVITY = {"Hcj", "Hcb", "Hc_unspecified"}
MAGNETIZATION = {"Br", "Mr", "Ms"}


def norm(u):
    return u.strip().lower().replace(" ", "").replace("²", "2").replace("³", "3").replace("−", "-")


def to_si(prop, value, unit):
    """Return (value_si, unit_si, basis). Raises ValueError on an unknown unit."""
    u = norm(unit)
    v = float(value)
    if prop in COERCIVITY:
        if u not in HC:
            raise ValueError(f"unknown coercivity unit {unit!r}")
        return HC[u](v), "kA/m", ""
    if prop in MAGNETIZATION:
        if u in {norm(k) for k in MAG_MASS}:
            return v, "A m2/kg", "mass"
        if u in MAG_VOL:
            return v * MAG_VOL[u], "T", "volume"
        raise ValueError(f"unknown magnetization unit {unit!r}")
    if prop == "BHmax":
        if u not in BH:
            raise ValueError(f"unknown (BH)max unit {unit!r}")
        return v * BH[u], "kJ/m3", ""
    if prop == "Tc":
        if u not in TC:
            raise ValueError(f"unknown temperature unit {unit!r}")
        return TC[u](v), "K", ""
    raise ValueError(f"unknown property {prop!r}")


def parse_temperature_K(raw):
    """Measurement temperature as written -> (kelvin or None, status).
    status: 'stated', 'assumed_RT' (phrase like 'room temperature' followed by a verify marker),
    'not_stated', or 'n/a' (for Curie temperature rows)."""
    r = (raw or "").strip().lower()
    if r in ("", "not stated"):
        return None, "not_stated"
    if r == "n/a":
        return None, "n/a"
    if r.startswith("room temperature"):
        return 298.0, "assumed_RT" if "verify" in r else "stated"
    num = r.split()[0]
    try:
        val = float(num)
    except ValueError:
        return None, "not_stated"
    if " c" in r or "°c" in r:
        val += 273.15
    return val, "stated"


if __name__ == "__main__":
    # self-test with textbook equivalences
    assert abs(to_si("Hcj", 1, "kOe")[0] - 79.5775) < 1e-3
    assert abs(to_si("Hcj", 1, "T")[0] - 795.775) < 1e-2
    assert abs(to_si("Hcj", 0.056, "MA/m")[0] - 56) < 1e-9
    assert abs(to_si("BHmax", 1, "MGOe")[0] - 7.9577) < 1e-3
    assert to_si("Br", 10.12, "kG")[:2] == (10.12 * 0.1, "T")
    assert to_si("Mr", 75.3, "emu/g")[1:] == ("A m2/kg", "mass")
    assert abs(to_si("Tc", 475, "°C")[0] - 748.15) < 1e-9
    print("units.py self-test passed")
