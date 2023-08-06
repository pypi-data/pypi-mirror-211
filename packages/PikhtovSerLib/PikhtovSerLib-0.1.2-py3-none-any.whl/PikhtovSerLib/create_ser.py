from PikhtovSerLib.json_serealazer import JsonSerelizator
from PikhtovSerLib.xml_serealazer import XMLSerelizator

class Choice:

    @staticmethod
    def create_serializer(formatt: str):
        format_name = formatt.lower()
        if format_name == 'xml':
            return XMLSerelizator()
        elif format_name == 'json':
            return JsonSerelizator()
        else:
            raise ValueError






