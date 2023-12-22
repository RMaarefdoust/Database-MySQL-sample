# IMDb Database Query System

This Python script offers a command-line interface for querying an IMDb database. It establishes a connection to a MySQL database using the `mysql.connector` library and retrieves information through various queries. The database schema encompasses tables for TV series, stars, genres, directors, and more.

## Prerequisites

Ensure you have the following prerequisites installed:

- Python 3.x
- MySQL Server
- `mysql.connector` Python library (install via `pip install mysql-connector-python`)
- `multiple dispatch` Python library (install via `pip install multipledispatch`)

## Usage

The script showcases various queries on the IMDb database:

1. **Release Year Count:**
   - Displays the count of series released each year.

2. **Get Series by Star:**
   - Retrieves a list of series in which a specified star has played.

3. **Get Series by Star and Genre:**
   - Retrieves series titles and ratings for a specified star and genre.

4. **Find Common Series:**
   - Displays the list of series (only titles) that all the input stars have played in.

5. **Get Popular Series by Star:**
   - Retrieves popular series for a specified star.

6. **Average Rating Per Genre:**
   - Calculates and displays the average ratings per genre.

7. **Get Series by Director, Star, and Genre:**
   - Retrieves series titles featuring a star, directed by a specific director, and belonging to a specific genre.

## Customization

**Note:** Make sure to replace placeholders such as `your_host`, `your_user`, and `your_password` with your actual MySQL database credentials.
