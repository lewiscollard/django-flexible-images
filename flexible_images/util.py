#!/usr/bin/python

def aspect_ratio(image):
    return float(image.height) / float(image.width)

def aspect_ratio_percent(image):
    return aspect_ratio(image) * 100
