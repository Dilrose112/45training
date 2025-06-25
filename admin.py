x=[ { "name": "Forrest Gump", "year": 1994, "duration": 142, "genres": ["Drama", "Romance"] },
{ "name": "Avengers: Endgame", "year": 2019, "duration": 181, "genres": ["Action",
"Adventure", "Drama"] }, { "name": "Back to the Future", "year": 1985, "duration": 114,
"genres": ["Adventure", "Comedy", "Sci-Fi"] } ]

def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def input_something(prompt):
    while True:
        value = input(prompt)
        if value.strip():
            return value
        else:
            print("Input cannot be empty. Please try again.")

def add():
    name = input_something("Enter movie name: ")
    year = input_int("Enter release year: ")
    duration = input_int("Enter duration in minutes: ")
    genres = input_something("Enter genres (comma-separated): ").split(',')
    genres = [genre for genre in genres]
    
    new_movie = {
        "name": name,
        "year": year,
        "duration": duration,
        "genres": genres
    }
    
    x.append(new_movie)

def list():
    if not x:
        print("No movies available.")
        return
    
    for i, movie in enumerate(x, start=1):
        print(str(i)+ ")", movie["name"],"("+str(movie["year"])+")",str(movie["duration"])+"mins",str(movie["genres"]))

def search():
    search_term = input_something("Enter movie name to search: ").lower()
    found_movies = [movie for movie in x if search_term in movie["name"].lower()]
    
    if not found_movies:
        print("No movies found.")
        return
    
    for i, movie in enumerate(found_movies, start=1):
        print(str(i) +")", movie["name"],"(" +str(movie["year"])+")",str(movie["duration"]),"mins",str(movie["genres"]))

def view():
    index=input_int("Enter movie index to view details : ")
    if index < 1 or index > len(x):
        print("Invalid index. Please try again.")
        return
    else:
        movie=x[index-1]
        print(str(index)+")", movie["name"],"(" +str(movie["year"])+")",str(movie["duration"]),"mins",str(movie["genres"]))

def delete():
    index=input_int("Enter movie index to delete: ")
    if index<1 or index >len(x):
        print("Index out of range. Please try again.")
    elif not x:
            print("No movies available.")
    else:
        x.pop(index-1)
        print("Movie at index",index,"deleted successfully")


print("Choose \n[a]dd\n[l]ist\n[s]earch \n[v]iew\n[d]elete\n[q]uit.")
print("List of movies: ")
list()
choice=input("Choose an action: ")
while choice!='q':
    if choice=='a':
        add()
        print("New list: ")
        list()
    elif choice=='l':
        list()
    elif choice=='s':
        search()
    elif choice=='v':
        view()
    elif choice=='d':
        delete()
        print("New list: ")
        list()
    choice=input("\nChoose an action again: ")

print("Goodbye!")




