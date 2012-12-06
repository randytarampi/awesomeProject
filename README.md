CMPT 470 Project
================

Due: 5 December 2012 2358 PT.

By: [Randy Tarampi](https://github.com/randytarampi), [Steven Evans](https://github.com/FaceBones) & [Conrad Locke](https://github.com/clocke)

We've made some sort of class schedule optimizer - it uses Django and is located at http://cmpt470.csil.sfu.ca:9017

Interested in what we had at our checkpoint evaluation? Check out the [checkpoint](https://github.com/randytarampi/awesomeProject/tree/checkpoint) tag.

What It Does:
-------------

It builds 'optimal' schedules given a set of courses and a set of unavailable times, where optimal minimizes the time spent on campus.

To Do:
------

Lots! We need to do lots of testing and general beautifying. As far as we're concerned, this is a bit more than a proof of concept, but substantially less than a polished, final product.

That said, we to do lots of work on the algorithm. The general styling and setup of the actual "[app](http://cmpt470.csil.sfu.ca:9017/scheduler/)" shouldn't be too much work - we're thinking about doing a bit experimenting with it depending on what we think looks "best", by no means is what you see finalized.

The data we're using has a few errors, like lectures that are scheduled like final exams, which tends to screw things up - see [MATH 152](http://cmpt470.csil.sfu.ca:9017/courses/MATH/152/). Since this data is from GoSFU (via Greg Baker's coursys), we can't really do much about it, nor do we think we should.

Other than that, which is to say, other than the styling, we would have liked to have more time to test. We're pretty sure that the algorithm works, but not totally 100% sure. Since the only testing it got was the mountains of user based testing (by Randy, Steven and any poor soul that we asked to try it out), and Conrad's whitebox testing, we're only relatively sure that it doesn't crash and burn out. If you've taken a look at the algorithm, you might notice that there's some extra functionality available that we did not care to actually give the user a chance at using, like the notion of 'needs/wants' - we didn't put it in because we didn't have time to test it.

There are a few input bugs here and there, like the addition of an invalid unavailable time (only on the first addition of a time!).  

So yeah, all in all, testing & styling.

Dependenices:
-------------

Requires [Dajax & Dajaxice](http://www.dajaxproject.com/).
Also requires [jQuery 1.7.2](http://code.jquery.com/jquery-1.7.2.js) and [jquery.ba-serializeobject](https://github.com/cowboy/jquery-misc/blob/master/jquery.ba-serializeobject.min.js).
Makes use of the [django-debug-toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar).

The arrow icons come from the [Mini icons 2](http://www.iconfinder.com/search/?q=iconset%3Aminiicons2) icon set. The loading spinner is care of [NETEYE](http://neteye.github.com/activity-indicator.html). The breadcrumb implementation comes care of [django-breadcrumbs](https://github.com/chronossc/django-breadcrumbs).

This project uses the HTML5 Boilerplate CSS reset, which can be found [here](https://github.com/h5bp/html5-boilerplate/blob/master/css/main.css).

Acknowledgements:
-----------------

Our CMPT 307 prof & textbook, without both of which we probably wouldn't have settled on (or even had) the idea. Our CMPT 470 prof, who didn't call us crazy.

Our friends, families, colleagues and loved ones who will presumingly bear with our frustrations/ranting during the building process. A special mention goes out to [Allison](https://github.com/allisonng) who made us cookies.
