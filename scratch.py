import tkinter as tk
from tkinter import ttk
import pandas as pd
import datetime
import os
import webbrowser
import tkinter.messagebox as messagebox
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from pycoingecko import CoinGeckoAPI
import time
from lxml import etree

print("Loading Crypto Nova...")


def on_enter(button):
    button.config(bg="#2d2d2d")


def on_leave(button):
    button.config(bg="#1f262d")


if not os.path.exists("Coins"):
    os.mkdir("Coins")
if not os.path.exists("Tax_Updater"):
    os.mkdir("Tax_Updater")
if not os.path.exists("Board_Sheet"):
    os.mkdir("Board_Sheet")


def update_coins():

    if os.path.exists(f"Coins/Wallet/wallet.csv"):
        wallet = pd.read_csv(f"Coins/Wallet/wallet.csv")
    else:
        print("File Not Found: One or more required files are missing!")
        return


    if os.path.exists(f"Coins/coin_tracker.csv"):
        # ---------------Get new colmun names
        columns = ["DATE"] + wallet.columns.tolist()
        tracker = pd.DataFrame(columns=columns)
        print(tracker)
        # ---------------Get old data
        oldtracker = pd.read_csv(f"Coins/coin_tracker.csv")
        data = oldtracker.values.tolist()
        print(data)
        # ---------------Get NEW data
        wallet_data = wallet.values.tolist()
        print(wallet_data)

        today = datetime.datetime.now().strftime("%d-%m-%Y")

        to_df = [today] + wallet_data[0]
        print(to_df)

        new_data = data + [to_df]
        new_tracker = pd.DataFrame(new_data, columns=columns)
        print(new_tracker)
        new_tracker = new_tracker.fillna(0.0)

        new_tracker.to_csv(f"Coins/coin_tracker.csv", index= False)
        merge_mods()
    else:
        columns = ["DATE"] + wallet.columns.tolist()
        tracker = pd.DataFrame(columns=columns)
        print(tracker)

        wallet_data = wallet.values.tolist()
        print(wallet_data)

        today = datetime.datetime.now().strftime("%d-%m-%Y")

        to_df = [today] + wallet_data[0]
        print(to_df)

        new_tracker = pd.DataFrame(to_df, columns=columns)
        print(new_tracker)
        new_tracker = new_tracker.fillna(0.0)

        new_tracker.to_csv(f"Coins/coin_tracker.csv", index=False)
        merge_mods()


def viewcoins():
    if os.path.exists(f"Coins/Wallet/wallet.csv") and os.path.exists(f"Coins/merged_v.csv"):
        wallet_window = tk.Toplevel(window)
        wallet_window.title("Wallet Tracker")
        wallet_window.configure(bg="#1a1c1f")

        merge_mods()

        df_wallet = pd.read_csv(f"Coins/Wallet/wallet.csv")
        df_all_values = pd.read_csv(f"Coins/merged_v.csv")
        maxeur = df_all_values["true_eur"].sum()
        column_names = df_wallet.columns.tolist()
        first_row_values = df_wallet.iloc[0].tolist()
        true_eur_values = df_all_values["true_eur"].tolist()


        print(maxeur)

        for i, column in enumerate(column_names):
            label_column = tk.Label(wallet_window, text=column, bg="#1a1c1f", fg="white")
            label_value = tk.Label(wallet_window, text="{:.6f}".format(first_row_values[i]), bg="#1a1c1f", fg="white")
            label_true_eur = tk.Label(wallet_window, text=true_eur_values[i], bg="#1a1c1f", fg="white")
            label_column.grid(row=i, column=0, padx=10, pady=5)
            label_value.grid(row=i, column=1, padx=10, pady=5)
            label_true_eur.grid(row=i, column=2, padx=10, pady=5)

            # Center alignment for column names and values
            label_column.config(anchor="center")
            label_value.config(anchor="center")
            label_true_eur.config(anchor="center")







    else:
        messagebox.showerror("Error", "you dont have a WALLET yet")
        return




