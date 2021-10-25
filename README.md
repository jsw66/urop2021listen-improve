# urop2021listen-improve
The repository for the UROP 2021 Summer project: Listen &amp; Improve web application

Instructions:

Once all files/folders are downloaded, the main file to run is called "webapp.py". During the project, all my files were inside a folder called "urop" so either creating a replica folder or a different named one, a simple ctrl+f can change the cwd. To run the webapp locally, simply run "webapp.py" in the command line.

To-do list/how things work:

1. The user authentication works for all cases e.g. when a user enters the wrong password whilst logging in, or tries to register with a username that's already in use. However, the flash messages have stopped appearing.

2. The way that user registration works is that there is a "users.csv" file inside the cwd and when a new user registers, their username, hashed password and personal information (about languages spoken etc.) are appended to the "users.csv" file. Upon registering (with a unique username), a file of "username_answers.csv" is also created in the cwd. This file has 2 column header: "question_id" and "answer". This is the file that will be updated whenever a user answers a question on the webapp. This is where the next step of the project lies: communicating between javascript and flask in order to append user performance data to the users csv file.

3. For uploading questions to the specific proficiency level web pages: if the questions are correctly labelled on the spreadsheet, simply re-running "scraper2.py" will update all the lists/dictionaries, which are then need to be copied manually into one line in the js file (I did this manually but it could be automated I think). There are only B1 and B2 questions at the moment, but the B1 and B2 web pages are fully operational and can be duplicated and small details changed to create C1 and C2.

4. Also related to uploading question data into javascript - for B1 proficiency, I have copied the python variable (designed to mimic a js array) into the js script in "B1.html", however, a better method is needed as there is a line character limit which is exceeded for "B2.html". So on the webapp only B1 loads the questions.
