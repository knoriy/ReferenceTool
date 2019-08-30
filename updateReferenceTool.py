import maya.cmds as mc
import os
import subprocess
from functools import partial


class UpdateReference:

    def __init__(self, *args):
        self.updateReferenceWinID = "UpdateReference"
        self.windowWidth = 700
        self.windowHeight = 30
        
        self.updateReferenceGreen = (0.3, 0.50, 0.40)
        self.updateReferenceGrey = (0.3, 0.3, 0.3)
        
        self.createGUI()

    def createGUI(self, *args):    

        if mc.window(self.updateReferenceWinID, exists=True):
            mc.deleteUI(self.updateReferenceWinID, wnd=True)

        mc.window(self.updateReferenceWinID, s=False, tlb=True, t="UpdateReference v1.0")
        mc.columnLayout(adj=True)

        mc.rowLayout(nc=2)
        mc.text(l='', w=self.windowWidth-30, h=10)
        
        mc.symbolButton(image='nodeGrapherModeAllLarge.png', w=25, h=25, c=lambda _:AboutClass())
        
        mc.setParent(top=True) 

        ######################################## toggleable tab ########################################

        referencedFiles =self.getReferenced()
        numberOfReferencedFiles = len(referencedFiles)

        if numberOfReferencedFiles == 0:
            mc.button(l='Currently there are not References in your scene', bgc=self.updateReferenceGreen, en=False, h=50, w=100)
        else:
            for currentReference in referencedFiles:
                updatedReferenceFile = self.checkForUpdatedReference(currentReference)
                if currentReference == updatedReferenceFile:
                    colour = self.updateReferenceGreen
                else:
                    colour = self.updateReferenceGrey
                mc.rowLayout(nc=4)
                mc.button(l="Open:     " + updatedReferenceFile, bgc=colour, c=partial(self.openFileDir, updatedReferenceFile), h=30, w=400)
                mc.button(l="Reload", bgc=colour, c=partial(self.reloadReference, currentReference), h=30, w=100)
                mc.button(l="Remove", bgc=colour, c=partial(self.removeReference, currentReference), h=30, w=100)
                mc.button(l="Update", bgc=colour, c=partial(self.updateReference, currentReference, updatedReferenceFile), h=30, w=100)
                mc.setParent(top=True)
            
        ######################################## toggleable tab ########################################
        mc.text(l='', h=10)
        
        mc.rowLayout(nc=4)
        mc.button(l="Open Reference Editor", bgc=self.updateReferenceGrey, c=partial(mc.ReferenceEditor), h=30, w=350)
        mc.button(l="Load Reference", bgc=self.updateReferenceGrey, c=partial(self.createReference), h=30, w=350)
        mc.setParent(top=True)

        mc.text(l='', h=10)
        mc.button(l="Refresh", bgc=self.updateReferenceGrey, c=partial(self.createGUI), h=30)
        mc.setParent(top=True)

        if numberOfReferencedFiles == 0:
            mc.showWindow(self.updateReferenceWinID)
            mc.window(self.updateReferenceWinID, e=True, w=self.windowWidth, h=170)
        else:
            mc.showWindow(self.updateReferenceWinID)
            mc.window(self.updateReferenceWinID, e=True, w=self.windowWidth, h=self.windowHeight*numberOfReferencedFiles+120)

    def getReferenced(self, *args):
        return sorted(mc.file(query=True, r=True, withoutCopyNumber=True))
    
    def checkForUpdatedReference(self, referencedFile, *args):
        if (len(referencedFile) > 1):
            fileName = referencedFile.split('.')[0]
            fileName = os.path.split(fileName)

            fileArray = []

            for file in os.listdir(os.path.split(referencedFile)[0]):
                if file.endswith(('.mb','.ma','.abc')) and fileName[-1] in file:
                    fileArray.append(file)
                fileArray = sorted(fileArray)
            finalPath = os.path.join(os.path.split(referencedFile)[0], fileArray[-1])

            return finalPath.replace("\\","/")

    def updateReference(self, currentReference, updatedReference, *args):
        currentReference =  mc.referenceQuery(currentReference, rfn=True)
        mc.file(updatedReference, loadReference=currentReference)
        self.createGUI()
    
    def removeReference(self, currentReference, *args):
        result = mc.confirmDialog( title='Remove Reference', message='Removing the following reference is undoable.', button=['Remove','Cancel'], defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
        if result == "Remove":
            mc.file(currentReference, removeReference=True)
            self.createGUI()

    def reloadReference(self, currentReference, *args):
        mc.file(currentReference, loadReference=currentReference)
        self.createGUI()
    
    def createReference(self, *args):
        referenceFileDir = mc.fileDialog2(fileMode=1, caption="Load Reference")
        mc.file(referenceFileDir[0], reference=True)
        self.createGUI()

    def openFileDir(self, refPath, *args):
        refPath	= refPath.replace('/', '\\')
        subprocess.Popen('explorer "%s"' % refPath)


if __name__ == "__main__":
    a = UpdateReference()


class AboutClass:

    def __init__(self):
        self.aboutMeWinID = "aboutMe"
        self.aboutMeGUI()

    def aboutMeGUI(self):    
        if (mc.window(self.aboutMeWinID, exists=True)):
            mc.deleteUI(self.aboutMeWinID, wnd=True)

        mc.window(self.aboutMeWinID, s=False, tlb=True, t="About me")
        mc.columnLayout(adj=True)
        
        mc.rowLayout(nc=1)
        mc.text(l='', h=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(l='<font color=#00d646><h2> Update Reference </h2></font>', al='center', w=196, h=40)
        mc.setParent('..')
        mc.rowLayout(nc=2)
        mc.text(l='Author: Kari A Noriy \nCopyright (c) 2019 Kari A Noriy', al='center', w=196, h=40)
        mc.setParent('..')
        mc.text(l='knoriy72@gmail.com', al='center', w=196, h=40)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(l='', w=11)
        mc.button(l='Website', ann="Open Kari A Noriy's website", w=170, h=30, c=partial(self.aboutMeOpenBrowser, 'Website'))
        mc.text(l='', w=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#00d646> Follow Me On: </font>', al='center', w=196, h=35)
        mc.setParent('..')
        
        mc.rowLayout(nc=4)
        mc.text(l='', w=10)
        mc.button(l='Artstation', ann="Kari A Noriy's Artstation Profile", w=85, h=30, c=partial( self.aboutMeOpenBrowser, 'Artstation'))
        mc.button(l='Facebook', ann='The Art Of Kari A Noriy on Facebook', w=85, h=30, c=partial( self.aboutMeOpenBrowser, 'Facebook'))
        mc.text(l='', w=10)
        mc.setParent(top=True)
        
        mc.showWindow(self.aboutMeWinID)
        mc.window(self.aboutMeWinID, e=True, w=200, h=265)
        
    def aboutMeOpenBrowser(self, site, *args):
        if site == 'Website':
            mc.launch(web="https://karianoriy.wixsite.com/home")
        elif site == 'Artstation':
            mc.launch(web="https://www.artstation.com/knoriy")
        elif site == 'Facebook':
            mc.launch(web="https://www.facebook.com/TheArtOfKariANoriy")