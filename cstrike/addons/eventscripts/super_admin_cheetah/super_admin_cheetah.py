# This file shouldn't be edited - Editing it may cause script not to work!
# For editing please check ../cfg/eventscripts/super_admin_cheetah/config.cfg

import es
import cfglib
import cmdlib
import random
import langlib
import usermsg
import popuplib
import effectlib
import playerlib
import gamethread
from path import path
from time import strftime

import os
OpSys = "Windows" if os.name == "nt" else "Linux" if os.name == "posix" else os.name

import psyco
psyco.full()

addonpath = "super_admin_cheetah"
cfgpath = es.getAddonPath(addonpath).replace("\\addons", "\\cfg").replace("/addons", "/cfg")
PageThatTeleportAndSavelocIsOn = 3

PlayedSeconds = 0
PlayedSeconds2 = 0
SAC_Dict_Shaking = {}
SAC_Dict_Ammo = {}
SAC_Dict_Regeneration = {}
SAC_Dict_Disguise = {}
SAC_Dict_Blind = {}
SAC_Dict_Saveloc = {}
SAC_Dict_Drug = {}
SAC_Dict_Freeze = {}
SAC_Dict_Mute = {}
SAC_Dict_Ban = {}
SAC_Dict_Give = {}

variables = [
        ["sac_version","v3.1CheeTaH-Public","Script version.",1],
        ["sac_consolecommand","0","Command brought by SAC",0],
        ["sac_saycommand","0","Command brought by SAC",0],
        ["sac_standard_flags","0","Command brought by SAC",0],
        ["sac_cmd_respawn","0","Command brought by SAC",0],
        ["sac_cmd_godmode","0","Command brought by SAC",0],
        ["sac_cmd_speed","0","Command brought by SAC",0],
        ["sac_cmd_jetpack","0","Command brought by SAC",0],
        ["sac_cmd_invisible","0","Command brought by SAC",0],
        ["sac_cmd_shake","0","Command brought by SAC",0],
        ["sac_cmd_unlimitedammo","0","Command brought by SAC",0],
        ["sac_cmd_regeneration","0","Command brought by SAC",0],
        ["sac_cmd_disguise","0","Command brought by SAC",0],
        ["sac_cmd_bury","0","Command brought by SAC",0],
        ["sac_cmd_blind","0","Command brought by SAC",0],
        ["sac_cmd_kill","0","Command brought by SAC",0],
        ["sac_cmd_saveloc","0","Command brought by SAC",0],
        ["sac_cmd_teleport","0","Command brought by SAC",0],
        ["sac_cmd_drug","0","Command brought by SAC",0],
        ["sac_cmd_slap","0","Command brought by SAC",0],
        ["sac_cmd_setcash","0","Command brought by SAC",0],
        ["sac_cmd_addcash","0","Command brought by SAC",0],
        ["sac_cmd_takecash","0","Command brought by SAC",0],
        ["sac_cmd_sethealth","0","Command brought by SAC",0],
        ["sac_cmd_addhealth","0","Command brought by SAC",0],
        ["sac_cmd_takehealth","0","Command brought by SAC",0],
        ["sac_cmd_freeze","0","Command brought by SAC",0],
        ["sac_cmd_noclip","0","Command brought by SAC",0],
        ["sac_cmd_message","0","Command brought by SAC",0],
        ["sac_cmd_message_center","0","Command brought by SAC",0],
        ["sac_cmd_message_private","0","Command brought by SAC",0],
        ["sac_cmd_kick","0","Command brought by SAC",0],
        ["sac_cmd_mute","0","Command brought by SAC",0],
        ["sac_cmd_ban","0","Command brought by SAC",0],
        ["sac_cmd_sptot","0","Command brought by SAC",0],
        ["sac_cmd_spts","0","Command brought by SAC",0],
        ["sac_cmd_sptt","0","Command brought by SAC",0],
        ["sac_cmd_sptct","0","Command brought by SAC",0],
        ["sac_cmd_map","0","Command brought by SAC",0],
        ["sac_cmd_currentmap","0","Command brought by SAC",0],
        ["sac_cmd_timeleft","0","Command brought by SAC",0],
        ["sac_cmd_thetime","0","Command brought by SAC",0],
        ["sac_cmd_teleportto","0","Command brought by SAC",0],
        ["sac_cmd_unban","0","Command brought by SAC",0],
        ["sac_cmd_unban2","0","Command brought by SAC",0],
        ["sac_cmd_give","0","Command brought by SAC",0],
    ]

ini = cfglib.AddonINI(es.getAddonPath(addonpath) + '/translations.ini')
translations = langlib.Strings(ini)

AddPropProps = 2

_frozen_model = 'materials/sprites/lgtning.vmt' # Model used when someone is frozen
_frozen_halo = 'materials/sprites/blueglow1.vmt' # Halo used when someone is frozen
_frozen_colorR = 0 # how red the lasers are
_frozen_colorG = 0 # how green the lasers are
_frozen_colorB = 255 # how blue the lasers are
_frozen_width = 10 # how width the start of the beam is
_frozen_endwidth = 10 # how width the end of the beam is
_frozen_alpha = 255 # alpha of the beam
_frozen_speed = 10 # speed of the beam
_frozen_fadelenght = 0 # fade lenght of the beam
_frozen_noise = 10 # noise of the beam - 0 = totally straight. 50 = very curvy
_frozen_framestart = 0 # framestart of the beam
_frozen_framerate = 10 # framerate of the beam
_frozen_dis = 80 # how long the beams are
    
