# django-events-management
This repository provides a simple Django application for managing events.

This fulfils the following user stories. As a User I can:
* Register using my email address & password
* Login using my email address & password
* Create an event, providing a title, description and date/time
* Modify an event if I am the organiser
* List the events, showing title, date/time, organiser email name, and number of attendees
* View a specific event, showing title, description, date/time and attendees list
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
* Customer Templating
* Lazy String Translation

Key performance features:
* Code has been written efficiently
* Optimised lazy-evaluated Query Sets

### Security
Key performance features:
* Each page checks that the user is authenticated and redirects to the login page if not
* Events can only be modified by the organiser
* No SQL has been written, instead relying on models for database interact to avoid potential SQL injection attack vectors
* Developed to run on the latest Django version

### Deployment
TBC

### Testing

CI Pipeline: https://gitlab.com/chrisBrookes93/django-events-management/-/pipelines

Models, Managers and Views have been heavily tested and code coverage is very high. This can be viewed using ```coverage```:
```bash
django_events_management\django_events>coverage run manage.py test
...
----------------------------------------------------------------------
Ran 49 tests in 5.214s

OK

django_events_management\django_events>coverage html
django_events_management\django_events>
```

## Improvements
* Make use of front-end JS (AJAX) to dynamically update content on pages
* Move to Jinja2 for templating for performance improvement
* Archive old events into a separate table/database for database optimisation
* Deploy static files to a CDN server for performance improvement
* Migrate from SQLite to MySQL/PostgreSQL for database scalability

