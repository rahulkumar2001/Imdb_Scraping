from bs4 import BeautifulSoup
import requests,pprint,json,os.path,random,time

#-----------------------------------task 1----------------------------------------------

def scrap_top_list():
	if os.path.exists("top_movies.json"):
		with open("top_movies.json","r") as file:
			read=file.read()
			data=json.loads(read)
		return (data)
	time.sleep(random.randint(15,30))		#for random time update
	url="https://www.imdb.com/india/top-rated-indian-movies/"
	link=requests.get(url)
	soup=BeautifulSoup(link.text,"html.parser")
	main_div=soup.find("div",class_="lister")
	tbody=main_div.find("tbody",class_="lister-list")
	trs=tbody.find_all("tr")

	movie_list=[]
	position=0
	for tr in trs:
		td=tr.find("td",class_="titleColumn")
		rating=tr.find("td",class_="ratingColumn").strong.get_text()
		name=td.find("a")
		year=td.find("span",class_="secondaryInfo")
		url=td.a["href"]
		position+=1
		movie_dic={
			"position":position,
			"name":name.text,
			"year":int(year.text[1:5]),
			"rating":rating,
			"url":"https://www.imdb.com"+url[0:17]
		}
		movie_list.append(movie_dic)

	with open("top_movies.json","w")as file:
		data=json.dump(movie_list,file,indent=4)

	return(movie_list)
# pprint.pprint(scrap_top_list())
# print ("--------------------------------------------")

 #---------------------------------------# task 2 -----------------------------------------------

movies = scrap_top_list()				#all movie store in movies
# def group_by_year(movie_list):			#parameter pass movie_list or anything of parameter
# 	years={}
# 	for i in movie_list:
# 		b=i["year"]
# 		years[b]=[]
# 	for key in years:
# 		for movie in movie_list:
# 			year=movie["year"]
# 			if key==year:
# 				years[key].append(movie)	
# 	return(years)
# pprint.pprint(group_by_year(movies))	#function call with arguments which store all movie list in movies


#----------------------------------------task 3----------------------------------------------

# def group_by_decade(movie_list):
# 	deacade={}
# 	for i in movie_list:
# 		b=(i["year"]//10)*10
# 		deacade[b]=[]

# 	for j in deacade:
# 		for m in movie_list:
# 			year=m["year"]
# 			deacade[j].append(m)
# 	return(deacade)
# pprint.pprint(group_by_decade(movies))


#----------------------------------------task 12------------------------------------------

url="https://www.imdb.com/title/tt0066763/fullcredits?ref_=tt_cl_sm#cast"
def scrap_movie_cast(url):
	dic_list=[]
	link=requests.get(url)
	soup=BeautifulSoup(link.text,"html.parser")

	main_div=soup.find("table",class_="cast_list")
	tds=main_div.find_all("td",class_="")
	for td in tds:
		dic={}
		ids=td.find("a").get("href")[6:15]
		dic["imdb_id"]=ids
		name=td.find("a").text.strip()
		dic["name"]=name
		dic_list.append(dic)
	return(dic_list)
# pprint.pprint(scrap_movie_cast(url))

# ----------------------------------------task 4 & 13  ------------------------------------------

def scrap_movie_details(movie_url):
	id1=movie_url[27:-1]
	file_name=id1+".json"
	if os.path.isfile(file_name):
		with open(file_name,"r") as file1:
			read=file1.read()
			data=json.loads(read)
		return(data)
	link=requests.get(movie_url)							#call api
	soup=BeautifulSoup(link.text,"html.parser")     #convert to html form using BeautifulSoup module

	name_tag=soup.find("div",class_="title_block")	#find movie name and poster using html
	name=name_tag.find("h1").text[:-8]
	poster_tag=soup.find("div",class_="poster")
	poster=poster_tag.find("img")["src"]

	a=[]
	director=[]
	language=[]
	country=[]
	time=soup.find("div",class_="subtext")        
	run=time.find("time").text.strip()
	if run[1]=="h" and run[-3:]=="min":
		runtime=int(run[0])*60+(int(run[3:-3]))		#find runtime using slice and hour to convert into min
	else:
		runtime=run[0:-3]
		print(runtime)
	for j in time:
		if j in time.find_all("a"):					#find which type or base of movie list
			genre_list=j.text
			a.append(genre_list)
	genre=a 										#pop last element of the genre list
	genre.pop()

	summary=soup.find("div",class_="plot_summary")		
	bio=summary.find("div",class_="summary_text").text.strip()	#find bio of discription of movie

	direct_tag=summary.find("div",class_="credit_summary_item") #find all director in a movie using find_all
	direct=direct_tag.find_all("a")	
	for i in direct:
		director.append(i.text)

	article=soup.find("div", {'class' : "article", 'id':"titleDetails"})
	txt_block=article.find_all("div",class_="txt-block")
	for m in txt_block:
		b = m.find("h4", class_="inline")			#find countary and all langauage in a list
		if(b !=  None):
			if b.text=="Country:":					
				Country=m.find("a").text
			if b.text=="Language:":
				Language=m.find_all("a")
				for i in Language:
					language.append(i.text)
	abc=scrap_movie_cast(movie_url)

	all_details={									#all data is convert into dictionary
		"name":name,
		"runtime":runtime,
		"genre":genre,
		"bio":bio,
		"Country":Country,
		"poster":poster,
		"director":director,
		"language":language,
		"cast": abc
	}
	print(all_details)

	with open(file_name,"w") as file1:
		json.dump(all_details,file1,indent=4)
	return(all_details)
