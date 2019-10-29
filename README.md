# Project 1
Consists of 4 files: requirements.txt file which indicates which python packages are required, import.py which allows the user to import the book.csv file into an empty books database, books.csv which is a list of 5000 books including title, author, isbn, and year published, as well as the application.py file which is the main python flask application. In addition, there are 2 folders, that go along with the application: templates which includes all the html files to format and dispaly the website as well as static which includes the css and image files needed for the application.

# import.py
Imports each row from books.csv that includes the isbn, title, author, and year published for 5000 books into the books table.

# application.py
File run within flask to start the python application. Includes routes to the following functions and app routes for redirecting user the correct pages: login() Get method which displays login template where they can enter username and password or go to the registration page. login() Post method checks username and password entered and if successful, user is taken to the book search page, but if they enter invalid data the user is taken to the errorLogin template. registration() Get method displays registration template. registration() Post method is where the user adds a username, password, first and last name to register an account. If successful, successLogin template is rendered. If bad data is entered, errorUser template is rendered.   viewUserInfo() Get method renders the viewUserInfo template for the session user, including userid, username, first name, and last name and allows the user to update their password or other user info or go to search for books. updateUser() Get method displays the updateUser template where user can update their first and last names or choose to update their password via the updatePswd page or go back to the viewUserInfo template. updateUser() Post method checks for valid entries and If user updates are successful, user is taken to the successUpdate page and if an error occurs, the user is taken to the errorUser page. updatePswd() Get method displays the updatePswd template for user to enter their old password as well as a new password and confirmation of that password. updatePswd() Post method checks the existing password, as well as ensures the new password equals the confirmation  password. If checks all pass, then renders the successUser template. Otherwise, renders the errorUser template. searchBooks() Get method renders serachBooks template and allows the user to enter any combination of isbn, title, or author data to find books based on search criteria. searchBooks() Post method, check if a match is not found, the errorBooks template is rendered. If a match is found, the findBooks template is rendered. findBooks() Post method renders the findBooks template where the user sees a list of mathing books that they can choose from. The user choice is then used to display information on the selected book via the viewUserBook template, including reviews by users of the website and ratings data from goodreads.com api call. reviewBook(book_id) Get method checks to see if the user has already reviewed the book_id and if so, then errorBook temlate is rendered. Otherwise, review template is rendered. review(book_id) Post method checks the user entered rating and comments and inserts them into the db. If successful, renders successReview template. Otherwise, renders errorBook template. logout() Get method clears the session data and logs the user out, rendering the successLougout template. excitingreads_api(book_isbn) method finds the book matching the isbn sent. If found, calls the goodreads.com api to get the book ratings and returns the book info as well as the goodreads count and rating data in the specified json format. If not found, returns and error message and code in the specified json format.

# layout.html
Template for all pages to display. Sets up title and links for html head. Sets up layout for html body, including card for image in upper left corner of page and block card in uppder right corner of page, plus h1 heading for page headins, h2 block heading placeholder, and container block card placeholder for page content. Pages that extend this template will add block heading and block card as needed. Users static files (linked to static folder) for css and image.

# login.html
Template for user login. Displays input field for username and masked password as well as a login button to submit entries and a link to the registration page for users that do not have a username yet. Extends layout.html with block heading.

# errorLogin.html
Template for error related to logging in or registration. Extends layout.html and takes error messages as input. Displays button to go back to the login screen and link to the registration screen.

# registration.html
Template for user registration. Displays input fields for first name, last name, username, and masked password as well as a register button to submit entries and a link to the login page for users that are already registered. Extends layout.html with block heading.

# successLogin.html
Template for successful user registration. Extends layout.html. Displays button to go back to login page.

# viewUserInfo.html
Template for viewing user information. Displays the userid and username, user's first and last name as well as. Also dislays button for updating password, updating other user info, and to go to the search books page. Extends layout.html with block heading and adds logout button to block card.

# updateUser.html
Template for updating user information. Displays the username as readonly as well as the first and last names. User can enter update to first or last name and submit using Update button. Also includes button to view and display the password as well as a link to go back to the view user info page. Extends layout.html with block heading and adds logout button to block card.

# updatePswd.html
Template for updating user password. Displays the username as readonly as well as a field to enter the old password, new password, and one to confirm the new password, all masked from viewer. Includes a button to submit password data. Also includes link to go back to the view user info page. Extends layout.html with block heading and adds logout button to block card.

# errorUser.html
Template for error related to user entries in update screens. Extends layout.html and takes error messages as input as well as adds logout button to block card. Displays button to go back to the user info screen and link to the search books screen.

# successUpdate.html
Template for success related to user entries in update screens. Extends layout.html, takes message as input and adds logout button to block card. Displays button to go back to the user info screen and link to the search books screen. 

# searchBooks.html
Template for entering either ISBN, title, or author to find a book. Includes a button to submit search criteria. Extends layout.html with block heading and adds user info as well as logout buttons to block card.

# errorBooks.html
Template for error related to book entries in book search and review screens. Extends layout.html and takes error messages as input as well as adds logout button to block card. Displays button to go back to the search books screen.

# findBooks.html
Template for showing books that match search criteria in a list with radio buttons for selection. Includes a button to submit selection. Extends layout.html with block heading and adds user info as well as logout buttons to block card.

# viewBookInfo.html
Template for showing book information on selected book, broken into 3 sections: first for Book Info with header and data, second for Review Info with header and data, and third for Goodreads.com Info with image, header, and data. Includes ISBN, title, author, and year published in first section. Displays any user reviews found, including user name, rating, and comment in second section. Dipslays goodreads.com review data, including goodreads.com average rating based on a scale of 5 and review count. Includes a button to submit user review as well as another to go back to the search books page. Extends layout.html with block heading and adds user info as well as user info and logout buttons to block card.

# review.html
Template for selecting rating (1-5) and entering comments for uesr review. Includes a button to submit user input as well as another to go back to the search books page. Extends layout.html with block heading and adds user info as well as user info and logout buttons to block card.

# successReview.html
Template for success related to review entries in review screen. Extends layout.html, takes message as input and adds logout button to block card. Displays button to go back to the user info screen and link to the search books screen. Extends layout.html with block heading and adds user info as well as user info and logout buttons to block card.

# successLogout.html
Template for success related to logging out. Extends layout.html and takes message as input. Displays button to go back to the login screen. 