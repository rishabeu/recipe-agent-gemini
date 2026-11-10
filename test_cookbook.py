import unittest
from cookbook import search_recipes, substitute_ingredient
from recipes import RECIPES

class CookbookTests(unittest.TestCase):
    def test_search_by_title(self):
        self.assertIn("Lemon Herb Pasta", search_recipes("lemon pasta"))
    def test_search_by_ingredient(self):
        self.assertIn("chickpea_curry", search_recipes("chickpeas"))
    def test_no_match(self):
        self.assertIn("No matching", search_recipes("xyzunlisted"))
    def test_substitution(self):
        self.assertIn("oat", substitute_ingredient("milk"))
    def test_unknown_substitution(self):
        self.assertIn("No documented", substitute_ingredient("saffron"))
    def test_recipe_structure(self):
        for recipe in RECIPES.values():
            self.assertTrue(recipe["ingredients"])
            self.assertTrue(recipe["steps"])

if __name__ == "__main__":
    unittest.main()
