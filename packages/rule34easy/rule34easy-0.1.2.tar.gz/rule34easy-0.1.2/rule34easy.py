import requests
import webbrowser as web


class Search:
	global count
	global tag
	def __init__(self, tag_timed: str, count_timed: int = 100):
		global count
		count = count_timed
		global tag
		tag = tag_timed
		try:
			if tag == None:
				print("Tags cannot be empty!")
			else:
				global data
				data = requests.get("https://r34-json-api.herokuapp.com/posts?&tags=" + tag.replace(" ", "+") + "&limit=" + str(count)).json()
		except:
			pass
	def get_json_index(self, index: int):
		try:
			return data[index]
		except:
			pass
	def get_data(self):
		try:
			return data
		except:
			pass
	def open_image(self, index: int):
		try:
			web.open(data[index]["file_url"]) # Opens image url
		except IndexError:
			print("Index out of radius")
		except:
			pass
	def download_file(self, path: str, index: int):
			try:
				fileurl = requests.get("https://r34-json-api.herokuapp.com/posts?tags=" + tag.replace(" ", "+") + "&limit=" + count).json()[index]["file_url"] # Gets url
				bytes = requests.get(fileurl).content # Gets url bytes
				open(path, "wb").write(bytes) # Writes bytes to file
			except:
				pass
	def get_tags(self, index: int):
		try:
			return requests.get("https://r34-json-api.herokuapp.com/posts?&tags=" + tag.replace(" ", "+") + "&limit" + str(count)).json()[index]["tags"]
		except:
			pass