def load():
    SetUpVariables()
    for Player in playerlib.getUseridList('#human'): tell(Player, translations('load_msg', {'version':es.ServerVar("sac_version")}, Lang(Player)))
    es.server.insertcmd("mp_restartgame 1")
    gamethread.delayedname(4, "Updater", Updater)
    gamethread.delayedname(4, "Muter", Muter)
    gamethread.delayedname(1, "SecsP", SecsP)
    es.addons.registerTickListener(tickListener)
    global SACMenu_Main
    SACMenu_Main = popuplib.easymenu('SACMenu_Main',None, MenuHandler1)
    SACMenu_Main.settitle("- Super Admin CheeTaH")
    SACMenu_Main.addoption('Player Management', "Player Management")
    SACMenu_Main.addoption('Fun Commands', "Fun Commands")
    SACMenu_Main.addoption('Music', "Music")
    SACMenu_Main.addoption('Propmenu', "Propmenu")
    SACMenu_Main.addoption('Mini-Games', "Mini-Games")
    SACMenu_Main.addoption('Change Map', "Change Map")
    SACMenu_Main.addoption('Admin Management', "Admin Management")
    
    global SACMenu_ChangeMap
    SACMenu_ChangeMap = popuplib.easymenu('SACMenu_ChangeMap',None, ChangeMap)
    SACMenu_ChangeMap.submenu(10, SACMenu_Main)
    SACMenu_ChangeMap.settitle('- Super Admin CheeTaH')
    SACMenu_ChangeMap.setdescription("-- Change Map", lang=None)
    mapPath = path(es.ServerVar('eventscripts_gamedir')).joinpath('maps')
    for MapName in mapPath.walkfiles("*.bsp"):
        if es.exists('map', MapName.namebase): SACMenu_ChangeMap.addoption(MapName.namebase, MapName.namebase)
    
    global SACMenu_PM
    SACMenu_PM = popuplib.easymenu('SACMenu_PM',None, MenuHandler4)
    SACMenu_PM.submenu(10, SACMenu_Main)
    SACMenu_PM.settitle("- Super Admin CheeTaH")
    SACMenu_PM.setdescription("-- Player Management")
    SACMenu_PM.addoption('Ban', "Ban")
    SACMenu_PM.addoption('UnBan', "UnBan")
    SACMenu_PM.addoption('Kick', "Kick")
    SACMenu_PM.addoption('Mute', "Mute")
    SACMenu_PM.addoption('Swap Player To Opposite Team', "Swap Player To Opposite Team")
    SACMenu_PM.addoption('Swap Player To Spectator', "Swap Player To Spectator")
    SACMenu_PM.addoption('Swap Player To T', "Swap Player To T")
    SACMenu_PM.addoption('Swap Player To CT', "Swap Player To CT")
    
    global SACMenu_Items
    SACMenu_Items = popuplib.easymenu('SACMenu_Items',None, MenuHandlerChooseItem)
    SACMenu_Items.submenu(10, SACMenu_PM)
    SACMenu_Items.settitle("- Super Admin CheeTaH")
    SACMenu_Items.setdescription("-- Fun Commands \n--- Give Weapon")
    SACMenu_Items.addoption("weapon_ak47", "Ak47")
    SACMenu_Items.addoption("weapon_aug", "Aug")
    SACMenu_Items.addoption("weapon_awp", "Awp")
    SACMenu_Items.addoption("weapon_deagle", "Deagle")
    SACMenu_Items.addoption("item_defuser", "Defuser")
    SACMenu_Items.addoption("weapon_elite", "Elite")
    SACMenu_Items.addoption("weapon_famas", "Famas")
    SACMenu_Items.addoption("weapon_fiveseven", "Fiveseven")
    SACMenu_Items.addoption("weapon_flashbang", "Flashbang")
    SACMenu_Items.addoption("weapon_galil", "Galil")
    SACMenu_Items.addoption("weapon_glock", "Glock")
    SACMenu_Items.addoption("weapon_hegrenade", "Hegrenade")
    SACMenu_Items.addoption("weapon_m249", "M249")
    SACMenu_Items.addoption("weapon_m3", "M3")
    SACMenu_Items.addoption("weapon_m4a1", "M4a1")
    SACMenu_Items.addoption("weapon_mac10", "Mac10")
    SACMenu_Items.addoption("weapon_mp5navy", "Mp5navy")
    SACMenu_Items.addoption("weapon_p228", "P228")
    SACMenu_Items.addoption("weapon_p90", "P90")
    SACMenu_Items.addoption("weapon_scout", "Scout")
    SACMenu_Items.addoption("weapon_sg550", "Sg550")
    SACMenu_Items.addoption("weapon_552", "Sg552")
    SACMenu_Items.addoption("weapon_smokegrenade", "Smokegrenade")
    SACMenu_Items.addoption("weapon_tmp", "Tmp")
    SACMenu_Items.addoption("weapon_ump45", "Ump45")
    SACMenu_Items.addoption("weapon_usp", "Usp")
    SACMenu_Items.addoption("weapon_xm1014", "Xm1014")
    
    global SACMenu_BanTime
    SACMenu_BanTime = popuplib.easymenu('SACMenu_BanTime',None, MenuHandlerChooseBanTime)
    SACMenu_BanTime.submenu(10, SACMenu_PM)
    SACMenu_BanTime.settitle("- Super Admin CheeTaH")
    SACMenu_BanTime.setdescription("-- Player Management\n--- Ban")
    SACMenu_BanTime.addoption('0', 'Permanent [0]')
    SACMenu_BanTime.addoption('5', '5 Minutes [5]')
    SACMenu_BanTime.addoption('30', 'Half An Hour [30]')
    SACMenu_BanTime.addoption('60', 'An Hour [60]')
    SACMenu_BanTime.addoption('1440', 'A Day [1440]')
    SACMenu_BanTime.addoption('2880', 'Two Days [2880]')
    SACMenu_BanTime.addoption('10080', 'A Week [10080]')
    SACMenu_BanTime.addoption('43200', 'A Month [43200]')
    SACMenu_BanTime.addoption('518400', 'A Year [518400]')
    
    global SACMenu_Fun
    SACMenu_Fun = popuplib.easymenu('SACMenu_Fun',None, MenuHandler3)
    SACMenu_Fun.submenu(10, SACMenu_Main)
    SACMenu_Fun.settitle("- Super Admin CheeTaH")
    SACMenu_Fun.setdescription("-- Fun Commands")
    SACMenu_Fun.addoption('Blind', "Blind")
    SACMenu_Fun.addoption('Bury', "Bury")
    SACMenu_Fun.addoption('Disguise', "Disguise")
    SACMenu_Fun.addoption('Drug', "Drug")
    SACMenu_Fun.addoption('Freeze', "Freeze")
    SACMenu_Fun.addoption('Give Weapon', "Give Weapon")
    SACMenu_Fun.addoption('Godmode', "Godmode")
    SACMenu_Fun.addoption('Invisible', "Invisible")
    SACMenu_Fun.addoption('Jetpack', "Jetpack")
    SACMenu_Fun.addoption('Noclip', "Noclip")
    SACMenu_Fun.addoption('Regeneration', "Regeneration")
    SACMenu_Fun.addoption('Respawn', "Respawn")
    SACMenu_Fun.addoption('Shake', "Shake")
    SACMenu_Fun.addoption('Skins', "Skins")
    SACMenu_Fun.addoption('Slap', "Slap")
    SACMenu_Fun.addoption('Slay', "Slay")
    SACMenu_Fun.addoption('Speed', "Speed")
    SACMenu_Fun.addoption('Save Location', "Tele: Save Location")
    SACMenu_Fun.addoption('Teleport', "Tele: Teleport")
    SACMenu_Fun.addoption('Unlimited Ammo', "Unlimited Ammo")
    
    global SACMenu_Music
    SACMenu_Music = popuplib.easymenu('SACMenu_Music',None, MusicPlayer)
    SACMenu_Music.submenu(10, SACMenu_Main)
    SACMenu_Music.settitle("- Super Admin CheeTaH")
    SACMenu_Music.setdescription("-- Music")
    AddedProps = 0
    File = open(cfgpath + '/soundlist.txt')
    for CurrentLine in File.readlines():
        if CurrentLine.startswith('"'):
            SplittedLine = CurrentLine.split('"')
            if len(SplittedLine) == 5:
                Page = AddedProps / 7 + 1
                AddedProps += 1
                SACMenu_Music.addoption('%s|%s|%s' %(SplittedLine[1],SplittedLine[3],str(Page)), SplittedLine[1])
                
    global SACMenu_Propmenu
    SACMenu_Propmenu = popuplib.easymenu('SACMenu_Propmenu',None, PropCreator)
    SACMenu_Propmenu.submenu(10, SACMenu_Main)
    SACMenu_Propmenu.settitle("- Super Admin CheeTaH")
    SACMenu_Propmenu.setdescription("-- Prop Menu")
    
    if (str(OpSys).lower() == "windows"): SACMenu_Propmenu.addoption("1--DelThis", "   Delete This Prop")
    else: SACMenu_Propmenu.addoption("1--DelThis", "   Delete This Prop [Only available on Windows. Sorry!]", 0)
    SACMenu_Propmenu.addoption("1--DelAll", "   Delete All")
    File = open(cfgpath + '/propslist.txt')
    for CurrentLine in File.readlines():
        if CurrentLine.startswith('"'):
            SplittedLine = CurrentLine.split('"')
            if len(SplittedLine) == 7: AddProp(SplittedLine[1],SplittedLine[3],SplittedLine[5])
            
    global SACMenu_SkinsMenu
    SACMenu_SkinsMenu = popuplib.easymenu('SACMenu_SkinsMenu',None, SACMenu_SkinsMenu_Selected)
    SACMenu_SkinsMenu.submenu(10, SACMenu_Fun)
    SACMenu_SkinsMenu.settitle("- Super Admin CheeTaH")
    SACMenu_SkinsMenu.setdescription("-- Fun Commands\n--- Skins")
    File = open(cfgpath + '/skinslist.txt')
    for CurrentLine in File.readlines():
        if CurrentLine.startswith('"'):
            SplittedLine = CurrentLine.split('"')
            if len(SplittedLine) == 5:
                SACMenu_SkinsMenu.addoption("%s|%s" %(SplittedLine[1],SplittedLine[3]), SplittedLine[1])
    
    global SACMenu_MiniGames
    SACMenu_MiniGames = popuplib.easymenu('SACMenu_MiniGames',None, MenuHandler1)
    SACMenu_MiniGames.submenu(10, SACMenu_Main)
    SACMenu_MiniGames.settitle("- Super Admin CheeTaH")
    SACMenu_MiniGames.setdescription("-- Mini Games")
    SACMenu_MiniGames.addoption('Wolves VS Sheeps', "Wolves VS Sheeps")
    SACMenu_MiniGames.addoption('Mini Zombiemod', "Mini Zombiemod")
    SACMenu_MiniGames.addoption('Stop MiniGames', "Stop the current game")
    
    global SACMenu_AdminManagement
    SACMenu_AdminManagement = popuplib.easymenu('SACMenu_AdminManagement',None, MenuHandler2)
    SACMenu_AdminManagement.submenu(10, SACMenu_Main)
    SACMenu_AdminManagement.settitle("- Super Admin CheeTaH")
    SACMenu_AdminManagement.setdescription("-- Admin Management")
    SACMenu_AdminManagement.addoption('List of admins', "List of Admins")
    SACMenu_AdminManagement.addoption('Add an Admin', "Add an Admin")
    SACMenu_AdminManagement.addoption('Remove an Admin', "Remove an Admin")
    
    cmdlib.registerClientCommand(es.ServerVar("sac_consolecommand"), client_cmd_openmenu, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_saycommand"), client_cmd_openmenu, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_respawn"), client_cmd_respawn, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_respawn"), client_cmd_respawn, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_godmode"), client_cmd_godmode, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_godmode"), client_cmd_godmode, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_speed"), client_cmd_speed, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_speed"), client_cmd_speed, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_jetpack"), client_cmd_jetpack, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_jetpack"), client_cmd_jetpack, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_invisible"), client_cmd_invisible, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_invisible"), client_cmd_invisible, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_shake"), client_cmd_shake, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_shake"), client_cmd_shake, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_unlimitedammo"), client_cmd_unlimitedammo, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_unlimitedammo"), client_cmd_unlimitedammo, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_regeneration"), client_cmd_regeneration, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_regeneration"), client_cmd_regeneration, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_disguise"), client_cmd_disguise, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_disguise"), client_cmd_disguise, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_bury"), client_cmd_bury, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_bury"), client_cmd_bury, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_blind"), client_cmd_blind, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_blind"), client_cmd_blind, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_kill"), client_cmd_kill, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_kill"), client_cmd_kill, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_saveloc"), client_cmd_saveloc, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_saveloc"), client_cmd_saveloc, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_teleport"), client_cmd_teleport, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_teleport"), client_cmd_teleport, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_teleportto"), client_cmd_teleportto, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_teleportto"), client_cmd_teleportto, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_drug"), client_cmd_drug, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_drug"), client_cmd_drug, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_slap"), client_cmd_slap, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_slap"), client_cmd_slap, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_setcash"), client_cmd_setcash, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_setcash"), client_cmd_setcash, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_addcash"), client_cmd_addcash, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_addcash"), client_cmd_addcash, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_takecash"), client_cmd_takecash, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_takecash"), client_cmd_takecash, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_give"), client_cmd_give, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_give"), client_cmd_give, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_sethealth"), client_cmd_sethealth, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_sethealth"), client_cmd_sethealth, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_addhealth"), client_cmd_addhealth, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_addhealth"), client_cmd_addhealth, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_takehealth"), client_cmd_takehealth, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_takehealth"), client_cmd_takehealth, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_freeze"), client_cmd_freeze, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_freeze"), client_cmd_freeze, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_noclip"), client_cmd_noclip, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_noclip"), client_cmd_noclip, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_message"), client_cmd_message, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_message"), client_cmd_message, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_message_private"), client_cmd_message_private, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_message_private"), client_cmd_message_private, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_message_center"), client_cmd_message_center, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_message_center"), client_cmd_message_center, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_ban"), client_cmd_ban, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_ban"), client_cmd_ban, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_unban"), client_cmd_unban, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_unban"), client_cmd_unban, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_kick"), client_cmd_kick, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_kick"), client_cmd_kick, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_mute"), client_cmd_mute, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_mute"), client_cmd_mute, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_sptot"), client_cmd_sptot, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_sptot"), client_cmd_sptot, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_spts"), client_cmd_spts, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_spts"), client_cmd_spts, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_sptt"), client_cmd_sptt, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_sptt"), client_cmd_sptt, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_sptct"), client_cmd_sptct, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_sptct"), client_cmd_sptct, "no comment...")
    cmdlib.registerClientCommand(es.ServerVar("sac_cmd_map"), client_cmd_map, "no comment...")
    cmdlib.registerSayCommand(es.ServerVar("sac_cmd_map"), client_cmd_map, "no comment...")
    cmdlib.registerServerCommand(es.ServerVar("sac_cmd_unban2"), server_cmd_unban, "Unbans a SteamID")

def unload():
    es.unload("%s/mini_zombiemod" %(str(addonpath)))
    es.unload("%s/wolves_vs_sheeps" %(str(addonpath)))
    gamethread.cancelDelayed("Updater")
    gamethread.cancelDelayed("Muter")
    gamethread.cancelDelayed("SecsP")
    es.addons.unregisterTickListener(tickListener)
    for Player in playerlib.getUseridList('#human'): tell(Player, translations('unload_msg', {'version':es.ServerVar("sac_version")}, Lang(Player)))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_consolecommand"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_saycommand"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_respawn"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_respawn"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_give"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_give"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_godmode"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_godmode"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_speed"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_speed"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_jetpack"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_jetpack"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_invisible"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_invisible"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_shake"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_shake"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_unlimitedammo"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_unlimitedammo"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_regeneration"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_regeneration"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_disguise"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_disguise"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_bury"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_bury"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_blind"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_blind"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_kill"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_kill"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_saveloc"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_saveloc"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_teleport"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_teleport"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_teleportto"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_teleportto"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_drug"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_drug"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_slap"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_slap"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_setcash"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_setcash"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_addcash"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_addcash"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_takecash"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_takecash"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_sethealth"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_sethealth"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_addhealth"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_addhealth"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_takehealth"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_takehealth"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_freeze"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_freeze"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_noclip"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_noclip"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_message"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_message"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_message_private"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_message_private"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_message_center"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_message_center"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_ban"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_ban"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_unban"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_unban"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_kick"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_kick"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_mute"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_mute"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_sptot"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_sptot"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_spts"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_spts"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_sptt"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_sptt"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_sptct"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_sptct"))
    cmdlib.unregisterClientCommand(es.ServerVar("sac_cmd_map"))
    cmdlib.unregisterSayCommand(es.ServerVar("sac_cmd_map"))
    cmdlib.unregisterServerCommand(es.ServerVar("sac_cmd_unban2"))
    
def es_map_start(ev):
    SetUpVariables()
    global PlayedSeconds
    PlayedSeconds = 1
def player_activate(ev):
    File = open(cfgpath + '/banned.txt')
    for CurrentLine in File.readlines():
        if CurrentLine.startswith('|[u:'):
            SplittedLine = CurrentLine.split('|')
            if len(SplittedLine) == 7:
                if str(SplittedLine[1]).lower() == str(ev['es_steamid']).lower():
                    es.server.insertcmd("kickid %s SAC BAN: %s/%s minutes left before you can play" %(ev['userid'],SplittedLine[4],SplittedLine[5]))
                    return
    gamethread.delayed(7, tell, (ev['userid'], translations('connect_msg', None, Lang(ev['userid']))))
