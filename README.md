NeuronBuild
==========

A script to import Neuromorpho data into 3D apps like Cinema 4D

NeuronBuild | Nick Woolridge | 2013 | n.woolridge@utoronto.ca
version date: March 11 2013

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
 are the splines that define the dendrite paths, and rail splines that define their radius.
    
New in 1.4:
    Modifications made by Graham Johnson on March 11, 2013
    – support for Cinema 4D r12 and r13 (Oconnect and AddMultiLineEditText compatibility
    – convert right handed .swc data to Cinema 4D left-handed with coordSystem test
    – added safety test if user hits cancel button while in the system browser. Reports as 'Cancelled in Browser.'
