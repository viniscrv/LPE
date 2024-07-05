### Summary

This is the back-end of a project developed using `Django Rest Framework`. The project's goal is to serve as a manager and analyzer for the execution of activities and habits.

The motivation behind the project is to have a quantitative control over how much effort you are putting into maintaining a certain habit. Studies show that the more you push yourself to perform an activity beyond your limit, the more likely you are to stop doing it. Therefore, it is important to focus on gradual improvement and slow down when necessary. For example, when starting the habit of reading, it is important not to start by reading a book a day but to gradually increase the number of pages per day.

With this in mind, the web app was created to log activities performed throughout the days and their respective perceived effort. With this data, the program generates statistics for better understanding.

The project includes statistical logic, calculating best and worst results, tracking pending activities per day, paginated history, and more.

With the goal of leveraging the framework's resources, the project utilizes Django admin tools, partially uses the User resources for Profile modeling, and implements authentication with django-simplejwt.


### To run the project

1. clone the project

2. start a python virtual environment 

3. ```pip install -r requirements.txt```

4. ```python manage.py migrate```

5. ```python manage.py runsever```


### User inteface

https://github.com/viniscrv/LPE-UI
