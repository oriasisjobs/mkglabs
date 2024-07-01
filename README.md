This is a chat app.
To improve user experience, I added username logic - 
Clients send a username upon connecting.
Server stores and uses these usernames for message identification, and send them with the messages.

Demo:
There is a zip file containig a demo video, and 5 images that illustrate the server and clients. feel free to watch :)

Presp:
Go to constants file, and put the openai API key (git do not allow to push it so I must have hide it)
if you did not isntall openai, please install it:
pip install openai==0.28.0

Run Server:
Navigate to project root folder, and run:
python chat_server.py

Run Clients:
Navigate to project root folder, and run:
python char_client.py

you can run several clients. For each, you can send messages, that the server will get, and send to all other connected clients.

Run AI Clients:
Navigate to project root folder, and run:
python char_AI_client.py
