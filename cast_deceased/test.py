from imdb import Cinemagoer


ia = Cinemagoer()


movie = ia.search_movie("heat")
movie_id = movie[0].movieID
movie_details = ia.get_movie(movie_id, info="main")
cast = movie_details["cast"]


# <Person id:0274684[http] name:_Martin Ferrero_>
actor_info = ia.get_person("0274684", info="biography")
print(actor_info.keys())

# for actor in movie_details["cast"]:
#     print(f"processing actor n°{list_num}")
#     actor_info = ia.get_person(actor.personID, info="biography")
#     try:
#         death_date.append(int(actor_info["death date"][:4]))
#         dead += 1
#     except:
#         alive += 1
#     list_num += 1
# death_date.sort()
# print(dead, alive, len(death_date), death_date)

# # print(movie_details['cast'])
# actor = ia.get_person('0000008', info='biography')
# print(actor.keys())
