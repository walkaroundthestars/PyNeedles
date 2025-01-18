import PySimpleGUI as psg  #poprawić blokowanie dodawania kiedu pola są puste
import re  #dodać sprawdzanie poprawności danych
import sqlite3  #poprawić wyświetlanie bazy w stash

from PySimpleGUI import theme_text_color

from Yarn import Yarn

class Main:
    psg.theme_background_color('#97694F')
    psg.theme_text_color('white')
    psg.theme_element_background_color('#97694F')
    psg.theme_text_element_background_color('#97694F')
    psg.theme_button_color(('white', '#663300'))
    psg.theme_input_text_color('white')
    psg.theme_input_background_color('#663300')
    psg.set_options(font=("Helvetica", 12))
    dataBaseFile = r"yarn.db"

    def __init__(self):
        self.yarns = []
        self.create_db()
        self.get_from_db()

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
        layout = [[psg.Text("Choose what do you want to do.")],
                  [psg.Button(button_text="See stash", size=(15,3)),
                  psg.Button(button_text="Add yarn", size=(15,3)),
                  psg.Button(button_text="Change quantity", size=(15,3))]]

        window = psg.Window("Yarn stash", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event == "See stash":
                self.see_stash()
            if event == "Add yarn":
                self.add_yarn()
            if event == "Change quantity":
                self.change_quantity()
            if event == psg.WIN_CLOSED:
                break

    def see_stash(self):
        headings = ["Brand", "Type", "Color name", "Code","Blend", "Length", "Weight", "Quantity"]

        yarn_values = []
        for yarn in self.yarns:
            yarn_values.append(yarn.get_values())
        table = psg.Table(headings=headings, values=yarn_values, size=(100,75), expand_x=True, expand_y=True, justification="center")

        layout = [[psg.Text("Here you will see your yarn stash"), psg.Cancel()], [table]]

        window = psg.Window("Yarn stash", layout, finalize=True, size=(950, 400), resizable=True)

        while True:
            event, values = window.read()
            if event == "Add yarn":
                self.add_yarn()
            if event == "Change quantity":
                self.change_quantity()
            if event in (psg.WIN_CLOSED, "Cancel"):
                break
        window.close()

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

        window.close()

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
                  [psg.Button(button_text="Add"), psg.Cancel(key="Cancel")],
                  ]

        window = psg.Window("Add yarn to stash", layout, finalize=True, size=(650, 600), resizable=True)

        while True:
            event, values = window.read()
            print(event)
            if event in (psg.WIN_CLOSED, "Cancel"):
                break
            if event == "Add":
                try:
                    yarn = Yarn(brand=values["Brand"],type=values["Type"],color_name=values["ColorName"],blend=values["Blend"],code=values["Code"], length=values["Length"], weight=values["Weight"],quantity=values["Quantity"])
                    self.yarns.append(yarn)
                    self.add_to_db(yarn)
                    psg.Popup("Yarn added to stash")
                    window["Brand"].update("")
                    window["Type"].update("")
                    window["ColorName"].update("")
                    window["Code"].update("")
                    window["Length"].update("")
                    window["Weight"].update("")
                    window["Blend"].update("")
                    window["Quantity"].update("")
                except ValueError as ve:
                    psg.popup_error("Fill all fields!")

        window.close()

    def change_quantity(self):
        lst = psg.Combo(values=self.yarns, key="combo_yarns", enable_events=True)

        layout = [[psg.Text("Here you will be able to change quantity of the yarn in stash")], [lst],
                  [psg.Text("Quantity in stash:"), psg.Text(" - ",key="Quantity")],
                  [psg.Text("Set quantity to:"), psg.Input(key="newQuantity", readonly=False)], [psg.OK()]]

        window = psg.Window("Change quantity", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event == psg.WIN_CLOSED:
                break
            choosen = values["combo_yarns"]
            if event == "combo_yarns":
                if choosen:
                    window["Quantity"].update(choosen.quantity)
            if event == "OK":
                choosen.quantity = int(values["newQuantity"])
                window["Quantity"].update(choosen.quantity)
                self.update_quantity_in_db(choosen, int(values["newQuantity"]))
        window.close()

    def create_db(self):
        connection = sqlite3.connect(Main.dataBaseFile)
        cursor =  connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS yarn (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT, type TEXT, color_name TEXT, code TEXT, length INTEGER, weight INTEGER, blend TEXT, quantity INTEGER)
        ''')

        connection.commit()
        connection.close()

    def add_to_db(self, yarn:Yarn):
        connection = sqlite3.connect(Main.dataBaseFile)
        cursor = connection.cursor()

        cursor.execute('''
                INSERT INTO yarn (brand, type, color_name, code, length, weight, blend, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',(yarn.brand, yarn.type, yarn.color_name, yarn.code, yarn.length, yarn.weight, yarn.blend, yarn.quantity))

        connection.commit()
        connection.close()

    def get_from_db(self):
        connection = sqlite3.connect(Main.dataBaseFile)
        cursor = connection.cursor()

        cursor.execute('''SELECT * FROM yarn''')
        connection.commit()

        data = cursor.fetchall()
        for row in data:
            self.yarns.append(Yarn(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
        connection.close()

    def update_quantity_in_db(self, yarn:Yarn, newQuantity:int):
        connection = sqlite3.connect(Main.dataBaseFile)
        cursor = connection.cursor()
        print(yarn.code, yarn.color_name)
        cursor.execute(f'''UPDATE yarn SET quantity=? WHERE code=? AND color_name=?''',(newQuantity,yarn.code,yarn.color_name))
        connection.commit()

        connection.close()

if __name__ == "__main__":
    app = Main()
    app.main_window()