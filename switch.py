#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  switch.py
#  
#  Copyright 2022  <pi@RPi3ShedPower>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

heatersOn = False
checkFail = False
switchNumber = config.switchNumberHeaters
id = config.switchIdHeaters
code = config.codeHeaters
stateWanted = False
heatersOn, successfullResult, offLine = cloud.operateSwitch(switchNumber,id,code,stateWanted)
if successfullResult:
	print("Heaters Switch Working")
else:
	print("Heaters Operation Fail")
	checkFail = True
if offLine:
	print("Heaters  Switch is offLine")
	checkFail = True

if checkFail and config.useHeaters:
	print("Heaters required but initial start up test failed")
	sys_exit()
elif checkFail:
	print("Heaters not available but not required according Config File")
def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
