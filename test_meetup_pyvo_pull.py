import pytest
from meetup_pyvo_pull import (
    process_start,
    process_description,
    remove_diacritic,
    get_meetup_data,
    load_and_fill_template,
)

testdata = [
    (1505209577, "2017-09-12 11:46:17"),
    (15052095770000, "2017-09-12 11:46:17"),
    (150520957700000000, "2017-09-12 11:46:17"),
    (1505209671, "2017-09-12 11:47:51"),
    ("1505209671", "2017-09-12 11:47:51"),
]


@pytest.mark.parametrize("timestamp, expected", testdata)
def test_process_start(timestamp, expected):
    assert process_start(timestamp) == expected


testdata = [
    ("</p>", ""),
    ("blah", ""),
    ("blah\nblah", "    blah"),
    ("blah\nblah\nblah", "    blah\n    blah"),
    ('blah</br><p><a href="#">blah</a></p>blah\nend', "    blahblah\n\n    blah"),
]


@pytest.mark.parametrize("description, expected", testdata)
def test_process_description(description, expected):
    assert process_description(description) == expected


testdata = [
    ("", ""),
    ("blah", "blah"),
    (
        "příšerně žluťoučký kůň pěl ďábelské ódy",
        "priserne zlutoucky kun pel dabelske ody",
    ),
]


@pytest.mark.parametrize("input, expected", testdata)
def test_remove_diacritic(input, expected):
    assert remove_diacritic(input) == expected


testdata = [
    (
        "Ostravske-Pyvo",
        "243107342",
        "Ty nejlepší lightning talky",
        "restaurace V.R. Levský",
        "Ostravské Pyvo",
    )
    # TODO add one more meetup to test
]


@pytest.mark.parametrize("group, meetup_id, name, venue_name, group_name", testdata)
def test_get_meetup_data(group, meetup_id, name, venue_name, group_name):
    data = get_meetup_data(group, meetup_id)
    assert data["name"] == name
    assert data["venue"]["name"] == venue_name
    assert data["group"]["name"] == group_name
    assert data["link"].endswith("{}/events/{}/".format(group, meetup_id))


@pytest.mark.parametrize("group, meetup_id, name, venue_name, group_name", testdata)
def test_load_and_fill_template(group, meetup_id, name, venue_name, group_name):
    meetup_data = get_meetup_data(group, meetup_id)
    data = {
        "city": "Ostrava",
        "start": process_start(meetup_data["time"]),
        "name": meetup_data["group"]["name"],
        "topic": meetup_data["name"],
        "description": process_description(meetup_data["description"]),
        "venue": "V.R. Levský",
        "url": meetup_data["link"],
    }

    result = load_and_fill_template(**data)
    assert "{" not in result
    assert "}" not in result
    for line in result.splitlines():
        line = line.strip()
        if not line.startswith("urls"):
            assert not line.endswith(":")
        else:
            assert line.endswith(":")
