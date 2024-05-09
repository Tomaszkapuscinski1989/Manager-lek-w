from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
import os

import baza

fontMaly = ("Times", 14)
fontDuzy = ("Times", 18)
bg1 = "#3b3a38"
bg2 = "#66625f"
bg3 = "#302c28"
fg1 = "white"


class GenerujDoTxt:
    def __init__(self, rodzic, nazwaBazy):
        self.rodzic = rodzic
        self.nazwaBazy = nazwaBazy

        generujRamka1 = LabelFrame(
            self.rodzic, text="Generuj", bg=bg1, bd=6, fg=fg1, padx=10, pady=10
        )
        generujRamka1.pack()

        generujPrzycisk1 = ttk.Button(
            generujRamka1, text="Generuj listę leków", style="my.TButton"
        )
        generujPrzycisk1.pack(side=LEFT, padx=(0, 5))
        generujPrzycisk1.bind("<Button-1>", self.generujListeLekow)
        generujPrzycisk1.bind("<Return>", self.generujListeLekow)

        generujPrzycisk2 = ttk.Button(
            generujRamka1, text="Generuj listę zapotrzebowania", style="my.TButton"
        )
        generujPrzycisk2.pack(side=LEFT)
        generujPrzycisk2.bind("<Button-1>", self.generujListeZapotrzebowania)
        generujPrzycisk2.bind("<Return>", self.generujListeZapotrzebowania)

    def generujListeZapotrzebowania(self, event):

        aktualnaData = datetime.datetime.now()

        with baza.open_base(self.nazwaBazy) as c:
            c.execute("""SELECT oid FROM TabelaPacjentow""")
            listaId = c.fetchall()
            c.execute("""SELECT * FROM TabelaPacjentow""")
            danePacjentow = c.fetchall()

        with open(f"lista_{aktualnaData:%d-%m-%Y}.txt", "w", encoding="utf-8") as f:
            for index, tymczasowa in enumerate(listaId, 0):
                idPacjenta, *_ = tymczasowa

                with baza.open_base(self.nazwaBazy) as c:
                    c.execute(
                        """SELECT * FROM TabelaLeków WHERE ID=:K1 """,
                        {"K1": idPacjenta},
                    )
                    lekiPacjenta = c.fetchall()

                for lekPacjenta in lekiPacjenta:
                    f.write(
                        f"{lekPacjenta[0]} - potrzebna ilość opakowań {lekPacjenta[1]}\n"
                    )

                f.write("\n")
                f.write(f"{danePacjentow[index][0]} {danePacjentow[index][1]}\n")
                f.write(f"{danePacjentow[index][4]}\n")
                f.write(f"Pesel: {danePacjentow[index][3]}\n")
                f.write("\n")
                f.write("---------------------------------")
                f.write("\n")

        try:
            os.chdir("Listy_zapotrzebowabia")
        except Exception as e:
            os.mkdir("Listy_zapotrzebowabia")
        else:

            os.chdir("..")

        finally:
            os.replace(
                f"./lista_{aktualnaData:%d-%m-%Y}.txt",
                f"./Listy_zapotrzebowabia/lista_{aktualnaData:%d-%m-%Y}.txt",
            )
            messagebox.showinfo("Info", "Wygenerowano listę wszystkich leków")

    def generujListeLekow(self, event):

        aktualnaData = datetime.datetime.now()

        with baza.open_base(self.nazwaBazy) as c:
            c.execute("""SELECT oid FROM TabelaPacjentow""")
            listaId = c.fetchall()
            c.execute("""SELECT * FROM TabelaPacjentow""")
            danePacjentow = c.fetchall()

        with open(f"lista_{aktualnaData:%d-%m-%Y}.txt", "w", encoding="utf-8") as f:
            for index, tymczasowa in enumerate(listaId, 0):
                idPacjenta, *_ = tymczasowa

                with baza.open_base(self.nazwaBazy) as c:
                    c.execute(
                        """SELECT * FROM TabelaLeków WHERE ID=:K1 """,
                        {"K1": idPacjenta},
                    )
                    lekiPacjenta = c.fetchall()

                for lekPacjenta in lekiPacjenta:
                    f.write(f"{lekPacjenta[0]} - dawkowanie {lekPacjenta[3]}\n")

                f.write("\n")
                f.write(f"{danePacjentow[index][0]} {danePacjentow[index][1]}\n")
                f.write(f"{danePacjentow[index][4]}\n")
                f.write(f"Pesel: {danePacjentow[index][3]}\n")
                f.write("\n")
                f.write("---------------------------------")
                f.write("\n")

        try:
            os.chdir("Spis_leków")
        except Exception as e:
            os.mkdir("Spis_leków")
        else:

            os.chdir("..")

        finally:
            os.replace(
                f"./lista_{aktualnaData:%d-%m-%Y}.txt",
                f"./Spis_leków/lista_{aktualnaData:%d-%m-%Y}.txt",
            )
            messagebox.showinfo("Info", "Wygenerowano listę wszystkich leków")
