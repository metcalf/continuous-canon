/*  Canon Inkjet Printer Driver for Linux
 *  Copyright CANON INC. 2001-2010
 *  All Rights Reserved.
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; version 2 of the License.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307, USA.
 *
 * NOTE:
 *  - As a special exception, this program is permissible to link with the
 *    libraries released as the binary modules.
 *  - If you write modifications of your own for these programs, it is your
 *    choice whether to permit this exception to apply to your modifications.
 *    If you do not wish that, delete this exception.
 */


void UtilCleaning(LPUIDB uidb);
void UtilRefreshing(LPUIDB uidb);
void UtilNozzleCheck(LPUIDB uidb);
void UtilHeadAdjust(LPUIDB uidb);
void UtilRollerCleaning(LPUIDB uidb);
void UtilPowerOff(LPUIDB uidb);
void UtilAutoPower(LPUIDB uidb);
void UtilSetConfig(LPUIDB uidb);
void UtilInkReset(LPUIDB uidb);
void UtilInkWarning(LPUIDB uidb);
void UtilQuietMode(LPUIDB uidb);
void UtilPlateCleaning(LPUIDB uidb);
void UtilInkCartridgeSet( LPUIDB uidb );
int UtilMessageBox(char *message, char *title, unsigned int flag);

void init_autopower_settings(void);			
void init_autopower_type2_settings(void);	
void init_inkwarning_settings(void);	
void init_quiet_settings(void);				
void init_papergap_settings(void);			
void init_manual_head_settings(void);		
void init_drylevel_value(void);				
void init_ink_cartridge_settings( void );	

void init_pss_value( void );
void init_roller_cleaning_type_a_value( void );
void init_nozzle_check_type_a_value( void );
void init_permit_cancel_dialog_value( void );

short isAllOutputSetTime( char *modelName );

#define	ID_OK		1
#define	ID_CANCEL	2
#define	ID_ABORT	3
#define	ID_RETRY	4
#define	ID_IGNORE	5
#define	ID_YES		6
#define	ID_NO		7

#define	MB_ICON_INFORMATION	0x00000000L
#define	MB_ICON_EXCLAMATION	0x00000001L
/* Ver.2.90 */
#define	MB_ICON_QUESTION	0x00000002L
#define MB_ICON_SYSERR		0x00000003L
/* Ver.3.00 */
#define	MB_ICON_NO			0x00000004L

#define	MB_OK				0x00000010L
#define	MB_CANCEL			0x00000020L
#define	MB_YES				0x00000040L
#define	MB_NO				0x00000080L
#define	MB_ABORT			0x00000100L
#define	MB_RETRY			0x00000200L
#define	MB_IGNORE			0x00000400L
