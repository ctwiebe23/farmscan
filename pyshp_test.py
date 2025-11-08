import shapefile

sf = shapefile.Reader("./app/data/soilmu_a_ne175")
print(sf.bbox)
shapes = sf.shapes()
print(len(shapes))
print(shapes[0])
records = sf.records()
print(len(records))
print(records[0].as_dict())