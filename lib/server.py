from pathlib import Path
from dosya import *

class Server(Object):
    def __init__(self,folder):
        self.publishKlasor=Klasor(folder)


