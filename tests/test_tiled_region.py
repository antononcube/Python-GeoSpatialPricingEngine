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
