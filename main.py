import os
from flask import Flask
app = Flask(__name__)
@app.route("/")
def home():
    return "Debiut – kierowcy działa :truck:"
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
11:34
import os
import pandas as pd
from flask import Flask, render_template_string
app = Flask(__name__)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Trasy Kierowców</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h2 { color: #2c3e50; }
        ul { margin-bottom: 30px; }
    </style>
</head>
<body>
    <h1>Trasy dla 3 kierowców</h1>
    {% for kierowca, trasa in trasy.items() %}
        <h2>{{ kierowca }}</h2>
        <ul>
            {% for adres in trasa %}
                <li>{{ adres }}</li>
            {% endfor %}
        </ul>
    {% endfor %}
</body>
</html>
"""
@app.route("/")
def home():
    # Wczytaj Excel
    try:
        df = pd.read_excel("adresy.xlsx")
    except FileNotFoundError:
        return "Nie znaleziono pliku 'adresy.xlsx' w katalogu aplikacji."
    if 'Adres' not in df.columns:
        return "Plik Excel musi mieć kolumnę o nazwie 'Adres'."
    adresy = df['Adres'].tolist()
    # Podział na 3 kierowców
    kierowcy = {"Kierowca 1": [], "Kierowca 2": [], "Kierowca 3": []}
    for i, adres in enumerate(adresy):
        key = f"Kierowca {(i % 3) + 1}"
        kierowcy[key].append(adres)
    return render_template_string(HTML_TEMPLATE, trasy=kierowcy)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
