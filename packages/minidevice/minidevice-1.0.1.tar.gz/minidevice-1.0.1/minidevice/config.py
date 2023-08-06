import os
WORK_DIR = os.path.dirname(__file__)
ADB_PATH = "{}/adb.exe".format(WORK_DIR)
MINITOUCH_PATH = "{}/minitouch/libs".format(WORK_DIR)
MINICAP_PATH = "{}/minicap/libs".format(WORK_DIR)
MINICAPSO_PATH = "{}/minicap/jni".format(WORK_DIR)
LINESEQ = os.linesep