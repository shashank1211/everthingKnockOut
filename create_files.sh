#!/bin/bash

sport="badminton"
teams=("sharks" "bulls" "hawks" "panthers")
categories=("men_singles" "women_singles" "men_doubles" "women_doubles" "mixed_doubles")

for team in "${teams[@]}"; do
    for category in "${categories[@]}"; do
        directory="teams/${sport}/${category}"
        team_file="${directory}/${team}.txt"

        # Create the directory if it doesn't exist
        mkdir -p "${directory}"
        
        # Create the text file for the team
        touch "${team_file}"

    done
done

echo "Text files created for all teams in ${sport} categories."