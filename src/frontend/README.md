# Frontend Developer's Readme


## Developer's Tools

Since web browsers have a wide attack surface they have many many security restrictions.
The [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Same_origin_policy_for_JavaScript) is one major limitation that needs to be respected.
Browsers tend to be even more restrictive when running locally: that is, when the URL starts with "file://" instead of "http://", more rules kick in;
 Now, something (???) about these rules blocks OpenLayers from working locally in Firefox (and IE? and Opera??), but not in Chrome.
Thus in order to do any proper debugging you must launch an **http server** (and, as the project develops, you'll need one anyway).
 In the long run, we will eventually have to support running on 'heavy' **servers** like
 Apache,
 nginx,
 or lighttpd,
 but in the meantime there's
 [Twisted's server](http://twistedmatrix.com/trac/wiki/TwistedWeb),
 [Ruby on Rails' server](http://www.ruby-doc.org/stdlib-1.9.3/libdoc/webrick/rdoc/index.html),
 [django's server](https://docs.djangoproject.com/en/dev/ref/django-admin/#runserver-port-or-address-port).
On linux, [thttpd]() and [webfs](http://linux.bytesex.org/misc/webfs.html) are very viable options ("cd frontend; webfsd -d . & firefox localhost:8000" will get you up and hacking)
or you could consider [Spawning](https://pypi.python.org/pypi/Spawning), [Gunicorn](http://gunicorn.org/), [Cherokee](http://cherokee-project.com/)
((**TODO**: pick a server, write batch files to start it on each of the three OSes.))

It behooves you to have a web **developer console** open. Chrome and Firefox have built-in inspectors accessible with ctrl-shift-i,
Firefox has the option of installing the Firebug extension which is
 a) older b) better than the built in inspector.

For certain in-depth debugging scenarios like **tracking the flow of call-response** with all the headers and contents
you might need to investigate [Fiddler](http://fiddler2.com/) which 
h


## Compatibility

Since this is a web app, it needs to be tested in all browsers on all platforms.
Since that's not a realistic goal, especially not at this stage and with this size of team,
we should at least cover:
Firefox on Windows, Mac, and Linux
Chrome on Windows, Mac, and Linux
e
