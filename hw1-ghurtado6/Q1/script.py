import http.client
import json
import time
import sys
import collections


DRAMA=18
MAXTRIES=20

def getData(conn,request):
	tries=0
	while tries<MAXTRIES:
		try:

			payload = "{}"
			conn.request("GET", request, payload)
			res = conn.getresponse()
			data = res.read()
			j = json.loads(data)
			result=j['results']
			print("Request done correctly")
			return result
		except:

			print("Sleeping after {} attempts".format(tries))
			time.sleep(10)
			tries+=1


def main(argv):
		try:
			api_key=argv[1]
			print("API key is {}".format(api_key))
		except:
			print("No api key given")

		conn = http.client.HTTPSConnection("api.themoviedb.org")


		page=1
		nb_films=0
		movie_ID_name=""
		similars=set()
		while nb_films<350:

			request="/3/discover/movie?with_genres={}&primary_release_year.gte={}&page={}&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key={}".format(DRAMA,2004,page,api_key)
			page+=1
			
			moviesResult=getData(conn,request)

			for film in moviesResult:
				if(nb_films<350):
					idCurr=film['id']
					movie_ID_name+=str(idCurr)+","
					movie_ID_name+=film['title']+"\n"
					nb_films+=1



					requestSim="/3/movie/{}/similar?api_key={}&language=en-US&page=1".format(idCurr,api_key)
					resSim =getData(conn,requestSim)
					try:
						
						i=0
						done=False
						while not done:
							try:
								idSim=resSim[i]['id']
								a=min(idSim,idCurr)
								b=max(idSim,idCurr)
								similars.add((a,b))
								i+=1
							except:
								done=True
					except:
						pass

						
				else:
					break

		movie_ID_sim_movie_ID="" 
		for similar in list(similars):
			movie_ID_sim_movie_ID+=str(similar[0])+","+str(similar[1])+"\n"



		f = open('movie_ID_name.csv','w')
		f.write(movie_ID_name)
		f.close()
		
		f = open('movie_ID_sim_movie_ID.csv','w')
		f.write(movie_ID_sim_movie_ID)
		f.close()

		print("Written sucessfuly the two CSVs")

 
if __name__ == "__main__":
	start_time = time.time()
	main(sys.argv)
	elapsed_time = time.time() - start_time
	print(elapsed_time)