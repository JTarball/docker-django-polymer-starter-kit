<a href="http://www.djangoproject.com/" >
	<img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" />
</a>

## 'tests' App

An app for the sole purpose of aiding testing

How to add test models for testing only
=======================================

You should only include this in your test settings ONLY:

INSTALLED_APPS += (
    ...
    'tests',
)

You can then 'migrate' as normal - the models will be included