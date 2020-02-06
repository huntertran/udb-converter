import understand
import pathlib
import os


class understand_to_lsedit_converter(object):

    db = ""
    ta_file = ""
    folders = []

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
    
    def extract_parent_folder(self, file):
        full_path = file.relname()
        return full_path[:-len(file.name())]

    def write_instance(self):
        current_path = pathlib.Path(__file__).parent.absolute()

        for file in self.db.ents("file"):
            self.ta_file.write("$INSTANCE " + self.cleanup_path(file.relname(), "") + " cFile")
            self.ta_file.write('\n')
            folder = self.extract_parent_folder(file)
            if folder not in self.folders:
                self.folders.append(folder)

        for folder in self.folders:
            self.ta_file.write("$INSTANCE " + self.cleanup_path(folder, "") + " cSubSystem")
            self.ta_file.write('\n')

        # folders = [x[0]
        #            for x in os.walk(os.path.join(current_path, "sources", "nginx"))]
        # for folder in folders:
        #     if(str(current_path) in folder):
        #         folder_path = folder[len(str(current_path)):]
        #         folder_path = folder_path.replace("\\", "/")
        #         self.ta_file.write("$INSTANCE " + folder_path + " cSubSystem")
        #         self.ta_file.write('\n')

    def cleanup_path(self, path, root_to_remove):
        clean_path = path[len(str(root_to_remove)):]
        return clean_path.replace("\\", "/")

    def write_contain(self):
        # current_path = pathlib.Path(__file__).parent.absolute()
        # folders = [x[0]
        #            for x in os.walk(os.path.join(current_path, "sources", "nginx"))]
        # for folder in folders:
        #     for root, dirs, files in os.walk(folder):
        #         for sub_dir in dirs:
        #             self.ta_file.write("contain " + self.cleanup_path(root, str(current_path)) +
        #                           " " + self.cleanup_path(root, str(current_path)) + sub_dir)
        #             self.ta_file.write('\n')
        #         for file_path in files:
        #             self.ta_file.write("contain " + self.cleanup_path(root, str(current_path)) +
        #                           " " + self.cleanup_path(root, str(current_path)) + file_path)
        #             self.ta_file.write('\n')

        # file contains in folder
        for file in self.db.ents("file"):
            folder_path = self.cleanup_path(self.extract_parent_folder(file), "")
            file_path = self.cleanup_path(file.name(), "")
            self.ta_file.write("contain " + folder_path + " " + file_path)

        # folder contains in folder
        self.folders.sort()
        for index, folder in enumerate(self.folders):
            if index < (len(self.folders) - 1) and folder in self.folders[index + 1]:
                # TODO: need implementation

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