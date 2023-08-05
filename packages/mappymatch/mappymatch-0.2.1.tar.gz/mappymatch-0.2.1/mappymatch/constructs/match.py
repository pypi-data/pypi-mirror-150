from typing import NamedTuple, Optional

from mappymatch.constructs.coordinate import Coordinate
from mappymatch.constructs.road import Road


class Match(NamedTuple):
    """
    represents a match made by a map matching algorithm
    """

    road: Optional[Road]
    coordinate: Coordinate
    distance: float

    def set_coordinate(self, c: Coordinate):
        return self._replace(coordinate=c)

    def to_json(self) -> dict:
        out = {
            "road_id": self.road.road_id if self.road else None,
            "coordinate_id": self.coordinate.coordinate_id,
            "distance_to_road": self.distance,
        }
        return out
