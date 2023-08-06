from typing import Union

from .has_coordinates import CoordinatesT, HasCoordinates

CoordinatesLike = Union[HasCoordinates[CoordinatesT], CoordinatesT]
