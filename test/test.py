import os, sys, glob
from filecmp import cmp

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
bindir = parentdir + "/bin/"

sys.path.append(bindir)
from trxmake import C_ModuleGenerator

PASS = 0
FAIL = -1

def main( ):
	result = PASS

	# TODO #3
	#result |= _testModuleGeneration( )
	

	# TODO: Change to "return result" whenever task #2 in the TODO file is done. 
	# It gives error when test is run in another system due to the "modules" parsing still
	# do not support relative paths.
	#result |= _testTrxmakeBuild( )

	result |= _testTrxmakeInstallation( )
	if PASS == result:
		print( "PASS" )
	else:
		print( "FAIL" )

	sys.exit( result )

def _testModuleGeneration( ):
	module = "mod1"
	os.system( "rm -rf ./%s"%( module ) )

	modGen = C_ModuleGenerator( modName = module, parentFolder = "./" )
	modGen.GenerateModule( )

	expectedList = ['./mod1/',												\
					'./mod1/src', './mod1/src/mod1.c',						\
					'./mod1/build',											\
					'./mod1/inc', './mod1/inc/mod1.h',						\
					'./mod1/test',											\
					'./mod1/test/src', './mod1/test/src/test.c', 			\
					'./mod1/test/build',									\
					'./mod1/test/inc', './mod1/test/inc/test.h']

	obtainedList = glob.glob( "./" + module + "/**", recursive = True )
	os.system( "rm -rf ./%s"%( module ) )

	expectedList.sort()
	obtainedList.sort()
	
	result = FAIL
	if ( expectedList == obtainedList ):
		result = PASS

	return result

def _testTrxmakeInstallation( ):
	installationFolder = os.getcwd() + "/test/trxmake_installation_folder/"

	os.system( "rm -rf ./{folder}".format( folder = installationFolder ) )
	os.system( "echo y | ./install/install.py -f {folder}  > /dev/null".format( folder = installationFolder ) )

	result = FAIL
	if True == cmp( installationFolder + "/trxmake/bin/trxmake.py", bindir + "/trxmake.py" ):
		result = PASS
	
	os.system( "rm -rf {folder}".format( folder = installationFolder ) )

	return result

def _testTrxmakeBuild( ):
	os.system( "python3 ./bin/trxmake.py -c build -f ./test/screws/screw/screw_test/build/trxmake.json > /dev/null" )
	result = FAIL
	if True == os.path.isfile( "test/screws/screw/screw_test/build/bin/app.elf" ):
		result = PASS

	return result

main( )

