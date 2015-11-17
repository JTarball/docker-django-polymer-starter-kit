<a href="http://www.djangoproject.com/" >
  <img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" />
</a>

## 'stats' App


# Limitation
- if bucketmanager goes down no historial rrd data will be collected. In the future we should timestamp the values going in redis by redis-stat
and reprocess them if they was a delay or if bucketmanager goes down.








Powered by django-allauth (http://www.intenct.nl/projects/django-allauth/) & includes a modified version of django-rest-auth (https://github.com/Tivix/django-rest-auth)

A basic app that deals with everything to do with front-end users include registration / activation / admin / user preferences.

- registration 
  - - deals with user registration & activation
- user details
  - - user preferences / accounts profiles / definition of accounts Model (User -- settings.AUTH_USER_MODEL)

# Built-in Django Admin?
The 'normal' django admin is for maintenance (super admin) only and will not be visible for users


# How to use


# ToDo / Future Work
- Emails via mailchimp
- Increase Complexity / Thorough testing of validators in serializers
- More social login interaction 
- Improved Stats & Logs 


# ChangeLog
- '0.0.1' version -- initial release 31/10/15










- use chartist.js


- Graphs

- minimal data is resolution of  a minute 

- 

- period should (1min, 15min, 1 hour, 1 day, 1 week, 1 month)

- so 

- chart type, stat, timestart, timend, period, special time = {last 30 days / last 3 months / ...}



1 min 15min 1hr 1day




-------------------
- last 24 hours
- last 30 days
- last 3 months
- last year 
-------------------
--- 
- period (1min, 15min, 1hour, 1day, 1week, 1month)
- granularity (1min, 15min, 1hour, 1day, 1week, 1month)

- aggregration (total / )


---------------
---- TYPE OF GRAPHS
- line graphs
- pie chart
- bar chart

-----

down sampling / up sampling


down sampling --- more data -> less data points ----- SUM?
up sampling   --- not enough data (rrd in past) -> more data points -- nan / missing (only solution at the moment)


ok in the case of upsampling -- there should be an *on the graph saying you have chosen a granularity that is not suitable for accuracy... we have interpolated values
best we could (rrd)




algorithm 
- use pandas convert to correct sample
- get lower granularity


not efficient
- period start date end date 
- granularity of stats


-----------------------------
start, end, granularity, period, sampling='last' (pandas option (could depend on stats))


- pull all stats for 

- start 
   - if on date - ok
   - else move backewards find date with granularity
- end
   - if on date - ok
   - else move forwards in time to date with granularity -- if reachs now then move backwards instead


- create data a timestamp from start -> end
  - populate with NaN
- fill in from redis where timestamp 


- for period 
rng = date_range('1/1/2012', periods=10, freq='5min')
- ts = Series(sample(xrange(100), 100), index=rng)
- ts.resample('h', how='last')
- turn into graph


- stats
  - counters  -- only increment (so can use instantaneous value at point in time)
  - 


  what about normal graphs
  - number of people joined ... 





- can use pandas to handle sampling and start end update
- timestamp -> date
- work out period from end date
- 


- start date 
- end date





- First attempt
-----
- use pandas to do most of the leg work
- start / period / freq
- get timestamp for start and end
- get data from redis
- - use pandas with timestamp?

  - get zunion - get with timestam







- dataframe --> epoch -> local time -> ?? -> timeseries












