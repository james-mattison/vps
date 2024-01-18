import random
from datetime import datetime
import mysql.connector as mysql


NAMES = [
    "Fred",
    "Bill",
    "Bob",
    "Adolf",
    "Josef",
    "Michael",
    "Jesus",
    "Bilbo",
    "Saltino",
    "Fredo",
    "Heinrich",
    "Hermann",
    "Vladimir",
    "Pierre",
    "Pablo",
    "Ash",
    "Freidrick",
    "Faggot",
    "FartyBoy"
]

STREETS = [
    "Clover",
    "Broad",
    "San Vicente",
    "Oak Park",
    "Shalom Heights",
    "Niggerwalky",
    "Compton Blvd",
    "Hawthorne Blvd",
    "Adolf-Hitler-Strasse",
    "Avenue of the Stars",
    "Hollywood Blvd",
    "Goatse Lane",
    "Peckers Cutoff",
    "Shithead Street",
    "Dickmuch Avenue",
    "FartyBoys Bicycle Lane"
]

CITIES = [
    "Berlin",
    "Los Angles",
    "Moscow",
    "Frankfurt",
    "San Luis Obispo",
    "Atascadero",
    "Paso Robles"
]

EMAIL_HOSTS = [
    "gmail.com",
    "fart.gov",
    "shit.fart",
    "nig.nog",
    "penis.anus",
    "ahh.info",
    "inout.io",
    "bog.dog",
    "com.net",
    "nanny.mon",
    "bart.simpson"
]

def random_name():
    idx = random.randrange(0, len(NAMES)-1)
    return NAMES[idx]

def random_address():
    num_len = random.randrange(2, 5)
    num = ""
    for x in range(num_len):
        num += str(random.randrange(1, 9))

    idx = random.randrange(0, len(STREETS) - 1)
    street = STREETS[idx]

    idx = random.randrange(0, len(CITIES) - 1)
    city = CITIES[idx]
    addr = f"{num} {street}, {city}"

    return addr

def random_phone():
    num = ""
    for i, x in enumerate(range(10)):
        if i in [3, 6]:
            num += '-'
        n = str(random.randrange(1,9))
        num += n
    return num


def random_satisfaction():
    return "{:0.2f}".format(random.random() * 10)


def random_date():
    now = datetime.now()
    m_add = random.randrange(1,13)
    d_add = random.randrange(1,30)

    if now.month + m_add > 12:
        m = m_add
    else:
        m = now.month + m_add

    if now.day + d_add > 30:
        d = d_add
    else:
        d = now.day + d_add

    when = now.replace(month = m, day = d)

    return when.strftime("%s") # UNIX epoch

def random_domain():
    idx = random.randrange(0, len(EMAIL_HOSTS) - 1)
    return EMAIL_HOSTS[idx]

def random_total():
    return "{:.2f}".format(random.random() * 100)

def build_inserts(how_many = 10):
    inserts = []

    for _ in range(how_many):
        sql = """INSERT INTO customer_information (
    name,
    email,
    phone,
    address,
    satisfaction_level,
    customer_since,
    total_spent,
    pending_orders,
    historical_orders
)  VALUES ( """


        name = random_name()

        host = random_domain()

        email = f"{name}@{host}"

        phone = random_phone()

        address = random_address()

        satisfaction = float(random_satisfaction())

        customer_since = int(random_date())

        spent = float(random_total())

        for ob in [name, email, phone, address, satisfaction, customer_since, spent]:
            sql += f"\n   '{ob}', "
        sql = sql[:-2] # trim last ,

        sql += ",\n   NULL,\n   NULL);"

        inserts.append(sql)

    return inserts



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("how_many", action = "store", type = int, nargs = "?", default = 25)
    parser.add_argument("--host", action = "store", default = None)
    args = parser.parse_args()
    conn = mysql.Connect(
        host = args.host,
        user = "root",
        password = "123456",
        database = "customers",
        autocommit = True
    )

    curs = conn.cursor(buffered = True, dictionary = True)


    def query(sql):
        print(f"Executing {sql}")
        curs.execute(sql)


    inserts = build_inserts(args.how_many)

    for insert in inserts:
        print(insert)
        query(insert)
    print(f"Inserted {len(inserts)} rows.")








