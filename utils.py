import math
from copy import deepcopy


def equaliser(teams, pivot):
    pivot = 2*pivot if 2*pivot < max([len(team) for team in teams]) else pivot
    teams = sorted(teams, key= lambda x: len(x), reverse = True)
    if len(teams) <= 0:
        raise ValueError("number of teams should be >0")
    if pivot > len(teams[0]):
        raise ValueError("pivot should be smaller or equal to max team size")

    equalised_distribution = [team[:pivot] for team in teams]
    empty_counts = [max(0, pivot - len(team)) for team in teams]
    empty_counts_1 = [max(0, pivot - len(team)) for team in teams]
    lacker_start = -1
    for i in range(len(empty_counts)):
        if empty_counts[i] >0:
            lacker_start = i
            break
    gap = sum(empty_counts)
    leftovers = [team[pivot:] for team in teams]
    [team.reverse() for team in leftovers]
    # extras = sum([len(x) for x in leftovers])
    counter = 0
    upper_lim = lacker_start
    print(upper_lim)
    while (counter < gap) and (upper_lim>0):
        for i in range(lacker_start, len(teams)):
            print("upper_lim",upper_lim)
            if not leftovers[counter % upper_lim]:
                upper_lim -= 1
            if upper_lim>0:
                if empty_counts[i]:
                    if leftovers[counter % upper_lim]:
                        leftovers[i].append(leftovers[counter % upper_lim].pop())
                        empty_counts[i] -= 1
                        counter += 1
            else:
                break
            if (counter >= gap) or (upper_lim == 0):
                break
    if upper_lim:
        counter = counter % upper_lim
        gap = gap + counter % upper_lim
        while (counter < gap) and upper_lim:
            for i in range(lacker_start, len(teams)):
                if not leftovers[counter % upper_lim]:
                    upper_lim -= 1
                if upper_lim:
                    if empty_counts_1[i]:
                        if leftovers[counter % upper_lim]:
                            leftovers[i].append(leftovers[counter % upper_lim].pop())
                            empty_counts_1[i] -= 1
                            counter += 1
                else:
                    break
                if counter >= gap:
                    break

    for i in range(len(teams)):
        equalised_distribution[i] += leftovers[i]
    return equalised_distribution


def get_pivot(teams):
    max_st = max([len(x) for x in teams])
    bits = len(bin(max_st)[2:])
    upper = math.pow(2,bits)
    lower = math.pow(2, bits-1)
    if max_st-lower > upper - max_st:
        return upper
    else:
        return lower

def replace_players(team1, team2):
    for i in range(min(len(team1),len(team2))):
        if i%2==0:
            team1[i], team2[i] = team2[i], team1[i]

def get_fixtures(teams, pivot):
    if len(teams)%2!=0:
        raise ValueError("count of teams should be divisible by 2")

    teams = deepcopy(teams)
    qualifiers = []
    for idx, team in enumerate(teams):
        if len(team)<=pivot:
            teams[idx] = team + ["NA"] * (pivot - len(team))
            continue
        extra = team[pivot:]
        extra.reverse()
        balance = team[pivot-len(extra):pivot]
        safe = team[:pivot-len(extra)]
        safe.extend(["qualifiers_" + str(i) for i in range(len(qualifiers), len(qualifiers)+len(balance))])
        qualifiers.extend([a+"_$vs$_"+b for a,b in zip(balance,extra)])
        teams[idx] = safe

    if len(teams)==4:
        replace_players(teams[0], teams[2])
        replace_players(teams[1],teams[3])
    knockouts = []
    team_pairs = [teams[i:i+2] for i in range(0,len(teams),2)]

    for idx, team_pair in enumerate(team_pairs):
        team_a, team_b = team_pair
        team_b.reverse()
        # print(team_a)
        # print("lol")
        # print(team_b)
        knockouts.extend([a + "_$vs$_" + b for a, b in zip(team_a, team_b)])

    return qualifiers, knockouts








if __name__ == "__main__":
    teams_1 = [[1, 2, 3, 4, 5, 6, 7, 8],
               [9, 10, 11, 12, 13],
               [15, 16, 17],
               [18, 19]]
    teams_2 = [[1, 2, 3, 4, 5, 6, 7, 8],
               [9, 10, 11, 12, 13, 20, 21, 22],
               [15, 16, 17],
               [18, 19]]
    teams_3 = [[1, 2, 3, 4, 5, 6, 7, 8],
               [9, 10, 11, 12, ],
               [15, 16, 17],
               [18, 19]]
    teams_4 = [[1, 2, 3, 4, 5, 6, 7],
               [9, 10, 11, 12],
               [15, 16, 17],
               [18, 19]]
    teams_5 = [[1, 2, 3, 4, 5, 6],
               [9, 10, 11, 12,7],
               [15, 16, 17],
               [18]]
    print(equaliser(teams_1, 4))
    print(equaliser(teams_2, 4))
    print(equaliser(teams_3, 4))
    print(equaliser(teams_4, 4))
    print(equaliser(teams_5, 4))

    print(get_pivot(teams_1))
    print(get_pivot(teams_2))
    print(get_pivot(teams_3))
    print(get_pivot(teams_4))
    print(get_pivot(teams_5))


