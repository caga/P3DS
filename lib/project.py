from dosya import *
from anytree import Node, RenderTree
class Project:
    def __init__(self,projectFolder=None):
        self.project=Klasor(projectFolder)
        # self.documentRoot=Klasor(documentRoot)
        self.parts=self.project.klasorler()
        self.node=Node(self.project.name)
    def createOrLoad(self,projectFolder):
        self.project=Klasor(projectFolder)
        self.parts=self.projectFolder.klasorler()
    def createPart(self,part):
        self.parts.append(part)
    def deletePart(self,part):
        path2Part=Path()
        path2Part=self.project.path / part
    def tree(self):
        self.project.tree()
