import mysql.connector
import json

def get_database_connection():
    config_file = "connectorConfig.json"
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    conn = mysql.connector.connect(**connection_config)
    return conn

def createProcedure(conn):
    cursor = conn.cursor()

    # Create the SQL procedure to update series ratings
    create_procedure_query = """
    CREATE PROCEDURE UpdateSeriesRating(IN series_name VARCHAR(255), IN new_rating DECIMAL(3,2))
    BEGIN
        DECLARE series_id VARCHAR(255);

        -- Get the series ID based on the series name
        SELECT IMDB_id INTO series_id FROM tvSeries WHERE title = series_name LIMIT 1;

        -- Check if series_id is not null
        IF series_id IS NOT NULL THEN
            -- Update the series rating
            UPDATE tvSeries SET rating = new_rating WHERE IMDB_id = series_id;
            SELECT 'Rating updated successfully.' AS message;
        ELSE
            SELECT 'Series not found.' AS message;
        END IF;
    END;
    """
    cursor.execute(create_procedure_query)
    conn.commit()
    cursor.close()
    

def updateRating(conn,series_name, new_rating):
    # Check if the new rating is within the IMDB range [0, 10]
    if not (0 <= new_rating <= 10):
        print("Invalid rating. Please provide a rating within the IMDB range [0, 10].")
        return

    cursor = conn.cursor()

    try:
        # Call the SQL procedure to update the series rating
        cursor.callproc("UpdateSeriesRating", (series_name, new_rating))
        conn.commit()
        print(f"Rating for series '{series_name}' updated to {new_rating} successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
#-------------------Part2-Question2--------------------------
import mysql.connector
def create_update_rating_procedure(conn):
    cursor = conn.cursor()
    # Create the stored procedure
    procedure_query = """
    CREATE PROCEDURE UpdateSeriesRating2(IN series_name VARCHAR(255), IN new_rating DECIMAL(3,2))
    BEGIN
        DECLARE series_id VARCHAR(255);

        -- Get the series ID based on the series name
        SELECT IMDB_id INTO series_id FROM tvSeries WHERE title = series_name LIMIT 1;

        -- Check if series_id is not null
        IF series_id IS NOT NULL THEN
            -- Check if the new rating is in the IMDB range [0,10]
            IF new_rating >= 0 AND new_rating <= 10 THEN
                -- Update the series rating
                UPDATE tvSeries SET rating = new_rating WHERE IMDB_id = series_id;
                SELECT 'Rating updated successfully.' AS message;
            ELSE
                SELECT 'Invalid rating. Rating should be in the range [0,10].' AS message;
            END IF;
        ELSE
            SELECT 'Series not found.' AS message;
        END IF;
    END;
    """
    cursor.execute(procedure_query)
    conn.commit()
    cursor.close()

def call_update_rating_procedure(conn, series_name, new_rating):
    cursor = conn.cursor()
    # Call the stored procedure
    cursor.callproc("UpdateSeriesRating2", args=(series_name, new_rating))

    # Fetch the result
    for result in cursor.stored_results():
        message = result.fetchone()[0]
        print(message,"\n\n")
    conn.commit()



def main():
    conn=get_database_connection()
    
    print("\n\n-------Update with if statements for Rate in python-----")

    # Create the SQL procedure to update series ratings
    #createProcedure(conn)


    # Example usage of the updateRating method
    series_name = "Babylon"  # Replace with the actual series name
    new_rating = 3.5  # Replace with the desired new rating

    # Call the method to update the series rating
    updateRating(conn,series_name, new_rating)


    #-------------------------------------------------------
    #-----------Part2-Question2----------------------------
    print("\n\n-------Update with if statements for Rate in MySQ-------  ")

    # Create the stored procedure
    #create_update_rating_procedure(conn)


    # Call the stored procedure with sample values
    call_update_rating_procedure(conn, "Babylon", 9.5)

    conn.close()


if __name__ == "__main__":
    main()

