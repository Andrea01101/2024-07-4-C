from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(datetime) as anno 
                        FROM sighting s 
                        ORDER BY anno DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes_year(anno: int):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape
                            FROM sighting s 
                            WHERE YEAR(s.datetime)=%s
                            ORDER BY shape ASC"""
            cursor.execute(query, (anno,))

            for row in cursor:
                if row["shape"] != "":
                    result.append(row["shape"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodes(year: int, shape: str):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
                            FROM sighting s 
                            WHERE Year(s.datetime)=%s AND s.shape =%s
                            ORDER BY s.longitude ASC"""
            cursor.execute(query, (year, shape,))

            for row in cursor:
                result.append(Sighting(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_edges(year: int, shape: str, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.id as s1id, s2.id as s2id, s2.longitude-s.longitude as peso
                       from sighting s, sighting s2 
                       where year(s2.`datetime`) = year(s.`datetime`) and year(s.`datetime`) = %s
                       and s.state = s2.state and s.shape = s2.shape and s.shape = %s
                       and s.longitude < s2.longitude
                       order by s1id, s2id"""
            cursor.execute(query, (year, shape,))

            for row in cursor:
                result.append((idMap[row["s1id"]],
                               idMap[row["s2id"]],
                               row["peso"]))

            cursor.close()
            cnx.close()
        return result

