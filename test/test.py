import os, sys, glob
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)
from bin import trxmake

PASS = 0
FAIL = -1

def main( ):
	result = PASS

	result |= _testModuleGeneration( )

	if result:
		print( "FAIL" )
	else:
		print( "PASS" )

	sys.exit( result )

def _testModuleGeneration( ):
	module = "mod1"
	os.system( "rm -rf ./%s"%( module ) )

	modGen = trxmake.C_ModuleGenerator( modName = module, parentFolder = "./" )
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

	result = FAIL
	if ( expectedList == obtainedList ):
		result = PASS

	return result

main( )

