from StrangeSerializer_for_lab_3.StrangeXML.StrangeXmlSerializer import StrangeXmlSerializer
from StrangeSerializer_for_lab_3.StrangeJSON.StrangeJsonSerializer import StrangeJsonSerializer


class StrangeSerializer:
    @staticmethod
    def create_strange_serializer(serializer_type):
        if serializer_type == 'json':
            return StrangeJsonSerializer
        elif serializer_type == 'xml':
            return StrangeXmlSerializer
        else:
            raise Exception("Error in serializer type")
