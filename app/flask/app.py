from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def loan_prediction_app():
    district_names = ['Rokycany', 'Louny', 'Strakonice', 'Pribram', 'Hl.m. Praha',
  'Brno - mesto', 'Melnik', 'Prachatice', 'Havlickuv Brod', 'Tachov',
  'Bruntal', 'Zlin', 'Vyskov', 'Kromeriz', 'Pelhrimov',
  'Usti nad Labem', 'Praha - vychod', 'Usti nad Orlici',
  'Litomerice', 'Kutna Hora', 'Frydek - Mistek', 'Cheb', 'Opava',
  'Cesky Krumlov', 'Olomouc', 'Zdar nad Sazavou', 'Ceske Budejovice',
  'Prerov', 'Jicin', 'Semily', 'Benesov', 'Rakovnik', 'Pisek',
  'Brno - venkov', 'Jihlava', 'Tabor', 'Karvina', 'Chrudim',
  'Chomutov', 'Teplice', 'Domazlice', 'Karlovy Vary', 'Kolin',
  'Plzen - jih', 'Kladno', 'Sumperk', 'Nachod', 'Liberec',
  'Ostrava - mesto', 'Vsetin', 'Prostejov', 'Svitavy',
  'Jindrichuv Hradec', 'Blansko', 'Pardubice', 'Hradec Kralove',
  'Most', 'Praha - zapad', 'Trebic', 'Nymburk', 'Decin',
  'Plzen - sever', 'Uherske Hradiste', 'Beroun',
  'Rychnov nad Kneznou', 'Plzen - mesto', 'Novy Jicin', 'Trutnov',
  'Breclav', 'Jesenik', 'Mlada Boleslav', 'Hodonin', 'Ceska Lipa',
  'Znojmo', 'Sokolov', 'Klatovy']
    district_names.sort()
    
    return render_template('index.html', district_names=district_names)