#!/usr/bin/env python3

import os
from datetime import date
import argparse
import json

class C_ModuleGenerator:
	def __init__( self, modName = None, parentFolder = '.', platform = "HOST", app = False ):
		self.modName = modName
		self.parentFolder = parentFolder
		self.dirPath = self.parentFolder + '/' + self.modName + '/'
		self.platform = platform
		self.app = app

	def GenerateModule( self ):
		self._MakeDirs( )
		self._WriteTemplates( self.app )
		self._GenerateModuleTest( )

	def _GenerateModuleTest( self ):
		modName = self.modName
		parentFolder = self.parentFolder
		dirPath = self.dirPath

		self.modName =  modName + "_test"
		self.parentFolder = parentFolder + "/" + modName
		self.dirPath = self.parentFolder + '/' + self.modName + '/'

		self._MakeDirs( )
		self._WriteTemplates( app = True )

		self.modName = modName
		self.parentFolder = parentFolder
		self.dirPath = dirPath

	def _MakeDirs( self ):
		os.system( "mkdir -p " + self.dirPath )
		os.system( "mkdir -p " + self.dirPath + "/src" )
		os.system( "mkdir -p " + self.dirPath + "/inc" )
		os.system( "mkdir -p " + self.dirPath + "/build" )

	def _WriteTemplates( self, app = False ):
		template = self._GenerateHeaderTemplate( )
		file = open( self.dirPath + "/inc/%s.h"%( self.modName ), "w" )
		file.write( template )
		file.close( )

		template = self._GenerateSourceTemplate( app )
		file = open( self.dirPath + "/src/%s.c"%( self.modName ), "w" )
		file.write( template )
		file.close( )

		template = self._GenerateTrxmakeTemplate( )
		file = open( self.dirPath + "/build/%s.json"%( "trxmake" ), "w" )
		file.write( template )
		file.close( )

		if "HOST" != self.platform and True == app :
			template = self._GenerateLdrScriptTemplate( )
			file = open( self.dirPath + "/build/%s.lds"%( self.platform ), "w" )
			file.write( template )
			file.close( )

		if True == app:
			template = self._GenerateTestScript( )
			file = open( self.dirPath + "/%s.py"%( "test"), "w" )
			file.write( template )
			file.close( )

	def _GenerateTestScript( self ):
		auxTemplate =						\
			"""
import sys

PASS = 0
FAIL = -1

def main( ):
	result = PASS

	sys.exit( result )

main( )
			"""

		template = ''
		for line in auxTemplate.splitlines( ):
			template += line.rstrip( )
			template += '\n'

		return template

	def _GenerateLdrScriptTemplate( self ):
		auxTemplate =						\
			"""
/******************************************************************************
*
* Copyright (C) 2012 - 2016 Texas Instruments Incorporated - http://www.ti.com/
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions
* are met:
*
*  Redistributions of source code must retain the above copyright
*  notice, this list of conditions and the following disclaimer.
*
*  Redistributions in binary form must reproduce the above copyright
*  notice, this list of conditions and the following disclaimer in the
*  documentation and/or other materials provided with the
*  distribution.
*
*  Neither the name of Texas Instruments Incorporated nor the names of
*  its contributors may be used to endorse or promote products derived
*  from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
* "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
* A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
* OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
* SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
* LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
* THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
* OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*
* GCC linker script for Texas Instruments MSP432P401R
*
* File creation date: 2016-05-09
*
******************************************************************************/

MEMORY
{
    MAIN_FLASH (RX) : ORIGIN = 0x00000000, LENGTH = 0x00040000
    INFO_FLASH (RX) : ORIGIN = 0x00200000, LENGTH = 0x00004000
    SRAM_CODE  (RWX): ORIGIN = 0x01000000, LENGTH = 0x00010000
    SRAM_DATA  (RW) : ORIGIN = 0x20000000, LENGTH = 0x00010000
}

REGION_ALIAS("REGION_TEXT", MAIN_FLASH);
REGION_ALIAS("REGION_INFO", INFO_FLASH);
REGION_ALIAS("REGION_BSS", SRAM_DATA);
REGION_ALIAS("REGION_DATA", SRAM_DATA);
REGION_ALIAS("REGION_STACK", SRAM_DATA);
REGION_ALIAS("REGION_HEAP", SRAM_DATA);
REGION_ALIAS("REGION_ARM_EXIDX", MAIN_FLASH);
REGION_ALIAS("REGION_ARM_EXTAB", MAIN_FLASH);

SECTIONS {

    /* section for the interrupt vector area                                 */
    PROVIDE (_intvecs_base_address =
        DEFINED(_intvecs_base_address) ? _intvecs_base_address : 0x0);

    .intvecs (_intvecs_base_address) : AT (_intvecs_base_address) {
        KEEP (*(.intvecs))
    } > REGION_TEXT

    /* The following three sections show the usage of the INFO flash memory  */
    /* INFO flash memory is intended to be used for the following            */
    /* device specific purposes:                                             */
    /* Flash mailbox for device security operations                          */
    PROVIDE (_mailbox_base_address = 0x200000);

    .flashMailbox (_mailbox_base_address) : AT (_mailbox_base_address) {
        KEEP (*(.flashMailbox))
    } > REGION_INFO

    /* TLV table for device identification and characterization              */
    PROVIDE (_tlv_base_address = 0x00201000);

    .tlvTable (_tlv_base_address) (NOLOAD) : AT (_tlv_base_address) {
        KEEP (*(.tlvTable))
    } > REGION_INFO

    /* BSL area for device bootstrap loader                                  */
    PROVIDE (_bsl_base_address = 0x00202000);

    .bslArea (_bsl_base_address) : AT (_bsl_base_address) {
        KEEP (*(.bslArea))
    } > REGION_INFO

    PROVIDE (_vtable_base_address =
        DEFINED(_vtable_base_address) ? _vtable_base_address : 0x20000000);

    .vtable (_vtable_base_address) : AT (_vtable_base_address) {
        KEEP (*(.vtable))
    } > REGION_DATA

    .text : {
        CREATE_OBJECT_SYMBOLS
        KEEP (*(.text))
        *(.text.*)
        . = ALIGN(0x4);
        KEEP (*(.ctors))
        . = ALIGN(0x4);
        KEEP (*(.dtors))
        . = ALIGN(0x4);
        __init_array_start = .;
        KEEP (*(.init_array*))
        __init_array_end = .;
        *(.init)
        *(.fini*)
    } > REGION_TEXT AT> REGION_TEXT

    .rodata : {
        *(.rodata)
        *(.rodata.*)
    } > REGION_TEXT AT> REGION_TEXT

    .ARM.exidx : {
        __exidx_start = .;
        *(.ARM.exidx* .gnu.linkonce.armexidx.*)
        __exidx_end = .;
    } > REGION_ARM_EXIDX AT> REGION_ARM_EXIDX

    .ARM.extab : {
        *(.ARM.extab* .gnu.linkonce.armextab.*)
    } > REGION_ARM_EXTAB AT> REGION_ARM_EXTAB

    __etext = .;

    .data : {
        __data_load__ = LOADADDR (.data);
        __data_start__ = .;
        KEEP (*(.data))
        KEEP (*(.data*))
        . = ALIGN (4);
        __data_end__ = .;
    } > REGION_DATA AT> REGION_TEXT

    .bss : {
        __bss_start__ = .;
        *(.shbss)
        KEEP (*(.bss))
        *(.bss.*)
        *(COMMON)
        . = ALIGN (4);
        __bss_end__ = .;
    } > REGION_BSS AT> REGION_BSS

    .heap : {
        __heap_start__ = .;
        end = __heap_start__;
        _end = end;
        __end = end;
        KEEP (*(.heap))
        __heap_end__ = .;
        __HeapLimit = __heap_end__;
    } > REGION_HEAP AT> REGION_HEAP

    .stack (NOLOAD) : ALIGN(0x8) {
        _stack = .;
        __stack = .;
        KEEP(*(.stack))
    } > REGION_STACK AT> REGION_STACK
}
			"""

		template = ''
		for line in auxTemplate.splitlines( ):
			template += line.rstrip( )
			template += '\n'

		return template

	def _GenerateTrxmakeTemplate( self ):
		auxTemplate =						\
			"""{							\
			\n\t"name": "%s", 				\
			\n\t"modules" : [ ],			\
			\n\t"defines" : [ ]				\
			\n}"""							\
			%( self.modName )

		template = ''
		for line in auxTemplate.splitlines( ):
			template += line.rstrip( )
			template += '\n'

		return template

	def _GenerateHeaderTemplate( self ):
		auxTemplate =						\
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

		template = ''
		for line in auxTemplate.splitlines( ):
			template += line.rstrip( )
			template += '\n'

		return template

	def _GenerateSourceTemplate( self, app = False ):
		auxTemplate = ''
		if True == app:
			auxTemplate = 												\
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
				\nint main( void ) {									\
				\n 														\
				\n\treturn 0;											\
				\n}														\
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
		else:
			auxTemplate = 												\
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

		template = ''
		for line in auxTemplate.splitlines( ):
			template += line.rstrip( )
			template += '\n'

		return template		

