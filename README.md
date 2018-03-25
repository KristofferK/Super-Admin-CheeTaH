# Super-Admin-CheeTaH
Admin script for Eventscripts Python I made back in 2010. Eventscripts is shutting down, so I'm moving the code to Github

## Description
A lot of my friends had problems with Super Admin (http://forums.eventscripts.com/viewtopic.php?t=25818), so I chose to update it into ESP, remove the need of EST, make it supprt multiple-language (INI). I did get a lot of inspiration from Super Admin. The default command to open admin is /sac, but it can be changed in the CFG.

## Features
Features can be seen in the following video. Please note that the video isn't made nor uploaded by me.

[![Youtube Video of SAC](https://img.youtube.com/vi/k__3fb00DVw/0.jpg)](https://www.youtube.com/watch?v=k__3fb00DVw)

## Installation
* Extract to cstrike\
* Edit your cstrike\cfg\eventscripts\super_admin_cheetah\config.cfg
* Edit your cstrike\addons\eventscripts\super_admin_cheetah\admins.txt to the admins you want on the server
* Put "es_xload super_admin_cheetah" in your cstrike\cfg\autoexec.cfg
* Restart your server

## Version Notes For 3.1
* Fixed ban. Forgot to change this to steamid3.
* Remove burn, gravity and disarm. Seems like es.fire doesn't work properly?
* Fixed not being able to add admins with | in their name.
* Fixed not being able to ban players with | in their name.
