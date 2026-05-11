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
        self._view._txtResults.controls.append(ft.Text(f"Trovati {len(conn)} aeroporti"))
        for c in conn:
            self._view._txtResults.controls.append(ft.Text(c))
        self._view.update_page()

    def handleCerca(self, e):
        self._view._txtResults.controls.clear()
        if self.aeroportoP is None or self.aeroportoA == "":
            self._view.create_alert("Inserire l'aeroporto")
            return
        p = self.aeroportoP
        a = self.aeroportoA
        conn = self._model.trovaPercorso(p, a)
        self._view._txtResults.controls.append(ft.Text(f"Trovati {len(conn)} aeroporti"))
        for c in conn:
            self._view._txtResults.controls.append(ft.Text(c))
        self._view.update_page()

    def fillDD(self, nodes):
        for n in nodes:
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(text=n, data=n, on_click=self.change))
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(text=n, data=n, on_click=self.change))

    def change(self, e):
        self.aeroportoA = e.control.data
        self.aeroportoP = e.control.data
