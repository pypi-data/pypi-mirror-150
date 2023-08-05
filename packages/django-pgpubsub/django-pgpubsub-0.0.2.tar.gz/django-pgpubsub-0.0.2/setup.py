# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgpubsub',
 'pgpubsub.management',
 'pgpubsub.management.commands',
 'pgpubsub.migrations',
 'pgpubsub.tests',
 'pgpubsub.tests.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-pgtrigger>=2.4.0', 'django>=2']

setup_kwargs = {
    'name': 'django-pgpubsub',
    'version': '0.0.2',
    'description': 'A distributed task processing framework for Django built on top of the Postgres NOTIFY/LISTEN protocol.',
    'long_description': 'django-pgpubsub\n===============\n\n``django-pgpubsub`` provides a framework for building an asynchronous\nand distributed message processing network on top of a Django application\nusing a PostgreSQL database. This is achieved by leveraging Postgres\'\n[LISTEN/NOTIFY](https://www.postgresql.org/docs/current/sql-notify.html)\nprotocol to build a message queue at the database layer.\nThe simple user-friendly interface,\nminimal infrastructural requirements and the ability to leverage Postgres\'\ntransactional behaviour to achieve exactly-once messaging, makes\n``django-pgpubsub`` a solid choice as a lightweight alternative to AMPQ\nmessaging services, such as\n[Celery](https://docs.celeryq.dev/en/stable/search.html?q=ampq)\n\n\nPrimary Authors\n---------------\n* [Paul Gilmartin](https://github.com/PaulGilmartin)\n* [Wesley Kendall](https://github.com/wesleykendall)\n\n\nHighlights\n==========\n\n- **Minimal Operational Infrastructure**: If you\'re already running a Django application\n  on top of a Postgres database, the installation of this library is the sum total\n  of the operational work required to implement a framework for a distributed\n  message processing framework. No additional servers or server configuration\n  is required.\n\n- **Integration with Postgres Triggers (via django-pgtrigger)**:\n  To quote the [official](https://www.postgresql.org/docs/current/sql-notify.html)\n  Postgres docs:\n\n  *"When NOTIFY is used to signal the occurrence of changes to a particular table,\n  a useful programming technique is to put the NOTIFY in a statement trigger that is triggered\n  by table updates.\n  In this way, notification happens automatically when the table is changed,\n  and the application programmer cannot accidentally forget to do it."*\n\n  By making use of the ``django-pgtrigger``\n  [library](https://pypi.org/project/django-pgtrigger/), ``django-pgpubsub``\n  offers a Django application layer abstraction of the trigger-notify Postgres\n  pattern. This allows developers to easily write python-callbacks which will\n  be invoked (asynchronously) whenever a custom ``django-pgtrigger`` is invoked.\n  Utilising a Postgres-trigger as the ground-zero for emitting a\n  message based on a database table event is far more robust than relying\n  on something at the application layer (for example, a ``post_save`` signal,\n  which could easily be missed if the ``bulk_create`` method was used).\n\n- **Lightweight Polling**: we make use of the Postgres ``LISTEN/NOTIFY``\n  protocol to have achieve notification polling which uses\n  [no CPU and no database transactions unless there is a message to read.](https://www.psycopg.org/docs/advanced.html#asynchronous-notifications)\n\n- **Exactly-once notification processing**: ``django-pgpubsub`` can be configured so\n  that notifications are processed exactly once. This is achieved by storing\n  a copy of each new notification in the database and mandating that a notification\n  processor must obtain a postgres lock on that message before processing it.\n  This allows us to have concurrent processes listening to the same message channel\n  with the guarantee that no two channels will act on the same notification. Moreover,\n  the use of Django\'s ``.select_for_update(skip_locked=True)`` method allows\n  concurrent listeners to continue processing incoming messages without waiting\n  for lock-release events from other listening processes.\n\n- **Durability and Recovery**: ``django-pgpubsub`` can be configured so that\n  notifications are stored in the database before they\'re sent to be processed.\n  This allows us to replay any notification which may have been missed by listening\n  processes, for example in the event a notification was sent whilst the listening\n  processes were down.\n\n- **Atomicity**: The Postgres ``NOTIFY`` protocol respects the atomicity\n  of the transaction in which it is invoked. The result of this is that\n  any notifications sent using ``django-pgpubsub`` will be sent if and only if\n  the transaction in which it sent is successfully committed to the database.\n\n\nLimitations\n===========\n\n- A database-based queue will not be capable of the same volume of throughput as a dedicated\n  AMPQ queue.\n\n- If a message is sent using Postgres\' ``NOTIFY`` and no process is listening at that time,\n  the message is lost forever. As explained in the **Durability and Recovery** section above,\n  pgpubsub can easily be configured so that we can replay "lost" messages, but this comes at the\n  performance penalty of inserting a row into a table before sending each notification. This is the same\n  penalty we must pay if we wish to have concurrent processes listening to the same channel without\n  duplicate notiifcation processing, as explained in the **Exactly-once notification processing** section above.\n\n\nAlternatives\n============\n\n- [Celery](https://docs.celeryq.dev/en/stable/search.html?q=ampq): The canonical distributed message processing library for django based applications. This can handle large volumes of throughput and is well tested in production.\n  It is however operationally quite heavy to maintain and set-up.\n\n- [Procrastinate](https://procrastinate.readthedocs.io/): This was a library we discovered whilst developing ``pgpubsub`` which also implements a distributed message processing library using the Postgres ``LISTEN/NOTIFY`` protocol. Whilst ``Procrastinate`` is well tested and offers several features which are not currently offered by ``pgpubsub``, we believe that the interface of ``pgpubsub`` coupled with the integration with django and Postgres triggers make our library a good alternative for certain use cases.\n\nQuick start\n===========\n\nPrerequisites\n-------------\n\nBefore using this library, you must be running Django 2.2 (or later) on top\nof a (single) PostgreSQL 9.4 (or later) database.\n\n\nInstalling\n----------\n\n    pip install django-pgpubsub\n\n``django-pgpubsub`` ships with a ``Notification`` model. This table must\nbe added to the app\'s database via the usual django ``migrate`` command.\n\nMinimal Example\n---------------\n\nLet\'s get a brief overview of how to use ``pgpubsub`` to asynchronously\ncreate a ``Post`` row whenever an ``Author`` row is inserted into the\ndatabase. For this example, our notifying event will come from a\npostgres trigger, but this is not a requirement for all notifying events.\nA more detailed version of this example, and an example which\ndoes not use a postgres trigger, can be found in the\n**Documentation (by Example)** section below.\n\n**Define a Channel**\n\nChannels are the medium through which we send notifications.\nWe define our channel in our app\'s ``channels.py`` file as a dataclass\nas follows:\n\n```python\nfrom pgpubsub.channels import TriggerChannel\n\n@dataclass\nclass AuthorTriggerChannel(TriggerChannel):\n    model = Author\n```\n\n**Define a Listener**\n\nA *listener* is the function which processes notifications sent through a channel.\nWe define our listener in our app\'s ``listeners.py`` file as follows:\n\n```python\nimport pgpubsub\n\nfrom .channels import AuthorTriggerChannel\n\n@pgpubsub.post_insert_listener(AuthorTriggerChannel)\ndef create_first_post_for_author(old: Author, new: Author):\n    print(f\'Creating first post for {new.name}\')\n    Post.objects.create(\n        author_id=new.pk,\n        content=\'Welcome! This is your first post\',\n        date=datetime.date.today(),\n    )\n```\n\nSince ``AuthorTriggerChannel`` is a trigger-based channel, we need\nto perform a ``migrate`` command after first defining the above listener\nso as to install the underlying trigger in the database.\n\n**Start Listening**\n\nTo have our listener function listen for notifications on the ``AuthorTriggerChannel``,\nwe use the ``listen`` management command:\n\n\n    ./manage.py listen\n\n\nNow whenever an ``Author`` is inserted into our database, our listener process creates\na ``Post`` object referencing that ``Author``:\n\nhttps://user-images.githubusercontent.com/18212082/165683416-b5cbeca1-ea94-4cd4-a5a1-81751e1b0feb.mov\n\n\nDocumentation (by Example)\n==========================\n\nIn this section we give a brief overview of how to use\n``pgpubsub`` to add asynchronous message processing functionality\nto an existing django application.\n\n\nOur Test Application\n--------------------\nSuppose we have the following basic django models (\na fully executable version of this example can be\nfound in ``pgpubsub.tests``):\n\n```python\n# models.py\nclass Author(models.Model):\n    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)\n    name = models.TextField()\n\n\nclass Post(models.Model):\n    content = models.TextField()\n    date = models.DateTimeField()\n    author = models.ForeignKey(\n        Author, null=True, on_delete=models.SET_NULL, related_name=\'entries\'\n    )\n```\n\nGiven these models, we\'ll describe the mechanics of using the ``pgpubsub`` library\nto achieve the following aims (which are for illustrative purposes only):\n\n* To asynchronously maintain a cache of how frequently ``Post`` objects are\n  read per day.\n\n* To define a postgres-trigger to ensure that, whenever an ``Author`` object is created, a ``Post`` object is\n  asynchronously created for that author with the title "Test Post".\n\n\nChannels\n---------\n\nChannels are the medium through which messages are sent.\nA channel is defined as a dataclass, where the dataclass fields define the accepted\nnotification payload. A channel must be declared in your app\'s ``channels.py`` file.\n\n\nFor our first example, the data required to update the aforementioned post-reads-per-day cache\nis a date and a ``Post`` id. This payload defines the fields of our first channel dataclass,\nthrough which notifications will be sent to update the post-reads-per-day cache:\n\n\n```python\n# channels.py\nimport datetime\n\nfrom pgpubsub.channels import Channel\n\n\n@dataclass\nclass PostReads(Channel):\n    model_id: int\n    date: datetime.date\n```\nNote the accepted dataclass field types for classes inheriting from\n``Channel`` are iterables (lists, tuples, dicts, sets) of:\n* python primitive types\n* (naive) datetime.date objects\n\n\nIn our second example we wish to have a channel through which\nnotifications sent whenever a postgres-trigger is invoked by the creation\nof an ``Author`` object. To achieve this, we define our channel like so (\nalso in our apps ``channels.py`` module):\n\n```python\nfrom pgpubsub.channels import TriggerChannel\n\n@dataclass\nclass AuthorTriggerChannel(TriggerChannel):\n    model = Author\n```\n\nNote that the key difference between this and the previous example is that\nthis channel inherits from ``TriggerChannel``, which defines the payload for\nall trigger-based notifications:\n\n```python\n@dataclass\nclass TriggerChannel(_Channel):\n    model = NotImplementedError\n    old: django.db.models.Model\n    new: django.db.models.Model\n```\n\nHere the ``old`` and ``new`` parameters are the (unsaved) versions of what the\ntrigger invoking instance looked like before and after the trigger was invoked.\nIn this example, ``old`` would refer to the state of our ``Author`` object\npre-creation (and would hence be ``None``) and ``new`` would refer to a copy of\nthe newly created ``Author`` instance. This payload is inspired by the ``OLD``\nand ``NEW`` values available in the postgres ``CREATE TRIGGER`` statement\n(https://www.postgresql.org/docs/9.1/sql-createtrigger.html). The only custom\nlogic we need to define on a trigger channel is the ``model`` class-level\nattribute.\n\n\nListeners\n--------\n\nIn the ``pgpubsub`` library, a *listener* is the function\nwhich processes notifications sent through some particular channel.\n\nA listener must be defined in our app\'s ``listeners.py`` file and must\nbe declared using one of the decorators in ``pgpubsub.listen.py``.\nThese decorators are also responsible for pointing a listener function\nto listen to a particular channel. When a function is associated to a channel\nin this way, we say that function "listening" to that channel.\n\nContinuing with the example whereby we maintain a cache of post reads,\nwe implement a listener function like so:\n\n```python\n# tests/listeners.py\nimport datetime\n\nimport pgpubsub\n\n# Simple cache for illustrative purposes only\npost_reads_per_date_cache = defaultdict(dict)\nauthor_reads_cache = dict()\n\n@pgpubsub.listener(PostReads)\ndef update_post_reads_per_date_cache(model_id: int, date: datetime.date):\n    print(f\'Processing update_post_reads_per_date with \'\n          f\'args {model_id}, {date}\')\n    print(f\'Cache before: {post_reads_per_date_cache}\')\n    current_count = post_reads_per_date_cache[date].get(model_id, 0)\n    post_reads_per_date_cache[date][model_id] = current_count + 1\n    print(f\'Cache after: {post_reads_per_date_cache}\')\n```\n\nA few notes on the above:\n\n* As we may expect, the channel we associate to a listener also\n  defines the signature of the listener function.\n* The notification payload is deserialized\n  in such a way that the input arguments to the listener function\n  have the same type as was declared on the ``PostReads`` channel.\n* It is possible to have multiple\n  listeners to a single channel and the signatures of those listeners\n  can vary by arguments declared as optional on their common channel -\n  see ``pgpubsub.tests.listeners.py`` for an example.\n\nNext we implement the listener which is used to asynchronously\ncreate a ``Post`` object whenever a new ``Author`` object is created.\nFor this listener, we can use the pre-defined ``post_insert_listener``\ndecorator:\n\n```python\n# tests/listeners.py\nimport pgpubsub\n\nfrom .channels import AuthorTriggerChannel\n\n\n@pgpubsub.post_insert_listener(AuthorTriggerChannel)\ndef create_first_post_for_author(old: Author, new: Author):\n    print(f\'Creating first post for {new.name}\')\n    Post.objects.create(\n        author_id=new.pk,\n        content=\'Welcome! This is your first post\',\n        date=datetime.date.today(),\n    )\n```\n\nAny listener associated to a trigger-based channel (one inheriting from\n``TriggerChannel``) necessarily has a signature consisting of the ``old``\nand ``new`` payload described in the previous section. Note that\ndeclaring a trigger-based listener in the manner above *actually\nwrites a postgres-trigger to our database*. This is achieved by\nleveraging the ``django-pgtrigger`` library to write a pg-trigger\nwhich will send a payload using the postgres ``NOTIFY`` command\nwhenever an ``Author`` object is inserted into the database. Note that\nas with all triggers defined using ``django-pgtrigger``, this trigger\nis first written to the database after a migration.\n\nFinally, we must also ensure that this ``listeners.py`` module is imported\ninto the app\'s config class (similar to how one would use django signals):\n\n```python\n# tests/apps.py\n\nclass TestsConfig(AppConfig):\n    name = \'tests\'\n\n    def ready(self):\n        import tests.listeners\n```\n\nListening\n---------\n\nTo have our listener functions "listen" for\nincoming notifications on their associated channel, we can make use\nof the ``listen`` management command provided by the ``pgpubsub`` library:\n\n    ./manage.py listen\n\nWhen a process started in this manner encounters an exception, ``pgpubsub``\nwill automatically spins up a secondary process to continue listening before the\nexception ends the initial process. This means that we do not have to worry about\nrestarting our listening processes any time a listener incurs a python level exception.\n\nThe ``listen`` command accepts two optional arguments:\n\n* ``--channels``: a space separated list of the\n  full module paths of the channels we wish to listen to.\n  When no value is supplied, we default to listening to all registered channels\n  in our project. For example,\n  we can use the following command to listen to notifications coming through\n  the ``PostReads`` channel only:\n\n\n    ./manage.py listen --channels \'pgpubsub.tests.channels.PostReads\'\n\n\n* ``--processes``: an integer which denotes the number of concurrent processes\n  we wish to dedicate to listening to the specified channels. When no value is\n  supplied, we default to using a single process. Note that if multiple processes\n  are listening to the same channel then by default both processes will act on\n  each notification. To prevent this and have each notification be acted upon\n  by exactly one listening process, we need to add ``lock_notifications = True``\n  to our channel. See the "Lockable Notifications and Exactly-Once Messaging"\n  section below for more.\n\n\nNotifications\n-------------\n\nWith our listener\'s listening on our channels, all that remains is to define where\nour notifications are sent from.\n\nFor our first example, we need to send a notification through the ``PostReads`` channel\nwhenever a ``Post`` object is read. To achieve this, we can make use of the\n``pgpubsub.notify.notify`` function. In our example, we create a ``fetch`` classmethod\non the ``Post`` model which is used to retrieve a ``Post`` instance from the database\nand also send a notification via the ``PostReads`` channel to asynchronously invoke the\n``update_post_reads_per_date_cache`` listener. This `fetch` method could then\nof course be utilised in whatever API call is used when a user reads a post:\n\n```python\n# tests/models.py\nimport pgpubsub\n\nclass Post(models.Model):\n    ...\n    @classmethod\n    def fetch(cls, post_id):\n        post = cls.objects.get(pk=post_id)\n        pgpubsub.notify(\n            \'pgpubsub.tests.channels.PostReads\',\n            model_id=post_id,\n            date=datetime.date.today(),\n        )\n        return post\n```\n\n\nA few notes on the above implementation:\n\n* Under the hood, this python function is making use of the postgres\n  ``NOTIFY`` command to send the payload as a JSON object.\n* The first argument to the `notify` function can either be the full module\n  path of a channel or the channel class itself. The following keyword\n  arguments should match the dataclass fields of the channel we\'re notifying\n  (up to optional kwargs).\n* Using ``pgpubsub.notify.notify`` is the appropriate choice for any non-postgres trigger\n  based notification.\n\n\nFor trigger based channels, notifications are sent purely at the database\nlayer whenever the corresponding trigger is invoked. To understand this in a bit\nmore detail, let\'s consider our example above:\n\n```python\n@pgpubsub.post_insert_listener(AuthorTriggerChannel)\ndef create_first_post_for_author(old: Author, new: Author):\n    print(f\'Creating first post for {new.name}\')\n    Post.objects.create(\n        author_id=new.pk,\n        content=\'Welcome! This is your first post\',\n        date=datetime.date.today(),\n    )\n```\n\nAs explained above, if we write this function and perform a migration\n, the ``post_insert_listener`` decorator ensures that a trigger function\nis written to the database. Then, after any ``Author`` row is inserted to the\ndatabase, the ``post_insert_listener`` also ensures that that database-level trigger\nfunction is invoked, firing a notification with a JSON payload consisting\nof the ``OLD`` and ``NEW`` values of the ``Author`` instance before and after the\nits creation. Associating the channel like so\n\n```python\npost_insert_listener(AuthorTriggerChannel)\n```\n\n\nensures that the notification is sent via the ``AuthorTriggerChannel`` and hence ends up being\nprocessed by the ``create_first_post_for_author`` listener. To examine the internals of the trigger functions used to send notifications at the database level,\nsee ``pgpubsub.triggers.py``.\n\nNote that postgres ensures that notifications sent via ``NOTIFY`` are only sent *after* the commit which\ncreated them is committed, we can be sure that in our example our newly\ncreated ``Author`` will be safely in the database before the listener process attempts to\nassociate a ``Post`` to it.\n\n\nLockable Notifications and Exactly-Once Messaging\n-------------------------------------------------\n\nIn the default implementation of the Postgres ``LISTEN/NOTIFY`` protocol,\nmultiple processes listening to the same channel will result in each process acting upon\neach notification sent through that channel. This behaviour is often undesirable, so\n``pgpubsub`` offers users the option to define channels which allow one, and only one,\nlistening process to act upon each notification. We can achieve this simply by defining\n``lock_notifications=True`` on our channel object. This is the desired notification\nprocessing behaviour for our ``AuthorTriggerChannel``, where we want to create exactly one\n``Post`` whenever an ``Author`` row is inserted:\n\n```python\nfrom pgpubsub.channels import TriggerChannel\n\n@dataclass\nclass AuthorTriggerChannel(TriggerChannel):\n    model = Author\n    lock_notifications = True\n```\n\nEnabling ``lock_notifications`` on a channel has the following effect:\n\n1. Whenever a notification is sent through that channel\n   (either via the ``pgpubsub.notify`` function or the ``pgpubsub.triggers.Notify`` trigger),\n   a ``pgpubsub.models.Notification`` object is inserted into the database. This stored notification\n   contains the same JSON payload as the transient Postgres notification. Note that\n   since Postgres notify events are atomic with respect to their transaction, the notification\n   is sent if and only if a ``Notification`` is stored.\n2. When a process listening to that channel detects an incoming Postgres notification,\n   it fetches and *obtains a lock upon* any stored ``Notification`` object with the same\n   payload. This is achieved as follows:\n\n    ```python\n\n        notification = (\n                Notification.objects.select_for_update(\n                        skip_locked=True).filter(\n                            channel=self.notification.channel,\n                            payload=self.notification.payload,\n                    ).first()\n                )\n    ```\n\n    The fact that ``select_for_update`` in the above applies a lock on ``notification``\n    ensures that no other process listening to the same channel can retrieve this notification\n    object. Moreover, the use of ``skip_locked=True`` means that any process which\n    cannot obtain the lock does not wait for the lock to release. This allows other processes\n    to freely skip this notification and poll for others, whilst the one which\n    did obtain the lock continues carries on to pass its notification into the\n    listener callback. If the callback then successfully completes, the stored\n    ``Notification`` is removed from the database.\n\n\nRecovery\n------------\n\nIn the default implementation of the Postgres ``LISTEN/NOTIFY`` protocol, if a notification\nis sent via a channel and no process is listening on that channel at that time, the\nnotification is lost forever. As described in the previous section,\nenabling ``lock_notifications`` on our channel means we store a ``Notification`` object\nin the database. Thus, if we happen to "lose" a notification on such a channel in the\naforementioned way (e.g. if all of our listener processes were down when a notification was sent), we still have a stored copy\nof the payload in our database.\n\n``pgpubsub`` provides a function ``pgpubsub.process_stored_notifications`` which fetches\nall stored ``Notifications`` from the database and sends them to their respective channels\nto be processed. This allows to recover from scenarios like the one in the paragraph described\nabove.\n\n\nLive Demos\n==========\n\n`bulk_create` over several processes\n------------------------------------\n\nIn the below example we show how `pgpubsub` handles a bulk creation\nof ``Author`` objects when several processes are listening to the\n``AuthorTriggerChannel`` channel. For the sake of the below demonstration,\nwe added a `time.sleep(3)` statement into the `create_first_post_for_author`\nlistener function. Note how only one processes is able to process any given\nnotification:\n\nhttps://user-images.githubusercontent.com/18212082/165823588-df91e84a-47f2-4220-8999-8556665e3de3.mov\n',
    'author': 'Opus 10 Engineering',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Opus10/django-pgpubsub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4',
}


setup(**setup_kwargs)
