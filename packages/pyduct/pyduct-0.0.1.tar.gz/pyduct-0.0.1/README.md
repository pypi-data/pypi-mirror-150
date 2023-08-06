# PyDuct
> A framework for building and running simple data engineering pipelines in Python.


In Data Science or Data Engineering you constantly hear term “data pipeline”. But there are so many meanings to this term and people often are refering to very specific tools or packages depending on their own background/needs. There are pipelines for pretty much everything and in Python alone I can think of [Luigi](https://luigi.readthedocs.io/en/stable/), [Airflow](https://airflow.apache.org/), [scikit-learn pipelines](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html), and [Pandas pipes](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pipe.html) just off the top of my head - [this article](https://towardsdatascience.com/data-pipelines-what-why-and-which-ones-1f674ba49946) does a good job of helping you understand what is out there.

It can be quite confusing especially if you want a simple and agnostic pipeline that you can customize for your specific needs with no bells and whistles or lock-ins to libraries etc. That is where PyDuct comes in. It is for the simple data engineer who just wants to get stuff done in an ordered and repeatable way.

PyDuct is a simple data pipeline that automates a chain of transformations performed on some data.

PyDuct data pipelines are a great way of introducing automation, reproducibility, structure, and flow to your data engineering projects.

---

PyDuct was made by [Robert Johnson](https://www.robtheoceanographer.com/) and [Alexander Kozlov](https://alexkozlov.com/) and [Mohammadreza Khanarmuei](https://www.linkedin.com/in/mohammadreza-khanarmuei-437a3163)

---

## What is it?

The PyDuct transformation pipelines use user defined transformation functions linked together into a TransformationPipe. The key feature of PyDuct is that the datasource passed in can be almost anything that you desire  - e.g. a pandas dataframe, a geopandas dataframe, and iris datacube, a numppy array, so long as your transformation steps read and write the same object PyDuct will work for you.

![pypipe arch](nbs/images/pypipe.jpeg)

## Install

`pip install pyduct`

## How to use

The TransformationPipe class accepts a list of transformation functions,'steps', to be applied sequentially. Each step contains a name and a function, applied to the input DataObject and will return a transformed DataObject. There is also a third argument in a step that is an optional dictionary of parameters to be passed to your step transformation functions.


In order to use PyDuct you need two things - a DataObject and a set of transformation steps

### DataObject

In this very simplified example we will use a [geopandas.GeoDataFrame](https://geopandas.org/en/stable/index.html) as our input DataObject. To do this we will load an example data set from [Kaggle](https://www.kaggle.com/) on the global distribution of Volcano Eruptions: https://www.kaggle.com/datasets/texasdave/volcano-eruptions that we have stored in the repo for this package as 'volcano_data_2010.csv'

```python
import pandas
import geopandas
```

Load the data and put it into a geopandas dataframe:

```python
df1 = pandas.read_csv('../test_data/volcano_data_2010.csv')
# Keep only relevant columns
df = df1.loc[:, ("Year", "Name", "Country", "Latitude", "Longitude", "Type")]
# Create point geometries
geometry = geopandas.points_from_xy(df.Longitude, df.Latitude)
geo_df = geopandas.GeoDataFrame(df[['Year','Name','Country', 'Latitude', 'Longitude', 'Type']], geometry=geometry)
geo_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Year</th>
      <th>Name</th>
      <th>Country</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Type</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2010</td>
      <td>Tungurahua</td>
      <td>Ecuador</td>
      <td>-1.467</td>
      <td>-78.442</td>
      <td>Stratovolcano</td>
      <td>POINT (-78.44200 -1.46700)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2010</td>
      <td>Eyjafjallajokull</td>
      <td>Iceland</td>
      <td>63.630</td>
      <td>-19.620</td>
      <td>Stratovolcano</td>
      <td>POINT (-19.62000 63.63000)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2010</td>
      <td>Pacaya</td>
      <td>Guatemala</td>
      <td>14.381</td>
      <td>-90.601</td>
      <td>Complex volcano</td>
      <td>POINT (-90.60100 14.38100)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2010</td>
      <td>Sarigan</td>
      <td>United States</td>
      <td>16.708</td>
      <td>145.780</td>
      <td>Stratovolcano</td>
      <td>POINT (145.78000 16.70800)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2010</td>
      <td>Karangetang [Api Siau]</td>
      <td>Indonesia</td>
      <td>2.780</td>
      <td>125.480</td>
      <td>Stratovolcano</td>
      <td>POINT (125.48000 2.78000)</td>
    </tr>
  </tbody>
</table>
</div>



### Steps

Just as an example of something to do we will define only one transformation steps to spatially subset to the Australian region. Yes, i know that this is an unrealistic example but it is just here to show you how to implement pipelines.

We must now write our transformation function - keep in mind that the function must take our DataObject as an input and return a transformed DataObject as a return... in this example that is a geopandas.GeoDataFrame

```python
from pyproj import crs
from shapely.geometry import Polygon, MultiPolygon, box, Point
```

```python
def spatialCrop(gdf: geopandas.GeoDataFrame, **kwargs):
    """
    This function will apply a sptial limit to a GeoDataFrame based on user-defined limits.
    ----------
    parameters:
        gdf (geopandas.GeoDataFrame): an input GeoDataFrame
        kwargs (dict): parameters, 
            - boundingBox (list): an iterable (lon_min, lat_min, lon_max, lat_max) of the specified region.
    Output:
        transformed_gdf (gdp.GeoDataFrame): GeoDataFrame that is spatially limited to the boundingBox.
    """
    if "boundingBox" not in kwargs:
        return gdf

    boundingBox = kwargs["boundingBox"]
    # just an example so we are doing naughty things with the CRS... look away here...
    coord_system = crs.crs.CRS('WGS 84')

    bounding = geopandas.GeoDataFrame(
        {
            'limit': ['bounding box'],
            'geometry': [
                box(boundingBox[0], boundingBox[1], boundingBox[2],
                    boundingBox[3])
            ]
        },
        crs=coord_system)
    limited_gdf = geopandas.tools.sjoin(gdf,
                                        bounding,
                                        op='intersects',
                                        how='left')
    limited_gdf = limited_gdf[limited_gdf['limit'] == 'bounding box']
    limited_gdf = limited_gdf.drop(columns=['index_right', 'limit'])

    return limited_gdf
```

### Define a PyDuct Pipe
Now that we have a step or function and some data we can now define our transformation pipeline:

```python
pipe = TransformationPipe(steps=[
    ('refine region', spatialCrop, {"boundingBox": [80, -50, 180, 0]})
])
```

### Evaluate your PyDuct Pipe
This where things get interesting... we can now call `evaluate` on our pipe and watch the magic happen:

#### Input data:

```python
geo_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Year</th>
      <th>Name</th>
      <th>Country</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Type</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2010</td>
      <td>Tungurahua</td>
      <td>Ecuador</td>
      <td>-1.467</td>
      <td>-78.442</td>
      <td>Stratovolcano</td>
      <td>POINT (-78.44200 -1.46700)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2010</td>
      <td>Eyjafjallajokull</td>
      <td>Iceland</td>
      <td>63.630</td>
      <td>-19.620</td>
      <td>Stratovolcano</td>
      <td>POINT (-19.62000 63.63000)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2010</td>
      <td>Pacaya</td>
      <td>Guatemala</td>
      <td>14.381</td>
      <td>-90.601</td>
      <td>Complex volcano</td>
      <td>POINT (-90.60100 14.38100)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2010</td>
      <td>Sarigan</td>
      <td>United States</td>
      <td>16.708</td>
      <td>145.780</td>
      <td>Stratovolcano</td>
      <td>POINT (145.78000 16.70800)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2010</td>
      <td>Karangetang [Api Siau]</td>
      <td>Indonesia</td>
      <td>2.780</td>
      <td>125.480</td>
      <td>Stratovolcano</td>
      <td>POINT (125.48000 2.78000)</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>58</th>
      <td>2018</td>
      <td>Kilauea</td>
      <td>United States</td>
      <td>19.425</td>
      <td>-155.292</td>
      <td>Shield volcano</td>
      <td>POINT (-155.29200 19.42500)</td>
    </tr>
    <tr>
      <th>59</th>
      <td>2018</td>
      <td>Kadovar</td>
      <td>Papua New Guinea</td>
      <td>-3.620</td>
      <td>144.620</td>
      <td>Stratovolcano</td>
      <td>POINT (144.62000 -3.62000)</td>
    </tr>
    <tr>
      <th>60</th>
      <td>2018</td>
      <td>Ijen</td>
      <td>Indonesia</td>
      <td>-8.058</td>
      <td>114.242</td>
      <td>Stratovolcano</td>
      <td>POINT (114.24200 -8.05800)</td>
    </tr>
    <tr>
      <th>61</th>
      <td>2018</td>
      <td>Kilauea</td>
      <td>United States</td>
      <td>19.425</td>
      <td>-155.292</td>
      <td>Shield volcano</td>
      <td>POINT (-155.29200 19.42500)</td>
    </tr>
    <tr>
      <th>62</th>
      <td>2018</td>
      <td>Aoba</td>
      <td>Vanuatu</td>
      <td>-15.400</td>
      <td>167.830</td>
      <td>Shield volcano</td>
      <td>POINT (167.83000 -15.40000)</td>
    </tr>
  </tbody>
</table>
<p>63 rows × 7 columns</p>
</div>



#### Evaluation:

```python
transformed_geo_df = pipe.evaluate(geo_df)
```

#### Transformed data:

```python
transformed_geo_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Year</th>
      <th>Name</th>
      <th>Country</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Type</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>6</th>
      <td>2010</td>
      <td>Merapi</td>
      <td>Indonesia</td>
      <td>-7.542</td>
      <td>110.442</td>
      <td>Stratovolcano</td>
      <td>POINT (110.44200 -7.54200)</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2010</td>
      <td>Tengger Caldera</td>
      <td>Indonesia</td>
      <td>-7.942</td>
      <td>112.950</td>
      <td>Stratovolcano</td>
      <td>POINT (112.95000 -7.94200)</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2011</td>
      <td>Merapi</td>
      <td>Indonesia</td>
      <td>-7.542</td>
      <td>110.442</td>
      <td>Stratovolcano</td>
      <td>POINT (110.44200 -7.54200)</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2013</td>
      <td>Merapi</td>
      <td>Indonesia</td>
      <td>-7.542</td>
      <td>110.442</td>
      <td>Stratovolcano</td>
      <td>POINT (110.44200 -7.54200)</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2013</td>
      <td>Paluweh</td>
      <td>Indonesia</td>
      <td>-8.320</td>
      <td>121.708</td>
      <td>Stratovolcano</td>
      <td>POINT (121.70800 -8.32000)</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2013</td>
      <td>Paluweh</td>
      <td>Indonesia</td>
      <td>-8.320</td>
      <td>121.708</td>
      <td>Stratovolcano</td>
      <td>POINT (121.70800 -8.32000)</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2013</td>
      <td>Okataina</td>
      <td>New Zealand</td>
      <td>-38.120</td>
      <td>176.500</td>
      <td>Lava dome</td>
      <td>POINT (176.50000 -38.12000)</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2014</td>
      <td>Kelut</td>
      <td>Indonesia</td>
      <td>-7.930</td>
      <td>112.308</td>
      <td>Stratovolcano</td>
      <td>POINT (112.30800 -7.93000)</td>
    </tr>
    <tr>
      <th>39</th>
      <td>2015</td>
      <td>Manam</td>
      <td>Papua New Guinea</td>
      <td>-4.100</td>
      <td>145.061</td>
      <td>Stratovolcano</td>
      <td>POINT (145.06100 -4.10000)</td>
    </tr>
    <tr>
      <th>41</th>
      <td>2015</td>
      <td>Okataina</td>
      <td>New Zealand</td>
      <td>-38.120</td>
      <td>176.500</td>
      <td>Lava dome</td>
      <td>POINT (176.50000 -38.12000)</td>
    </tr>
    <tr>
      <th>45</th>
      <td>2016</td>
      <td>Rinjani</td>
      <td>Indonesia</td>
      <td>-8.420</td>
      <td>116.470</td>
      <td>Stratovolcano</td>
      <td>POINT (116.47000 -8.42000)</td>
    </tr>
    <tr>
      <th>50</th>
      <td>2017</td>
      <td>Dieng Volc Complex</td>
      <td>Indonesia</td>
      <td>-7.200</td>
      <td>109.920</td>
      <td>Complex volcano</td>
      <td>POINT (109.92000 -7.20000)</td>
    </tr>
    <tr>
      <th>52</th>
      <td>2017</td>
      <td>Aoba</td>
      <td>Vanuatu</td>
      <td>-15.400</td>
      <td>167.830</td>
      <td>Shield volcano</td>
      <td>POINT (167.83000 -15.40000)</td>
    </tr>
    <tr>
      <th>53</th>
      <td>2017</td>
      <td>Merapi</td>
      <td>Indonesia</td>
      <td>-7.542</td>
      <td>110.442</td>
      <td>Stratovolcano</td>
      <td>POINT (110.44200 -7.54200)</td>
    </tr>
    <tr>
      <th>55</th>
      <td>2018</td>
      <td>Kadovar</td>
      <td>Papua New Guinea</td>
      <td>-3.620</td>
      <td>144.620</td>
      <td>Stratovolcano</td>
      <td>POINT (144.62000 -3.62000)</td>
    </tr>
    <tr>
      <th>59</th>
      <td>2018</td>
      <td>Kadovar</td>
      <td>Papua New Guinea</td>
      <td>-3.620</td>
      <td>144.620</td>
      <td>Stratovolcano</td>
      <td>POINT (144.62000 -3.62000)</td>
    </tr>
    <tr>
      <th>60</th>
      <td>2018</td>
      <td>Ijen</td>
      <td>Indonesia</td>
      <td>-8.058</td>
      <td>114.242</td>
      <td>Stratovolcano</td>
      <td>POINT (114.24200 -8.05800)</td>
    </tr>
    <tr>
      <th>62</th>
      <td>2018</td>
      <td>Aoba</td>
      <td>Vanuatu</td>
      <td>-15.400</td>
      <td>167.830</td>
      <td>Shield volcano</td>
      <td>POINT (167.83000 -15.40000)</td>
    </tr>
  </tbody>
</table>
</div>



The power of this work is in its reproducibility and scalablilty.

## Credits

- Logo art from "Vecteezy.com"
- Demo data from "Kaggle.com"
