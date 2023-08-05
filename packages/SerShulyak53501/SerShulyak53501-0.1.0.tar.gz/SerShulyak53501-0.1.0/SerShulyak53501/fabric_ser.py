from SerKosach153501.xml_ser import XMLSerializer
from SerKosach153501.json_ser import JsonSerializer


class Fabric:
    
    @staticmethod
    def create_serializer(format_name : str):
        format_name = format_name.lower()
        
        if (format_name == "json"):
            return JsonSerializer()
        elif (format_name == "xml"):
            return XMLSerializer()
        else:
            raise ValueError