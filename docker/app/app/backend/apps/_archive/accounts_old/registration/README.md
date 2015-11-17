README.md


How is a user authenticated via a backend

 Behind the scenes, Django maintains a list of “authentication backends” that it checks for authentication. When somebody calls django.contrib.auth.authenticate() – as described in How to log a user in above – Django tries authenticating across all of its authentication backends. If the first authentication method fails, Django tries the second one, and so on, until all backends have been attempted.


AUTHENICATION_BACKENDS settings 
default: ('django.contrib.auth.backends.ModelBackend',)

If a backend raises a PermissionDenied exception, authentication will immediately fail. Django won’t check the backends that follow.

