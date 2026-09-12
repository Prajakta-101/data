import csv
import random
from datetime import datetime
from utils import generate_state_id, generate_user_id, generate_org_id, random_datetime, fmt_ts, jitter_coords, gen_timestamps

random.seed(42)

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 9, 1)
NUM_USERS = 100
NUM_VOLUNTEERS = 50
NUM_ORGS = 30
NUM_SKILL_USERS = 60
SKILL_LEVELS = ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT"]

# countries
COUNTRIES = [
    {"country_id": 1, "country_name": "United States", "phone_code": "1", "country_code": "US", "is_eu_member": False},
    {"country_id": 2, "country_name": "India", "phone_code": "91", "country_code": "IN", "is_eu_member": False},
    {"country_id": 3, "country_name": "Ireland", "phone_code": "353", "country_code": "IE", "is_eu_member": True},
]

def write_countries():
    with open("countries.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["country_id", "country_name", "phone_code", "country_code", "last_updated_at", "is_eu_member"])
        for c in COUNTRIES:
            ts = fmt_ts(random_datetime(START_DATE, END_DATE))
            writer.writerow([c["country_id"], c["country_name"], c["phone_code"], c["country_code"], ts, c["is_eu_member"]])

# states 
STATES = [
    (1, "California", "CA", 36.7783, -119.4179),
    (1, "Texas", "TX", 31.9686, -99.9018),
    (1, "Virginia", "VA", 37.4316, -78.6569),
    (2, "Maharashtra", "MH", 19.7515, 75.7139),
    (2, "Karnataka", "KA", 15.3173, 75.7139),
    (3, "Leinster", "LE", 53.3498, -7.0000),
]

def write_states():
    rows = []
    with open("states.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["state_id", "country_id", "state_name", "state_code", "last_updated_at"])
        for country_id, name, code, lat, lon in STATES:
            country_code = next(c["country_code"] for c in COUNTRIES if c["country_id"] == country_id)
            state_id = generate_state_id(country_code, code)
            ts = fmt_ts(random_datetime(START_DATE, END_DATE))
            writer.writerow([state_id, country_id, name, code, ts])
            rows.append({"state_id": state_id, "country_id": country_id, "lat": lat, "lon": lon})
    return rows

# cities - a couple per state, jittered slightly off the state centroid
CITIES = [
    ("US", "CA", "San Jose"),
    ("US", "CA", "Sacramento"),
    ("US", "TX", "Austin"),
    ("US", "VA", "Richmond"),
    ("IN", "MH", "Mumbai"),
    ("IN", "MH", "Pune"),
    ("IN", "KA", "Bengaluru"),
    ("IE", "LE", "Dublin"),
]

def write_cities(state_rows):
    state_lookup = {s["state_id"]: s for s in state_rows}
    city_id = 1
    with open("cities.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["city_id", "state_id", "city_name", "lattitude", "longitude", "last_updated_at"])
        for country_code, state_code, city_name in CITIES:
            state_id = f"{country_code}-{state_code}"
            state = state_lookup[state_id]
            lat, lon = jitter_coords(state["lat"], state["lon"], offset=0.3)
            ts = fmt_ts(random_datetime(START_DATE, END_DATE))
            writer.writerow([city_id, state_id, city_name, lat, lon, ts])
            city_id += 1

# help categories 
HELP_CATEGORIES = [
    ("1", None, "FOOD", "Food assistance and donations"),
    ("1.1", "1", "FOOD_DONATE", "Donate food items"),
    ("1.2", "1", "FOOD_REQUEST", "Request food help"),
    ("2", None, "CLOTHES", "Clothing assistance"),
    ("2.1", "2", "CLOTHES_DONATE", "Donate clothes"),
    ("3", None, "TRANSPORT", "Transportation help"),
    ("4", None, "TUTORING", "Tutoring and education support"),
]

def write_help_categories():
    with open("help_categories.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cat_id", "cat_name", "cat_desc", "last_updated_at"])
        for cat_id, parent_id, name, desc in HELP_CATEGORIES:
            ts = fmt_ts(random_datetime(START_DATE, END_DATE))
            writer.writerow([cat_id, name, desc, ts])

# users 
FIRST_NAMES = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Riley", "Morgan", "Jamie", "Priya", "Rahul", "Aisling", "Liam"]
LAST_NAMES = ["Smith", "Patel", "Kelly", "Nguyen", "Garcia", "Brown", "Sharma", "Walsh", "Kumar", "Doyle"]
GENDERS = ["Male", "Female", "Other"]

def write_users(state_rows):
    rows = []
    with open("users.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "user_id", "state_id", "country_id", "user_status_id",
            "full_name", "first_name", "middle_name", "last_name",
            "primary_email_address", "primary_phone_number",
            "addr_ln1", "addr_ln2", "addr_ln3", "city_name", "zip_code",
            "last_location", "last_updated_at", "time_zone",
            "profile_picture_path", "gender",
            "language_1", "language_2", "language_3",
            "promotion_wizard_stage", "promotion_wizard_last_updated_at",
            "external_auth_provider", "dob", "is_eu"
        ])
        for i in range(1, NUM_USERS + 1):
            user_id = generate_user_id(i)
            state = random.choice(state_rows)
            state_id = state["state_id"]
            country_id = state["country_id"]
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            full_name = f"{first} {last}"
            email = f"user{i}@example.com"
            phone = f"555-01{i:03d}"
            zip_code = f"{10000 + i}"
            lat, lon = jitter_coords(state["lat"], state["lon"], offset=0.3)
            last_location = f"({lat},{lon})"
            ts = fmt_ts(random_datetime(START_DATE, END_DATE))
            dob = fmt_ts(random_datetime(datetime(1960, 1, 1), datetime(2005, 1, 1)))[:10]
            is_eu = state_id.startswith("IE")

            writer.writerow([
                user_id, state_id, country_id, 1,
                full_name, first, "", last,
                email, phone,
                "123 Main St", "", "", "SampleCity", zip_code,
                last_location, ts, "UTC",
                "", random.choice(GENDERS),
                "", "", "",
                1, ts,
                "", dob, is_eu
            ])
            rows.append({"user_id": user_id, "state_id": state_id, "country_id": country_id, "lat": lat, "lon": lon})
    return rows

# volunteer_details - pick 50 random users out of the 100, make them volunteers
def write_volunteer_details(user_rows):
    volunteers = random.sample(user_rows, NUM_VOLUNTEERS)
    with open("volunteer_details.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "user_id", "terms_and_conditions", "terms_accepted_at",
            "govt_id_path1", "govt_id_path2", "path1_updated_at", "path2_updated_at",
            "availability_days", "availability_times", "created_at", "last_updated_at"
        ])
        for v in volunteers:
            created, updated = gen_timestamps(START_DATE, END_DATE)
            days = '["Monday","Wednesday","Friday"]'
            times = '["09:00-12:00","14:00-17:00"]'
            writer.writerow([
                v["user_id"], True, fmt_ts(created),
                "s3://fake-bucket/id1.jpg", "s3://fake-bucket/id2.jpg",
                fmt_ts(created), fmt_ts(created),
                days, times,
                fmt_ts(created), fmt_ts(updated)
            ])
    return volunteers

