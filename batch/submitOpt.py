import sys,os
import glob


from optparse import OptionParser

def optParsing():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--optVars",dest="optVars",help="Optimisation Variables: format-> var:step",default="")
    parser.add_option("--optDampMC", dest="optDampMC",help="Statistics of the SR",default=100,type="float")
    parser.add_option("--presel", dest="presel",help="Preselection: comma separated list of cuts",default="")
    parser.add_option("--optName", dest="optName",help="Optimisation Name",default="")
    parser.add_option("--optIters", dest="optIters",help="Genetic Algorithm Iterations",type="int",default=25)
    parser.add_option("--queue", dest="queue",help="Queue",default="8nh")
    parser.add_option("--submit", dest="submit",help="Submit",default=False,action="store_true")
    
    
    
    
    
    (config, sys.argv[1:]) = parser.parse_args(sys.argv[1:])
    return config




def main():

    config = optParsing()
    

    #Generate JO_File

    joFile=open("JO_Stau_"+config.optName+".txt","w")
    joFile.write("signal /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/StauStau_200_1.root\n")
    joFile.write("bkg /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/Diboson.root\n")
    joFile.write("bkg /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/ttbar.root\n")
    joFile.write("bkg /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/Wjets_enu.root\n")
    joFile.write("bkg /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/Wjets_munu.root\n")
    joFile.write("bkg /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/Wjets_taunu.root\n")
    joFile.write("bkg /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/Zjets_ee.root\n")
    joFile.write("bkg /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/Zjets_mumu.root\n")
    joFile.write("bkg /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/Zjets_tautau.root\n")
    joFile.write("bkg /eos/atlas/user/p/pbutti/SkimsForOptimisation_2/StauStau_dataSS.root\n")

    joFile.write("\n\n")
    joFile.write("tree susy\n")
    joFile.write("tag "+config.optName+"\n")
    joFile.write("doPlots false\n")
    joFile.write("round false\n")
    joFile.write("\n\n")

    #parse preselection
    PreselCuts=(config.presel).split(",")
    joFile.write("cut ")
    for icut in range(len(PreselCuts)):
        if (icut==0):
            joFile.write("("+PreselCuts[icut]+")")
        else:
            joFile.write("*("+PreselCuts[icut]+")")
    joFile.write("\n")

    joFile.write("\n\n")
    joFile.write("weight weight\n")
    joFile.write("displayweight weight\n")
    joFile.write("noCheck false\n")
    joFile.write("lumi 80\n")
    joFile.write("syst 30\n")
    joFile.write("\n\n")

    joFile.write("MCDamp "+str(config.optDampMC)+"\n")

    #parse variables and step

    OptVars = (config.optVars).split(",")
    print OptVars

    for iv in range(len(OptVars)):
        joFile.write("var   "+OptVars[iv].split(":")[0]+"   "+OptVars[iv].split(":")[1]+"\n")

    joFile.write("\n\n")

    joFile.write("alg Minimizer Minuit2:Scan:1000000\n")
    joFile.write("alg Minimizer Minuit2:Simplex:1000000:usePrevBest\n")
    joFile.write("alg Minimizer Minuit2:Migrad:1000000:usePrevBest\n")

    joFile.write("alg Minimizer Genetic:.:"+str(config.optIters)+":usePrevBest:round\n\n\n\n")


    subfolder=config.optName+"_dir"
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    joFile.close()

    os.system("mv JO_Stau_"+config.optName+".txt "+subfolder+"/")
    script=open(subfolder+"/"+config.optName+"_job.sh","w")
    script.write("cd "+os.environ["PWD"]+"/"+subfolder+"/"+"\n")
    script.write("source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh\n")
    script.write("Optimizer "+"JO_Stau_"+config.optName+".txt\n")
    script.close()

    cmd = "bsub -o "+ os.environ["PWD"]+"/"+subfolder+"/"+config.optName+"_optOut.out -e "+os.environ["PWD"]+"/"+subfolder+"/"+config.optName+"_optErr.err "+" -q "+config.queue+" "+os.environ["PWD"]+"/"+subfolder+"/"+config.optName+"_job.sh"
    print cmd

    if (config.submit):
        os.system("chmod u+x "+ subfolder+"/"+config.optName+"_job.sh")
        os.system(cmd)
    else:
        print cmd
    
if __name__=="__main__":
    main()
