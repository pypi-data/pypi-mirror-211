#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 18:18:43 2021

@author: adonay
"""
import os
import os.path as op
import threading
import pandas as pd
from datetime import datetime
import time
import re
import queue
import PySimpleGUIQt as sg
from PySide2.QtWidgets import QHeaderView

from DiscordAlertsTrader.brokerages import get_brokerage
from DiscordAlertsTrader import gui_generator as gg
from DiscordAlertsTrader import gui_layouts as gl
from DiscordAlertsTrader.discord_bot import DiscordBot
from DiscordAlertsTrader.configurator import cfg, channel_ids

def match_authors(author_str:str)->str:
    """Author have an identifier in discord, it will try to find full author name

    Parameters
    ----------
    author_str : str
        string to match the author

    Returns
    -------
    str
        author with identifier
    """
    if "#" in author_str:
        return author_str
    authors = []
    for chn in channel_ids.keys():
        at = pd.read_csv(op.join(cfg['general']['data_dir'] , f"{chn}_message_history.csv"))["Author"].unique()
        authors.extend(at)
    authors = list(dict.fromkeys(authors))
    authors = [a for a in authors if author_str.lower() in a.lower()]
    if len(authors) == 0:
        author = f"{author_str}#No match, find author identifier#1234"
    elif len(authors) > 1:
        author = f"{author_str}#Multiple matches, find author identifier#1234"
    else:
        author = authors[0]
    return author

def fit_table_elms(Widget_element):
    Widget_element.resizeRowsToContents()
    Widget_element.resizeColumnsToContents()
    Widget_element.resizeRowsToContents()
    Widget_element.resizeColumnsToContents()

# sg.theme('Dark Blue 3')
sg.SetOptions(font=("Helvitica 10"))
                # element_padding=(0, 0), margins=(1, 1))

fnt_b = "Arial 10"
fnt_h = "Arial 10"

ly_cons, MLINE_KEY = gl.layout_console()

def mprint(*args, **kwargs):
    window[MLINE_KEY].print(*args, **kwargs)

print(1)
gui_data = {}
gui_data['port'] = gg.get_portf_data()
ly_port = gl.layout_portfolio(gui_data['port'], fnt_b, fnt_h)

gui_data['trades'] = gg.get_tracker_data()
ly_track = gl.layout_traders(gui_data['trades'], fnt_b, fnt_h)

gui_data['stats'] = gg.get_stats_data()
ly_stats = gl.layout_stats(gui_data['stats'], fnt_b, fnt_h)
print(2)

chns = channel_ids.keys()
ly_chns = []
for chn in chns:
    chn_fname = cfg['general']['data_dir']+f"/{chn}_message_history.csv"
    if not op.exists(chn_fname):
        os.makedirs(cfg['general']['data_dir'], exist_ok=True)
        pd.DataFrame(columns=cfg["col_names"]['chan_hist'].split(',')).to_csv(chn_fname, index=False)
    gui_data[chn] = gg.get_hist_msgs(chan_name=chn)
    ly_ch = gl.layout_chan_msg(chn, gui_data[chn], fnt_b, fnt_h)
    ly_chns.append(ly_ch)

bksession = get_brokerage()
ly_accnt = gl.layout_account(bksession, fnt_b, fnt_h)

layout = [[sg.TabGroup([
                        [sg.Tab("Console", ly_cons, font=fnt_b)],
                        [sg.Tab('Portfolio', ly_port)],
                        [sg.Tab('Analysts portfolio', ly_track)],
                        [sg.Tab('Analysts stats', ly_stats)],
                        [sg.Tab(c, h) for c, h in zip(chns, ly_chns)],                        
                        [sg.Tab("Account", ly_accnt)]
                        ], title_color='black')],
          [sg.Input(default_text="Author#1234, STC 1 AAA 115C 05/30 @2.5 [click portfolio row number to prefill]",
                    size= (110,1.5), key="-subm-msg",
                    tooltip="Click portfolio row number to prefill the STC alert"),
           sg.Button("Trigger alert", key="-subm-alert", tooltip="Will generate alert in portfolio and tracker", size= (20,1))]
        ]
print(3)
window = sg.Window('Discord Alerts Trader for BullTrades', layout,size=(100, 800), # force_toplevel=True,
                    auto_size_text=True, resizable=True)
print(4)
def mprint_queue(queue_item_list):
    # queue_item_list = [string, text_color, background_color]
    kwargs = {}
    text = queue_item_list[0]
    len_que = len(queue_item_list)
    if len_que == 2:
        kwargs["text_color"] = queue_item_list[1]
    elif len_que == 3:
        tcol = queue_item_list[1]
        tcol = "black" if tcol == "" else tcol
        kwargs["text_color"] = tcol

        bcol = queue_item_list[2]
        bcol = "white" if bcol == "" else bcol
        kwargs["background_color"] = bcol

    window[MLINE_KEY].print(text, **kwargs)

def update_portfolios_thread(window):
    while True:
        time.sleep(60)
        window["_upd-portfolio_"].click()
        time.sleep(2)  
        window["_upd-track_"].click()
print(5)
event, values = window.read(.1)

els = ['_portfolio_', '_track_', ] + [f"{chn}_table" for chn in chns]
els = els + ['_orders_', '_positions_'] if bksession is not None else els
for el in els:
    try:
        fit_table_elms(window.Element(el).Widget)
    except:
        pass

for chn in chns:
    table = window[f"{chn}_table"].Widget.horizontalHeader()
    table.setSectionResizeMode(2, QHeaderView.Stretch)
    window[f"{chn}_table"].Widget.scrollToBottom()

print(6)
event, values = window.read(.1)
print(7)
trade_events = queue.Queue(maxsize=20)
alistner = DiscordBot(trade_events, brokerage=bksession)
print(8)
threading.Thread(target=update_portfolios_thread, args=(window,), daemon=True).start()
print(9)
event, values = window.read(.1)

# exclusion filters for the portfolio and analysts tabs
port_exc = {"Closed":False,
            "Open":False,
            "NegPnL":False,
            "PosPnL":False,
            "live PnL":False,
            "stocks":True,
            "options":False,
            }
track_exc = port_exc.copy()
stat_exc = port_exc.copy()
port_exc["Cancelled"] = True

print(10)
dt, _  = gg.get_tracker_data(track_exc, **values)
window.Element('_track_').Update(values=dt)
fit_table_elms(window.Element("_track_").Widget)
dt, hdr = gg.get_portf_data(port_exc)
window.Element('_portfolio_').Update(values=dt)
fit_table_elms(window.Element("_portfolio_").Widget)
dt, hdr = gg.get_stats_data(port_exc)
window.Element('_stat_').Update(values=dt)
fit_table_elms(window.Element("_stat_").Widget)

def run_gui():  
    while True:    
        event, values = window.read(1)#.1)

        if event == sg.WINDOW_CLOSED:
            break
        if '_portfolio_' in event and values['_portfolio_'] != []:
            pix = values['_portfolio_'][0]
            dt, hdr = gg.get_portf_data(port_exc, **values)
            symb = dt[pix][hdr.index('Symbol')]
            auth = match_authors(dt[pix][hdr.index('Trader')])
            qty = dt[pix][hdr.index('filledQty')]
            price = dt[pix][hdr.index('1-$-Current')]
            if "_" in symb:
                # option
                exp = r"(\w+)_(\d{6})([CP])([\d.]+)"        
                match = re.search(exp, symb, re.IGNORECASE)
                if match:
                    symbol, date, type, strike = match.groups()
                    symb_str = f"{auth}, STC {qty} {symbol} {strike}{type} {date[:2]}/{date[2:4]} @{price}"
            else:
                symb_str= f"{auth}, STC {qty} {symb} @{price}"
            window.Element("-subm-msg").Update(value=symb_str)
            
        if event == "_upd-portfolio_": # update button in portfolio
            ori_col = window.Element("_upd-portfolio_").ButtonColor
            window.Element("_upd-portfolio_").Update(button_color=("black", "white"))
            event, values = window.read(.1)
            dt, _ = gg.get_portf_data(port_exc, **values)
            window.Element('_portfolio_').Update(values=dt)
            fit_table_elms(window.Element("_portfolio_").Widget)
            window.Element("_upd-portfolio_").Update(button_color=ori_col)

        elif event == "_upd-track_": # update button in analyst alerts
            ori_col = window.Element(f'_upd-track_').ButtonColor
            window.Element("_upd-track_").Update(button_color=("black", "white"))
            event, values = window.read(.1)
            dt, _  = gg.get_tracker_data(track_exc, **values)
            window.Element('_track_').Update(values=dt)
            fit_table_elms(window.Element("_track_").Widget)
            window.Element("_upd-track_").Update(button_color=ori_col)

        elif event == "_upd-stat_": # update button in analyst stats
            ori_col = window.Element(f'_upd-stat_').ButtonColor
            window.Element("_upd-stat_").Update(button_color=("black", "white"))
            event, values = window.read(.1)
            dt, _  = gg.get_stats_data(stat_exc, **values)
            window.Element('_stat_').Update(values=dt)
            fit_table_elms(window.Element("_stat_").Widget)
            window.Element("_upd-stat_").Update(button_color=ori_col)

        elif event.startswith("-port-"): # radial click, update portfolio
            key =  event.replace("-port-", "")
            state = window.Element(event).get()
            port_exc[key] = state
            dt, _ = gg.get_portf_data(port_exc, **values)
            window.Element('_portfolio_').Update(values=dt)

        elif event.startswith("-track-"): # radial click, update analyst alerts
            key =  event.replace("-track-", "")
            state = window.Element(event).get()
            track_exc[key] = state
            dt, _ = gg.get_tracker_data(track_exc, **values)
            window.Element('_track_').Update(values=dt)

        elif event.startswith("-stat-"): # radial click, update analyst stats
            key =  event.replace("-stat-", "")
            state = window.Element(event).get()
            stat_exc[key] = state
            dt, _ = gg.get_stats_data(stat_exc, **values)
            window.Element('_stat_').Update(values=dt)

        elif event[-3:] == "UPD":
            chn = event[:-4]
            ori_col = window.Element(f'{chn}_UPD').ButtonColor
            window.Element(f'{chn}_UPD').Update(button_color=("black", "white"))
            event, values = window.read(.1)

            args = {}
            for k, v in values.items():
                if k[:len(chn)] == chn:
                    args[k[len(chn)+1:]] = v
            dt, _  = gg.get_hist_msgs(chan_name=chn, **args)
            if args['n_rows'] != "":
                n_rows = eval(args['n_rows'])
                n_rows = max(1, n_rows)
                window.Element(f"{chn}_table").Update(values=dt,  num_rows=n_rows)
            else:
                window.Element(f"{chn}_table").Update(values=dt)

            fit_table_elms(window.Element(f"{chn}_table").Widget)
            window.Element(f'{chn}_UPD').Update(button_color=ori_col)

        elif event == 'acc_updt':
            ori_col = window.Element("acc_updt").ButtonColor
            window.Element("acc_updt").Update(button_color=("black", "white"))
            event, values = window.read(.1)
            gl.update_acct_ly(bksession, window)
            fit_table_elms(window.Element(f"_positions_").Widget)
            fit_table_elms(window.Element(f"_orders_").Widget)
            window.Element("acc_updt").Update(button_color=ori_col)

        elif event == "-subm-alert":
            ori_col = window.Element("-subm-alert").ButtonColor
            window.Element("-subm-alert").Update(button_color=("black", "white"))
            event, values = window.read(.1)
            try:        
                author, msg = values['-subm-msg'].split(',')
            except ValueError:
                author, msg = values['-subm-msg'].split(':')
            author = match_authors(author.strip())
            msg = msg.strip()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            new_msg = pd.Series({
                'AuthorID': None,
                'Author': author,
                'Date': date, 
                'Content': msg,
                'Channel': "GUI_input"
                })
            alistner.new_msg_acts(new_msg, from_disc=False)
            window.Element("-subm-alert").Update(button_color=ori_col)

        try:
            event_feedb = trade_events.get(False)
            mprint_queue(event_feedb)
        except queue.Empty:
            pass



def run_client():
    alistner.run(cfg['discord']['discord_token'])


def gui():   
    client_thread = threading.Thread(target=run_client)

    # start the threads
    client_thread.start()
    run_gui()

    # close the GUI window
    window.close()
    alistner.close_bot()
    exit()


if __name__ == '__main__':
    gui()
