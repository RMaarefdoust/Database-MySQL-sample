import mysql.connector
import json
import time

def get_database_connection():
    config_file = "connectorConfig.json"
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    conn = mysql.connector.connect(**connection_config)
    return conn
def createAvgProcedure(conn):
    cursor = conn.cursor()

    # Create a stored procedure to get average ratings per genre
    create_procedure_query = """
    CREATE PROCEDURE GetAvgRatingsPerGenre()
    BEGIN
        DECLARE start_time TIMESTAMP;
        DECLARE end_time TIMESTAMP;

        SET start_time = CURRENT_TIMESTAMP;

        SELECT sg.genre, IFNULL(AVG(ts.rating), 0) AS average_rating
        FROM SeriesGenre sg
        LEFT JOIN tvSeries ts ON sg.IMDB_id = ts.IMDB_id
        GROUP BY sg.genre;

        SET end_time = CURRENT_TIMESTAMP;
        SELECT TIMEDIFF(end_time, start_time) AS execution_time;
    END;
    """
    cursor.execute(create_procedure_query)

    conn.commit()

def callAvgProcedure(conn):
    cursor = conn.cursor()

    # Call the stored procedure to get average ratings per genre
    cursor.callproc("GetAvgRatingsPerGenre")

    # Fetch the results
    print("Genre\t\tAverage Rating")
    print("---------------------------")
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            print(f"{row}")  # Print the entire row

    cursor.close()

def pythonAvgFunction(conn):
    start_time = time.time()

    cursor = conn.cursor()
    query = """
    SELECT sg.genre, AVG(ts.rating) AS average_rating
    FROM SeriesGenre sg
    JOIN tvSeries ts ON sg.IMDB_id = ts.IMDB_id
    GROUP BY sg.genre;
    """
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()
    print("\033[31m Average Ratings Per Genre:\033[0m")
    for result in results:
        genre, average_rating = result
        print(f"\033[91m {genre}: {average_rating:.2f} \033[0m")

    cursor.close()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken for pythonAvgFunction: {execution_time} seconds")
    return execution_time


def main():
    # Call the function to calculate average rating for each genre
    conn = get_database_connection()
    # Create the stored procedure
    #createAvgProcedure(conn)

    time1=pythonAvgFunction(conn)
    print()

    # Call the stored procedure and measure time
    start_time = time.time()
    callAvgProcedure(conn)
    end_time = time.time()

    execution_time = end_time - start_time
    
    print("\033[31m-----------------------------------------------\033[0m")
    print(f"Time taken callAvgProcedure: {execution_time:.2f} seconds")
    print("\033[31m-----------------------------------------------\033[0m")
    print(f"Time taken Pythonode: {time1:.2f} seconds")
    print("\033[31m-----------------------------------------------\033[0m")



    conn.close()

if __name__ == "__main__":
    main()
