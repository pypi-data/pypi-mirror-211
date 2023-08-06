from Brigada.json_utils import Json
from Brigada.xml_utils import Xml

class Brigada:
    @staticmethod
    def createSerializer(format):
        if format == ".json":
            return Json()

        elif format == ".xml":
            return Xml()

        else:
            raise Exception("Wrong format")    