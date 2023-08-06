################################################################################
Geometry-to-Grid generator
################################################################################

.. begin-inclusion-intro-marker-do-not-remove

Gridify takes geometries in a geopandas dataframe to describe areas to in- and exclude. It then generates a grid of box shaped polygons covering the include area.


.. end-inclusion-intro-marker-do-not-remove


.. begin-inclusion-usage-marker-do-not-remove

How to use
----------

Import packages

.. code:: ipython3

    import geopandas as gpd
    import shapely.geometry
    import matplotlib.pyplot as plt

    from gridify.gridify import gridify

Define an include area consisting of a polygon and a line part. And put
it in a geodataframe.

.. code:: ipython3

    part1 = shapely.geometry.box(
       minx=0,
       miny=0,
       maxx=0.5,
       maxy=1,
    )
    part2 = shapely.geometry.LineString(
       [
           (0.5, 0),
           (5 / 6, 1.0),
       ]
    )
    include_gdf = gpd.GeoDataFrame({"col1": [1, 2]}, geometry=[part1, part2])
    ax = include_gdf.plot(column="col1")
    ax.set_xlim([-.1, 1.2])
    ax.set_ylim([-.1, 1.2])


.. image:: https://gitlab.com/rwsdatalab/codebase-opensource/image/gridify/-/raw/develop/docs/_static/figs/output_3_1.png


Define an area to exclude

.. code:: ipython3

    exclude = shapely.geometry.box(
        minx=0.5,
        miny=0.5,
        maxx=1.1,
        maxy=1.1,
    )
    exclude_gdf = gpd.GeoDataFrame({"col1": [1]}, geometry=[exclude])
    ax = exclude_gdf.plot(color="red", alpha=0.5)
    ax.set_xlim([-.1, 1.2])
    ax.set_ylim([-.1, 1.2])



.. image:: https://gitlab.com/rwsdatalab/codebase-opensource/image/gridify/-/raw/develop/docs/_static/figs/output_5_1.png


Use include area and exclude area to define a grid with (1/3) as grid
size. Include partial overlap with the exclusion area into the grid.

.. code:: ipython3

    grid = gridify(
        include_area=include_gdf,
        exclude_area=exclude_gdf,
        grid_size=((1/3), (1/3)),
        include_partial=False,
    )

    ax = grid.boundary.plot()
    ax.set_xlim([-.1, 1.2])
    ax.set_ylim([-.1, 1.2])



.. image:: https://gitlab.com/rwsdatalab/codebase-opensource/image/gridify/-/raw/develop/docs/_static/figs/output_7_1.png


Plot the grid overlapping the include area in green, and the exclude
area in red.

.. code:: ipython3

    ax = include_gdf.plot(color="green", alpha=0.5)
    exclude_gdf.plot(ax=ax, color="red", alpha=0.5)
    grid.boundary.plot(ax=ax, color="blue")



.. image:: https://gitlab.com/rwsdatalab/codebase-opensource/image/gridify/-/raw/develop/docs/_static/figs/output_9_1.png


Alternatively, partial overlap may be included into the final grid.

.. code:: ipython3

    grid_include_partial = gridify(
        include_area=include_gdf,
        exclude_area=exclude_gdf,
        grid_size=((1/3), (1/3)),
        include_partial=True,
    )

    ax = include_gdf.plot(color="green", alpha=0.5)
    exclude_gdf.plot(ax=ax, color="red", alpha=0.5)
    grid_include_partial.boundary.plot(ax=ax, color="blue")

.. image:: https://gitlab.com/rwsdatalab/codebase-opensource/image/gridify/-/raw/develop/docs/_static/figs/output_11_1.png

.. end-inclusion-usage-marker-do-not-remove


.. begin-inclusion-installation-marker-do-not-remove

Installation
------------

To install gridify, do:

.. code-block:: console

  git clone https://gitlab.com/rwsdatalab/codebase-opensource/image/gridify.git
  cd gridify
  pip install .

Run tests (including coverage) with:

.. code-block:: console

  pip install -r requirements-dev.txt
  python setup.py test

.. end-inclusion-installation-marker-do-not-remove


Documentation
-------------

.. _README:

Include a link to your project's full documentation here.


.. begin-inclusion-license-marker-do-not-remove

License
-------

Copyright 2022 Rijkswaterstaat

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


.. end-inclusion-license-marker-do-not-remove
