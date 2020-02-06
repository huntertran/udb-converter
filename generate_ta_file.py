import understand
import pathlib
import os


class understand_to_lsedit_converter(object):

    db = ""
    ta_file = ""

    def open_file_for_write(self):
        ta_file = open("nginx_architecture.ta", "w")
        return ta_file

    def clear_content(self):
        self.ta_file.truncate(0)

    def write_common_part(self):
        common_part = open("common_part.txt")
        for line in common_part.readlines():
            self.ta_file.write(line)
            self.ta_file.write('\n')

    def write_instance(self):
        current_path = pathlib.Path(__file__).parent.absolute()

        for file in self.db.ents("file"):
            # if(str(current_path) in file.longname()):
            # relative_path = file.longname()[len(str(current_path)):]
            relative_path = file.relname().replace("\\", "/")
            self.ta_file.write("$INSTANCE " + relative_path + " cFile")
            self.ta_file.write('\n')

        folders = [x[0]
                   for x in os.walk(os.path.join(current_path, "sources", "nginx"))]
        for folder in folders:
            if(str(current_path) in folder):
                folder_path = folder[len(str(current_path)):]
                folder_path = folder_path.replace("\\", "/")
                self.ta_file.write("$INSTANCE " + folder_path + " cSubSystem")
                self.ta_file.write('\n')

    def cleanup_path(self, path, root_to_remove):
        clean_path = path[len(str(root_to_remove)):]
        return clean_path.replace("\\", "/")

    def write_contain(self):
        current_path = pathlib.Path(__file__).parent.absolute()
        folders = [x[0]
                   for x in os.walk(os.path.join(current_path, "sources", "nginx"))]
        for folder in folders:
            for root, dirs, files in os.walk(folder):
                for sub_dir in dirs:
                    self.ta_file.write("contain " + self.cleanup_path(root, str(current_path)) +
                                  " " + self.cleanup_path(root, str(current_path)) + sub_dir)
                    self.ta_file.write('\n')
                for file_path in files:
                    self.ta_file.write("contain " + self.cleanup_path(root, str(current_path)) +
                                  " " + self.cleanup_path(root, str(current_path)) + file_path)
                    self.ta_file.write('\n')

    def write_clinks(self):
        current_path_str = str(pathlib.Path(__file__).parent.absolute())
        for file in self.db.ents("file"):
            if(current_path_str.lower() in file.longname().lower()):
                file_path = self.cleanup_path(file.longname(), current_path_str)
                related_paths = file.depends()
                for related_path in related_paths:
                    self.ta_file.write("cLinks " + file.relname() +
                                  " " + related_path.relname())
                    self.ta_file.write('\n')

    def convert(self, udb_file_path):
        self.db = understand.open(udb_file_path)
        self.ta_file = self.open_file_for_write()
        self.write_common_part()
        self.write_instance()
        self.write_contain()
        self.write_clinks()
        self.ta_file.close()


converter = understand_to_lsedit_converter()
converter.convert("nginx.udb")