import unittest
import scraper


class InitialScrapeTest(unittest.TestCase):

    def setUp(self):

        self.prim_link = "%s%s%s" %(
            "https://www.og.decc.gov.uk/",
            "eng/fox/decc/PED301X/",
            "companyBlocks",
        )
        self.scraper = scraper.CompanyLinks(
            "%s%s" %(
                self.prim_link,
                "Nav",
            )
        )
    def test_comapny_links_has_links(self):
        links = self.scraper.get_raw_links()
        self.assertGreater(len(links), 20)

    def test_cleaned_links_contains_http(self):
        links = self.scraper.get_clean_links()
        self.assertEqual(links[1][:4], 'http')

    def test_links_have_correct_links(self):
        links = self.scraper.get_clean_links()
        for i in ['6083', '125', '6084']:
            self.assertIn(
                "%s%s%s" %(
                    self.prim_link,
                    "Display?COMPANY_GROUP_ID=",
                    i,
                ),
                links,
            )

class SecondaryScrapeTest(unittest.TestCase):

    def setUp(self):
        self.prim_link = "%s%s%s" %(
            "https://www.og.decc.gov.uk/",
            "eng/fox/decc/PED301X/",
            "companyBlocks",
        )
        self.scraper = scraper.CompanyInfo(
            "%s%s" %(
                self.prim_link,
                "Display?COMPANY_GROUP_ID=125",
            )
        )

    def test_table_has_elements(self):
        table = self.scraper.get_table()
        self.assertGreaterEqual(len(table), 1)


    def test_table_has_correct_element(self):
        record = self.scraper.scrape()
        for i in range(4):
            self.assertEqual(
                record[i]['company'],
                'FIRST OIL EXPRO LIMITED'
            )

    def test_last_item_has_correct_element(self):
        record = self.scraper.scrape()
        self.assertEqual(
            record[-2]['company'],
            'ANTRIM RESOURCES (N.I.) LIMITED'
        )


if __name__ == '__main__':
    unittest.main()
