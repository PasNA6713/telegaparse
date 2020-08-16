import pytest
from web_worker import *


def random_list(massive: list):
	"""func for selecting random sublist from list"""
	massive_to_return = []
	for i in range(random.randint(1, len(massive))):
		token = random.choice(massive)
		if token in massive_to_return:
			continue
		massive_to_return.append(token)
	return massive_to_return


def gen_filter_params():
	"""function for generating random filter params"""
	with open('settings.json') as data_file: 
		loaded_data = dict(json.load(data_file))
		districts = random_list(list(loaded_data["districts"].values()))
		filter_params = {
			"markets": random_list(list(loaded_data["markets"].values())),
			"categories": random_list(list(loaded_data["categories"].values())),
			"start price": {
				"from": 0,
				"to": random.randint(0, 10000)
			},
			"current price": {
				"from": 0,
				"to": random.randint(100000, 12000000)
			},
			"districts": [],
			"regions": []
		}
		for i in districts:
			filter_params["districts"].append(i["code"])
			filter_params["regions"].extend(random_list(i["regions"]))
		return(filter_params)


def test_get_url():
	"""test for func that converts filter params to url"""
	one_page_filter_params = {
		"markets": [1, 2],
		"categories": [1, 3],
		"districts": [1, 2, 3, 4],
		"regions": [10],
		"start price": {
			"from": 10000,
			"to": 120000
		},
		"current price": {
			"from": 10000,
			"to": 120000
		}
	}
	return_to_test = get_url(one_page_filter_params)
	assert  return_to_test == "https://торги-россии.рф/search?title_search=&search=&marketplaces%5B%5D=1&marketplaces%5B%5D=2&categorie_childs%5B%5D=1&categorie_childs%5B%5D=3&districts%5B%5D=1&districts%5B%5D=2&districts%5B%5D=3&districts%5B%5D=4&regions%5B%5D=10&trades-section=bankrupt&begin-price-from=10000&begin-price-to=120000&current-price-from=10000&current-price-to=120000"


def test_WebWorker():
	"""test for creating WebWorker"""
	web_worker = WebWorker(gen_filter_params())
	assert web_worker


def test_get_lot_info():
	""""""
	web_worker = WebWorker(gen_filter_params())
	if web_worker._lots:
		assert get_lot_info(random.choice(web_worker._lots))
	else:
		test_get_lot_info()


def worker_tester(web_worker):
	"""function for testing worker with different filter params"""
	def some_func(lots_info_list):
		pass

	my_func = web_worker.get_lots_info(some_func)
	while web_worker._lots_info:
		my_func()
	assert web_worker._lots_info == deque([]) and web_worker._lots == deque([])


def test_bypass_all_lots_1():
	"""filter for 1 page"""
	page = {'markets': ['8', '38', '48', '6', '12', '32', '20', '31', '49', '9', '45', '28', '11', '7', '39', '3', '13', '5', '14', '44', '30', '24', '42', '29', '40'], 'categories': ['33', '24', '7', '20', '5', '12', '9', '32', '22', '19', '26', '17', '38', '36', '41', '18', '35', '27'], 'start price': {'from': 0, 'to': 8899}, 'current price': {'from': 0, 'to': 8769659}, 'districts': ['2', '4', '8', '7', '1', '5'], 'regions': [11, 80, 29, 47, 7, 20, 41, 79, 27, 82, 24, 17, 70, 19, 75, 3, 55, 42, 32, 37, 77, 50, 69, 57, 31, 36, 62, 48, 56, 73]}
	web_worker = WebWorker(page)
	worker_tester(web_worker)


def test_bypass_all_lots_2():
	"""filter for 2 pages"""
	page = {'markets': ['29', '18', '7', '30', '41', '4', '9', '24', '27', '47', '46', '12', '5', '20', '43', '48', '50', '13', '8', '14', '37', '10', '2', '38', '19', '17', '28', '39', '45', '23', '25'], 'categories': ['38', '26', '12', '7', '35', '14', '2', '23', '36', '41', '19', '28', '27', '34', '18'], 'start price': {'from': 0, 'to': 6593}, 'current price': {'from': 0, 'to': 5774666}, 'districts': ['1', '3'], 'regions': [69, 62, 48, 50, 32, 30, 84, 23, 34, 8, 1]}
	web_worker = WebWorker(page)
	worker_tester(web_worker)


def test_bypass_all_lots_rand():
	"""random filter"""
	page = gen_filter_params()
	web_worker = WebWorker(page)
	if web_worker._lots:
		worker_tester(web_worker)
	else:
		test_bypass_all_lots_rand()
	