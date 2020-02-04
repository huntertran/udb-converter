import understand
import pathlib

def open_file_for_write():
    ta_file = open("nginx_architecture.ta", "w")
    return ta_file

def clear_content(ta_file):
    ta_file.truncate(0)

def write_common_part(ta_file):
    common_part = open("common_part.txt")
    for line in common_part.readlines():
        ta_file.write(line)
    ta_file.write('\n')

def write_instance(ta_file, db):

    current_path = pathlib.Path(__file__).parent.absolute()

    for file in db.ents("file"):
        relative_path = file.longname()[len(str(current_path)):]
        relative_path = relative_path.replace("\\","/")
        ta_file.write("$INSTANCE " + relative_path + " cFile")
        ta_file.write('\n')

db = understand.open("nginx.udb")
# for file in db.ents("file"):
    # if source in file.longname():
    # print(file.longname())
ta_file = open_file_for_write()
write_common_part(ta_file)
write_instance(ta_file, db)