def player_say(ev):
    userid = ev['userid']
    text = ev['text'].lower()
    if text == str(es.ServerVar("sac_cmd_currentmap")).lower(): tell(userid, translations('currentmap', {'map':es.ServerVar("eventscripts_currentmap")}, Lang(userid)))
    elif text == str(es.ServerVar("sac_cmd_timeleft")).lower():
        global PlayedSeconds
        TotalSeconds = int(es.ServerVar('mp_timelimit')) * 60
        if (TotalSeconds != 0):
            TotalLeftSeconds = TotalSeconds - PlayedSeconds
            LeftMinutes = TotalLeftSeconds / 60
            LeftSeconds = TotalLeftSeconds - LeftMinutes * 60
            if LeftMinutes < 0:
                LeftMinutes = 0
                LeftSeconds = 0
            TimeLeft = '%02d:%02d' %(LeftMinutes,LeftSeconds)
            tell(userid, translations('timeleft', {'timeleft':TimeLeft}, Lang(userid)))
        else: tell(userid, translations('timeleft_no_limit', None, Lang(userid)))
    elif text == str(es.ServerVar("sac_cmd_thetime")).lower(): tell(userid, translations('thetime', {'time':strftime("%d-%m-%Y %H:%M:%S (%I:%M %p)")}, Lang(userid)))
def player_spawn(ev):
    if not (es.exists('userid',ev['userid'])): return
    Player = int(ev['userid'])
    PlayerP = playerlib.getPlayer(Player)
    SAC_Dict_Shaking[int(Player)] = "0"
    SAC_Dict_Freeze[int(Player)] = "0"
    SAC_Dict_Ammo[int(Player)] = "0"
    SAC_Dict_Regeneration[int(Player)] = "0"
    SAC_Dict_Disguise[int(Player)] = "0"
    SAC_Dict_Blind[int(Player)] = 0
    SAC_Dict_Drug[int(Player)] = "0"
    es.cexec(ev['userid'], "r_screenoverlay normal")
    if PlayerP.getPrimary(): PlayerP.setWeaponColor(255, 255, 255, 255)
    elif PlayerP.getSecondary(): PlayerP.setWeaponColor(255, 255, 255, 255)
def player_death(ev):
    if not (es.exists('userid',ev['userid'])): return
    Player = int(ev['userid'])
    SAC_Dict_Shaking[int(Player)] = "0"
    SAC_Dict_Freeze[int(Player)] = "0"
    SAC_Dict_Ammo[int(Player)] = "0"
    SAC_Dict_Regeneration[int(Player)] = "0"
    SAC_Dict_Disguise[int(Player)] = "0"
    SAC_Dict_Blind[int(Player)] = 0
    SAC_Dict_Drug[int(Player)] = "0"
    es.cexec(Player, "r_screenoverlay normal")
def tell(userid, text): es.tell(userid, "#multi", "\x05SAC#default: "+str(text))
def ctell(userid, text): usermsg.centermsg(userid, "SAC: "+str(text))
def Lang(userid): return playerlib.getPlayer(userid).getLanguage()
def NotAdmin(userid): tell(userid, translations('not_admin', None, Lang(userid)))
def addAdmin(userid, adder):
    if not (es.exists('userid',userid)): return
    if (es.isbot(userid)):
        tell(adder, translations('added_admin_is_a_bot', {'added':es.getplayername(userid)}, Lang(adder)))
        return
    File = open(es.getAddonPath(addonpath) + '/admins.txt')
    for CurrentLine in File.readlines():
        if (str(CurrentLine).lower().startswith("|[u:")):
            SplittedLine = CurrentLine.split("|")
            if (len(SplittedLine) == 5):
                if (str(SplittedLine[1]).lower() == str(es.getplayersteamid(userid)).lower()):
                    tell(adder, translations('already_admin', {'added':es.getplayername(userid)}, Lang(adder)))
                    return
    for Player in playerlib.getUseridList('#human'): tell(Player, translations('added_admin', {'adder':es.getplayername(adder),'added':es.getplayername(userid)}, Lang(Player)))
    File = open(es.getAddonPath(addonpath) + '/admins.txt', 'a')
    File.write("\n\n// %s can not add admins. He has the name %s. He was added from ingame by %s(%s) on %s\n|%s|0|%s|%s" %(es.getplayersteamid(userid),es.getplayername(userid),es.getplayername(adder),es.getplayersteamid(adder),strftime("%Y-%m-%d %H:%M:%S"),es.getplayersteamid(userid),str(es.getplayername(userid)).replace('|',''),es.ServerVar("sac_standard_flags")))
    File.close()

def removeAdmin(removed, remover):
    File = open(es.getAddonPath(addonpath) + '/admins.txt')
    SLine = -1
    for CurrentLine in File.readlines():
        SLine += 1
        if (str(CurrentLine).lower().startswith("|[u:")):
            SplittedLine = CurrentLine.split("|")
            if (len(SplittedLine) == 5):
                if (str(SplittedLine[3]).lower() == str(removed).lower()):
                    # delete him from the file somehow
                    filehandle = open(es.getAddonPath(addonpath) + '/admins.txt', 'r')
                    filelines = filehandle.readlines()
                    filehandle.close()
                    del filelines[SLine]
                    filehandle = open(es.getAddonPath(addonpath) + '/admins.txt', 'w')
                    filehandle.writelines(filelines)
                    filehandle.close()
                    MenuHandler2(remover, 'Remove an Admin', None)
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('removed_admin', {'remover':es.getplayername(remover),'removed':str(SplittedLine[3])}, Lang(Player)))
                    return
    
def SetUpVariables():
    for var in variables:
        vari = es.ServerVar(var[0],var[1],var[2])
        vari.set(var[1])
        if (var[3] == 1): vari.makepublic()
    es.mexec("../cfg/eventscripts/%s/config.cfg" %(addonpath))
    File = open(cfgpath + '/soundlist.txt')
    for CurrentLine in File.readlines():
        if CurrentLine.startswith('"'):
            SplittedLine = CurrentLine.split('"')
            if len(SplittedLine) == 5:
                es.stringtable('downloadables', 'sound/'+SplittedLine[3])
    
def IsAdmin(userid):
    File = open(es.getAddonPath(addonpath) + '/admins.txt')
    for CurrentLine in File.readlines():
        if (str(CurrentLine).lower().startswith("|[u")):
            SplittedLine = CurrentLine.split("|")
            if (len(SplittedLine) == 5):
                if (str(SplittedLine[1]).lower() == str(es.getplayersteamid(userid)).lower()):
                    if SplittedLine[2] == "0": return 1
                    elif SplittedLine[2] == "1": return 2
    return 0
    
def getViewProp(userid):
    returnvalue = None
    if es.exists("userid", userid):
        entities = es.createentityindexlist()
        for entity in entities:
            entities[entity]["targetname"] = es.entitygetvalue(entity, "targetname")
        es.entsetname(userid, "viewed_prop")
        for entity in entities:
            if es.entitygetvalue(entity, "targetname") != "viewed_prop":
                continue
            returnvalue = entity
            es.entitysetvalue(entity, "targetname", entities[entity]["targetname"])
            break
    return returnvalue
    
    
def AddProp(Type,Name,Path):
    global AddPropProps
    Page = AddPropProps / 7 + 1
    AddPropProps += 1
    SACMenu_Propmenu.addoption("%s--%s|%s|%s" %(str(Page),Type,Name.lower(),Path), Name)
    
def SlayEffects(userid):
    if not es.exists("userid", userid): return
    UseridP = playerlib.getPlayer(userid)
    if (UseridP.isdead): return
    x,y,z = es.getplayerlocation(userid)
    es.fire(userid, "!self", "dispatcheffect", "explosion")
    es.effect("sparks", es.createvectorstring(x, y, z + 50), 10, 10, "0,0,0")
    effectlib.drawLine(es.createvectorstring(x, y, z + 500), es.createvectorstring(x, y, z), "materials/sprites/lgtning.vmt", "materials/sprites/blueglow1.vmt", 0.5, 10, 10, 255, 255, 255, 255, 10, 0, 10, 0, 10)
    es.emitsound("player", userid, "weapons/hegrenade/explode%i.wav" % random.randint(3, 5), 0.5, 0.5)
    es.emitsound("player", userid, "ambient/office/zap1.wav", 1, 0.5)
    UseridP.slay()
    
def Updater():
    for Player in playerlib.getUseridList('#alive'):
        if SAC_Dict_Drug[int(Player)] != "0": es.cexec(Player, "r_screenoverlay effects/tp_eyefx/tp_eyefx")
        if SAC_Dict_Shaking[int(Player)] != "0": usermsg.shake(Player, SAC_Dict_Shaking[int(Player)], 0.1)
        if SAC_Dict_Blind[int(Player)] != "0": usermsg.fade(Player, 2, 1, 100, 0, 0, 0, SAC_Dict_Blind[int(Player)])
        if SAC_Dict_Regeneration[int(Player)] != "0":
            if (int(playerlib.getPlayer(Player).getHealth()) < 100): playerlib.getPlayer(Player).setHealth(int(playerlib.getPlayer(Player).getHealth()) + 1)
        if SAC_Dict_Ammo[int(Player)] != "0":
            PlayerP = playerlib.getPlayer(Player)
            if PlayerP.getPrimary():
                PlayerP.setClip(PlayerP.getPrimary(), 999)
                PlayerP.setAmmo(PlayerP.getPrimary(), 0)
            if PlayerP.getSecondary():
                PlayerP.setClip(PlayerP.getSecondary(), 999)
                PlayerP.setAmmo(PlayerP.getSecondary(), 0)
        Players = playerlib.getUseridList('#alive,#human')
        if SAC_Dict_Freeze[int(Player)] != "0":
            xR,yR,zR = es.getplayerlocation(Player)
            xH = xR + _frozen_dis
            yH = yR + _frozen_dis
            zH = zR + _frozen_dis
            xL = xR - _frozen_dis
            yL = yR - _frozen_dis
            zL = zR - _frozen_dis
            ### Circles
            effectlib.drawCircle((xR, yR, zR), _frozen_dis, steps = 20, seconds = 0.11, width = _frozen_width, endwidth = _frozen_endwidth, red = _frozen_colorR, green = _frozen_colorG, blue = _frozen_colorB)
            effectlib.drawCircle((xR, yR, zH), _frozen_dis, steps = 20, seconds = 0.11, width = _frozen_width, endwidth = _frozen_endwidth, red = _frozen_colorR, green = _frozen_colorG, blue = _frozen_colorB)
            ### Vertical lines
            effectlib.drawLine((xR, yR, zR), (xR, yR, zH), _frozen_model, _frozen_halo, 0.11, _frozen_width, _frozen_endwidth, _frozen_colorR, _frozen_colorG, _frozen_colorB, _frozen_alpha, _frozen_speed, _frozen_fadelenght, _frozen_noise, _frozen_framestart, _frozen_framerate)
            effectlib.drawLine((xH, yR, zR), (xH, yR, zH), _frozen_model, _frozen_halo, 0.11, _frozen_width, _frozen_endwidth, _frozen_colorR, _frozen_colorG, _frozen_colorB, _frozen_alpha, _frozen_speed, _frozen_fadelenght, _frozen_noise, _frozen_framestart, _frozen_framerate)
            effectlib.drawLine((xL, yR, zR), (xL, yR, zH), _frozen_model, _frozen_halo, 0.11, _frozen_width, _frozen_endwidth, _frozen_colorR, _frozen_colorG, _frozen_colorB, _frozen_alpha, _frozen_speed, _frozen_fadelenght, _frozen_noise, _frozen_framestart, _frozen_framerate)
            effectlib.drawLine((xR, yH, zR), (xR, yH, zH), _frozen_model, _frozen_halo, 0.11, _frozen_width, _frozen_endwidth, _frozen_colorR, _frozen_colorG, _frozen_colorB, _frozen_alpha, _frozen_speed, _frozen_fadelenght, _frozen_noise, _frozen_framestart, _frozen_framerate)
            effectlib.drawLine((xR, yL, zR), (xR, yL, zH), _frozen_model, _frozen_halo, 0.11, _frozen_width, _frozen_endwidth, _frozen_colorR, _frozen_colorG, _frozen_colorB, _frozen_alpha, _frozen_speed, _frozen_fadelenght, _frozen_noise, _frozen_framestart, _frozen_framerate)
            ### Low horizontal lines
            effectlib.drawLine((xL, yR, zR), (xH, yR, zR), _frozen_model, _frozen_halo, 0.11, _frozen_width, _frozen_endwidth, _frozen_colorR, _frozen_colorG, _frozen_colorB, _frozen_alpha, _frozen_speed, _frozen_fadelenght, _frozen_noise, _frozen_framestart, _frozen_framerate)
            effectlib.drawLine((xR, yH, zR), (xR, yL, zR), _frozen_model, _frozen_halo, 0.11, _frozen_width, _frozen_endwidth, _frozen_colorR, _frozen_colorG, _frozen_colorB, _frozen_alpha, _frozen_speed, _frozen_fadelenght, _frozen_noise, _frozen_framestart, _frozen_framerate)
            ### High horizontal Lines
            effectlib.drawLine((xL, yR, zH), (xH, yR, zH), _frozen_model, _frozen_halo, 0.11, _frozen_width, _frozen_endwidth, _frozen_colorR, _frozen_colorG, _frozen_colorB, _frozen_alpha, _frozen_speed, _frozen_fadelenght, _frozen_noise, _frozen_framestart, _frozen_framerate)
            effectlib.drawLine((xR, yH, zH), (xR, yL, zH), _frozen_model, _frozen_halo, 0.11, _frozen_width, _frozen_endwidth, _frozen_colorR, _frozen_colorG, _frozen_colorB, _frozen_alpha, _frozen_speed, _frozen_fadelenght, _frozen_noise, _frozen_framestart, _frozen_framerate)
    gamethread.delayedname(.1, "Updater", Updater)
    
