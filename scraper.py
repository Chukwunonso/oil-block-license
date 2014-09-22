# -*- coding: utf-8 -*-

"""
This bot was built for a website that is dynamically loaded.
There are two frames.
A list of links of companies is in one,
and information pertaining to an active link is in the other.
The list is processed first to yield the links needed for the final
step.
"""

import json
from datetime import date
import turbotlib
from bs4 import BeautifulSoup as bs
import requests
import re
import time

class  CompanyLinks(object):
    "Class used to extract all the links"

    def __init__(self, main_link):

        self.main_link = main_link

    def get_raw_links(self):
        "Get the relevant links within the 'a' tag"

        req = requests.get(self.main_link)
        soup = bs(req.text)
        company_links = soup.find_all(href=re.compile("COMPANY_GROUP_ID"))
        return company_links

    def get_clean_links(self):
        "Return the naked links reading for parsing."

        raw_links = self.get_raw_links()
        cleaned = [link.get('href') for link in raw_links]
        return cleaned


class CompanyInfo(object):
    "Class that takes a link, and returns related data."

    def __init__(self, link):

        self.link = link
        self.company_name = ''

    def get_table(self):
        "Find the table containing info"

        req = requests.get(self.link)
        soup = bs(req.text)
        table = soup.find('table', class_='setoutList')
        return table

    def get_company_name(self, tds):
        """
        Website data is designed such that company name is
        shared among some records. The first entry holds the
        company name while all which share this are blank
        i.e. empty string.
        Therefore assign every company name to subsequent records
        that don't have explicit company names.
        """
        if tds[0].text != '':
            self.company_name = tds[0].text
            return self.company_name
        else:
            return self.company_name

    def scrape(self):
        "Run the scraping"

        sample_date = str(date.today())
        #turbotlib.log("Starting run...") # Optional debug logging
        table = self.get_table()
        records = []
        for tr in table.find_all('tr')[1:]:
            tds = tr.find_all('td')
            company_name = self.get_company_name(tds)
            if len(tds) > 1:
                record = {
                    "company": str(company_name),
                    "block": tds[1].text,
                    "interest": tds[2].text,
                    "operator": tds[3].text,
                    "licence": tds[4].text,
                    "sample_date": sample_date,
                    "source_url": self.link
                }
                records.append(record)
        return records


def run_scraper():
    "Initialize and run"

    links = CompanyLinks(
        "%s%s%s" %(
            "https://www.og.decc.gov.uk/",
            "eng/fox/decc/PED301X/",
            "companyBlocksNav"
        )
    )
    for i, j in enumerate(links.get_clean_links()):
        info = CompanyInfo(j)
        try:
            turbotlib.log("progress: %s" % i)
            print json.dumps(info.scrape())
        except AttributeError as e:
            #print "Fails at %s as %s" %(i, e)
            pass


if __name__ == '__main__':
    run_scraper()
