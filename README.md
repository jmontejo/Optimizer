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

signal  - Specify the path to the signal ntuple. Key can exist only once
bkg     - Specify the path to background ntuples. Several backgrounds can be specified 
          and will be merged
tree    - Name of the tree in the ntuples. The same tree name is expected in all samples.
          The special tree name "sample" can be given when using SampleHandler objects
          to use the name of the sample. Or the name "export" to use the equivalent name
          in ntuples exported from the stop1L framework
tag     - Name for the JO. Output folders and files will use this tag
cut     - Preselection cut to be applied. The optimization running time depends strongly
          on the number of events. Applying preselection cuts speeds up the process.
weight  - The event-wise weight to be applied in the samples
lumi    - Target luminosity in pb
syst    - Systematic uncertainty to be assumed in the signal region
noCheck - Default false, can be set to true. Asume all variable input names are correct 
          and branches exist. Skips sanity checks
doPlots - Default true, can be set to false. Produce shape comparison plots between signal
          and background after preselection.
round   - Default true, can be set to false. After optimization round the cuts to the
          step-size defined in "var".
var     - Takes two values, name of the variable and granularity of rounding. Functions
          and arrays are accepted as variable names (e.g. Sum$(jet_pt) or jet_pt[0]).
          The optimization result is rounded to the specified granularity
          Example: var  jet_pt[0]  5000
alg     - Algorithms to be used for the optimization, takes two values. Several instances
          can be specified and will be run one after another. When the root Minimizer is 
          used a second string of options can be provided separated by semicolons.
          Example: alg  Minimizer   Minuit2:Migrad:1000000:usePrevBest
          

Batch Submission
====================

In batch folder there is an example of batch submission script. At the moment the list of files that are going to be processed is hardcoded (to-do-fix)
The script accept the following options:

--optVars "var1:step1,var2:step2"     Comma separated list of variables to run the optimisation with with the step. Example:
--optDampMC 100.                      Limit for MC damping. It is effectively the BKG statistics of the SR
--presel  "cut1<10,cut2==5,cut3>1"    Root Tree-like comma separated list of cuts to apply at preselection level, before the optimisation
--optName "name"                      Job/Optimisation Tag Name
--optIters 100                        Number of iterations for the genetic algorithm
--queue    1nh                        Queue where to submit the jobs
--submit                              Submit the jobs
