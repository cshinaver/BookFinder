import unittest

from bookfinder.api.scraper import AmazonScraper


class ApiScraperTestCase(unittest.TestCase):
    def test_amazon_scraper_gets_purchase_choices(self):
        """
        PurchaseChoice should have isbn, title, price, seller, thumbnail_link,
        book_type, regular_link, rental and author
        """
        book_title = "Compilers"
        scraper = AmazonScraper()
        ls = scraper.get_amazon_purchase_choices_for_keyword(book_title)
        b = ls[0]
        self.assertNotEqual(b['isbn'], '')
        self.assertNotEqual(b['title'], '')
        self.assertNotEqual(b['price'], '')
        self.assertNotEqual(b['seller'], '')
        self.assertNotEqual(b['thumbnail_link'], '')
        self.assertNotEqual(b['book_type'], '')
        self.assertNotEqual(b['link'], '')
        self.assertNotEqual(b['rental'], '')
        self.assertNotEqual(b['authors'], None)
        self.assertNotEqual(len(b['authors']), 0)
