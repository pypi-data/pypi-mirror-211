from Am_serializer.json_utils import Json
from Am_serializer.xml_utils import Xml

class Ser:
    @staticmethod
    def createSerializer(format):
        if format == ".json":
            return Json()

        elif format == ".xml":
            return Xml()

        else:
            raise Exception("Wrong format")    