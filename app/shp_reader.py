import shapefile
import sqlite3

sf = shapefile.Reader("data/soilmu_a_ne175.shp")
conn = sqlite3.connect('db/soil_data.sqlite')
cursor = conn.cursor()

shapes = sf.shapes()
records = sf.records()

enclosedShapes = shapefile.ShapeRecords([])

for (shape, record) in zip(shapes, records):
    if shapefile.bbox_contains(sf.bbox, shape.bbox):
        sR = shapefile.ShapeRecord(shape, record)
        enclosedShapes.append(sR)
        
for shapefile.ShapeRecord in enclosedShapes:
    query = "select tfact from joined_layer where mukey = ?"
    mukey = shapefile.ShapeRecord.record[3]
    if mukey is None:
        print("no mukey found")
    else:
        qResult = cursor.execute(query, (mukey,))
        result = qResult.fetchone()
        tfact = result[0]
        
        if result is None:
            print("invalid query")
        elif (tfact is None):
            print(shapefile.ShapeRecord.record[3])
        elif (not tfact):
            print("no value :(")
        else:
            if int(tfact) > 4:
                print("yay!")
            else:
                print("aw")
        
        
        