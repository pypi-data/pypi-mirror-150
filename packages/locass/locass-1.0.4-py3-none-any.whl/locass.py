"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Simple Localization Manager writed on Python
version Beta 0.1
Copyright © Shchur Artem 2022
License: MIT License
Source code: Available on Github
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Have a nice coding!
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class LocalManager():
    def __init__(self):
        self.Path = "./test-locals/"
        self.Langs = {"RU": "ru.lang", "EN": "en.lang"}
        self.Keymarker = "[k]"
        self.Valuemarker = "[v]"
        self.langvalue = None

    def configure(self,path, langs, keym, valuem):
        self.Path = path
        self.Langs = langs
        self.Valuemarker = valuem
        self.Keymarker = keym
    def loadLang(self, key):
        """
        Loading selected localization to use-in
        :param key: Key to selected localization, declared in Langs
        :return: None
        """
        path = ""
        try:
            path = self.Langs.get(str(key))
        except:
            print("[ERROR] Invaild language key. Try to reinstall the application.")
            exit(1)
        try:
            obj = open(self.Path + path, "r")
            self.langvalue = obj.readlines()
            obj.close()
        except FileNotFoundError:
            print("[ERROR] Couldn't load localization file. Try to reinstall the application. Details: Cannot found",
                  path)
            exit(1)

    def g(self, key):
        """
        Returning selected by key parameter phrase from selected localization
        :param key: Key to phrase, declared in localization
        :return: Selected phrase from localization
        """
        if (self.langvalue == None):
            print("[ERROR] Couldn't load localization. Try to reinstall the application.")
            exit(1)
        word = None
        for line in self.langvalue:
            if (self.Keymarker + key + self.Valuemarker in line):
                word = line[len(key) + 6:]
                word = word.replace("\n", "")
                word = word.replace("\r", "")
                break
        if (word == None):
            print(
                "[ERROR] Couldn't load correct word in selected localization. Try to change another language or reinstall the application. Details: requested key:",
                key)
        else:
            return word




def Generator():
    pass

if __name__ == "__main__":
    Generator()

