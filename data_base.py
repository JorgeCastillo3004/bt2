import psycopg2
from common_functions import load_json
from unidecode import unidecode


def getdb():
    return psycopg2.connect(
                host="localhost",
                user="wohhu",
                password="caracas123",
        dbname='sports_db',
        )

def save_news_database(dict_news):  
    query = "INSERT INTO news VALUES(%(news_id)s, %(news_content)s, %(image)s,\
             %(published)s, %(news_summary)s, %(news_tags)s, %(title)s)"
    cur = con.cursor()
    cur.execute(query, dict_news)
    con.commit()

def save_sport_database(sport_dict):
    try:
        query = "INSERT INTO sport VALUES(%(sport_id)s, %(is_active)s, %(desc_i18n)s,\
                                         %(logo)s, %(sport_mode)s, %(name_i18n)s, %(point_name)s, %(name)s)"
        cur = con.cursor()
        cur.execute(query, sport_dict)
        con.commit()
    except:
        con.rollback()

def get_dict_sport_id():
    query = "SELECT sport.name, sport.sport_id FROM sport"
    # 
    # -- WHERE team.sport_id = '{}'
    cur = con.cursor()
    cur.execute(query)  
    dict_results = {row[0] : row[1] for row in cur.fetchall()}
    return dict_results

def save_league_info(dict_ligue_tornament): 
    query = "INSERT INTO league VALUES(%(league_id)s, %(league_country)s, %(league_logo)s, %(league_name)s, %(league_name_i18n)s, %(sport_id)s)"
    cur = con.cursor()                                                                           
    cur.execute(query, dict_ligue_tornament)                                                         
    con.commit()                                                                                     

def save_season_database(season_dict):
    query = "INSERT INTO season VALUES(%(season_id)s, %(season_name)s, %(season_end)s,\
                                     %(season_start)s, %(league_id)s)"
    cur = con.cursor()
    cur.execute(query, season_dict)
    con.commit()

def save_tournament(dict_tournament):
    query = "INSERT INTO tournament VALUES(%(tournament_id)s, %(team_country)s, %(desc_i18n)s,\
                                     %(end_date)s, %(logo)s, %(name_i18n)s, %(season)s, %(start_date)s, %(tournament_year)s)"
    cur = con.cursor()
    cur.execute(query, dict_tournament)
    con.commit()

def save_team_info(dict_team):
    query = "INSERT INTO team VALUES(%(team_id)s, %(team_country)s, %(team_desc)s,\
     %(team_logo)s, %(team_name)s, %(sport_id)s)"
    cur = con.cursor()                                                                           
    cur.execute(query, dict_team)                                                        
    con.commit()

def save_league_team_entity(dict_team):
    query = "INSERT INTO league_team VALUES(%(instance_id)s, %(team_meta)s, %(team_position)s, %(league_id)s, %(season_id)s, %(team_id)s)"  
    cur = con.cursor()
    cur.execute(query, dict_team)
    con.commit()

def save_player_info(dict_team):    
    query = "INSERT INTO player VALUES(%(player_id)s, %(player_country)s, %(player_dob)s,\
     %(player_name)s, %(player_photo)s, %(player_position)s)"
    cur = con.cursor()
    cur.execute(query, dict_team)
    con.commit()

def save_team_players_entity(player_dict):
    query = "INSERT INTO team_players_entity VALUES(%(player_meta)s, %(season_id)s, %(team_id)s,\
     %(player_id)s)"
    cur = con.cursor()
    cur.execute(query, player_dict)
    con.commit()

def get_team_id(league_id, season_id, team_name):
    query = """
    SELECT t2.team_id \
    FROM league_team AS t1\
    JOIN team AS t2 ON t1.team_id = t2.team_id\
    WHERE t1.league_id = '{}' AND t1.season_id = '{}' AND t2.team_name = '{}'""".format(league_id, season_id, team_name)

    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchone()
    return results[0]

def get_seasons(league_id, season_name):
    query = "SELECT season_name, season_id FROM season  WHERE league_id ='{}' and season_name = '{}';".format(league_id, season_name)
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    for row in cur.fetchall():
        print(row)
    return results

def get_list_id_teams(sport_id, team_country, team_name):
    query = """SELECT team_id FROM team WHERE sport_id ='{}' and team_country = '{}' and team_name = '{}';""".format(sport_id, team_country, team_name)
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results

def get_dict_results(table= 'league', columns = 'sport_id, league_country, league_name, league_id'):    
    query = f"SELECT {columns} FROM {table};"   
    cur = con.cursor()
    cur.execute(query)
    dict_results = {row[0] + '_'+ row[1] + '_' + row[2]: row[3] for row in cur.fetchall()}
    return dict_results

