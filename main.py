import os
from utils import get_pivot, get_fixtures, equaliser
import pandas as pd
import math


def get_teams(folder):
    files = os.listdir(folder)
    teams = []
    for file in files:
        suffix = file.split("_")[-1]
        players = [x.strip() + "_" + suffix for x in open(folder + "/" + file, "r").readlines()]
        teams.append(players)
    return teams


def generate_fixtures(teams, pivot=None, save_folder=None):
    if pivot is None:
        pivot = get_pivot(teams)
    eq_teams = equaliser(teams, pivot)
    print(eq_teams)
    qualifiers, knockouts = get_fixtures(eq_teams, pivot)
    if save_folder:
        os.makedirs(save_folder)
        qualifiers_df = pd.DataFrame([{"rounds": "qualifiers_" + str(i),
                                       "player1": value.split("_$vs$_")[0],
                                       "player2": value.split("_$vs$_")[1]} for i, value in
                                      enumerate(qualifiers)]).reset_index()
        qualifiers_df.to_csv(save_folder + "/qualifiers.csv")

        knockouts_df = pd.DataFrame([{"rounds": "round_of_" + str(pivot * 4) + "_" + str(i),
                                      "player1": value.split("_$vs$_")[0],
                                      "player2": value.split("_$vs$_")[1]} for i, value in
                                     enumerate(knockouts)]).reset_index()
        qualifiers_df.to_csv(save_folder + "/qualifiers.csv")
        knockouts_df.to_csv(save_folder + "/round_of_" + str(pivot * 4)+".csv")
        # with open(save_folder + "/qualifiers.txt", "w") as f:
        #     f.write("\n".join(qualifiers))
        # with open(save_folder + "/knockouts.txt", "w") as f:
        #     f.write("\n".join(knockouts))
    return qualifiers, knockouts


def divide_fixtures(player_set):
    match_length = len(player_set) // 2
    if match_length == 1:
        data = [{"rounds": "round_of_2_0", "winner_of_1": "round_of_4_0", "winner_of_2": "round_of_4_1"}]
        return pd.DataFrame(data)

    else:
        fixtures = []
        chunk_size = len(player_set) // 4
        set_1 = player_set[:chunk_size]
        set_2 = player_set[chunk_size:2 * chunk_size]
        set_3 = player_set[2 * chunk_size:3 * chunk_size]
        set_4 = player_set[3 * chunk_size:]
        fixtures.extend(list(zip(set_1, set_4)))
        second_set = list(zip(set_3, set_2))
        print(len(player_set), int(math.log(len(player_set),2))%2==0)
        if int(math.log(len(player_set),2))%2!=0:
            second_set.reverse()
        fixtures.extend(second_set)
        fixtures = [{"rounds": "round_of_" + str(len(player_set)) + "_" + str(i),
                     "winner_of_1": value[0],
                     "winner_of_2": value[1]}
                    for i, value in enumerate(fixtures)]
        return pd.DataFrame(fixtures)


def generate_static_fixtures(pivot, save_folder):
    init_round = pivot * 4
    player_set = ["round_of_" + str(init_round) + "_" + str(i) for i in range(2 * pivot)]
    further_set = []
    rounds = int(math.log(init_round, 2))
    for _ in range(rounds):
        if len(player_set) == 1:
            break
        further_set.append({"fixtures": divide_fixtures(player_set), "round": "round_of_" + str(len(player_set))})
        further_set[-1]["fixtures"].to_csv(save_folder + "/" + further_set[-1]["round"] + ".csv")
        init_round = init_round // 2
        player_set = ["round_of_" + str(init_round) + "_" + str(i) for i in range(len(player_set) // 2)]
    return further_set


if __name__ == '__main__':
    # inp_folder = "teams/badminton/mixed_doubles"
    # out_folder = "games_v3/"
    # teams = get_teams(inp_folder)
    # print(generate_fixtures(teams, 4, save_folder="games_v3/mixed_doubles"))
    # generate_static_fixtures(4, save_folder="games_v3/mixed_doubles")
    #
    # inp_folder = "teams/badminton/men_doubles"
    # teams = get_teams(inp_folder)
    # print(generate_fixtures(teams, 8, save_folder="games_v3/men_doubles"))
    # generate_static_fixtures(8, save_folder="games_v3/men_doubles")
    #
    # inp_folder = "teams/badminton/men_singles"
    # teams = get_teams(inp_folder)
    # print(generate_fixtures(teams, 16, save_folder="games_v3/men_singles"))
    # generate_static_fixtures(16, save_folder="games_v3/men_singles")
    #
    # inp_folder = "teams/badminton/doubles"
    # teams = get_teams(inp_folder)
    # print(generate_fixtures(teams, 4, save_folder="games_v3/doubles"))
    # generate_static_fixtures(4, save_folder="games_v3/doubles")
    #
    # inp_folder = "teams/badminton/women_singles"
    # teams = get_teams(inp_folder)
    # print(generate_fixtures(teams, 4, save_folder="games_v3/women_singles"))
    # generate_static_fixtures(4, save_folder="games_v3/women_singles")



    out_folder = "games_tableTennis_v3/"

    inp_folder = "teams/tableTennis/men_singles"
    teams = get_teams(inp_folder)
    print(generate_fixtures(teams, 16, save_folder=f"{out_folder}/men_singles"))
    generate_static_fixtures(16, save_folder=f"{out_folder}/men_singles")
    #
    # inp_folder = "teams/tableTennis/women_singles"
    # teams = get_teams(inp_folder)
    # print(generate_fixtures(teams, 2, save_folder=f"{out_folder}/women_singles"))
    # generate_static_fixtures(2, save_folder=f"{out_folder}/women_singles")

    inp_folder = "teams/tableTennis/men_doubles"
    teams = get_teams(inp_folder)
    print(generate_fixtures(teams, 8, save_folder=f"{out_folder}/men_doubles"))
    generate_static_fixtures(8, save_folder=f"{out_folder}/men_doubles")

    # inp_folder = "teams/tableTennis/women_doubles"
    # teams = get_teams(inp_folder)
    # print(generate_fixtures(teams, 1, save_folder=f"{out_folder}/women_doubles"))
    # generate_static_fixtures(1, save_folder=f"{out_folder}/women_doubles")