def Muter():
    for Player in playerlib.getUseridList('#all'):
        if int(Player) in SAC_Dict_Mute:
            SAC_Dict_Mute[int(Player)] -= 1
            if SAC_Dict_Mute[int(Player)] == 0:
                del SAC_Dict_Mute[int(Player)]
    gamethread.delayedname(60, "Muter", Muter)
    
def SecsP():
    global PlayedSeconds
    global PlayedSeconds2
    PlayedSeconds += 1
    PlayedSeconds2 += 1
    gamethread.delayedname(1, "SecsP", SecsP)
    if (PlayedSeconds2 == 59): # should be 59, but 10 is good for testing
        PlayedSeconds2 = 0
        SLine = -1
        File = open(cfgpath + '/banned.txt', 'r')
        global BanDecreasers
        BanDecreasers = {}
        for CurrentLine in File.readlines():
            SLine += 1
            if CurrentLine.startswith('|[u:'):
                SplittedLine = CurrentLine.split('|')
                if len(SplittedLine) == 7:
                    if (int(SplittedLine[4]) > 1):
                        BanDecreasers[SLine] = SLine
        File.close()
        DecreaseBan()
                            
        File = open(cfgpath + '/banned.txt')
        for CurrentLine in File.readlines():
            if CurrentLine.startswith('|[u:'):
                SplittedLine = CurrentLine.split('|')
                if len(SplittedLine) == 7:
                    if (int(SplittedLine[4]) == 1):
                        UnBan(SplittedLine[1])
def DecreaseBan():
    global BanDecreasers
    File = open(cfgpath + '/banned.txt', 'r')
    filelines = File.readlines()
    File.close()
    
    for LINE in BanDecreasers:
        SplittedLine = filelines[LINE].split('|')
        dumdum1 = SplittedLine[1]
        dumdum2 = SplittedLine[2]
        dumdum3 = SplittedLine[3]
        dumdum4 = int(SplittedLine[4]) - 1
        dumdum5 = SplittedLine[5]
        filelines[LINE] = "|%s|%s|%s|%s|%s|\n" %(dumdum1,dumdum2,dumdum3,dumdum4,dumdum5)
    File = open(cfgpath + '/banned.txt', 'w')
    File.writelines(filelines)
    File.close()
def changeTeam(Doer, Doed, Team):
    if not es.exists('userid', Doed): return
    es.server.insertcmd('es_xchangeteam %s %s' %(Doed,Team))
    if Team == 1:
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('moved_team', {'DoedName':es.getplayername(Doed),'DoerName':es.getplayername(Doer),'team':'spectate'}, Lang(Player)))
    elif Team == 2:
        es.setplayerprop(Doed, 'CCSPlayer.m_iClass', random.randint(1, 4))
        usermsg.showVGUIPanel(Doed, 'class_ter', False, {})
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('moved_team', {'DoedName':es.getplayername(Doed),'DoerName':es.getplayername(Doer),'team':'T'}, Lang(Player)))
    elif Team == 3:
        es.setplayerprop(Doed, 'CCSPlayer.m_iClass', random.randint(5, 8))
        usermsg.showVGUIPanel(Doed, 'class_ct', False, {})
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('moved_team', {'DoedName':es.getplayername(Doed),'DoerName':es.getplayername(Doer),'team':'CT'}, Lang(Player)))
    
def Freeze(Doer, Doed):
    DoedName = es.getplayername(Doed)
    DoerName = es.getplayername(Doer)
    if (SAC_Dict_Freeze[int(Doed)]) != "0":
        SAC_Dict_Freeze[int(Doed)] = "0"
        playerlib.getPlayer(int(Doed)).freeze(0)
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('freeze_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    else:
        SAC_Dict_Freeze[int(Doed)] = "1"
        playerlib.getPlayer(int(Doed)).freeze(1)
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('freeze_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))

def tickListener():
    for muted in playerlib.getUseridList('#all'):
        if int(muted) in SAC_Dict_Mute:
            for all in playerlib.getUseridList('#all'):
                es.voicechat('nolisten', all, muted)
def UnBan(steamid):
    SLine = -1
    File = open(cfgpath + '/banned.txt')
    for CurrentLine in File.readlines():
        SLine += 1
        if CurrentLine.startswith('|[u:'):
            SplittedLine = CurrentLine.split('|')
            if len(SplittedLine) == 7:
                if str(SplittedLine[1]).lower() == str(steamid).lower():
                    filehandle = open(cfgpath + '/banned.txt', 'r')
                    filelines = filehandle.readlines()
                    filehandle.close()
                    del filelines[SLine]
                    filehandle = open(cfgpath + '/banned.txt', 'w')
                    filehandle.writelines(filelines)
                    filehandle.close()
                    return

def IsBanned(steamid):
    File = open(cfgpath + '/banned.txt')
    for CurrentLine in File.readlines():
        if CurrentLine.startswith('|[u:'):
            SplittedLine = CurrentLine.split('|')
            if len(SplittedLine) == 7:
                if str(SplittedLine[1]).lower() == str(steamid).lower(): return SplittedLine[2]
    return False
def ChangeMap(Doer, NextMap, popupname):
    if es.exists('map', NextMap):
        gamethread.delayed(0.0, ChangeMapTell, ("5", NextMap))
        gamethread.delayed(1.0, ChangeMapTell, ("4", NextMap))
        gamethread.delayed(2.0, ChangeMapTell, ("3", NextMap))
        gamethread.delayed(3.0, ChangeMapTell, ("2", NextMap))
        gamethread.delayed(4.0, ChangeMapTell, ("1", NextMap))
        gamethread.delayed(5.0, ChangeMapTell, ("0", NextMap))
        gamethread.delayed(5.1, es.server.insertcmd, ('changelevel %s' %(NextMap)))
    else:
        tell(Doer, translations('no_such_map', {map:'NextMap'}, Lang(Doer)))
        SACMenu_ChangeMap.send(Doer)
    
def ChangeMapTell(timeLeft, NextMap):
    for Player in playerlib.getUseridList('#human'):
        tell(Player, translations('changing_map', {'map':NextMap,'sec':timeLeft}, Lang(Player)))
    
def HasFlag(userid, flag):
    File = open(es.getAddonPath(addonpath) + '/admins.txt')
    for CurrentLine in File.readlines():
        if (str(CurrentLine).lower().startswith("|[u:")):
            SplittedLine = CurrentLine.split("|")
            if (len(SplittedLine) == 5):
                if (str(SplittedLine[1]).lower() == str(es.getplayersteamid(userid)).lower()):
                    SplittedFlag = SplittedLine[4].split(",")
                    for Flag in SplittedFlag:
                        if str(Flag).lower().replace("\n", "") == str(flag).lower().replace("\n", ""):
                            File.close()
                            return 1
    File.close()
    return 0
    ###################
    ### ########### ###
    ###  #########  ###
    ### Menu Hanlde ###
    ###  #########  ###
    ### ########### ###
    ###################
    
def MenuHandler1(userid, choice, popupname):
    if (choice == "Fun Commands"):
        if HasFlag(userid, "fun"):
            SACMenu_Main.send(userid)
            tell(userid, translations('flag', None, Lang(userid)))
            return
        SACMenu_Fun.send(userid)
    elif (choice == "Change Map"):
        if HasFlag(userid, "changemap"):
            SACMenu_Main.send(userid)
            tell(userid, translations('flag', None, Lang(userid)))
            return
        SACMenu_ChangeMap.send(userid)
    elif (choice == "Player Management"): SACMenu_PM.send(userid)
    elif (choice == "Music"):
        if HasFlag(userid, "Music"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_Main.send(userid)
            return
        SACMenu_Music.send(userid)
    elif (choice == "Propmenu"):
        if HasFlag(userid, "Props"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_Main.send(userid)
            return
        SACMenu_Propmenu.send(userid)
    elif (choice == "Mini-Games"):
        if HasFlag(userid, "Minigames"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_Main.send(userid)
            return
        SACMenu_MiniGames.send(userid)
    elif (choice == "Admin Management"): SACMenu_AdminManagement.send(userid)
    elif (choice == "Wolves VS Sheeps"):
        SACMenu_MiniGames.send(userid)
        es.unload("%s/mini_zombiemod" %(str(addonpath)))
        es.reload("%s/wolves_vs_sheeps" %(str(addonpath)))
        es.server.insertcmd("mp_restartgame 3")
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('enabled_wolves_vs_sheeps', {'name':es.getplayername(userid)}, Lang(Player)))
        
    elif (choice == "Mini Zombiemod"):
        SACMenu_MiniGames.send(userid)
        es.unload("%s/wolves_vs_sheeps" %(str(addonpath)))
        es.reload("%s/mini_zombiemod" %(str(addonpath)))
        es.server.insertcmd("mp_restartgame 3")
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('enabled_mini_zombiemod', {'name':es.getplayername(userid)}, Lang(Player)))
    elif (choice == "Stop MiniGames"):
        SACMenu_MiniGames.send(userid)
        es.server.insertcmd("es_xunload %s/mini_zombiemod" %(addonpath))
        es.server.insertcmd("es_xunload %s/wolves_vs_sheeps" %(addonpath))
        es.server.insertcmd("mp_restartgame 3")
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('disabled_minigames', {'name':es.getplayername(userid)}, Lang(Player)))
    
def MenuHandler2(userid, choice, popupname):
    if (choice == "List of admins"):
        File = open(es.getAddonPath(addonpath) + '/admins.txt')
        tell(userid, " ")
        tell(userid, " ")
        tell(userid, " ")
        tell(userid, "---- ---- ---- ---- ---- ---- ---- ---- ----")
        tell(userid, "SAC Admins:")
        for CurrentLine in File.readlines():
            if (str(CurrentLine).lower().startswith("|[u:")):
                SplittedLine = CurrentLine.split("|")
                if (len(SplittedLine) == 5):
                    tell(userid, "---- ---- ---- ---- ---- ---- ---- ---- ----")
                    tell(userid, "%s%s" %(translations('Name', None, Lang(userid)), SplittedLine[3]))
                    tell(userid, "%s%s" %(translations('SteamID', None, Lang(userid)), SplittedLine[1]))
                    if (es.getuserid(SplittedLine[1])): tell(userid, "%s%s" %(translations('Status', None, Lang(userid)), translations('currently_online', {'name':es.getplayername(es.getuserid(SplittedLine[1]))}, Lang(userid))))
                    else: tell(userid, "%s%s" %(translations('Status', None, Lang(userid)), translations('currently_offline', None, Lang(userid))))
                    if (int(SplittedLine[2])): tell(userid, "%s%s" %(translations('Power', None, Lang(userid)), translations('can_edit_admins', None, Lang(userid))))
                    else: tell(userid, "%s%s" %(translations('Power', None, Lang(userid)), translations('cant_edit_admins', None, Lang(userid))))
        tell(userid, "---- ---- ---- ---- ---- ---- ---- ---- ----")
        tell(userid, translations('check_console', None, Lang(userid)))
        tell(userid, "---- ---- ---- ---- ---- ---- ---- ---- ----")
        SACMenu_AdminManagement.send(userid)
    elif (choice == "Add an Admin"):
        if (IsAdmin(userid) == 2):
            if popuplib.exists('AddAnAdminMenu'):
                popuplib.delete('AddAnAdminMenu')
            global AddAnAdminMenu
            AddAnAdminMenu = popuplib.easymenu('AddAnAdminMenu',None, AddAnAdminBlock)
            AddAnAdminMenu.settitle('- Super Admin CheeTaH')
            AddAnAdminMenu.setdescription("-- Admin Management\n--- Add An Admin")
            AddAnAdminMenu.submenu(10, SACMenu_AdminManagement)
            AddAnAdminMenu.addoption('UpdateList', 'Update List\n-----------------------------')
            for Player in sorted(playerlib.getUseridList('#all'), key=lambda player: es.getplayername(player)): AddAnAdminMenu.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
            AddAnAdminMenu.send(userid)
        else:
            tell(userid, translations('no_access_to_add_or_remove_admins', None, Lang(userid)))
            SACMenu_AdminManagement.send(userid)
    elif (choice == "Remove an Admin"):
        if (IsAdmin(userid) == 2):
            if popuplib.exists('RemoveAnAdminMenu'):
                popuplib.delete('RemoveAnAdminMenu')
            global RemoveAnAdminMenu
            RemoveAnAdminMenu = popuplib.easymenu('RemoveAnAdminMenu',None, RemoveAnAdminBlock)
            RemoveAnAdminMenu.settitle('- Super Admin CheeTaH')
            RemoveAnAdminMenu.setdescription("-- Admin Management\n--- Remove An Admin")
            RemoveAnAdminMenu.submenu(10, SACMenu_AdminManagement)
            RemoveAnAdminMenu.addoption('UpdateList', 'Update List\n-----------------------------')
            File = open(es.getAddonPath(addonpath) + '/admins.txt')
            for CurrentLine in File.readlines():
                if (str(CurrentLine).lower().startswith("|[u:")):
                    SplittedLine = CurrentLine.split("|")
                    if (len(SplittedLine) == 5): RemoveAnAdminMenu.addoption(SplittedLine[3], SplittedLine[3])
            RemoveAnAdminMenu.send(userid)
                        
        else:
            tell(userid, translations('no_access_to_add_or_remove_admins', None, Lang(userid)))
            SACMenu_AdminManagement.send(userid)
    
def PropCreator(userid, choice2, popupname):
    choice2 = str(choice2).split("--")
    choice = choice2[1]
    SACMenu_Propmenu.sendPage(userid, int(choice2[0]))
    if (str(choice).lower().startswith("d|")):
        choiceSplit = choice.split("|")
        if (len(choiceSplit) == 3):
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('spawned_prop', {'name':es.getplayername(userid),'prop':choiceSplit[1]}, Lang(Player)))
            es.server.insertcmd("es_xprop_dynamic_create %s %s" %(userid, choiceSplit[2]))
            return
    elif (str(choice).lower().startswith("p|")):
        choiceSplit = choice.split("|")
        if (len(choiceSplit) == 3):
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('spawned_prop', {'name':es.getplayername(userid),'prop':choiceSplit[1]}, Lang(Player)))
            es.server.insertcmd("es_xprop_physics_create %s %s" %(userid, choiceSplit[2]))
            return
    elif (choice == "DelAll"):
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('deleted_all_props', {'name':es.getplayername(userid)}, Lang(Player)))
        for entity_index in es.createentitylist():
            if str(es.entitygetvalue(entity_index, "classname")).startswith("prop_"):
                es.server.insertcmd("es_xremove %s" %(entity_index))
        return
    elif (choice == "DelThis"):
        index = getViewProp(userid)
        if index != None and es.entitygetvalue(index, "classname").startswith("prop_"):
            es.server.insertcmd("es_xremove %s" %(index))
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('deleted_a_prop', {'name':es.getplayername(userid)}, Lang(Player)))
            return
        tell(userid, translations('not_a_prop', None, Lang(userid)))
    
