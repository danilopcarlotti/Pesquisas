from recursive_folders import recursive_folders
import sys, shutil

if __name__ == "__main__":
    r = recursive_folders()
    paths = r.find_files(sys.argv[1])
    dest_path = sys.argv[2]
    ok = False
    for p in paths:
        arq = p.split("/")[-1]
        shutil.copy2(p, dest_path + arq)
        if not ok:
            print("ok")
            ok = True
