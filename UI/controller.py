import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()

        if self._view.ddyear.value is None:
            self._view.txt_result1.controls.append(ft.Text("Inserire un anno"))
            self._view.update_page()
            return
        if self._view.ddshape.value is None or self._view.ddshape.value == "":
            self._view.txt_result1.controls.append(ft.Text("Inserire una forma"))
            self._view.update_page()
            return

        year = int(self._view.ddyear.value)
        shape = self._view.ddshape.value
        self._model.buildGraph(year, shape)
        n = self._model.getNodes()
        e = self._model.getEdges()

        self._view.txt_result1.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero vertici: {n}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero archi: {e}"))

        lista = self._model.getTopFiveEdges()
        self._view.txt_result1.controls.append(ft.Text("I 5 archi di peso maggiore sono"))
        for edge in lista:
            self._view.txt_result1.controls.append(ft.Text(f"{edge[0].id}->{edge[1].id}| weight = {edge[2]['weight']}"))

        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDYear(self):
        years = self._model.getYear()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(f"{y}"))
        self._view.update_page()

    def handle_ddshape(self, e):
        self._view.ddshape.value = None
        year = int(self._view.ddyear.value)
        shapes = self._model.getShape(year)
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()
