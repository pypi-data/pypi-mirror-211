#! /usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = 'Alan Loh'
__copyright__ = 'Copyright 2022, nenupy'
__credits__ = ['Alan Loh']
__maintainer__ = 'Alan'
__email__ = 'alan.loh@obspm.fr'
__status__ = 'Production'


import pytest
from unittest.mock import patch
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time, TimeDelta
import numpy as np

from nenupy.schedule import (
    Schedule,
    ObsBlock,
    ReservedBlock,
    ESTarget,
    SSTarget,
    Constraints,
    ElevationCnst,
    AzimuthCnst,
    MeridianTransitCnst,
    AzimuthCnst,
    LocalTimeCnst,
    TimeRangeCnst,
    Constraints
)


# ============================================================= #
# -------------------------- TestBST -------------------------- #
# ============================================================= #

@pytest.fixture(scope="class")
def get_schedule_instance():
    return Schedule(
        time_min=Time("2022-01-01T00:00:00"),
        time_max=Time("2022-01-03T00:00:00"),
        dt=TimeDelta(3600, format="sec")
    )

@pytest.fixture(autouse=True, scope="class")
def _use_schedule(request, get_schedule_instance):
    request.cls.schedule = get_schedule_instance

@pytest.mark.usefixtures("_use_schedule")
class TestSchedule:

    # ========================================================= #
    # ------------------ test_schedule_init ------------------- #
    def test_schedule_init(self):
        assert self.schedule.size == 48
        assert self.schedule.starts.size == 48
        assert self.schedule.stops.size == 48
        assert np.all(self.schedule.freeSlots)
        assert self.schedule.idxSlots.size == 48


    def test_schedule_time2idx(self):
        indices = self.schedule.time2idx(Time("2022-01-01T00:30:00"))
        assert indices.size == 1
        assert indices[0] == 0
        indices = self.schedule.time2idx(Time("2022-01-01T00:30:00"), Time("2022-01-01T02:30:00"))
        assert indices.size == 3


    # ========================================================= #
    # --------------- test_schedule_add_booking --------------- #
    def test_schedule_add_booking(self):
        self.schedule.add_booking(
            time_min=Time("2022-01-01T02:30:00"),
            time_max=Time("2022-01-01T05:10:00"),
        )
        assert np.all(self.schedule.freeSlots[:2])
        assert np.all(~self.schedule.freeSlots[2:6])
        assert np.all(self.schedule.freeSlots[6:])


    # ========================================================= #
    # --------------- test_schedule_del_booking --------------- #
    def test_schedule_del_booking(self):
        self.schedule.remove_booking(
            time_min=Time("2022-01-01T02:30:00"),
            time_max=Time("2022-01-01T05:10:00"),
        )
        assert np.all(self.schedule.freeSlots)


    # ========================================================= #
    # --------------- test_insert_reserved_block --------------- #
    def test_insert_reserved_block(self):
        maintenance = ReservedBlock(
            time_min=Time("2022-01-01T10:00:00"),
            time_max=Time("2022-01-01T14:00:00")
        )
        maintenance2 = ReservedBlock(
            time_min=Time("2022-01-01T16:00:00"),
            time_max=Time("2022-01-01T20:00:00")
        )
        self.schedule.insert(maintenance, maintenance2)
        self.schedule.insert(maintenance + maintenance2)
        assert sum(self.schedule.freeSlots) == 40


    # ========================================================= #
    # --------------- test_insert_reserved_block --------------- #
    def test_insert_obs_block(self):
        cyga = ObsBlock(
            name='blabla',
            program='ES01',
            target=ESTarget.fromName("Cyg A"),
            duration=TimeDelta(1800*4, format="sec"),
            constraints=Constraints(
                ElevationCnst(elevationMin=10),
                AzimuthCnst(170),
                MeridianTransitCnst()
            )
        )
        self.schedule.insert(cyga)

    # ========================================================= #
    # ------------------ test_schedule_plot ------------------- #
    @patch("matplotlib.pyplot.show")
    def test_schedule_plot(self, mock_show):
        self.schedule.plot()
# ============================================================= #
# ============================================================= #

