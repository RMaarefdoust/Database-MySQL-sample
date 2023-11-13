from cgi import print_arguments
import mysql.connector
import json
from collections import Counter
import itertools
from multipledispatch import dispatch

def get_database_connection():
    config_file = "connectorConfig.json"
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    conn = mysql.connector.connect(**connection_config)
    return conn

#------------------------Question1---------------------------------
def releaseyearCount(conn):
    cursor = conn.cursor()
    # count series by release year
    query = """
    SELECT ReleaseYear, SUM(series_count) AS total_series_count
    FROM (
            SELECT ReleaseYear, COUNT(*) AS series_count
            FROM tvSeries
            GROUP BY ReleaseYear
        ) subquery
    GROUP BY ReleaseYear
    ORDER BY ReleaseYear;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

#---------------------------Question2---------------------------------
@dispatch(object, str)
def getSeries(conn, star_name):
    cursor = conn.cursor()
    
    #get series titles for the specified star
    query = """
    SELECT ts.title
    FROM tvSeries ts
    JOIN SeriesStars acs ON ts.IMDB_id = acs.IMDB_id
    WHERE acs.star = %s;
    """
    cursor.execute(query, (star_name,))
    result = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return result

#---------------------------Question3---------------------
@dispatch(object, str, str)
def getSeries(conn, starName, genre):
    cursor = conn.cursor()
    # get series titles and ratings for the specified star and genre
    query = """
    SELECT ts.title, ts.rating
    FROM tvSeries ts
    JOIN SeriesStars acs ON ts.IMDB_id = acs.IMDB_id
    JOIN SeriesGenre sg ON ts.IMDB_id = sg.IMDB_id
    WHERE acs.star = %s AND sg.genre = %s;
    """
    cursor.execute(query, (starName, genre))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        if genre is None:
            print(f"{starName} has not played in any series.")
        else:
            print(f"{starName} has not played in any series in the {genre} genre.")
    else:
        if genre is None:
            print(f"Series in which {starName} has played:")
        else:
            print(f"Series in the {genre} genre in which {starName} has played:")
        for row in results:
            if genre is None:
                print(f"Title: {row[0]}")
            else:
                print(f"Title: {row[0]}, Rating: {row[1]}")

#-----------------------------Question4----------------------------------
def getSeriesCostar(conn,list_starNames):
    if not list_starNames:
        return []  # Return an empty list if the input list is empty
    cursor = conn.cursor()
    # Create a temporary table to hold the series for each star
    cursor.execute("CREATE TEMPORARY TABLE TempSeries (star_name VARCHAR(255), series_title VARCHAR(255))")
    # Insert the series for each star into the temporary table
    for starName in list_starNames:
        query = """
            INSERT INTO TempSeries (star_name, series_title)
            SELECT %s, ts.title
            FROM tvSeries ts
            JOIN SeriesStars acs ON ts.IMDB_id = acs.IMDB_id
            WHERE acs.star = %s;
        """
        cursor.execute(query, (starName, starName))
    in1=len(list_starNames)
    # Find the common series 
    query = f"""
        SELECT series_title
        FROM TempSeries
        GROUP BY series_title
        HAVING COUNT(*) >= {in1};
    """
    cursor.execute(query)
    common_series = [row[0] for row in cursor.fetchall()]
    # Drop the temporary table
    cursor.execute("DROP TEMPORARY TABLE TempSeries")
    cursor.close()
    return common_series

#------------------------------Question5--------------------------------
def getPopularSeries(conn,starName):
    cursor = conn.cursor()

    # Calculate the average rating
    avg_rating_query = "SELECT AVG(rating) FROM tvSeries;"
    cursor.execute(avg_rating_query)
    avg_rating = cursor.fetchone()[0]

    # get popular series titles for the specified star
    query = """
    SELECT ts.title
    FROM tvSeries ts
    JOIN SeriesStars acs ON ts.IMDB_id = acs.IMDB_id
    WHERE acs.star = %s AND ts.rating > %s;
    """
    cursor.execute(query, (starName, avg_rating))
    popular_series = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return popular_series
#------------------------------Question 6-----------------------------
def getRatingPerGenre(conn):
    cursor = conn.cursor()

    #  calculate the average rating for each genre
    query = """
    SELECT sg.genre, AVG(ts.rating) AS average_rating
    FROM SeriesGenre sg
    JOIN tvSeries ts ON sg.IMDB_id = ts.IMDB_id
    GROUP BY sg.genre;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("\033[31m Average Ratings Per Genre:\033[0m")
    for result in results:
        genre, average_rating = result
        print(f"\033[91m {genre}: {average_rating:.2f} \033[0m")
    cursor.close()

