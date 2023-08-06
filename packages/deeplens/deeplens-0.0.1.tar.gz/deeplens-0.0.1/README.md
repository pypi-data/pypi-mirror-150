# deeplens
A simple parser written in python for [Amazon Deeplens](https://aws.amazon.com/deeplens/).

This simple parser allows for Amazon Deeplens owners to easily
parse their downloaded data from the MQTT test client.

## Usage 
```python3
import deeplens

with open("subscription.json", "r") as sub:
    sub = sub.read()

deeplens = deeplens.dlens(sub)
```

The data then can be parsed 3 different ways using the different
download types featured: JSON, strings, raw.

## Classs Methods
```python3
dlens.face()       #returns an array containing chance of face data.
dlens.max()        #maxium chance of face.
dlens.min()        #minium chance of face.
dlens.avg()        #average chance of face total.
dlens.timestamps() #list containing timestamps logged.
dlens.format()     #formatting type returns python object type dict, str, or bytes.
dlens.topic()      #topic id set
dlens.qos()        #Quality of Service returns a bool.
```
