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

## Database Average Ratings per Genre

This Python script demonstrates the calculation of average ratings per genre from a MySQL database. The script connects to the database using the `mysql-connector`, performs the calculation through both a stored procedure and a direct Python function, and measures the execution time for comparison.

### Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- MySQL Server
- `mysql-connector` Python package (install using `pip install mysql-connector`)

### Configuration

1. Create a MySQL database and tables `SeriesGenre` and `tvSeries` with appropriate columns.
2. Update the `connectorConfig.json` file with your MySQL connection details.

### Usage

1. Run the script by executing the following command:

   ```bash
   python script_name.py
   ```

2. The script will:

   - Connect to the MySQL database.
   - Optionally, create a stored procedure (`GetAvgRatingsPerGenre`) for calculating average ratings per genre.
   - Calculate average ratings per genre using both the stored procedure and a direct Python function.
   - Display the results and execution time for both methods.

### Important Notes

- Uncomment the `createAvgProcedure(conn)` line in the `main()` function if you want to create the stored procedure before calculating average ratings.
- Ensure that your MySQL server is running and accessible before executing the script.

## Series Rating Updater

This Python script provides functionality to update the ratings of TV series in a MySQL database. It includes two methods of updating ratings: one directly in Python with if statements, and the other through a MySQL stored procedure with additional if statements for rating validation.

### Prerequisites

Before running the script, ensure that you have:

- Python 3.x
- MySQL Server
- `mysql-connector` Python package (install using `pip install mysql-connector`)

### Configuration

1. Create a MySQL database and a table `tvSeries` with appropriate columns.
2. Update the `connectorConfig.json` file with your MySQL connection details.

### Usage

1. Run the script by executing the following command:

   ```bash
   python script_name.py
   ```

2. The script will:

   - Connect to the MySQL database.
   - Optionally, create a stored procedure (`UpdateSeriesRating2`) for updating series ratings with additional validation.
   - Update the rating of a specified TV series using both Python with if statements and the MySQL stored procedure.
   - Display the results.

### Important Notes

- Uncomment the `createProcedure(conn)` line in the `main()` function if you want to create the original stored procedure before updating series ratings.
- Uncomment the `create_update_rating_procedure(conn)` line in the `main()` function if you want to create the updated stored procedure for additional rating validation.
- Ensure that your MySQL server is running and accessible before executing the script.
