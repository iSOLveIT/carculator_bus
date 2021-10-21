import numpy as np

from carculator_bus import *


def test_acceleration():
    ecm = EnergyConsumptionModel("Urban delivery", size=["13m-city"])
    # Sum of acceleration should be close to zero
    assert np.isclose(ecm.acceleration.sum(), 0) == True
    # Average speed of Urban delivery driving cycle should be above 10 and below 50
    assert (ecm.velocity[..., 0] / 1000 * 3600).mean() > 10
    assert (ecm.velocity[..., 0] / 1000 * 3600).mean() < 50


def test_motive_energy():
    # 40t diesel and gas trucks must have a fuel consumption comprised between
    # 15 L/100km and 35 L/km

    tip = BusInputParameters()
    tip.static()
    _, array = fill_xarray_from_input_parameters(tip)
    tm = BusModel(array, country="CH")
    tm.set_all()

    assert (
        tm.array.sel(
            powertrain=["ICEV-d", "ICEV-g"], parameter="TtW energy", size="13m-city"
        )
        / 1000
        * 100
        / 42.4
    ).min() > 14
    assert (
        tm.array.sel(
            powertrain=["ICEV-d", "ICEV-g"], parameter="TtW energy", size="13m-city"
        )
        / 1000
        * 100
        / 42.4
    ).max() < 45
