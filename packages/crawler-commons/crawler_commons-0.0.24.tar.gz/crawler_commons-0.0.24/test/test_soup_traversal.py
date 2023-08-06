import unittest

from bs4 import BeautifulSoup

from crawlutils.soup_traversal import get_td_text


class TestSoupTraversal(unittest.TestCase):

    def test_soup_traversal(self):
        html = """
            <table>
                <tr><td>정정사유</td><td>정정사유값</td></tr>
            </table>
        """
        soup = BeautifulSoup(html, "html.parser")
        r = get_td_text(soup.select("td"), '정정사유')
        self.assertEqual(r, '정정사유값')

    def test_soup_traversal(self):
        html = """
            <table>
                <tr><td>정정사유</td><td>정정사유값1</td></tr>
                <tr><td>정정사2</td><td>정정사유값2</td></tr>
                <tr><td>정정사3</td><td>정정사유값3</td></tr>
                <tr><td>정정사4</td><td>정정사유값4</td></tr>
            </table>
        """
        soup = BeautifulSoup(html, "html.parser")
        r = get_td_text(soup.select("td"), '정정사1', '정정사3')
        self.assertEqual('정정사유값3', r)