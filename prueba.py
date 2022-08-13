# from datetime import datetime
# # ts = int('1651105913') # End
# # ts2 = int('1651104453') # Start
# #
# #
# # # if you encounter a "year is out of range" error the timestamp
# # # may be in milliseconds, try `ts /= 1000` in that case
# # print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
# # print(datetime.utcfromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S'))
#
# h = datetime.fromtimestamp(1651104453760/1000)
# d = h.strftime("%m/%d/%Y, %H:%M:%S")
# h2 = datetime.fromtimestamp(1651105913467/1000)
# m = 1459/60
# print(f'Star: {d}')
# print(f'End: {h2}')
# print(f'Duracion: {m}')

import webbrowser
summoner = 'gg fructis'
webbrowser.open(f'https://euw.op.gg/summoners/euw/{summoner}', new=2)