# organizations 
ORG_NAME_PARTS = ["Helping Hands", "Community First", "Bright Futures", "United Relief", "Neighborhood Aid",
                   "Hope Foundation", "Care Network", "Open Hands", "Local Support", "Together We Rise"]
ORG_TYPES = ["non_profit", "for_profit"]
ORG_SIZES = ["small", "medium", "large"]

def write_organizations(state_rows):
    orgs = []
    with open("organizations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "org_id", "org_name", "street", "city_name", "state_id", "zip_code",
            "mission", "web_url", "phone", "email",
            "org_type", "org_size", "org_rating",
            "is_collaborator", "is_contributor",
            "created_at", "last_updated_at"
        ])
        for i in range(1, NUM_ORGS + 1):
            org_id = generate_org_id(i)
            state = random.choice(state_rows)
            state_id = state["state_id"]
            name = f"{random.choice(ORG_NAME_PARTS)} {i}"
            created, updated = gen_timestamps(START_DATE, END_DATE)
            writer.writerow([
                org_id, name, "456 Community Rd", "SampleCity", state_id, f"{20000+i}",
                "Helping the local community with essential services.",
                f"http://www.{name.lower().replace(' ', '')}.org",
                f"555-02{i:03d}", f"contact{i}@example.org",
                random.choice(ORG_TYPES), random.choice(ORG_SIZES), random.randint(1, 5),
                random.choice([True, False]), random.choice([True, False]),
                fmt_ts(created), fmt_ts(updated)
            ])
            orgs.append({"org_id": org_id, "state_id": state_id})
    return orgs

