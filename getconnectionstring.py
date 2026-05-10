import configparser

# Create the configparser object
config = configparser.ConfigParser()

# Read the config.ini file
config.read('config.ini')

# Debug print to verify sections
print("Sections:", config.sections())

# Access values safely
drive = config['database']['DRIVER']
server = config['database']['SERVER']
Database = config['database']['DATABASE']
uid = config['database']['UID']
password = config['database']['PWD']

# Construct the connection string
connectionstring = (
    f"DRIVER={{{drive}}};"
    f"SERVER={server};"
    f"DATABASE={Database};"
    f"UID={uid};"
    f"PWD={password};"
)

print("Connection is successful")
print(connectionstring)
