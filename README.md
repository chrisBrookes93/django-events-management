# django-events-management
This repository contains a simple Django application for managing events.

This fulfils the following user stories. 

As a User I can:
* Register using my email address & password
* Login using my email address & password
* Create an event, providing a title, description & date/time
* Modify an event if I am the organiser
* List the events, showing title, date/time, organiser email name, & number of attendees
* View a specific event, showing title, description, date/time & attendees list
* View a list of events sorted so that upcoming are first

Other non-functional requirements:
* Server must be able to handle multiple thousand events, users and attendees

## Django Apps
* Users - For user management
* Events - For event management

### Endpoints
| URI | Description |
| --- | --- |
| / | Root of the application |
| /admin | Admin Panel |
| /users/register | Register as a new User |
| /users/login | Login | 
| /users/logout | Logout |
| /events | List events |
| /events/<id> | View a specific event |
| /events/edit/[id] | Edit an event |
| /events/create | Create an event |
| /events/attend_event/[id] | Mark attendance |
| /events/unattend_event/[id] | Mark un-attendance |

## Key Considerations

### Performance
As this is a prototype and is only required to handle requests in the thousands, the following has not yet been implemented:
* External DB Server
* Caching Server
* Custom Templating
* Lazy String Translation

Key performance features:
* Code has been written efficiently
* Optimised lazy-evaluated QuerySets

### Security
Key security features:
* Each page checks that the user is authenticated
* Events can only be modified by the organiser
* No SQL has been written, instead relying on Models for database interaction to avoid potential SQL injection attack vectors
* Developed to run on the latest Django/Python/NGINX versions
* Redirect to SSL is enabled
* CSRF Token or Session Cookie will not be served over HTTP
* Referrer Policy projects the users' privacy

### Development
Should you wish to use this application in a development context, you will need to set the following environment variables:
* DEBUG=1
* SECRET_KEY=[key]

Without these, ``python manage.py runserver`` and ``python manage.py test`` will not work.
### Deployment
This application can be deployed easily using ```docker-compose```.

```bash
~$ mkdir django_evt
~$ cd django_evt
~/django_evt$ git clone https://github.com/chrisBrookes93/django-events-management.git .
~/django_evt$ sudo docker-compose up --build
```

#### Deployment Checklist:
* Checkout repository
* Generate certificates and place in ``/django_events/config/nginx/certs`` (example self-signed ones provided)
* Set correct values for your environment variables in ``/config/web/web-variables.env``
* Navigate to: https://0.0.0.0:443/admin. Login with the default admin and **change the password**:
    * Default Email: *admin@events.com*
    * Default Password: *EventsEvents*
* Access the main site via: https://0.0.0.0:443


### Testing

GitLab CI Pipeline: https://gitlab.com/chrisBrookes93/django-events-management/-/pipelines

Models, Managers and Views have been heavily tested and code coverage is very high. This can be viewed using ```coverage```:
```bash
django_events_management\django_events>coverage run manage.py test
...
----------------------------------------------------------------------
Ran 49 tests in 5.214s

OK

django_events_management\django_events>coverage report
Name                                   Stmts   Miss  Cover
----------------------------------------------------------
django_events_management\settings.py      23      0   100%
django_events_management\urls.py           4      0   100%
django_events_management\views.py          5      0   100%
events\admin.py                            6      0   100%
events\models.py                          27      1    96%
events\urls.py                             3      0   100%
events\views.py                           87      0   100%
users\admin.py                            14      0   100%
users\forms.py                             6      0   100%
users\managers.py                         16      1    94%
users\models.py                           13      0   100%
users\urls.py                              4      0   100%
users\views.py                            16      0   100%
----------------------------------------------------------
TOTAL                                    224      2    99%

django_events_management\django_events>
```

## Improvements
* Make use of front-end JS (AJAX) to dynamically update content on pages
* Move to Jinja2 for templating for performance improvement
* Archive old events into a separate table/database for database optimisation
* Deploy static files to a CDN server for performance improvement
* Migrate from SQLite to MySQL/PostgreSQL for database scalability
* Use a caching server
* Improve exception handling & logging
