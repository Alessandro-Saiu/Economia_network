import networkx as nx
import random



class Game(object):
    def __init__(self, grafo, target_list = []):
        self.g = grafo
        self.target = target_list
        self.interactions = []
        self.deny = []

    def __iter__(self):
        return self.interactions

    def __next__(self):
        self._indice += 1
        if self._indice >= len(self.interactions):
            self._indice = -1
            raise StopIteration
        else:
            return self.interactions[self._indice]

    def reset(self):
        self.interactions = []
        self.deny = []

    def increase_leader_prestige(self, target):
        for edge in self.g.edges():
            if edge[0] == target and self.g.nodes[edge[1]]["coalition"] == "West":
                # print(f"{edge[0]} gained prestige in the eyes of {edge[1]}")
                self.g.edges[edge]["weight"] += 1

    def increase_ally_prestige(self, target):
        for edge in self.g.edges():
            if edge[0] == target and self.g.nodes[edge[1]]["coalition"] == "Leader":
                print(f"{edge[0]} gained prestige in the eyes of {edge[1]}")
                self.g.edges[edge]["weight"] += 1
            elif edge[1] == target and self.g.nodes[edge[0]]["coalition"] == "Leader":
                # print(f"{edge[1]} gained prestige in the eyes of {edge[0]}")
                self.g.edges[edge]["weight"] += 1

    def decrease_leader_prestige(self, target):
        for edge in self.g.edges():
            if edge[0] == target and self.g.nodes[edge[1]]["coalition"] == "West":
                # print(f"{edge[0]} lost prestige in the eyes {edge[1]}")
                self.g.edges[edge]["weight"] -= 1

    def decrease_ally_prestige(self, target):
        for edge in self.g.edges():
            if edge[0] == target and self.g.nodes[edge[1]]["coalition"] == "Leader":
                # print(f"{edge[0]} lost prestige in the eyes {edge[1]}")
                self.g.edges[edge]["weight"] -= 1
            elif edge[1] == target and self.g.nodes[edge[0]]["coalition"] == "Leader":
                # print(f"{edge[1]} lost prestige in the eyes {edge[0]}")
                self.g.edges[edge]["weight"] -= 1

    def increase_pact_prestige(self, target):
        for edge in self.g.edges():
            if edge[0] == target and self.g.nodes[edge[1]]["coalition"] == "Anti-west":
                # print(f"{edge[0]} gained prestige in the eyes of {edge[1]}")
                self.g.edges[edge]["weight"] += 1

    def increase_challenger_prestige(self, target):
        for edge in self.g.edges():
            if edge[0] == target and self.g.nodes[edge[1]]["coalition"] == "Challenger":
                # print(f"{edge[0]} gained prestige in the eyes of {edge[1]}")
                self.g.edges[edge]["weight"] += 1
            elif edge[1] == target and self.g.nodes[edge[0]]["coalition"] == "Challenger":
                # print(f"{edge[1]} gained prestige in the eyes of {edge[0]}")
                self.g.edges[edge]["weight"] += 1

    def decrease_pact_prestige(self, target):
        for edge in self.g.edges():
            if edge[0] == target and self.g.nodes[edge[1]]["coalition"] == "Anti-west":
                # print(f"{edge[0]} lost prestige in the eyes {edge[1]}")
                self.g.edges[edge]["weight"] -= 1

    def decrease_challenger_prestige(self, target):
        for edge in self.g.edges():
            if edge[0] == target and self.g.nodes[edge[1]]["coalition"] == "Challenger":
                # print(f"{edge[0]} lost prestige in the eyes {edge[1]}")
                self.g.edges[edge]["weight"] -= 1
            elif edge[1] == target and self.g.nodes[edge[0]]["coalition"] == "Challenger":
                # print(f"{edge[1]} lost prestige in the eyes {edge[0]}")
                self.g.edges[edge]["weight"] -= 1

    def start_first_stage(self):
        for country in self.g.nodes():
            probability = 33

            if self.g.nodes[country]["coalition"] == "Challenger" and self.g.nodes[country]["aptitude"] == "ambitious":
                probability += 12
                enemy = random.choice(self.target)
                if self.g.nodes[enemy]["coalition"] == "West" or "Leader":
                    probability -= 5
                elif self.g.nodes[enemy]["coalition"] == "Leader" and self.g.nodes[enemy]["n_warheads"] >= 200:
                    probability -= 10

            elif self.g.nodes[country]["coalition"] == "Challenger" and self.g.nodes[country]["aptitude"] == "content":
                enemy = random.choice(self.target)
                if self.g.nodes[enemy]["coalition"] == "West" or "Leader":
                    probability -= 5
                elif self.g.nodes[enemy]["coalition"] == "Leader" and self.g.nodes[enemy]["n_warheads"] >= 200:
                    probability -= 10

            else:
                continue

            if random.randint(1, 100) <= probability:
                edge = (country, enemy)
                print(f"{country} is making demands on {enemy}!")

                if self.g.nodes[enemy]["coalition"] == "Neutral":
                    print(f"{enemy} can't oppose to a nuclear power")
                    self.g.add_edge(country, enemy, weight=5)
                    self.target.remove(enemy)

                elif self.g.has_edge(country, enemy):
                    self.g.edges[edge]["weight"] += 2
                    self.interactions.append(edge)

                else:
                    self.g.add_edge(country, enemy, weight=5)
                    self.interactions.append(edge)

            else:
                print(f"{country} preferred the status quo")

        return self.interactions

    def start_second_stage(self):
        probability = 33

        for interaction in self.start_first_stage():
            # Sezione se aggredito un leader
            if self.g.nodes[interaction[1]]["coalition"] == "Leader":

                if self.g.nodes[interaction[1]]["stance"] == "hard":
                    print(f"\n{interaction[1]} is uncompromising")

                    if self.g.nodes[interaction[1]]["n_warheads"] >= 300:
                        probability += 42

                    else:
                        probability += 32

                elif self.g.nodes[interaction[1]]["stance"] == "soft":
                    print(f"\n{interaction[1]} prefer to negotiate")

                    if self.g.nodes[interaction[1]]["n_warheads"] >= 300:
                        probability += 32

                    else:
                        probability += 22

                for country in self.g.nodes():
                    if self.g.nodes[country]["coalition"] == "West" or self.g.nodes[country]["coalition"] == "Leader" \
                            and self.g.nodes[country]["reliability"] == "reliable" \
                            and self.g.nodes[country] != interaction[1]:
                        print(f"{country} does support {interaction[1]}")
                        probability += 2.5

                    if self.g.nodes[country]["coalition"] == "West" or self.g.nodes[country]["coalition"] == "Leader" \
                            and self.g.nodes[country]["reliability"] == "unreliable" \
                            and self.g.nodes[country] != interaction[1]:
                        print(f"{country} doesn't support {interaction[1]}!")
                        probability -= 2.5

            # Sezione se aggredito protetto
            elif self.g.nodes[interaction[1]]["coalition"] == "West":

                if self.g.nodes[interaction[1]]["stance"] == "hard":
                    print(f"\n{interaction[1]} is uncompromising")
                    probability += 22

                elif self.g.nodes[interaction[1]]["stance"] == "soft":
                    print(f"\n{interaction[1]} prefer to negotiate")
                    probability += 15

                for country in self.g.nodes():
                    if self.g.nodes[country]["coalition"] == "West" or self.g.nodes[country]["coalition"] == "Leader" \
                            and self.g.nodes[country]["reliability"] == "reliable" \
                            and self.g.nodes[country] != interaction[1]:
                        print(f"{country} does support {interaction[1]}")
                        probability += 7

                    if self.g.nodes[country]["coalition"] == "West" or self.g.nodes[country]["coalition"] == "Leader" \
                            and self.g.nodes[country]["reliability"] == "unreliable" \
                            and self.g.nodes[country] != interaction[1]:
                        print(f"{country} doesn't support {interaction[1]}!")
                        probability -= 7

            # Decisione operata dal Paese aggredito
            if random.randint(1, 100) <= probability:
                print(f"\n{interaction[1]} will make no concessions!\n")
                self.g.edges[(interaction[0], interaction[1])]["weight"] -= 1
                self.deny.append(interaction)
                if self.g.nodes[interaction[1]]["coalition"] == "Leader":
                    self.increase_leader_prestige(interaction[1])
                    self.increase_ally_prestige(interaction[1])
                else:
                    self.increase_ally_prestige(interaction[1])

            else:
                print(f"\n{interaction[1]} will concede!\n")
                self.g.edges[(interaction[0], interaction[1])]["weight"] += 3
                if self.g.nodes[interaction[1]]["coalition"] == "Leader":
                    self.decrease_leader_prestige(interaction[1])
                    self.decrease_ally_prestige(interaction[1])
                else:
                    self.decrease_ally_prestige(interaction[1])
                self.increase_pact_prestige(interaction[0])
                self.increase_challenger_prestige(interaction[0])

        return self.deny

    def start_third_stage(self):
        ally_coalition = []
        deny_list = self.start_second_stage()
        if len(deny_list) > 1:
            for interaction in deny_list:
                for country in self.g.nodes():
                    if self.g.nodes[country]["coalition"] == "West" \
                            and self.g.nodes[country] != self.g.nodes[interaction[1]] \
                            and self.g.nodes[country]["reliability"] == "reliable":
                        probability = 80
                        if random.randint(1, 100) <= probability:
                            print(f"{country} will support {interaction[1]}!")
                            self.increase_ally_prestige(country)
                            ally_coalition.append(country)
                        else:
                            print(f"{country} will not support {interaction[1]}!")
                            self.decrease_ally_prestige(country)

                    elif self.g.nodes[country]["coalition"] == "West" \
                            and self.g.nodes[country] != self.g.nodes[interaction[1]] \
                            and self.g.nodes[country]["reliability"] == "unreliable":
                        probability = 40
                        if random.randint(1, 100) <= probability:
                            print(f"{country} will aid {interaction[1]}!")
                            self.increase_ally_prestige(country)
                            ally_coalition.append(country)
                        else:
                            print(f"{country} will not aid {interaction[1]}!")
                            self.decrease_ally_prestige(country)

                    elif self.g.nodes[country]["coalition"] == "Leader" \
                            and self.g.nodes[country] != self.g.nodes[interaction[1]] \
                            and self.g.nodes[country]["reliability"] == "reliable":
                        probability = 80
                        if random.randint(1, 100) <= probability:
                            print(f"{country} will aid {interaction[1]}!")
                            ally_coalition.append(country)
                            self.increase_ally_prestige(country)
                            self.increase_leader_prestige(country)
                        else:
                            print(f"{country} will not aid {interaction[1]}!")
                            self.decrease_ally_prestige(country)
                            self.decrease_leader_prestige(country)

                    elif self.g.nodes[country]["coalition"] == "Leader" \
                            and self.g.nodes[country] != self.g.nodes[interaction[1]] \
                            and self.g.nodes[country]["reliability"] == "unreliable":
                        probability = 40
                        if random.randint(1, 100) <= probability:
                            print(f"{country} will aid {interaction[1]}!")
                            ally_coalition.append(country)
                            self.increase_ally_prestige(country)
                            self.increase_leader_prestige(country)
                        else:
                            print(f"{country} will not aid {interaction[1]}!")
                            self.decrease_ally_prestige(country)
                            self.decrease_leader_prestige(country)

            probability_MW = 33
            challenger_coalition = []
            print("\nA war risk to erupt!!\n")
            for interaction in deny_list:
                challenger_coalition.append(interaction[0])
                for country in self.g.nodes():
                    if self.g.nodes[country]["coalition"] == "Anti-west" \
                            and self.g.nodes[country]["reliability"] == "reliable":
                        probability = 80
                        if random.randint(1, 100) <= probability:
                            print(f"{country} will aid {interaction[0]}!")
                            self.increase_challenger_prestige(country)
                            challenger_coalition.append(country)
                            probability_MW += 5
                        else:
                            print(f"{country} will not aid {interaction[0]}!")
                            self.decrease_challenger_prestige(country)
                            probability_MW -= 5

                    elif self.g.nodes[country]["coalition"] == "Anti-west" \
                            and self.g.nodes[country]["reliability"] == "unreliable":
                        probability = 40
                        if random.randint(1, 100) <= probability:
                            print(f"{country} will aid {interaction[0]}!")
                            self.increase_challenger_prestige(country)
                            challenger_coalition.append(country)
                            probability_MW += 5
                        else:
                            print(f"{country} will not aid {interaction[0]}!")
                            self.decrease_challenger_prestige(country)
                            probability_MW -= 5

                    elif self.g.nodes[country]["coalition"] == "Challenger" \
                            and self.g.nodes[country] != self.g.nodes[interaction[0]] \
                            and self.g.nodes[country]["reliability"] == "reliable":
                        probability = 80
                        if random.randint(1, 100) <= probability:
                            print(f"{country} will aid {interaction[0]}!")
                            challenger_coalition.append(country)
                            self.increase_challenger_prestige(country)
                            self.increase_pact_prestige(country)
                            probability_MW += 5

                        else:
                            print(f"{country} will not aid {interaction[0]}!")
                            self.decrease_challenger_prestige(country)
                            self.decrease_pact_prestige(country)
                            probability_MW -= 5

                    elif self.g.nodes[country]["coalition"] == "Challenger" \
                            and self.g.nodes[country] != self.g.nodes[interaction[0]] \
                            and self.g.nodes[country]["reliability"] == "unreliable":
                        probability = 40
                        if random.randint(1, 100) <= probability:
                            print(f"{country} will aid {interaction[0]}!")
                            challenger_coalition.append(country)
                            self.increase_challenger_prestige(country)
                            self.increase_pact_prestige(country)
                            probability_MW += 5

                        else:
                            print(f"{country} will not aid {interaction[0]}!")
                            self.decrease_challenger_prestige(country)
                            self.decrease_pact_prestige(country)
                            probability_MW -= 5

            if random.randint(1, 100) <= probability_MW:
                print("\nA war erupt!!")
                if len(challenger_coalition) > 1:
                    nuked_challenger = random.choice(challenger_coalition)
                else:
                    nuked_challenger = challenger_coalition[0]

                self.g.remove_node(nuked_challenger)
                print(f"{nuked_challenger} have been nuked!!")
                nuked_ally = random.choice(ally_coalition)
                print(f"{nuked_ally} have been nuked!!")
                self.g.remove_node(nuked_ally)
                self.target.remove(nuked_ally)

                for interaction in self.deny:
                    if nuked_challenger in interaction:
                        self.deny.remove(interaction)

            else:
                print(f"\n{challenger_coalition[0]} retires the demands")
                for edge in self.g.edges():
                    if edge[0] == challenger_coalition[0] and ((self.g.nodes[edge[1]]["coalition"] == "Challenger") or (
                            self.g.nodes[edge[1]]["coalition"] == "Anti-west")):
                        self.g.edges[edge]["weight"] -= 10
        else:
            return


    def update_status(self):
        for country in self.g.edges():
            if self.g.edges[country]["weight"] >= 9 and \
                    self.g.nodes[country[0]]["coalition"] == "Challenger" and \
                    self.g.nodes[country[1]]["coalition"] == "Neutral":
                self.g.nodes[country[1]]["coalition"] = "Anti-west"
                print(f"\n{country[1]} become an anti-west ally")

            elif self.g.edges[country]["weight"] >= 9 and \
                    self.g.nodes[country[0]]["coalition"] == "Challenger" and \
                    self.g.nodes[country[1]]["coalition"] == "West" :
                self.g.nodes[country[1]]["coalition"] = "Anti-west"
                for edge in self.g.edges():
                    if edge[1] == country[1] and edge[0] == self.g.nodes[country[1]]["coalition"] == "Leader":
                        self.g.remove_edge(edge[0], edge[1])
                print(f"\n{country[1]} become an anti-west ally")

            elif self.g.edges[country]["weight"] >= 9 and \
                    self.g.nodes[country[0]]["coalition"] == "Challenger" and \
                    self.g.nodes[country[1]]["coalition"] == "Leader" :
                self.g.nodes[country[1]]["coalition"] = "Anti-west"
                for edge in self.g.edges():
                    if edge[0] == country[1] and edge[0] == self.g.nodes[country[1]]["coalition"] == "West":
                        self.g.remove_edge(edge[0], edge[1])
                    elif edge[0] == country[1] and edge[0] == self.g.nodes[country[1]]["coalition"] == "Leader":
                        self.g.remove_edge(edge[0], edge[1])
                print(f"\n{country[1]} become an anti-west ally")

            elif self.g.edges[country]["weight"] <= 2 and \
                    self.g.nodes[country[0]]["coalition"] == "Challenger" and \
                    self.g.nodes[country[1]]["coalition"] == "Leader":
                self.g.remove_edge(country)
                print(f"\n{country[0]} failed to influence {country[1]}")

            elif self.g.edges[country]["weight"] <= 2 and \
                    self.g.nodes[country[0]]["coalition"] == "Leader" and \
                    self.g.nodes[country[1]]["coalition"] == "West":
                self.g.remove_edge(country[0], country[1])
                print(f"\n{country[0]} is no longer allied with {country[1]}")

            elif self.g.edges[country]["weight"] <= 2 and \
                    self.g.nodes[country[0]]["coalition"] == "Leader" and \
                    self.g.nodes[country[1]]["coalition"] == "Leader":
                self.g.remove_edge(country[0], country[1])
                print(f"\n{country[0]} is no longer allied with {country[1]}")

            elif self.g.edges[country]["weight"] <= 2 and \
                    self.g.nodes[country[0]]["coalition"] == "Challenger" and \
                    self.g.nodes[country[1]]["coalition"] == "Anti-west":
                self.g.remove_edge(country[0], country[1])
                print(f"\n{country[0]} is no longer allied with {country[1]}")

            elif self.g.edges[country]["weight"] <= 2 and \
                    self.g.nodes[country[0]]["coalition"] == "Challenger" and \
                    self.g.nodes[country[1]]["coalition"] == "Challenger":
                self.g.remove_edge(country[0], country[1])
                print(f"\n{country[0]} is no longer allied with {country[1]}")
