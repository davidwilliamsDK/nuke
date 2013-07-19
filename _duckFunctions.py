import nuke
import re, os, sys
import myNameParser as fileNameParser


padding = 4

def updateSavers(nameParser = None): 

    if nameParser == None:
        nameParser = fileNameParser.nameParser(nuke.root().name()) 
    renderBasePath = r"%s" % (nameParser.renderPath)
    print '***********running update savers***************'
    print 'renderBasePath ' + renderBasePath

    #if sys.platform == "linux2":
        #renderBasePath = renderBasePath.replace("//%s/" % nameParser.renderServerName, "/mnt/nfs/%s/" % nameParser.renderServerName)

    
    #FIND ALL THE "LEGAL" WRITE NODES _duckSaver
    
    for node in nuke.allNodes("Write"):
         match = re.match('(\w+)(duckSaver)$', node.name())
         fileType = node['file_type'].value()
         if fileType == " ":
         
             nuke.message('You must chose *File Type* on the duckSaver')
             
             return False
         
         else:
             
             if match:
                 element = match.group(1)
                 type = match.group(2)
    
                 print  'element ' + element
                 print  'type ' + type
    
                 if element == "main_":
                     basePath = r"%s/%s/" % (renderBasePath,nameParser.version)
                     print "MAIN basePath " + basePath
                     node['file'].setValue("%s/%s_%s_%s_comp.%%0%dd.%s" % (basePath, nameParser.product, nameParser.seqName, nameParser.shotName,padding, fileType))

                 else:
                     elementPath = renderBasePath.replace("compOut", "2dElements")
                     basePath = elementPath
                     print 'element' +  basePath
                     node['file'].setValue("%s/%s/%s/%s%s_%s_%s_2dElement.%%0%dd.%s" % (basePath,element,nameParser.version, element, nameParser.seqName, nameParser.shotName, nameParser.version, padding, fileType))

                 if not os.path.exists(os.path.dirname(node['file'].value())):
                     print 'making folders'
                     os.makedirs(os.path.dirname(node['file'].value()))

                 return True

#updateSavers()

def deleteFrames(deleteRangeArray):
    for node in nuke.allNodes("Write"):
        match = re.match('(\w+)(duckSaver)$', node.name())
        fileType = node['file_type'].value()
        delete = False
        
        if fileType == " ":
            return False
        if match and not node['disable'].value():
            if node.knobs().has_key('deleteFrames'):
                if node['deleteFrames'].value():
                    delete = True
                else:
                    print("Skip deleting frames")
            else:
                delete = True
        else:
            print("Error")
        
        if delete:
            for frame in deleteRangeArray:
                deleteFrame = node['file'].value().replace("%%0%dd" % padding, eval("'%%0%dd'" % padding) % (frame))
                if os.path.exists(deleteFrame):
                    os.unlink(deleteFrame)





    

