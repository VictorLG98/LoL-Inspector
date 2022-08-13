from riotwatcher import LolWatcher
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from requests.exceptions import HTTPError
from datetime import datetime
import webbrowser
from threading import Thread
import os
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("API")


class LoLInterface:
    """
    Interface that allows user to search for League of Legends Summoners info, ranked stats,
    matches...
    """

    def __init__(self):
        self.summoner_result = ""
        # Api key needed to work with Riot Api
        self.api_key = API

        # LolWatcher instance creation
        self.watcher = LolWatcher(self.api_key)
        self.puuid = ""
        self.my_matches = 0
        self.window = Tk()
        self.my_region = ""

        # Treeview style
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 14, 'bold'), foreground='blue')
        self.style.configure("mystyle.Treeview", background="#b5c3f7", font=('Comic Sans MS', 11), rowheight=25,
                             foreground='black', fieldbackground='#3e61de', highlightthickness=0, bd=0,)
        self.style.map('Treeview',
                       background=[('selected', 'blue')])
        self.window.title("League of Legends Inspector")
        self.window.resizable(False, False)
        self.window.config(pady=10, padx=10, background='#05061a')

        # New window
        self.new_win = Toplevel(self.window)
        self.new_win.resizable(False, False)
        self.new_win.config(bg='#05061a')
        self.my_tree = ttk.Treeview(self.new_win, selectmode=BROWSE, style="mystyle.Treeview")
        self.new_win.withdraw()

        # New window
        self.new_win2 = Toplevel(self.window)
        self.new_win2.resizable(False, False)
        self.new_win2.config(bg='#378060')
        self.new_win2.withdraw()

        # New window
        self.new_win3 = Toplevel(self.window)
        self.new_win3.resizable(False, False)
        self.new_win3.config(bg='#378060')
        self.new_win3.withdraw()

        # New window
        self.new_win4 = Toplevel(self.window)
        self.new_win4.resizable(False, False)
        self.new_win4.config(bg='#378060')
        self.new_win4.withdraw()

        # Protocol when user press close window button
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing5)
        self.new_win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.new_win2.protocol("WM_DELETE_WINDOW", self.on_closing2)
        self.new_win3.protocol("WM_DELETE_WINDOW", self.on_closing3)
        self.new_win4.protocol("WM_DELETE_WINDOW", self.on_closing4)

        # Listbox creation and configuration
        self.list = Listbox(justify=CENTER)
        self.list.config(borderwidth=2, activestyle=NONE, fg="white",
                          bg="#1d238c", font=("Arial", 15, "bold"), selectforeground="#03f8fc",
                          selectbackground="#03052e", selectborderwidth=2, selectmode=SINGLE,
                         highlightbackground='#313cf7', highlightcolor='#2029c7')
        self.list.grid(row=1, column=0, columnspan=2, pady=10, sticky=EW)

        # Scrollbar creation for Listbox
        self.scroll = Scrollbar()
        self.scroll.grid(row=1, column=2, sticky=NS, pady=10)
        self.list.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.list.yview)

        # Labels, Entries and Buttons...
        self.label = Label(text="Summoner name: ",
                           font=('Comic Sans MS', 15, 'bold'), background='#05061a', foreground='#0f1adb')
        self.label.grid(row=2, column=0)
        self.text = Entry(justify=CENTER, font=('Comic Sans MS', 13, 'bold'), foreground='black',
                          background='white', insertbackground='blue')
        self.text.grid(row=2, column=1)
        self.clear_entry = Button(text='Clear', command=self.clear, font=('Comic Sans MS', 10, 'bold'),
                                  background='#858aed', width=10)
        self.clear_entry.grid(row=3, column=1)
        self.buscar_btn = Button(text="Search Summoner", command=self.buscar_Invocador,
                                 font=('Comic Sans MS', 14, 'bold'), background='#858aed')
        self.buscar_btn.grid(row=5, column=0, sticky=EW, columnspan=3, pady=10)
        self.view_ranked = Button(text="View ranked info", command=self.view_ranked_info,
                                  font=('Comic Sans MS', 14, 'bold'), background='#858aed')
        self.view_ranked.grid(row=6, column=0, sticky=EW, columnspan=3)
        self.region_label = Label(text="Player region: ", font=('Comic Sans MS', 15, 'bold'),
                                  background='#05061a', foreground='#0f1adb')
        self.region_label.grid(row=4, column=0, sticky=E)

        # Combobox to select the Summoner region
        self.combo = ttk.Combobox(self.window, state="readonly",
                                  values=['EUW1', 'BR1', 'EUN1', 'JP1', 'KR', 'LA1', 'LA2', 'NA1',
                                          'OC1', 'TR1', 'RU'], font=('Comic Sans MS', 10, 'bold'),
                                  justify=CENTER)
        self.combo.grid(row=4, column=1, pady=10, sticky=W)
        self.last_20 = Label(text="Last 20 games of", font=('Comic Sans MS', 14, 'bold'), background='#05061a',
                             foreground='#0f1adb')
        self.last_20.grid(row=0, column=0, columnspan=2)
        self.view_active = Button(text="View active game", command=self.thread,
                                  font=('Comic Sans MS', 14, 'bold'), background='#858aed')
        self.view_active.grid(row=7, column=0, sticky=EW, pady=10, columnspan=3)
        self.top_p = Button(text="Top Challenger Players", command=self.top_Players,
                                  font=('Comic Sans MS', 14, 'bold'), background='#858aed')
        self.top_p.grid(row=8, column=0, sticky=EW, columnspan=3)
        self.loadbtn = Button(text="Recent Searches", command=self.loadPlayers,
                            font=('Comic Sans MS', 14, 'bold'), background='#858aed')
        self.loadbtn.grid(row=9, column=0, sticky=EW, columnspan=3, pady=10)
        self.listbox = Listbox(self.new_win4, justify=CENTER)

        self.selection = 0
        self.list.select_set(self.selection)
        self.list.bind("<Down>", self.OnEntryDown)
        self.list.bind("<Up>", self.OnEntryUp)
        self.listbox.bind('<Double-Button>', self.double_click2)

        self.window.mainloop()

    def clear(self):
        self.text.delete(0, END)

    def thread(self):
        s = Thread(target=self.view_active_game)
        s.start()

    def OnEntryDown(self, event):
        if self.selection < self.list.size() - 1:
            self.list.select_clear(self.selection)
            self.selection += 1
            self.list.select_set(self.selection)

    def OnEntryUp(self, event):
        if self.selection > 0:
            self.list.select_clear(self.selection)
            self.selection -= 1
            self.list.select_set(self.selection)

    def view_ranked_info(self):
        """Function that shows a message box with info about the Summoner ranked status"""

        # Get the combo item
        self.my_region = self.combo.get()

        # If statement to check if Summoner Entry is correct
        if self.text.get() == "" or self.text.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title="Error!", message="You must enter a summoner name and region.")
        else:
            try:
                # We get the Summoner info
                me = self.watcher.summoner.by_name(self.my_region, self.text.get())

                # Get the summoner ranked info
                my_ranked_stats = self.watcher.league.by_summoner(self.my_region, me['id'])
            except HTTPError:
                messagebox.showerror(title="Error!", message="You must enter a correct Summoner name or refresh the"
                                                             " api key"
                                                             " or the Summoner does not exist in the specified region")
            except UnicodeEncodeError:
                messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
            else:
                try:
                    self.savePlayers()
                    # Calculate the winrate
                    winrate = my_ranked_stats[0]['wins']/(my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
                    winrate = winrate*100

                    # Messagebox with all the info
                    messagebox.showinfo(title=f"{self.text.get()} ranked info",
message=f"""
Mode: {my_ranked_stats[0]['queueType']}\n
Elo: {my_ranked_stats[0]['tier']}\n
League Points: {my_ranked_stats[0]['leaguePoints']}\n
Wins: {my_ranked_stats[0]['wins']}\n
Losses: {my_ranked_stats[0]['losses']}\n
Games: {my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses']}\n
Winrate: {round(winrate)}%\n
HotSreak: {my_ranked_stats[0]['hotStreak']}\n
""")
                except IndexError:
                    messagebox.showwarning(title="Atención!", message="The player has not completed the placement"
                                                                      " games.")

    def buscar_Invocador(self):
        """Function that gets the last 20 games of the Summoner and adds them to the Listbox"""

        self.my_region = self.combo.get()
        if self.text.get() == "" or self.text.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title="Error!", message="You must enter a summoner name and region.")
        else:
            try:
                me = self.watcher.summoner.by_name(self.my_region, self.text.get())
            except HTTPError:
                messagebox.showerror(title="Error!", message="You must enter a correct Summoner name or refresh the"
                                                             " api key"
                                                             " or the Summoner does not exist in the specified region")
            except UnicodeEncodeError:
                messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
            else:
                self.savePlayers()

                self.puuid = me['puuid']

                # We search for the Summoner matches
                self.my_matches = self.watcher.match.matchlist_by_puuid(self.my_region, self.puuid)
                self.list.delete(0, END)

                for i in range(1, 21):
                    self.list.insert(END, f'{me["name"]} 🡺 Game {i}')

                # Bind that allows user to interact with Listbox items by double clicking them
                self.list.bind("<Double-1>", self.OnDoubleClick)
                self.list.bind("<Return>", self.OnDoubleClick)
                self.last_20.config(text=f"Last 20 games of {me['name']}")

    def OnDoubleClick(self, event):
        """
        Function that allows user to interact with Listbox items by double clicking them and
            shows a pop up window with a Treeview with all game selected info
        """

        self.new_win.config(cursor='top_left_arrow')
        item = self.list.curselection()
        item2 = ''.join(map(str, item))
        try:
            match_detail = self.watcher.match.by_id(self.my_region, self.my_matches[int(item2)])
        except HTTPError:
            messagebox.showerror(title='Error!', message='Close the window and try again.')
        participants = []
        for puid in match_detail['metadata']['participants']:
            participants.append(self.watcher.summoner.by_puuid(self.my_region, puid)['name'])

        par = [i for i in participants]
        champ1 = [i['championName'] for i in match_detail['info']['participants']]
        role1 = [i['individualPosition'] for i in match_detail['info']['participants']]
        kills = [i['kills'] for i in match_detail['info']['participants']]
        deaths1 = [i['deaths'] for i in match_detail['info']['participants']]
        assists1 = [i['assists'] for i in match_detail['info']['participants']]
        wards1 = [i['wardsPlaced'] for i in match_detail['info']['participants']]
        gold = [i['goldEarned'] for i in match_detail['info']['participants']]
        minions = [i['totalMinionsKilled'] for i in match_detail['info']['participants']]
        neu_minions = [i['neutralMinionsKilled'] for i in match_detail['info']['participants']]
        suma1 = [x + y for x, y in zip(minions, neu_minions)]
        dano_total = [i['totalDamageDealtToChampions'] for i in match_detail['info']['participants']]
        dano_recibido = [i['totalDamageTaken'] for i in match_detail['info']['participants']]
        win = [i['win'] for i in match_detail['info']['participants']]

        data = {
            'Summoner': par,
            'Champion': champ1,
            'Role': role1,
            'Kills': kills,
            'Deaths': deaths1,
            'Assists': assists1,
            'Wards': wards1,
            'Gold Earned': gold,
            'Farm': suma1,
            'Total Damage Dealt': dano_total,
            'Total Taken Damage': dano_recibido,
            'Result': win
        }

        # Create pandas Dataframe
        df = pd.DataFrame(data)
        df['Role'].replace(to_replace=dict(UTILITY='SUPPORT'), inplace=True)
        df['Champion'].replace(to_replace=dict(MonkeyKing='Wukong'), inplace=True)
        df['Result'].replace({True: 'VICTORY', False: 'DEFEAT'}, inplace=True)
        # self.summoner_result = str(df.loc[df['Summoner'] == self.text.get()]['Result'])
        game_start = datetime.fromtimestamp(match_detail['info']['gameStartTimestamp']/1000)
        game_start = game_start.strftime("%m/%d/%Y - %H:%M:%S")
        game_end = datetime.fromtimestamp(match_detail['info']['gameEndTimestamp'] / 1000)
        game_end = game_end.strftime("%m/%d/%Y - %H:%M:%S")
        game_duration = round(match_detail['info']['gameDuration']/60)

        for name in match_detail['info']['participants']:
            if str(name['summonerName']).lower() == self.text.get().lower():
                if name['win']:
                    self.summoner_result = "VICTORY"
                else:
                    self.summoner_result = "DEFEAT"

        for r in role1:
            if r == 'Invalid':
                match_de = 'ARAM'
            else:
                match_de = match_detail["info"]["gameType"]

        self.new_win.title(f'[Game ID: {match_detail["info"]["gameId"]}] [Game Type:'
                                   f' {match_de}]'
                                   f' [Summoner Result: [{self.summoner_result}] '
                           f'[Game Start: {game_start}] [Game End: {game_end}]'
                           f' [Game Duration: {game_duration} minutes]')

        # Had to delete Treeview object because a bug¿?
        del self.my_tree

        # Create the Treeview with DataFrame info
        self.my_tree = ttk.Treeview(self.new_win, selectmode=BROWSE, style="mystyle.Treeview")
        self.my_tree["column"] = list(df.columns)
        self.my_tree["show"] = "headings"
        self.my_tree.bind('<Double-Button>', self.double_click3)
        self.my_tree.bind('<Return>', self.double_click3)

        for column in self.my_tree["column"]:
            self.my_tree.heading(column, text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.my_tree.insert("", END, values=row)

        def copyy():
            try:
                curItem = self.my_tree.focus()
                item = self.my_tree.item(curItem)
                self.new_win.clipboard_clear()
                self.new_win.clipboard_append(item['values'][0])
                messagebox.showinfo(title="Info!", message="Copied succesfully!")
            except IndexError:
                messagebox.showwarning(title="Atention!", message="You must make a selection.")

        self.my_tree.column("Summoner", width=150, minwidth=150, anchor=CENTER)
        self.my_tree.column("Champion", width=100, minwidth=100, anchor=CENTER)
        self.my_tree.column("Role", width=100, minwidth=100, anchor=CENTER)
        self.my_tree.column("Kills", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("Deaths", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("Assists", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("Wards", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("Gold Earned", width=120, minwidth=120, anchor=CENTER)
        self.my_tree.column("Farm", width=80, minwidth=80, anchor=CENTER)
        self.my_tree.column("Total Damage Dealt", width=190, minwidth=190, anchor=CENTER)
        self.my_tree.column("Total Taken Damage", width=190, minwidth=190, anchor=CENTER)
        self.my_tree.column("Result", width=100, minwidth=100, anchor=CENTER)
        m = Menu(self.new_win, tearoff=0)
        m.add_command(label="View Player OPGG", command=self.view_opgg)
        m.add_command(label="Copy Summoner Name", command=copyy)

        def do_popup(event):
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

        self.my_tree.bind("<Button-3>", do_popup)

        self.my_tree.grid(row=0, column=0)

        self.window.grab_set()
        self.new_win.deiconify()

    def on_closing5(self):
        """Function that triggers when user closes second window."""
        m = messagebox.askyesno(title="Exit?", message="Are you sure you want to exit?")
        if m:
            self.window.destroy()

    def on_closing(self):
        """Function that triggers when user closes second window."""

        self.new_win.withdraw()

    def on_closing2(self):
        """Function that triggers when user closes second window."""

        self.new_win2.withdraw()

    def on_closing3(self):
        """Function that triggers when user closes second window."""

        self.new_win3.withdraw()

    def on_closing4(self):
        """Function that triggers when user closes second window."""

        self.new_win4.withdraw()

    def view_active_game(self):
        """
        Function that allows user to look at the game that player is actually playing.
        """

        self.my_region = self.combo.get()

        if self.text.get() == "" or self.text.get().isspace() or self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title='Error!', message='You must enter a Summoner name and region.')
        else:
            try:
                me = self.watcher.summoner.by_name(self.my_region, self.text.get())
                me_now = me['name']
                active_game = self.watcher.spectator.by_summoner('EUW1', me['id'])
            except HTTPError:
                messagebox.showerror(title='Error!', message='Requested Summoner is not in an active game.')
            except UnicodeEncodeError:
                messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")
            else:
                participants = []
                elos = []
                l_points = []
                wins = []
                losses = []
                hot_streak = []
                win_r = []
                total_g = []
                rank = []
                for p in active_game['participants']:
                    participants.append(p['summonerName'])

                for p in participants:
                    me = self.watcher.summoner.by_name(self.my_region, p)
                    my_ranked_stats = self.watcher.league.by_summoner(self.my_region, me['id'])
                    try:
                        elos.append(my_ranked_stats[0]['tier'])
                        l_points.append(my_ranked_stats[0]['leaguePoints'])
                        wins.append(my_ranked_stats[0]['wins'])
                        losses.append(my_ranked_stats[0]['losses'])
                        hot_streak.append(my_ranked_stats[0]['hotStreak'])
                        winrate = my_ranked_stats[0]['wins'] / (
                                    my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
                        winrate = winrate * 100
                        win_r.append(f'{round(winrate)}%')
                        total_g.append(my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
                        rank.append(my_ranked_stats[0]['rank'])
                    except KeyError:
                        messagebox.showwarning(title="Error!", message="Something went wrong, try again")
                    except ValueError:
                        messagebox.showwarning(title="Error!", message="Something went wrong, try again")

                par = [i for i in participants]

                game_start = datetime.fromtimestamp(active_game['gameStartTime'] / 1000)
                game_start = game_start.strftime("%m/%d/%Y - %H:%M:%S")
                game_duration = round(active_game['gameLength'] / 60)

                data = {
                    'Summoner': par,
                    'Elo': elos,
                    'Division': rank,
                    'League Points': l_points,
                    'Wins': wins,
                    'Losses': losses,
                    'Total Games': total_g,
                    'Win Rate': win_r
                }

                def copyy():
                    try:
                        curItem = my_tree2.focus()
                        item = my_tree2.item(curItem)
                        self.new_win2.clipboard_clear()
                        self.new_win2.clipboard_append(item['values'][0])
                        messagebox.showinfo(title="Info!", message="Copied succesfully!")
                    except IndexError:
                        messagebox.showwarning(title="Atention!", message="You must make a selection.")

                # Create pandas Dataframe
                try:
                    df = pd.DataFrame(data)
                except ValueError:
                    messagebox.showwarning(title="Error!", message="Something went wrong, try again")
                else:

                    my_tree2 = ttk.Treeview(self.new_win2, selectmode=BROWSE, style="mystyle.Treeview")
                    my_tree2["column"] = list(df.columns)
                    my_tree2["show"] = "headings"

                    for column in my_tree2["column"]:
                        my_tree2.heading(column, text=column)

                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        my_tree2.insert("", END, values=row)

                    my_tree2.column("Summoner", width=150, minwidth=150, anchor=CENTER)
                    my_tree2.column("Elo", width=140, minwidth=140, anchor=CENTER)
                    my_tree2.column("Division", width=100, minwidth=100, anchor=CENTER)
                    my_tree2.column("League Points", width=140, minwidth=140, anchor=CENTER)
                    my_tree2.column("Wins", width=80, minwidth=80, anchor=CENTER)
                    my_tree2.column("Losses", width=80, minwidth=80, anchor=CENTER)
                    my_tree2.column("Total Games", width=140, minwidth=140, anchor=CENTER)
                    my_tree2.column("Win Rate", width=120, minwidth=120, anchor=CENTER)

                    m = Menu(self.new_win2, tearoff=0)
                    m.add_command(label="View Player OPGG", command=self.view_opgg)
                    m.add_command(label="Copy Summoner Name", command=copyy)

                    def do_popup(event):
                        try:
                            m.tk_popup(event.x_root, event.y_root)
                        finally:
                            m.grab_release()

                    my_tree2.bind("<Button-3>", do_popup)

                    my_tree2.grid(row=0, column=0)

                    self.new_win2.title(f'{me_now} is now playing! '
                                        f'[Game Start: {game_start}] [Game Actual Duration: {game_duration} minutes]')

                    self.savePlayers()
                    self.window.grab_set()
                    self.new_win2.deiconify()

    def top_Players(self):
        """Pop up window that shows a Treeview with the best players of the specified region"""

        if self.combo.get() == "" or self.combo.get().isspace():
            messagebox.showerror(title="Error!", message="You must specify the Region.")
        else:
            top = self.watcher.league.challenger_by_queue(self.combo.get(), 'RANKED_SOLO_5x5')

            name = [i['summonerName'] for i in top['entries']]
            points = [i['leaguePoints'] for i in top['entries']]
            wins = [i['wins'] for i in top['entries']]
            losses = [i['losses'] for i in top['entries']]

            data = {
                'Summoner': name,
                'League Points': points,
                'Wins': wins,
                'Losses': losses,
            }

            df = pd.DataFrame(data)
            df.sort_values(by=['League Points'], ascending=False, inplace=True)

            my_tree3 = ttk.Treeview(self.new_win3, selectmode=BROWSE, style="mystyle.Treeview")
            my_tree3["column"] = list(df.columns)
            my_tree3["show"] = "headings"

            scroll = Scrollbar(self.new_win3, orient="vertical", command=my_tree3.yview)
            scroll.grid(row=0, column=1, sticky=NS)

            my_tree3.configure(yscrollcommand=scroll.set)

            for column in my_tree3["column"]:
                my_tree3.heading(column, text=column)

            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                my_tree3.insert("", END, values=row)

            my_tree3.column("Summoner", width=150, minwidth=150, anchor=CENTER)
            my_tree3.column("League Points", width=140, minwidth=140, anchor=CENTER)
            my_tree3.column("Wins", width=100, minwidth=100, anchor=CENTER)
            my_tree3.column("Losses", width=100, minwidth=100, anchor=CENTER)

            my_tree3.grid(row=0, column=0)

            def copyy():
                try:
                    curItem = my_tree3.focus()
                    item = my_tree3.item(curItem)
                    self.window.clipboard_clear()
                    self.window.clipboard_append(item['values'][0])
                    messagebox.showinfo(title="Info!", message="Copied succesfully!")
                except IndexError:
                    messagebox.showwarning(title="Atention!", message="You must make a selection.")

            def opgg():
                curItem = my_tree3.focus()
                if curItem:
                    item = my_tree3.item(curItem)
                    if self.combo.get() == 'EUW1':
                        region = 'euw'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'NA1':
                        region = 'na'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'BR1':
                        region = 'br'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'JP1':
                        region = 'jp'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'EUN1':
                        region = 'eune'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'KR':
                        region = 'kr'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'LA1':
                        region = 'lan'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'LA2':
                        region = 'las'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'OC1':
                        region = 'oce'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'TR1':
                        region = 'tr'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                    elif self.combo.get() == 'RU':
                        region = 'ru'
                        webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
                else:
                    messagebox.showwarning(title="Atention!", message="You must select an element.")

            def info():
                curItem = my_tree3.focus()
                item = my_tree3.item(curItem)

                self.my_region = self.combo.get()
                # We get the Summoner info
                try:
                    me = self.watcher.summoner.by_name(self.my_region, item['values'][0])
                    my_ranked_stats = self.watcher.league.by_summoner(self.my_region, me['id'])
                    total_games = my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses']
                    winrate = my_ranked_stats[0]['wins'] / (
                            my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
                    winrate = round(winrate * 100)

                    messagebox.showinfo(title=f"{item['values'][0]}",
message=f"""
Elo: {my_ranked_stats[0]['tier']}
League Points: {my_ranked_stats[0]['leaguePoints']}
Wins: {my_ranked_stats[0]['wins']}
Losses: {my_ranked_stats[0]['losses']}
Total Games: {total_games}
Win Rate: {winrate}%
""")
                except HTTPError:
                    messagebox.showerror(title='Error!', message='Summoner selected region is invalid.')
                except IndexError:
                    messagebox.showerror(title='Error!', message="Summoner selected region is invalid.")

            m = Menu(self.new_win3, tearoff=0)
            m.add_command(label="Copy Summoner Name", command=copyy)
            m.add_command(label="Search Ranked Info", command=info)
            m.add_command(label="Search Player OPGG", command=opgg)

            def do_popup(event):
                try:
                    m.tk_popup(event.x_root, event.y_root)
                finally:
                    m.grab_release()

            my_tree3.bind("<Button-3>", do_popup)

            self.new_win3.title(f'Top {len(name)} Challenger Players of {self.combo.get()}')
            self.savePlayers()

            self.window.grab_set()
            self.new_win3.deiconify()

    def savePlayers(self):
        try:
            with open('summoners.txt', mode='a') as f:
                f.writelines(f"{self.text.get()} | {self.combo.get()}\n")
            f.close()
        except UnicodeEncodeError:
            with open('summoners.txt', mode='a', encoding='utf-8') as f:
                f.writelines(f"{self.text.get()} | {self.combo.get()}\n")
            f.close()

    def loadPlayers(self):
        self.listbox.delete(0, END)
        scroll = Scrollbar(self.new_win4)
        scroll.grid(row=0, column=1, sticky=NS)
        try:
            with open('summoners.txt', mode='r', encoding='utf-8') as f:
                content = f.readlines()
            f.close()
        except FileNotFoundError:
            messagebox.showwarning(title="Atención!", message="There are not recent searchs or"
                                                              " not 5 searches at least.")
        except UnicodeEncodeError:
            with open('summoners.txt', mode='r', encoding='euc_kr') as f:
                content = f.readlines()
            f.close()
        else:

            final_content = list(dict.fromkeys(content))

            f_cont = []
            for i in final_content:
                f_cont.append(i.replace('\n', ''))

            strings = [x for x in f_cont if x]

            self.listbox.config(borderwidth=2, activestyle=NONE, fg="white",
                             bg="#1d238c", font=("Arial", 15, "bold"), selectforeground="#03f8fc",
                             selectbackground="#03052e", selectborderwidth=2, selectmode=SINGLE,
                             highlightbackground='#313cf7', highlightcolor='#2029c7', yscrollcommand=scroll.set,
                                width=33)
            scroll.config(command=self.listbox.yview)
            btn = Button(self.new_win4, text="Limpiar historial", command=self.limpiarHist,
                         font=('Comic Sans MS', 14, 'bold'), background='#858aed')
            btn.grid(row=1, column=0, sticky=EW, columnspan=2)

            if len(strings) >= 5:
                self.listbox.insert(END, *strings)
                self.listbox.grid(row=0, column=0)
                self.new_win4.title(f'Last {len(strings)} searches')
                self.new_win4.config(bg='blue')

                self.window.grab_set()
                self.new_win4.deiconify()

            else:
                messagebox.showwarning(title="Atención!", message="There are not 5 searches at least.")

    def double_click2(self, event):
        """Called when user double clicks element from ListBox"""
        self.text.delete(0, 'end')
        content = self.listbox.get(self.listbox.curselection())
        content = content.split(sep=' | ')
        self.window.clipboard_clear()
        self.window.clipboard_append(content[0])
        self.text.insert(0, content[0])
        self.combo.set(content[1])

    def double_click3(self, event):
        """Called when user double clicks element from ListBox"""
        curItem = self.my_tree.focus()
        item = self.my_tree.item(curItem)

        self.my_region = self.combo.get()
        # We get the Summoner info
        try:
            me = self.watcher.summoner.by_name(self.my_region, item['values'][0])
            my_ranked_stats = self.watcher.league.by_summoner(self.my_region, me['id'])
            total_games = my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses']
            winrate = my_ranked_stats[0]['wins'] / (
                    my_ranked_stats[0]['wins'] + my_ranked_stats[0]['losses'])
            winrate = round(winrate * 100)

            messagebox.showinfo(title=f"{item['values'][0]}",
                                message=f"""
                Elo: {my_ranked_stats[0]['tier']}
                League Points: {my_ranked_stats[0]['leaguePoints']}
                Wins: {my_ranked_stats[0]['wins']}
                Losses: {my_ranked_stats[0]['losses']}
                Total Games: {total_games}
                Win Rate: {winrate}%
                """)
        except HTTPError:
            messagebox.showerror(title='Error!', message='Summoner selected region is invalid.')
        except IndexError:
            messagebox.showerror(title='Error!', message="Summoner selected region is invalid.")
        except KeyError:
            messagebox.showerror(title='Error!', message="Summoner selected region is invalid.")
        except UnicodeEncodeError:
            messagebox.showerror(title="Error!", message="Bad encoding.. Try with other Summoner.")

    def limpiarHist(self):
        y = messagebox.askyesno(title='Atention!', message='Are you sure you want to delete the search history?')
        if y:
            try:
                os.remove('summoners.txt')
            except FileNotFoundError:
                print("File Not Found")
            else:
                self.listbox.delete(0, END)
                messagebox.showinfo(title="Info", message="Search history deleted succesfully")
                self.on_closing4()

    def view_opgg(self):
        curItem = self.my_tree.focus()
        if curItem:
            item = self.my_tree.item(curItem)
            if self.combo.get() == 'EUW1':
                region = 'euw'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'NA1':
                region = 'na'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'BR1':
                region = 'br'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'JP1':
                region = 'jp'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'EUN1':
                region = 'eune'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'KR':
                region = 'kr'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'LA1':
                region = 'lan'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'LA2':
                region = 'las'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'OC1':
                region = 'oce'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'TR1':
                region = 'tr'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
            elif self.combo.get() == 'RU':
                region = 'ru'
                webbrowser.open(f'https://{region}.op.gg/summoners/{region}/{item["values"][0]}')
        else:
            messagebox.showwarning(title="Atention!", message="You must select an element.")


if __name__ == "__main__":
    LI = LoLInterface()
