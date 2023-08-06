import sys
import os
import argparse
import shutil
import glob

from importlib import resources
from datetime import datetime


from nerrds import gen_conf



def is_tool(name):
	    return shutil.which(name) is not None

def main():


	#------------------------------------------------------ check if AMBER is available and quit if not ------------------------------------------------

	sander_MPI = 1 if is_tool("sander.MPI") else 0
	sander = 1 if is_tool("sander") else 0
	 
	if sander_MPI + sander == 0:
	    print("could not find sander or sander.MPI (needed to refine models), quitting")
	    sys.exit(0)


	#-------------------------------------------------------------- args ----------------------------------------------------------------------------

	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--pdb", type=str, help="input PDB file",required=True)
	parser.add_argument("-s", "--shifts", type=str, help="input shifts file in NMR-STAR v3 or NEF format",required=True)

	parser.add_argument("-c", "--conf", help="number of conformers to generate per model in input ensemble (default 50)")
	parser.add_argument("-r", "--avrmsd", help="average RMSD of conformers generated per model in input ensemble (default 2A)")
	parser.add_argument("-n", "--ncpu", help="number of CPUs used to refine models in AMBER (default 1)")

	parser.add_argument("-t", "--htc", help="run on NMRbox via HTCondor",action="store_true")
	parser.add_argument("-j", "--job", help="job ID")

	args = parser.parse_args()



	#-------------------------------------------------------------- parameters ----------------------------------------------------------------------------

	# number of conformers to generate per model in input ensemble
	if args.conf:
	    conformers = args.conf
	else:
	    conformers = 50 

	# average RMSD of confomers generated
	if args.avrmsd:
	    average_rmsd = args.avrmsd
	else:
	    average_rmsd = 2    

	# number of CPUs used to refine models in AMBER
	if args.ncpu:
	    if sander_MPI == 1:
	        cpu = int(args.ncpu)
	    else:
	        print("cannot find sander.MPI to run refinement with multiple cpus, continuing with ncpu=1")
	        cpu = 1
	else:
	    cpu = 1


	#-------------------------------------------------------------- variables ----------------------------------------------------------------------------


	natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\\d+)', s)] # used throughout to loop through files in natural order

	home_dir = os.getcwd()

	# shifts and PDB ensemble required as input
	path_to_pdb = home_dir+"/"+args.pdb
	path_to_shifts = home_dir+"/"+args.shifts

	# useful for later when running ansurr
	pdb_id = os.path.splitext(os.path.basename(path_to_pdb))[0]    
	shifts_id = os.path.splitext(os.path.basename(path_to_shifts))[0]

	# unique jobID based on time - could append pdb_id?
	job_id = datetime.now().strftime("%Y"+"%m"+"%d"+"_"+"%H"+"%M"+"%S"+"%f"+"_"+pdb_id+"_"+shifts_id) 


	#------------------------------------------------------ check if job to be run on HT condor --------------------------------------------------------------

	if args.htc:

	    print('ok')





	else:

		gen_conf.gen_conf(path_to_pdb, home_dir, job_id, pdb_id)




if __name__ == "__main__":
    main()
