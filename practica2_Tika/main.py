from tikapp import TikaApp

class Tika:
    detect_content_type = None
    detect_language = None
    extract_all = None
    extract_content = None
    def __init__(self, file_path):
        self.file_path = file_path
        self.tika_client = TikaApp(file_jar='tika-app-1.16.jar')
        
    def TikaReader(self):
        self.detect_content_type = self.tika_client.detect_content_type(self.file_path)
        print(self.detect_content_type)
        self.detect_language = self.tika_client.detect_language(self.file_path)
        print(self.detect_language)
        self.extract_all = self.tika_client.extract_all_content(self.file_path, convert_to_obj=True)
        print(self.extract_all)
        self.extract_content = self.tika_client.extract_only_content(self.file_path)
        print(self.extract_content)
        
    def ProcessJSONTika(json):
        #Dado el JSON de procesamiento Tika escribir por consola los metadatos sobre
        #autores, fecha de creación y fecha de modificación.
        pass
    
if __name__ == "__main__":
    tika = Tika('Guion_De_Eficacia_proyecto_final[1].docx')
    tika.TikaReader()