from riotwatcher import LolWatcher, ApiError
import pandas as pd
import json

# golbal variables
api_key = 'RGAPI-7cf73907-6c03-43eb-8816-baeb4fc0ed0a'
watcher = LolWatcher(api_key)
my_region = 'EUW1'
player = input("Introduce el nombre: ")

me = watcher.summoner.by_name(my_region, player)
print(me)
puuid = me['puuid']
idd = me['id']
# h = watcher.spectator.by_summoner('EUW1', idd)
# print(h)

# Return the rank status for Doublelift
my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
print(my_ranked_stats)

my_matches = watcher.match.matchlist_by_puuid(my_region, puuid)

# fetch last match detail
last_match = my_matches[0]
f = watcher.league.challenger_by_queue('EUW1', 'RANKED_SOLO_5x5')
for l in f['entries']:
    print(l['summonerName'])
match_detail = watcher.match.by_id(my_region, last_match)

# print(match_detail)
# pretty = json.dumps(f, indent=4)
# with open('nuevo2.txt', mode='w') as f:
#     f.writelines(pretty)
# print(pretty)
cont = 1
for match in my_matches:
    match_detail = watcher.match.by_id(my_region, match)
    participants = []
    for puid in match_detail['metadata']['participants']:
        participants.append(watcher.summoner.by_puuid(my_region, puid)['name'])

    par = [i for i in participants[0:5]]
    champ1 = [i['championName'] for i in match_detail['info']['participants'][0:5]]
    role1 = [i['individualPosition'] for i in match_detail['info']['participants'][0:5]]
    kills = [i['kills'] for i in match_detail['info']['participants'][0:5]]
    deaths1 = [i['deaths'] for i in match_detail['info']['participants'][0:5]]
    assists1 = [i['assists'] for i in match_detail['info']['participants'][0:5]]
    wards1 = [i['wardsPlaced'] for i in match_detail['info']['participants'][0:5]]
    gold = [i['goldEarned'] for i in match_detail['info']['participants'][0:5]]
    minions = [i['totalMinionsKilled'] for i in match_detail['info']['participants'][0:5]]
    neu_minions = [i['neutralMinionsKilled'] for i in match_detail['info']['participants'][0:5]]
    suma1 = [x + y for x, y in zip(minions, neu_minions)]
    dano_total = [i['totalDamageDealtToChampions'] for i in match_detail['info']['participants'][0:5]]
    dano_recibido = [i['totalDamageTaken'] for i in match_detail['info']['participants'][0:5]]


    data = {
                'Invocador': par,
                'Champion': champ1,
                'Role': role1,
                'Kills': kills,
                'Deaths': deaths1,
                'Assists': assists1,
                'Wards': wards1,
                'Gold Earned': gold,
                'Farm': suma1,
                'Daño total': dano_total,
                'Daño recibido': dano_recibido,
                'Win': f"{match_detail['info']['teams'][0]['win']}"
            }

    par2 = [i for i in participants[5:10]]
    champ2 = [i['championName'] for i in match_detail['info']['participants'][5:10]]
    role2 = [i['individualPosition'] for i in match_detail['info']['participants'][5:10]]
    kills2 = [i['kills'] for i in match_detail['info']['participants'][5:10]]
    deaths2 = [i['deaths'] for i in match_detail['info']['participants'][5:10]]
    assists2 = [i['assists'] for i in match_detail['info']['participants'][5:10]]
    wards2 = [i['wardsPlaced'] for i in match_detail['info']['participants'][5:10]]
    gold2 = [i['goldEarned'] for i in match_detail['info']['participants'][5:10]]
    minions2 = [i['totalMinionsKilled'] for i in match_detail['info']['participants'][5:10]]
    neu_minions2 = [i['neutralMinionsKilled'] for i in match_detail['info']['participants'][5:10]]
    suma = [x + y for x, y in zip(minions2, neu_minions2)]
    dano_total2 = [i['totalDamageDealtToChampions'] for i in match_detail['info']['participants'][5:10]]
    dano_recibido2 = [i['totalDamageTaken'] for i in match_detail['info']['participants'][5:10]]

    data2 = {
                'Invocador': par2,
                'Champion': champ2,
                'Role': role2,
                'Kills': kills2,
                'Deaths': deaths2,
                'Assists': assists2,
                'Wards': wards2,
                'Gold Earned': gold2,
                'Farm': suma,
                'Daño total': dano_total2,
                'Daño recibido': dano_recibido2,
                'Win': f"{match_detail['info']['teams'][1]['win']}"
            }

    df = pd.DataFrame(data, index=['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5'])
    df['Role'].replace(to_replace=dict(UTILITY='SUPPORT'), inplace=True)
    df2 = pd.DataFrame(data2, index=['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5'])
    df2['Role'].replace(to_replace=dict(UTILITY='SUPPORT'), inplace=True)
    print("GAME ", cont)
    print(df)
    print(df2)
    cont += 1

# print(f'Equipo azul: {participants[0]} - {participants[1]} - {participants[2]} - {participants[3]}'
#       f' - {participants[4]}')
# print(f'Equipo rojo: {participants[5]} - {participants[6]} - {participants[7]} - {participants[8]}'
#       f' - {participants[9]}')
