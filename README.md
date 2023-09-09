# django-simplesshkey

This is a fork of https://github.com/gwuniversity/django-simplesshkey


## Installation
1. Installation with `pipenv`: 
  - `pipenv install -e git+https://github.com/Maki-IT/django-simplesshkey@master#egg=django-simplesshkey`
2. Alternative/manual installation: 
  - Clone or copy the directory `simplesshkey` of this repository to your project's root (where other apps are located as well)
3. Add `simplesshkey` to the `INSTALLED_APPS` list in your project's `settings.py`.
4. Also in `settings.py` set the following variables:
   See [settings](#settings) bellow
  ``` python
  SSHKEY_ALLOW_EDIT = <True/False>
  SSHKEY_DEFAULT_HASH = '<sha256/md5/legacy>
  AUTH_USER_MODEL = "<app.model>"  # Set this, if you use a custom user model 
  ```
5. Map the URLs into your project. See [url configuration](#url-configuration) below
6. Make migrations `python manage.py makemigrations`
7. Apply migrations `python manage.py migrate`
8. See [templates](#templates) for example templates

## Original

django-simplesshkey allows you to associate multiple SSH public keys with Django
user accounts.  It provides views to list, add, edit, and delete keys, each of
which is intended for end-user consumption.  Of course, you can also manage SSH keys
from the administration interface.

SSH keys are simply stored in the Django database, and what you do with them is
up to you: you can have a cron job that regularly dumps SSH keys to files, or
connect a signal to take an action each time a SSH key is saved...
For instance, the author `uses Ansible to deploy the SSH keys to several machines
<https://framagit.org/compile-farm/gccfarm>`_.


## About django-sshkey and django-simplesshkey

`django-simplesshkey` is a fork of django-sshkey_, based on version 2.5.0.

The goal of this fork is twofolds:

* Keep only basic functionalities needed to manage SSH keys linked to Django
  users.  In particular, the optional integration with OpenSSH has been
  completely removed, which simplifies configuration and avoids leaking
  information by default (public lookup view).  Also, sending emails when
  keys are added or modified is no longer done, because it can easily be
  implemented outside of this application.

* Be more flexible: impose less constraints on the model (no unicity),
  allow to override some fields of the model or form.  Also, sending emails
  outside of this application obviously allows more flexibility.

Of course, if you need all the extra features of django-sshkey, you should
continue using it!


## URL Configuration

Added ``rawkeys\<username>`` URL to get public keys associated with a given user

This text assumes that your project's ``urls.py`` maps ``simplesshkey.urls``
into the URL namespace as follows::

```
  urlpatterns = [
  ...
    re_path('^sshkey/', include('simplesshkey.urls')),
    ...
  ]
```

You will need to adjust your URLs in the examples below if you use a different
mapping.


## Settings

``SSHKEY_ALLOW_EDIT``
  Boolean, defaults to ``False``.  Whether or not editing keys is allowed.

``SSHKEY_DEFAULT_HASH``
  String, either ``sha256``, ``md5``, or ``legacy`` (the default).  The default
  hash algorithm to use for calculating the fingerprint of keys.  The resulting
  hash is stored in the ``fingerprint`` field of each SSH key object.
  Legacy behavior enforces OpenSSH's pre-6.8 behavior of MD5 without the ``MD5:``
  prefix.


## Templates

Example templates are available in the [templates.example](simplesshkey/templates.example/sshkey) directory.

``sshkey/userkey_list.html``
  Used when listing a user's keys.

``sshkey/userkey_detail.html``
  Used when adding or editing a user's keys.


## Management commands

- ``import_sshkey [--auto-resolve] [--prefix PREFIX] [--name NAME] USERNAME KEY_PATH ...``

  Imports SSH public keys to tie to a user. If ``--auto-resolve/-a`` are given,
  attempt to generate unique key names using a UUID. The prefix used during
  this process is the key name, but can be changed using ``--prefix/-p``.

- ``normalize_sshkeys [USERNAME KEY_NAME]``

  Recalculates key data to reflect a changed setting, for instance, if you have
  changed ``SSHKEY_DEFAULT_HASH`` and some keys have incorrect fingerprints in
  your database. Given no arguments, all keys will be normalized. The username
  asnd key name are optional, and if specified, will limit affected keys to
  those owned by a user, or a particular key of a user.  This can also be done
  via the administration panel, but if you have a large key database the
  request could end up timing out.


.. _django-sshkey: https://github.com/ClemsonSoCUnix/django-sshkey
