# -*- coding: utf-8 -*-
"""Documentation about the Geometry-to-Grid generator module."""

import logging
from itertools import product
from typing import Tuple

import geopandas as gpd
import numpy as np
import shapely.geometry

logger = logging.getLogger(__name__)


def gridify(
    include_area: gpd.GeoDataFrame,
    exclude_area: gpd.GeoDataFrame = None,
    grid_size: Tuple[float, float] = (288, 288),
    include_partial: bool = True,
) -> gpd.GeoDataFrame:
    """Construct grid that covers an area.

    Gridify covers the area given by include_area with grid_size sized box shaped
    polygons. The area indicated by exclude_area is subtracted. If include_partial
    is True (default), then boxes that partially overlap the resulting area are
    included, and if include_partial is False then they are excluded.

    Parameters
    ----------
    include_area : geopandas.GeoDataFrame
        Geopandas dataframe that indicates the area to be included
    exclude_area : geopandas.GeoDataFrame
    grid_size : tuple[float, float]
    include_partial : bool

    Returns
    -------
    Geopandas dataframe containing grid covering include_area excluding exclude_area.

    """
    minx, miny, maxx, maxy = include_area.total_bounds
    width, height = grid_size
    grid = _make_grid(minx, miny, maxx, maxy, width, height)

    grid = grid.sjoin(
        include_area, how="inner", predicate="intersects"
    ).drop_duplicates(subset="geometry")
    grid["col"] = range(grid.shape[0])  # For debugging / vis

    if exclude_area is not None:
        exclude_poly = exclude_area.dissolve().geometry[0]
        if include_partial:
            grid = grid[~grid.within(exclude_poly)]
        else:
            grid = grid[~grid.intersects(exclude_poly)]

    return grid


def _make_grid(
    min_x: float, min_y: float, max_x: float, max_y: float, width: float, height: float
) -> gpd.GeoDataFrame:
    """Make a grid of polygons in a geopandas GeoSeries.

    Parameters
    ----------
        min_x: minimum x value of resulting grid
        min_y: minimum y value of resulting grid
        max_x: maximum x value of resulting grid
        max_y: maximum y value of resulting grid
        width: width of grid cells
        height: height of grid cells

    Returns
    -------
    gpd.GeoDataFrame containing a grid with bounding points (min_x, min_y, max_x, max_y)
    built out of width x height cells
    """
    return gpd.GeoDataFrame(
        geometry=gpd.GeoSeries(
            [
                shapely.geometry.box(x, y, x + width, y + height)
                for x, y in product(
                    np.arange(min_x, max_x, width), np.arange(min_y, max_y, height)
                )
            ]
        )
    )
