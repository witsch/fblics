fblics
======

Script to convert the [Frauen-Bundesliga schedule](http://www.ffc-turbine.de/ms01_buli1415.php)
as provided by [Turbine Potsdam](http://www.ffc-turbine.de/) to the iCalendar data exchange format.


Installation
------------

```shell
  $ pip install fblics
```


Usage examples
--------------

```shell
  $ fblics --help
  $ fblics > bundesliga.ics
  $ fblics -u http://www.ffc-turbine.de/ms02_saison1415.php > 2.bundesliga.ics
  $ fblics -f Frankfurt > frankfurt.ics
  $ fblics --turbine > turbine.ics
```
