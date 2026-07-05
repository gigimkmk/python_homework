# home work 1

class FootballTeam:
    def __init__(self, team_name, coach):
        self.team_name = team_name
        self.coach = coach
        self.players = [] 

   
    def add_player(self, name, position, number, age, nationality):
        player = {
            "name": name,
            "position": position,
            "number": number,
            "age": age,
            "nationality": nationality
        }
        self.players.append(player)

    
    def remove_player(self, number):
        for player in self.players:
            if player["number"] == number:
                self.players.remove(player)
                return "Player removed"
        return "Player not found"

   
    def update_player(self, number, key, value):
        for player in self.players:
            if player["number"] == number:
                player[key] = value
                return "Player updated"
        return "Player not found"


    def show_team_info(self):
        print(f"Team: {self.team_name}")
        print(f"Coach: {self.coach}")
        print("Players:")
        for p in self.players:
            print(p)

    def show_player_info(self, number):
        for player in self.players:
            if player["number"] == number:
                print(player)
                return
        print("Player not found")


team = FootballTeam("Barcelona", "Xavi")

team.add_player("Messi", "Forward", 10, 36, "Argentina")
team.add_player("Pedri", "Midfielder", 8, 21, "Spain")

team.show_team_info()

team.update_player(10, "goals", 1)

team.show_player_info(10)

team.remove_player(8)
team.show_team_info()

# updateidan cota gamichirda gavichede da chatgpt movixmare vicodi rogor damewera ufro awyobis da tanmimdevrobis problema mqonda 