def MusicPlayer(userid, choice, popupname):
    choice = choice.split("|")
    es.emitsound("player", userid, choice[1], 1, 0)
    for Player in playerlib.getUseridList('#human'): tell(Player, translations('played_song', {'name':es.getplayername(userid),'song':choice[0]}, Lang(Player)))
    SACMenu_Music.sendPage(userid, int(choice[2]))
    
def AddAnAdminBlock(userid, choice, popupname):
    if (choice == "UpdateList"):
        MenuHandler2(userid, "Add an Admin", None)
        return
    addAdmin(choice, userid)
    
def RemoveAnAdminBlock(userid, choice, popupname):
    if (choice == "UpdateList"):
        MenuHandler2(userid, "Remove an Admin", None)
        return
    removeAdmin(choice, userid)

def MenuHandlerChooseBanTime(userid, choice, popupname):
    SAC_Dict_Ban[int(userid)] = choice
    MenuHandler4(userid, 'Ban2', None)

def MenuHandlerChooseItem(userid, choice, popupname):
    SAC_Dict_Give[int(userid)] = choice
    MenuHandler3(userid, 'Give Weapon2', None)

def SACMenu_SkinsMenu_Selected(userid,choice,popupname):
    Menu = 'SetSkins_%s' %userid
    if popuplib.exists(Menu): popuplib.delete(Menu)
    Menu2 = popuplib.easymenu(Menu,None, SetSkinBlock)
    Menu2.settitle('- Super Admin CheeTaH')
    Menu2.setdescription("-- Fun Commands\n--- Skins\n---- %s" %(choice.split("|")[0]), lang=None)
    Menu2.submenu(10, SACMenu_SkinsMenu)
    SearchFor = '#alive'
    Players = playerlib.getUseridList(SearchFor)
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if not Players: Menu2.addoption('UpdateList|%s'%(choice), 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
    else: Menu2.addoption('UpdateList|%s'%(choice), 'Update List\n-----------------------------')
    for Player in Players:
        Menu2.addoption("%s|%s"%(Player,choice), '%s (%s)' %(es.getplayername(Player), Player))
    Menu2.send(userid)
    
def MenuHandler4(userid, choice, popupname):
    if (choice == 'UnBan'):
        if HasFlag(userid, "Ban"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_PM.send(userid)
            return
        AnyAdded = 0
        Menu = 'UnBanMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, UnBanBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Player Management \n--- Unban", lang=None)
        Menu2.submenu(10, SACMenu_PM)
        Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        File = open(cfgpath + '/banned.txt')
        for CurrentLine in File.readlines():
            if CurrentLine.startswith('|[u:'):
                SplittedLine = CurrentLine.split('|')
                if len(SplittedLine) == 7:
                    Menu2.addoption(SplittedLine, '%s - %s/%s minutes left' %(SplittedLine[2],SplittedLine[4],SplittedLine[5]))
                    AnyAdded = 1
        if (AnyAdded == 0): Menu2.addoption('...', 'No SAC banned players!',0)
        Menu2.send(userid)
        
    if (choice == 'Ban'):
        if HasFlag(userid, "Ban"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_PM.send(userid)
            return
        SACMenu_BanTime.send(userid)
        
    if (choice == 'Ban2'):
        if HasFlag(userid, "Ban"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_PM.send(userid)
            return
        Menu = 'BanMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, BanBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Player Management \n--- Ban\n---- %s" %(SAC_Dict_Ban[int(userid)]), lang=None)
        Menu2.submenu(10, SACMenu_BanTime)
        SearchFor = '#all'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
            
    if (choice == 'Kick'):
        if HasFlag(userid, "kick"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_PM.send(userid)
            return
        Menu = 'Kickmenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, KickBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Player Management \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_PM)
        SearchFor = '#all'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    if (choice == 'Mute'):
        if HasFlag(userid, "Mute"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_PM.send(userid)
            return
        Menu = 'MuteMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, MuteBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Player Management \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_PM)
        SearchFor = '#all'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if int(Player) not in SAC_Dict_Mute: Menu2.addoption(Player, '[Mute: 00] %s (%s)' %(es.getplayername(Player), Player))
            else: Menu2.addoption(Player, '[Mute: %02d] %s (%s)' %(SAC_Dict_Mute[Player], es.getplayername(Player), Player))
        Menu2.send(userid)
        
    if (choice == 'Swap Player To Opposite Team'):
        if HasFlag(userid, "Changeteam"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_PM.send(userid)
            return
        Menu = 'SPTOPMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, SPTOPBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Player Management \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_PM)
        SearchFor = '#all'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (int(es.getplayerteam(Player)) == 1): Menu2.addoption(Player, '[SPEC] %s (%s)' %(es.getplayername(Player), Player))
            elif (int(es.getplayerteam(Player)) == 2): Menu2.addoption(Player, '[T] %s (%s)' %(es.getplayername(Player), Player))
            elif (int(es.getplayerteam(Player)) == 3): Menu2.addoption(Player, '[CT] %s (%s)' %(es.getplayername(Player), Player))
            else: Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    if (choice == 'Swap Player To Spectator'):
        if HasFlag(userid, "Changeteam"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_PM.send(userid)
            return
        Menu = 'SPTSMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, SPTSBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Player Management \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_PM)
        SearchFor = '#all'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (int(es.getplayerteam(Player)) == 1): Menu2.addoption(Player, '[SPEC] %s (%s)' %(es.getplayername(Player), Player))
            elif (int(es.getplayerteam(Player)) == 2): Menu2.addoption(Player, '[T] %s (%s)' %(es.getplayername(Player), Player))
            elif (int(es.getplayerteam(Player)) == 3): Menu2.addoption(Player, '[CT] %s (%s)' %(es.getplayername(Player), Player))
            else: Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    if (choice == 'Swap Player To T'):
        if HasFlag(userid, "Changeteam"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_PM.send(userid)
            return
        Menu = 'SPTTMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, SPTTBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Player Management \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_PM)
        SearchFor = '#all'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (int(es.getplayerteam(Player)) == 0): Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
            elif (int(es.getplayerteam(Player)) == 1): Menu2.addoption(Player, '[SPEC] %s (%s)' %(es.getplayername(Player), Player))
            elif (int(es.getplayerteam(Player)) == 3): Menu2.addoption(Player, '[CT] %s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    if (choice == 'Swap Player To CT'):
        if HasFlag(userid, "Changeteam"):
            tell(userid, translations('flag', None, Lang(userid)))
            SACMenu_PM.send(userid)
            return
        Menu = 'SPTCTMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, SPTCTBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Player Management \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_PM)
        SearchFor = '#all'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (int(es.getplayerteam(Player)) == 0): Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
            elif (int(es.getplayerteam(Player)) == 1): Menu2.addoption(Player, '[SPEC] %s (%s)' %(es.getplayername(Player), Player))
            elif (int(es.getplayerteam(Player)) == 2): Menu2.addoption(Player, '[T] %s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
    
def MenuHandler3(userid, choice, popupname):
    ## Fun command menu handler
    if HasFlag(userid, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    if (choice == 'Give Weapon'): SACMenu_Items.send(userid)
    elif (choice == 'Give Weapon2'):
        Menu = 'GiveMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, GiveBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands\n--- Give Weapon\n---- %s" %(SAC_Dict_Give[int(userid)]), lang=None)
        Menu2.submenu(10, SACMenu_Items)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
    elif choice == 'Skins':
        SACMenu_SkinsMenu.send(userid)
    elif (choice == 'Respawn'):
        Menu = 'RespawnMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None, RespawnBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#dead'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (int(es.getplayerteam(Player)) == 2): Menu2.addoption(Player, '[T] %s (%s)' %(es.getplayername(Player), Player))
            if (int(es.getplayerteam(Player)) == 3): Menu2.addoption(Player, '[CT] %s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Godmode'):
        Menu = 'GodMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,GodBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (playerlib.getPlayer(Player).inGodMode()): Menu2.addoption(Player, '[GOD] %s (%s)' %(es.getplayername(Player), Player))
            else: Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Speed'):
        Menu = 'SpeedMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,SpeedBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (playerlib.getPlayer(Player).getSpeed() != 1.0): Menu2.addoption(Player, '[Speed] %s (%s)' %(es.getplayername(Player), Player))
            else: Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Jetpack'):
        Menu = 'JetpackMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,JetpackBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (playerlib.getPlayer(Player).getJetpack()): Menu2.addoption(Player, '[Jetpack] %s (%s)' %(es.getplayername(Player), Player))
            else: Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Invisible'):
        Menu = 'InvisibleMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,InvisibleBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            Visibilityness = str(playerlib.getPlayer(Player).getColor()).split(", ")[3].replace(")", "")
            Menu2.addoption(Player, '[%03d/255] %s (%s)' %(int(Visibilityness), es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Shake'):
        Menu = 'ShakeMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,ShakeBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if SAC_Dict_Shaking[int(Player)] != "0": Menu2.addoption(Player, '[SHAKING: %03d] %s (%s)' %(int(SAC_Dict_Shaking[int(Player)]), es.getplayername(Player), Player))
            if SAC_Dict_Shaking[int(Player)] == "0": Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Unlimited Ammo'):
        Menu = 'UnlimitedAmmoMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,UnlimitedAmmoBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if SAC_Dict_Ammo[int(Player)] != "0": Menu2.addoption(Player, '[UNLIMITED AMMO] %s (%s)' %(es.getplayername(Player), Player))
            if SAC_Dict_Ammo[int(Player)] == "0": Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Regeneration'):
        Menu = 'RegenerationMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,RegenerationBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if SAC_Dict_Regeneration[int(Player)] != "0": Menu2.addoption(Player, '[REG] %s (%s)' %(es.getplayername(Player), Player))
            if SAC_Dict_Regeneration[int(Player)] == "0": Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Disguise'):
        Menu = 'DisguiseMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,DisguiseBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if SAC_Dict_Disguise[int(Player)] != "0": Menu2.addoption(Player, '[DIS] %s (%s)' %(es.getplayername(Player), Player))
            if SAC_Dict_Disguise[int(Player)] == "0": Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Bury'):
        Menu = 'BuryMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,BuryBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Blind'):
        Menu = 'BlindMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,BlindBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            Menu2.addoption(Player, '[%03d/255] %s (%s)' %(int(SAC_Dict_Blind[Player]), es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Slay'):
        Menu = 'SlayMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,SlayBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Save Location'):
        x,y,z = es.getplayerlocation(userid)
        SAC_Dict_Saveloc[userid] = "%f,%f,%f" %(float(x),float(y),float(z))
        tell(userid, translations('saveloc',{'x':x,'y':y,'z':z},Lang(userid)))
        SACMenu_Fun.sendPage(userid, int(PageThatTeleportAndSavelocIsOn))
        
    elif (choice == 'Teleport'):
        if int(userid) not in SAC_Dict_Saveloc:
            tell(userid, translations('no_savedloc',None,Lang(userid)))
            SACMenu_Fun.sendPage(userid, int(PageThatTeleportAndSavelocIsOn))
            return
        Menu = 'TeleportMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,TeleportBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Drug'):
        Menu = 'DrugMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,DrugBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if SAC_Dict_Drug[int(Player)] != "0": Menu2.addoption(Player, '[DRUGGED] %s (%s)' %(es.getplayername(Player), Player))
            if SAC_Dict_Drug[int(Player)] == "0": Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Slap'):
        Menu = 'SlapMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,SlapBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Freeze'):
        Menu = 'FreezeMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,FreezeBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (playerlib.getPlayer(Player).getFreeze()): Menu2.addoption(Player, '[FROZEN] %s (%s)' %(es.getplayername(Player), Player))
            else: Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
        
    elif (choice == 'Noclip'):
        Menu = 'NoclipMenu'
        if popuplib.exists(Menu): popuplib.delete(Menu)
        Menu2 = popuplib.easymenu(Menu,None,NoclipBlock)
        Menu2.settitle('- Super Admin CheeTaH')
        Menu2.setdescription("-- Fun Commands \n--- %s" %(choice), lang=None)
        Menu2.submenu(10, SACMenu_Fun)
        SearchFor = '#alive'
        Players = playerlib.getUseridList(SearchFor)
        Players = sorted(Players, key=lambda player: es.getplayername(player))
        if not Players: Menu2.addoption('UpdateList', 'Update List\n-----------------------------\n%s' %(translations('none_matching', {'arg':str(SearchFor).replace("#", "")}, Lang(userid))))
        else: Menu2.addoption('UpdateList', 'Update List\n-----------------------------')
        for Player in Players:
            if (playerlib.getPlayer(Player).getNoClip()): Menu2.addoption(Player, '[NOCLIP] %s (%s)' %(es.getplayername(Player), Player))
            else: Menu2.addoption(Player, '%s (%s)' %(es.getplayername(Player), Player))
        Menu2.send(userid)
    
    
    ###################
    ### ########### ###
    ###  #########  ###
    ### Client CMDs ###
    ###  #########  ###
    ### ########### ###
    ###################
def client_cmd_openmenu(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    SACMenu_Main.send(Doer)
    
def client_cmd_respawn(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Respawn', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            PlayerP = playerlib.getPlayer(Doed)
            PlayerName = es.getplayername(Doed)
            if not (PlayerP.isdead):
                tell(Doer, translations('already_alive', {'name':PlayerName}, Lang(Doer)))
                continue
            es.setplayerprop(Doed,"CCSPlayer.m_iPlayerState",0)
            es.setplayerprop(Doed,"CCSPlayer.baseclass.m_lifeState",512)
            es.server.insertcmd('es_xspawnplayer %s' % Doed)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('respawned', {'DoedName':PlayerName,'DoerName':DoerName}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_godmode(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Godmode', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            if (DoedP.inGodMode()):
                DoedP.godmode(0)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('god_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
            else:
                DoedP.godmode(1)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('god_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))

    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_speed(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Speed', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            es.setplayerprop(Doed, "CBasePlayer.localdata.m_flLaggedMovementValue", args[1])
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('speed', {'DoedName':DoedName,'DoerName':DoerName,'speed':args[1]}, Lang(Player)))

    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_jetpack(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Jetpack', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            if (DoedP.getJetpack()):
                DoedP.jetpack(0)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('jetpack_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
            else:
                DoedP.jetpack(1)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('jetpack_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))

    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
        
def client_cmd_invisible(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Invisible', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if int(args[1]) > 255: args[1] = 255
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            if DoedP.getPrimary(): DoedP.setWeaponColor(255, 255, 255, int(args[1]))
            elif DoedP.getSecondary(): DoedP.setWeaponColor(255, 255, 255, int(args[1]))
            procent = round(float(args[1]) / 2.55, 2)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('invisible', {'DoedName':DoedName,'DoerName':DoerName,'real':args[1],'procent':procent}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_shake(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Shake', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            if(int(float(args[1])) == 0):
                SAC_Dict_Shaking[int(Doed)] = "0"
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('shaked_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
            else:
                SAC_Dict_Shaking[int(Doed)] = int(float(args[1]))
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('shaked_on', {'DoedName':DoedName,'DoerName':DoerName,'mag':SAC_Dict_Shaking[int(Player)]}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_unlimitedammo(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Unlimited Ammo', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            if (SAC_Dict_Ammo[int(Doed)] != "0"):
                    SAC_Dict_Ammo[int(Doed)] = "0"
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('unlimited_ammo_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
            else:
                SAC_Dict_Ammo[int(Doed)] = "1"
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('unlimited_ammo_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
           
    
def client_cmd_regeneration(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Regeneration', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            if (SAC_Dict_Regeneration[int(Doed)] != "0"):
                    SAC_Dict_Regeneration[int(Doed)] = "0"
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('regeneration_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
            else:
                SAC_Dict_Regeneration[int(Doed)] = "1"
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('regeneration_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_disguise(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Disguise', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            if (SAC_Dict_Disguise[int(Doed)] != "0"):
                SAC_Dict_Disguise[int(Doed)] = "0"
                RandomValue = int(random.randint(1,4))
                if (int(es.getplayerteam(Doed)) == 2):
                    if (RandomValue == 1): DoedP.setModel("player/t_arctic")
                    if (RandomValue == 2): DoedP.setModel("player/t_guerilla")
                    if (RandomValue == 3): DoedP.setModel("player/t_leet")
                    if (RandomValue == 4): DoedP.setModel("player/t_phoenix")
                if (int(es.getplayerteam(Doed)) == 3):
                    if (RandomValue == 1): DoedP.setModel("player/ct_gign")
                    if (RandomValue == 2): DoedP.setModel("player/ct_gsg9")
                    if (RandomValue == 3): DoedP.setModel("player/ct_sas")
                    if (RandomValue == 4): DoedP.setModel("player/ct_urban")
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('disguise_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
            else:
                SAC_Dict_Disguise[int(Doed)] = "1"
                DoedP.setModel("props_c17/oildrum001.mdl")
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('disguise_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_bury(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Bury', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            x,y,z = es.getplayerlocation(Doed)
            z -= float(args[1])
            es.entitysetvalue(DoedP.index, 'origin', ' '.join(es.createvectorstring(x,y,z).split(',')))
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('bury', {'DoedName':DoedName,'DoerName':DoerName,'depth':args[1]}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_blind(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Blind', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            SAC_Dict_Blind[int(Doed)] = args[1]
            procent = round(float(args[1]) / 2.55, 2)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('blind', {'DoedName':DoedName,'DoerName':DoerName,'real':args[1],'procent':procent}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_kill(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Slay', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            SlayEffects(Doed)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('slay', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_saveloc(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    x,y,z = es.getplayerlocation(Doer)
    SAC_Dict_Saveloc[Doer] = "%f,%f,%f" %(float(x),float(y),float(z))
    tell(Doer, translations('saveloc',{'x':x,'y':y,'z':z},Lang(Doer)))
    
def client_cmd_teleportto(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax_no_menu',{'Syntax':'<players to moved> <player to get moved to>'},Lang(Doer)))
        return
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    Players2 = es.getuserid(args[1])
    if not Players:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
        return
    if not Players2:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
        return
    DoerName = es.getplayername(Doer)
    LocoName = es.getplayername(Players2)
    x,y,z = es.getplayerlocation(Players2)
    LocoLocation = "%f,%f,%f" %(float(x),float(y),float(z))
    for Doed in Players:
        DoedP = playerlib.getPlayer(Doed)
        DoedName = es.getplayername(Doed)
        if (DoedP.isdead):
            tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            continue
        es.entitysetvalue(DoedP.index, 'origin', ' '.join(LocoLocation.split(',')))
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('teleport_name', {'DoedName':DoedName,'DoerName':DoerName,'LocoName':LocoName}, Lang(Player)))
        
    
def client_cmd_teleport(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    if int(Doer) not in SAC_Dict_Saveloc:
        tell(Doer, translations('no_savedloc',None,Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Teleport', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            es.entitysetvalue(DoedP.index, 'origin', ' '.join(SAC_Dict_Saveloc[int(Doer)].split(',')))
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('teleport', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
      
def client_cmd_drug(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Drug', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            if (SAC_Dict_Drug[int(Doed)] != "0"):
                SAC_Dict_Drug[int(Doed)] = "0"
                es.cexec(Doed, "r_screenoverlay normal")
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('drug_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
            else:
                SAC_Dict_Drug[int(Doed)] = "1"
                es.cexec(Doed, "r_screenoverlay effects/tp_eyefx/tp_eyefx")
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('drug_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_slap(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Slap', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            x = random.randint(-200, 200)
            y = random.randint(-200, 200)
            z = random.randint(200, 400)
            es.emitsound("player", Doed, 'player/damage%s.wav'%(random.randint(1,3)), 1, 0.2)
            es.setplayerprop(Doed, "CCSPlayer.baseclass.localdata.m_vecBaseVelocity", es.createvectorstring(x,y,z))
            DoedP.setHealth(int(DoedP.getHealth()) - int(args[1]))
            if (int(DoedP.getHealth()) < 1): DoedP.slay()
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('slap', {'DoedName':DoedName,'DoerName':DoerName, 'dmg':args[1]}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_give(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Give Weapon', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            es.server.insertcmd("es_xgive %s %s" %(Doed,args[1]))
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('give', {'DoedName':DoedName,'DoerName':DoerName, 'item':args[1]}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_setcash(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax_no_menu',{'Syntax':'<players> <cash>'},Lang(Doer)))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            SetCash = int(args[1])
            if (SetCash < 0): SetCash = 0
            if (SetCash > 16000): SetCash = 16000
            es.setplayerprop(Doed,"CCSPlayer.m_iAccount",SetCash)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('cash', {'DoedName':DoedName,'DoerName':DoerName, 'money':str(es.getplayerprop(Doed, "CCSPlayer.m_iAccount"))}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
        
def client_cmd_addcash(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax_no_menu',{'Syntax':'<players> <cash>'},Lang(Doer)))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            SetCash = int(int(args[1]) + int(es.getplayerprop(Doed, "CCSPlayer.m_iAccount")))
            if (SetCash < 0): SetCash = 0
            if (SetCash > 16000): SetCash = 16000
            es.setplayerprop(Doed,"CCSPlayer.m_iAccount",SetCash)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('cash', {'DoedName':DoedName,'DoerName':DoerName, 'money':str(es.getplayerprop(Doed, "CCSPlayer.m_iAccount"))}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
        
def client_cmd_takecash(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax_no_menu',{'Syntax':'<players> <cash>'},Lang(Doer)))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            SetCash = int(es.getplayerprop(Doed, "CCSPlayer.m_iAccount") - int(args[1]))
            if (SetCash < 0): SetCash = 0
            if (SetCash > 16000): SetCash = 16000
            es.setplayerprop(Doed,"CCSPlayer.m_iAccount",SetCash)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('cash', {'DoedName':DoedName,'DoerName':DoerName, 'money':str(es.getplayerprop(Doed, "CCSPlayer.m_iAccount"))}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_sethealth(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax_no_menu',{'Syntax':'<players> <health>'},Lang(Doer)))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            SetHealth = int(args[1])
            if (SetHealth < 1):
                SetHealth = 0
                DoedP.slay()
            es.setplayerprop(Doed,"CCSPlayer.baseclass.m_iHealth",SetHealth)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('health', {'DoedName':DoedName,'DoerName':DoerName, 'hp':str(es.getplayerprop(Doed, "CCSPlayer.baseclass.m_iHealth"))}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
        
def client_cmd_addhealth(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax_no_menu',{'Syntax':'<players> <health>'},Lang(Doer)))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            SetHealth = es.getplayerprop(Doed, "CCSPlayer.baseclass.m_iHealth") + int(args[1])
            if (SetHealth < 1):
                SetHealth = 0
                DoedP.slay()
            es.setplayerprop(Doed,"CCSPlayer.baseclass.m_iHealth",SetHealth)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('health', {'DoedName':DoedName,'DoerName':DoerName, 'hp':str(es.getplayerprop(Doed, "CCSPlayer.baseclass.m_iHealth"))}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
        
def client_cmd_takehealth(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax_no_menu',{'Syntax':'<players> <health>'},Lang(Doer)))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            SetHealth = es.getplayerprop(Doed, "CCSPlayer.baseclass.m_iHealth") - int(args[1])
            if (SetHealth < 1):
                SetHealth = 0
                DoedP.slay()
            es.setplayerprop(Doed,"CCSPlayer.baseclass.m_iHealth",SetHealth)
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('health', {'DoedName':DoedName,'DoerName':DoerName, 'hp':str(es.getplayerprop(Doed, "CCSPlayer.baseclass.m_iHealth"))}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_freeze(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Freeze', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            Freeze(Doer, Doed)
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_noclip(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "fun"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler3, (Doer, 'Noclip', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedP = playerlib.getPlayer(Doed)
            DoedName = es.getplayername(Doed)
            if (DoedP.isdead):
                tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
                continue
            if (DoedP.getNoClip()):
                DoedP.noclip(0)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('noclip_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
            else:
                DoedP.noclip(1)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('noclip_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_message(Doer, args):
    if not args: args = " "
    DoerName = es.getplayername(Doer)
    if not IsAdmin(Doer):
        tell(Doer, translations('msg_to_admin', {'DoerName':DoerName, 'msg':str(args)}, Lang(Doer)))
        for Player in playerlib.getUseridList('#human'):
            if IsAdmin(Player): tell(Player, translations('msg_to_admin', {'DoerName':DoerName, 'msg':str(args)}, Lang(Player)))
        return
    if HasFlag(Doer, "message"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    for Player in playerlib.getUseridList('#human'): tell(Player, translations('msg_from_admin', {'DoerName':DoerName, 'msg':str(args)}, Lang(Player)))
    
def client_cmd_message_private(Doer, args):
    if not IsAdmin(Doer):
        return
        NotAdmin(Doer)
    if HasFlag(Doer, "message"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    if len(args) == 0:
        tell(Doer, translations('wrong_syntax_no_menu',{'Syntax':'<players> <message>'},Lang(Doer)))
        return
    if len(args) == 1: pMSG = " "
    else:
        pMSG = ""
        pFIRST = 1
        for pLINE in args:
            if pFIRST == 0: pMSG = "%s %s" %(str(pMSG), str(pLINE))
            pFIRST = 0
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedName = es.getplayername(Doed)
            tell(Doed, translations('msg_from_admin_private', {'DoerName':DoerName,'DoedName':DoedName,'msg':str(pMSG)}, Lang(Doed)))
            if (Doed != Doer): tell(Doer, translations('msg_from_admin_private', {'DoerName':DoerName,'DoedName':DoedName,'msg':str(pMSG)}, Lang(Doer)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
        
def client_cmd_message_center(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if not args: args = " "
    DoerName = es.getplayername(Doer)
    if HasFlag(Doer, "message"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    for Player in playerlib.getUseridList('#human'): ctell(Player, translations('msg_from_admin_center', {'DoerName':DoerName, 'msg':str(args)}, Lang(Player)))
    
def client_cmd_ban(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "Ban"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler4, (Doer, 'Ban', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        File = open(cfgpath + '/banned.txt', 'a')
        for Doed in Players:
            DoedName = es.getplayername(Doed)
            if IsBanned(es.getplayersteamid(Doed)): tell(Doer, '%s is already banned!' %(DoedName))
            else:
                File.write("\n|%s|%s|%s|%s|%s|" %(es.getplayersteamid(Doed),str(DoedName).replace("|", ""),str(DoerName).replace("|", ""),args[1],args[1]))
                gamethread.delayed(0.5, es.server.insertcmd, "kickid %s banned" %(Doed))
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('banned', {'DoedName':DoedName,'DoerName':DoerName,'minutes':args[1]}, Lang(Player)))
        File.close()
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
           
def client_cmd_unban(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "Ban"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 5
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler4, (Doer, 'UnBan', None))
        return
    steamid = "%s%s%s%s%s" %(args[0],args[1],args[2],args[3],args[4])
    if IsBanned(steamid):
        DoerName = es.getplayername(Doer)
        unbanneded = "%s (%s)" %(IsBanned(steamid), steamid)
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('unbanned', {'DoerName':DoerName,'unbanneded':unbanneded}, Lang(Player)))
        UnBan(steamid)
    else:
        tell(Doer, "%s isn't banned!" %(steamid))
def client_cmd_kick(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "Kick"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler4, (Doer, 'Kick', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedName = es.getplayername(Doed)
            es.server.insertcmd("kickid %s Kicked" %(Doed))
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('kicked', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_mute(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "Mute"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 2
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler4, (Doer, 'Mute', None))
        return
    DoerName = es.getplayername(Doer)
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            DoedName = es.getplayername(Doed)
            SAC_Dict_Mute[int(Doed)] = int(args[1])
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('muted', {'DoedName':DoedName,'DoerName':DoerName,'minutes':args[1]}, Lang(Player)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
        
def server_cmd_unban(args):
    WantedArgs = 5
    if (len(args) != WantedArgs):
        es.dbgmsg(0,'SAC: Syntax: %s <steamid>' %(es.ServerVar("sac_cmd_unban2")))
        return
    steamid = "%s%s%s%s%s" %(args[0],args[1],args[2],args[3],args[4])
    if IsBanned(steamid):
        DoerName = 'Console'
        unbanneded = "%s (%s)" %(IsBanned(steamid), steamid)
        for Player in playerlib.getUseridList('#human'): tell(Player, translations('unbanned', {'DoerName':DoerName,'unbanneded':unbanneded}, Lang(Player)))
        es.dbgmsg(0,"SAC: Unbanned: %s" %(unbanneded))
        UnBan(steamid)
    else:
        es.dbgmsg(0,"SAC: %s isn't banned" %(steamid))
def client_cmd_sptot(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "Changeteam"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler4, (Doer, 'Swap Player To Opposite Team', None))
        return
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            if (int(es.getplayerteam(Doed)) == 2): changeTeam(Doer, Doed, 3)
            elif (int(es.getplayerteam(Doed)) == 3): changeTeam(Doer, Doed, 2)
            else: changeTeam(Doer, Doed, int(es.getplayerteam(Doed)))
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_spts(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "Changeteam"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler4, (Doer, 'Swap Player To Spectator', None))
        return
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            changeTeam(Doer, Doed, 1)
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_sptt(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "Changeteam"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler4, (Doer, 'Swap Player To T', None))
        return
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            changeTeam(Doer, Doed, 2)
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_sptct(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "Changeteam"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax',{'given':len(args),'needed':WantedArgs},Lang(Doer)))
        gamethread.delayed(0.01, MenuHandler4, (Doer, 'Swap Player To CT', None))
        return
    Players = playerlib.getUseridList(args[0])
    Players = sorted(Players, key=lambda player: es.getplayername(player))
    if (Players):
        for Doed in Players:
            changeTeam(Doer, Doed, 3)
    else:
        tell(Doer, translations('none_matching', {'arg':args[0]}, Lang(Doer)))
    
def client_cmd_map(Doer, args):
    if not IsAdmin(Doer):
        NotAdmin(Doer)
        return
    if HasFlag(Doer, "changemap"):
        tell(Doer, translations('flag', None, Lang(Doer)))
        return
    WantedArgs = 1
    if (len(args) != WantedArgs):
        tell(Doer, translations('wrong_syntax_no_menu',{'Syntax':'<map>'},Lang(Doer)))
        return
    ChangeMap(Doer, args[0], None)
   
    
    
    ###############################
    ### ####################### ###
    ###  #####################  ###
    ### Menu handle for players ###
    ###  #####################  ###
    ### ####################### ###
    ###############################
    
    
def RespawnBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if not (DoedP.isdead): tell(Doer, translations('already_alive', {'name':DoedName}, Lang(Doer)))
            else:
                es.setplayerprop(Doed,"CCSPlayer.m_iPlayerState",0)
                es.setplayerprop(Doed,"CCSPlayer.baseclass.m_lifeState",512)
                es.server.insertcmd('es_xspawnplayer %s' % Doed)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('respawned', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Respawn', None))
    
def GodBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                if (DoedP.inGodMode()):
                    DoedP.godmode(0)
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('god_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
                else:
                    DoedP.godmode(1)
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('god_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Godmode', None))
    
def SpeedBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                if (playerlib.getPlayer(Doed).getSpeed() != 1.0):
                    es.setplayerprop(Doed, "CBasePlayer.localdata.m_flLaggedMovementValue", "1.0")
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('speed', {'DoedName':DoedName,'DoerName':DoerName,'speed':'1.0'}, Lang(Player)))
                else:
                    es.setplayerprop(Doed, "CBasePlayer.localdata.m_flLaggedMovementValue", "2.0")
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('speed', {'DoedName':DoedName,'DoerName':DoerName,'speed':'2.0'}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Speed', None))
    
def JetpackBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                if (DoedP.getJetpack()):
                    DoedP.jetpack(0)
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('jetpack_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
                else:
                    DoedP.jetpack(1)
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('jetpack_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Jetpack', None))
      
def InvisibleBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                Visibilityness = str(playerlib.getPlayer(Doed).getColor()).split(", ")[3].replace(")", "")
                if (int(Visibilityness) == 0): VisValue = 51
                elif (int(Visibilityness) == 51): VisValue = 102
                elif (int(Visibilityness) == 102): VisValue = 153
                elif (int(Visibilityness) == 153): VisValue = 204
                elif (int(Visibilityness) == 255): VisValue = 0
                else: VisValue = 255
                DoedP.setColor(255, 255, 255, int(VisValue))
                if DoedP.getPrimary(): DoedP.setWeaponColor(255, 255, 255, int(VisValue))
                elif DoedP.getSecondary(): DoedP.setWeaponColor(255, 255, 255, int(VisValue))
                procent = round(float(VisValue) / 2.55, 2)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('invisible', {'DoedName':DoedName,'DoerName':DoerName,'real':VisValue,'procent':procent}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Invisible', None))
    
def ShakeBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                if (SAC_Dict_Shaking[int(Doed)] != "0"):
                    SAC_Dict_Shaking[int(Doed)] = "0"
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('shaked_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
                else:
                    SAC_Dict_Shaking[int(Doed)] = "50"
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('shaked_on', {'DoedName':DoedName,'DoerName':DoerName,'mag':SAC_Dict_Shaking[int(Player)]}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Shake', None))
    
def UnlimitedAmmoBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                if (SAC_Dict_Ammo[int(Doed)] != "0"):
                    SAC_Dict_Ammo[int(Doed)] = "0"
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('unlimited_ammo_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
                else:
                    SAC_Dict_Ammo[int(Doed)] = "1"
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('unlimited_ammo_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Unlimited Ammo', None))
    
def RegenerationBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                if (SAC_Dict_Regeneration[int(Doed)] != "0"):
                    SAC_Dict_Regeneration[int(Doed)] = "0"
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('regeneration_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
                else:
                    SAC_Dict_Regeneration[int(Doed)] = "1"
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('regeneration_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Regeneration', None))
    
def DisguiseBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                if (SAC_Dict_Disguise[int(Doed)] != "0"):
                    SAC_Dict_Disguise[int(Doed)] = "0"
                    RandomValue = int(random.randint(1,4))
                    if (int(es.getplayerteam(Doed)) == 2):
                        if (RandomValue == 1): DoedP.setModel("player/t_arctic")
                        if (RandomValue == 2): DoedP.setModel("player/t_guerilla")
                        if (RandomValue == 3): DoedP.setModel("player/t_leet")
                        if (RandomValue == 4): DoedP.setModel("player/t_phoenix")
                    if (int(es.getplayerteam(Doed)) == 3):
                        if (RandomValue == 1): DoedP.setModel("player/ct_gign")
                        if (RandomValue == 2): DoedP.setModel("player/ct_gsg9")
                        if (RandomValue == 3): DoedP.setModel("player/ct_sas")
                        if (RandomValue == 4): DoedP.setModel("player/ct_urban")
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('disguise_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
                else:
                    SAC_Dict_Disguise[int(Doed)] = "1"
                    DoedP.setModel("props_c17/oildrum001.mdl")
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('disguise_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Disguise', None))
    
def BuryBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                x,y,z = es.getplayerlocation(Doed)
                z -= 30
                es.entitysetvalue(DoedP.index, 'origin', ' '.join(es.createvectorstring(x,y,z).split(',')))
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('bury', {'DoedName':DoedName,'DoerName':DoerName,'depth':50}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Bury', None))

def BlindBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                Blindness = SAC_Dict_Blind[int(Doed)]
                if (int(Blindness) == 0): BlindValue = 153
                elif (int(Blindness) == 153): BlindValue = 175
                elif (int(Blindness) == 175): BlindValue = 200
                elif (int(Blindness) == 200): BlindValue = 225
                elif (int(Blindness) == 225): BlindValue = 250
                elif (int(Blindness) == 250): BlindValue = 255
                else: BlindValue = 0
                SAC_Dict_Blind[int(Doed)] = BlindValue
                procent = round(BlindValue / 2.55, 2)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('blind', {'DoedName':DoedName,'DoerName':DoerName,'real':BlindValue,'procent':procent}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Blind', None))

def SlayBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                SlayEffects(Doed)
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('slay', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Slay', None))

def TeleportBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                es.entitysetvalue(DoedP.index, 'origin', ' '.join(SAC_Dict_Saveloc[int(Doer)].split(',')))
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('teleport', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Teleport', None))

def SetSkinBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    Doed = Doed.split("|")
    DoedOld = Doed
    Doed = Doed[0]
    if not Doed.startswith("UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            playerlib.getPlayer(Doed).setModel(DoedOld[2])
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('setSkin', {'DoedName':es.getplayername(Doed),'DoerName':es.getplayername(Doer),'SkinName':DoedOld[1]}, Lang(Player)))
    SACMenu_SkinsMenu_Selected(Doer,"%s|%s" %(DoedOld[1],DoedOld[2]),None)
    
def DrugBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                if (SAC_Dict_Drug[int(Doed)] != "0"):
                    SAC_Dict_Drug[int(Doed)] = "0"
                    es.cexec(Doed, "r_screenoverlay normal")
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('drug_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
                else:
                    SAC_Dict_Drug[int(Doed)] = "1"
                    es.cexec(Doed, "r_screenoverlay effects/tp_eyefx/tp_eyefx")
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('drug_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Drug', None))

def SlapBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                x = random.randint(-200, 200)
                y = random.randint(-200, 200)
                z = random.randint(200, 400)
                es.emitsound("player", Doed, 'player/damage%s.wav'%(random.randint(1,3)), 1, 0.2)
                es.setplayerprop(Doed, "CCSPlayer.baseclass.localdata.m_vecBaseVelocity", es.createvectorstring(x,y,z))
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('slap', {'DoedName':DoedName,'DoerName':DoerName, 'dmg':'0'}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Slap', None))

def FreezeBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                Freeze(Doer, Doed)
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Freeze', None))

def NoclipBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            DoedP = playerlib.getPlayer(Doed)
            if (DoedP.isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                if (DoedP.getNoClip()):
                    DoedP.noclip(0)
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('noclip_off', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
                else:
                    DoedP.noclip(1)
                    for Player in playerlib.getUseridList('#human'): tell(Player, translations('noclip_on', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Noclip', None))

def KickBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            es.server.insertcmd("kickid %s Kicked" %(Doed))
            for Player in playerlib.getUseridList('#human'): tell(Player, translations('kicked', {'DoedName':DoedName,'DoerName':DoerName}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler4, (Doer, 'Kick', None))

def MuteBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = es.getplayername(Doer)
            DoedName = es.getplayername(Doed)
            if int(Doed) not in SAC_Dict_Mute:
                SAC_Dict_Mute[int(Doed)] = 30
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('muted', {'DoedName':DoedName,'DoerName':DoerName,'minutes':'30'}, Lang(Player)))
            else:
                del SAC_Dict_Mute[int(Doed)]
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('muted', {'DoedName':DoedName,'DoerName':DoerName,'minutes':'0'}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler4, (Doer, 'Mute', None))

def SPTOPBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            if (int(es.getplayerteam(Doed)) == 2): changeTeam(Doer, Doed, 3)
            elif (int(es.getplayerteam(Doed)) == 3): changeTeam(Doer, Doed, 2)
            else: changeTeam(Doer, Doed, int(es.getplayerteam(Doed)))
    gamethread.delayed(0.01, MenuHandler4, (Doer, 'Swap Player To Opposite Team', None))

def SPTSBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else: changeTeam(Doer, Doed, 1)
    gamethread.delayed(0.01, MenuHandler4, (Doer, 'Swap Player To Spectator', None))

def SPTTBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else: changeTeam(Doer, Doed, 2)
    gamethread.delayed(0.01, MenuHandler4, (Doer, 'Swap Player To T', None))

def SPTCTBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else: changeTeam(Doer, Doed, 3)
    gamethread.delayed(0.01, MenuHandler4, (Doer, 'Swap Player To CT', None))

def GiveBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = str(es.getplayername(Doer))
            DoedName = str(es.getplayername(Doed))
            if (playerlib.getPlayer(Doed).isdead): tell(Doer, translations('dead', {'name':DoedName}, Lang(Doer)))
            else:
                item = SAC_Dict_Give[int(Doer)]
                es.server.insertcmd("es_xgive %s %s" %(Doed,item))
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('give', {'DoedName':DoedName,'DoerName':DoerName,'item':item}, Lang(Player)))
    gamethread.delayed(0.01, MenuHandler3, (Doer, 'Give Weapon2', None))

def BanBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    if (Doed != "UpdateList"):
        if not (es.exists('userid',Doed)): tell(Doer, translations('no_such_userid', {'userid':Doed}, Lang(Doer)))
        else:
            DoerName = str(es.getplayername(Doer)).replace("|","")
            DoedName = str(es.getplayername(Doed)).replace("|","")
            if IsBanned(es.getplayersteamid(Doed)): tell(Doer, '%s is already banned!' %(DoedName))
            else:
                File = open(cfgpath + '/banned.txt', 'a')
                File.write("\n|%s|%s|%s|%s|%s|" %(es.getplayersteamid(Doed),str(DoedName).replace("|", ""),str(DoerName).replace("|", ""),SAC_Dict_Ban[int(Doer)],SAC_Dict_Ban[int(Doer)]))
                File.close()
                gamethread.delayed(0.5, es.server.insertcmd, "kickid %s banned" %(Doed))
                for Player in playerlib.getUseridList('#human'): tell(Player, translations('banned', {'DoedName':DoedName,'DoerName':DoerName,'minutes':SAC_Dict_Ban[int(Doer)]}, Lang(Player)))
    if (Doer != Doed): gamethread.delayed(0.01, MenuHandler4, (Doer, 'Ban2', None))

def UnBanBlock(Doer, Doed, popupname):
    if not IsAdmin(Doer):
        NotAdmin(userid)
        return
    gamethread.delayed(0.01, MenuHandler4, (Doer, 'UnBan', None))
    if (Doed == "UpdateList"): return
    DoerName = es.getplayername(Doer)
    unbanneded = "%s (%s)" %(IsBanned(Doed[1]), Doed[1])
    for Player in playerlib.getUseridList('#human'): tell(Player, translations('unbanned', {'DoerName':DoerName,'unbanneded':unbanneded}, Lang(Player)))
    UnBan(Doed[1])