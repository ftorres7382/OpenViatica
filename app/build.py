import subprocess

subprocess.run(["nuitka", "--follow-imports", "--output-dir=build", "OpenViatica.py"])