import sqlite3


def start_db():
    try:
        # con = sqlite3.connect('db_temp.db')
        con = sqlite3.connect(':memory:')
        print("Connection is established: Database is created in memory")
        cursor = create_cursor(con)
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS geodata("
            "asn text, "
            "city text, "
            "continent_code text, "
            "country text, "
            "country_area text, "
            "country_calling_code text, "
            "country_capital text, "
            "country_code text, "
            "country_code_iso3 text, "
            "country_name text, "
            "country_population text, "
            "country_tld text, "
            "currency text, "
            "currency_name text, "
            "in_eu text, "
            "ip text PRIMARY KEY, "
            "languages text, "
            "latitude text, "
            "longitude text, "
            "org text, "
            "postal text, "
            "region text, "
            "region_code text, "
            "timezone text, "
            "utc_offset text, "
            "version text)")
        con.commit()
        return cursor, con
    except Exception as e:
        print(str(e))  # Exception hidden for security reasons like expose table names
        print("An error has occurred. Contact your administrator.")


def create_cursor(con):
    return con.cursor()


def load_ip_data_bulk(data, cursor, list_ips):
    try:
        for ip_data in data:
            if ip_data.get("error", False):
                cursor.execute(f"INSERT INTO geodata(ip) VALUES('{ip_data.get('ip', 'No IP')}')")
                print(
                    f"Error with IP {ip_data.get('ip', 'No IP')}: {ip_data.get('reason', 'No reason')}. Inserting only ip.")
            else:
                keys = ', '.join(list(ip_data.keys())).replace(", message", "")
                values = "'" + ','.join([str(s).replace(",", " ") for s in ip_data.values()]).replace(",",
                                                                                                      "' ,'") + "'"
                values = values.replace("'Please message us at ipapi.co/trial for full access' ,", "")
                cursor.execute(f"INSERT INTO geodata({keys}) VALUES({values})".replace("''", "'"))
                print(f"Inserting ip {ip_data.get('ip', 'No IP')}")
        return list_ips
    except Exception as e:
        print(f"Error on ip {ip_data.get('ip', 'No IP')}")
        list_ips.remove(str(ip_data.get('ip', 'No IP')))
        return list_ips


def load_ip_data_individual(data, cursor, list_ips):
    try:
        new_row = {"ip": data.get('ip', 'No IP'),
                   "country_code": data.get('country_code', 'No country code'),
                   "country_name": data.get('country_name', 'No country name'),
                   "region_code": data.get('region_code', 'No region code'),
                   "region": data.get('region_name', 'No region name'),
                   "city": data.get('city', 'No city'),
                   "latitude": data.get('latitude', 'No latitude'),
                   "longitude": data.get('longitude', 'No longitude'),
                   }

        keys = ', '.join(list(new_row.keys())).replace(", message", "")
        values = "'" + ','.join([str(s).replace(",", " ") for s in new_row.values()]).replace(",",
                                                                                              "' ,'") + "'"
        cursor.execute(f"INSERT INTO geodata({keys}) VALUES({values})")
        print(f"Inserting ip {new_row.get('ip', 'No IP')}")
    except Exception as e:
        print(f"An error has occurred with ip {data.get('ip', 'No IP')}. Contact your administrator.")


def delete_existent_data(cursor, list_ips):
    cursor.row_factory = lambda cursor, row: row[0]
    cursor.execute(f"SELECT ip from geodata")
    list_results = cursor.fetchall()
    new_list = [v for v in list_ips if v not in list_results]
    return new_list


def get_one_row(cursor, ip_address):
    cursor.execute(f"SELECT * from geodata where ip = '{ip_address}'")
    list_results = cursor.fetchone()
    names = [description[0] for description in cursor.description]
    return dict(zip(names, list_results))


def get_all_row(cursor):
    cursor.execute(f"SELECT * from geodata")
    list_results = cursor.fetchall()
    names = [description[0] for description in cursor.description]
    return names, list_results


def dump_db(cursor):
    cursor.execute(f"dump table geodata")
    cursor.commit()