import understand
import pathlib
import os

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
        if(str(current_path) in file.longname()):
            relative_path = file.longname()[len(str(current_path)):]
            relative_path = relative_path.replace("\\","/")
            ta_file.write("$INSTANCE " + relative_path + " cFile")
            ta_file.write('\n')
    
    folders = [x[0] for x in os.walk(os.path.join(current_path, "sources", "nginx"))]
    for folder in folders:
        if(str(current_path) in folder):
            folder_path = folder[len(str(current_path)):]
            folder_path = folder_path.replace("\\","/")
            ta_file.write("$INSTANCE " + folder_path + " cSubSystem")
            ta_file.write('\n')

def cleanup_path(path, root_to_remove):
    clean_path = path[len(str(root_to_remove)):]
    return clean_path.replace("\\","/")


def write_contain(ta_file, db):
    current_path = pathlib.Path(__file__).parent.absolute()
    folders = [x[0] for x in os.walk(os.path.join(current_path, "sources", "nginx"))]
    for folder in folders:
        for root,dirs,files in os.walk(folder):
            for sub_dir in dirs:
                ta_file.write("contain " + cleanup_path(root, str(current_path)) + " " + cleanup_path(root, str(current_path)) + sub_dir)
                ta_file.write('\n')
            for file_path in files:
                ta_file.write("contain " + cleanup_path(root, str(current_path)) + " " + cleanup_path(root, str(current_path)) + file_path)
                ta_file.write('\n')

def write_clinks(ta_file, db):
    current_path_str = str(pathlib.Path(__file__).parent.absolute())
    for file in db.ents("file"):
        if(current_path_str.lower() in file.longname().lower()):
            file_path = cleanup_path(file.longname(), current_path_str)
            related_paths = file.depends()
            for related_path in related_paths:
                ta_file.write("cLinks " + file_path + " " + related_path)
                ta_file.write('\n')

db = understand.open("nginx.udb")
ta_file = open_file_for_write()
write_common_part(ta_file)
write_instance(ta_file, db)
write_contain(ta_file, db)
write_clinks(ta_file,db)
ta_file.close()