class Builder:	
	def __init__( self, build_file = None, platform = "HOST", buildtype = "app" ):
		self.build_file = build_file
		self.platform = platform
		self.buildtype = buildtype
		self.attributes = { "name": 		None,
							"specs":		None,
							"cpu": 			None,
							"arch": 		None,
							"march":		None,
							"mfloat_abi":	None,
							"mfpu":			None,
							"cc":			"gcc",
							"modules":		[],
							"defines": 		[] }
		self._ParseBuild( )

	def _ParseBuild( self ):
		self._ParseBuildFile( )
		self._ParsePlatform( )
		self._ParseCpu( )

	def _ParseBuildFile( self ):
		if( None != self.build_file ):
			file = open( self.build_file )
			data = json.load( file )				
			file.close()

			if "modules" in data.keys():
				self.attributes[ "modules" ] 	= data[ "modules" ]
			if "defines" in data.keys():
				self.attributes[ "defines" ]	= data[ "defines" ]
			if "name" in data.keys():
				self.attributes[ "name" ]		= data[ "name" ]

		if( "app" == self.buildtype and None == self.attributes[ "name" ] ):
			self.attributes[ "name" ] = "app"			

	def _ParsePlatform( self ):
		if( "MSP432" == self.platform ):
			self.attributes[ "specs" ] 	= "nosys.specs"
			self.attributes[ "cpu" ] 	= "cortex-m4"

	def _ParseCpu( self ):
		if( "cortex-m4" == self.attributes[ "cpu" ] ):
			self.attributes[ "arch" ] 		= "thumb"
			self.attributes[ "march" ] 		= "armv7e-m"
			self.attributes[ "mfloat_abi" ] 	= "hard"
			self.attributes[ "mfpu" ] 		= "fpv4-sp-d16"
			self.attributes[ "cc" ] 		= "arm-none-eabi-gcc"

	def _GenerateSourcesChunk( self ):
		outString = 														\
			"""# This is a trxmake autogenerated file; take care editing.\n	\
			\nSRCDIR = ./../src												\
			\nINCDIR = ./../inc												\
			\nOBJDIR = ./obj												\
			\n																\
			\nSRCS := $(wildcard $(SRCDIR)/*.c)								\
			\n\n"""

		outString += "INCS  = -I$(INCDIR)\n"
		for mod in self.attributes[ "modules" ]:
			outString += "INCS += -I{module}/inc\n".format( module = mod )
		outString += '\n'

		outString += "OBJS := $(SRCS:.c=.o)\n"
		for mod in self.attributes[ "modules" ]:
			outString += "OBJS += $(wildcard {module}/build/obj/*.o)\n".format( module = mod )
		outString += '\n'

		outString +=														\
			"""PREPROS := $(SRCS:.c=.i)										\
			\nASMS := $(SRCS:.c=.asm)										\
			\n\n"""

		return outString

	def _GenerateFlagsChunk( self ):
		outString = ''
		outString += "CC = {cc}\n".format( cc = self.attributes[ "cc"] )
		if( "app" == self.buildtype and "HOST" != self.platform ):
			outString += "LD = arm-none-eabi-ld\n"
		outString += "\n"

		outString += "CCPFLAGS  = -D{platform}\n".format( platform = self.platform )
		for define in self.attributes[ "defines" ]:
			outString += "CPPFLAGS += -D{defi}\n".format( defi = define )
		outString += '\n'

		outString += "CFLAGS  = -g -Wall -Werror -std=c99 $(INCS)"
		if( "HOST" != self.platform ):
			outString += 														\
				"""\nCFLAGS += -mcpu={cpu} -m{arch} -march={march}					\
				\nCFLAGS += -mfloat-abi={mfloat_abi} -mfpu={mfpu}				\
				\nCFLAGS += --specs={specs}										\
				"""																\
				.format( 	cpu 		= self.attributes[ "cpu" ],				\
							arch 		= self.attributes[ "arch" ],			\
							march 		= self.attributes[ "march" ],			\
							mfloat_abi 	= self.attributes[ "mfloat_abi" ],		\
							mfpu 		= self.attributes[ "mfpu" ],			\
							specs 		= self.attributes[ "specs" ] )		
		outString += '\n'

		auxString = ''
		if( "app" == self.buildtype ):			
			auxString += "LDFLAGS = -Wl,-Map={name}.map".format( name = self.attributes[ "name" ] )
			if( "HOST" != self.platform ):
				auxString += " -T {name}.lds".format( name = self.platform )
		outString += auxString

		outString += '\n'

		return outString

	def _GenerateDirectives( self ):
		outString = ''
		outString += self._GenerateDirectivePreprocessor( )
		outString += self._GenerateDirectiveAssembly( )
		outString += self._GenerateDirectiveObjects( )
		outString += '\n'

		return outString

	def _GenerateDirectivePreprocessor( self ):
		outString = 															\
			"""																	\
			\n# Get post-preprocessing file.									\
			\n%.i : %.c															\
			\n\tmkdir -p prepro/												\
			\n\t$(CC) -E -o $@ $(CPPFLAGS) $(CFLAGS) $^							\
			\n\tmv $@ prepro/													\
			\n																	\
			"""

		return outString

	def _GenerateDirectiveAssembly( self ):
		outString = 															\
			"""																	\
			\n# Get assembly code.												\
			\n%.asm : %.c														\
			\n\tmkdir -p asm/													\
			\n\t$(CC) -S -o $@  $(CPPFLAGS) $(CFLAGS) $^						\
			\n\tmv $@ asm/														\
			\n																	\
			"""

		return outString

	def _GenerateDirectiveObjects( self ):
		outString = 															\
			"""\n# Get object files and generate dependencies (*.d)				\
			\n%.o : %.c															\
			\n\tmkdir -p obj/													\
			\n\tmkdir -p depens/												\
			\n\t$(CC) -MD -c -MF $*.d -o $@ $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $^	\
			"""
		if "app" == self.buildtype:
			outString += 														\
			"""\n\t# Objects need to remain in the source directory for later linking. (little bug but working.)	\
			\n\tcp $@ obj/														\
			"""
		else:
			outString += 														\
			"""\n\tmv $@ obj/														\
			"""
		outString += "\n\tmv $*.d depens/"

		return outString

	def _GenerateCommands( self ):
		outString = ''
		outString += self._GenerateCommandBuild( )
		outString += self._GenerateCommandAll( )
		outString += self._GenerateCommandClean( )
		outString += '\n'

		return outString

	def _GenerateCommandBuild( self ):
		outString = 															\
		"""\n# Build the guy.													\
		\n.PHONY: build															\
		"""

		if "app" == self.buildtype:
			outString += 														\
			"""																	\
			\nbuild: {name}.elf													\
			\n{name}.elf : $(OBJS)												\
			\n\tmkdir -p bin/													\
			\n\tmkdir -p map/													\
			\n\t$(CC) -o $@ $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $^					\
			\n\tmv $@ bin/														\
			\n\tmv {name}.map map/												\
			\n\t# Remove object files from the source directory, not needed anymore after linking.	\
			\n\trm ../src/*.o													\
			""".format( name = self.attributes[ "name" ] )
		else:
			outString += "\nbuild: $(OBJS)"

		outString += '\n'

		return outString

	def _GenerateCommandAll( self ):
		outString = ''
		outString += 															\
		"""																		\
		\n# Generate all files.													\
		\n.PHONY: all 															\
		\nall: $(OBJS) $(ASMS) $(PREPROS)										\
		"""
		outString += '\n'

		return outString

	def _GenerateCommandClean( self ):
		outString = ''
		outString += 															\
		"""																		\
		\n# Cleanning.															\
		\n.PHONY: clean 														\
		\nclean:																\
		"""

		if "app" == self.buildtype:
			outString += "\n\trm -fr bin/ prepro/ asm/ obj/ depens/ map/"
		else:
			outString += "\n\trm -fr prepro/ asm/ obj/ depens/"

		outString += '\n'

		return outString

	def GenerateMakefile( self ):		
		outString = 	self._GenerateSourcesChunk( )
		outString += 	self._GenerateFlagsChunk( )
		outString += 	self._GenerateDirectives( )
		outString += 	self._GenerateCommands( )

		makefile = ''
		for line in outString.splitlines( ):
			makefile += line.rstrip( )
			makefile += '\n'

		makefilePath = os.path.dirname( os.path.abspath( self.build_file ) )
		file = open( makefilePath + "/Makefile", 'w' )
		file.write( makefile )
		file.close( )

	def Make( self ):
		makefilePath = os.path.dirname( os.path.abspath( self.build_file ) )

		cwd = os.getcwd( )
		os.chdir( makefilePath )
		os.system( "make clean")
		os.system( "make")
		os.chdir( cwd )

	def GetAttributes( self ):
		return self.attributes

	def SetModules( self, modulesSet ):
		self.attributes[ "modules" ] = modulesSet

