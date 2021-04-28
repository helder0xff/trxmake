#!/usr/bin/env python3

import os
import argparse

parser = argparse.ArgumentParser( description = ''' TRX build app ''' )

parser.add_argument( 	'-f',
						'--folder',
						type = str,
						choices = [ "genmod" ],
						default = '~/',
						help = 'Installation folder.'
					)
args = parser.parse_args( )

def main( args ):
	installationFolder = args.folder + '/trxmake/bin/'

	print( "You are about to install trxmake on {folder}".format( folder = args.folder ) )
	userInput = 'A'
	while userInput not in ['Y', 'N', 'y', 'n']:
		userInput = input( "Is that right? (Y/N)\n" )

	if userInput in [ 'N', 'n' ]:
			quit()

	os.system("mkdir -p " + installationFolder )
	CWD = os.getcwd()
	THIS_DIR = os.path.dirname(os.path.realpath(__file__))
	os.chdir(THIS_DIR)
	os.system("cp ../bin/trxmake.py " +	installationFolder + "trxmake_v2.py")
	os.system("chmod +x " + installationFolder + "trxmake_v2.py")
	os.chdir(CWD)	

main( args )

### end of file ###