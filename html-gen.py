#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Script for envelope money distribution."""


# Imports
import sys

# Global variables

output_file_name = {
    'file': None,
    'encoding': 'utf-8',
    'mode': 'w'
}


# Class definitions

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class HTML:

    def __init__(self):
        self.tag = "html"
        self.content = "<%s>\n" % self.tag

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.content = "%s</%s>" % (self.content, self.tag)
        return self

    def __str__(self):
        return self.content

    def __iadd__(self, other):
        self.content = "%s%s</%s>\n" % (self.content,
                                        other,
                                        other.tag)
        return self


class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.content = "<%s>\n" % self.tag

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def __str__(self):
        return self.content

    def __iadd__(self, other):
        self.content = "%s%s</%s>\n" % (self.content,
                                        str(other),
                                        other.tag)
        return self


class Tag:

    def __init__(self, tag, is_single=False, klass=(), child=False, **kwargs):
        self.tag = tag              # имя тега
        self.is_single = is_single  # одинарный тег
        self.text = ""              # текст внутри тега
        self.content = ""           # собираем тег тут

        self.klass = []             # список классов стилей
        for item in klass:
            self.klass.append(item)

        self.attrs = []             # список других аттрибутов
        for attr, value in kwargs.items():
            self.attrs.append(" %s=\"%s\"" % (attr, value))

        self.child = child          # дочерний html тег класса Tag

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def __str__(self):

        if self.is_single:  # форматирование одинарного тега
            self.content = \
                "    <%s%s data-image=\"responsive\"/>\n   " % (self.tag,
                                                                " ".join(self.attrs))
        elif self.child:    # дочерний тег
            if self.klass:  # дочерний тег с классом
                self.content = \
                    "   <%s class=\"%s\"%s> %s %s" % (self.tag,
                                                      " ".join(self.klass),
                                                      " ".join(self.attrs),
                                                      self.text,
                                                      self.content)
            elif self.attrs:  # дочерний тег с аттрибутами
                self.content = "    <%s %s> %s %s" % (self.tag,
                                                      " ".join(self.attrs),
                                                      self.text,
                                                      self.content)
            else:           # дочерний тег без классов стилей
                self.content = "    <%s> %s %s" % (self.tag,
                                                   self.text,
                                                   self.content)
        elif self.klass:    # родительский тег класса Tag с классами стилей
            self.content = "   <%s class=\"%s\"%s> %s %s" % (self.tag,
                                                             " ".join(
                                                                 self.klass),
                                                             " ".join(
                                                                 self.attrs),
                                                             self.text,
                                                             self.content)
        else:
            self.content = "   <%s%s> %s %s" % (self.tag,
                                                " ".join(self.attrs),
                                                self.text,
                                                self.content)

        return self.content

    def __iadd__(self, other):
        if other.is_single:
            self.content = "%s \n %s" % (self.content,
                                         other)
        else:
            self.content = "%s \n %s</%s>" % (self.content,
                                              other,
                                              other.tag)
        return self


# Function definitions

def export(data):
    if output_file_name['file'] is None:
        print("\n" + bcolors.OKGREEN + data + "\n")
    else:
        with open(**output_file_name) as fp:
            fp.write(data)
        print(bcolors.OKGREEN + "Файл " +
              bcolors.HEADER + output_file_name['file'] +
              bcolors.OKGREEN + " сгенерирован")


def main():
    with HTML() as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead", test_attr="random value") as div:
                with Tag("p", child=True, another_attr="test") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png",  child=True) as img:
                    div += img

                body += div

            doc += body

    export(str(doc))


if __name__ == "__main__":
    # Проверяем есть ли аргумент (имя файла) в строке запуска
    if len(sys.argv) > 1:
        # Передаем переданное аргументом имя файла в настройки вывода
        output_file_name['file'] = sys.argv[1]
    main()


# ==== Необходимый результат выполнения: ========
#
# <html>
# <head>
#   <title>hello</title>
# </head>
# <body>
#     <h1 class="main-text">Test</h1>
#     <div class="container container-fluid" id="lead">
#         <p>another test</p>
#         <img src="/icon.png" data-image="responsive"/>
#     </div>
# </body>
# </html>
