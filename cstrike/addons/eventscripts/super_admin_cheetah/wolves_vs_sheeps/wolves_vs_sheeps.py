import es
import playerlib

def unload():
    es.server.queuecmd("es_xgive %s func_buyzone enable" %(es.getuserid()))
    for Player in playerlib.getUseridList('#all'): playerlib.getPlayer(Player).setColor(255, 255, 255, 255)
        

def round_start(ev):
    es.server.queuecmd("es_xgive %s func_buyzone disable" %(es.getuserid()))

def round_end(ev):
    if int(ev['reason']) == 8:
        es.msg("#green", "---------------")
        es.msg("#green", "Wolves win !")
        es.msg("#green", "---------------")
    if int(ev['reason']) == 7: SheepsWon()
    if int(ev['reason']) == 10: SheepsWon()
    if int(ev['reason']) == 11: SheepsWon()

def SheepsWon():
    es.msg("#green", "---------------")
    es.msg("#green", "Sheeps win !")
    es.msg("#green", "---------------")
    for Player in playerlib.getUseridList('#t'): playerlib.getPlayer(Player).slay()

def player_spawn(ev):
    PlayerP = playerlib.getPlayer(ev['userid'])
    if int(ev['es_userteam']) == 2:
        es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "player_weaponstrip"))
        es.server.queuecmd("es_xfire %s player_weaponstrip strip" %(ev['userid']))
        es.server.queuecmd("es_xfire %s player_weaponstrip kill" %(ev['userid']))
        es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "weapon_knife"))
        PlayerP.setColor(255, 0, 0, 255)
    if int(ev['es_userteam']) == 3:
        es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "player_weaponstrip"))
        es.server.queuecmd("es_xfire %s player_weaponstrip strip" %(ev['userid']))
        es.server.queuecmd("es_xfire %s player_weaponstrip kill" %(ev['userid']))
        PlayerP.setColor(0, 0, 255, 255)

def item_pickup(ev):
    if (ev['item'] == "c4"): es.remove("weapon_c4")
    if int(ev['es_userteam']) == 2:
        if ev['item'] != "knife" and ev['item'] != "player_weaponstrip":
            es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "player_weaponstrip"))
            es.server.queuecmd("es_xfire %s player_weaponstrip strip" %(ev['userid']))
            es.server.queuecmd("es_xfire %s player_weaponstrip kill" %(ev['userid']))
            es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "weapon_knife"))
    if int(ev['es_userteam']) == 3:
        if ev['item'] != "player_weaponstrip":
            es.server.queuecmd("es_xgive %s %s" %(ev['userid'], "player_weaponstrip"))
            es.server.queuecmd("es_xfire %s player_weaponstrip strip" %(ev['userid']))
            es.server.queuecmd("es_xfire %s player_weaponstrip kill" %(ev['userid']))