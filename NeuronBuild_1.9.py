"""
NeuronBuild | Nick Woolridge | 2013 | n.woolridge@utoronto.ca
version date: January 26, 2020
A script to import swc files downloaded from neuromorpho.org, and create accurate
spline-based models of neuronal structure. The original swc file format is detailed here:
Cannon, R.C, Turner, D.A, Pyapali, G.K, Wheal, H.V. An on-line archive of reconstructed
hippocampal neurons. Journal of Neuroscience Methods. 84 1–2. pp 49-54. 1998
The reconstruction units are μm (micrometers).
Note: soma (cell body) definitions vary from file to file; this script assumes a three point spline
(which is very common). The soma object is disabled by default, since they rarely produce acceptable geometry.
Note: use of neuromorpho files may come with an obligation to cite the original publication.

How to use:
- add to your C4D scripts folder (on Mac OS X: Applications/MAXON/CINEMA 4D R14/library/scripts or in the user prefs folder)
- Browse and download a .swc or .swc.txt file from http://neuromorpho.org/
- Open the script manager in C4D, the script should be in the pop-up menu at the top of the window.
- In the Script manager in C4D load the NeuronBuild script and click "Execute".
- An import options dialog should appear; choose options for imported geometry, and click "Import File".
- In the open file dialog, choose the swc file and click "OK".
- A neuron should appear in your viewport.
- If all the geometry options are chosen, the geometry consists of a HyperNURBs object, which contains a Connect object, which
contains a null object, which contains the sweep objects that define the axons and dendrites.
Since the Soma (cell body) definition in the swc files is so rudimentary, you may want to
delete or hide it, and let the soma be defined by the merging dendrite roots. Within the sweep
objects are n-sided splines (named "Profile") set to 6-sides; you could search for these
objects and change the number of sides to 4 to simplify the geometry. Also in the SweepNURBs objects
are the splines that define the dendrite paths, and rail splines that define their radii.
The new volume builder and volume mesher objects allow for the creation of a single, optimized mesh. The resolution
of the mesh is set by the Voxel Size setting in the volume builder object. If the default resolution is too low
(which it almost ceratinly will be), gradually lower the Voxel Size until you have an acceptable result.
BE CAREFUL: jumping immediately to a very low voxel size may generate an enormous number of polygons, which could potentially
exhaust your system resources.

Version History
1.9     Updated for Python 3.x and Cinema4D R24 compatability ("print" statement parentheses added).
1.8     Added options (disabled by default) to insert the model hierarchy in a Volume builder and Volume mesher object,
        yeilding a single mesh. Adjust the Voxel dimension in the volume builder to adjust resolution. Be careful not
        to make the resolution too low, since this can potentially generate large poly counts.
        Added support for other SWC entities. Removed R12, R13 compatibility.
1.7:    Added support for glial processes (ID 7 in neuromorpho's version of the SWC file format).
        This means that astrocytes are now supported
1.6:    Incomplete conversion to Upy framework; do not use.
1.5:    Stable version for C4D R13-R21
1.4:    Modifications made by Graham Johnson on March 11, 2013
        – support for Cinema 4D r12 and r13 (Oconnect and AddMultiLineEditText compatibility
        – convert right handed .swc data to Cinema 4D left-handed with coordSystem test
        – added safety test if user hits cancel button while in the system browser. Reports as 'Cancelled in Browser.'

This software is open-source under the MIT License.

Copyright (c) 2013-2020 Nicholas Woolridge

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import c4d, os
from c4d import gui

#Welcome to the world of Python

#Create IDs for the GUI elements in the settings dialog
DLG_GROUP_1 = 1000
DLG_GROUP_2 = 1001
TEXTBOX = 1002
CANCELBUTTON = 1003
IMPORTBUTTON = 1004
HNCHECK = 1005
CONNECTCHECK = 1006
RAILCHECK = 1007
SWEEPCHECK = 1008
PROFILETEXT = 1009
PROFILESIDES = 1010

VOLUMEBUILDERCHECK = 1011
VOLUMEMESHERCHECK = 1012
SINGLESPLINECHECK = 1013

coordsystem="left"
versionNumber=c4d.GetC4DVersion()

def somaMake(somaLines, neuroFile, fileName):
    """Create splines to make the cell body."""

    #reference global variables that set model parameters
    global DoHN, DoConnect, DoRail, DoSweep, DoSingleSpline, NSides, DoVB, DoVM, NullName

    #create spline
    Spline = c4d.BaseObject(c4d.Ospline)

    #add name to spline
    Spline[c4d.ID_BASELIST_NAME] = "Soma"

    #set type to linear
    Spline[c4d.SPLINEOBJECT_TYPE] = 0

    #set number of points for spline
    Spline.ResizeObject(len(somaLines))
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

    Spline.Message(c4d.MSG_UPDATE) #Message Update

    #create sweep object
    if DoSweep == True:
        Sweep = c4d.BaseObject(c4d.Osweep)
        Sweep[c4d.ID_BASELIST_NAME] = "Soma Sweep"
        Sweep[c4d.SWEEPOBJECT_CONSTANT] = False
        Sweep[c4d.SWEEPOBJECT_RAILDIRECTION] = False
        Sweep[c4d.CAP_TYPE] = 1
        Sweep.SetPhong(True, True, 80)
        Sweep.SetDeformMode(False)
        doc.InsertObject(Sweep)

        #create the profile for the sweep
        Profile = c4d.BaseObject(c4d.Osplinenside)
        Profile[c4d.ID_BASELIST_NAME] = "Profile"
        Profile[c4d.PRIM_NSIDE_RADIUS] = sRad
        Profile[c4d.PRIM_NSIDE_SIDES] = NSides
        doc.InsertObject(Profile)

        Profile.Message(c4d.MSG_UPDATE) #Message Update

        Spline.InsertUnder(Sweep)
        Profile.InsertUnder(Sweep)

        Sweep.Message(c4d.MSG_UPDATE) #Message Update

    #add undo for spline creation
    doc.AddUndo(c4d.UNDOTYPE_NEW, Spline)

    #insert the spline under the null object
    if DoSweep == True:
        parent = doc.SearchObject(NullName)
        Sweep.InsertUnder(parent)

    c4d.EventAdd()

def splineMake(splineLines, neuroFile, fileName):
    #Create splines to define the dendrites and axons

    #reference global variables that set model parameters
    global DoHN, DoConnect, DoRail, DoSweep, DoSingleSpline, NSides, DoVB, DoVM, NullName

    #run through the data file, identifying contiguous spline segments. this is possible because
    #the last value in the data refers to the "root" point of that branch segment
    splineSep = []
    for n in range(0, len(splineLines)):
        currLine = splineLines[n]
        sIndex = int(currLine[0])
        sRoot = int(currLine[6])
        if sIndex > sRoot + 1:
            splineSep.append(sIndex)

    #ensures that the final spline is included in the drawing
    finalIndex = int(splineLines[len(splineLines)-1][0])

    if finalIndex not in splineSep:
        splineSep.append(finalIndex)

    #now build the spline segments as separate splines
    for n in range(0, len(splineSep)):
        if n < (len(splineSep) - 1):

            #determine the offset between segemnts; this is the number of vertices in each spline segment
            offset = splineSep[n+1] - splineSep[n] + 1

            #ensures that the final point is included in the drawing
            if splineSep[n+1] == finalIndex:
                offset = offset + 1

            #special case: if the spline is not rooted, one fewer point
            if int(neuroFile[splineSep[n]-1][6]) < 0:
                offset = offset - 1

            #create an empty spline
            Spline = c4d.BaseObject(c4d.Ospline)

            #allocate points for the spline
            Spline.ResizeObject(offset)

            #get the data line that starts the segment
            splineStart = neuroFile[splineSep[n]-1]
            splineType = int(splineStart[1])

            #determine what type of spline it is and name it
            if splineType == 2:
                name = "Axon " + str(n)
            elif splineType == 3:
                name = "Basal Dendrite " + str(n)
            elif splineType == 4:
                name = "Apical Dendrite " + str(n)
            elif splineType == 5:
                name = "Custom " + str(n)
            elif splineType == 6:
                name = "Unspecified Neurites " + str(n)
            elif splineType == 7:
                name = "Glial Process " + str(n)

            Spline[c4d.ID_BASELIST_NAME] = name
            Spline[c4d.SPLINEOBJECT_TYPE] = 0

            #find the root point for this segment by going back to
            #the line in neuroFile that contains it
            #if the point is unrooted, let it be 'its own root'
            if int(splineStart[6]) >= 0:
                rootLine = neuroFile[((int(splineStart[6])) - 1)]
            else:
                rootLine = splineStart

            x, y, z = float(rootLine[2]), float(rootLine[3]), float(rootLine[4])
            rootPos = c4d.Vector(x, y, z)
            if coordsystem=="left":  #Convert to left-hand for C4D added by GJ March 11, 2013
                rootPos = c4d.Vector(x, y, -z)
            Spline.SetPoint(0, rootPos)

            for m in range(1, offset):
                l = int(splineSep[n]) + (m - 2)

                #correction to account for difference in unrooted points
                if rootLine == splineStart:
                    l = l + 1

                currLine = neuroFile[l]

                #create the variables for positioning the points
                sx = float(currLine[2])
                sy = float(currLine[3])
                sz = float(currLine[4])
                if coordsystem=="left":  #Convert to left-hand for C4D added by GJ March 11, 2013
                    sz = -sz
                #radius, not used yet
                sRad = float(currLine[5])
                pos = c4d.Vector(sx, sy, sz)
                Spline.SetPoint(m, pos)

            #create the spline
            doc.InsertObject(Spline)
            c4d.EventAdd()

            #in order to scale the sweepNURBs object, we create a copy of the spline
            #to act as a rail spline, and then add the radius value to one of the coords
            if DoRail == True:
                railSpline = Spline.GetClone()
                railSpline[c4d.ID_BASELIST_NAME] = name + " Rail"

                rVector = c4d.Vector((x + (float(rootLine[5]))), y, z)
                if coordsystem == "left":  #Convert to left-hand for C4D added by GJ March 11, 2013
                    rVector = c4d.Vector((x + (float(rootLine[5]))), y, -z)

                railSpline.SetPoint(0, rVector)
                for m in range(1, offset):
                    l = int(splineSep[n]) + (m - 2)


                    #correction to account for difference in unrooted points
                    if rootLine == splineStart:
                        l = l + 1

                    currLine = neuroFile[l]

                    #create the variables for positioning the points
                    sRad = float(currLine[5])
                    #add the radius to the x coord this time
                    sx = (float(currLine[2]) + sRad)
                    sy = float(currLine[3])
                    sz = float(currLine[4])
                    if coordsystem=="left":  #Convert to left-hand for C4D added by GJ March 11, 2013
                        sz = -sz
                    #radius, not used yet

                    pos = c4d.Vector(sx, sy, sz)
                    railSpline.SetPoint(m, pos)

                doc.InsertObject(railSpline)
                c4d.EventAdd()

                railSpline.Message(c4d.MSG_UPDATE) #Message Update

            #create the sweep object
            if DoSweep == True:
                Sweep = c4d.BaseObject(c4d.Osweep)
                Sweep[c4d.ID_BASELIST_NAME] = name
                #the seep object needs to have two default settings disabled
                Sweep[c4d.SWEEPOBJECT_CONSTANT] = False
                Sweep[c4d.SWEEPOBJECT_RAILDIRECTION] = False
                Sweep[c4d.CAP_TYPE] = 1
                Sweep.SetPhong(True, True, 80)

                #create the profile for the sweep
                Profile = c4d.BaseObject(c4d.Osplinenside)
                Profile[c4d.ID_BASELIST_NAME] = "Profile"
                Profile[c4d.PRIM_NSIDE_RADIUS] = sRad
                Profile[c4d.PRIM_NSIDE_SIDES] = NSides
                doc.InsertObject(Profile)

            #insert the splines as children of the sweepNURBs object, in the correct order
            if DoRail == True:
                if DoSweep == True:
                    railSpline.InsertUnder(Sweep)
            if DoSweep == True:
                Spline.InsertUnder(Sweep)
                Profile.InsertUnder(Sweep)

            #add undo for spline creation
            doc.AddUndo(c4d.UNDOTYPE_NEW, Spline)

            #create and insert the spline into the SingleSplineNull if that option is chosen
            if DoSingleSpline == True:
                SplineCopy = Spline.GetClone()
                doc.InsertObject(SplineCopy)
                c4d.EventAdd()
                SSOName = "Single_Spline_Object_" + fileName
                parent = doc.SearchObject(SSOName)
                SplineCopy.InsertUnder(parent)
                doc.AddUndo(c4d.UNDOTYPE_NEW, SplineCopy)

                #do the same for the Rail splines
                SplineRailCopy = railSpline.GetClone()
                doc.InsertObject(SplineRailCopy)
                c4d.EventAdd()
                SSROName = "Single_Spline_Object_Rail_" + fileName
                parent = doc.SearchObject(SSROName)
                SplineRailCopy.InsertUnder(parent)
                doc.AddUndo(c4d.UNDOTYPE_NEW, SplineRailCopy)

            #insert the spline under the null object
            if DoSweep == True:
                parent = doc.SearchObject(NullName)
                Sweep.InsertUnder(parent)
            else:
                parent = doc.SearchObject(NullName)
                Spline.InsertUnder(parent)

            c4d.EventAdd()

            Spline.Message(c4d.MSG_UPDATE) #Message Update

def readFile(path):
    #Access the neuromorpho swc file, strip comments, and load it into the neuroFile nested list.

    #reference global variables that set model parameters
    global DoHN, DoConnect, DoRail, DoSweep, DoSingleSpline, DoVB, DoVM, NullName

    neuroFile = []
    somaLines = []
    splineLines = []

    #Get the name of the file and split off the last file extension
    filePath = os.path.basename(path)
    fileName = os.path.splitext(filePath)[0]

    #here we read the file, and create two sub lists: one for the soma, and one for the axons, dendrites, and other structures
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

    #create null to contain splines for procedural hierarchy
    groupNull = c4d.BaseObject(c4d.Onull)
    NullName  = "groupNull_" + fileName
    groupNull[c4d.ID_BASELIST_NAME] = NullName
    #insert the null in the scene
    doc.InsertObject(groupNull)
    #add undo for null creation
    doc.AddUndo(c4d.UNDOTYPE_NEW, groupNull)
    c4d.EventAdd()

    #create single spline null
    #if DoSingleSpline == True:
    SplineNull = c4d.BaseObject(c4d.Onull)
    SplineNull[c4d.ID_BASELIST_NAME] = "Single_Spline_Object_" + fileName
    #insert the null in the scene
    doc.InsertObject(SplineNull)
    doc.AddUndo(c4d.UNDOTYPE_NEW, SplineNull)
    c4d.EventAdd()

    #create single spline RAIL null
    #if DoSingleSpline == True:
    SplineRailNull = c4d.BaseObject(c4d.Onull)
    SplineRailNull[c4d.ID_BASELIST_NAME] = "Single_Spline_Object_Rail_" + fileName
    #insert the null in the scene
    doc.InsertObject(SplineRailNull)
    doc.AddUndo(c4d.UNDOTYPE_NEW, SplineRailNull)
    c4d.EventAdd()

    groupNull.Message(c4d.MSG_UPDATE) #Message Update

    #call the functions that build the soma and other splines, if applicable
    if len(somaLines) > 0:
        somaMake(somaLines, neuroFile, fileName)

    if len(splineLines) > 0:
        splineMake(splineLines, neuroFile, fileName)


    #Create single spline from all neuron spline segments
    if DoSingleSpline == True:
        #find and select the grouped source splines
        SSOName = "Single_Spline_Object_" + fileName
        op = doc.SearchObject(SSOName)
        #issue the join command to connect the source splines
        if not op:
            raise TypeError("there's no object selected")
        result = c4d.utils.SendModelingCommand(
                                  command = c4d.MCOMMAND_JOIN,
                                  list = [op])
        op[c4d.ID_BASELIST_NAME] = "Component_Splines_" + fileName
        #check if result is a list
        if result is False:
            raise TypeError("Join didn't work")
        elif result is True:
            print("join should not return true")
        elif isinstance(result, list):
            doc.InsertObject(result[0])

        #find and select the grouped source Rail splines
        SSROName = "Single_Spline_Object_Rail_" + fileName
        op = doc.SearchObject(SSROName)
        #issue the join command to connect the source splines
        if not op:
            raise TypeError("there's no object selected")
        resultR = c4d.utils.SendModelingCommand(
                                  command = c4d.MCOMMAND_JOIN,
                                  list = [op])
        op[c4d.ID_BASELIST_NAME] = "Component_Rail_Splines_" + fileName
        #check if result is a list
        if resultR is False:
            raise TypeError("Join didn't work")
        elif resultR is True:
            print("join should not return true")
        elif isinstance(resultR, list):
            doc.InsertObject(resultR[0])

        c4d.EventAdd()

        startObject = doc.SearchObject(SSOName)
        #startobject.Message(c4d.MSG_UPDATE) #Message Update

        #send Message to update object cache (bounding box)s
        startObject.Message(c4d.MSG_UPDATE)
        #get the bounding box radius
        bbox = startObject.GetRad()
        bboxList = [bbox[0],bbox[1],bbox[2]]
        #determine the Largest of the list items (used below if creating volume builder to determine voxel size)
        largestSize = max(bboxList)
        largestAxis = bboxList.index(largestSize)

        #print bboxList
        #print "The largest Dimension is ", largestSize , " and it's the " , largestAxis , " Axis"

    #create connect object
    if DoConnect == True:
        #Create and name connect object
        Connect = c4d.BaseObject(c4d.Oconnector)
        Connect[c4d.ID_BASELIST_NAME] = "Connect_" + fileName
        Connect[c4d.CONNECTOBJECT_WELD] = False
        #insert the connect object in the scene
        doc.InsertObject(Connect)

        #add undo for Connect creation
        doc.AddUndo(c4d.UNDOTYPE_NEW, Connect)
        c4d.EventAdd()

        #insert previously created group groupNull under Connect
        groupNull.InsertUnder(Connect)

    #create HN object
    if DoHN == True:
        HN = c4d.BaseObject(c4d.Osds)
        HN[c4d.ID_BASELIST_NAME] = "SDS_" + fileName
        #insert the HyperNURBs in the scene
        doc.InsertObject(HN)
        #add undo for HN creation
        doc.AddUndo(c4d.UNDOTYPE_NEW, HN)
        c4d.EventAdd()

        if DoConnect == True:
            Connect.InsertUnder(HN)
        else:
            groupNull.InsertUnder(HN)


    #create Volume Builder object
    if DoVB == True:
        VB = c4d.BaseObject(c4d.Ovolumebuilder)
        VB[c4d.ID_BASELIST_NAME] = "Volume_Builder_" + fileName
        #insert the Volume Builder in the scene
        doc.InsertObject(VB)

        #add undo for Volume Builder creation
        doc.AddUndo(c4d.UNDOTYPE_NEW, VB)
        c4d.EventAdd()

        #set the appropriate voxel dimension
        VoxelDim = (largestSize * 2) / 200
        #set the voxel (grid) size of the volume builder
        VB[c4d.ID_VOLUMEBUILDER_GRID_SIZE] = float(VoxelDim)

        if DoHN == True:
            HN.InsertUnder(VB)
        else:
            groupNull.InsertUnder(VB)

    #create Volume Mesher object
    if DoVM == True:
        VM = c4d.BaseObject(c4d.Ovolumemesher)
        VM[c4d.ID_BASELIST_NAME] = "Volume_Mesher_" + fileName
        #insert the Volume Builder in the scene
        doc.InsertObject(VM)
        #set the volume mesh threshold to a 60%
        VM[c4d.ID_VOLUMETOMESH_THRESHOLD] = float(0.6)

        #add undo for Volume Builder creation
        doc.AddUndo(c4d.UNDOTYPE_NEW, VM)
        c4d.EventAdd()

        if DoVB == True:
            VB.InsertUnder(VM)
        else:
            groupNull.InsertUnder(VM)

    #close out the undo stack
    doc.EndUndo()


class SettingsDlg(gui.GeDialog):

    def __init__(self, title=None, input_text=None):
        self.title = title or "User Input"
        self.input_text = input_text or ""
        self.result = None

    def CreateLayout(self):
        self.SetTitle("NeuronBuild")
        #creat the layout of the dialog
        self.GroupBegin(DLG_GROUP_1, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, cols=1, rows=9, title="NeuronBuild", groupflags=5)
        self.GroupBorderSpace(20, 20, 20, 20)

        #add multiline edit box for script description
        self.AddMultiLineEditText(TEXTBOX, flags=c4d.BFH_CENTER|c4d.BFV_TOP, inith=100, initw=400, style=c4d.DR_MULTILINE_READONLY|c4d.DR_MULTILINE_WORDWRAP)
        #self.AddStaticText(TEXTBOX, flags=c4d.BFH_CENTER|c4d.BFV_TOP, inith=100, initw=400, borderstyle=c4d.BORDER_NONE)

        self.AddSeparatorH(c4d.BFH_FIT)

        #add check boxes for various construction options
        self.AddCheckbox(HNCHECK, flags=c4d.BFH_LEFT, initw=400, inith=0, name="Add HyperNURBs object")
        self.SetBool(HNCHECK, True)

        self.AddCheckbox(CONNECTCHECK, flags=c4d.BFH_LEFT, initw=400, inith=0, name="Add Connect object")
        self.SetBool(CONNECTCHECK, True)

        self.AddCheckbox(RAILCHECK, flags=c4d.BFH_LEFT, initw=400, inith=0, name="Add rail splines (controls thickness)")
        self.SetBool(RAILCHECK, True)

        self.AddCheckbox(SWEEPCHECK, flags=c4d.BFH_LEFT, initw=400, inith=0, name="Add SweepNURBs object")
        self.SetBool(SWEEPCHECK, True)

        self.AddCheckbox(SINGLESPLINECHECK, flags=c4d.BFH_LEFT, initw=400, inith=0, name="Create Single Spline from dendrites, etc.")
        self.SetBool(SINGLESPLINECHECK, True)

        self.AddStaticText(PROFILETEXT, flags=c4d.BFH_LEFT, initw=400, inith=0, name="Sweep profile sides:")

        self.AddEditSlider(PROFILESIDES, flags=c4d.BFH_FIT, initw=30, inith=0)
        self.SetLong(PROFILESIDES, 6, min=3, max=8, step=1)

        #Add UI for Volume Builder and Mesher

        self.AddCheckbox(VOLUMEBUILDERCHECK, flags=c4d.BFH_LEFT, initw=300, inith=0, name="Add Volume Builder object")
        self.SetBool(VOLUMEBUILDERCHECK, False)

        self.AddCheckbox(VOLUMEMESHERCHECK, flags=c4d.BFH_LEFT, initw=300, inith=0, name="Add Volume Mesher object")
        self.SetBool(VOLUMEMESHERCHECK, False)

        self.GroupEnd()


        self.GroupBegin(DLG_GROUP_2, flags=c4d.BFH_RIGHT|c4d.BFV_BOTTOM, cols=2, rows=1, title="", groupflags=5)
        self.GroupBorderSpace(20, 20, 20, 20)
        self.AddButton(CANCELBUTTON, flags=c4d.BFH_RIGHT, name="Cancel")
        self.AddButton(IMPORTBUTTON, flags=c4d.BFH_RIGHT, name="Import File")
        self.GroupEnd()

        return True

    def InitValues(self):
        #initiate the gadgets with values
        self.SetString(TEXTBOX, "Version 1.8 The NeuronBuild script imports accurate neuromorpho SWC files "\
        "(from neuromorpho.org)and creates spline-based geometry (scale assumes µm as world unit). Choose modeling options below; " \
        "if all boxes are unchecked, only the base splines will be added to the scene. ©2013-2020 Nicholas Woolridge. MIT License")

        self.result = True
        return True

    def Command(self, id, msg):
        #reference global variables that set model parameters
        global DoHN, DoConnect, DoRail, DoSweep, DoSingleSpline, NSides, DoVB, DoVM
        #handle user input
        if id==IMPORTBUTTON:
            close = True
            DoHN = self.GetBool(HNCHECK)
            DoConnect = self.GetBool(CONNECTCHECK)
            DoRail = self.GetBool(RAILCHECK)
            DoSweep = self.GetBool(SWEEPCHECK)
            DoSingleSpline = self.GetBool(SINGLESPLINECHECK)
            NSides = self.GetLong(PROFILESIDES)

            DoVB = self.GetBool(VOLUMEBUILDERCHECK)
            DoVM = self.GetBool(VOLUMEMESHERCHECK)

            self.result = True

        elif id==CANCELBUTTON:
            close = True
            self.result = None

        else:
            close = False
            DoHN = self.GetBool(HNCHECK)
            DoConnect = self.GetBool(CONNECTCHECK)
            DoRail = self.GetBool(RAILCHECK)
            DoSweep = self.GetBool(SWEEPCHECK)
            DoSingleSpline = self.GetBool(SINGLESPLINECHECK)
            NSides = self.GetLong(PROFILESIDES)

            DoVB = self.GetBool(VOLUMEBUILDERCHECK)
            DoVM = self.GetBool(VOLUMEMESHERCHECK)

        if close:
            self.Close()

        return True

def open_settings_dialog(default=None, title=None, width=300, height=400):
    dialog = SettingsDlg(title, default)
    dialog.Open(c4d.DLG_TYPE_MODAL, defaultw=width, defaulth=height)
    return dialog.result

def main():
    #Call the readfile function. Start undo here.

    #reference global variables that set model parameters
    global DoHN, DoConnect, DoRail, DoSweep, DoSingleSpline, NSides, DoVB, DoVM

    value = open_settings_dialog("test", "test")

    #test to see wehther the dialog "Cancel" button is pressed
    if value is None:
        print("Cancelled.")
    else:
        doc.StartUndo()

        # open the C4D file browser to allow the user to choose a text file to read
        neuromorphoFile = c4d.storage.LoadDialog()

        # run the read file procedure
        if neuromorphoFile:
            readFile(neuromorphoFile)
        else:
            print("Cancelled in Browser.")


if __name__=='__main__':
    main()
