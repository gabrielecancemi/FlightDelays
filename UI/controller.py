import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.aeroportoA = None
        self.aeroportoP = None

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()

    def handleAnalizza(self, e):
        self._view._txtResults.controls.clear()
        n = self._view._txtInCMin.value
        if n is None:
            self._view.create_alert("Inserire il numero")
            return

        try:
            n = int(n)
        except:
            self._view.create_alert("Inserire un intero")

        nodes = self._model.createGraph(n)

        self._view._txtResults.controls.append(ft.Text(f"Nodi: {self._model.sizeNodes()}; Archi: {self._model.sizeEdges()}"))
        self.fillDD(nodes)
        self._view.update_page()


    def handleConnessi(self, e):
        self._view._txtResults.controls.clear()
        if self.aeroportoP is None:
            self._view.create_alert("Inserire l'aeroporto")
            return
        p = self.aeroportoP
        conn = self._model.aeroportiConnessi(p)
        if len(conn) == 0:
            self._view._txtResults.controls.append(ft.Text(f"Nessun aeroporto adiacenti", color="red"))
            return
        self._view._txtResults.controls.append(ft.Text(f"Trovati {len(conn)} aeroporti adiacenti", color="green"))
        for c in conn:
            self._view._txtResults.controls.append(ft.Text(f"{c[0]} - {c[1]} voli"))
        self._view.update_page()

    def handleCerca(self, e):
        self._view._txtResults.controls.clear()
        if self.aeroportoP is None or self.aeroportoA == "":
            self._view.create_alert("Inserire gli aeroporti")
            return
        tratte = self._view._txtInNTratteMax.value
        if tratte is None or tratte == "":
            self._view.create_alert("Inserire il numero di tratte")
        try:
            tratte = int(tratte)
        except:
            self._view.create_alert("Inserire un intero")

        p = self.aeroportoP
        a = self.aeroportoA
        path, voli = self._model.trovaPercorso(p, a, tratte)
        if not path:
            self._view._txtResults.controls.append(ft.Text(f"Nessun percorso trvato da {p} a {a}", color="red"))
            return
        self._view._txtResults.controls.append(ft.Text(f"Percorso da {p} a {a} con {voli} voli e {tratte} tratte", color="green"))
        for c in path:
            self._view._txtResults.controls.append(ft.Text(c))
        self._view.update_page()

    def fillDD(self, nodes):
        for n in nodes:
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(text=n, data=n, on_click=self.changeA))
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(text=n, data=n, on_click=self.changeP))

    def changeA(self, e):
        self.aeroportoA = e.control.data

    def changeP(self, e):
        self.aeroportoP = e.control.data
