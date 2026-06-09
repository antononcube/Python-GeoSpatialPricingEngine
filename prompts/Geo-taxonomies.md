# Geo taxonomies 

Prompts for creation, ingestion, and plotting Geo-taxonomies.

---

## Geo-taxonomy ingestion

See the notebook ["Geo-taxonomy-ingestion.ipynb"](../notebooks/Jupyter/Geo-taxonomy-ingestion.ipynb).
The Geo-taxonomy JSON file was created with the Wolfram Language package 
[GeoTileTaxonomy.m](https://github.com/antononcube/SystemModeling/blob/master/WL/GeoTileTaxonomy.m), [AAp1].

### Ingestion

In the Python notebook "./notebooks/Jupyter/Geo-taxonomy-ingestion.ipynb" ingest the JSON file "./resources/Hextile1deg.json" 
that is an array of dictionaries. The column "Coordinates" has JSON string of polygon coordinates.

### Plot

Translate from Mathematica to Python using "plotly":

```mathematica
Graphics[{FaceForm[{Gray, Opacity[0.3]}], EdgeForm[White], 
  Polygon/@df["PolygonCoordinates"]}, ImageSize -> 1000]
```

---

## References

[AAp1] Anton Antonov, [GeoTileTaxonomy.m](https://github.com/antononcube/SystemModeling/blob/master/WL/GeoTileTaxonomy.m), (2022-2026), [SystemModeling at GitHub](https://github.com/antononcube/SystemModeling).