#----------------------Question7--------------------------
def getSeriesDirectorStarGenre(conn,director, star, genre):
    cursor = conn.cursor()
    query = """
        SELECT ts.title
        FROM tvSeries ts
        WHERE ts.IMDB_id IN (
            SELECT sd.IMDB_id
            FROM SeriesDirector sd
            WHERE sd.director = %s
        ) AND ts.IMDB_id IN (
            SELECT ss.IMDB_id
            FROM SeriesStars ss
            WHERE ss.star = %s
        ) AND ts.IMDB_id IN (
            SELECT sg.IMDB_id
            FROM SeriesGenre sg
            WHERE sg.genre = %s
        );
    """
    cursor.execute(query, (director, star, genre))
    results = cursor.fetchall()
    series_titles = [result[0] for result in results]
    cursor.close()
    return series_titles

#----------------------------------------------------------
#------------------Main------------------------------------
def main():
    conn = get_database_connection()
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    print(RED+BOLD+"------------------Question1------------------")
    # Example Question 1
    series_counts = releaseyearCount(conn)
    for year, count in series_counts:
        print(f"Year {year}: {count} series released.")
    print(GREEN+BOLD+"------------------------------------------------")
    

    # Example Question 2
    print(GREEN+BOLD+"------------------Question2------------------")
    star_name = "Jack Nicholson"
    series_list = getSeries(conn, star_name)
    print(f"Series in which {star_name} has played:")
    for series_title in series_list:
        print(series_title)
    print(YELLOW+BOLD+"------------------------------------------------")
    
    
    # Example Question 3
    print(YELLOW+BOLD+"------------------Question3------------------") 
    star_name = "Jack Nicholson"
    genre_name = "Horror"
    getSeries(conn,star_name, genre_name)
    print(RED+BOLD+"------------------------------------------------")
    
    
    # Example Question 4
    print(RED+BOLD+"------------------Question4------------------")
    list_starNames = ["Tom Hanks", "Meryl Streep"]
    common_series = getSeriesCostar(conn,list_starNames)
    print(f"The common series for all persons of list: {', '.join(list_starNames)} are: {', '.join(common_series)}")
    print(GREEN+BOLD+"------------------------------------------------")
    
    
    # Example Question5
    print(GREEN+BOLD+"------------------Question5------------------")
    star_name = "Jack Nicholson"
    popular_series = getPopularSeries(conn,star_name)
    print(f"Popular series that  {star_name}  has played in: {',  '.join(popular_series)}")
    print(RED+BOLD+"------------------------------------------------")


    # Example Question6
    print(RED+BOLD+"------------------Question6------------------")
    getRatingPerGenre(conn)
    print(YELLOW+BOLD+"------------------------------------------------")


    # Example Question7
    print(YELLOW+BOLD+"------------------Question7------------------")
    director = "David F. Sandberg"
    star = "Zachary Levi"
    genre = "Comedy"  
    series_list = getSeriesDirectorStarGenre(conn,director, star, genre)

    if series_list:
        print(f"Series featuring {star},\n directed by {director}, \n and belonging to the {genre} genre:")
        i=1
        for series_title in series_list:
            print(str(i)+"-----",series_title)
            i=i+1
    else:
        print(f"No series found for {star} featuring {star}, directed by {director}, and belonging to the {genre} genre.")
    
    print(GREEN+BOLD+"------------------------------------------------")

    conn.close()

if __name__ == "__main__":
    main()
