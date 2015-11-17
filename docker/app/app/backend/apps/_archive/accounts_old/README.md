<a href="http://www.djangoproject.com/" >
	<img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" />
</a>

## 'accounts' App

An 'accounts' app which stores user informtation and controls registration

- The accounts deals with everything to do with front-end users include registration / activation / admin / user preferences.

The 'accounts' app is actually divided into two apps:

	registration   --- deals with user registration & activation
	backend        --- user preferences / account profiles / definition of accounts Model (User -- settings.AUTH_USER_MODEL) / front-end backend (admin page)



The normal django admin is considered for maintenance (super admin) use only and shouldn't be visible to users.
