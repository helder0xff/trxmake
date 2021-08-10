/**
 * @file	screw.c
 * @author	helder
 * @date	2021-07-22
 * @brief	??
 */

/* Includes go here.	*/
#include <screw.h>
#include <screw_head.h>
#include <screw_body.h>
#include <stdio.h>

/* typedefs go here.	*/

/* Consts go here.	*/

/* #defines go here.	*/

/* static vars go here.	*/

/* static function declarations go here.	*/

/* non static function implementation go here.	*/

void screw_print( void ) {
    printf("%s\n", "I am a SCREW.");
    screw_head_print( );
    screw_body_print( );
}

/* static function implementation go here.	*/

//*** end of file ***//
