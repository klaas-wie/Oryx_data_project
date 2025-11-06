import unittest
import os
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

    def test_parse_li_item_naval_losses(self):
        html = '''<li>
    <img alt="" class="thumbborder" 
         data-file-height="600" 
         data-file-width="1200" 
         height="12" 
         src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/23px-Flag_of_the_Soviet_Union.svg.png" 
         width="23" /> 
    2 Stenka-class patrol boat (Operated by the Sea Guard): 
    <a href="https://i.postimg.cc/8zG990c2/36.png">(1, BG-32 'Donbass' sunk)</a>&nbsp;
    <a href="https://i.postimg.cc/661SR8Mj/2011-Project-205-P-Tarantul-class-border-patrol-ship-dam-20-03-24.jpg">(1, damaged)</a>
</li>'''
        li = BeautifulSoup(html, "lxml").li
        losses = parse_li_item(li, category="Naval")
        self.assertEqual(len(losses), 2)
        self.assertEqual(losses[0]["equipment_type"], "Stenka-class patrol boat (Operated by the Sea Guard)")
        self.assertEqual(losses[0]["loss_type"], "BG-32 'Donbass' sunk")
        self.assertEqual(losses[0]["category"], "Naval")
        self.assertEqual(losses[0]["link_type"], "postimg")
        self.assertEqual(losses[1]["equipment_type"], "Stenka-class patrol boat (Operated by the Sea Guard)")
        self.assertEqual(losses[1]["loss_type"], "damaged")
        self.assertEqual(losses[1]["category"], "Naval")
        self.assertEqual(losses[1]["link_type"], "postimg")

    def test_parse_html_category_filter(self):
        file = os.path.join(os.path.dirname(__file__), "test_snippet.html")
        losses = parse_oryx_html(file, start_category="Tanks")
        self.assertEqual(len(losses), 1)
        self.assertEqual(losses[0]["equipment_type"], "T-62")

if __name__ == "__main__":
    unittest.main()