def get_dict_teams(sport_id = 'FOOTBALL'):
    query = """
    SELECT league.league_country, team.team_name, team.team_id\
    FROM team \
    JOIN league_team ON team.team_id = league_team.team_id\
    JOIN league league_team.league_id = league.league_id    
    WHERE team.id_sport = '{}'""".format(sport_id)

    cur = con.cursor()
    cur.execute(query)

    dict_results = {unidecode('-'.join(row[0].replace('&', '').split() ) ).upper():\
                    {'team_name': unidecode('-'.join(row[1].split() ) ).upper(),\
                     'team_id': row[2]} for row in cur.fetchall()}
    return dict_results

def get_dict_league_ready(sport_id = 'TENNIS'):
    query = """
        SELECT team.sport_id, team.team_country, league.league_country, team.team_name, team.team_id
        FROM team
        JOIN league_team ON team.team_id = league_team.team_id
        JOIN league ON league_team.league_id = league.league_id
        WHERE team.sport_id = '{}'""".format(sport_id)
    # 
    # -- WHERE team.sport_id = '{}'
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    dict_results = {}
    for row in results: 
        dict_results.setdefault(row[0], {}).setdefault(row[1], {}).setdefault(row[2], {})[row[3]] = {'team_id': row[4]} 

    return dict_results

######################################## FUNCTIONS RELATED TO MATCHS ########################################
def save_math_info(dict_match):
    dict_match['rounds'] = ' '.join(dict_match['rounds'].split())

    print("dict_match: ", dict_match['statistic'])
    table_dict = {
    "match_id": 255,
    "match_country": 80,
    "end_time": 1,  # No es una cadena de caracteres
    "match_date": 1,  # No es una cadena de caracteres
    "name": 70,
    "place": 128,
    "start_time": 1,  # No es una cadena de caracteres
    "league_id": 40,
    "stadium_id": 255,
    "tournament_id": 255,
    "rounds": 40,
    "season_id": 40,
    "status": 40,
    "statistic": 1600}

    for key, value in dict_match.items():
        try:
            print(f"{key} {len(value)}/{table_dict[key]} {value}")
        except:
            print("Possible error: ")
            print(f"key: {key}, value:{value} #")
    query = "INSERT INTO match VALUES(%(match_id)s, %(match_country)s, %(end_time)s,\
     %(match_date)s, %(name)s, %(place)s, %(start_time)s, %(rounds)s, %(season_id)s, \
         %(status)s, %(statistic)s, %(league_id)s, %(stadium_id)s)"
    cur = con.cursor()
    cur.execute(query, dict_match)
    con.commit()

def save_details_math_info(dict_match):
    query = "INSERT INTO match_detail VALUES(%(match_detail_id)s, %(home)s, %(visitor)s,\
     %(match_id)s, %(team_id)s)"
    cur = con.cursor()
    cur.execute(query, dict_match)
    con.commit()

def save_score_info(dict_match):
    query = "INSERT INTO score_entity VALUES(%(score_id)s, %(points)s, %(match_detail_id)s)"
    cur = con.cursor()
    cur.execute(query, dict_match)
    con.commit()

def save_stadium(dict_match):
    query = "INSERT INTO stadium VALUES(%(stadium_id)s, %(capacity)s, %(country)s,\
     %(desc_i18n)s, %(name)s, %(photo)s)"
    cur = con.cursor()
    cur.execute(query, dict_match)
    con.commit()

def get_rounds_ready(league_id, season_id):
    query = "SELECT DISTINCT rounds FROM match WHERE league_id = '{}' AND season_id = '{}';".format(league_id, season_id)   
    print("query inside rounds ready: ")
    print(query)
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results

def check_league_duplicate(league_id):
    query = "SELECT league_id FROM league WHERE league_id ='{}';".format(league_id) 
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results

def check_season_duplicate(season_id):
    query = "SELECT season_id FROM season WHERE season_id ='{}';".format(season_id) 
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results

def check_player_duplicates(player_country, player_name, player_dob):
    query = "SELECT player_id FROM player WHERE player_country ='{}' AND player_name ='{}' AND player_dob ='{}';".format(player_country, player_name, player_dob)
    print("Check player duplicates")
    print(query)
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results

def check_player_duplicates_id(player_id):
    query = "SELECT player_id FROM player WHERE player_id ='{}';".format(player_id) 
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results

def check_team_duplicates(team_name, sport_id):
    query = "SELECT team_id FROM team WHERE team_name ='{}' AND sport_id ='{}';".format(team_name, sport_id)
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results

def check_team_duplicates_id(team_id):
    query = "SELECT team_id FROM team WHERE team_id ='{}';".format(team_id)
    print("check team duplicates")
    print(query)
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results

def get_team_id_f1(team_name):
    query = f"SELECT team_id, team_name FROM team WHERE team_desc ='{team_name}'"
    cur = con.cursor()
    cur.execute(query)  
    results = {row[0]: row[1] for row in cur.fetchall()}
    return results

def get_team_id_pilot(racer_name, team_name):    
    dict_team_id = get_team_id_f1(team_name)
    for team_id, complete_name in dict_team_id.items():        
        if racer_name.upper().split()[0] in complete_name.upper().split():
            return team_id

