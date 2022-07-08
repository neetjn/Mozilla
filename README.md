# Mozilla Take Home Coding Exercise

This project is a simple take home coding exercise provided by Mozilla. The goal is to create a web service capable of handling basic banking capabilities without any restriction on data storage or programming language.

## Breakdown

I leveraged the following tools to build this web service:

* **Python 3.8** : Given the position in question will be leveraging Python, I went ahead and used it for this exercise.
  * Pipenv for package management.
  * Peewee ORM
  * r2dto for data serialization.
  * Falcon for a RESTful framework.
  * gunicorn for an http server.
* **SQLite 3** : I used SQLite for it's simplicity, the peewee ORM can be reconfigured to hook into most conventional relational databases so I didn't see any reason to waste additional times provisioning my environment.

The exercise instructs this service should be able to handle requests at a commercial scale. Admittingly it's not my proudest work however my window was 3-4 hours and I wanted to make sure I had a scalable service in place.

## Approach

The instructions detail a rather unconventional approach where an account's unique identifier consists of it's name with the following parameters:

### Endpoints

POST /accounts
--
Request Body:
```json
{name: string}
```

GET /accounts/:name
--
Response Body:
```json
{name: string, balance: float}
```

POST /accounts/:name/deposit
---
Request Body:
```json
{amount: float}
```

POST /accounts/:name/withdraw
--
Request Body:
```json
{amount: float}
```

I've implemented these endpoints using the following design structure:

* Database Tables:
  * **Account**: Using uuid as primary key/unique identifier.
```sql
0|id|TEXT|1||1
1|name|VARCHAR(255)|1||0
2|balance|REAL|1||0
3|updated|INTEGER|0||0
4|created|INTEGER|1||0
5|is_deleted|INTEGER|1||0
6|deleted|INTEGER|0||0
```
  * **Transaction**: Using uuid as primary key/unique identifier.
```sql
0|id|TEXT|1||1
1|account_id|TEXT|1||0
2|type|VARCHAR(255)|1||0
3|amount|REAL|1||0
4|created|INTEGER|1||0
```
* RESTful architecture is quite straightforward. Endpoints have been split into designated resources as defined by the Falcon framework. I've created two separate resource modules for both accounts and transactions. The endpoints for deposits and withdrawals have been segmented into the transaction resources.
* The core functionality of the web service has been compiled into two separate "core" modules, following the philosophy of completely separating the core functionality from the http layer. This functionality should also be able to be tested without having to marionette an entire http server.
* The data tier is quite lackluster. I didn't have the time to build a bootstrapping mechanism for the database or stand up any tests to validate some performance targets. However, the data tier should be simple, any we could very easily add performance gains by using over the wire caching and memoization.
* Balances are stored as float values, however when transactions come in the amounts are processed as decimal values with 2pt precision. Excess change is factored away. Realistically, I'm not sure whether any financial instituions aggregate value beyond two decimal places however if this logic were preferred it would be easy to add a round-up mechanism.
* Transactions are provided in the form of withdrawals or deposits. The system has a built in maximum overdraft amount that will not allow accounts to degrade past a certain balance.

I admit this wasn't the cleanest approach, however I wanted to design a service that was easy to add onto and build over whether from the data layer or application layer.

## Setup

This project was created using Python 3.8 and pipenv. Pipenv can be installed with pip, from there a simple `pipenv install` and `pipenv shell` will get you started. Sqlite 3 must also be available on the host machine. This can be installed on most linux distributions using their respective package managers -- however an external database can very easily be configured if you'd like to use a dockerized version.

Environmental Constants:

* **MZ_HOST**: http server host.
* **MZ_PORT**: http server port.
* **MZ_WORKERS**: number of workers for the gunicorn http server.
* **MZ_DB_NAME**: sqlite database name.
* **MZ_MAX_OVERDRAFT**: maximum overdraft amount for account balances.

To start the http server enter the pipenv/virtualenv shell and use `python -m mozilla`. The database tables may need to be created first, to do this use `python -m mozilla --bootstrap=1`.

Once the http server is up and running web requests can be made to the specified endpoints above using via `http://{MZ_HOST}:{MZ_PORT}/{route}`.

## Retrospective

This exercise was a great brain teaser. I'm sure the greater aims of this exercise were to figure out how to deal with race conditions with an influx of transactions and how to properly maintain state. I've tried to address further solutions to these points in the following TODO:

* Add tests :(
* Complete the v2 api so we access/modify accounts by id not by name, by would by some generic object id or base64 encoded incremental.
* Over the wire caching and smart memoization (can use something like redis to get by multiple node issues w/ in mem cache).
* Use a message queue system to circumvent multiple modifier race conditions. The balance updated by transactions would be a speculative value. A secondary process / cron job would calculate the total balance at the end of a cycle after ingesting the message queue and properly update the user's REAL balance.
* Add ability to link accounts, transfer between accounts.
* Some sort of authentication layer.
* I noticed I check for an existing account by name when creating an account, this additional query can be stripped as I've made the name column a unique field.
* Dockersize the application for ease of use/deployment.
* HATEOS for service discovery, to ensure an end application can easily ingest the service with a root service description.
