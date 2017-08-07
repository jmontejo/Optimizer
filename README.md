Optimizer - an optimization code for SR definitions in early R&D
===============================================================

Author: Javier Montejo Berlingen

Project
-------

The project is hosted at:

    https://gitlab.cern.ch/jmontejo/Optimizer

Documentation
=============

The Optimizer is a RootCore package, and is installed and compiled in the same way.
The steering of the optimization is done via a plain-text job option file. Example 
JO files can be found under Optimizer/share. 

Different optimization algorithms are available, from very basic random scans to
Minuit or genetic algorithms. The code is focused to scenarios where brute-force
scans are not possible, usually in the early R&D phase where a large number of 
variables is being tested.

The optimization is done via the command:

    ./Optimizer myJobOption

The running time depends strongly on the settings of the JO and vary between minutes
and days (for very bad choices in the genetic algorithm)

Job options
===========

The JO file is a plain-text file in the form: 
key value [value ...]

Comments start with a hashtag (#). Since white-space is used as a separator to parse
the JO, strings can not contain whitespace (and currently quotes are not supported).

The list of keys used in the JO are:

signal  - specify the path to the signal ntuple. Key can exist only once
bkg     - specify the path to background ntuples. Several backgrounds can be specified 
          and will be merged
tree    - name of the tree in the ntuples. The same tree name is expected in all samples.
          The special tree name "sample" can be given when using SampleHandler objects
          to use the name of the sample.
tag     - name for the JO. Output folders and files will use this tag
cut     - preselection cut to be applied. The optimization running time depends strongly
          on the number of events. Applying preselection cuts speeds up the process.
weight  - the event-wise weight to be applied in the samples
lumi    - target luminosity in pb
syst    - systematic uncertainty to be assumed in the signal region
noCheck - Default false, can be set to true. Asume all variable input names are correct 
          and branches exist. Skips sanity checks
var     - Takes two values, name of the variable and granularity of rounding. Functions
          and arrays are accepted as variable names (e.g. Sum$(jet_pt) or jet_pt[0]).
          The optimization result is rounded to the specified granularity
          Example: var  jet_pt[0]  5000
