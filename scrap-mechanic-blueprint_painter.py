from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QColorDialog, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from os import listdir, environ
from os.path import basename, dirname, isdir, isfile
from shutil import copy2
from json import load, dump

c = None
p = f'{environ["APPDATA"]}/Axolot Games/Scrap Mechanic/User/'
blueprint_path = f'{p}{listdir(p)[0]}/Blueprints/'; l = listdir(blueprint_path)
b = {}

app = QApplication([], styleSheet='QComboBox QAbstractItemView {background: #d3d3d3; border: 1px solid grey;}')
app.setApplicationName("Scrap Mechanic Blueprint Festő")
w = QWidget(styleSheet='QWidget {font-family: Arial; background-color: #71797e;} QMessageBox QLabel {color: white; font-weight: bold;}', windowIcon=QIcon('icon.png'), height=250)
cw = QWidget(styleSheet='QColorDialog QPushButton {font-family: Arial; color: black} QColorDialog {background: #1f2120} QColorDialog QLabel {font-family: Arial; color: white;}', windowIcon=QIcon('icon.png'))
blueprint_list = QComboBox(w, styleSheet='font-size: 25px; font-weight: bold; background: #d3d3d3', iconSize=QSize(64, 64))
colorchooser = QPushButton('Szín kiválasztása', w, styleSheet='font-size: 25px; font-weight: bold; background: #d3d3d3')
paint = QPushButton('Festés!', w, styleSheet='font-size: 25px; font-weight: bold; background: DarkGreen')

layout = QVBoxLayout(w)
layout.addWidget(blueprint_list)
layout.addWidget(colorchooser)
layout.addWidget(paint)

def ch():
    global c
    color = QColorDialog(parent=cw)
    c = color.getColor(parent=cw).name().strip('#')
    colorchooser.setStyleSheet(f'font-size: 25px; font-weight: bold; background: #{c}')
def pa():
    global c
    if c is None:
        QMessageBox(QMessageBox.Critical, 'Hiba', 'Nem adtál meg színt!', QMessageBox.Ok, w).exec_()
    else:
        file = b[str(blueprint_list.currentText())]+'/blueprint.json'
        if isfile(file):
            with open(file, 'r') as f:
                try:
                    data = load(f)
                except:
                    QMessageBox(QMessageBox.Critical, 'Hiba', 'A blueprint nem értelmezhető! (üres, hibás, nem blueprint, stb...)', QMessageBox.Ok, w).exec_()
                    pass
                else:
                    try:
                        for i in range(len(data['bodies'])):
                            for j in range(len(data['bodies'][i]['childs'])):
                                data['bodies'][i]['childs'][j]['color'] = c
                        if 'joints' in data:
                            for i in range(len(data['joints'])):
                                data['joints'][i]['color'] = c
                    except:
                        QMessageBox(QMessageBox.Critical, 'Hiba', 'A blueprint nem értelmezhető! (üres, hibás, nem blueprint, stb...)', QMessageBox.Ok, w).exec_()
                        pass
                    else:
                        n = basename(file).split('.')
                        n[0] += '_backup'
                        try:
                            copy2(file, dirname(file)+'/'+('.'.join(n)))
                        except:
                            QMessageBox(QMessageBox.Critical, 'Hiba', 'A biztonsági mentés létrehozása sikertelen!', QMessageBox.Ok, w).exec_()
                        try:
                            with open(b[str(blueprint_list.currentText())]+'/description.json', 'r', encoding='utf-8') as f:
                                ds = load(f)
                            ds['description'] += ' |Átfestve|'
                            with open(b[str(blueprint_list.currentText())]+'/description.json', 'w', encoding='utf-8') as f:
                                ds = dump(ds, f, separators=(",", ":"))
                        except:
                            pass
                        try:
                            with open(file, 'w') as f:
                                dump(data, f, separators=(",", ":"))
                        except:
                            QMessageBox(QMessageBox.Critical, 'Hiba', 'A blueprint módosítása sikertelen!', QMessageBox.Ok, w).exec_()
                            pass
                        else:
                            QMessageBox(QMessageBox.Information, 'Információ', 'Festés sikeres!', QMessageBox.Ok, w).exec_()
        else:
            QMessageBox(QMessageBox.Critical, 'Hiba', 'A blueprint nem létezik!', QMessageBox.Ok, w).exec_()
for i in l:
    if isdir(f'{blueprint_path}{i}'):
        with open(f'{blueprint_path}{i}/description.json', 'r', encoding='utf-8') as f:
            try: d = load(f)
            except: pass
            else:
                b[d['name']] = f'{blueprint_path}{i}'
                try:
                    blueprint_list.addItem(QIcon(f'{blueprint_path}{i}/icon.png'), d['name'])
                except:
                    pass
colorchooser.clicked.connect(ch)
paint.clicked.connect(pa)
w.show()
app.exec_()
