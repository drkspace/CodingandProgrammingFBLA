from subprocess import call
call(["python", "releases/pyinstaller.py", "--onefile", "fec.py"])
call(["mv", "dist/fec", "releases/"])
call(["rm", "-r", "dist"])
call(["rm", "-r", "build"])
call(["rm", "fec.spec"])
