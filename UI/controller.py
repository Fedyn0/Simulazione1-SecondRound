import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenre = None

    def fillDDGenre(self):

        genres = self._model.getAllGenres()

        for genre in genres:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(key = genre,
                                   data = genre,
                                   on_click= self._choiceDDGenre)
            )
        self._view.update_page()

    def _choiceDDGenre(self,e):
        self._choiceGenre = e.control.data
        print(f"Hai selezionato il genere {self._choiceGenre}")

    def handleCreaGrafo(self, e):
        print(self._choiceGenre.GenreId)
        self._model.buildGraph(self._choiceGenre.GenreId)

    def handleCammino(self,e):
        pass