from tkinter import *
from tkinter import ttk

import pac
import baza

fontMaly = ("Times", 14)
fontDuzy = ("Times", 18)
bg1 = "#3b3a38"
bg2 = "#66625f"
bg3 = "#302c28"
fg1 = "white"


class Main(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Manager leków")
        self.configure(bg=bg1)
        self.geometry("+10+10")
        self.nazwaBazy = "Spis_Leków.db"

        with baza.open_base(self.nazwaBazy) as c:

            c.execute(
                """ CREATE TABLE IF NOT EXISTS TabelaPacjentow (
                IMIE text,
                NAZWISKO text,
                TELEFON text,
                PESEL text,
                ADRES text

                )"""
            )

            c.execute(
                """ CREATE TABLE IF NOT EXISTS TabelaLeków (
                Nazwa text,
                ILOSC text,
                ID text,
                DAWKOWANIE text
                )"""
            )

        pac.Pacjenci(self, self.nazwaBazy)


# ________________________________________________________________________________________________


if __name__ == "__main__":

    start = Main()

    s = ttk.Style()
    s.theme_use("default")

    s.configure(
        "mystyle.Treeview",
        rowheight=25,
        fieldbackground=bg2,
        background=bg2,
        foreground=fg1,
        font=fontMaly,
    )
    s.configure("mystyle.Treeview.Heading", font=fontMaly, foreground="black")

    s.map(
        "mystyle.Treeview",
        background=[("selected", "blue")],
        foreground=[("selected", fg1)],
    )

    s.configure("my.TButton", font=fontMaly)
    s.map("my.TButton", relief=[("pressed", "SUNKEN"), ("!pressed", "rised")])

    s.configure(
        "mystyle.TCombobox",
        fieldbackground=bg2,
        background=bg2,
        foreground=fg1,
        font=fontMaly,
    )

    start.mainloop()
