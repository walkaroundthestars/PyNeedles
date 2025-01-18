import PySimpleGUI as psg
import matplotlib.pyplot as plt  #dodać statystyki
import sqlite3
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
        layout = [[psg.VPush()],[psg.Text("Welcome to PyNeedles!", font=("Helvetica", 20), expand_x=True, justification="center")],
                [psg.Push(), psg.Button(button_text="Yarn stash", size=(15,3)),
                psg.Button(button_text="Count stitches", size=(15,3)), psg.Push()], [psg.VPush()]]

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
        layout = [[psg.Push(), psg.Cancel()],[psg.VPush()],[psg.Text("Choose what do you want to do.", font=("Helvetica", 20), expand_x=True, justification="center")],
                  [psg.Push(), psg.Button(button_text="See stash", size=(15,3)),
                  psg.Button(button_text="Add yarn", size=(15,3)),
                  psg.Button(button_text="Change quantity", size=(15,3)), psg.Push()], [psg.VPush()]]

        window = psg.Window("Yarn stash", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event == "See stash":
                self.see_stash()
            if event == "Add yarn":
                self.add_yarn()
            if event == "Change quantity":
                self.change_quantity()
            if event in (psg.WIN_CLOSED, "Cancel"):
                break

        window.close()

    def see_stash(self):
        headings = ["Brand", "Type", "Color name", "Code", "Blend", "Length", "Weight", "Quantity"]

        yarn_values = []
        for yarn in self.yarns:
            yarn_values.append(yarn.get_values())
        table = psg.Table(headings=headings, header_background_color=psg.theme_input_background_color(), header_text_color="white",
                          values=yarn_values, size=(100,75), expand_x=True, expand_y=True, justification="center")

        layout = [[psg.Text("Your yarn stash:", font=("Bold")), psg.Push(), psg.Button(button_text="Your statistics", key="statistics"), psg.Cancel()], [table]]

        window = psg.Window("Yarn stash", layout, finalize=True, size=(1000, 400), resizable=True)
        window.TKroot.minsize(650, 400)

        while True:
            event, values = window.read()
            if event == "statistics":
                self.statistics()
            if event in (psg.WIN_CLOSED, "Cancel"):
                break
        window.close()

    def count_stitches(self):
        layout = [[psg.Push(), psg.Cancel()],[psg.VPush()],[psg.Text("Count how many stitches you need to cast on.", font=("Helvetica", 15), expand_x=True, justification="center")],
                  [psg.Push(), psg.Text("Number of stitches per 10cm of base yarn:"), psg.Input(key="baseGauge"), psg.Push()],
                  [psg.Push(), psg.Text("Number of stitches per 10cm of your yarn:"), psg.Input(key="userGauge"), psg.Push()],
                  [psg.Push(), psg.Button(button_text="Calculate", size=(15,2)), psg.Push()],
                  [psg.Push(), psg.Text("You need to cast on "), psg.Text("...", key="result"), psg.Text("stitches."), psg.Push()], [psg.VPush()]]


        window = psg.Window("Count stitches", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event == "Calculate":
                if values["baseGauge"].isdigit() and values["userGauge"].isdigit():
                    result = round((int(values["baseGauge"]) * int(values["userGauge"]))/10)
                    window["result"].update(result)
                else:
                    psg.popup_error("Fill all fields correctly!")
            if event in (psg.WIN_CLOSED, "Cancel"):
                break

        window.close()

    def add_yarn(self):
        brands = []
        for yarn in self.yarns:
            if yarn.brand not in brands:
                brands.append(yarn.brand)
        types = []
        for yarn in self.yarns:
            if yarn.type not in types:
                types.append(yarn.type)

        layout = [[psg.Push(),psg.Cancel(key="Cancel")],[psg.VPush()],
                  [psg.Text("Add new yarn to your stash", font=("Helvetica", 15), expand_x=True, justification="center")],
                  [psg.Text("Brand:")],
                  [psg.Combo(key="Brand", values=brands)],
                  [psg.Text("Type:")],
                  [psg.Combo(key="Type", values=types)],
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
                  [psg.Button(button_text="Add")],
                  [psg.VPush()]]

        window = psg.Window("Add yarn to stash", layout, finalize=True, size=(450, 600), resizable=True)
        window.TKroot.minsize(450, 400)

        while True:
            event, values = window.read()
            if event in (psg.WIN_CLOSED, "Cancel"):
                break
            if event == "Add":
                if values["Brand"] and values["Type"] and values["ColorName"] and values["Blend"] and values["Code"] and values["Length"].isdigit() and values["Weight"].isdigit() and values["Quantity"].isdigit():
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
                else:
                    psg.popup_error("Fill all fields correctly!")

        window.close()

    def change_quantity(self):
        basic_yarn_data = []
        for yarn in self.yarns:
            basic_yarn_data.append([yarn.brand, yarn.type, yarn.color_name, yarn.code])

        lst = psg.Combo(values=basic_yarn_data, key="combo_yarns", enable_events=True, readonly=True)

        layout = [[psg.Push(),psg.Cancel()],[psg.VPush()],[psg.Text("Change quantity of the yarn in your stash", font=("Helvetica", 15), expand_x=True, justification="center")],
                  [psg.Push(), lst, psg.Push()],
                  [psg.Push(), psg.Text("Quantity in stash:"), psg.Text(" - ",key="Quantity"), psg.Push()],
                  [psg.Push(), psg.Text("Set quantity to:"), psg.Input(key="newQuantity", readonly=False), psg.Push()],
                  [psg.Push(), psg.Button(button_text="Change"), psg.Push()], [psg.VPush()]]

        window = psg.Window("Change quantity", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event in (psg.WIN_CLOSED, "Cancel"):
                break
            choosen = values["combo_yarns"]
            selected_yarn = None
            if choosen:
                for yarn in self.yarns:
                    if choosen[0] == yarn.brand and choosen[1] == yarn.type and choosen[2] == yarn.color_name and choosen[3] == yarn.code:
                        selected_yarn = yarn
            if event == "combo_yarns":
                if choosen:
                    window["Quantity"].update(selected_yarn.quantity)
            if event == "Change":
                if values["combo_yarns"] and values["newQuantity"].isdigit():
                    selected_yarn.quantity = int(values["newQuantity"])
                    window["Quantity"].update(selected_yarn.quantity)
                    self.update_quantity_in_db(selected_yarn, int(values["newQuantity"]))
                else:
                    psg.popup_error("Fill all fields correctly!")
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
        cursor.execute(f'''UPDATE yarn SET quantity=? WHERE code=? AND color_name=?''',(newQuantity,yarn.code,yarn.color_name))
        connection.commit()

        connection.close()

    def statistics(self):
        layout = [[psg.Push(), psg.Cancel()],
                  [psg.Text("Here you will see your statistics")]]

        window = psg.Window("Statistics", layout, finalize=True, size=(650, 400))

        while True:
            event, values = window.read()
            if event in (psg.WIN_CLOSED, "Cancel"):
                break
        window.close()

if __name__ == "__main__":
    app = Main()
    app.main_window()