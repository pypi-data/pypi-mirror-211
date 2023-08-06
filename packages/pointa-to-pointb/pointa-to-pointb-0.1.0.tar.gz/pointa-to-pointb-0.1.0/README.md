# Description

This package helps to calculate spatial and euclidean distance between two points of interest, say Point A and Point B.



# How to Use

### For calculating Geo spatial distance between two points in space.

`Inputs` : Latitude and Longitude pairs for Point A and Point B.
`Output` : distance in meters between the two sets of coordinates

```code
from pointa_to_pointb import geo_distance

longA = 52.370216
latA = 4.895168
longB = 52.520008
latB = 13.404954

geometrical_distance = geo_distance.haversine(longA, latA, longB, latB)
print(geometrical_distance)

``` 

### For calculating Geo spatial distance between two bounding boxes.

`Inputs` : Bounding box coordinates (top left and bottom right) for for Point A and Point B pairs .
`Output` : nanhattan distance inbetween the two sets of coordinates representing two bounding boxes

```code 
from pointa_to_pointb import bbox_distance

bbox1 = (20, 21, 25, 18)
bbox2 = (55, 55, 100, 10)

manh_distance = bbox_distance.manhanttan_distance(bbox1, bbox2)
print(manh_distance)

gap_distance = bbox_distance.gap_distance(bbox1, bbox2)
print(gap_distance)


```