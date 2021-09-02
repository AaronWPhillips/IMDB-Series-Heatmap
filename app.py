import requests
import numpy
import itertools
import seaborn
import matplotlib.pyplot as plt

omdb_api = "http://www.omdbapi.com/"
omdb_api_key = ""

def fetch_ratings_from_imdb(omdb_id):
   ratings = []

   request_params = {
      "apikey": omdb_api_key,
      "i": omdb_id
   }   
   result = requests.get(omdb_api, params=request_params).json()
   
   title = result["Title"]
   number_of_seasons = int(result["totalSeasons"])
   current_season = 1

   while current_season <= number_of_seasons:
      current_season_ratings = []
      
      request_params = {
         "apikey": omdb_api_key,
         "i": omdb_id,
         "Season": current_season
      }
      result = requests.get(omdb_api, params=request_params).json()
      
      for current_episode in result["Episodes"]:
         if current_episode["imdbRating"] == "N/A":
            current_season_ratings.append(float(0.0))
         else:   
            current_season_ratings.append(float(current_episode["imdbRating"]))
      ratings.append(current_season_ratings)
      current_season = current_season + 1

   return title, list(zip(*itertools.zip_longest(*ratings, fillvalue=float(0.0))))
   
def generate_meshgrid_from_ratings(ratings):
   ratings_array = numpy.array(ratings)
   
   return numpy.meshgrid(ratings_array.shape[0], ratings_array.shape[1])

def display_heatmap_with_seaborn(title, ratings):
   print(ratings)
   heatmap = seaborn.heatmap(ratings, cmap="PiYG", annot=True)
   heatmap.set_xlabel("Episode")
   heatmap.set_ylabel("Season")
   heatmap.set_title(f"{title} ratings heatmap")
   plt.show()

if __name__ == "__main__":
   print("RatingsMap - Please input an IMDB show ID and we'll generate a heatmap!")
   show_id = input("Show ID: ")

   title, ratings = fetch_ratings_from_imdb(show_id)

   grid = generate_meshgrid_from_ratings(ratings)

   display_heatmap_with_seaborn(title, ratings)
