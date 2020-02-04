import understand

def open_file_for_write():
    ta_file = open("nginx_architecture.ta", "w")
    return ta_file

def write_common_part():
    ta_file = open_file_for_write()
    common_part = open("common_part.txt")
    for line in common_part.readlines():
        ta_file.write(line)
    ta_file.write('\n')

db = understand.open("nginx.udb")
# for file in db.ents("file"):
    # if source in file.longname():
    # print(file.longname())
write_common_part()