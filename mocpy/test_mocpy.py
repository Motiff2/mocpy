import pytest
import random
from .interval_set import IntervalSet
from .moc import MOC
from astropy.coordinates import SkyCoord


@pytest.fixture()
def isets():
    random.seed(0)

    a = IntervalSet()
    for x in range(0, 10):
        start = random.randint(0, 100)
        a.add((start, start + random.randint(0, 30)))

    b = IntervalSet()
    for x in range(0, 10):
        start = random.randint(0, 100)
        b.add((start, start + random.randint(0, 30)))

    return dict(a=a, b=b)


def test_interval_set(isets):

    assert isets['a'].intervals == [(27, 126)]

    assert isets['b'].intervals == [(9, 61), (68, 105)]

    assert isets['a'].union(isets['b']).intervals == [(9, 126)]

    assert isets['a'].difference(isets['b']).intervals == [(61, 68), (105, 126)]

    assert isets['b'].difference(isets['a']).intervals == [(9, 27)]

    assert isets['a'].intersection(isets['b']).intervals == [(27, 61), (68, 105)]

    assert IntervalSet.flatten(isets['a'].intervals) == [27, 126]


def get_random_skycoords(size):
    return SkyCoord(ra=[random.uniform(0, 1) * 360 for i in range(size)],
                    dec=[random.uniform(0, 1)*180 - 90 for i in range(size)],
                    unit="deg")


skycoords1 = get_random_skycoords(size=1000)
skycoords2 = get_random_skycoords(size=2000)
skycoords3 = get_random_skycoords(size=5000)


def test_compare_the_two_from_coo_list_methods():
    moc_fast = MOC.from_coo_list_no_iteration(skycoords1, max_norder=14)
    moc_slow = MOC.from_coo_list(skycoords1, max_norder=14)
    assert moc_fast == moc_slow


@pytest.mark.parametrize("skycoords", [
    skycoords1,
    skycoords2,
    skycoords3
])
def test_mocpy_from_coo_no_iteration(skycoords):
    moc = MOC.from_coo_list_no_iteration(skycoords, max_norder=14)


@pytest.mark.parametrize("skycoords", [
    skycoords1,
    skycoords2,
    skycoords3
])
def test_mocpy_from_coo_list(skycoords):
    moc = MOC.from_coo_list(skycoords, max_norder=14)
