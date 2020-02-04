import understand

db = understand.open("nginx.udb")
for file in db.ents("file"):
    # if source in file.longname():
    print(file.longname())