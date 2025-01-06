# The Lord of the Rings Chatbot Powered by the Ollama LLM Model

The Lord of the Rings has garnered a massive fan base, both for its movies and its books. J.R.R. Tolkien's innovative fantasy world is nothing short of a masterpiece. However, the vast and intricate content of the books can make it challenging to quickly find answers about characters, events, or actions in the story. A chatbot offers an ideal solution to this challenge, providing instant access to the information fans seek. This chatbot application is built on the RAG (Retrieval-Augmented Generation) technique of GenAI.

Here, the chatbot is built using the `Llama 3.1` language model, specifically the 8-billion parameter variant (Llama 3.1: 8B), through the Ollama platform. The knowledge base encompasses the complete contents of all three books in the Lord of the Rings series. The text is first divided into smaller chunks, each paired with its corresponding vector embeddings. These embeddings are used to efficiently retrieve relevant chunks in response to a given query or question. The query and response interaction is seamlessly integrated into a Discord channel for streamlined communication.

The Discord channel supports these commands:

- **/hello**: The chatbot introduces itself and highlights its capabilities.
- **/ask**: Send a question or query to the chatbot, and it will provide a response based on the content you requested. The chatbot exclusively answers questions related to the Lord of the Rings book contents. If a query is irrelevant to the books, it responds with a prompt indicating the query is outside its scope.
- **/private**: A private chat thread is created in the channel to ensure the conversation remains confidential.
- **/summarize**: This command summarizes your last few chats with the chatbot. It is recommended to use it in a private chat thread to ensure only relevant information is included in the summary.

The Python files for these operations are available in the repository. Below are the steps to run your LOTR Discord chatbot powered by Ollama's Llama model 3.1.
