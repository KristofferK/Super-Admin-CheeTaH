import es
import playerlib
import random
import gamethread
import usermsg


def load():
    global old_timelimit
    old_timelimit = es.ServerVar("mp_roundtime")
    es.ServerVar("mp_roundtime").set(9)
    gamethread.delayedname(0.100, "BlindDelayName", BlindLoop)
    gamethread.delayedname(0.100, "FixAmmo", FixAmmo)

def unload():
    es.ServerVar("mp_roundtime").set(old_timelimit)
    es.ServerVar("ammo_338mag_max").set(30)
    es.ServerVar("ammo_357sig_max").set(52)
    es.ServerVar("ammo_45acp_max").set(100)
    es.ServerVar("ammo_50AE_max").set(35)
    es.ServerVar("ammo_556mm_box_max").set(200)
    es.ServerVar("ammo_556mm_max").set(90)
    es.ServerVar("ammo_57mm_max").set(100)
    es.ServerVar("ammo_762mm_max").set(90)
    es.ServerVar("ammo_9mm_max").set(120)
    es.ServerVar("ammo_buckshot_max").set(32)
    gamethread.cancelDelayed("BlindDelayName")
    gamethread.cancelDelayed("FixAmmo")

def ammo(player):
    if not es.exists('userid',player): return
    PlayerP = playerlib.getPlayer(player)
    weapon1 = PlayerP.getPrimary()
    weapon2 = PlayerP.getSecondary()
    if weapon1:
        PlayerP.setClip(weapon1, 999)
        PlayerP.setAmmo(weapon1, 0)
    if weapon2:
        PlayerP.setClip(weapon2, 999)
        PlayerP.setAmmo(weapon2, 0)

def round_start(ev):
    Number = random.randint(1,5)
    Player = es.getuserid()
    if (Player):
        if (Number == 1): es.emitsound("player", Player, "music/HL2_song3.mp3", 0.45, 0)
        if (Number == 2): es.emitsound("player", Player, "music/HL2_song29.mp3", 0.45, 0)
        if (Number == 3): es.emitsound("player", Player, "music/HL2_song20_submix4.mp3", 0.45, 0)
        if (Number == 4): es.emitsound("player", Player, "music/HL2_song14.mp3", 0.45, 0)
        if (Number == 5): es.emitsound("player", Player, "music/HL2_song16.mp3", 0.45, 0)
    es.ServerVar("mp_roundtime").set(9)
    es.ServerVar("ammo_338mag_max").set(1000)
    es.ServerVar("ammo_357sig_max").set(1000)
    es.ServerVar("ammo_45acp_max").set(1000)
    es.ServerVar("ammo_50AE_max").set(1000)
    es.ServerVar("ammo_556mm_box_max").set(1000)
    es.ServerVar("ammo_556mm_max").set(1000)
    es.ServerVar("ammo_57mm_max").set(1000)
    es.ServerVar("ammo_762mm_max").set(1000)
    es.ServerVar("ammo_9mm_max").set(1000)
    es.ServerVar("ammo_buckshot_max").set(1000)

##############################################################
# WIN MESSAGE ADDEDED BY MAXOLAHIRD FROM WOLVES_VS_SHEEPS.PY #
#       IDK IF IS CORRECTLY, IF ISN'T, CORRECT PLEASE        #
##############################################################
def round_end(ev):
    if int(ev['reason']) == 8:
        es.msg("#green", "------------")
        es.msg("#green", "Zombies Win!")
        es.msg("#green", "------------")
    if int(ev['reason']) == 7: SurvivorsWon()
    if int(ev['reason']) == 10: SurvivorsWon()
    if int(ev['reason']) == 11: SurvivorsWon()
	
def SurvivorsWon():
    es.msg("#green", "--------------")
    es.msg("#green", "Survivors Win!")
    es.msg("#green", "--------------")
    for Player in playerlib.getUseridList('#t'): playerlib.getPlayer(Player).slay()

def item_pickup(ev):
    if (ev['item'] == "c4"): es.remove("weapon_c4")
    if (ev['es_userteam'] == "2"):
        if ev['item'] != "knife" and ev['item'] != "player_weaponstrip":
            es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "player_weaponstrip"))
            es.server.queuecmd("es_xfire %s player_weaponstrip strip" %(ev['userid']))
            es.server.queuecmd("es_xfire %s player_weaponstrip kill" %(ev['userid']))
            es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "weapon_knife"))
    if (ev['es_userteam'] == "3"):
        ammo(ev['userid'])

def player_spawn(ev):
    PlayerP = playerlib.getPlayer(ev['userid'])
    if (ev['es_userteam'] == "2"):
        es.setplayerprop(ev['userid'], "CBasePlayer.m_iHealth", 4000)
        es.setplayerprop(ev['userid'], "CBasePlayer.localdata.m_flLaggedMovementValue", 1.2)
        es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "player_weaponstrip"))
        es.server.queuecmd("es_xfire %s player_weaponstrip strip" %(ev['userid']))
        es.server.queuecmd("es_xfire %s player_weaponstrip kill" %(ev['userid']))
        es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "weapon_knife"))
    if (ev['es_userteam'] == "3"):
        es.setplayerprop(ev['userid'], "CBasePlayer.m_iHealth", 100)
        es.cexec(ev['userid'], "play vo/npc/male01/zombies01.wav")
        ammo(ev['userid'])

def player_blind(ev):
    if (ev['es_userteam'] == "3"):
        es.setplayerprop(ev['userid'], "CCSPlayer.m_flFlashDuration", "1")
        es.setplayerprop(ev['userid'], "CCSPlayer.m_flFlashMaxAlpha", "1")

def player_hurt(ev):
    if (ev['es_userteam'] == "2"): es.emitsound("player", ev['userid'], "npc/zombie/zombie_pain%i.wav"%(random.randint(1,6)), 1, 0.5)
    if (ev['es_userteam'] == "3"): es.emitsound("player", ev['userid'], "vo/npc/male01/pain0%i.wav"%(random.randint(1,9)), 1, 0.5)

def player_death(ev):
    if (ev['es_userteam'] == "2"): es.emitsound("player", ev['userid'], "npc/zombie/zombie_die%i.wav"%(random.randint(1,3)), 1, 0.5)
    if (ev['es_userteam'] == "3"): es.emitsound("player", ev['userid'], "vo/npc/male01/no0%i.wav"%(random.randint(1,2)), 1, 0.5)

def BlindLoop():
    Players = playerlib.getUseridList('#alive,#t')
    if (Players):
        for Blindie in Players:
            usermsg.fade(Blindie, 2, 250, 300, 255, 0, 0, 50)
    gamethread.delayedname(0.25, "BlindDelayName", BlindLoop)

def FixAmmo():
    Players = playerlib.getUseridList('#alive,#ct')
    if (Players):
        for Ammoer in Players:
            ammo(Ammoer)
    gamethread.delayedname(1, "FixAmmo", FixAmmo)