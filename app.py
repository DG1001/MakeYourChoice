from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

app = Flask(__name__)

# In-Memory-Speicher für Events
events = {}
event_counter = 1
data_file = 'data.json'

def load_events():
    global events, event_counter
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            events = json.load(f)
            # Umwandlung der Schlüssel in Ganzzahlen
            event_counter = max(map(int, events.keys())) + 1 if events else 1

def save_events():
    with open(data_file, 'w') as f:
        json.dump(events, f)

@app.route('/')
def index():
    """Startseite: Listet alle erstellten Events auf."""
    return render_template_string('''
        <html>
        <head>
            <title>Doodle Clone</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f0f4f8;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #007aff;
                    text-align: center;
                }
                a {
                    color: #007aff;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    margin: 10px 0;
                    padding: 10px;
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    transition: background-color 0.3s;
                }
                li:hover {
                    background-color: #f9f9f9;
                }
                .button {
                    display: inline-block;
                    background-color: #007aff;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-align: center;
                    text-decoration: none;
                    margin: 10px 0;
                }
                .button:hover {
                    background-color: #0051a8;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: center;
                }
                th {
                    background-color: #007aff;
                    color: white;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Doodle Clone</h1>
                <p><a class="button" href="{{ url_for('create_event') }}">Neues Event erstellen</a></p>
                <ul>
                    {% for event_id, event in events.items() %}
                        <li>
                            <a href="{{ url_for('view_event', event_id=event_id) }}">{{ event['name'] }}</a>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        </body>
        </html>
    ''', events=events)

@app.route('/create', methods=['GET', 'POST'])
def create_event():
    """Seite zum Erstellen eines neuen Events.
       Im POST-Request werden Eventname und Optionen (durch Komma getrennt) verarbeitet."""
    global event_counter
    if request.method == 'POST':
        event_name = request.form.get('name', '').strip()
        options = request.form.get('options', '')
        # Die Termine werden über Komma getrennt eingegeben
        option_list = [opt.strip() for opt in options.split(',') if opt.strip()]
        if not event_name or not option_list:
            return "Bitte geben Sie einen Eventnamen und mindestens einen Termin an.", 400
        # Erzeuge das Event als Dictionary
        event = {
            'id': event_counter,
            'name': event_name,
            'options': option_list,
            'votes': {option: 0 for option in option_list}
        }
        events[event_counter] = event
        save_events()  # Speichere die Events in der JSON-Datei
        event_counter += 1  # Aktualisiere den event_counter nach dem Hinzufügen des Events
        return redirect(url_for('view_event', event_id=event['id']))
    
    # GET: Zeige das Formular zum Erstellen eines neuen Events
    return render_template_string('''
        <html>
        <head>
            <title>Neues Event erstellen</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f0f4f8;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #007aff;
                    text-align: center;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                .button {
                    display: inline-block;
                    background-color: #007aff;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-align: center;
                    text-decoration: none;
                    margin: 10px 0;
                }
                .button:hover {
                    background-color: #0051a8;
                }
                form {
                    max-width: 600px;
                    margin: 0 auto;
                }
                label {
                    display: block;
                    margin: 10px 0 5px;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    margin-bottom: 10px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Neues Event erstellen</h1>
                <form method="post">
                    <label>Eventname:</label>
                    <input type="text" name="name" required>
                    <label>Termine (durch Komma getrennt):</label>
                    <input type="text" name="options" placeholder="z.B. 2025-03-01, 2025-03-05, 2025-03-10" required>
                    <input class="button" type="submit" value="Erstellen">
                </form>
                <p><a class="button" href="{{ url_for('index') }}">Zurück</a></p>
            </div>
        </body>
        </html>
    ''')

@app.route('/event/<event_id>', methods=['GET', 'POST'])
def view_event(event_id):
    """Seite zur Anzeige eines Events mit den Terminvorschlägen und zur Abstimmung."""
    event = events.get(event_id)  # event_id als String verwenden
    if event is None:
        return "Event nicht gefunden", 404
    
    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option in event['votes']:
            event['votes'][selected_option] += 1
        save_events()  # Speichere die aktualisierten Stimmen in der JSON-Datei
        return redirect(url_for('view_event', event_id=event_id))
    
    return render_template_string('''
        <html>
        <head>
            <title>{{ event.name }}</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f0f4f8;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #007aff;
                    text-align: center;
                }
                h2 {
                    color: #333;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                .button {
                    display: inline-block;
                    background-color: #007aff;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-align: center;
                    text-decoration: none;
                    margin: 10px 0;
                }
                .button:hover {
                    background-color: #0051a8;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: center;
                }
                th {
                    background-color: #007aff;
                    color: white;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{{ event.name }}</h1>
                <h2>Termine und Stimmen</h2>
                <table>
                    <tr>
                        <th>Termin</th>
                        <th>Stimmen</th>
                    </tr>
                    {% for option, count in event.votes.items() %}
                        <tr>
                            <td>{{ option }}</td>
                            <td>{{ count }}</td>
                        </tr>
                    {% endfor %}
                </table>
                <h2>Abstimmen</h2>
                <form method="post">
                    <label>Wählen Sie einen Termin:</label>
                    <select name="option">
                        {% for option in event.options %}
                            <option value="{{ option }}">{{ option }}</option>
                        {% endfor %}
                    </select>
                    <input class="button" type="submit" value="Abstimmen">
                </form>
                <p><a class="button" href="{{ url_for('index') }}">Zurück zur Übersicht</a></p>
            </div>
        </body>
        </html>
    ''', event=event)

if __name__ == '__main__':
    load_events()  # Lade die Events beim Start der Anwendung
    app.run(debug=True)