url="https://www.imdb.com/title/tt0066763/"
# pprint.pprint(scrap_movie_details(url))



# ----------------------------------------task 5 ------------------------------------------

def get_movie_list_details(movies_list): 
	if os.path.exists("movies_details.json"):
		with open("movies_details.json","r") as file:
			read=file.read()
			data=json.loads(read)
		return (data)

	user=int(input("How many movies you want to scrap under 250th movies list?:"))	
	movies_ls=[]
	for j in movies_list[0:user]:
		url=j["url"]
		movies_dic=scrap_movie_details(url)
		movies_ls.append(movies_dic)
	return (movies_ls)		

	with open("movies_details.json","w")as file:
		data=json.dump(movies_ls,file,indent=4)
		write=data.write()
	return (write)
movies_name=get_movie_list_details(movies)	  #fuction call and return value
# pprint.pprint(movies_name)

# ----------------------------------------task 6 ------------------------------------------

def analysis_movies_language(movies_list):
	language_dic={}
	for i in movies_list:
		for key in i["language"]:
			if key not in language_dic:
				language_dic[key]=0
	for lan in language_dic:
		for m in movies_list:
			for l in m["language"]:
				if l==lan:
					language_dic[lan]+=1
	return(language_dic)
# pprint.pprint(analysis_movies_language(movies_name))

# ----------------------------------------task 7-----------------------------------------

def analysis_movies_directors(movie_list):
	director_dic={}
	for j in movie_list:
		for d in j["director"]:
			if d not in director_dic:
				director_dic[d] = 0
	for dirc in director_dic:
		for k in movie_list:
			for di in k['director']:
				if(di==dirc):
					director_dic[dirc]+=1
	return(director_dic)
# pprint.pprint(analysis_movies_directors(movies_name))

#----------------------------------------task 10------------------------------------------

def analysis_language_and_directors(movies_list):
	director_=[]
	language_=[]
	count=0
	for i in movies_list:
		for key in i["language"]:
			if key not in language_:
				count=+1
				language_.append(key)

	for j in movies_list:
		for direc in j["director"]:
			if direc not in director_:
				director_.append(direc)

	dic1={}
	for i in director_:
		dic2={}
		for j in language_:
			count=0
			for m in movies_name:
				der=m["director"]
				lang=m["language"]
				if i in der:
					if j in lang:
						count+=1
			if count!=0:
				dic2[j]=count
		dic1[i]=dic2
	return(dic1)
# pprint.pprint(analysis_language_and_directors(movies_name))

#----------------------------------------task 11------------------------------------------

def analysis_movies_genre(movies_list):
	dic3={}
	for i in movies_list:
		for key in i["genre"]:
			dic3[key]=0
	for genre_key in dic3:
		for i in movies_list:
			for key_ in i["genre"]:
				if genre_key==key_:
					dic3[genre_key]+=1							
	return(dic3)
# pprint.pprint(analysis_movies_genre(movies_name))

#----------------------------------------task 14------------------------------------------

def analyse_co_actors(movies_list):
	dic={}
	for i in movies_list:
		cast=i["cast"]
		dic[cast[0]["imdb_id"]]= {"Name" : cast[0]["name"], "frequent_co_actor" : []}
	for j in dic:
		for k in movies_list:
			for l in k:
				if l=="cast":
					main=k[l][0]["imdb_id"]
					if main==j:
						for ca in k[l][1:6]:
							counter=1
							for id_match in dic[j]["frequent_co_actor"]:
								if id_match["id"]==ca["imdb_id"]:
									counter+=id_match["num_movies"]							
							n={"id":ca["imdb_id"],"name":ca["name"],"num_movies":counter}
							dic[j]["frequent_co_actor"].append(n)
	return(dic)
# pprint.pprint(analyse_co_actors(movies_name))

#----------------------------------------task 15------------------------------------------

def analyse_actors(movies_list):
	dic2={}
	for i in movies_list:
		for cas in i["cast"]:
			k=cas["imdb_id"]
			dic={"name":"","no_of_movies":0}
			for j in movies_list:
				n=j["cast"]
				for key in n:
					if k==key["imdb_id"]:
						dic["name"]=cas["name"]
						dic["no_of_movies"]+=1
			dic2[k]=dic
	return(dic2)				
# pprint.pprint(analyse_actors(movies_name))