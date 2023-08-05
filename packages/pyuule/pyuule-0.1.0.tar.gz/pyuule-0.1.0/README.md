# pyuule

UULE's are Google's objects for referencing locations. This Python library allows you to encode and encode UULE's!

## What is a UULE anyway?

There are two forms of UULE. The first type, prefixed by a 'w+':
```
w+CAIQICIhTm90dGluZ2hhbSxFbmdsYW5kLFVuaXRlZCBLaW5nZG9t
```
can be used to direct searches to a specific location. The "canonical location" name must be drawn from Google's [list of place names](https://developers.google.com/google-ads/api/data/geotargets). A search on Google can then be done with results drawn from the area around this location with a UULE query parameter added, for e.g. the following search is scoped to results near the location of Nottingham in the UK:
[www.google.com/search?q=restaurants&uule=w+CAIQICIhTm90dGluZ2hhbSxFbmdsYW5kLFVuaXRlZCBLaW5nZG9t](http://www.google.com/search?q=restaurants&uule=w+CAIQICIhTm90dGluZ2hhbSxFbmdsYW5kLFVuaXRlZCBLaW5nZG9t)

The second type of UULE is often attached to cookies from Google, for e.g.:
```
a+cm9sZToxCnByb2R1Y2VyOjEyCnByb3ZlbmFuY2U6MAp0aW1lc3RhbXA6MTY4MDg3NzkwNjIzNjczNgpsYXRsbmd7CmxhdGl0dWRlX2U3OjMwMjY2NjY2MApsb25naXR1ZGVfZTc6LTk3NzMzMzMwMAp9CnJhZGl1czotMQo
```
These encode some metadata, but most interestingly, the radius over which to search, and the latitude and longitude of the searcher.

## Usage

This library allows you to encode and decode query parameter UULE's:

```python3
>>> import pyuule

>>> pyuule.decode_w("w+CAIQICImV2VzdCBOZXcgWW9yayxOZXcgSmVyc2V5LFVuaXRlZCBTdGF0ZXM")
"Nottingham,England,United Kingdom"

>>> pyuule.encode_w("Saint-Germain-des-Pres,Ile-de-France,France")
"w+CAIQICIrU2FpbnQtR2VybWFpbi1kZXMtUHJlcyxJbGUtZGUtRnJhbmNlLEZyYW5jZQ"
```

and additionaly allows you to decode cookie UULEs:
```python3
>>> pyuule.decode_a("a+cm9sZToxCnByb2R1Y2VyOjEyCnByb3ZlbmFuY2U6MAp0aW1lc3RhbXA6MTY4MDg3NzkwNjIzNjczNgpsYXRsbmd7CmxhdGl0dWRlX2U3OjMwMjY2NjY2MApsb25naXR1ZGVfZTc6LTk3NzMzMzMwMAp9CnJhZGl1czotMQo")
{
    "role": 1,
    "producer": 12,
    "provenance": 0,
    "timestamp": 1680877906236736,
    "latitude": 3.0266666,
    "longitude": -9.77333300,
    "radius": -1,
:   
```


## Acknowledgements

The following blog post was helpful in writing this library:
https://valentin.app/uule.html
