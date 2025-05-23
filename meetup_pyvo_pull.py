#!/usr/bin/env python

import os
import sys
import unicodedata
import textwrap
from urllib.request import urlopen
from datetime import datetime
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from jinja2 import Template
from teemup import parse

DIR = os.path.dirname(os.path.abspath(__file__))


def get_meetup_data(group, meetup_id):
    # Get available data about meetup
    url = "https://www.meetup.com/{}/events/{}".format(group, meetup_id)
    return parse(urlopen(url).read())[0]


def process_description(description):
    # Process description from HTML to intended YAML
    output = []
    parts = description.splitlines()
    indent = " " * 4
    for part in parts:
        part = part.strip()
        part = textwrap.fill(
            part, width=75, subsequent_indent=indent, initial_indent=indent
        )
        output.append(part)

    return "\n".join(output)


def load_and_fill_template(**kwargs):
    # Load YAML template and fill it with content of **kwargs
    template_file = os.path.join(DIR, "event.yaml.tpl")
    with open(template_file, "r") as fh:
        template = fh.read()

    template = Template(template)

    return template.render(**kwargs)


def remove_diacritic(input_str):
    # Remove diacritics from string
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    only_ascii = nfkd_form.encode("ASCII", "ignore")
    return only_ascii.decode()


if __name__ == "__main__":

    parser = ArgumentParser(
        description="Create event based on meetup on meetup.com",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--city",
        dest="city",
        type=str,
        required=True,
        help="Name of the city",
    )
    parser.add_argument(
        "-v",
        "--venue",
        dest="venue",
        type=str,
        required=True,
        help="Name of the venue in the city",
    )
    parser.add_argument(
        "-s",
        "--serie",
        dest="serie",
        type=str,
        default=None,
        help="Name of the serie. {{city}}-pyvo if ommited",
    )
    parser.add_argument(
        "-g",
        "--group",
        dest="group",
        type=str,
        required=True,
        help="Name of the group on meetup.com",
    )
    parser.add_argument(
        "-i",
        "--id",
        dest="meetup_id",
        type=str,
        required=True,
        help="Id of the meetup on meetup.com",
    )

    args = parser.parse_args()

    # Check city
    if not os.path.isdir(os.path.join(DIR, "cities", args.city)):
        print("City {} doesn't exist".format(args.city))
        sys.exit(1)

    # Check venue in the city
    if not os.path.isfile(
        os.path.join(DIR, "cities", args.city, "venues", args.venue + ".yaml")
    ):
        print("Venue {} doesn't exist".format(args.venue))
        sys.exit(1)

    # Construct serie name if arg is ommited
    if args.serie is None:
        args.serie = args.city + "-pyvo"
        print("Argument --serie is omitted, using {}".format(args.serie))
    if not os.path.isdir(os.path.join(DIR, "series", args.serie)):
        print("Serie {} doesn't exist".format(args.serie))
        sys.exit(1)

    meetup_data = get_meetup_data(args.group, args.meetup_id)
    data = {
        "city": args.city,
        "start": meetup_data["starts_at"].strftime("%Y-%m-%d %H:%M:%S"),
        "name": meetup_data["group_name"],
        "topic": meetup_data["title"],
        "description": process_description(meetup_data["description"]),
        "venue": args.venue,
        "url": meetup_data["url"],
    }

    event_file_content = load_and_fill_template(**data)
    event_date = data["start"].split()[0]
    event_name = remove_diacritic(data["topic"]).replace(" ", "-")
    event_file_name = "{}-{}.yaml".format(event_date, event_name)

    dest_file_name = os.path.join(
        DIR, "series", args.serie, "events", event_file_name
    )

    with open(dest_file_name, "w") as fh:
        print("Writing to", dest_file_name)
        fh.write(event_file_content)