parser = argparse.ArgumentParser( description = ''' trxmake 1.0 :: TRX build app. ''' )
parser.add_argument( 	'-c',
						'--command',
						type = str,
						choices = [ "genmod", "build" ],
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
parser.add_argument(	'-f',
						'--file',
						type = str,
						default = None,
						help = 'Build file.'
					)
parser.add_argument(	'--platform',
						type = str,
						choices = [ "HOST", "MSP432" ],
						default = "HOST",
						help = 'Platform we are building for.'
					)
parser.add_argument(	'-M',
						'--Make',
						type = str,
						choices = [ "True", "False" ],
						default = "True",
						help = "Build (Make) the thing.")
parser.add_argument(	'-a',
						'--app',
						type = str,
						choices = [ "True", "False" ],
						default = "False",
						help = "The module is actually an app.")						
args = parser.parse_args( )
def main( args ):
	if "genmod" == args.command:
		modGen = C_ModuleGenerator( modName = args.module, parentFolder = args.parent, platform = args.platform, app = True if args.app == 'True' else False )
		modGen.GenerateModule( )
	elif "build" == args.command:
		appBuilder = Builder( build_file = args.file, platform = args.platform, buildtype =  "app" )
		modsSet = set( appBuilder.GetAttributes( )[ "modules" ] )
		auxModSet = set( modsSet )
		# Get all modules
		for mod in modsSet:
			trxmakeFile = mod + "/build/trxmake.json"
			modBuilder = Builder( build_file = trxmakeFile, platform = args.platform, buildtype =  "mod" )
			auxModSet |= set( modBuilder.GetAttributes( )[ "modules" ] )
			del modBuilder
		# Generate all mod makefiles
		for mod in auxModSet:
			trxmakeFile = mod + "/build/trxmake.json"
			modBuilder = Builder( build_file = trxmakeFile, platform = args.platform, buildtype =  "mod" )
			modBuilder.GenerateMakefile( )
			if "True" == args.Make:
				modBuilder.Make( )
			del modBuilder
		appBuilder.SetModules( auxModSet )
		appBuilder.GenerateMakefile( )
		if "True" == args.Make:
			appBuilder.Make( )
		del appBuilder
	else:
		parser.print_help()

if __name__ == "__main__":
	main( args )

### end of file ###
