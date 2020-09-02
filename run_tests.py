import sys,os

root_dir = os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(os.path.join(root_dir,'Configurations','tests')):
    test_files = files
    break

tests_paths = [os.path.join(root_dir,'Configurations','tests',file) for file in test_files]
run_cmd = "python D:\\workspace\\SL_platform\\main.py -c "
tests_cmd = [run_cmd + path for path in tests_paths]
for cmd in tests_cmd:
    os.system(cmd)
