"""
Creates needed tables and loads test bookmark data
"""

import pyodbc

def load_data(con):
    """ Use SQL to load records into the data structure
    Args:
        con: database connection object
    Returns:
        true if creation is successful, otherwise returns the exception
    """
    cursor = con.cursor()
    try:
        cursor.execute("""
            INSERT INTO Tagit.Resource (uri, title) 
            VALUES ('https://docs.intersystems.com/iris20194/csp/docbook/Doc.View.cls?KEY=RSQL_droptable', 'DROP TABLE')
        """)
        cursor.execute("""
            INSERT INTO Tagit.Resource (uri, title) 
            VALUES ('https://docs.intersystems.com/iris20194/csp/docbook/Doc.View.cls?KEY=AFL_globals', 'First Look: Globals')
        """)
        cursor.execute("""
            INSERT INTO Tagit.Tag (name) 
            VALUES ('sql')
        """)
        cursor.execute("""
            INSERT INTO Tagit.Tag (name) 
            VALUES ('intersystemsiris')
        """)
        cursor.execute("""
            INSERT INTO Tagit.Tag (name) 
            VALUES ('table')
        """)
        cursor.execute("""
            INSERT INTO Tagit.Tag (name) 
            VALUES ('globals')
        """)
        cursor.execute("""
            INSERT INTO Tagit.Tag (name) 
            VALUES ('objectscript')
        """)
        con.commit()
    except Exception as e:
        print("Error loading data: " + str(e))
        return e

    print("Data loaded!")
    return True

def load_references(con):
    """ Use SQL to create the references between tags and bookmarks
    Args:
        con: database connection object
    Returns:
        true if creation is successful, otherwise returns the exception
    """
    cursor = con.cursor()
    try:
        cursor.execute("""
            INSERT INTO Tagit.TagMap 
            (tagid, resourceid) 
            VALUES (1,1)
        """)
        cursor.execute("""
            INSERT INTO Tagit.TagMap 
            (tagid, resourceid) 
            VALUES (2,1)
        """)
        cursor.execute("""
            INSERT INTO Tagit.TagMap 
            (tagid, resourceid) 
            VALUES (3,1)
        """)
        cursor.execute("""
            INSERT INTO Tagit.TagMap 
            (tagid, resourceid) 
            VALUES (2,2)
        """)
        cursor.execute("""
            INSERT INTO Tagit.TagMap 
            (tagid, resourceid) 
            VALUES (5,2)
        """)
        con.commit()
    except Exception as e:
        print("Error loading data: " + str(e))
        return e

    print("References loaded!")
    return True


def drop_tables(con):
    """ Use SQL to drop data structures
    Args:
        con: database connection object
    Returns:
        true if creation is successful, otherwise returns the exception
    """
    cursor = con.cursor()
    try:
        cursor.execute("""
            DROP TABLE Tagit.Resource CASCADE
        """)
        cursor.execute("""
            DROP TABLE Tagit.Tag CASCADE
        """)
        cursor.execute("""
            DROP TABLE Tagit.TagMap CASCADE
        """)
        con.commit()
    except Exception as e:
        print("Error deleting tables: " + str(e))
        return e

    print("Deleted tables!")
    return True

def create_tables(con):
    """ Use SQL to create data structures
    Args:
        con: database connection object
    Returns:
        true if creation is successful, otherwise returns the exception
    """

    cursor = con.cursor()
    try:
        cursor.execute("""
            CREATE TABLE Tagit.Resource
            (
                uri VARCHAR(4096), 
                title VARCHAR(512), 
                type VARCHAR(512) DEFAULT 'bookmark', 
                views INT DEFAULT 1, 
                %PUBLICROWID 
            )
        """)
        cursor.execute("""
            CREATE TABLE Tagit.Tag
            (
                name VARCHAR(128) UNIQUE, 
                description VARCHAR(4096),
                %PUBLICROWID 
            )
        """)
        cursor.execute("""
            CREATE TABLE Tagit.TagMap
            (
                tagid INT, 
                resourceid INT, 
                CONSTRAINT tagidFK FOREIGN KEY (tagid) REFERENCES Tagit.Tag, 
                CONSTRAINT resourceidFK FOREIGN KEY (resourceid) REFERENCES Tagit.Resource, 
                %PUBLICROWID 
            )
        """)
        con.commit()
    except Exception as e:
        print("Error creating tables: " + str(e))
        return e

    print("Created tables!")
    return True

def get_connection_info(file_name):
    """ Get connection details from config file
    Args:
        file_name: name of file on disk including path (relative or absolute)
    Returns:
        a dictionary containing connection details
    """
    
    # Initial empty dictionary to store connection details
    connections = {}

    # Open config file to get connection info
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            # remove all white space (space, tab, new line)
            line = ''.join(line.split())

            # get connection info
            connection_param, connection_value = line.split(":", 1)
            connections[connection_param] = connection_value
    return connections


def run():
    # Retrieve connection information from configuration file
    connection_detail = get_connection_info("connection.config")

    ip = connection_detail["ip"]
    port = int(connection_detail["port"])
    namespace = connection_detail["namespace"]
    username = connection_detail["username"]
    password = connection_detail["password"]
    driver = "{InterSystems ODBC}"

    # Create connection to InterSystems IRIS
    connection_string = 'DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}' \
        .format(driver, ip, port, namespace, username, password)

    connection = pyodbc.connect(connection_string)
    print("Connected to InterSystems IRIS")

    drop_tables(connection)
    create_tables(connection)
    load_data(connection)
    load_references(connection)

if __name__ == '__main__':
    run()
