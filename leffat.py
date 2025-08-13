import sqlite3
from tabulate import tabulate

class MovieDatabase:
    def __init__(self, db_file='leffat2.db'):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def display_table(self, table_name):
        try:
            # Get table data
            self.cur.execute(f"SELECT * FROM {table_name}")
            data = self.cur.fetchall()
            
            if not data:
                print(f"\n{table_name.capitalize()} table is empty")
                return
                
            # Get column names
            self.cur.execute(f"PRAGMA table_info({table_name})")
            columns = self.cur.fetchall()
            headers = [column[1] for column in columns]
            
            # Special handling for movies table
            if table_name == "movies":
                data_with_names = []
                for row in data:
                    movie_id, name, year, director_id, actor_id = row
                    
                    # Get director name with error handling
                    self.cur.execute("SELECT name FROM directors WHERE id=?", (director_id,))
                    director_result = self.cur.fetchone()
                    director = director_result[0] if director_result else f"Unknown Director (ID:{director_id})"
                    
                    # Get actor name with error handling
                    self.cur.execute("SELECT name FROM actors WHERE id=?", (actor_id,))
                    actor_result = self.cur.fetchone()
                    actor = actor_result[0] if actor_result else f"Unknown Actor (ID:{actor_id})"
                    
                    data_with_names.append((movie_id, name, year, director, actor))
                
                data = data_with_names
                headers = ["ID", "Movie Title", "Year", "Director", "Actor"]
            
            print(f"\n{table_name.capitalize()} Table:")
            print(tabulate(data, headers=headers, tablefmt="grid"))
            
        except sqlite3.Error as e:
            print(f"Error displaying {table_name}: {e}")

    def add_actor(self):
        print("\nAdd New Actor")
        name = input("Name: ")
        year = input("Year of birth: ")
        hotness = input("Hotness score (1-100): ")
        
        try:
            self.cur.execute(
                "INSERT INTO actors (name, year_of_birth, hotness) VALUES (?, ?, ?)",
                (name, year, hotness)
            )
            self.conn.commit()
            print("Actor added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding actor: {e}")

    def add_director(self):
        print("\nAdd New Director")
        name = input("Name: ")
        year = input("Year of birth: ")
        
        try:
            self.cur.execute(
                "INSERT INTO directors (name, year_of_birth) VALUES (?, ?)",
                (name, year)
            )
            self.conn.commit()
            print("Director added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding director: {e}")

    def add_movie(self):
        print("\nAdd New Movie")
        
        # Display existing directors and actors
        print("\nAvailable Directors:")
        self.cur.execute("SELECT id, name FROM directors")
        directors = self.cur.fetchall()
        print(tabulate(directors, headers=["ID", "Name"], tablefmt="grid"))
        
        print("\nAvailable Actors:")
        self.cur.execute("SELECT id, name FROM actors")
        actors = self.cur.fetchall()
        print(tabulate(actors, headers=["ID", "Name"], tablefmt="grid"))
        
        # Get movie details
        title = input("\nMovie Title: ")
        year = input("Release Year: ")
        
        # Get director and actor with validation
        while True:
            director_id = input("Director ID: ")
            self.cur.execute("SELECT id FROM directors WHERE id=?", (director_id,))
            if self.cur.fetchone():
                break
            print("Invalid director ID. Please try again.")
        
        while True:
            actor_id = input("Actor ID: ")
            self.cur.execute("SELECT id FROM actors WHERE id=?", (actor_id,))
            if self.cur.fetchone():
                break
            print("Invalid actor ID. Please try again.")
        
        try:
            self.cur.execute(
                "INSERT INTO movies (name, year_of_release, director_id, actor_id) VALUES (?, ?, ?, ?)",
                (title, year, director_id, actor_id)
            )
            self.conn.commit()
            print("Movie added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding movie: {e}")

    def close(self):
        self.conn.close()

def main():
    db = MovieDatabase()
    
    while True:
        print("\nMovie Database Management System")
        print("1. View Tables")
        print("2. Add Data")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")
        
        if choice == "1":
            print("\nView Tables:")
            print("1. Actors")
            print("2. Directors")
            print("3. Movies")
            view_choice = input("Select table to view (1-3): ")
            
            if view_choice == "1":
                db.display_table("actors")
            elif view_choice == "2":
                db.display_table("directors")
            elif view_choice == "3":
                db.display_table("movies")
            else:
                print("Invalid choice.")
                
        elif choice == "2":
            print("\nAdd Data:")
            print("1. Add Actor")
            print("2. Add Director")
            print("3. Add Movie")
            add_choice = input("Select what to add (1-3): ")
            
            if add_choice == "1":
                db.add_actor()
            elif add_choice == "2":
                db.add_director()
            elif add_choice == "3":
                db.add_movie()
            else:
                print("Invalid choice.")
                
        elif choice == "3":
            break
            
        else:
            print("Invalid choice. Please try again.")
    
    db.close()
    print("\nGoodbye!")

if __name__ == "__main__":
    main()