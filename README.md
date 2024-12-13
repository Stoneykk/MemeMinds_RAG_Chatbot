# MemeMinds

You should first have the following:
1. MongoDB in your local environment
2. An OpenAI API key

To setup the environment, you should build the retrival database first,
Before that, you should put your OpenAI key in whereever it asks for.

You can run RetrivalDB.py to setup the retrival database automatically.
You should use wiki_raw.csv to set up the database described above, otherwise, the FAISS index will process for a very long time.

Then you should be able to run main.py in your terminal, and test the system.

