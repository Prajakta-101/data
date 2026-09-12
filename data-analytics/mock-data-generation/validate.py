import csv

# just basic sanity checks before we trust these csvs for a pr
# reads what we generated and checks pks are unique + fks point to real rows

def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def check_unique(rows, key_fields, label):
    seen = set()
    dupes = 0
    for r in rows:
        key = tuple(r[k] for k in key_fields)
        if key in seen:
            dupes += 1
        seen.add(key)
    status = "OK" if dupes == 0 else f"FAIL ({dupes} dupes)"
    print(f"{label} unique {key_fields}: {status}")

def check_fk(child_rows, child_key, parent_rows, parent_key, label):
    parent_ids = set(r[parent_key] for r in parent_rows)
    orphans = 0
    for r in child_rows:
        val = r[child_key]
        if val and val not in parent_ids:
            orphans += 1
    status = "OK" if orphans == 0 else f"FAIL ({orphans} orphans)"
    print(f"{label}: {status}")

def main():
    countries = read_csv("countries.csv")
    states = read_csv("states.csv")
    cities = read_csv("cities.csv")
    help_categories = read_csv("help_categories.csv")
    users = read_csv("users.csv")
    volunteer_details = read_csv("volunteer_details.csv")
    organizations = read_csv("organizations.csv")
    user_skills = read_csv("user_skills.csv")
    user_locations = read_csv("user_locations.csv")
    volunteer_locations = read_csv("volunteer_locations.csv")

    print("--- primary key checks ---")
    check_unique(countries, ["country_id"], "countries")
    check_unique(states, ["state_id"], "states")
    check_unique(cities, ["city_id"], "cities")
    check_unique(help_categories, ["cat_id"], "help_categories")
    check_unique(users, ["user_id"], "users")
    check_unique(volunteer_details, ["user_id"], "volunteer_details")
    check_unique(organizations, ["org_id"], "organizations")
    check_unique(user_skills, ["user_id", "cat_id"], "user_skills")
    check_unique(user_locations, ["user_id"], "user_locations")
    check_unique(volunteer_locations, ["user_id"], "volunteer_locations")

    print("\n--- foreign key checks ---")
    check_fk(states, "country_id", countries, "country_id", "states.country_id -> countries")
    check_fk(cities, "state_id", states, "state_id", "cities.state_id -> states")
    check_fk(users, "state_id", states, "state_id", "users.state_id -> states")
    check_fk(users, "country_id", countries, "country_id", "users.country_id -> countries")
    check_fk(organizations, "state_id", states, "state_id", "organizations.state_id -> states")
    check_fk(volunteer_details, "user_id", users, "user_id", "volunteer_details.user_id -> users")
    check_fk(user_skills, "user_id", users, "user_id", "user_skills.user_id -> users")
    check_fk(user_skills, "cat_id", help_categories, "cat_id", "user_skills.cat_id -> help_categories")
    check_fk(user_locations, "user_id", users, "user_id", "user_locations.user_id -> users")
    check_fk(volunteer_locations, "user_id", volunteer_details, "user_id", "volunteer_locations.user_id -> volunteer_details")

    print("\nall checks ran, look above for any FAIL lines")

if __name__ == "__main__":
    main()