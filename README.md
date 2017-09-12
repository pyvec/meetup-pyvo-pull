# Meetup pyvo pull

Script for making pyvo.cz events from meetup.com.

## Install

Script is useful only inside pyvo/pyvo-data repository.

### Clone pyvec/pyvo-data repo

```
$ git clone git@github.com:pyvec/pyvo-data.git
Cloning into 'pyvo-data'...
remote: Counting objects: 1629, done.
remote: Compressing objects: 100% (24/24), done.
remote: Total 1629 (delta 11), reused 20 (delta 5), pack-reused 1599
Receiving objects: 100% (1629/1629), 274.53 KiB | 333.00 KiB/s, done.
Resolving deltas: 100% (945/945), done.
```

### Clone this repo

```
$ git clone git@github.com:pyvec/meetup-pyvo-pull.git
Cloning into 'meetup-pyvo-pull'...
remote: Counting objects: 21, done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 21 (delta 4), reused 21 (delta 4), pack-reused 0
Receiving objects: 100% (21/21), 5.07 KiB | 5.07 MiB/s, done.
Resolving deltas: 100% (4/4), done.
```

### Copy script and template

```
$ cp meetup-pyvo-pull/meetup_pyvo_pull.py meetup-pyvo-pull/event.yaml.tpl ./pyvo-data/
```

## Usage

### Go to folder with all necessary data

```
$ cd pyvo-data/
```

### Help

```
$ ./meetup_pyvo_pull.py --help
usage: meetup_pyvo_pull.py [-h] -c CITY -v VENUE [-s SERIE] -g GROUP -i
                           MEETUP_ID

### Create event based on meetup on meetup.com

optional arguments:
  -h, --help            show this help message and exit
  -c CITY, --city CITY  Name of the city (default: None)
  -v VENUE, --venue VENUE
                        Name of the venue in the city (default: None)
  -s SERIE, --serie SERIE
                        Name of the serie. {{city}}-pyvo if ommited (default:
                        None)
  -g GROUP, --group GROUP
                        Name of the group on meetup.com (default: None)
  -i MEETUP_ID, --id MEETUP_ID
                        Id of the meetup on meetup.com (default: None)
```

### Example usage

```
$ ./meetup_pyvo_pull.py --city ostrava --venue vr-levsky --serie ostrava-pyvo -g Ostravske-Pyvo -i 243107342
Writing to /tmp/pyvo-data/series/ostrava-pyvo/events/2017-10-04-Ty-nejlepsi-lightning-talky.yaml
```

### Result

```
$ cat /tmp/pyvo-data/series/ostrava-pyvo/events/2017-10-04-Ty-nejlepsi-lightning-talky.yaml
city: ostrava
start: 2017-10-04 19:00:00
name: Ostravské Pyvo
topic: Ty nejlepší lightning talky
description: |
    Ahoj.

    Po prázdninách, které jsme si protáhli až do září a zakončili je
    grilovačkou, je tu opět Pyvo v plné síle. Nicméně začátek by měl být
    vždy pozvolný a tak si pojďme udělat říjnové Pyvo oddechové.

    Tématem budou lightning talky. Lightning talk je mini přednáška či
    prezentace trvající maximálně pět minut, během které ukáže prezentující
    bez velké přípravy něco zajímavého nebo třeba představí svůj projekt.
    Že je pět minut málo? Omyl! I mezi těmito krátkými vystoupeními se dá
    najít spousta opravdu zajímavých a zábavných. A my se na Pyvu podíváme
    na záznamy těch nejlepších.

    Pokud máte vlastní oblíbený lightning talk, dejte nám o něm vědět.

    Těšíme se na hojnou účast.

venue: vr-levsky
talks: []
urls:
- https://www.meetup.com/Ostravske-Pyvo/events/243107342/
```

## License

MIT
