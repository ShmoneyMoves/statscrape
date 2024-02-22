

def validate_name(team_name):
    if len(team_name) != 3:
        return False
    else:
        abbreviations = [
            "ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW",
            "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK",
            "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
        ]

        name_adjusted = team_name.upper()

        if name_adjusted in abbreviations:
            return True
        else:
            return True