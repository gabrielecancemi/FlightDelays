from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAirportsN(n):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.*, count(distinct(f.AIRLINE_ID)) as n
                from flights f, airports a 
                where f.DESTINATION_AIRPORT_ID = a.ID or f.ORIGIN_AIRPORT_ID  = a.ID 
                group by a.ID
                having n >= %s"""

        cursor.execute(query, (n,))

        for row in cursor:
            result.append(Airport(row["ID"], row["IATA_CODE"], row["AIRPORT"], row["CITY"], row["STATE"], row["COUNTRY"], row["LATITUDE"], row["LONGITUDE"], row["TIMEZONE_OFFSET"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getFlights():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.DESTINATION_AIRPORT_ID, f.ORIGIN_AIRPORT_ID, count(*) as n  from flights f 
                group by f.DESTINATION_AIRPORT_ID, f.ORIGIN_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
            result.append((row["DESTINATION_AIRPORT_ID"], row["ORIGIN_AIRPORT_ID"], row["n"]))

        cursor.close()
        conn.close()
        return result