# -*- coding: utf-8 -*-
divider = "1"
def information_extractor(name):
    text = open("static/text_data/" + name[:-4] + divider + name[-4:], "r").read()
    return text.split("\n/*/\n")
