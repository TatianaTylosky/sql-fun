import psycopg2
import argparse
import logging
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def catalog():
    logging.info("fetching catalog")
    command = "select keyword from snippets order by keyword"
    with connection, connection.cursor() as cursor:
        cursor.execute(command)
        keywords = cursor.fetchall()
    
    logging.debug("Keywords retrieved successfully.")
    return keywords
 
# this needs fixing
def everything():
  logging.info("get everything")
  command = "select * from snippets"
  with connection, connection.cursor() as cursor:
    cursor.execute(command)
    alldata = cursor.fetchall()
    
  logging.debug("Got everything successfully")
  return alldata

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    command = "insert into snippets values (%s, %s)"
    
    
    with connection, connection.cursor() as cursor:
      cursor.execute("select message from snippets where keyword=%s", (name,))
    
      try:
          command = "insert into snippets values (%s, %s)"
          cursor.execute(command, (name, snippet))
      except psycopg2.IntegrityError as e:
          connection.rollback()
          command = "update snippets set message=%s where keyword=%s"
          cursor.execute(command, (snippet, name))

    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet


def get(name):
    #Retrieve the snippet with a given name.
    logging.info("Retrieving snippet with the name of {!r}".format(name))
    stringname = str(name)
    command = "select keyword, message from snippets where keyword='" + stringname + "'"
    
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        snippet = cursor.fetchone()
    
    logging.debug("Snippet retrieved successfully.")
    
    if not snippet:
        print("No snippet was found with that name.")
        sys.exit()
    
    #Returns the snippet.
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return snippet  
  
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    
    # Subparser for the catalog command
    logging.debug("Constructing catalog subparser")

    catalog_parser = subparsers.add_parser("catalog", help="Catalog")

    
     # Subparser for the everything command
    logging.debug("Constructing everything subparser")

    everything_parser = subparsers.add_parser("everything", help="Store a snippet")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")

    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")

    get_parser = subparsers.add_parser("get", help="Get a snippet")
    get_parser.add_argument("name", help="The name of the snippet")    
    
    
    arguments = parser.parse_args(sys.argv[1:])
      
      

    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        keywords = catalog(**arguments)
        print("Retrieved catalog: {!r}".format(keywords))
    elif command == "everything":
        alldata = everything(**arguments)
        print("Retrieved all data: {!r}".format(alldata))
        print type(alldata)




if __name__ == "__main__":
    main()
