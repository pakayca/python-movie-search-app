# Movie Search and Tracker

A lightweight desktop application built with Python and Tkinter. It allows users to search for movies and TV shows using the OMDB API and automatically saves the search history to a local SQLite database.

## Features
* Real-time API Integration: Fetches movie details (IMDB rating, director, plot, genre) via the OMDB API.
* Local Database: Uses SQLite3 to store search history automatically.
* History Log: Retrieves and displays the last 10 movie searches directly within the graphical interface.
* GUI: Clean graphical user interface built with Tkinter.

## Technologies Used
* Python 3
* Tkinter
* SQLite3
* OMDB API

## Setup and Execution
1. Clone this repository:
   ```bash
   git clone https://github.com/pakayca/python-movie-search-app.git
   
2. Get a free API key from OMDB API.

3. Open main.py and paste your API key in the designated variable:
  API_KEY = "YOUR_API_KEY_HERE"

5. Run the application
