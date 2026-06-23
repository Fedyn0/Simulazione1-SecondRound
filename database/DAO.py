from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllGenres():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select g.*
                from genre g """
            cursor.execute(query)

            for row in cursor:
                result.append(Genre(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(genreId):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct  ar.*
            from artist ar, album al, track t
            where ar.ArtistId = al.ArtistId 
            and al.AlbumId = t.AlbumId 
            and t.GenreId = %s"""

            cursor.execute(query, (genreId,))

            for row in cursor:
                result.append(Artist(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(genreId, idMapA):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct a1.ArtistId as id1, a2.ArtistId as id2
                    from invoice i1, invoiceLine il1, track t1, album a1,
                         invoice i2, invoiceLine il2, track t2, album a2
                    where i1.CustomerId = i2.CustomerId 
                    and i1.InvoiceId = il1.InvoiceId
                    and il1.TrackId = t1.TrackId
                    and t1.AlbumId = a1.AlbumId
                    and i2.InvoiceId = il2.InvoiceId
                    and il2.TrackId = t2.TrackId
                    and t2.AlbumId = a2.AlbumId
                    and a1.ArtistId < a2.ArtistId
                    and t1.GenreId = t2.GenreId 
                    and t1.GenreId = %s"""

            cursor.execute(query, (genreId, ))

            for row in cursor:
                artista1 = idMapA[row["id1"]]
                artista2 = idMapA[row["id2"]]
                result.append((artista1, artista2))

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getPopolaritaOfArtista(ArtistId, GenreId):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select count(i.InvoiceLineId) as popolarita
                from invoiceline i, track t, album a 
                where i.TrackId = t.TrackId 
                and t.AlbumId = a.AlbumId 
                and ArtistId = %s
                and t.GenreId = %s"""

            cursor.execute(query, (ArtistId, GenreId ))

            for row in cursor:
                result.append(row["popolarita"])

            cursor.close()
            cnx.close()

        return result