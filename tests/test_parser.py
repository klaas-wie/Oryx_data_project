import unittest
from html_parser import parse_li_item, parse_oryx_html  # import your functions
from bs4 import BeautifulSoup

class TestOryxParser(unittest.TestCase):

    def test_parse_li_item_single_loss(self):
        html = '<li>2 T-54-3M: <a href="https://i.postimg.cc/1032.jpg">(1, destroyed)</a></li>'
        li = BeautifulSoup(html, "lxml").li
        losses = parse_li_item(li, category="Tanks")
        self.assertEqual(len(losses), 1)
        self.assertEqual(losses[0]["equipment_type"], "T-54-3M")
        self.assertEqual(losses[0]["loss_type"], "destroyed")
        self.assertEqual(losses[0]["category"], "Tanks")
        self.assertEqual(losses[0]["link_type"], "postimg")

    def test_parse_li_item_multiple_losses_in_one_link(self):
        html = '<li>4 T-55A: <a href="https://i.postimg.cc/1009.jpg">(2, 3, 4 and 5, damaged)</a></li>'
        li = BeautifulSoup(html, "lxml").li
        losses = parse_li_item(li, category="Tanks")
        self.assertEqual(len(losses), 4)
        self.assertTrue(all(loss["loss_type"] == "damaged" for loss in losses))

    # def test_parse_html_category_filter(self):
    #     html = '''
    #     <h3>Tanks (50)</h3>
    #     <ul>
    #         <li>1 T-62: <a href="https://i.postimg.cc/abcd.jpg">(1, destroyed)</a></li>
    #     </ul>
    #     <h3>Aircraft (20)</h3>
    #     <ul>
    #         <li>1 Su-25: <a href="https://i.postimg.cc/efgh.jpg">(1, destroyed)</a></li>
    #     </ul>
    #     '''
    #     soup = BeautifulSoup(html, "lxml")
    #     # simulate parsing only from Tanks onward
    #     losses = parse_oryx_html(soup, start_category="Tanks")
    #     self.assertEqual(len(losses), 1)
    #     self.assertEqual(losses[0]["equipment_type"], "T-62")

if __name__ == "__main__":
    unittest.main()
