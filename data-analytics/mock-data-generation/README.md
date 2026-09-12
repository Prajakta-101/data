# Mock Data Generation

## What this is
Fake data for the Virginia analytics tables. Used for local dev, testing the API, dashboard testing, demos. Nothing here is real — no real names, emails, phone numbers, anything.

## Tables it makes
countries, states, cities, help_categories, users, volunteer_details, organizations, user_skills, user_locations, volunteer_locations

## What you need
Python 3.9+ (I used Anaconda 3.12.2). No pip installs needed, just uses the standard csv, random, and datetime modules that come with Python.

## How to run it
```bash
python3 generate_mock_data.py
```
Run it from inside this folder. It'll spit out all 10 csv files right here.

## Changing how many rows you get
Near the top of generate_mock_data.py there's a few numbers you can change:
- NUM_USERS (default 100)
- NUM_VOLUNTEERS (default 50, this many of the users become volunteers)
- NUM_ORGS (default 30)
- NUM_SKILL_USERS (default 60, this many users get assigned skills)

Change those and rerun the script. countries/states/cities/help_categories stay fixed since they're basically real reference data, not something you'd want random amounts of.

## How the tables connect
- states.country_id points to countries.country_id
- cities.state_id points to states.state_id
- users.state_id points to states.state_id
- users.country_id points to countries.country_id
- volunteer_details.user_id points to users.user_id
- user_skills.user_id points to users.user_id
- user_skills.cat_id points to help_categories.cat_id
- organizations.state_id points to states.state_id
- user_locations.user_id points to users.user_id
- volunteer_locations.user_id points to volunteer_details.user_id — NOT straight to users. A user has to be a volunteer first before they can have a volunteer_locations row.

## ID formats
- user_id looks like SID-00-XXX-XXX-XXX-XXX-XXX, matches how prod generates it
- org_id looks like ORG-XXX-XXX-XXX-XXXX, same deal
- state_id is like US-CA or IN-MH (country code + state code)
- cat_id is like 1, 1.1 (parent then child number)

## Why the coordinates make sense
Each state has a rough center point (lat/lon). Cities, users, orgs, and the two location tables all get their coordinates by nudging slightly off their state's center point, so a user in California actually shows up near California, not randomly anywhere on the map.

## Where the files end up
data-analytics/mock-data-generation/ — same folder as this script

## Checking it worked
```bash
python3 validate.py
```
This checks that no ID repeats where it shouldn't, and that every foreign key actually points to something real (no orphan rows). If everything's fine you'll see "OK" on every line. If something's broken it'll say FAIL and tell you exactly what and how many rows.