# user_skills - pick 60 random users, give each 1-3 random skills, no duplicate (user_id, cat_id) pairs
def write_user_skills(user_rows):
    skill_users = random.sample(user_rows, NUM_SKILL_USERS)
    cat_ids = [c[0] for c in HELP_CATEGORIES]
    rows_written = 0
    with open("user_skills.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "cat_id", "skill_level", "created_at", "last_updated_at"])
        for u in skill_users:
            num_skills = random.randint(1, 3)
            chosen_cats = random.sample(cat_ids, min(num_skills, len(cat_ids)))
            for cat_id in chosen_cats:
                created, updated = gen_timestamps(START_DATE, END_DATE)
                writer.writerow([
                    u["user_id"], cat_id, random.choice(SKILL_LEVELS),
                    fmt_ts(created), fmt_ts(updated)
                ])
                rows_written += 1
    return rows_written

# user_locations - every user gets a row, coords stay near their state's centroid
def write_user_locations(user_rows):
    with open("user_locations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "prev_loc", "curr_loc", "last_updated_at"])
        for u in user_rows:
            prev_lat, prev_lon = jitter_coords(u["lat"], u["lon"], offset=0.02)
            curr_lat, curr_lon = jitter_coords(u["lat"], u["lon"], offset=0.02)
            ts = fmt_ts(random_datetime(START_DATE, END_DATE))
            writer.writerow([
                u["user_id"],
                f"POINT({prev_lon} {prev_lat})",
                f"POINT({curr_lon} {curr_lat})",
                ts
            ])

# volunteer_locations - only volunteers get a row, must match volunteer_details.user_id
def write_volunteer_locations(volunteer_rows):
    with open("volunteer_locations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "prev_loc", "curr_loc", "last_updated_at"])
        for v in volunteer_rows:
            prev_lat, prev_lon = jitter_coords(v["lat"], v["lon"], offset=0.02)
            curr_lat, curr_lon = jitter_coords(v["lat"], v["lon"], offset=0.02)
            ts = fmt_ts(random_datetime(START_DATE, END_DATE))
            writer.writerow([
                v["user_id"],
                f"POINT({prev_lon} {prev_lat})",
                f"POINT({curr_lon} {curr_lat})",
                ts
            ])

if __name__ == "__main__":
    write_countries()
    state_rows = write_states()
    write_cities(state_rows)
    write_help_categories()
    user_rows = write_users(state_rows)
    volunteer_rows = write_volunteer_details(user_rows)
    org_rows = write_organizations(state_rows)
    skill_count = write_user_skills(user_rows)
    write_user_locations(user_rows)
    write_volunteer_locations(volunteer_rows)
    print(f"wrote {len(COUNTRIES)} countries, {len(state_rows)} states, {len(CITIES)} cities, {len(HELP_CATEGORIES)} help categories, {len(user_rows)} users, {len(volunteer_rows)} volunteer_details, {len(org_rows)} organizations, {skill_count} user_skills, {len(user_rows)} user_locations, {len(volunteer_rows)} volunteer_locations")