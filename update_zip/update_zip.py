import zipfile, os, subprocess, pathlib, os
#python3 -mzipfile -c ../repo/plugin.video.lo-scienziato-pazzo.zip ../plugin.video.lo-scienziato-pazzo
import pathlib
mypath = pathlib.Path(os.path.join(os.getcwd(), __file__)).parent
srun = subprocess.run(["python3", "-mzipfile", "-c", mypath/".."/"repo"/"lo-scienziato-pazzo-installer.zip", mypath/".."/"lo-scienziato-pazzo-installer"], shell=True, capture_output=True)
print(srun.stdout.decode("utf-8"))