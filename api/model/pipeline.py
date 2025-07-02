import joblib

class Pipeline:
    
    def __init__(self):
        """Inicializa o pipeline"""
        self.pipeline = None
    
    def carrega_pipeline(self, path):
        """Carrega o pipeline salvo com joblib"""
        self.pipeline = joblib.load(path)
        return self.pipeline
