import json as _json


class dlens(object):
    '''deeplens
    Parse Amazon AWS deeplens json, string, and hexadecimal data.
    '''
    def __init__(self, d):
        self.__d = _json.loads(d)

    @property
    def qos(self):
        '''
        Return Quality of Service boolean value from deeplens json.
        '''
        qualityOfService = self.__d["qos"]
        return bool(qualityOfService)

    @property
    def topic(self):
        '''
        Return topicFilter from deeplens json.
        '''
        topic = self.__d["topicFilter"]
        return topic

    @property
    def format(self):
        '''
        Return format type as python class from first avaiable parsed key.
        '''
        topic0 = self.__d["messages"][0]["format"]
        if topic0 == "string":
            return str
        elif topic0 == "raw":
            return bytes
        return dict

    @property
    def timestamps(self):
        '''
        Return timestamps as integer array from deeplens json.
        '''
        stampArray = []
        for arrayLength in range(len(self.__d["messages"])):
            stampArray.append(self.__d["messages"][arrayLength]["timestamp"])
        return stampArray

    @property
    def avg(self):
        '''
        Returns the average of the total amount of percentage chance of face.
        '''
        averagePercent = 0.00
        for total in self.face(precise=False):
            averagePercent += total
        
        averagePercent = averagePercent / len(self.face(precise=True))
        return averagePercent

    def min(self, precise=True):
        '''
        Return the minium percentage chance of face as float unless precise is False.
        '''
        if not precise:
            miniumChance = min(self.face(precise=False))
        else:
            miniumChance = min(self.face(precise=True))
        return miniumChance

    def max(self, precise=True):
        '''
        Return the maxium percentage chance of face as float unless precise is False.
        '''
        if not precise:
            maxiumChance = max(self.face(precise=False))
        else:
            maxiumChance = max(self.face(precise=True))
        return maxiumChance

    def face(self, precise=True):
        '''
        Return float array of chance of face or use whole precentage numbers.
        '''
        faceArray = []
        facePercentage = []
        faceStrPercentage = []
        faceRawPercentage = []

        for arrayLength in range(len(self.__d["messages"])):
            faceArray.append(self.__d["messages"][arrayLength]["payload"])

        if self.format == dict:
            for dictionary in faceArray:
                try:
                    if not precise:
                        facePercentage.append(round(dictionary["face"] * 100))
                    else:
                        facePercentage.append(dictionary["face"])
                except KeyError:
                    continue
        elif self.format == str:
            for dictionary in faceArray:
                facePercentage.append(_json.loads(dictionary))
            
            for i in range(len(facePercentage)):
                try:
                    if not precise:
                        faceStrPercentage.append(round(facePercentage[i]["face"] * 100))
                    else:
                        faceStrPercentage.append(facePercentage[i]["face"])
                except KeyError:
                    continue
            
        elif self.format == bytes:
            for dictionary in faceArray:
                facePercentage.append(json.loads(bytes.fromhex(dictionary)))

            for i in range(len(facePercentage)):
                try:
                    if not precise:
                        faceRawPercentage.append(round(facePercentage[i]["face"] * 100))
                    else:
                        faceRawPercentage.append(facePercentage[i]["face"])
                except KeyError:
                    continue

        if self.format == str:
            return faceStrPercentage
        elif self.format == bytes:
            return faceRawPercentage
        return facePercentage
