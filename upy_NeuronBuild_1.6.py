# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 13:09:18 2010

@author: Ludovic Autin
"""

import sys,os
#pyubic have to be in the pythonpath, if not add it
#pathtoupy = "/Users/ludo/pathtoupy/"
#sys.path.insert(0,pathtoupy)
#if you want to use numpy, numpy have to be in the pythonpath to

import numpy

import upy
upy.setUIClass()

from upy import uiadaptor
#you can import the daptor directly
#from pyubic.qtUI import qtUIDialog as uiadaptor
#from pyubic.tkUI import tkUIDialog as uiadaptor

#get the helperClass for modeling
helperClass = upy.getHelperClass()

###Create IDs for the GUI elements in the settings dialog
##DLG_GROUP_1 = 1000
##DLG_GROUP_2 = 1001
##TEXTBOX = 1002
##CANCELBUTTON = 1003
##IMPORTBUTTON = 1004
##HNCHECK = 1005
##CONNECTCHECK = 1006
##RAILCHECK = 1007
##SWEEPCHECK = 1008
##PROFILETEXT = 1009
##PROFILESIDES = 1010
##
##coordsystem="left"
##versionNumber=c4d.GetC4DVersion()

class NeuronBuildUI(uiadaptor):

    def setup(self):
        #get the helper
        #self.helper = helperClass(vi=vi)
        #dont want to dock it ie maya 
        #self.dock = False
        #initialize widget and layout
        self.w=240

        self.h=290
        self.initWidget()        
        self.setupLayout()                
        
    #dont touch theses two functions specific for c4d
    def CreateLayout(self):
        self._createLayout()
        return 1
    def Command(self,*args):
#        print args
        self._command(args)
        return 1
    def somaMake(self,somaLines, neuroFile, fileName):
        """Create splines to make the cell body."""

        #reference global variables that set model parameters
        #global DoHN, DoConnect, DoRail, DoSweep, NSides
        
        #create spline
        parent = helperClass().getObject(self.name)
    
    
##        Spline = c4d.BaseObject(c4d.Ospline)
##        
##        #add name to spline
##        Spline[c4d.ID_BASELIST_NAME] = "Soma"
##        
##        #set type to linear
##        Spline[c4d.SPLINEOBJECT_TYPE] = 0
##        
##        #set number of points for spline
##        Spline.ResizeObject(len(somaLines))

        somaL = []

        for n in range(0, len(somaLines)):
            currLine = somaLines[n]
            
            #create the variables for positioning the points
            sx = float(currLine[2])
            sy = float(currLine[3])
            sz = float(currLine[4])
            if coordsystem=="left":  #Convert to left-hand for C4D added by GJ March 11, 2013
                sz = -sz
            sRad = float(currLine[5])
            pos = c4d.Vector(sx, sy, sz)
            Spline.SetPoint(n, pos)
        
        #create the soma spline
        doc.InsertObject(Spline)
        
##        #create sweep object
##        if DoSweep == True:
##            Sweep = c4d.BaseObject(c4d.Osweep)
##            Sweep[c4d.ID_BASELIST_NAME] = "Soma Sweep"
##            Sweep[c4d.SWEEPOBJECT_CONSTANT] = False
##            Sweep[c4d.SWEEPOBJECT_RAILDIRECTION] = False
##            Sweep[c4d.CAP_TYPE] = 1
##            Sweep.SetPhong(True, True, 80)
##            Sweep.SetDeformMode(False)
##            doc.InsertObject(Sweep)
##        
##            #create the profile for the sweep
##            Profile = c4d.BaseObject(c4d.Osplinenside)
##            Profile[c4d.ID_BASELIST_NAME] = "Profile"
##            Profile[c4d.PRIM_NSIDE_RADIUS] = sRad
##            Profile[c4d.PRIM_NSIDE_SIDES] = NSides
##            doc.InsertObject(Profile)
##            
##            Spline.InsertUnder(Sweep)
##            Profile.InsertUnder(Sweep)
##            
##        #add undo for spline creation
##        doc.AddUndo(c4d.UNDOTYPE_NEW, Spline)
##
##        #insert the spline under the null object
##        if DoSweep == True:
##            parent = doc.SearchObject(fileName)
##            Sweep.InsertUnder(parent)
##                
##        c4d.EventAdd()
##                
##    def splineMake(splineLines, neuroFile, fileName):
##        """Create splines to define the dendrites and axons."""
##        
##        #reference global variables that set model parameters
##        global DoHN, DoConnect, DoRail, DoSweep, NSides
##        
##        #run through the data file, identifying contiguous spline segments. this is possible because
##        #the last value in the data refers to the "root" point of that branch segment
##        splineSep = [] 
##        for n in range(0, len(splineLines)):
##            currLine = splineLines[n]
##            sIndex = int(currLine[0])  
##            sRoot = int(currLine[6])
##            if sIndex > sRoot + 1:
##                splineSep.append(sIndex)
##                
##        #now build the spline segments as separate splines
##        for n in range(0, len(splineSep)):
##            if n < (len(splineSep) - 1):
##                
##                #determine the offset between segemnts; this is the number of vertices in each spline segment
##                offset = splineSep[n+1] - splineSep[n]
##                
##                #create an empty spline
##                Spline = c4d.BaseObject(c4d.Ospline)
##                
##                #allocate points for the spline
##                Spline.ResizeObject(offset)
##                
##                #get the data line that starts the segment
##                splineStart = neuroFile[splineSep[n]]
##                splineType = int(splineStart[1])
##                            
##                #determine what type of spline it is and name it
##                if splineType == 2: 
##                    name = "Axon " + str(n)
##                elif splineType == 3: 
##                    name = "Basal Dendrite " + str(n)
##                elif splineType == 4:
##                    name = "Apical Dendrite " + str(n)
##                    
##                Spline[c4d.ID_BASELIST_NAME] = name
##                Spline[c4d.SPLINEOBJECT_TYPE] = 0
##                
##                #find the root poiont for this segment by going back to 
##                #the line in neuroFile that contains it
##                #and then we have to step back one line in the source file
##                rootLine = neuroFile[((int(splineStart[6])) - 1)]
##                rootRoot = neuroFile[int(rootLine[6]) - 1]
##                x, y, z = float(rootRoot[2]), float(rootRoot[3]), float(rootRoot[4])
##                rootPos = c4d.Vector(x, y, z)
##                if coordsystem=="left":  #Convert to left-hand for C4D added by GJ March 11, 2013
##                    rootPos = c4d.Vector(x, y, -z)
##                Spline.SetPoint(0, rootPos)
##                
##                for m in range(1, offset):
##                    l = int(splineSep[n]) + (m - 1)
##                    currLine = neuroFile[l]
##                    
##                    #create the variables for positioning the points
##                    sx = float(currLine[2])
##                    sy = float(currLine[3])
##                    sz = float(currLine[4])
##                    if coordsystem=="left":  #Convert to left-hand for C4D added by GJ March 11, 2013
##                        sz = -sz
##                    #radius, not used yet
##                    sRad = float(currLine[5])
##                    pos = c4d.Vector(sx, sy, sz)
##                    Spline.SetPoint(m, pos)
##                
##                #create the spline
##                doc.InsertObject(Spline)
##                c4d.EventAdd()
##                
##                #in order to scale the sweepNURBs object, we create a copy of the spline
##                #to act as a rail spline, and then add the radius value to one of the coords
##                if DoRail == True:
##                    railSpline = Spline.GetClone()
##                    railSpline[c4d.ID_BASELIST_NAME] = name + " Rail"
##                    
##                    rVector = c4d.Vector((x + (float(rootRoot[5]))), y, z)
##                    if coordsystem == "left":  #Convert to left-hand for C4D added by GJ March 11, 2013
##                        rVector = c4d.Vector((x + (float(rootRoot[5]))), y, -z)
##
##                    railSpline.SetPoint(0, rVector)
##                    for m in range(1, offset):
##                        l = int(splineSep[n]) + (m - 1)
##                        currLine = neuroFile[l]
##                        
##                        #create the variables for positioning the points
##                        sRad = float(currLine[5])
##                        #add the radius to the x coord this time
##                        sx = (float(currLine[2]) + sRad)
##                        sy = float(currLine[3])
##                        sz = float(currLine[4])
##                        if coordsystem=="left":  #Convert to left-hand for C4D added by GJ March 11, 2013
##                            sz = -sz
##                        #radius, not used yet
##        
##                        pos = c4d.Vector(sx, sy, sz)
##                        railSpline.SetPoint(m, pos)
##                    
##                    doc.InsertObject(railSpline) 
##                    c4d.EventAdd()   
##                
##                #create the sweep object
##                if DoSweep == True:
##                    Sweep = c4d.BaseObject(c4d.Osweep)
##                    Sweep[c4d.ID_BASELIST_NAME] = name
##                    #the seep object needs to have two default settings disabled
##                    Sweep[c4d.SWEEPOBJECT_CONSTANT] = False
##                    Sweep[c4d.SWEEPOBJECT_RAILDIRECTION] = False
##                    Sweep[c4d.CAP_TYPE] = 1
##                    Sweep.SetPhong(True, True, 80)
##        
##                    #create the profile for the sweep
##                    Profile = c4d.BaseObject(c4d.Osplinenside)
##                    Profile[c4d.ID_BASELIST_NAME] = "Profile"
##                    Profile[c4d.PRIM_NSIDE_RADIUS] = sRad
##                    Profile[c4d.PRIM_NSIDE_SIDES] = NSides
##                    doc.InsertObject(Profile)
##                
##                #insert the splines as children of the sweepNURBs object, in the correct order
##                if DoRail == True:
##                    if DoSweep == True:
##                        railSpline.InsertUnder(Sweep)
##                if DoSweep == True:
##                    Spline.InsertUnder(Sweep)
##                    Profile.InsertUnder(Sweep)
##                
##                #add undo for spline creation
##                doc.AddUndo(c4d.UNDOTYPE_NEW, Spline)
##                
##                #insert the spline under the null object
##                if DoSweep == True:
##                    parent = doc.SearchObject(fileName)
##                    Sweep.InsertUnder(parent)
##
##                c4d.EventAdd()
##
    def readFile(self,path):
        """Access the neuromorpho swc file, strip comments, and load it into the neuroFile nested list. """

        #reference global variables that set model parameters
        #global DoHN, DoConnect, DoRail, DoSweep
        
        neuroFile = []
        somaLines = []
        splineLines = []
        
        #Get the name of the file and split off the last file extension
        filePath = os.path.basename(path)
        fileName = os.path.splitext(filePath)[0]

        #here we read the file, and create two sub lists: one for the soma, and one for the axons and dendrites
        for line in open(path):
            # ignore lines that are comments
            if line.startswith('#'):
                pass
            else:
                # create nested list of data
                 x = [value for value in line.split()]
                 neuroFile.append(x) 
                 #create 
                 if x[1] == "1":
                     somaLines.append(x)
                 else:
                     splineLines.append(x)

        #the numlines variable stores the length of the data files (number of points)
        numLines = len(neuroFile)
        
        self.name = fileName
        #create null to contain splines
        Null = helperClass().newEmpty(fileName)
##        Null[c4d.ID_BASELIST_NAME] = fileName
##        #insert the null in the scene
##        doc.InsertObject(Null)
##        #add undo for null creation
##        doc.AddUndo(c4d.UNDOTYPE_NEW, Null)
##        c4d.EventAdd()
        
        #call the functions that build the soma and other splines, if applicable
        if len(somaLines) > 0:
            self.somaMake(somaLines, neuroFile, fileName)
        #if len(splineLines) > 0:   
        #    splineMake(splineLines, neuroFile, fileName)

        return
        
##        #create connect object
##        if DoConnect == True:
##            if versionNumber >= 14000:
##                Connect = c4d.BaseObject(c4d.Oconnector)
##                Connect[c4d.ID_BASELIST_NAME] = fileName
##                #insert the connector in the scene
##                doc.InsertObject(Connect)
##            else:
##                c4d.CallCommand(1011010)
##                Connect = doc.SearchObject("Connect")
##            if Connect:
##                #add undo for Connect creation
##                doc.AddUndo(c4d.UNDOTYPE_NEW, Connect)
##                c4d.EventAdd()
##
##                Null.InsertUnder(Connect)
##        
##        #create HN object
##        if DoHN == True:
##            HN = c4d.BaseObject(c4d.Osds)   
##            HN[c4d.ID_BASELIST_NAME] = fileName
##            #insert the HyperNURBs in the scene
##            doc.InsertObject(HN)
##            #add undo for HN creation
##            doc.AddUndo(c4d.UNDOTYPE_NEW, HN)
##            c4d.EventAdd()
##            
##            if DoConnect == True: 
##                Connect.InsertUnder(HN)
##            else:
##                Null.InsertUnder(HN)
##        
##        #close out the undo stack
##        doc.EndUndo()
        

    def initWidget(self, title=None, input_text=None, id = 10):
        ## FIXME: THIS CURRENTLY SETS ACTION=NONE

        self.title = title or "NeuronBuild"
        self.menuorder = ["File","Edit","Help"]

        #menu are always define by the MENU_ID dictionary and the self.menuorder
        self.MENU_ID={"File":
            [self._addElemt(name="Recent Files",action=None,),
             self._addElemt(name="Open",action=None),
             self._addElemt(name="Save",action=None),
             self._addElemt(name="Exit",action=None)],
                "Edit" :
            [self._addElemt(name="Options",action=None)],
                "Help" :
            [self._addElemt(name="About",action=None),#self.drawAbout},
             self._addElemt(name="Help",action=None),#self.launchBrowser},
             ],
            }
        self.input_text = input_text or ""
       # self.result = None
        txt = "The NeuronBuild script imports accurate neuromorpho SWC files \n" +  "and creates spline-based geometry (scale assumes Âµm as world unit). \nChoose modeling options below;\n" + "if all boxes are unchecked, \nonly the base splines will be added to the scene.\n"

        self.TEXTAREA = {"intro":self._addElemt(id =id,name="description",value = txt, width = 200, height = 100, type = "inputStrArea", variable = self.addVariable("string",txt))}
        id = id+1
        self.CHECKBOXS ={
            "hypernurbs":self._addElemt(id=id,name="Add HyperNURBs object",width=80,height=10,
                              action=None,type="checkbox",icon=None, value = True,
                              variable=self.addVariable("int",0)),
            "connect":self._addElemt(id=id+1,name="Add Connect object",width=80,height=10, value =True,
                             action=None,type="checkbox",icon=None,
                             variable=self.addVariable("int",0)),
            "railsplines":self._addElemt(id=id+2,name="Add rail splines (controls thickness)",width=80,height=10, value = True,
                             action=None,type="checkbox",icon=None,
                             variable=self.addVariable("int",0)),
            "sweepnurbs":self._addElemt(id=id+3,name="Add SweepNURBs object",width=80,height=10, value = True,
                             action=None,type="checkbox",icon=None,
                             variable=self.addVariable("int",0))
                             }
        self.LABELS = {"test":self._addElemt(id=id+4,name="test", label="Sweep profile sides:", width = 80, height=10, type = "label",variable = self.addVariable("string","test"))}
        #in order to display the boxes checked to begin with, the value = True command was used. But when
        #I call getbool, I still get False? So this only gets set when the button changes? In that case
        #we will have to only do something if unchecked -> true
        id = id + len(self.CHECKBOXS) +1

        self.SLIDERS = {"sweep":self._addElemt(id = id,name="Sweep profile sides:",width=80,height=10,
                                             action=None,type="sliders", value = 6,
                                             variable=self.addVariable("float",1.0),
                                             mini=3,maxi=8,step=1)}
        id = id+1
        self.BUTTONS = {"cancel":self._addElemt(id=id,name="Cancel",width=80,height=10,action=self.close,alignement = 500,type="button"),
                        "import":self._addElemt(id=id+1,name="Import File",width=80,height=10,alignement =10,action=self.loadFile,type="button")}
        
        
    def setupLayout(self):
        self._layout = []
        self._layout.append([self.TEXTAREA["intro"]])
        self._layout.append([self.CHECKBOXS["hypernurbs"]])
        self._layout.append([self.CHECKBOXS["connect"]])
        self._layout.append([self.CHECKBOXS["railsplines"]])
        self._layout.append([self.CHECKBOXS["sweepnurbs"]])
        self._layout.append([self.LABELS["test"]])
        self._layout.append([self.SLIDERS["sweep"]])
        self._layout.append([self.BUTTONS["cancel"],self.BUTTONS["import"]])

    def loadFile(self,*args):
        self.fileDialog(label="choose a .swc file",callback=self.readFile)

        
        #creat the layout of the dialog
##        self.GroupBegin(DLG_GROUP_1, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, cols=1, rows=7, title="NeuronBuild", groupflags=5)
##        self.GroupBorderSpace(10, 10, 10, 10)
##       
##        #add multiline edit box for script description
##        if versionNumber >= 13000:
##            self.AddMultiLineEditText(TEXTBOX, flags=c4d.BFH_CENTER|c4d.BFV_TOP, inith=100, initw=300, style=c4d.DR_MULTILINE_READONLY|c4d.DR_MULTILINE_WORDWRAP)
##        else:
##            self.AddMultiLineEditText(TEXTBOX, flags=c4d.BFH_CENTER|c4d.BFV_TOP, inith=100, initw=300)
###            self.AddStaticText(TEXTBOX, flags=c4d.BFH_CENTER|c4d.BFV_TOP, inith=100, initw=300, borderstyle=1)
##        
##        #add check boxes for various construction options
##        self.AddCheckbox(HNCHECK, flags=c4d.BFH_LEFT, initw=300, inith=0, name="Add HyperNURBs object")
##        self.SetBool(HNCHECK, True)
##         
##        self.AddCheckbox(CONNECTCHECK, flags=c4d.BFH_LEFT, initw=300, inith=0, name="Add Connect object")
##        self.SetBool(CONNECTCHECK, True)
##        
##        self.AddCheckbox(RAILCHECK, flags=c4d.BFH_LEFT, initw=300, inith=0, name="Add rail splines (controls thickness)")
##        self.SetBool(RAILCHECK, True)
##        
##        self.AddCheckbox(SWEEPCHECK, flags=c4d.BFH_LEFT, initw=300, inith=0, name="Add SweepNURBs object")
##        self.SetBool(SWEEPCHECK, True)
##        
##        self.AddStaticText(PROFILETEXT, flags=c4d.BFH_LEFT, initw=300, inith=0, name="Sweep profile sides:")
##        
##        self.AddEditSlider(PROFILESIDES, flags=c4d.BFH_FIT, initw=30, inith=0)
##        self.SetLong(PROFILESIDES, 6, min=3, max=8, step=1)
##        
##        self.GroupEnd()
##        
##        
##        self.GroupBegin(DLG_GROUP_2, flags=c4d.BFH_RIGHT|c4d.BFV_BOTTOM, cols=2, rows=1, title="", groupflags=5)
##        self.GroupBorderSpace(10, 10, 10, 10)
##        self.AddButton(CANCELBUTTON, flags=c4d.BFH_RIGHT, name="Cancel")
##        self.AddButton(IMPORTBUTTON, flags=c4d.BFH_RIGHT, name="Import File")
##        self.GroupEnd()
##       
##        return True
##
##    def InitValues(self):
##        #initiate the gadgets with values
##        if versionNumber >= 13000:
##            self.SetString(TEXTBOX, "The NeuronBuild script imports accurate neuromorpho SWC files "\
##            "and creates spline-based geometry (scale assumes Âµm as world unit). Choose modeling options below; " \
##            "if all boxes are unchecked, only the base splines will be added to the scene.")
##        else:
##            self.SetString(TEXTBOX, "The NeuronBuild script imports\naccurate neuromorpho SWC files\n"\
##                           "and creates spline-based geometry\n(scale assumes Âµm as world unit).\nChoose modeling options below;\n" \
##                           "if all boxes are unchecked, only\nthe base splines will be added to\nthe scene.")
##        self.result = True
##        return True
##
##    def Command(self, id, msg):
##        #reference global variables that set model parameters
##        global DoHN, DoConnect, DoRail, DoSweep, NSides
##        #handle user input
##        if id==IMPORTBUTTON:
##            close = True
##            DoHN = self.GetBool(HNCHECK)
##            DoConnect = self.GetBool(CONNECTCHECK)
##            DoRail = self.GetBool(RAILCHECK)
##            DoSweep = self.GetBool(SWEEPCHECK)
##            NSides = self.GetLong(PROFILESIDES)
##            self.result = True
##
##        elif id==CANCELBUTTON:
##            close = True
##            self.result = None
##
##        else:
##            close = False
##            DoHN = self.GetBool(HNCHECK)
##            DoConnect = self.GetBool(CONNECTCHECK)
##            DoRail = self.GetBool(RAILCHECK)
##            DoSweep = self.GetBool(SWEEPCHECK)
##            NSides = self.GetLong(PROFILESIDES)
##        
##        if close:
##            self.Close()
##            
##        return True
##        
##    def open_settings_dialog(default=None, title=None, width=240, height=290):
##        dialog = SettingsDlg(title, default)
##        dialog.Open(c4d.DLG_TYPE_MODAL, defaultw=width, defaulth=height)
##        return dialog.result
        
      
##def main():
##    """Call the readfile function. Start undo here."""
##    
##    #reference global variables that set model parameters
##    global DoHN, DoConnect, DoRail, DoSweep, NSides
##    
##    value = open_settings_dialog("test", "test")
##    
##    #test to see wehther the dialog "Cancel" button is pressed
##    if value is None:
##        print "Cancelled."
##    else:
##        doc.StartUndo()
##        
##        # open the C4D file browser to allow the user to choose a text file to read
##        neuromorphoFile = c4d.storage.LoadDialog()
##        
##        # run the read file procedure
##        if neuromorphoFile:
##            readFile(neuromorphoFile)
##        else:
##            print "Cancelled in Browser."
##
##
##if __name__=='__main__':
##    main()

if uiadaptor.host == "tk":
    #from DejaVu import Viewer
    #vi = Viewer()    
    #require a master
    try :
        import tkinter #python3
    except :
        import Tkinter as tkinter
 
    root = tkinter.Tk()
    mygui = NeuronBuildUI(title="NeuronBuildUI")
    #mygui.display()
elif uiadaptor.host == "qt":
    try :
        from PyQt4 import QtGui
    except :
        try :
            from PySide import QtGui
        except :
            print ("noQt support")
            exit()
    app = QtGui.QApplication(sys.argv)
    mygui = NeuronBuildUI(title="NeuronBuildUI")
    #ex.show()
else :
    mygui = NeuronBuildUI(title="NeuronBuildUI")
    #call it
mygui.setup()
mygui.display()
if uiadaptor.host == "qt": app.exec_()#work without it ?

##execfile("/Users/ludo/DEV/upy/trunk/upy/examples/layout.py")
