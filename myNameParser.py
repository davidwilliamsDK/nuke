import re
import sys
import os
import nuke

class nameParser():
    def __init__(self, filePath):
        
        
        
        #nukeScripts =  os.path.dirname ( nuke.root().knob("name").getValue() )

        
        #print renderPath
        
        #GET CURRENT COMPNAME AND COMPPATH
        compPath, compName = os.path.split(nuke.root().name())
        filePath = os.path.join(compPath,compName)
       
   
        RenderPath = compPath.replace('nukeScripts','compOut')
        
        #Set RoyalRenderPath
        winRoyalRender = r'\\vfx-render-manager\royalrender\bin\win\rrSubmitterconsole.exe'
        linuxRoyalRender ='/mnt/rrender/bin/lx64/rrSubmitterconsole'
       
        
        self.filePath = filePath
        self.fileName = compName
        self.renderPath = RenderPath
        self.scriptDir = compPath
        self.compOutName = None
        self.compOutFolder = None
        self.writeOutName = None
        self.product = None
        self.projectName = None
        self.vendor = None
        self.seqName = None
        self.shotName = None
        self.version = None
        self.type = None
        self.note = None
        self.farmNum = None
        self.sig = None
        self.serverName = 'vfx-data-server\dsPipe'
        self.serverShare = "P"
        self.renderServerName = 'vfx-data-server\dsPipe'
        self.application = None
        self.firstDir = None
        self.windowRender = winRoyalRender
        self.linuxRender = linuxRoyalRender

        #USE REG EXPR TO CHECK COMPNAME AND POPULATE
        match = re.match('^(\w+)_(\w+)_(\w+)_(\w+)_(v\d+)_(\w+)_(\w+)_(\w+)\.nk',self.fileName)
        if match:
            self.vendor, self.product, self.seqName, self.shotName, self.version, self.type, self.note, self.sig = match.groups()
            print match.groups()

        
    def rrPath(self):
        
        if sys.platform == "linux2":
           
            self.WinRRPath = r"\\vfx-render-manager\royalrender\bin\win\rrSubmitterconsole.exe"
        else:
            self.RRPath = r"\\vfx-render-manager\royalrender\bin\win\rrSubmitterconsole.exe"
            
        return 
       