def check_team_season_duplicates(league_id, season_id, team_id):
    query = "SELECT season_id FROM league_team WHERE league_id ='{}' AND season_id ='{}' AND team_id ='{}';".format(league_id, season_id, team_id)
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results

def check_team_player_entitiy(season_id, team_id, player_id):
    query = """SELECT player_id FROM team_players_entity WHERE
                 season_id ='{}' AND team_id ='{}' AND player_id ='{}';""".format(season_id, team_id, player_id)
    cur = con.cursor()
    cur.execute(query)  
    results = [row[0] for row in cur.fetchall()]
    return results  

def get_match_id(league_country, league_name, match_date, match_name):
    
    query = """
    SELECT match.match_id
    FROM match
    JOIN league ON league.league_id = match.league_id
    WHERE league.league_country = '{}' and 
    league.league_name = '{}' and 
    match.match_date = '{}' and match.name = '{}'""".format(league_country, league_name, match_date, match_name)    
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchone()

def get_math_details_ids(match_id):
    query = """
    SELECT match_detail_id, home FROM match_detail
     WHERE match_id = '{}';""".format(match_id);
    cur = con.cursor()
    cur.execute(query)

    dict_results = {row[0]:row[1] for row in cur.fetchall()}
    return dict_results

def get_match_ready(match_id):
    query = "SELECT MATCH_ID FROM MATCH WHERE MATCH_ID='{}';".format(match_id)  
    cur = con.cursor()
    cur.execute(query)
    results = [row[0] for row in cur.fetchall()]
    return results

def check_match_duplicate(league_id, match_date, match_name):
    query = """SELECT MATCH_ID FROM MATCH WHERE LEAGUE_ID ='{}'
                 AND MATCH_DATE='{}' AND NAME='{}';""".format(league_id, match_date, match_name)    
    print(query)
    cur = con.cursor()
    cur.execute(query)
    results = [row[0] for row in cur.fetchall()]
    return results

def get_stadium_id(place_name):
    query = """SELECT STADIUM_ID FROM STADIUM WHERE NAME ='{}';""".format(place_name)   
    cur = con.cursor()
    cur.execute(query)
    results = [row[0] for row in cur.fetchall()]
    return results

def check_stadium(stadium_id):
    query = """SELECT STADIUM_ID FROM STADIUM WHERE stadium_id ='{}';""".format(stadium_id) 
    cur = con.cursor()
    cur.execute(query)
    results = [row[0] for row in cur.fetchall()]
    return results

def update_score(params):
    query = "UPDATE score_entity SET points = %(points)s WHERE match_detail_id = %(match_detail_id)s"
    # query = "INSERT INTO score_entity VALUES(%(score_id)s, %(points)s, %(match_detail_id)s)"
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()

def update_match_status(params):
    query = "UPDATE match SET status = %(status)s WHERE match_id = %(match_id)s"
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()

def get_match_by_day():
    # Query to retrieve pending matches for updating.
    query = """
        SELECT sport.name, league.league_name, league.league_country,\
        match.match_date, match.start_time, match.name, match.match_id \
        FROM MATCH 
        JOIN LEAGUE ON MATCH.LEAGUE_ID = LEAGUE.LEAGUE_ID
        JOIN SPORT ON SPORT.SPORT_ID = LEAGUE.SPORT_ID
        WHERE MATCH.MATCH_DATE = CURRENT_DATE       
        """
    # AND MATCH.STATUS = 'P' 
    cur = con.cursor()
    cur.execute(query)    
    return cur.fetchall()

def get_match_by_league_name(league_name_, month_number, day_number):
    # Query to retrieve pending matches for updating.
    query = f"""
        SELECT sport.name, league.league_name, league.league_country,
               match.match_date, match.start_time, match.name, match.match_id
        FROM MATCH 
        JOIN LEAGUE ON MATCH.LEAGUE_ID = LEAGUE.LEAGUE_ID
        JOIN SPORT ON SPORT.SPORT_ID = LEAGUE.SPORT_ID
        WHERE LEAGUE.LEAGUE_NAME LIKE '{league_name_}' AND
              MATCH.STATUS = 'P' AND
              EXTRACT(MONTH FROM match.match_date) = {month_number} AND
              EXTRACT(DAY FROM match.match_date) = {day_number}
    """ 
    cur = con.cursor()
    cur.execute(query)    
    return cur.fetchall()

def get_match_update():
    # Query to retrieve pending matches for updating.
    query = """
        SELECT sport.name, league.league_name, league.league_country,\
        match.match_date, match.start_time, match.name, match.match_id \
        FROM MATCH 
        JOIN LEAGUE ON MATCH.LEAGUE_ID = LEAGUE.LEAGUE_ID
        JOIN SPORT ON SPORT.SPORT_ID = LEAGUE.SPORT_ID
        WHERE MATCH.MATCH_DATE <= CURRENT_DATE AND \
        START_TIME < CURRENT_TIME AND \
        MATCH.STATUS = 'P' 
        """
    cur = con.cursor()
    cur.execute(query)    
    return cur.fetchall()

con = getdb()