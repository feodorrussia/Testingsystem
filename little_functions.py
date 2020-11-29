# -*- coding: utf-8 -*-
divider = ""
def information_extractor_f(name):
    text = open("static/text_data/" + name[:-4] + divider + name[-4:], "r").read()
    return text.split("\n/*/\n")
