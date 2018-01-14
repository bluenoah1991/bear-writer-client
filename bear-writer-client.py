# -*- encoding: utf-8 -*-

import datetime
import tzlocal
import codecs
import argparse
import xcall
import StringIO

# Parse arguments
parser = argparse.ArgumentParser(description='Bear Writer Client')
parser.add_argument('-i', required=True, dest='identifier', metavar='IDENTIFIER', 
    help='note unique identifier')
parser.add_argument('-t', required=True, dest='title', metavar='NAME',
    help='note permalink title')
parser.add_argument('-d', required=True, dest='dir', metavar='DIRECTORY',
    help='output path')
args = parser.parse_args()

# Call X-Callback-Url
note = xcall.xcall('bear', 'open-note', {
    'id': args.identifier,
    'show_window': 'no'
})

# Relpace first line
head = u"""---
layout: post
title: %s
description: %s
date: %s
img: %s
tags: %s
---

"""

buf = StringIO.StringIO(note['note'])
firstLine = buf.readline()
if firstLine.startswith('# '):
    title = firstLine[2:].strip()
    description = ''
    date = datetime.datetime.now(tzlocal.get_localzone()).strftime("%Y-%m-%d %H:%M:%S %z")
    img = ''
    tags = ''
    firstLine = head % (title, description, date, img, tags)
restLines = buf.read()
post = "%s%s" % (firstLine, restLines)

# Save to directory
with codecs.open('%s/%s-%s.markdown' % (
    args.dir, datetime.datetime.now().strftime("%Y-%m-%d"), args.title), 'w', encoding="utf-8") as f:
    f.write(post)

print('Successfully saved.')