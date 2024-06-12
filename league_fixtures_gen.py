import random


def generate_fixtures(players):

    random.shuffle(players)
    odd_num_players = False
    fixtures = []

    if len(players) % 2 != 0:
        odd_num_players = True
        players.append(None)  # Add a dummy player if the number of players is odd

    mid_point = len(players) // 2
    group_1 = players[:mid_point]
    group_2 = players[mid_point:]

    for index in range(len(group_1)):

        g1_player_index = index
        g2_p1_index = index
        g2_p2_index = index + 1

        if g2_p2_index == len(group_2):
            g2_p2_index = 0

        if group_2[g2_p1_index]:
            fixture_1 = (group_1[g1_player_index], group_2[g2_p1_index])
            fixtures.append(fixture_1)

        if group_2[g2_p2_index]:
            fixture_2 = (group_1[g1_player_index], group_2[g2_p2_index])
            fixtures.append(fixture_2)

    if odd_num_players:
        final_fixture = (group_1[-1], group_1[-2])
        fixtures.append(final_fixture)

    return fixtures


# Example usage:
# players = ["A", "B", "C", "D", "E", "F", "G", "H"]

player_file = "teams/chess/groups/group_4.txt"
with open(player_file, "r") as file:
    players = file.read().splitlines()

fixtures = generate_fixtures(players)

print(f"Total number of matches = {len(fixtures)}")
for fixture in fixtures:
    print(f"{fixture[0]} vs {fixture[1]}")
