import random
from datetime import timedelta

random.seed(42)

# builds the SID-00-xxx-xxx-xxx-xxx-xxx style ids used in prod
def generate_user_id(n):
    s = str(n).zfill(15)
    return "SID-00-" + "-".join([s[i:i+3] for i in range(0, 15, 3)])

# ORG-xxx-xxx-xxx-xxxx style
def generate_org_id(n):
    s = str(n).zfill(13)
    return f"ORG-{s[0:3]}-{s[3:6]}-{s[6:9]}-{s[9:13]}"

# combo state id like US-CA, IN-MH
def generate_state_id(country_code, state_code):
    return country_code.upper() + "-" + state_code.upper()

# cat_id like 1, 1.1, 1.2 (parent.child)
def generate_cat_id(parent_id, child_num):
    if parent_id:
        return f"{parent_id}.{child_num}"
    return str(child_num)

# nudges lat/lon a bit so points aren't stacked on the same spot
def jitter_coords(lat, lon, offset=0.05):
    new_lat = lat + random.uniform(-offset, offset)
    new_lon = lon + random.uniform(-offset, offset)
    return round(new_lat, 6), round(new_lon, 6)

def random_datetime(start, end):
    diff = end - start
    secs = random.randint(0, int(diff.total_seconds()))
    return start + timedelta(seconds=secs)

# created_at always <= last_updated_at
def gen_timestamps(start, end):
    created = random_datetime(start, end)
    updated = random_datetime(created, end)
    return created, updated

def fmt_ts(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")