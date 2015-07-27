#!/usr/bin/python
# This was a homework assignment in my computer networking class in the
# Fall quarter of 2013.

# Imported modules
import socket
import os        # So we know the proper OS path separator.
import random    # For fun :D

# Constants
SERVER_PORT = 6789                                         # Port number, as required by assignment.
SERVER_NAME = ''                                           # Host name, as required by assignment.
SERVER_ADDRESS = (SERVER_NAME, SERVER_PORT)                # Address of server, using AF_INET style address
SERVER_WORKING_DIRECTORY = os.path.realpath(os.getcwd())   # The working directory of the web server (canonical name)
BUFFER_SIZE = 1024                                         # Size of receive buffer.

#####################
# makePageWithTitle #
#####################
def makePageWithTitle(title, htmlMessage):
    """Takes a string and makes a simple web page from it."""
    return ("<html><head><title>{0}" +
           "</title></head><body>{1}" +
           "</body></html>").format(title, htmlMessage)

############################
# requestedFileToLocalFile #
############################
def requestedFileToLocalFile(fileName):
    """\
    Takes a file name that a client would request, and converts
    it to the appropriate file on the local machine.
    """
    fileName = fileName.strip()                 # Remove leading and trailing whitespace
    fileName = fileName.replace('/', os.sep)    # Replace all forward slashes with the proper path separator.

    # If we just have the path separator, then default to index.html
    if fileName == os.sep:
        return requestedFileToLocalFile("index.html")

    # Remove the beginning path separator if one is there.
    elif fileName[0] == os.sep:
        fileName = fileName[1:]

    # Get the absolute (canonical) path to this file.
    fileName = os.path.realpath(fileName)

    # Only return the name of the file if it can be found
    # within the working directory of the web server.
    if fileName.startswith(SERVER_WORKING_DIRECTORY):
        return fileName
    else:
        return None

########
# main #
########
def main():
    """Entry point."""

    # Prepare the welcoming socket.
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP socket.  Addresses will be of the form (hostnameOrIP, portNumber).
    serverSocket.bind(SERVER_ADDRESS)                                   # Bind the server's welcoming socket to the address previously defined.
    serverSocket.listen(5)                                              # Listen for connections made to the server.  The 5 represents the maximum number of queued connections.

    # Display some status information.
    print 'The server is ready to accept connections!  Server address: ' + str(SERVER_ADDRESS)

    # From here, we just sit around and wait for a connection.
    while True:

        # Establish the connection
        print 'Waiting for connection . . .'
        connectionSocket, addr = serverSocket.accept()
        print 'Connection received by ' + str(addr)

        # This is where we handle the connection.
        try:

            # Wait for a message.
            print 'Waiting for message.  Buffer size is ' + str(BUFFER_SIZE)
            message = connectionSocket.recv(BUFFER_SIZE)

            # If we did not receive anything, say so and try again.
            if len(message) < 1:
                print 'Nothing received.'
                continue

            # Okay, we got one, so I'm just displaying this for debugging purposes.
            print 'Message received.'
            print 'Length of message ==> ' + str(len(message))
            print
            xx = 'Message Content'
            print xx
            print '-' * len(xx)
            print message

            # Although this is not necessary, I am a Python novice, so
            # I am breaking my code up like this so I can see what I am
            # doing a little bit better.
            requestedFile = message.split()[1]
            localFile = requestedFileToLocalFile(requestedFile)
            print 'Requested file:  ' + str(requestedFile)
            print 'Retrieving file: ' + str(localFile)

            # If we got a file that wasn't a valid local file,
            # then just act as if the file wasn't found.
            if localFile is None:
                raise IOError

            # Read the input data from the file.
            # This should automatically close the file if needed.
            # The file is being opened in binary mode, as all files
            # are "binary files" anyway.  The only thing special about
            # opening a file in text mode is how newlines are handled.
            with open(localFile, "rb") as f:
                outputdata = f.read()

            # Send the data in the file to the client.
            connectionSocket.send(outputdata)

        # We got here if the file wasn't found.  Create a "file not found" page.
        except IOError:

            errorMessage = "<h1>404 - File not found!</h1><br />"
            errorMessage += "Sorry about that.  It seems like your file doesn't exist. :(<br />"

            if random.choice([True, False]):
                errorMessage += "<br />To make up for it, here's a cat pushing a watermelon out of a lake.<br />"
                errorMessage += "<img src=\"cat_watermelon.jpg\" /><br />"
            else:
                errorMessage += "<img src=\"sadbrony.jpg\" /><br />"

            # Display an error message.
            connectionSocket.send(
                makePageWithTitle(
                    "404 Not found",
                    errorMessage
                    ))

        # Perform the cleanup here.
        finally:
            connectionSocket.close()
            print '-' * 40
            print ''

    # Okay, we're done!  Close the server socket.
    # This is just for completeness, we should never get here.
    serverSocket.close()

# Start the program.
main()
