from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import baza
import txt


fontDuzy = ("Times", 18)
fontMaly = ("Times", 14)
bg1 = "#3b3a38"
bg2 = "#66625f"
bg3 = "#302c28"
fg1 = "white"


class Leki:
    def __init__(self, rodzic, nazwaBazy):
        self.nazwaBazy = nazwaBazy
        self.rodzic = rodzic

        with baza.open_base(self.nazwaBazy) as c:
            c.execute("SELECT * FROM TabelaLeków")
            r4 = c.fetchall()

        self.counter = len(r4)

        lekiRamka1 = LabelFrame(
            self.rodzic, text="Leki", bg=bg1, bd=6, fg=fg1, padx=10, pady=10
        )
        lekiRamka1.pack(fill=X, expand=True)

        lekiRamka2 = Frame(lekiRamka1, bg=bg1)
        lekiRamka2.pack(fill=X, expand=True)

        self.tree_frame = Frame(lekiRamka2)
        self.tree_frame.pack(side=LEFT, fill=X, expand=True)

        tree_scrolly = ttk.Scrollbar(self.tree_frame)
        tree_scrolly.pack(side=RIGHT, fill=Y)
        tree_scrollx = ttk.Scrollbar(self.tree_frame, orient=HORIZONTAL)
        tree_scrollx.pack(side=BOTTOM, fill=X)

        self.my_tree = ttk.Treeview(
            self.tree_frame,
            style="mystyle.Treeview",
            selectmode="browse",
            yscrollcommand=tree_scrolly.set,
            xscrollcommand=tree_scrollx.set,
        )
        self.my_tree.pack(fill=X, expand=True)

        tree_scrolly.config(command=self.my_tree.yview)
        tree_scrollx.config(command=self.my_tree.xview)

        self.my_tree["columns"] = ("nazwa", "ilosc", "dawk", "oid")

        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.heading("#0", text="", anchor=E)

        self.my_tree.column("nazwa", anchor=W, width=140)
        self.my_tree.heading("nazwa", text="Nazwa", anchor=W)

        self.my_tree.column("ilosc", anchor=W, width=40)
        self.my_tree.heading("ilosc", text="Ilośc", anchor=W)

        self.my_tree.column("dawk", anchor=W, width=40)
        self.my_tree.heading("dawk", text="Dawkowanie", anchor=W)

        self.my_tree.column("oid", width=0, stretch=NO)
        self.my_tree.heading("oid", text="", anchor=E)

        self.my_tree.tag_configure("odd", background=bg2)
        self.my_tree.tag_configure("even", background=bg3)

        self.my_tree.bind("<Double-Button-1>", self.WyswietlLek)

        lekiRamka3 = Frame(lekiRamka2, bg=bg1)
        lekiRamka3.pack(side=RIGHT, fill=Y, padx=(10, 0))

        nowyPrzycisk = ttk.Button(lekiRamka3, text="Nowy lek", style="my.TButton")
        nowyPrzycisk.pack()
        nowyPrzycisk.bind("<Button-1>", self.nowyLek)
        nowyPrzycisk.bind("<Return>", self.nowyLek)

        edytujPrzycisk = ttk.Button(lekiRamka3, text="Edytuj lek", style="my.TButton")
        edytujPrzycisk.pack(pady=5)
        edytujPrzycisk.bind("<Button-1>", self.edytujLek)
        edytujPrzycisk.bind("<Return>", self.edytujLek)

        usunPrzycisk = ttk.Button(lekiRamka3, text="Usuń lek", style="my.TButton")
        usunPrzycisk.pack()
        usunPrzycisk.bind("<Button-1>", self.usunLek)
        usunPrzycisk.bind("<Return>", self.usunLek)

        resetPrzycisk = ttk.Button(lekiRamka3, text="Resetuj ilość", style="my.TButton")
        resetPrzycisk.pack(pady=(5, 0))
        resetPrzycisk.bind("<Button-1>", self.resetujIloscLekow)
        resetPrzycisk.bind("<Return>", self.resetujIloscLekow)

        lekiRamka4 = Frame(lekiRamka1, bg=bg1)
        lekiRamka4.pack(fill=X, expand=True)

        nazwaLekuEtykieta = Label(
            lekiRamka4, text="Nazwa", font=fontDuzy, bg=bg1, fg=fg1
        )
        self.nazwaLeku = Entry(lekiRamka4, font=fontMaly, bg=bg2, fg=fg1)
        iloscLekuEtykieta = Label(
            lekiRamka4, text="Ilość", font=fontDuzy, bg=bg1, fg=fg1
        )
        self.iloscLeku = Entry(lekiRamka4, font=fontMaly, bg=bg2, fg=fg1)
        dawkaLekuEtykieta = Label(
            lekiRamka4, text="Dawkowanie", font=fontDuzy, bg=bg1, fg=fg1
        )
        self.dawkaLeku = Entry(lekiRamka4, font=fontMaly, bg=bg2, fg=fg1)

        nazwaLekuEtykieta.grid(row=0, column=0, sticky=W + E)
        self.nazwaLeku.grid(row=0, column=1, sticky=W + E)
        iloscLekuEtykieta.grid(row=1, column=0, sticky=W + E)
        self.iloscLeku.grid(row=1, column=1, sticky=W + E)
        dawkaLekuEtykieta.grid(row=2, column=0, sticky=W + E)
        self.dawkaLeku.grid(row=2, column=1, sticky=W + E)

        self.txt = txt.GenerujDoTxt(self.rodzic, self.nazwaBazy)

    def WyswietlLek(self, event):
        try:
            self.nazwaLeku.delete(0, END)
            self.iloscLeku.delete(0, END)
            self.dawkaLeku.delete(0, END)

            selected = self.my_tree.focus()
            self.values = self.my_tree.item(selected, "values")

            self.nazwaLeku.insert(0, self.values[0])
            self.iloscLeku.insert(0, self.values[1])
            self.dawkaLeku.insert(0, self.values[2])

        except Exception:
            pass

    def kk(self, pac_id):

        self.index = pac_id

        with baza.open_base(self.nazwaBazy) as c:
            c.execute(
                "SELECT Nazwa, ILOSC, DAWKOWANIE, oid FROM TabelaLeków where ID=:k1",
                {"k1": pac_id},
            )
            r2 = c.fetchall()

        self.my_tree.delete(*self.my_tree.get_children())

        with baza.open_base(self.nazwaBazy) as c:
            c.execute("SELECT * FROM TabelaLeków")
            r4 = c.fetchall()

        self.counter = len(r4)

        for value in r2:

            if self.counter % 2 == 0:

                self.my_tree.insert(
                    parent="",
                    index="end",
                    iid=self.counter,
                    text="",
                    values=(value[0], value[1], value[2], value[-1]),
                    tags=("odd",),
                )
            else:
                self.my_tree.insert(
                    parent="",
                    index="end",
                    iid=self.counter,
                    text="",
                    values=(value[0], value[1], value[2], value[-1]),
                    tags=("even",),
                )
            self.counter += 1

        self.nazwaLeku.delete(0, END)
        self.iloscLeku.delete(0, END)
        self.dawkaLeku.delete(0, END)

    def nowyLek(self, event):

        if (
            (self.nazwaLeku.get() != "")
            and (self.iloscLeku.get() != "")
            and (self.dawkaLeku.get() != "")
        ):

            try:
                with baza.open_base(self.nazwaBazy) as c:
                    c.execute(
                        "INSERT INTO TabelaLeków VALUES (:k1, :k2, :k3, :k4)",
                        {
                            "k1": self.nazwaLeku.get(),
                            "k2": int(self.iloscLeku.get()),
                            "k3": self.index,
                            "k4": self.dawkaLeku.get(),
                        },
                    )
            except ValueError:
                messagebox.showerror("Error", "Ilość musi byc liczbą")

            except Exception as e:

                messagebox.showerror("Error", "Nie znany bląd")

            else:
                self.kk(self.index)
                messagebox.showinfo("Info", "Dodano nowy lek")
                self.values = ""

        else:
            messagebox.showerror("Error", "Uzupełj wszystkie dane")

    def edytujLek(self, event):

        if (
            (self.nazwaLeku.get() != "")
            and (self.iloscLeku.get() != "")
            and (self.dawkaLeku.get() != "")
        ):

            try:

                with baza.open_base(self.nazwaBazy) as c:
                    c.execute(
                        """UPDATE TabelaLeków SET Nazwa=:k1, ILOSC=:k2, DAWKOWANIE=:k3  WHERE oid = :k4 """,
                        {
                            "k1": self.nazwaLeku.get(),
                            "k2": int(self.iloscLeku.get()),
                            "k3": self.dawkaLeku.get(),
                            "k4": self.values[-1],
                        },
                    )

                self.kk(self.index)

            except AttributeError:
                messagebox.showerror("Error", "Ilość musi byc liczbą")
            except ValueError:

                messagebox.showerror("Error", "Ilość musi byc liczbą")

            except Exception:
                messagebox.showerror("Error", "Nie znany bląd")
            else:

                messagebox.showinfo("Info", "Wpis edytowano")
                self.values = ""

        else:
            messagebox.showerror("Error", "Uzupełj wszystkie dane")

    def usunLek(self, event):

        try:
            with baza.open_base(self.nazwaBazy) as c:
                c.execute(
                    """DELETE FROM TabelaLeków where oid=:oid""",
                    {"oid": self.values[-1]},
                )

            self.kk(self.index)

        except AttributeError:
            messagebox.showerror("Error", "Wybierz wpis")
        except Exception:
            messagebox.showerror("Error", "Nie znany bląd")
        else:
            messagebox.showinfo("Info", "Wpis usunięto")
            self.values = ""

    def resetujIloscLekow(self, event):
        try:
            with baza.open_base(self.nazwaBazy) as c:
                c.execute("SELECT oid FROM TabelaLeków")
                r2 = c.fetchall()

            for i in r2:
                with baza.open_base(self.nazwaBazy) as c:
                    c.execute(
                        """UPDATE TabelaLeków SET ILOSC=:k1 WHERE oid = :k2 """,
                        {
                            "k1": "0",
                            "k2": i[0],
                        },
                    )

            self.kk(self.index)

        except AttributeError:
            messagebox.showerror("Error", "Brak wpisów")
        except Exception:
            messagebox.showerror("Error", "Nie znany bląd")
        else:
            messagebox.showinfo("Info", "Wyzerowano  ilość leków")
