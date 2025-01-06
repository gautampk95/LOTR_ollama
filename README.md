# The Lord of the Rings Chatbot Powered by the Ollama LLM Model

The Lord of the Rings has garnered a massive fan base, both for its movies and its books. J.R.R. Tolkien's innovative fantasy world is nothing short of a masterpiece. However, the vast and intricate content of the books can make it challenging to quickly find answers about characters, events, or actions in the story. A chatbot offers an ideal solution to this challenge, providing instant access to the information fans seek. This chatbot application is built on the RAG (Retrieval-Augmented Generation) technique of GenAI.

Here, the chatbot is built using the `Llama 3.1` language model, specifically the 8-billion parameter variant (Llama 3.1: 8B), through the Ollama platform. The knowledge base encompasses the complete contents of all three books in the Lord of the Rings series. The text is first divided into smaller chunks, each paired with its corresponding vector embeddings. These embeddings are used to efficiently retrieve relevant chunks in response to a given query or question. The query and response interaction is seamlessly integrated into a Discord channel for streamlined communication.

The Discord channel supports these commands to interact with the Chatbot:

- **`/hello`**: The chatbot introduces itself and highlights its capabilities.
- **`/ask`**: Send a question or query to the chatbot, and it will provide a response based on the content you requested. The chatbot exclusively answers questions related to the Lord of the Rings book contents. If a query is irrelevant to the books, it responds with a prompt indicating the query is outside its scope.
- **`/private`**: A private chat thread is created in the channel to ensure the conversation remains confidential.
- **`/summarize`**: This command summarizes your last few chats with the chatbot. It is recommended to use it in a private chat thread to ensure only relevant information is included in the summary.

The Python files for these operations are available in the repository. Below are the steps to run your LOTR Discord chatbot powered by Ollama's Llama model 3.1.

## Steps to run the chatbot application on Discord

At first, you can pull, clone, or download the repository [LOTR_ollama](https://github.com/gautampk95/LOTR_ollama). This repository folder contains all the necessary Python script files and the knowledge base folder.

This Python application can be run locally using Visual Studio Code, Cursor, or any IDE of your choice. Alternatively, it can be deployed as a cloud instance (e.g., Amazon EC2). However, note that launching EC2 or other cloud instances may incur additional costs. For experimentation purposes, it is recommended to run the chatbot application locally.

If you prefer not to run the application in a Python virtual environment, you can skip this step. However, it is recommended to create a Python virtual environment first in the command terminal, as shown below:
```bash
# if you are using a Linux machine write 'python3' instead
python -m venv chat_bot   # chat_bot is the name of the virtual environment

# to activate the venv in windows environment
.\chat_bot\Scripts\activate

# to activate the venv in Linux environment
source ./chat_bot/bin/activate
```

Change the directory path to where Python scripts are located. Next, install the required libraries listed in the requirements text file, then pull and run Llama 3.1 (to test it):
```bash
pip install -r requirements.txt
ollama pull llama3.1
ollama run llama3.1
```

In the `.env` file enter the `DISCORD_BOT_TOKEN` and `CLIENT_ID`. To get and set these environment variables, follow these steps to set up and configure your Discord channel:
- Go to the Discord Developer Applications [website](https://discord.com/developers/applications) and create a new application with a name that reflects your application's purpose (e.g., LOTR ChatBot). Then, under Settings > Bot, click on "Reset Token" to generate your bot token. Store this token as `DISCORD_BOT_TOKEN` in your `.env` file.
- Enable "Server Members Intent" and "Message Content Intent" on the same Bot settings page. In the Bot Permissions section, enable "Send Messages" and any other permissions you wish to grant.
- Under Settings > OAuth2, copy the Client ID and store this as `CLIENT_ID` in your `.env` file.
- Create a redirect URI to add your bot to a Discord server (either create a new server or use an existing one). Use the following URL: https://discord.com/api/oauth2/authorize?&client_id=CLIENTID&scope=bot&permissions=8 . Replace CLIENTID with the Client ID from the Discord Developer Applications website for your bot application.
- Follow the instructions to select the Discord server where you want to add the bot, and authorize it to access the server.

After adding the bot to the server, you can start interacting with it in the Discord server channels using the commands provided earlier. To run the bot application, simply execute your Python script in your IDE's terminal, as shown below:
```bash
python app.py
```

The responses generated by the bot may not be perfect, but you'll notice interesting results and be able to evaluate the performance of the Llama model. You can also experiment with different language models to see varying outcomes. To do so, simply make changes in the `app.py` file. However, it's worth noting that the bot will not generate the same result consistently for the same query. The first time it runs, it takes some time to prepare the knowledge base chunks and save them in a pickle file for faster execution in subsequent runs.

## Note

As mentioned earlier, this bot can be launched to run 24/7 on a cloud instance. However, it is not free, and the free-tier Amazon EC2 instance (such as t2.micro) cannot handle Llama 3.1, as the model requires at least 8 GB of RAM. For local machine usage, it is recommended to run this application on a system with a minimum of 8 GB of RAM, with 16 GB being ideal for better performance.

The bot takes a few seconds to a few minutes to generate responses. Under ideal conditions, with higher memory, response times can be reduced to just a few seconds. Since my machine has 16 GB of RAM, the bot's performance is sufficient for experimentation purposes. Improvements can be made to enhance the bot's efficiency and speed.

The text files in the 'Knowledge_base_books' folder belong to their respective owners and are used solely for experimentation purposes.

## Screenshots of the Chatbot conversation

<p float="left">
  <img src="/chatbot_conv/intro.png" width="450" />
  <img src="/chatbot_conv/chatbot_channel_chats.png" width="450" />
</p>

<p float="left">
  <img src="/chatbot_conv/private_chat_1.png" width="300" />
  <img src="/chatbot_conv/private_chat_2.png" width="300" />
  <img src="/chatbot_conv/private_chat_3.png" width="300" />
</p>

