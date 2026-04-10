from db import get_connection

def get_active_rentals_count():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM Utleie
    WHERE InnlevertDato IS NULL
    """

    cursor.execute(query)
    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return result


def get_available_equipment_count():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT SUM(AntallPåLager)
    FROM Utstyr
    """

    cursor.execute(query)
    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return result


def get_latest_rentals(limit=5):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT UtleieId, UtstyrId, KundeNr, UtleidDato, InnlevertDato
    FROM Utleie
    ORDER BY UtleidDato DESC
    LIMIT %s
    """

    cursor.execute(query, (limit,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result