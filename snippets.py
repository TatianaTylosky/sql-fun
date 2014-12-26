import psycopg2
import argparse
import logging
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet


def get(name):
    #Retrieve the snippet with a given name.
    logging.info("Retrieving snippet with the name of {!r}".format(name))
    cursor = connection.cursor()
    stringname = str(name)
    command = "select keyword, message from snippets where keyword='" + stringname + "'"
    cursor.execute(command, (name))
    connection.commit()
    snippet = cursor.fetchone()
    logging.debug("Snippet retrieved successfully.")
    
#     if snippet=="":
#       print("There is no snippet with that name.")
#       sys.exit()
    
    #Returns the snippet.
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return snippet  
  
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")


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



if __name__ == "__main__":
    main()
