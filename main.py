from googlesearch import search

# Get the query to search for.

query = input("Main theme of the companies to hunt:\n")

# Go through all the links from the google search and print them.

for i in search(query, tld="de", num = 30, stop = 30, pause = 2):
    print(i)
