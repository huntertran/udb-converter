import understand
import pathlib
import os


class understand_to_lsedit_converter(object):

    db = ""
    ta_file = ""
    folders = []

    def open_file_for_write(self, file_name):
        ta_file = open(file_name, "w")
        return ta_file

    def clear_content(self):
        self.ta_file.truncate(0)

    def write_common_part(self):
        # common_part = open("common_part.txt")
        # for line in common_part.readlines():
        #     self.ta_file.write(line)
        common_part = "SCHEME TUPLE :\ncLinks		cFunction	cFunction\ncontain		cFunction		cFunction\n// Relation Inheritance\nSCHEME ATTRIBUTE : \ncSubSystem {\n	class_style = 4\n	color = (0.0 0.0 1.0)\n}\ncFile {\n	class_style = 2\n	color = (0.9 0.9 0.9)\n	labelcolor = (0.0 0.0 0.0)\n}\ncFunction {\n	color = (1.0 0.0 0.0)\n	labelcolor = (0.0 0.0 0.0)\n}\n(cLinks) {\n	color = (0.0 0.0 0.0)\n}FACT TUPLE :\n"
        self.ta_file.write(common_part)
        self.ta_file.write('\n')

    def extract_parent_folder(self, file):
        full_path = file.relname()
        return full_path[:-len(file.name())]

    def write_instance(self):

        for file in self.db.ents("file"):
            if ":" not in file.relname():
                self.ta_file.write(
                    "$INSTANCE /" + self.cleanup_path(file.relname(), "") + " cFile")
                self.ta_file.write('\n')
            folder = self.extract_parent_folder(file)
            if folder not in self.folders:
                self.folders.append(folder)

        for folder in self.folders:
            if ":" not in folder:
                self.ta_file.write(
                    "$INSTANCE /" + self.cleanup_path(folder, "") + " cSubSystem")
                self.ta_file.write('\n')

    def cleanup_path(self, path, root_to_remove):
        clean_path = path[len(str(root_to_remove)):]
        return clean_path.replace("\\", "/")

    def write_contain(self):

        # file contains in folder
        for file in self.db.ents("file"):
            folder_path = self.cleanup_path(
                self.extract_parent_folder(file), "")
            file_path = self.cleanup_path(file.name(), "")

            if ":" not in folder_path and ":" not in file_path:
                self.ta_file.write(
                    "contain /" + folder_path + " /" + folder_path + file_path)
                self.ta_file.write("\n")

        # folder contains in folder

        unique_folders = [""]
        # remove first party's libraries that was used by source code
        self.folders = [folder for folder in self.folders if ":" not in folder]
        # merge folders' path to the longest unique
        self.folders.sort()

        for folder in self.folders:
            isFolderPathExisted = False
            for unique_folder in unique_folders:
                if folder in unique_folder:
                    isFolderPathExisted = True
                    break
                if unique_folder in folder:
                    unique_folders.remove(unique_folder)
                    break
            if not isFolderPathExisted:
                unique_folders.append(folder)

        for unique_folder in unique_folders:
            folders = unique_folder.split("\\")
            folders = [folder for folder in folders if folder != ""]
            self.populate_folders(folders)

    def populate_folders(self, folders):
        if len(folders) <= 2:
            current_folders_scope = folders
            self.write_folder_contain_folder(current_folders_scope)
        else:
            for index in range(1, len(folders)):
                current_folders_scope = []
                for j in range(0, index+1):
                    current_folders_scope.append(folders[j])

                self.write_folder_contain_folder(current_folders_scope)

    def write_folder_contain_folder(self, current_folders_scope):
        child_folder = "/".join(current_folders_scope)
        current_folders_scope.pop()
        parent_folder = "/".join(current_folders_scope)
        if parent_folder != "":
            self.ta_file.write(
                "contain /" + parent_folder + "/ /" + child_folder + "/")
            self.ta_file.write('\n')

    def write_clinks(self):
        for file in self.db.ents("file"):
            related_paths = file.depends()
            for related_path in related_paths:
                if ":" not in file.relname() and ":" not in related_path.relname():
                    self.ta_file.write("cLinks /"
                    + self.cleanup_path(file.relname(), "")
                    + " /" + self.cleanup_path(related_path.relname(), ""))

                    self.ta_file.write('\n')

    def convert(self, udb_file_path, ta_file_path):
        self.db=understand.open(udb_file_path)
        self.ta_file=self.open_file_for_write(ta_file_path)
        self.write_common_part()
        self.write_instance()
        self.write_contain()
        self.write_clinks()
        self.ta_file.close()


converter=understand_to_lsedit_converter()
converter.convert("demo\\nginx.udb","demo\\nginx_architecture.ta")
