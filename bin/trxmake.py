#!/usr/bin/env python3

import os
from datetime import date
import argparse

class C_ModuleGenerator:
	def __init__( self, modName = None, parentFolder = '.' ):
		self.modName = modName
		self.parentFolder = parentFolder
		self.dirPath = self.parentFolder + '/' + self.modName + '/'

	def GenerateModule( self ):
		self._MakeDirs( )
		self._WriteTemplates( )
		self._GenerateModuleTest( )

	def _GenerateModuleTest( self ):
		modName = self.modName
		parentFolder = self.parentFolder
		dirPath = self.dirPath

		self.modName = "test"
		self.parentFolder = parentFolder + "/" + modName
		self.dirPath = self.parentFolder + '/' + self.modName + '/'

		self._MakeDirs( )
		self._WriteTemplates( )

		self.modName = modName
		self.parentFolder = parentFolder
		self.dirPath = dirPath

	def _MakeDirs( self ):
		os.system( "mkdir -p " + self.dirPath )
		os.system( "mkdir -p " + self.dirPath + "/src" )
		os.system( "mkdir -p " + self.dirPath + "/inc" )
		os.system( "mkdir -p " + self.dirPath + "/build" )

	def _WriteTemplates( self ):
		template = self._GenerateHeaderTemplate( )
		file = open( self.dirPath + "/inc/%s.h"%( self.modName ), "w" )
		file.write( template )
		file.close( )

		template = self._GenerateSourceTemplate( )
		file = open( self.dirPath + "/src/%s.c"%( self.modName ), "w" )
		file.write( template )
		file.close( )		

	def _GenerateHeaderTemplate( self ):
		template = 							\
			"""/**							\
			\n * @file\t%s.h				\
			\n * @author\t%s				\
			\n * @date\t%s					\
			\n * @brief\t??					\
			\n */							\
			\n 								\
			\n#ifndef %s_H					\
			\n#define %s_H 					\
			\n								\
			\n#endif /* %s_H */				\
			\n								\
			\n//*** end of file ***//		\
			\n"""							\
			%( 	self.modName, 				\
				os.environ[ 'USER' ],		\
				date.today(), 				\
				self.modName.upper( ), 		\
				self.modName.upper( ), 		\
				self.modName.upper( ) )

		return template

	def _GenerateSourceTemplate( self ):
		template = 													\
			"""/**													\
			\n * @file\t%s.c										\
			\n * @author\t%s										\
			\n * @date\t%s											\
			\n * @brief\t??											\
			\n */													\
			\n 														\
			\n/* Includes go here.	*/								\
			\n#include <%s.h>										\
			\n														\
			\n/* typedefs go here.	*/								\
			\n 														\
			\n/* Consts go here.	*/								\
			\n 														\
			\n/* #defines go here.	*/								\
			\n 														\
			\n/* static vars go here.	*/							\
			\n														\
			\n/* static function declarations go here.	*/			\
			\n 														\
			\n/* non static function implementation go here.	*/	\
			\n 														\
			\n/* static function implementation go here.	*/		\
			\n 														\
			\n//*** end of file ***//								\
			\n"""													\
			%( 	self.modName, 										\
				os.environ[ 'USER' ],								\
				date.today(), 										\
				self.modName )

		return template		

parser = argparse.ArgumentParser( description = ''' TRX build app ''' )
parser.add_argument( 	'-c',
						'--command',
						type = str,
						choices = [ "genmod" ],
						default = None,
						help = 'What trxmake must do.'
						)
parser.add_argument( 	'-m',
						'--module',
						type = str,
						default = None,
						help = 'Module name.'
						)
parser.add_argument(	'-p',
						'--parent',
						type = str,
						default = './',
						help = 'Parent folder of the module.'
					)
args = parser.parse_args( )
def main( args ):
	if "genmod" == args.command:
		modGen = C_ModuleGenerator( modName = args.module, parentFolder = args.parent )
		modGen.GenerateModule( )
	else:
		parser.print_help()

main( args )

### end of file ###
