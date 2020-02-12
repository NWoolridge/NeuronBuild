NeuronBuild
==========

Scripts to import neuron morphology data (from neuromorpho.org) into Cinema 4D and ZBrush.

## NeuronBuild  C4D
https://github.com/NWoolridge/NeuronBuild

Watch a video on using this script: https://vimeo.com/207323665

The current working version is 1.8. Version 1.6 is experimental, and not yet fully functional.

NeuronBuild C4D | Nick Woolridge | 2013-2020 | n.woolridge@utoronto.ca
Version date: March 2013

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
- If all the geometry options are chosen, the geometry consists of a HyperNURBs object, which contains a Connect object, which contains a null object, which contains the sweep objects that define the axons and dendrites. 
Since the Soma (cell body) definition in the swc files is so rudimentary, you may want to 
delete or hide it, and let the soma be defined by the merging dendrite roots. Within the sweep
objects are n-sided splines (named "Profile") set to 6-sides; you could search for these 
objects and change the number of sides to 4 to simplify the geometry. Also in the SweepNURBs objects
are the splines that define the dendrite paths, and rail splines that define their radius.
    
Version History
- 1.8:  Added options (disabled by default) to insert the model hierarchy in a Volume builder and Volume mesher object,
        yeilding a single mesh. Adjust the Voxel dimension in the volume builder to adjust resolution. Be careful not
        to make the resolution too low, since this can potentially generate large poly counts.
        Added support for other SWC entities. Removed R12, R13 compatibility.
- 1.7:    Added support for glial processes (ID 7 in neuromorpho's version of the SWC file format).
        This means that astrocytes are now supported (unreleased)
- 1.6:    Incomplete conversion to Upy framework; do not use.
- 1.5:    Stable version for C4D R13-R21
- 1.4:    Modifications made by Graham Johnson on March 11, 2013
        – support for Cinema 4D r12 and r13 (Oconnect and AddMultiLineEditText compatibility
        – convert right handed .swc data to Cinema 4D left-handed with coordSystem test
        – added safety test if user hits cancel button while in the system browser. Reports as 'Cancelled in Browser.'

This software is open-source under the MIT License.

## NeuronBuild ZBrush
https://github.com/NWoolridge/NeuronBuild

The current version is 1.2.

NeuronBuild ZBrush | 2017 Nicholas Woolridge & Marcus Burgess | n.woolridge@utoronto.ca

Many thanks to Marcus Burgess, moderator at the ZBrush ZScipting Help Forum, who was extremely helpful in understanding how to do just about everything this script does!

Watch a video on using this script: https://vimeo.com/207323832

Version date: March 2017

How to use:
- Obtaining neuron morphology files: go to http://neuromorpho.org and find and download a neuron file you are interested in. These will usually have the ".swc" or ".txt" file extension; either is fine.
- In ZBrush, use Menus > ZScript > Load; navigate your file system to find the script file, select it, and click on "Open"
- A button called "Import_Neuromorpho_SWC_File" will appear in the tutorial palette; the tutorial palette is just below the viewport. Drag the divider up to see the button.
- Click on the "Import_Neuromorpho_SWC_File" button, and choose the neuron morphology file you downloaded earlier.
- Depending upon the complexity and size of the file, parsing the file can take some time; a note will appear indicating the number of lines in the file, then the zsphere construction will occur. It may appear that ZBrush has frozen, but be patient.
- PLEASE NOTE: to generate a mesh from a zsphere model, one would normally use the adaptive skin function. We have found that users should choose the "Use Classic Skinning" option in the Adaptive skin settings, otherwise ZBrush may crash.
- ALSO NOTE: the scale of the models produced in Neuronbuild ZBrush is currently set to 1/50 the size of the models produced by the NeuronBuild C4D script. This is due to scale limitations within ZBrush. To have the models from each script match in terms of relative dimensions, scale a model produced by Neuronbuild ZBrush by 50x in C4D or other apps.

If you use this script, please consider posting the results of your work in the ZBrush forums at: http://www.zbrushcentral.com/zbcinfinite.php
