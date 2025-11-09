import shapefile
import sqlite3

sf = shapefile.Reader("../data/soilmu_a_ne175.shp")
conn = sqlite3.connect('../db/soil_data.sqlite')
cursor = conn.cursor()

shapes = sf.shapes()
records = sf.records()

enclosedShapes = shapefile.ShapeRecords([])

for (shape, record) in zip(shapes, records):
    if shapefile.bbox_contains(sf.bbox, shape.bbox):
        sR = shapefile.ShapeRecord(shape, record)
        enclosedShapes.append(sR)
        
maxViabilityScore = 0;
viableShapes = shapefile.ShapeRecords([])
for shapefile.ShapeRecord in enclosedShapes:
    viabilityScore = 0;
    query = "select tfact,flodfreqdcd,iccdcdpct,ph1to1h2o_r,pi_r,om_r from joined_layer where mukey = ?"
    mukey = shapefile.ShapeRecord.record[3]
    
    if mukey is None:
        print("no mukey found")
    else:
        qResult = cursor.execute(query, (mukey,))
        result = qResult.fetchone()
        tfact = result[0]
        floodfreq = result[1]
        soilCapability = result[2]
        pHLevel = result[3]
        pIndex = result[4]
        organicMatter = result[5]
        
        if result is None:
            print("invalid query")
        elif (tfact is None):
            print(shapefile.ShapeRecord.record[3])
        elif (tfact):
            if int(tfact) > 4:
                viabilityScore += 1
        
        if isinstance(floodfreq, str):
            if floodfreq == "None" or floodfreq == "Occasional":
                viabilityScore += 1
                 
        if isinstance(soilCapability, int):
            viabilityScore -= int(soilCapability) / 100
        
        if (pHLevel is not None and pHLevel):
            if isinstance(float(pHLevel), float):
                if (float(pHLevel) > 6 and float(pHLevel) < 7.5):
                    if (float(pHLevel) <= 6.8):
                        viabilityScore += 1
                    viabilityScore += 1
        
        if (pIndex is not None and pIndex):
            if isinstance(float(pIndex), float):
                if (float(pIndex) > 15 and float(pIndex) < 35):
                    viabilityScore += 1
        
        if (organicMatter is not None and organicMatter):
            if isinstance(float(organicMatter), float):
                if (float(organicMatter) >= 3 and float(organicMatter) <= 6):
                    viabilityScore += 1
        
        if viabilityScore < 0:
            viabilityScore = 0
        if viabilityScore > maxViabilityScore:
            maxViabilityScore = viabilityScore
            viableShapes.clear()
            viableShapes.append(shapefile.ShapeRecord)
        elif viabilityScore == maxViabilityScore:
            viableShapes.append(shapefile.ShapeRecord)
            
print(maxViabilityScore)
print(len(viableShapes))