def add_coin():
    add_window = tk.Toplevel(window)
    add_window.title("Add coin")
    add_window.geometry("300x150")
    add_window.configure(bg="#1a1c1f")
    symbol_label = tk.Label(add_window, text="Coin symbol:", padx=10, pady=10, fg="white", bg="#3c464f", borderwidth=0)
    symbol_label.pack(fill="x")
    symbol_entry = tk.Entry(add_window)
    symbol_entry.pack()
    amount_label = tk.Label(add_window, text="Coin amount:", padx=10, pady=10, fg="white", bg="#3c464f", borderwidth=0)
    amount_label.pack(fill="x")
    amount_entry = tk.Entry(add_window)
    amount_entry.pack()

    def add_to_dataframe():
        if os.path.exists("Coins/Wallet/wallet.csv"):
            dfadd = pd.read_csv("Coins/Wallet/wallet.csv")
            symbol = symbol_entry.get().upper()
            amount = float(amount_entry.get())
            if symbol in dfadd.columns:
                dfadd.at[0, symbol] += amount
            else:
                dfadd[symbol] = 0
                dfadd.at[0, symbol] = amount
            if not os.path.exists("Coins/Wallet"):
                os.makedirs("Coins/Wallet")
            print(dfadd)
            dfadd.to_csv("Coins/Wallet/wallet.csv", index=False)
            update_coins()
            merge_mods()
            add_window.destroy()
        else:
            messagebox.showerror("Error", "You need a Coins/Wallet/wallet.csv in order to do this")
            window.mainloop()
    add_button = tk.Button(add_window, text="Add coin", command=add_to_dataframe, padx=10, pady=5, fg="white",
                           bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    add_button.pack(fill="x")
    add_button.bind("<Enter>", lambda event: on_enter(add_button))
    add_button.bind("<Leave>", lambda event: on_leave(add_button))


def mod():
    if os.path.exists("Coins/Wallet/wallet.csv"):
        dfcoin = pd.read_csv("Coins/Wallet/wallet.csv")
        mod_window = tk.Toplevel(window)
        mod_window.title("Modify wallet")
        mod_window.configure(bg="#1a1c1f")

        def save_modifications():
            updated_data = {}

            # Iterate over the entry boxes
            for i, column in enumerate(column_names):
                entry_widget = mod_window.grid_slaves(row=i, column=1)[0]
                value = entry_widget.get()
                updated_data[column] = value


            for column, value in updated_data.items():
                dfcoin[column] = value

            print(dfcoin)
            dfcoin.to_csv("Coins/Wallet/wallet.csv", index=False)
            update_coins()
            print("Wallet.csv updated!")
            messagebox.showinfo("Updated Wallet Values", "Your virtual Wallet has been updated")

        column_names = dfcoin.columns

        for i, column in enumerate(column_names):
            label = tk.Label(mod_window, text=column, bg="#1a1c1f", fg="white")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            value_entry = tk.Entry(mod_window, bg="white")
            value_entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")

            initial_value = str(dfcoin[column].values[0])
            value_entry.insert(tk.END, initial_value)

        mod_window.grid_rowconfigure(i, weight=1)
        mod_window.grid_columnconfigure(1, weight=1)

        save_button = tk.Button(mod_window, text="Save", command=save_modifications,
                                padx=10, pady=5, fg="white", bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
        save_button.grid(row=i + 1, column=0, columnspan=2, padx=10, pady=10)
        save_button.bind("<Enter>", lambda event: on_enter(save_button))
        save_button.bind("<Leave>", lambda event: on_leave(save_button))


        mod_window.update()
        screen_width = mod_window.winfo_screenwidth()
        screen_height = mod_window.winfo_screenheight()
        window_width = mod_window.winfo_width()
        window_height = mod_window.winfo_height()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        mod_window.geometry(f"+{x}+{y}")
    else:
        messagebox.showerror("Error", "You have no coins yet, you need to -Start From Scratch-")
        return






    # if os.path.exists("Coins/Wallet/wallet.csv"):
    #     dfcoin = pd.read_csv("Coins/Wallet/wallet.csv")
    #     mod_window = tk.Toplevel(window)
    #     mod_window.title("Modify wallet")
    #     mod_window.geometry("700x200")
    #     mod_window.configure(bg="#1a1c1f")
    #     text = tk.Text(mod_window, height=10)
    #     text.pack()
    #     text.insert(tk.END, str(dfcoin))
    #
    #     def save_modifications():
    #         modified_df = pd.read_csv(io.StringIO(text.get("1.0", tk.END)))
    #         modified_df.to_csv("Coins/Wallet/wallet.csv", index=False)
    #         update_coins()
    #         make_wallet_mod()
    #         mod_window.destroy()
    #     save_button = tk.Button(mod_window, text="Save modifications", command=save_modifications,
    #                             padx=10, pady=5, fg="white", bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    #     save_button.pack(fill="x")
    #     save_button.bind("<Enter>", lambda event: on_enter(save_button))
    #     save_button.bind("<Leave>", lambda event: on_leave(save_button))


def sfs():
    sfs_window = tk.Toplevel(window)
    sfs_window.title("Start From Scratch")
    sfs_window.geometry("500x175")
    sfs_window.configure(bg="#1f262d")
    symbol_label = tk.Label(sfs_window, text="Symbol", padx=10, pady=10, fg="white", bg="#3c464f", borderwidth=0)
    symbol_label.pack(fill="x")
    symbol_entry = tk.Entry(sfs_window)
    symbol_entry.pack()
    amount_label = tk.Label(sfs_window, text="Amount", padx=10, pady=10, fg="white", bg="#3c464f", borderwidth=0)
    amount_label.pack(fill="x")
    amount_entry = tk.Entry(sfs_window)
    amount_entry.pack()

    def add_to_dataframe():
        symbol = symbol_entry.get().upper()
        amount = float(amount_entry.get())
        df[symbol] = [amount]
        print(df)
        symbol_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
    add_button = tk.Button(sfs_window, text="Add to dataframe", command=add_to_dataframe, padx=10, pady=5, fg="white",
                           bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    add_button.pack(fill="x")
    add_button.bind("<Enter>", lambda event: on_enter(add_button))
    add_button.bind("<Leave>", lambda event: on_leave(add_button))
    df = pd.DataFrame()

    def print_dataframe():
        df_window = tk.Toplevel(sfs_window)
        df_window.title("Dataframe")
        df_text = tk.Text(df_window)
        df_text.pack()
        df_str = df.to_string()
        df_text.insert(tk.END, df_str)

        def save_dataframe():
            os.makedirs("Coins/Wallet", exist_ok=True)
            df.to_csv("Coins/Wallet/wallet.csv", index=False)
            update_coins()
            tax()
            df_window.destroy()
        save_button = tk.Button(df_window, text="Save to CSV", command=save_dataframe, padx=10, pady=5, fg="white",
                                bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
        save_button.pack(fill="x")
        save_button.bind("<Enter>", lambda event: on_enter(save_button))
        save_button.bind("<Leave>", lambda event: on_leave(save_button))
    display_button = tk.Button(sfs_window, text="Display dataframe", command=print_dataframe, padx=10, pady=5,
                               fg="white", bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    display_button.pack(fill="x")
    display_button.bind("<Enter>", lambda event: on_enter(display_button))
    display_button.bind("<Leave>", lambda event: on_leave(display_button))
    sfs_window.mainloop()


def pure():
    pure_window = tk.Toplevel(window)
    pure_window.title("Pure Coins")
    pure_window_width = 300
    pure_window_height = 250

    pure_window_x = x + window_width
    pure_window_y = y - pure_window_height-29

    pure_window.geometry(f"{pure_window_width}x{pure_window_height}+{pure_window_x}+{pure_window_y}")


    pure_window.configure(bg="#1a1c1f")
    modify_button = tk.Button(pure_window, text="Modify", command=mod, padx=10, pady=5, fg="white", bg="#1f262d",
                              font=("Arial", 12, "bold"), borderwidth=0)
    add_button = tk.Button(pure_window, text="Add", command=add_coin, padx=10, pady=5, fg="white", bg="#1f262d",
                           font=("Arial", 12, "bold"), borderwidth=0)
    view_table_button = tk.Button(pure_window, text="View Table", command=viewcoins, padx=10, pady=5, fg="white",
                                  bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    scratch_button = tk.Button(pure_window, text="Start from scratch (CAUTION!)", command=sfs, padx=10, pady=5,
                               fg="white", bg="#eb4034", font=("Arial", 12, "bold"), borderwidth=0)
    modify_button.pack(fill="x", pady=(30, 0))
    add_button.pack(fill="x", pady=(10, 0))
    view_table_button.pack(fill="x", pady=(10, 0))
    scratch_button.pack(fill="x", pady=(10, 0))
    modify_button.bind("<Enter>", lambda event: on_enter(modify_button))
    modify_button.bind("<Leave>", lambda event: on_leave(modify_button))
    add_button.bind("<Enter>", lambda event: on_enter(add_button))
    add_button.bind("<Leave>", lambda event: on_leave(add_button))
    view_table_button.bind("<Enter>", lambda event: on_enter(view_table_button))
    view_table_button.bind("<Leave>", lambda event: on_leave(view_table_button))


def make_wallet_mod1():
    if os.path.exists(f"Coins/Wallet/wallet.csv"):
        cg = CoinGeckoAPI()
        print("//////// CoinGeckoAPI - is running ...")
        df = pd.read_csv("Coins/Wallet/wallet.csv", header=None)
        df_transposed = df.transpose()
        df_transposed.columns = ['Crypto', 'Amount']
        df_transposed['Crypto'] = df_transposed['Crypto'].str.lower()
        df_transposed.to_csv("Coins/Wallet/wallet_mod.csv", index=False)
        fuu = pd.read_csv("Coins/Wallet/wallet_mod.csv")
        fuu['value_usd'] = None
        fuu['value_eur'] = None

        def update_progress_bar(progress):
            progress_var.set(progress)
        progress_window = tk.Toplevel()
        progress_window.title("Progress")
        progress_window_width = 300
        progress_window_height = 100

        progress_window_x = x + 50
        progress_window_y = y - progress_window_height-29

        progress_window.geometry(
            f"{progress_window_width}x{progress_window_height}+{progress_window_x}+{progress_window_y}")

        progress_window.configure(bg="#1a1c1f")
        progress_label = tk.Label(progress_window, text="Updating coin values...", padx=10, pady=5, fg="white",
                                  bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
        progress_label.pack(pady=10)
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=len(fuu), length=300)
        progress_bar.pack(padx=20, pady=10)

        for index, row in fuu.iterrows():
            coin = row['Crypto']
            try:
                data = cg.get_price(ids=coin, vs_currencies=['USD', 'EUR'])
                usd_value = data[coin]['usd']
                eur_value = data[coin]['eur']

                fuu.at[index, 'value_usd'] = usd_value
                fuu.at[index, 'value_eur'] = eur_value
            except Exception as e:
                print(f"Error: {coin} not found on CoinGecko API")
                continue
            update_progress_bar(index+1)
            progress_window.update()
        fuu['true_usd'] = fuu['Amount'] * fuu['value_usd']
        fuu['true_eur'] = fuu['Amount'] * fuu['value_eur']
        fuu.to_csv("Coins/all_valuescg.csv")
        progress_window.destroy()
    else:
        messagebox.showerror("File not found", "You need a Coins/Wallet/wallet.csv in orther to calculate this")
        window.mainloop()


def make_wallet_mod():
    if os.path.exists(f"Coins/Wallet/wallet.csv"):
        df = pd.read_csv("Coins/Wallet/wallet.csv", header=None)
        df_transposed = df.transpose()
        df_transposed.columns = ['Crypto', 'Amount']
        df_transposed['Crypto'] = df_transposed['Crypto'].str.upper()
        df_transposed.to_csv("Coins/Wallet/wallet_mod.csv", index=False)
        fuu = pd.read_csv(f"Coins/Wallet/wallet_mod.csv")
        fuu['value_usd'] = None
        fuu['value_eur'] = None

        def update_progress_bar(progress):
            progress_var.set(progress)
        progress_window = tk.Toplevel()
        progress_window.title("Progress")
        progress_window_width = 300
        progress_window_height = 100

        progress_window_x = x + 50
        progress_window_y = y - progress_window_height - 29

        progress_window.geometry(
            f"{progress_window_width}x{progress_window_height}+{progress_window_x}+{progress_window_y}")
        progress_window.configure(bg="#1a1c1f")
        progress_label = tk.Label(progress_window, text="Updating coin values...", padx=10, pady=5, fg="white",
                                  bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
        progress_label.pack(pady=10)
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=len(fuu), length=300)
        progress_bar.pack(padx=20, pady=10)

        for index, row in fuu.iterrows():
            coin = row['Crypto']
            try:
                print("//////// min-api.cryptocompare.com - is running ...")
                response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={coin}&tsyms=USD,EUR')
                response.raise_for_status()
                data = response.json()

                usd_value = data['USD']
                eur_value = data['EUR']
                fuu.at[index, 'value_usd'] = usd_value
                fuu.at[index, 'value_eur'] = eur_value
            except Exception as e:
                print(f"Error: {coin} not found on CryptoCompare API")
                continue
            update_progress_bar(index+1)
            progress_window.update()
        fuu['true_usd'] = fuu['Amount'] * fuu['value_usd']
        fuu['true_eur'] = fuu['Amount'] * fuu['value_eur']
        fuu.to_csv("Coins/all_valuescc.csv")
        progress_window.destroy()
    else:
        messagebox.showerror("File not found", "You need a Coins/Wallet/wallet.csv in orther to calculate this")
        return


def merge_mods():
    if os.path.exists(f"Coins/Wallet/wallet.csv"):
        make_wallet_mod()
        make_wallet_mod1()
        df_cc = pd.read_csv("Coins/all_valuescc.csv")
        df_cg = pd.read_csv("Coins/all_valuescg.csv")
        df_cg.fillna(df_cc, inplace=True)
        merged_df = df_cg.to_csv("Coins/all_values.csv", index=False)
        merged_df = df_cg.to_csv("Coins/merged_v.csv", index=False)
        print(merged_df)
        return merged_df
    else:
        messagebox.showerror("File not found", "You need a Coins/Wallet/wallet.csv in orther to calculate this")
        return




def liquid():
    liquid_window = tk.Toplevel(window)
    liquid_window.title("Coins in Liquid State")
    liquid_window_width = 300
    liquid_window_height = 220
    liquid_window_x = x + window_width
    liquid_window_y = y + 200
    liquid_window.geometry(f"{liquid_window_width}x{liquid_window_height}+{liquid_window_x}+{liquid_window_y}")
    liquid_window.configure(bg="#1a1c1f")
    usd_label = tk.Label(liquid_window, text="Enter value in USD:", padx=10, pady=20, fg="white",
                         bg="#3c464f", borderwidth=0)
    usd_label.pack(fill="x", pady=(20, 0))
    usd_entry = tk.Entry(liquid_window)
    usd_entry.pack(pady=(10, 0))
    df = pd.DataFrame(columns=['USD'])

    def add_usd():
        value_str = usd_entry.get()
        if "+" in value_str:
            values = value_str.split("+")
            value = sum([float(v.strip()) for v in values])
        else:
            value = float(value_str.strip())
        df.loc[len(df)] = [value]
        print(df)
        usd_entry.delete(0, 'end')
        file_path = os.path.join('Coins', 'liquid_value.csv')
        print("liquid_value.csv was saved")
        df.to_csv(file_path, index=False)
    add_button = tk.Button(liquid_window, text="Add USD", command=add_usd, padx=10, pady=5, fg="white", bg="#1f262d",
                           font=("Arial", 12, "bold"), borderwidth=0)
    add_button.pack(fill="x", pady=(10, 0))
    add_button.bind("<Enter>", lambda event: on_enter(add_button))
    add_button.bind("<Leave>", lambda event: on_leave(add_button))
    done_button = tk.Button(liquid_window, text="Done", command=liquid_window.destroy, padx=10, pady=5, fg="white",
                            bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    done_button.pack(fill="x", pady=(10, 0))
    done_button.bind("<Enter>", lambda event: on_enter(done_button))
    done_button.bind("<Leave>", lambda event: on_leave(done_button))
    usd_entry.bind('<Return>', lambda event: add_usd())
    liquid_window.wait_window(liquid_window)
    return True


def open_coins_window():
    coins_window = tk.Toplevel(window)
    coins_window.title("Coins")
    global coins_window_width
    coins_window_width = 300
    coins_window_height = 150
    coins_window_x = x + window_width
    coins_window_y = y
    coins_window.geometry(f"{coins_window_width}x{coins_window_height}+{coins_window_x}+{coins_window_y}")
    coins_window.configure(bg="#1a1c1f")
    coins_button1 = tk.Button(coins_window, text="Pure Coins", command=pure, padx=10, pady=5, fg="white",
                              bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    coins_button3 = tk.Button(coins_window, text="Liquid State", command=liquid, padx=10, pady=5, fg="white",
                              bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    coins_button1.pack(fill="x", pady=(30, 0))
    coins_button3.pack(fill="x", pady=(10, 0))
    coins_button1.bind("<Enter>", lambda event: on_enter(coins_button1))
    coins_button1.bind("<Leave>", lambda event: on_leave(coins_button1))
    coins_button3.bind("<Enter>", lambda event: on_enter(coins_button3))
    coins_button3.bind("<Leave>", lambda event: on_leave(coins_button3))


def tax():
    if not os.path.exists(f"Tax_Updater/Default_tax.csv"):
        columns = ["DATE", "Amount Spent", "On Tax Amount", "Total Amount Spent (A)", "Total On Tax amount (B)", "Use",
                   "A+Use", "A-Use", "B+Use", "B-Use", "Total Use"]
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.read_csv(f"Tax_Updater/Default_tax.csv")

    def add_use():
        date1 = datetime.datetime.now().strftime("%d-%m-%Y")
        spent1 = 0
        on_tax1 = 0
        print(date1)
        print(spent1)
        print(on_tax1)

        a_total1 = float(df["Amount Spent"].sum()) + spent1
        print(a_total1)

        b_total1 = float(df["On Tax Amount"].sum()) + on_tax1
        print(b_total1)

        use1 = float(use_entry.get())

        print(use1)
        usetotal1 = float(df["Use"].sum()) + use1
        print(usetotal1)

        target1 = float(df["A+Use"].iloc[-1])
        print(target1)
        target2 = float(df["A-Use"].iloc[-1])
        print(target2)

        ap_use1 = target1 + use1
        print(ap_use1)
        ad_use1 = target2 - use1
        print(ad_use1)

        target3 = float(df["B+Use"].iloc[-1])
        target4 = float(df["B-Use"].iloc[-1])

        bp_use1 = target3 + use1
        bd_use1 = target4 - use1

        new_row = [date1, spent1, on_tax1, a_total1, b_total1, use1, ap_use1, ad_use1, bp_use1, bd_use1, usetotal1]
        df.loc[len(df)] = new_row
        print(df)
        update_table()

    def add_amounts():
        spent = float(spent_entry.get())
        on_tax = float(amount_spent_entry.get())
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        a_total = float(df["Amount Spent"].sum()) + spent
        b_total = float(df["On Tax Amount"].sum()) + on_tax
        use = 0
        ap_use = float(df["A+Use"].iloc[-1])
        ad_use = float(df["A-Use"].iloc[-1])
        bp_use = float(df["B+Use"].iloc[-1])
        bd_use = float(df["B-Use"].iloc[-1])
        usetotal = df["Use"].sum()
        new_row = [date, spent, on_tax, a_total, b_total, use, ap_use, ad_use, bp_use, bd_use, usetotal]
        df.loc[len(df)] = new_row
        print(df)
        update_table()

    def update_table():
        table.delete(*table.get_children())
        for i, row in df.iterrows():
            table.insert('', 'end', values=list(row))
    taxx_window = tk.Toplevel(window)
    taxx_window.title("Tax List")
    taxx_window.geometry("1550x600")
    taxx_window.configure(bg="#1a1c1f")
    table_height = int(taxx_window.winfo_height()/2)
    table = ttk.Treeview(taxx_window, columns=list(df.columns), show='headings', height=table_height)
    for col in df.columns:
        table.heading(col, text=col)
        table.column(col, width=int(1400/len(df.columns)))
    for i, row in df.iterrows():
        table.insert('', 'end', values=list(row))
    scrollbar = ttk.Scrollbar(taxx_window, orient=tk.VERTICAL, command=table.yview)
    scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
    table.configure(yscrollcommand=scrollbar.set)
    table.place(relx=0, rely=0, relwidth=1, relheight=0.5)
    spent_label = tk.Label(taxx_window, text="Amount Spent:", padx=10, pady=20, fg="white",
                           bg="#3c464f", borderwidth=0)
    spent_label.place(relx=0.1, rely=0.5, anchor=tk.NW)
    spent_entry = tk.Entry(taxx_window)
    spent_entry.place(relx=0.2, rely=0.5, anchor=tk.NW)
    amount_spent_label = tk.Label(taxx_window, text="On Tax Amount:", padx=10, pady=20, fg="white",
                                  bg="#3c464f", borderwidth=0)
    amount_spent_label.place(relx=0.1, rely=0.6, anchor=tk.NW)
    amount_spent_entry = tk.Entry(taxx_window)
    amount_spent_entry.place(relx=0.2, rely=0.6, anchor=tk.NW)
    use_label = tk.Label(taxx_window, text="Use:", padx=10, pady=20, fg="white", bg="#3c464f", borderwidth=0)
    use_label.place(relx=0.7, rely=0.5, anchor=tk.NW)
    use_entry = tk.Entry(taxx_window)
    use_entry.place(relx=0.8, rely=0.5, anchor=tk.NW)

    def saveb():
        df.to_csv(f"Tax_Updater/Default_tax.csv", index=False)
        if os.path.exists(f"Tax_Updater/Default_tax.csv"):
            messagebox.showinfo("Tax Values saved!", "Your Tax values were saved with success!")
            board_sheet()
        else:
            messagebox.showerror("Save ERROR 404?", "Sorry, something went wrong... Couldn't save your file...")
            return
    add_amounts_button = tk.Button(taxx_window, text="Add Amounts", font=("TkDefaultFont", 16), command=add_amounts,
                                   padx=10, pady=20, fg="white", bg="#3c464f", borderwidth=0)
    add_amounts_button.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
    add_use_button = tk.Button(taxx_window, text="Add Use", font=("TkDefaultFont", 16), command=add_use,
                               padx=10, pady=20, fg="white", bg="#3c464f", borderwidth=0)
    add_use_button.place(relx=0.8, rely=0.7, anchor=tk.NE)
    save_button = tk.Button(taxx_window, text="Save", font=("TkDefaultFont", 16), command=saveb, padx=10,
                            pady=10, fg="white", bg="#3c464f", borderwidth=0)
    save_button.place(relx=0.5, rely=1, anchor=tk.S)
    add_amounts_button.bind("<Enter>", lambda event: on_enter(add_amounts_button))
    add_amounts_button.bind("<Leave>", lambda event: on_leave(add_amounts_button))
    add_use_button.bind("<Enter>", lambda event: on_enter(add_use_button))
    add_use_button.bind("<Leave>", lambda event: on_leave(add_use_button))
    save_button.bind("<Enter>", lambda event: on_enter(save_button))
    save_button.bind("<Leave>", lambda event: on_leave(save_button))


def get_exchange_rate():
    search_query = '1 USD to EUR'
    url = f"https://www.google.com/search?q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    global result
    result = soup.find("span", class_="DFlfde SwHCTb")
    if result is None:
        messagebox.showerror("Error", "def get_exchange_rate() is corrupted")
        return
    else:
        global exchange_rate
        exchange_rate = result["data-value"]
        print(exchange_rate)
        return float(exchange_rate)

def board_sheet():
    print("API Values merging...")
    merge_mods()
    response = messagebox.askyesno("Add Liquid value?", "Do you have liquid state assets you want to add?")
    if response == True:
        liquid()
    else:
        pass

    if not os.path.exists(f"Board_Sheet/Prime_sheet.csv"):
        columns1 = ["DATE", "Portófio Value USD", "Portófio Value EUR", "Crypto Cap", "Taxed", "Median Tax Amount",
                    "A+Use", "A-Use", "B+Use", "B-Use", "Change USD 24h", "Change EUR 24h", "Change USD 7D",
                    "Change EUR 7D", "Profit / Loss (€)", "Profit / Loss (%)"]
        print(columns1)
        dfbs = pd.DataFrame(columns=columns1)
        print(dfbs)
        dfbs.to_csv(f"Board_Sheet/Prime_sheet.csv", index=False)
    else:
        dfbs = pd.read_csv(f"Board_Sheet/Prime_sheet.csv")
        print(dfbs)

    if os.path.exists(f'Coins/liquid_value.csv'):
        dfliquid = pd.read_csv(f'Coins/liquid_value.csv')
        print(dfliquid)
        lusd_value = dfliquid.loc[0, "USD"]
        eur_exchange_rate = get_exchange_rate()
        if result is None:
            messagebox.showerror("Code is not working", "Make sure google didn't change the layout of the page "
                                                        "when searching '1 USD to EUR'")
            return
        leur_value = lusd_value * eur_exchange_rate
    else:
        leur_value = 0
        lusd_value = 0

    if os.path.exists(f"Coins/all_values.csv"):
        df1 = pd.read_csv(f"Coins/all_values.csv")
        portusd1 = df1["true_usd"].sum() + lusd_value
        porteur1 = df1["true_eur"].sum() + leur_value
        portusd = float(f"{portusd1:.3f}")
        porteur = float(f"{porteur1:.3f}")
    else:
        messagebox.showerror("File not found!", "Coins/all_values.csv is not yet created")
        return

    if os.path.exists(f"Tax_Updater/Default_tax.csv"):
        df2 = pd.read_csv(f"Tax_Updater/Default_tax.csv")
        taxuse1 = df2["A+Use"].iloc[-1]
        taxuse2 = df2["A-Use"].iloc[-1]
        taxuse3 = df2["B+Use"].iloc[-1]
        taxuse4 = df2["B-Use"].iloc[-1]
        usdfinal = float(portusd)
        eurfinal = float(porteur)
        cryptocap = str(df2["Total Amount Spent (A)"].iloc[-1])
        taxcap = str(df2["Total On Tax amount (B)"].iloc[-1])
        mediantax1 = float((taxuse1 + taxuse2 + taxuse3 + taxuse4) / 4)
        mediantax = f"{mediantax1:.3f}"
        profit = float(porteur) - float(mediantax)
        solid_profit = round(float(profit), 3)
        profitp1 = (float(profit) / float(mediantax)) * 100
        profitp = f"{profitp1:.3f}"
        finalprofitp = str(profitp)
    else:
        messagebox.showerror("File not found!", "Tax_Updater/Default_tax.csv is not yet created")
        return

    if len(dfbs["Portófio Value USD"]) > 0:
        last_valueusd = dfbs["Portófio Value USD"].iloc[-1]
        last_valueusd = float(last_valueusd)
        lastchangeusd = round(float(portusd - last_valueusd), 3)
    else:
        lastchangeusd = 0.000

    if len(dfbs["Portófio Value EUR"]) > 0:
        last_valueeur = dfbs["Portófio Value EUR"].iloc[-1]
        last_valueeur = float(last_valueeur)
        lastchangeeur = round(float(porteur - last_valueeur), 3)
    else:
        lastchangeeur = 0.000

    if len(dfbs["Change USD 24h"]) >= 6:
        last_seven_values = pd.concat([dfbs["Change USD 24h"].tail(6), pd.Series([lastchangeusd])])
        lastchange7usd = round(float(last_seven_values.median()), 3)
    else:
        lastchange7usd = 0.000

    if len(dfbs["Change EUR 24h"]) >= 6:
        last_seven_values1 = pd.concat([dfbs["Change EUR 24h"].tail(6), pd.Series([lastchangeeur])])
        lastchange7eur = round(float(last_seven_values1.median()), 3)
    else:
        lastchange7eur = 0.000

    datebs = datetime.datetime.now().strftime("%d-%m-%Y")
    new_row = [datebs, usdfinal, eurfinal, cryptocap, taxcap, mediantax, taxuse1, taxuse2,
               taxuse3, taxuse4, lastchangeusd, lastchangeeur, lastchange7usd,
               lastchange7eur, solid_profit, finalprofitp]
    print(new_row)

    def display_tables():
        window = tk.Tk()
        window.title("Sheet Cheat")
        tree1 = ttk.Treeview(window, show="headings", height=20)
        tree1["columns"] = list(dfbs.columns)
        for col in dfbs.columns:
            tree1.column(col, anchor="center", width=111)
            tree1.heading(col, text=col, anchor="center")
        for i, row in dfbs.iterrows():
            tree1.insert("", tk.END, text=i, values=list(row))
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree1.yview)
        scrollbar.pack(side="right", fill="y")
        tree1.configure(yscrollcommand=scrollbar.set)
        tree2 = ttk.Treeview(window, show="headings", height=2)
        tree2["columns"] = list(dfbs.columns)
        for col in dfbs.columns:
            tree2.column(col, anchor="center", width=111)
            tree2.heading(col, text=col, anchor="center")
        tree2.insert("", tk.END, text=len(dfbs), values=new_row)

        def save_new_row():
            dfbs.loc[len(dfbs)] = new_row
            dfbs.to_csv("Board_Sheet/Prime_sheet.csv", index=False)
            tree1.insert("", tk.END, text=len(dfbs) - 1, values=new_row)
            empty_row = [""] * len(dfbs.columns)
            tree2.insert("", tk.END, text=len(dfbs), values=empty_row)
            messagebox.showinfo("Saved", "New row saved successfully!")

        save_button = tk.Button(window, text="Save new row", command=save_new_row, padx=10,
                                pady=5, fg="white", bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
        tree1.pack()
        tree2.pack()
        save_button.bind("<Enter>", lambda event: on_enter(save_button))
        save_button.bind("<Leave>", lambda event: on_leave(save_button))
        save_button.pack(fill="x")
        return

    display_tables()


def coing():
    if os.path.exists(f"Coins/coin_tracker.csv"):
        print("Coins/coin_tracker.csv - load success")
        df = pd.read_csv(f"Coins/coin_tracker.csv")
        cg_window = tk.Toplevel(window)
        cg_window.geometry("300x300")
        cg_window.title("Crypto Tracker")
        cg_window.configure(bg="#1a1c1f")
        column_names = list(df.columns)[1:]
        listbox = tk.Listbox(cg_window, selectmode=tk.MULTIPLE)
        for name in column_names:
            listbox.insert(tk.END, name)
        listbox.pack()

        def get_selection():
            selected_items = [listbox.get(i) for i in listbox.curselection()]
            selected_columns = ["DATE"] + selected_items
            selected_data = df[selected_columns]
            print(selected_data.to_string(index=False))
            selected_df = pd.DataFrame(selected_data)
            print(selected_df)
            selected_df.plot(x="DATE")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.title("Crypto Prices Over Time")
            plt.xticks(rotation=90)
            plt.subplots_adjust(bottom=0.24)
            plt.show()
        buttona = tk.Button(cg_window, text="Get Selection", command=get_selection, padx=10, pady=20, fg="white",
                            bg="#3c464f", borderwidth=0)
        buttona.pack(fill="x")
        buttona.bind("<Enter>", lambda event: on_enter(buttona))
        buttona.bind("<Leave>", lambda event: on_leave(buttona))
    else:
        messagebox.showerror("Error", "You dont have a Coins/coin_tracker.csv file")
        window.mainloop()


def true_value_eur():
    if os.path.exists(f"Board_Sheet/Prime_sheet.csv"):
        print("Board_Sheet/Prime_sheet.csv - load success")
        dfprime = pd.read_csv(f"Board_Sheet/Prime_sheet.csv")
        columns_to_plot = ['DATE', 'Portófio Value EUR', 'Median Tax Amount', 'A+Use', 'A-Use', 'B+Use', 'B-Use']
        df_to_plot = dfprime[columns_to_plot]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axhline(0, color='black', linestyle='--')
        ax.plot(df_to_plot['DATE'], df_to_plot['Portófio Value EUR'], label='Portfolio Value EUR')
        ax.plot(df_to_plot['DATE'], df_to_plot['Median Tax Amount'], label='Median Tax Amount')
        ax.plot(df_to_plot['DATE'], df_to_plot['A+Use'], label='A+Use')
        ax.plot(df_to_plot['DATE'], df_to_plot['A-Use'], label='A-Use')
        ax.plot(df_to_plot['DATE'], df_to_plot['B+Use'], label='B+Use')
        ax.plot(df_to_plot['DATE'], df_to_plot['B-Use'], label='B-Use')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.set_title('Portfolio Performance')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.24)
        ax.legend()
        plt.show()
    else:
        messagebox.showerror("Error", "You dont have a Board_Sheet/Prime_sheet.csv")
        window.mainloop()


def true_value_usd():
    if os.path.exists(f"Board_Sheet/Prime_sheet.csv"):
        print("Board_Sheet/Prime_sheet.csv - load success")
        dfprime = pd.read_csv(f"Board_Sheet/Prime_sheet.csv")
        columns_to_plot = ['DATE', 'Portófio Value USD', 'Median Tax Amount', 'A+Use', 'A-Use', 'B+Use', 'B-Use']
        df_to_plot = dfprime[columns_to_plot]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axhline(0, color='black', linestyle='--')
        ax.plot(df_to_plot['DATE'], df_to_plot['Portófio Value USD'], label='Portfolio Value USD')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.set_title('Portfolio Performance')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.24)
        ax.legend()
        plt.show()
    else:
        messagebox.showerror("Error", "You dont have a Board_Sheet/Prime_sheet.csv")
        window.mainloop()


def profit1():
    if os.path.exists(f"Board_Sheet/Prime_sheet.csv"):
        print("Board_Sheet/Prime_sheet.csv - load success")
        dfprime = pd.read_csv(f"Board_Sheet/Prime_sheet.csv")
        columns_to_plot = ["DATE", "Profit / Loss (€)"]
        df_to_plot = dfprime[columns_to_plot]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axhline(0, color='black', linestyle='--')
        ax.plot(df_to_plot['DATE'], df_to_plot['Profit / Loss (€)'], label='Profit / Loss (€)')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.set_title('Portfolio Profit / Loss (€)')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.24)
        ax.legend()
        plt.show()
    else:
        messagebox.showerror("Error", "You dont have a Board_Sheet/Prime_sheet.csv")
        window.mainloop()


def profit2():
    if os.path.exists(f"Board_Sheet/Prime_sheet.csv"):
        print("Board_Sheet/Prime_sheet.csv - load success")
        dfprime = pd.read_csv(f"Board_Sheet/Prime_sheet.csv")
        columns_to_plot = ["DATE", "Profit / Loss (%)"]
        print(columns_to_plot)
        df_to_plot = dfprime[columns_to_plot]
        print(" ")
        print(df_to_plot)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axhline(0, color='black', linestyle='--')
        ax.plot(df_to_plot['DATE'], df_to_plot['Profit / Loss (%)'], label='Profit / Loss (%)')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.set_title('Portfolio Profit / Loss (%)')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.24)
        ax.legend()
        plt.show()
    else:
        messagebox.showerror("Error", "You dont have a Board_Sheet/Prime_sheet.csv")
        window.mainloop()


def changes():
    if os.path.exists(f"Board_Sheet/Prime_sheet.csv"):
        print("Board_Sheet/Prime_sheet.csv - load success")
        dfprime = pd.read_csv(f"Board_Sheet/Prime_sheet.csv")
        columns_to_plot = ["DATE", "Change USD 24h", "Change EUR 24h", "Change USD 7D", "Change EUR 7D"]
        print(columns_to_plot)
        df_to_plot = dfprime[columns_to_plot]
        print(df_to_plot)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axhline(0, color='black', linestyle='--')

        ax.plot(df_to_plot['DATE'], df_to_plot['Change USD 24h'], label='Change USD 24h')
        ax.plot(df_to_plot['DATE'], df_to_plot['Change EUR 24h'], label='Change EUR 24h')
        ax.plot(df_to_plot['DATE'], df_to_plot['Change USD 7D'], label='Change USD 7D')
        ax.plot(df_to_plot['DATE'], df_to_plot['Change EUR 7D'], label='Change EUR 7D')

        ax.fill_between(df_to_plot['DATE'], df_to_plot['Change USD 24h'], 0, where=(df_to_plot['Change USD 24h'] < 0),
                        interpolate=True, color='red', alpha=0.3)
        ax.fill_between(df_to_plot['DATE'], df_to_plot['Change EUR 24h'], 0, where=(df_to_plot['Change EUR 24h'] < 0),
                        interpolate=True, color='red', alpha=0.3)
        ax.fill_between(df_to_plot['DATE'], df_to_plot['Change USD 7D'], 0, where=(df_to_plot['Change USD 7D'] < 0),
                        interpolate=True, color='red', alpha=0.3)
        ax.fill_between(df_to_plot['DATE'], df_to_plot['Change EUR 7D'], 0, where=(df_to_plot['Change EUR 7D'] < 0),
                        interpolate=True, color='red', alpha=0.3)
        ax.fill_between(df_to_plot['DATE'], df_to_plot['Change USD 24h'], 0, where=(df_to_plot['Change USD 24h'] >= 0),
                        interpolate=True, color='green', alpha=0.3)
        ax.fill_between(df_to_plot['DATE'], df_to_plot['Change EUR 24h'], 0, where=(df_to_plot['Change EUR 24h'] >= 0),
                        interpolate=True, color='green', alpha=0.3)
        ax.fill_between(df_to_plot['DATE'], df_to_plot['Change USD 7D'], 0, where=(df_to_plot['Change USD 7D'] >= 0),
                        interpolate=True, color='green', alpha=0.3)
        ax.fill_between(df_to_plot['DATE'], df_to_plot['Change EUR 7D'], 0, where=(df_to_plot['Change EUR 7D'] >= 0),
                        interpolate=True, color='green', alpha=0.3)

        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.set_title('Portfolio Changes')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.24)
        ax.legend()
        plt.show()
    else:
        messagebox.showerror("Error", "Ypu dont have a Board_Sheet/Prime_sheet.csv")
        window.mainloop()


def graps():
    graps_window = tk.Toplevel(window)
    graps_window.title("Graphics")
    graps_window_width = 300
    graps_window_height = 400
    graps_window_x = x - graps_window_width
    graps_window_y = y
    graps_window.geometry(f"{graps_window_width}x{graps_window_height}+{graps_window_x}+{graps_window_y}")
    graps_window.configure(bg="#1a1c1f")
    graph_button1 = tk.Button(graps_window, text="Coin tracker", command=coing, padx=10, pady=5, fg="white",
                              bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    graph_button3 = tk.Button(graps_window, text="Changes", command=changes, padx=10, pady=5,
                              fg="white", bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    true_value_askbutton = tk.Button(graps_window, text="Value in EUR", command=true_value_eur, padx=10, pady=5,
                                     fg="white", bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    true_value_askbutton.pack(fill="x", pady=(30, 0))
    true_value_askbutton1 = tk.Button(graps_window, text="Value in USD", command=true_value_usd, padx=10, pady=5,
                                      fg="white", bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    true_value_askbutton1.pack(fill="x", pady=(10, 0))
    profit_button = tk.Button(graps_window, text="Profit / Loss (€)", command=profit1, padx=10, pady=5, fg="white",
                              bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    profit_button.pack(fill="x", pady=(30, 0))
    profit_button1 = tk.Button(graps_window, text="Profit / Loss (%)", command=profit2, padx=10, pady=5, fg="white",
                               bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
    profit_button1.pack(fill="x", pady=(10, 0))
    graph_button1.pack(fill="x", pady=(30, 0))
    graph_button3.pack(fill="x", pady=(10, 0))
    graph_button1.bind("<Enter>", lambda event: on_enter(graph_button1))
    graph_button1.bind("<Leave>", lambda event: on_leave(graph_button1))
    graph_button3.bind("<Enter>", lambda event: on_enter(graph_button3))
    graph_button3.bind("<Leave>", lambda event: on_leave(graph_button3))


window = tk.Tk()
window.title("Project Nova")
window_width = 400
window_height = 425
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
image = Image.open("pngegg.png")
image = image.convert("RGBA")
data = image.getdata()
new_data = []
for item in data:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item[:3] + (255,))
image.putdata(new_data)
bbox = image.getbbox()
image = image.crop(bbox)
width, height = image.size
new_size = (int(width/5), int(height/5))
resized_image = image.resize(new_size)
tk_image = ImageTk.PhotoImage(resized_image)
label = tk.Label(window, image=tk_image,)
button1 = tk.Button(window, text="Coins", command=open_coins_window, padx=10, pady=20, fg="white",
                    bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
button2 = tk.Button(window, text="Tax Updater", command=tax, padx=10, pady=20, fg="white", bg="#1f262d",
                    font=("Arial", 12, "bold"), borderwidth=0)
button3 = tk.Button(window, text="Board Sheet", command=board_sheet, padx=10, pady=20, fg="white",
                    bg="#1f262d", font=("Arial", 12, "bold"), borderwidth=0)
button4 = tk.Button(window, text="Graphics", command=graps, padx=10, pady=20, fg="white", bg="#1f262d",
                    font=("Arial", 12, "bold"), borderwidth=0)
button1.bind("<Enter>", lambda event: on_enter(button1))
button1.bind("<Leave>", lambda event: on_leave(button1))
button2.bind("<Enter>", lambda event: on_enter(button2))
button2.bind("<Leave>", lambda event: on_leave(button2))
button3.bind("<Enter>", lambda event: on_enter(button3))
button3.bind("<Leave>", lambda event: on_leave(button3))
button4.bind("<Enter>", lambda event: on_enter(button4))
button4.bind("<Leave>", lambda event: on_leave(button4))
label.pack()
button1.pack(fill="x", pady=(10, 0))
button2.pack(fill="x")
button3.pack(fill="x")
button4.pack(fill="x")
window.configure(bg="#1a1c1f")
print("Loading complete!")
window.mainloop()
