import http.client
import json
import time
import sys
import collections


DRAMA=18


def main(argv):
	try:
		try:
			api_key=argv[1]
			print("API key is {}".format(api_key))
		except:
			print("No api key given")

		conn = http.client.HTTPSConnection("api.themoviedb.org")


		page=1
		nb_films=0
		result=""

		while nb_films<350:

			payload = "{}"
			conn.request("GET", "/3/discover/movie?with_genres={}&primary_release_year.gte={}&page={}&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key={}".format(DRAMA,2004,page,api_key), payload)
			page+=1
			res = conn.getresponse()
			data = res.read()
			j = json.loads(data)


			for film in j['results']:
				if(nb_films<350):
					result+=str(film['id'])+","
					result+=film['title']+"\n"
					nb_films+=1
				else:
					break

		f = open('movie_ID_name.csv','w')
		f.write(result) #Give your csv text here.
		## Python will convert \n to os.linesep
		f.close()

		print("Written sucessfuly in movie_ID_name.csv")
	except:
		print("There was an error somewhere")

 
if __name__ == "__main__":
	main(sys.argv)