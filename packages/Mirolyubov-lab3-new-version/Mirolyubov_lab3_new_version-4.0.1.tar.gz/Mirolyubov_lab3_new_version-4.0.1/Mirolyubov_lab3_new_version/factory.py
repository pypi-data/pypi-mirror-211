from Mirolyubov_lab3_new_version.json_serializer import Json
from Mirolyubov_lab3_new_version.xml_serializer import Xml


class Factory:
    @staticmethod
    def create_serializer(format):
        if format == ".json":
            return Json()

        elif format == ".xml":
            return Xml()

        else:
            raise Exception("Unknown type of serialization")
