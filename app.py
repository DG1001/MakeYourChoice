from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# In-Memory-Speicher für Events
events = {}
event_counter = 1

@app.route('/')
def index():
    """Startseite: Listet alle erstellten Events auf."""
    return render_template_string('''
        <html>
        <head>
            <title>Doodle Clone</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    background-color: #f5f5f7;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #007aff;
                }
                a {
                    color: #007aff;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    margin: 10px 0;
                }
                .button {
                    background-color: #007aff;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .button:hover {
                    background-color: #0051a8;
                }
            </style>
        </head>
        <body>
            <h1>Doodle Clone</h1>
            <p><a class="button" href="{{ url_for('create_event') }}">Neues Event erstellen</a></p>
            <ul>
                {% for event_id, event in events.items() %}
                    <li>
                        <a href="{{ url_for('view_event', event_id=event_id) }}">{{ event['name'] }}</a>
                    </li>
                {% endfor %}
            </ul>
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
        event_counter += 1
        return redirect(url_for('view_event', event_id=event['id']))
    
    # GET: Zeige das Formular zum Erstellen eines neuen Events
    return render_template_string('''
        <html>
        <head>
            <title>Neues Event erstellen</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    background-color: #f5f5f7;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #007aff;
                }
                .button {
                    background-color: #007aff;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .button:hover {
                    background-color: #0051a8;
                }
                form {
                    margin-top: 20px;
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
                }
            </style>
        </head>
        <body>
            <h1>Neues Event erstellen</h1>
            <form method="post">
                <label>Eventname:</label>
                <input type="text" name="name" required>
                <label>Termine (durch Komma getrennt):</label>
                <input type="text" name="options" placeholder="z.B. 2025-03-01, 2025-03-05, 2025-03-10" required>
                <input class="button" type="submit" value="Erstellen">
            </form>
            <p><a class="button" href="{{ url_for('index') }}">Zurück</a></p>
        </body>
        </html>
    ''')

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def view_event(event_id):
    """Seite zur Anzeige eines Events mit den Terminvorschlägen und zur Abstimmung."""
    event = events.get(event_id)
    if event is None:
        return "Event nicht gefunden", 404
    
    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option in event['votes']:
            event['votes'][selected_option] += 1
        return redirect(url_for('view_event', event_id=event_id))
    
    return render_template_string('''
        <html>
        <head>
            <title>{{ event.name }}</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    background-color: #f5f5f7;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #007aff;
                }
                h2 {
                    color: #333;
                }
                .button {
                    background-color: #007aff;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .button:hover {
                    background-color: #0051a8;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    margin: 10px 0;
                }
                select {
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <h1>{{ event.name }}</h1>
            <h2>Termine und Stimmen</h2>
            <ul>
                {% for option, count in event.votes.items() %}
                    <li>{{ option }}: {{ count }} Stimme(n)</li>
                {% endfor %}
            </ul>
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
        </body>
        </html>
    ''', event=event)

if __name__ == '__main__':
    app.run(debug=True)
