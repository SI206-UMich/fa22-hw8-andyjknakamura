import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    list = []
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute('SELECT * FROM restaurants')
    rows = cur.fetchall()
    for row in rows:
        q = "SELECT category FROM categories WHERE id = ?"
        p = (row[2],)
        cur.execute(q, p)
        category = cur.fetchone()
        x = "SELECT building FROM buildings WHERE id = ?"
        y = (row[3],)
        cur.execute(x, y)
        building = cur.fetchone()
        dict = {}
        dict['name'] = row[1]
        dict['category'] = category[0]
        dict['building'] = building[0]
        dict['rating'] = row[4]
        list.append(dict)
    return list

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    d = {}
    data = get_restaurant_data(db_filename)
    for item in data:
        if item['category'] not in d:
            d[item['category']] = 1
        else:
            d[item['category']] += 1
    sorted_list = sorted(d.items(), key=lambda x:x[1], reverse=True)
    print(sorted_list)
    sorted_dict = dict(sorted_list)
    x = []
    for item in sorted_dict.keys():
        if ' ' not in item:
            x.append(item)
        else:
            new_item = item.replace(' ', '\n')
            x.append(new_item)
    y = sorted(sorted_dict.values(), reverse=True)
    fig = plt.figure(figsize=(160,10))
    ax = fig.add_subplot(111)
    ax.bar(x, y)
    ax.set_title('Types of restaurants on South University Avenue')
    ax.set_xlabel('restaurant categories')
    ax.set_ylabel('number of restaurants')
    plt.show()
    return sorted_dict

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    print(barchart_restaurant_categories('South_U_Restaurants.db'))

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)
    '''
    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)
    '''

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
