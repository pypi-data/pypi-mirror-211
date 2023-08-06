from StrangeSerializerLab3.StrangeXML import StrangeXmlSerializer
from StrangeSerializerLab3.StrangeJSON import StrangeJsonSerializer


class StrangeSerializer:
    @staticmethod
    def create_strange_serializer(serializer_type):
        if serializer_type == 'json':
            return StrangeJsonSerializer
        elif serializer_type == 'xml':
            return StrangeXmlSerializer
        else:
            raise Exception("Error in serializer type")
