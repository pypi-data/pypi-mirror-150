import sys
import os
import shutil
import subprocess

from importlib import resources



def refine(home_dir, job_id, pdb, cpu):

    tleap = shutil.which("tleap")
    sander = shutil.which("sander")
    sander_MPI = shutil.which("sander.MPI")
    cpptraj = shutil.which("cpptraj")

    wd = home_dir+'/'+job_id+'/refined/'+os.path.splitext(os.path.basename(pdb))[0] # make dir to run refinement in
    os.makedirs(wd,exist_ok=True)

    with resources.path("nerrds.scripts.AMBER", "leap.in") as f:
        leap_script = f
    with resources.path("nerrds.scripts.AMBER", "min.in") as f:
        min_script = f
    with resources.path("nerrds.scripts.AMBER", "min_solv.in") as f:
        min_solv_script = f
    with resources.path("nerrds.scripts.AMBER", "extract_pdb.cpptraj") as f:
        cpptraj_script = f

    shutil.copyfile(leap_script, wd+"/leap.in") # copy various refinement scripts into wd
    shutil.copyfile(min_script, wd+"/min.in")  
    shutil.copyfile(min_solv_script, wd+"/min_solv.in")
    shutil.copyfile(pdb, wd+'/prot_for_min.pdb') # pdb is renamed to generic name referred to in refinement scripts, will be renamed after

    os.chdir(wd)

    run_tleap = subprocess.run([tleap, "-f", "leap.in"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))

    if int(cpu)==1:  
        run_amber = subprocess.run([sander, "-i", "min_solv.in", "-o", "min_solv.out", "-p", "prot_solv.parm7", "-c", "prot_solv.rst7", "-r", "prot_min_solv.rst7", "-x", "prot_min_solv.nc", "-ref", "prot_solv.rst7", "-O"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
        run_amber = subprocess.run([sander, "-i", "min.in", "-o", "min.out", "-p", "prot_solv.parm7", "-c", "prot_min_solv.rst7", "-r", "prot_min.rst7", "-x", "prot_min.nc", "-O"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
    elif int(cpu) > 1:
        run_amber = subprocess.run(["mpirun", "-np", str(cpu), sander_MPI, "-i", "min_solv.in", "-o", "min_solv.out", "-p", "prot_solv.parm7", "-c", "prot_solv.rst7", "-r", "prot_min_solv.rst7", "-x", "prot_min_solv.nc", "-ref", "prot_solv.rst7", "-O"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
        run_amber = subprocess.run(["mpirun", "-np", str(cpu), sander_MPI, "-i", "min.in", "-o", "min.out", "-p", "prot_solv.parm7", "-c", "prot_min_solv.rst7", "-r", "prot_min.rst7", "-x", "prot_min.nc", "-O"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))

    if os.path.exists("prot_min.nc"):
        run_cpptraj = subprocess.run([cpptraj, "-i", cpptraj_script],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
        shutil.copyfile(wd+'/prot_min.pdb',wd.split('/')[-1]+'_refined.pdb')

    os.chdir(home_dir)


