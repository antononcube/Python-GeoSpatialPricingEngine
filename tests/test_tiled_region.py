import sys
import types

import pytest

class _TaxonomyData:
    def __init__(self, records):
        self.records = records

    def to_dict(self, orient):
        assert orient == "records"
        return self.records


class _NearestResult:
    def __init__(self, tile_id):
        self.tile_id = tile_id

    def take_value(self):
        return {"ID": [self.tile_id]}


class _FakeNearestNeighborsProcessor:
    instances = []

    def __init__(self, tile_centers):
        self.tile_centers = tile_centers
        self.points = []
        self.instances.append(self)

    def find_nearest(self, point, n):
        assert n == 1
        self.points.append(point)
        return _NearestResult("tile-1")


sys.modules.setdefault(
    "GeometricNearestNeighborsProcessor",
    types.SimpleNamespace(
        GeometricNearestNeighborsProcessor=_FakeNearestNeighborsProcessor
    ),
)

package = pytest.importorskip("GeoSpatialPricingEngine")

GeoPoint = package.GeoPoint
GeoTaxonomy = package.GeoTaxonomy
TiledRegionTrivial = package.TiledRegionTrivial


def test_tile_for_point_maps_coordinates_and_reuses_mapper(monkeypatch):
    _FakeNearestNeighborsProcessor.instances.clear()
    fake_module = types.SimpleNamespace(
        GeometricNearestNeighborsProcessor=_FakeNearestNeighborsProcessor
    )
    monkeypatch.setattr(
        "GeoSpatialPricingEngine.tiled_region.GeometricNearestNeighborsProcessor",
        fake_module.GeometricNearestNeighborsProcessor,
    )

    taxonomy = GeoTaxonomy(
        _TaxonomyData(
            [
                {
                    "tile_id": "tile-1",
                    "center_lat": 10.0,
                    "center_lon": 20.0,
                }
            ]
        )
    )
    region = TiledRegionTrivial(taxonomy)

    assert region.tile_for_point(GeoPoint(11.0, 21.0)) == "tile-1"
    assert region.tile_for_coords(12.0, 22.0) == "tile-1"
    assert len(_FakeNearestNeighborsProcessor.instances) == 1
    assert _FakeNearestNeighborsProcessor.instances[0].tile_centers == {
        "tile-1": (10.0, 20.0)
    }
    assert _FakeNearestNeighborsProcessor.instances[0].points == [
        (11.0, 21.0),
        (12.0, 22.0),
    ]


def test_tile_for_point_requires_geo_point():
    region = TiledRegionTrivial(GeoTaxonomy(_TaxonomyData([])))

    with pytest.raises(TypeError, match="GeoPoint"):
        region.tile_for_point((1.0, 2.0))


def test_trivial_paths_contain_start_and_end_tiles(monkeypatch):
    monkeypatch.setattr(
        "GeoSpatialPricingEngine.tiled_region.GeometricNearestNeighborsProcessor",
        _FakeNearestNeighborsProcessor,
    )
    region = TiledRegionTrivial(GeoTaxonomy(_TaxonomyData([])))
    region.tile_for_point = lambda point: f"tile-{point.x}"
    region.tile_for_coords = lambda x, y: f"tile-{x}"

    assert region.find_path(GeoPoint(1.0, 2.0), GeoPoint(3.0, 4.0)) == [
        "tile-1.0",
        "tile-3.0",
    ]
    assert region.find_path_for_coords(5.0, 6.0, 7.0, 8.0) == [
        "tile-5.0",
        "tile-7.0",
    ]


def test_trivial_region_converts_orders_to_calibration_records():
    region = TiledRegionTrivial(GeoTaxonomy(_TaxonomyData([])))
    region.find_path_for_coords = lambda x1, y1, x2, y2: [
        f"tile-{x1}",
        f"tile-{x2}",
    ]
    orders = types.SimpleNamespace(
        data=_TaxonomyData(
            [
                {
                    "id": 5,
                    "start_lat": 10.0,
                    "start_lon": 20.0,
                    "end_lat": 11.0,
                    "end_lon": 21.0,
                    "distance": 1004.7,
                    "price": 394,
                }
            ]
        )
    )

    assert region.to_calibration_records(orders) == {
        "5": {
            "id": 5,
            "path": ["tile-10.0", "tile-11.0"],
            "distance": 1004.7,
            "price": 394,
        }
    }
