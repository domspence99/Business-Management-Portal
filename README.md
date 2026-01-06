# Business Management Portal
#### Video Demo:  https://youtu.be/SP2SYflB8ww
#### Description:
This business management portal allows business administrators and authoritative users access to manage and views active,
previous and future jobs that are currently taking place within the business. This would mainly be aimed at small scale
business to track and manage the status of their jobs, that are securely stored inside an external database. This could
be useful for small businesses that are currently using a lesser secure system such as Excel files etc to manage their
jobs.


### Systems in place
1. Secure login system
Before a user can enter the portal, they must first register with a unique username and valid password. The system checks if the username already exists within the database and there is error handling if the username already exists. The password is then hashed and stored along with the username securely in an external database. The user can then log in using the credentials provided to register.
2. Secure external database with job information
Once the user has logged into their account, only their active jobs will be listed on the home page. If the user has not created any jobs yet, they can use the navigation bar or 'add a job' icon to begin adding a job to the system. The form used to add a job included various error handling methods so that the user must provide valid inputs into the form. Once the information is submitted via the post form, the variables are then retrieved within flask and stored in python variables. These python variables are then used as inputs to the external sqlite database. Once the user has added their jobs and they have been saved to the database, they are visible on the active jobs home page. This home page pulls all the job information from the specific users database and displays it in a clean and user-friendly manor using jinja templating to render the scrollable table. If the user would like to edit/view a specific job they can use the icons provided in the rows to go in and make any changes to current jobs. This allows users to go into already created jobs and re-save elements of the job as it progresses through its life-cycle. Likewise, if a job is no longer needed or required they can delete from the table - but this will also delete it from the database.


### Improvements over time
As there was a time constraint on my work I was unable to complete some features that were within my capabilities, these were:
- A search and filter system on the job list to filter out active/past/future jobs etc
- A personal profile section, to seperate certain jobs from certain users
- Edit the session keys from being stored locally to being stored within cookies

#### Why?
This portal provides a clean and efficient way for small scale business to view and manage their jobs or daily tasks. Each user can clearly see what they are expected to do and can edit their progress as jobs develop. This makes it a much more secure and efficient system than some of the standard procedures such as managing through excel spreadsheets etc - which can be easily hacked or lost.
