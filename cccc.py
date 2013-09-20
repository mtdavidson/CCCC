#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import sys
import re
import sqlite3

from BeautifulSoup import BeautifulSoup

price_regex = re.compile(".*\xa3([0-9]+\.[0-9]+).*")
conn = sqlite3.connect('cards.sqlite')
c = conn.cursor()

#TODO Check cards table exists if not create it

def query_chaoscards (card_number):
    result = {}

    card_number = card_number.replace ("_", ":").replace ("-", ":");

    print card_number;

    url = 'http://www.chaoscards.co.uk/rss/1/productlistings_rss/c84:' + card_number
    page = urllib2.urlopen (url).read ()

    soup = BeautifulSoup (page)

    item = soup.find ('item');

    if not hasattr (item, 'guid'):
        return;

    url = item.guid.contents[0]
    page = urllib2.urlopen (url).read ()

    soup = BeautifulSoup (page)
    soup.prettify ()

    price = soup.find (id='price_break_1').span.span.span.contents[0]
    r = price_regex.search(str (price))
    price = r.groups ()[0]

    result = {
        'card_number': card_number,
        'card_name': soup.find (id='product_title').contents[0],
        'price': price
    }

    return result

def query_koolkingdoms (card_number):
    result = {}
    url = 'http://www.koolkingdom.co.uk/acatalog/info_' + card_number + '.html';
    try:
        try:
            #Attempt to get page with standard URL
            page = urllib2.urlopen(url).read();
        except urllib2.HTTPError:
            #On failure attempt alternative
            page = urllib2.urlopen(url.replace ("_", "-")).read()
    except urllib2.HTTPError:
        print card_number + " could not be found"
        return result;

    soup = BeautifulSoup(page)
    soup.prettify()

    card_name = soup.title.string

    price = soup.find('actinic:prices').span
    r = price_regex.search(str (price))
    price = r.groups ()[0]

    result = {
        'card_number': card_number,
        'card_name': card_name,
        'price': price
    }

    return result;

while True:
    card_number = raw_input("Please Enter a Card Number: ")
    card_number = card_number.upper();
    card_number = card_number.replace ("-", "_");

    if (card_number == ""):
        continue;
    elif card_number == "QUIT":
        break;

    qty = 1;
    qty_input = raw_input ("Please Enter a QTY: %s"%qty + chr(8)*1)
    if not qty_input:
        qty_input = qty;

    if not str(qty_input).isdigit():
        print "QTY not valid"
        continue;

    qty = int (qty_input);

    kk = query_koolkingdoms (card_number);

    if (len (kk) == 0):
        continue;

    price = float (kk ['price'])

    cc = query_chaoscards (card_number);

    print "Kool Kingodoms:"
    print kk;
    print "Chaos Cards:"
    print cc;

    if (len (cc) != 0):
        price = (price + float (cc ['price'])) / 2

    #TODO: Use string formatting
    print kk['card_number'] + " " + kk['card_name'] + " " + " " + str(qty) + " " + str(float (price) * qty) + "[" + kk['price'] + "]";

    try:
        c.execute ("INSERT INTO cards VALUES (?, ?, ?, ?)", (card_number, card_name, qty, price))
        print "Added"
    except sqlite3.IntegrityError as e:
        print "Duplicate"
        c.execute ("UPDATE cards SET qty = qty + ?, price = ? WHERE card_number = ?", (qty, price, card_number));
        print "QTY Incremented and price updated"

    conn.commit ()

c.close ();
