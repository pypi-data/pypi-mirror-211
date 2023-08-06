from .converter import TikaConverterService, LocalConverterService

class ConverterFactory():

    @staticmethod
    def buildConverter(converter_info):
        tika_server_url=converter_info['server_url'] if converter_info['name'] =='TIKA' else None
        return TikaConverterService(tika_server_url=tika_server_url) if tika_server_url else LocalConverterService()
