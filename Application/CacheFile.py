from pickle import dump, load


class CacheFile:
    def __init__(self, name: str):
        self.path = 'Cache/' + name + '.pkl'

    def write(self, new_object=None):
        try:
            with open(self.path, 'wb') as file:
                dump(new_object, file)
        except BaseException:
            raise BaseException

    def read(self):
        try:
            with open(self.path, 'rb') as file:
                file_data = load(file)
                return file_data

        except EOFError:
            return None

        except FileNotFoundError:
            self.write()
            self.read()

        except BaseException:
            raise BaseException


if __name__ == "__main__":
    test_file = CacheFile("test")
    mas = [1, 2, 3]
    mas2 = list()
    mas2.append(mas)
    test_file.write(mas2)
    print(test_file.read())
    print(test_file.read())
