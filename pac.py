from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import baza
import lek

fontMaly = ("Times", "14")
fontDuzy = ("Times", "18")
bg1 = "#3b3a38"
bg2 = "#66625f"
bg3 = "#302c28"
fg1 = "white"


class Pacjenci:
    def __init__(self, rodzic, nazwaBazy):
        self.rodzic = rodzic
        self.nazwaBazy = nazwaBazy

        pacjenciRamka1 = LabelFrame(
            self.rodzic, text="Pacjent", bg=bg1, bd=6, fg=fg1, padx=10, pady=10
        )

        pacjenciRamka1.pack()

        pacjenciRamka2 = Frame(pacjenciRamka1, bg=bg1)
        pacjenciRamka2.pack(side=LEFT)

        yPasekPrzewijacia = ttk.Scrollbar(pacjenciRamka2, orient=VERTICAL)
        yPasekPrzewijacia.pack(side=RIGHT, fill=Y)

        self.listaPacjentowWBazie = Listbox(
            pacjenciRamka2,
            yscrollcommand=yPasekPrzewijacia.set,
            font=fontMaly,
            bg=bg2,
            fg=fg1,
        )
        self.listaPacjentowWBazie.pack(expand=True)

        yPasekPrzewijacia.config(command=self.listaPacjentowWBazie.yview)

        with baza.open_base(self.nazwaBazy) as c:
            c.execute("""SELECT * FROM TabelaPacjentow""")
            danePacjentow = c.fetchall()

        for danePacjenta in danePacjentow:
            imieInazwisko = f"{danePacjenta[0]} {danePacjenta[1]}"
            self.listaPacjentowWBazie.insert(END, imieInazwisko)

        self.listaPacjentowWBazie.config(activestyle="none")

        self.listaPacjentowWBazie.bind("<Double-Button-1>", self.wyswietlPacjentow)

        pacjenciRamka3 = Frame(pacjenciRamka1, bg=bg1)
        pacjenciRamka3.pack(side=LEFT)

        id_lable = Label(
            pacjenciRamka3, text="Id:", anchor=E, font=fontDuzy, bg=bg1, fg=fg1
        )
        self.idPacjet = Entry(
            pacjenciRamka3,
            font=fontMaly,
            state=DISABLED,
            disabledbackground=bg3,
            disabledforeground=fg1,
        )
        id_lable.grid(row=0, column=0, sticky=W + E)
        self.idPacjet.grid(row=0, column=1, sticky=W + E, padx=10)

        name_lable = Label(
            pacjenciRamka3, text="Imię:", anchor=E, font=fontDuzy, bg=bg1, fg=fg1
        )
        name_lable.grid(row=1, column=0, sticky=W + E)
        self.imiePacjenta = Entry(pacjenciRamka3, font=fontMaly, bg=bg2, fg=fg1)
        self.imiePacjenta.grid(row=1, column=1, sticky=W + E, padx=10)

        last_lable = Label(
            pacjenciRamka3, text="Nazwisko:", anchor=E, font=fontDuzy, bg=bg1, fg=fg1
        )
        last_lable.grid(row=2, column=0, sticky=W + E)
        self.nazwiskoPacjenta = Entry(pacjenciRamka3, font=fontMaly, bg=bg2, fg=fg1)
        self.nazwiskoPacjenta.grid(row=2, column=1, sticky=W + E, padx=10)

        phone_lable = Label(
            pacjenciRamka3, text="Telefon:", anchor=E, font=fontDuzy, bg=bg1, fg=fg1
        )
        phone_lable.grid(row=3, column=0, sticky=W + E)
        self.telefonPacjenta = Entry(pacjenciRamka3, font=fontMaly, bg=bg2, fg=fg1)
        self.telefonPacjenta.grid(row=3, column=1, sticky=W + E, padx=10)

        phone_lable = Label(
            pacjenciRamka3, text="Pesel:", anchor=E, font=fontDuzy, bg=bg1, fg=fg1
        )
        self.peselPacjenta = Entry(pacjenciRamka3, font=fontMaly, bg=bg2, fg=fg1)
        phone_lable.grid(row=4, column=0, sticky=W + E)
        self.peselPacjenta.grid(row=4, column=1, sticky=W + E, padx=10)

        phone_lable = Label(
            pacjenciRamka3, text="Adres:", anchor=E, font=fontDuzy, bg=bg1, fg=fg1
        )
        self.adresPacjenta = Entry(pacjenciRamka3, font=fontMaly, bg=bg2, fg=fg1)
        phone_lable.grid(row=5, column=0, sticky=W + E)
        self.adresPacjenta.grid(row=5, column=1, sticky=W + E, padx=10)

        pacjenciRamka4 = Frame(pacjenciRamka1, bg=bg1)
        pacjenciRamka4.pack(pady=10)

        nowyPrzycisk = ttk.Button(pacjenciRamka4, text="Nowy", style="my.TButton")
        nowyPrzycisk.grid(row=0, column=0, sticky=W + E)
        nowyPrzycisk.bind("<Button-1>", self.nowyPacjent)
        nowyPrzycisk.bind("<Return>", self.nowyPacjent)

        edytujPrzycisk = ttk.Button(pacjenciRamka4, text="Edytuj", style="my.TButton")
        edytujPrzycisk.grid(row=1, column=0, sticky=W + E, pady=5)
        edytujPrzycisk.bind("<Button-1>", self.edytujDanePacjenta)
        edytujPrzycisk.bind("<Return>", self.edytujDanePacjenta)

        usunPrzycisk = ttk.Button(pacjenciRamka4, text="Usuń", style="my.TButton")
        usunPrzycisk.grid(row=2, column=0, sticky=W + E)
        usunPrzycisk.bind("<Button-1>", self.usunPacjenta)
        usunPrzycisk.bind("<Return>", self.usunPacjenta)

        self.leki = lek.Leki(self.rodzic, self.nazwaBazy)

    def wyswietlPacjentow(self, event):

        self.idPacjet.configure(state="normal")
        self.idPacjet.delete(0, END)
        self.imiePacjenta.delete(0, END)
        self.nazwiskoPacjenta.delete(0, END)
        self.telefonPacjenta.delete(0, END)
        self.peselPacjenta.delete(0, END)
        self.adresPacjenta.delete(0, END)

        index = self.listaPacjentowWBazie.index(ANCHOR)

        with baza.open_base(self.nazwaBazy) as c:
            c.execute("""SELECT *,oid FROM TabelaPacjentow""")
            DanePacjentaZoid = c.fetchall()

        self.idPacjet.insert(0, DanePacjentaZoid[index][-1])
        self.imiePacjenta.insert(0, DanePacjentaZoid[index][0])
        self.nazwiskoPacjenta.insert(0, DanePacjentaZoid[index][1])
        self.telefonPacjenta.insert(0, DanePacjentaZoid[index][2])
        self.peselPacjenta.insert(0, DanePacjentaZoid[index][3])
        self.adresPacjenta.insert(0, DanePacjentaZoid[index][4])
        self.idPacjet.configure(state="disabled")

        self.leki.kk(DanePacjentaZoid[index][-1])

    def nowyPacjent(self, event):

        if (
            (self.imiePacjenta.get() != "")
            and (self.nazwiskoPacjenta.get() != "")
            and (self.telefonPacjenta.get() != "")
            and (self.peselPacjenta.get() != "")
            and (self.adresPacjenta.get() != "")
        ):

            if (len(self.telefonPacjenta.get()) == 9) and (
                len(self.peselPacjenta.get()) == 11
            ):
                try:
                    with baza.open_base(self.nazwaBazy) as c:
                        c.execute(
                            "INSERT INTO TabelaPacjentow VALUES (:k1, :k2, :k3, :k4, :k5)",
                            {
                                "k1": self.imiePacjenta.get(),
                                "k2": self.nazwiskoPacjenta.get(),
                                "k3": int(self.telefonPacjenta.get()),
                                "k4": int(self.peselPacjenta.get()),
                                "k5": self.adresPacjenta.get(),
                            },
                        )
                except ValueError:
                    messagebox.showerror("Error", "Podaj poprawny dane/")
                except Exception as e:
                    messagebox.showerror("Error", "Nie znany bład")
                else:
                    self.odswiezDanePacjentów()

                    messagebox.showinfo("Info", "Dodano pacjenta")

            else:
                messagebox.showerror(
                    "Error",
                    "Podaj poprawny dane\nNumer telefonu powinien składać się z 9 cyfr a pesel z 11 cyfr",
                )

        else:
            messagebox.showerror("Error", "Uzupełj wszystkie dane")

    def edytujDanePacjenta(self, event):

        if (
            (self.imiePacjenta.get() != "")
            and (self.nazwiskoPacjenta.get() != "")
            and (self.telefonPacjenta.get() != "")
            and (self.peselPacjenta.get() != "")
            and (self.adresPacjenta.get() != "")
        ):
            if (len(self.telefonPacjenta.get()) == 9) and (
                len(self.peselPacjenta.get()) == 11
            ):
                try:
                    index = self.listaPacjentowWBazie.index(ANCHOR)

                    with baza.open_base(self.nazwaBazy) as c:
                        c.execute("""SELECT *,oid FROM TabelaPacjentow""")
                        danePacjentowZoid = c.fetchall()

                    oid = danePacjentowZoid[index][-1]

                    with baza.open_base(self.nazwaBazy) as c:
                        c.execute(
                            """UPDATE TabelaPacjentow SET IMIE=:k1, NAZWISKO=:k2, TELEFON=:k3, PESEL=:k4, ADRES=:k5 WHERE oid = :k6 """,
                            {
                                "k1": self.imiePacjenta.get(),
                                "k2": self.nazwiskoPacjenta.get(),
                                "k3": self.telefonPacjenta.get(),
                                "k4": self.peselPacjenta.get(),
                                "k5": self.adresPacjenta.get(),
                                "k6": oid,
                            },
                        )

                except Exception as e:
                    messagebox.showerror("Error", "Wybierz wpis")
                else:
                    self.odswiezDanePacjentów()

                    messagebox.showinfo("Info", "Wpis edytowano")
            else:
                messagebox.showerror(
                    "Error",
                    "Podaj poprawny danenNumer telefonu powinien składać się z 9 cyfr a pesel z 11 cyfr",
                )

        else:
            messagebox.showerror("Error", "Uzupełj wszystkie dane")

    def usunPacjenta(self, event):

        try:
            index = self.listaPacjentowWBazie.index(ANCHOR)

            with baza.open_base(self.nazwaBazy) as c:
                c.execute("""SELECT *,oid FROM TabelaPacjentow""")
                danePacjentoeZoid = c.fetchall()

            oid = danePacjentoeZoid[index][-1]

        except Exception as e:
            messagebox.showerror("Error", "Wybierz wpis do usunięcia")

        else:
            with baza.open_base(self.nazwaBazy) as c:
                c.execute(
                    """DELETE FROM TabelaPacjentow where oid=:oid""", {"oid": oid}
                )
                c.execute("""DELETE FROM TabelaLeków where ID=:oid""", {"oid": oid})

            self.odswiezDanePacjentów()

            messagebox.showinfo("Info", "Wpis usunieto")

    def odswiezDanePacjentów(self):

        with baza.open_base(self.nazwaBazy) as c:
            c.execute("""SELECT * FROM TabelaPacjentow""")
            danePacjentow = c.fetchall()

        self.listaPacjentowWBazie.delete(0, END)
        for danePacjenta in danePacjentow:
            imieInazwisko = f"{danePacjenta[0]} {danePacjenta[1]}"
            self.listaPacjentowWBazie.insert(END, imieInazwisko)

        self.idPacjet.configure(state="normal")
        self.idPacjet.delete(0, END)
        self.imiePacjenta.delete(0, END)
        self.nazwiskoPacjenta.delete(0, END)
        self.telefonPacjenta.delete(0, END)
        self.peselPacjenta.delete(0, END)
        self.adresPacjenta.delete(0, END)
        self.idPacjet.configure(state="disabled")
