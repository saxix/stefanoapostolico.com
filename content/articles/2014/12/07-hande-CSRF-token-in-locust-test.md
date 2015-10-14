Title: Handle CSRF token in Locust test
Date: 2014-12-07
Category: tech
Tags: locust, performance, django
Status: published

Locust and Django CSRF

<!-- PELICAN_END_SUMMARY -->

Simple solution to handle Django 
[Cross Site Request Forgery protection](https://docs.djangoproject.com/en/dev/ref/csrf/)
into [Locust](http://locust.io/) load tests

```python

class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        response = self.client.get("/auth/login/")
        csrftoken = response.cookies['csrftoken']
        response = self.client.post("/auth/login/", 
                                    {"username": "admin",
                                     "password": "password"},
                                    headers={"X-CSRFToken": csrftoken})
 
          
class WebsiteUser(HttpLocust):
    host = 'http://localhost:8000'
    task_set = UserBehavior
 
```