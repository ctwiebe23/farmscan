import shapefile
from pprint import pprint

sf = shapefile.Reader("./app/data/soilmu_a_ne175")

shapes = sf.shapes()
records = sf.records()

total_width = 0
total_height = 0

max_width = 0
min_width = float('inf')
max_height = 0
min_height = float('inf')

for (shape, record) in zip(shapes, records):
  width = shape.bbox[2] - shape.bbox[0]
  height = shape.bbox[3] - shape.bbox[1]
  
  total_width += width
  total_height += height
  
  if width > max_width:
    max_width = width
  elif width < min_width:
    min_width = width
  
  if height > max_height:
    max_height = height
  elif height < min_height:
    min_height = height
    
num_shapes = len(shapes)
avg_width = total_width / num_shapes
avg_height = total_height / num_shapes

pprint({
  "max width": max_width,
  "min width": min_width,
  "avg width": avg_width,
  "max height": max_height,
  "min height": min_height,
  "avg height": avg_height,
})