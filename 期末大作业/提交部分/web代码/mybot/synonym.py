import csv
import os


class Synonym:

    def __init__(self, filename):
        self.filename = filename
        self.synonyms_list = None
        # 同义词替换表
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='UTF-8'):
                pass
        with open(filename, 'r', encoding='UTF-8') as file:
            self.synonyms_list = list(csv.reader(file))

    def add(self, new):
        self.synonyms_list.append(new)
        return True

    def delete(self, index):
        try:
            self.synonyms_list.pop(index)
            return True
        except IndexError:
            return False

    def update(self, index, new):
        if index >= len(self.synonyms_list):
            return False
        self.synonyms_list[index] = new
        return True

    @staticmethod
    def __get(word, words):
        if word in words:
            return words
        return False

    def get(self, word):
        for words in self.synonyms_list:
            res = self.__get(word, words)
            if res is not False:
                return res
        return [word]

    def replace(self, word, sentence):
        similarities = self.get(word)
        sentences = []
        for s in similarities:
            sentences.append(sentence.replace(word, s))
        return sentences

    def update_to_file(self):
        if self.synonyms_list is not None:
            with open(self.filename, 'w', newline='', encoding='UTF-8') as file:
                writer = csv.writer(file)
                for row in self.synonyms_list:
                    writer.writerow(row)
                return True
        return False

    def __del__(self):
        self.update_to_file()
        return True








