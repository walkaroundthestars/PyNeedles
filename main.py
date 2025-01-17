import PySimpleGUI as psg
import re  #dodać sprawdzanie poprawności danych
import sqlite3  #dodać baze danych
from Yarn import Yarn

class Main:
    psg.theme_background_color('#97694F')
    psg.theme_text_color('white')
    psg.theme_element_background_color('#97694F')
    psg.theme_text_element_background_color('#97694F')
    psg.theme_button_color(('white', '#663300'))
    psg.theme_input_text_color('white')
    psg.theme_input_background_color('#663300')

    def main_window(self):
        layout = [[psg.Text("Welcome to PyNeedles!", font=("Helvetica", 20), expand_x=True, justification="center")],
                [psg.Button(button_text="Yarn stash", size=(15,3)),
                psg.Button(button_text="Count stitches", size=(15,3))]]

        window = psg.Window("Welcome!", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event == "Yarn stash":
                self.yarn_stash()
            if event == "Count stitches":
                self.count_stitches()
            if event == psg.WIN_CLOSED:
                break

    def yarn_stash(self):
        layout = [[psg.Text("Here you will see your yarn stash")],
                  [psg.Button(button_text="See stash", size=(15,3)),
                  psg.Button(button_text="Add yarn", size=(15,3)),
                  psg.Button(button_text="Change quantity", size=(15,3))]]

        window = psg.Window("Yarn stash", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event == "Add yarn":
                self.add_yarn()
            if event == "Change quantity":
                self.change_quantity()
            if event == psg.WIN_CLOSED:
                break

    def count_stitches(self):
        layout = [[psg.Text("Here you will see counter for stitches")],
                  [psg.Text("Number of stitches per 10cm of base yarn:"), psg.Input(key="baseGauge")],
                  [psg.Text("Number of stitches per 10cm of your yarn:"), psg.Input(key="userGauge")],
                  [psg.Button(button_text="Calculate", size=(15,2)), psg.Text("Result", key="result")]]


        window = psg.Window("Count stitches", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event == "Calculate":
                result = (int(values["baseGauge"]) * int(values["userGauge"]))/10
                window["result"].update(result)
            if event == psg.WIN_CLOSED:
                break

    def add_yarn(self):
        layout = [[psg.Text("Here will be a form for adding yarn")],
                  [psg.Text("Brand:")],
                  [psg.Input(key="Brand")],
                  [psg.Text("Type:")],
                  [psg.Input(key="Type")],
                  [psg.Text("ColorName:")],
                  [psg.Input(key="ColorName")],
                  [psg.Text("Blend:")],
                  [psg.Input(key="Blend")],
                  [psg.Text("Code:")],
                  [psg.Input(key="Code")],
                  [psg.Text("Length per skein:")],
                  [psg.Input(key="Length")],
                  [psg.Text("Weight per skein:")],
                  [psg.Input(key="Weight")],
                  [psg.Text("Quantity in grams:")],
                  [psg.Input(key="Quantity")],
                  [psg.OK(), psg.Cancel()]
                  ]

        window = psg.Window("Add yarn to stash", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event == psg.WIN_CLOSED or event == "Cancel":
                break

            yarn = Yarn(brand=values["Brand"],type=values["Type"],color_name=values["ColorName"],blend=values["Blend"],code=values["Code"], length=values["Length"], weight=values["Weight"],quantity=values["Quantity"])

            print(f"Added {yarn.quantity} grams of {yarn.brand} {yarn.type} in color {yarn.color_name}")

    def change_quantity(self):
        yarns = ["blue", "yellow", "green", "black", "white"]
        lst = psg.Combo(values=yarns, key="yarns")

        layout = [[psg.Text("Here you will be able to change quantity of the yarn in stash")], [lst],
                  [psg.Text("Quantity in stash:"), psg.Input(key="Quantity", readonly=True)],
                  [psg.Text("Set quantity to:"), psg.Input(key="newQuantity", readonly=False)], [psg.OK()]]

        window = psg.Window("Change quantity", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event == psg.WIN_CLOSED:
                break

if __name__ == "__main__":
    app = Main()
    app.main_window()