# Doodle Clone

This is a simple web application that mimics the functionality of Doodle, allowing users to create events and vote on available options (dates). The application is built using Flask, a lightweight web framework for Python.

## Features

- Create new events with a name and multiple date options.
- View all created events and their respective voting options.
- Vote for preferred dates for each event.
- Data is stored in a JSON file for persistence.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install Flask
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

- On the homepage, you can see a list of all events.
- Click on "Neues Event erstellen" to create a new event.
- Fill in the event name and available dates, then submit the form.
- Click on an event to view its details and vote for your preferred date.

## License

This project is licensed under the MIT License.
