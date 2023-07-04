import re, json, math, random#, requests, pandas as pd, copy
from colorama import Fore, Back, Style, init
from replit import db
from tabulate import tabulate

init(autoreset=True)

def init_globals():
  global pokedex, movesdata, moves, moves_formatted, typeChart, allnatures, reSymbols, turn

  pokedex = json.loads(open('pokedex.txt').read())
  
  movesdata = json.loads(open('moves.txt').read())
  moves = movesdata.keys()
  moves_formatted = open('allmoves.txt').read().splitlines()
  turn = 0
  allnatures = open('allnatures.txt').read().splitlines()
  reSymbols = "[ &,.*!-:]"

  typeChart = json.loads(open('type_chart.txt').read())

#print(pokedex["cofagrigus"]["abilities"]["0"])

#chrstc_list = list(pokedex["bulbasaur"].keys())

#------------- test for data | UNUSED; FOR TESTING -------------#

def init_data():
  pokemon_test = input("Select your Pokemon. ").lower()
  
  for count, chrstc in enumerate(chrstc_list):
    print(count, "-", chrstc)
  
  chrstc = int(input("Select a characteristic to view. Indices only. "))
  print(pokedex[pokemon_test][chrstc_list[chrstc]])



#------------ ask game mode --------------#

def ask_gameMode():
  gameMode = input(Fore.LIGHTGREEN_EX + """What game mode would you like to play?
  
======================================

1 | Sandbox | Choose your own Pokemon
2 | Random  | Random Pokemon*

*Levels and Natures are also randomized.

Movesets will be chosen later. This choice will not affect movesets.

======================================

Enter index of mode to play with:
""" + Fore.RESET)

  return gameMode

#------------ select pokemon -------------#

def give_randomPokemon():
  global p1_pokemon, p1_pokemonName, p1_level, p1_nature
  global p2_pokemon, p2_pokemonName, p2_level, p2_nature

  p1_pokemon_index = random.randrange(0, len(pokedex.keys()))
  p1_pokemonName = pokedex[list(pokedex.keys())[p1_pokemon_index]]['name']
  p1_pokemon = eval(f"(re.sub(r'{reSymbols}','', p1_pokemonName.lower()))")


  p1_level = random.randrange(0, 100)
  p1_nature = allnatures[random.randrange(0, 25)]

  p2_pokemon_index = random.randrange(0, len(pokedex.keys()))
  p2_pokemonName = pokedex[list(pokedex.keys())[p2_pokemon_index]]['name']
  p2_pokemon = eval(f"(re.sub(r'{reSymbols}','', p2_pokemonName.lower()))")

  p2_level = random.randrange(0, 100)
  p2_nature = allnatures[random.randrange(0, 25)]


#------------------------------------#  

def ask_selectPKMN():
  global p1_pokemon, p1_pokemonName, p1_level, p1_nature
  global p2_pokemon, p2_pokemonName, p2_level, p2_nature
  
  print(Fore.RED + "Player 1, select your Pokemon:", end=' ')
  p1_pokemonName = input()
  p1_pokemon = eval(f"(re.sub(r'{reSymbols}','', p1_pokemonName.lower()))")
  
  if p1_pokemon == 'test':
    return 'test'

  print(Fore.RED + "(Type 'help' for Nature information)\nNature:", end=' ')
  p1_nature = input().title()
  
  if p1_nature == 'Help':
    list_natures(); print(Fore.RED + "\nNature:", end=' '); p1_nature = input().title()
  
  print(Fore.RED + "Level:", end=' ')
  p1_level = int(input())
  
  print(Fore.BLUE + "Player 2, select your Pokemon:", end=' ')
  p2_pokemonName = input()
  p2_pokemon = eval(f"(re.sub(r'{reSymbols}','', p2_pokemonName.lower()))")

  print(Fore.BLUE + "Nature:", end=' ')
  p2_nature = input().title()
  
  if p2_nature == 'Help':
    list_natures(); print(Fore.BLUE + "\nNature:", end=' '); p2_nature = input().title()

  print(Fore.BLUE + "Level:", end=' ')
  p2_level = int(input())


#------------- list natures in selection -------------#

def list_natures():
  print('\n'+'\n'.join(open('natures.txt').read().splitlines()))

  
#------------- declare stats of players' pokemon -------------#

#Forgive me, for I have sinned.
def init_statDictionaries(player):
  exec(f'''global {player}_stats;{player}_values = [pokedex[{player}_pokemon]["baseStats"][key] for key in dict.keys(pokedex[{player}_pokemon]["baseStats"])]
{player}_keys = ["{player}_hp", "{player}_atk", "{player}_def", "{player}_spa", "{player}_spd", "{player}_spe"]
{player}_stats = dict(zip({player}_keys, {player}_values))
{player}_stats["{player}_level"], {player}_stats["{player}_nature"], {player}_stats["{player}_pkmn"] = {player}_level, {player}_nature, {player}_pokemon''')  

#------------- initialize all stats -------------#
def init_stats():
  global p1_stats, p2_stats #, p1_stats_2, p2_stats_2

  #makes list of natures and their buffs (buffs contained as corresponding key indeces to the stat dictionaries)
  naturebuffs = open('naturesbuffs.txt').read().splitlines()
  naturebuffs = [str(i) for i in naturebuffs] ; naturebuffs = [i.split(' ') for i in naturebuffs] 
  
  #creates stat dictionaries for players' pokemon
  #creates values (stat values) and keys (stat names); zips them. Also adds in the level and nature.
  init_statDictionaries('p1'); init_statDictionaries('p2')

    
#calc stats

  #calc HP
  p1_stats['p1_hp'] = math.floor(((2 * p1_stats['p1_hp']) * p1_stats['p1_level']) / 100 + p1_stats['p1_level'] + 10)
  p2_stats['p2_hp'] = math.floor(((2 * p2_stats['p2_hp']) * p2_stats['p2_level']) / 100 + p2_stats['p2_level'] + 10)
  

  #calc all other stats
  for i in p1_stats.keys():
    if list(p1_stats.keys()).index(i) < 6 and list(p1_stats.keys()).index(i) > 0:
      p1_stats[i] = math.floor((2 * p1_stats[i] * p1_stats['p1_level']) / 100 + 5)
      
  
  for i in p2_stats.keys():
    if list(p2_stats.keys()).index(i) < 6 and list(p2_stats.keys()).index(i) > 0:
      p2_stats[i] = math.floor((2 * p2_stats[i] * p2_stats['p2_level']) / 100 + 5)
      

  #adds types to stats dict
  p1_stats.update({'p1_types' : pokedex[p1_pokemon]['types']})
  p2_stats.update({'p2_types' : pokedex[p2_pokemon]['types']})
  
  #calc nature
  do_natures(naturebuffs, 'p1')
  do_natures(naturebuffs, 'p2')

  p1_stats['statChanges'] = {'atk': [2, 2], 'def': [2, 2], 'spa': [2, 2], 'spd': [2, 2], 'spe': [2, 2]}
  p2_stats['statChanges'] = {'atk': [2, 2], 'def': [2, 2], 'spa': [2, 2], 'spd': [2, 2], 'spe': [2, 2]}


  #p1_stats_2 = copy.deepcopy(p1_stats)
  #p2_stats_2 = copy.deepcopy(p2_stats)

#------- do the natures -------#
def do_natures(naturebuffs, player):

  for i in naturebuffs:
    if eval(f"{player}_stats['{player}_nature'] in i and {player}_stats['{player}_nature'] not in ['Hardy','Docile','Bashful','Quirky','Serious']"):
      #now, we take i[1] and i[2] (the indices of what stats are changed). We find the associated stat. 
      do_natureBuffs(*find_changedStat(i, player, naturebuffs))

      
#------------- do the stat changes from nature -------------#

def do_natureBuffs(upperstat, lowerstat, player):
  if player == 'p1':
    p1_stats[upperstat] *= 1.1
    p1_stats[lowerstat] *= 0.9
    p1_stats[upperstat] = math.floor(p1_stats[upperstat]); p1_stats[lowerstat] = math.floor(p1_stats[lowerstat])
  else:
    p2_stats[upperstat] *= 1.1
    p2_stats[lowerstat] *= 0.9
    p2_stats[upperstat] = math.floor(p2_stats[upperstat]); p2_stats[lowerstat] = math.floor(p2_stats[lowerstat])
    

#------------- find the changed stats from nature -------------#

def find_changedStat(i, player, naturebuffs):
  
  upperstat_IDX = int(naturebuffs[naturebuffs.index(i)][1])
  lowerstat_IDX = int(naturebuffs[naturebuffs.index(i)][2])
  
  upperstat = list(p1_stats.keys())[upperstat_IDX] if player == 'p1' else list(p2_stats.keys())[upperstat_IDX]
  lowerstat = list(p1_stats.keys())[lowerstat_IDX] if player == 'p1' else list(p2_stats.keys())[lowerstat_IDX]

  return upperstat, lowerstat, player

  
#------------- ask about move settings -------------#
def ask_moveSettings():
  
  print(Fore.LIGHTGREEN_EX + """
How do you want to create your movesets?

======================================

1 | Pre-set | All moves are the default for the level
2 | Choose  | Create movesets based on valid moves for the Pokemon*
3 | Sandbox | All moves are allowed on all Pokemon.
4 | Random  | All moves are completely random. 

*(TMs and Egg Moves included)

======================================

Enter index of mode to play with:
""", end='')

  moveSetting = input()
  while moveSetting not in ("3", "4"):
    moveSetting = input("That game mode is not functional at this moment. Please choose a different index. ")
  return int(moveSetting)

#------------- make move-sets -------------#
def init_movesets(moveSetting, player):
  
  print()

  if player == "p1": 
    fore = Fore.RED 
  else: fore = Fore.BLUE
    
  global p1_moves
  global p2_moves
  
  if moveSetting == 1: #Pre-set
    print(1)
  elif moveSetting == 2: #Choose
    print(2)
    
    
  elif moveSetting == 3: #Sandbox
    
    exec(f"""for i in range(1,5):
      while len({player}_moves) != 4:
        try: 
          move_to_add = input(f'{fore}' + 'Player {player[1]}, select move: ')
          if move_to_add == 'test' and len({player}_moves) == 0:
            {player}_moves.extend(("Scary Face","Calm Mind","Flame Charge","Mud Shot"))
            break
          (moves_formatted[moves_formatted.index(move_to_add)])
          {player}_moves.append(move_to_add)
        except ValueError as excep: 
          print('Move not valid. Please re-type.'); continue
        print({player}_moves)""")


  #---------------------------------#
    
  else: #Random
    exec(f"""while len({player}_moves) != 4: 
      move_to_add = moves_formatted[random.randrange(0, 900)]
      if move_to_add not in {player}_moves:
        {player}_moves.append(move_to_add)""")

  exec(f'{player}_stats["{player}_moves"] = {player}_moves')



  # ************** BATTLE ************** #

def init_TurnStart(player):
  exec(f'''
global {player}_turn_start
{player}_turn_start = []

{player}_turn_start.append("Player 1" if player == 'p1' else "Player 2")
{player}_turn_start.append({player}_pokemonName)
{player}_turn_start.append({player}_stats["{player}_level"])
{player}_turn_start.append({player}_stats["{player}_hp"])
''')
  
  for i in eval(f"{player}_stats['statChanges'].keys()"):
    exec(f"{player}_turn_start.append({player}_stats['{player}_{i}'] * ({player}_stats['statChanges'][i[-3:]][0] / {player}_stats['statChanges'][i[-3:]][1]) / {player}_stats['{player}_{i}'])")
    

  if player == "p1":
    return p1_turn_start
  else: return p2_turn_start


#------------------------ MOVE -----------------------------#
  
def tell_TurnStart():

  global turn 
  turn += 1

  #print(init_TurnStart("p1"), init_TurnStart("p2"))
  table_keys = ["Player","Pokemon", "Level","Current HP", "Atk Buff", "Def Buff", "SpA Buff", "SpD Buff", "Spe Buff", "Status"]
  table_values = list(zip(table_keys, init_TurnStart("p1"),init_TurnStart("p2")))

  print(Fore.RESET + "\n======================================")
  print(f'\nTurn {turn}')
  print(tabulate(table_values, floatfmt = ".2f"))
  print()

#------------------------------------------------#

def find_TurnOrder():
  if p1_stats['p1_spe'] > p2_stats['p2_spe']:
    return ['p1', 'p2']
  else: return ['p2','p1']


#--------- Damage Calc Multipliers --------#
  
def weather():
  return 1

def critical():
  crit_chance = 6.25
  random_num = random.randrange(0, 400)
  if random_num // 4 <= crit_chance:
    print(Fore.YELLOW + "\nA critical hit!")
    return True
  else: 
    return False

def random_roll():
  random_mult = random.randrange(85, 100) / 100
  return random_mult
  
def STAB(player, move):
  if eval(f"movesdata['{move}']['type'] in {player}_stats['{player}_types']"):
    return 1.5
  else: return 1
    
def is_burned():
  return 1


def type_effectiveness(target, move):
  #typeChart (dict)
  moveType = movesdata[move]['type'].lower()
  
  defenseTypes = list(map(lambda i: i.lower(), eval(f"{target}_stats['{target}_types']")))
                          
  move_effectives = typeChart[moveType]

  move_mults = []
  for i in defenseTypes:
    move_mults.append(move_effectives[i])

  multiplier = math.prod(move_mults)

  #prints the effectiveness of the move
  if multiplier == 2 or multiplier == 4:
    print(Fore.YELLOW + "It's super effective!")
  elif multiplier == 0.5 or multiplier == 0.25:
    print(Fore.YELLOW + "It's not very effective...")
  elif multiplier == 0:
    print(Fore.YELLOW + "It had no effect.")
    
  return multiplier



def attacker_AtkorSpa(player, move):
  if movesdata[move]['category'] == "Physical":
    move_category = 'atk'
    return eval(f"{player}_stats['{player}_atk'] * return_statMultiplier(player, move_category)")
  else:
    move_category = 'spa'
    return eval(f"{player}_stats['{player}_spa'] * return_statMultiplier(player, move_category)")


def target_AtkorSpa(target, move):
  if movesdata[move]['category'] == "Physical":
    move_category = 'def'
    return eval(f"{target}_stats['{target}_def'] * return_statMultiplier(target, move_category)")
  else:
    move_category = 'spd'
    return eval(f"{target}_stats['{target}_spd'] * return_statMultiplier(target, move_category)")
    
# ------------------------ #

def do_damage(player, target, move):

#damage calc (add critical ignoring stat changes (separate calcs for if critical and if not)) 

  if critical():
    damage = eval(f"math.floor(((((((2 * {player}_stats['{player}_level']) / 5) + 2) * movesdata['{move}']['basePower'] * (attacker_AtkorSpa(player, move) / target_AtkorSpa(target, move))) / 50) + 2) * weather() * 1.5 * random_roll() * STAB('{player}', '{move}') * type_effectiveness(target, move) * is_burned())")
    #Check how stats are calculated and somehow nullify the defensive stat changes. Please. (STILL DO 7.23)
  else: 
    damage = eval(f"math.floor(((((((2 * {player}_stats['{player}_level']) / 5) + 2) * movesdata['{move}']['basePower'] * (attacker_AtkorSpa(player, move) / target_AtkorSpa(target, move))) / 50) + 2) * weather() * random_roll() * STAB('{player}', '{move}') * type_effectiveness(target, move) * is_burned())")

  if damage == 0:
    damage = 1

  hp_after_damage = eval(f"{target}_stats['{target}_hp'] - {damage}")
  if hp_after_damage > 0: 
    exec(f"{target}_stats['{target}_hp'] = {hp_after_damage}")
  else: 
    exec(f"{target}_stats['{target}_hp'] = 0")


#------------- Make stat multiplier ---------------#

def make_statMultiplier(player, changedStat, changedStatValue):

  print(changedStat, changedStatValue, eval(f"{player}_stats['statChanges']['{changedStat}'][0]"), eval(f"{player}_stats['statChanges']['{changedStat}'][1]"))
  
  if changedStatValue > 0:
    if eval(f"{player}_stats['statChanges']['{changedStat}'][0] == 6"):
      print(f"Player{player[-1]}'s {changedStat} can't be raised any higher!")
    elif eval(f"{player}_stats['statChanges']['{changedStat}'][0] + {changedStatValue} > 6"):
      exec(f"{player}_stats['statChanges']['{changedStat}'][0] = 6")
    else:
      exec(f"{player}_stats['statChanges']['{changedStat}'][0] += changedStatValue")
    
    
  else:
    
    if eval(f"{player}_stats['statChanges']['{changedStat}'][1] == 8"):
      print("That stat can't go any lower!")
    elif eval(f"{player}_stats['statChanges']['{changedStat}'][1] - {changedStatValue} > 8"):
      exec(f"{player}_stats['statChanges']['{changedStat}'][1] = 8")
    else:
      exec(f"{player}_stats['statChanges']['{changedStat}'][1] -= changedStatValue")

  stat_numerator = eval(f"{player}_stats['statChanges']['{changedStat}'][0]")
  stat_denominator = eval(f"{player}_stats['statChanges']['{changedStat}'][1]")

  stat_multiplier = stat_numerator / stat_denominator

  return stat_multiplier

#-------------------- small func: gives fraction value of stat changes --#

def return_statMultiplier(player, move_category):

  #working
  stat_multiplier = eval(f"{player}_stats['statChanges']['{move_category}'][0] / {player}_stats['statChanges']['{move_category}'][1]")
  
  return stat_multiplier
  
#----------------- Do stat change -----------------#

def do_statChange(player, target, selected_move):

    if movesdata[selected_move]['target'] == "self":
      move_target = player
    else: 
      move_target = target

    changedStats = list(movesdata[selected_move]['boosts'].keys())
    changedStatValues = list(movesdata[selected_move]['boosts'].values())
  
    for enum, stat in enumerate(changedStats):
      stat_multiplier = make_statMultiplier(move_target, stat, changedStatValues[enum])

      #WORKING. IT CHANGES {player}_stats accordingly.
      """if move_target == 'p1':
        p1_stats[f'p1_{stat}'] *= stat_multiplier
      else: 
        p2_stats[f'p2_{stat}'] *= stat_multiplier""" 
      #Maybe don't use... Let's see if we can change the stats indirectly, using the multiplier +/ fraction values -- not changing the stat directly.
    
  
#------------- Check accuracy (check if move hits) --------------#

def check_moveHit(player, move):

  moveAccuracy = eval(f"movesdata['{move}']['accuracy']")

  if moveAccuracy == True:
    print(f"\n{player.title()} used {movesdata[move]['name']}!")
    return True
    
  randomNum = random.randint(0, 99)
  
  if randomNum in range(moveAccuracy):
    print(f"\n{player.title()} used {movesdata[move]['name']}!")
    return True
  else: 
    print(f"\n{player.title()} used {movesdata[move]['name']}!\nThe move missed!")
    return False

#------------------ Secondary Effects ------------------#

    #------- check if secondary happens (hits) -------#

def check_Hit(chance):

  if chance == True:
    return True
    
  randomNum = random.randint(0, 99)

  if randomNum in range(chance):
    return True
    
    #------ secondary stat change ------#

def do_secondaryStatChange_self(move_target, move, secondary):
  changedStats = list(secondary["self"]["boosts"].keys())
  changedStatValues = list(secondary["self"]["boosts"].values())
  for enum, stat in enumerate(changedStats):
    stat_multiplier = make_statMultiplier(move_target, stat, changedStatValues[enum])

def do_secondaryStatChange_boosts(move_target, move, secondary):
  changedStats = list(secondary["boosts"].keys())
  changedStatValues = list(secondary["boosts"].values())
  for enum, stat in enumerate(changedStats):
    stat_multiplier = make_statMultiplier(move_target, stat, changedStatValues[enum])


    #---------- do secondary ------------#
def do_secondary(player, target, move):
  secondary = movesdata[move]["secondary"]

  if check_Hit(secondary["chance"]):
    if "self" in secondary:
      do_secondaryStatChange_self(player, move, secondary)
    elif "boosts" in secondary:
      do_secondaryStatChange_boosts(target, move, secondary)
    else: pass
      
            #{'dustproof', 'status', 'self', 'volatileStatus', 'chance', 'boosts'} 
            #boosts = to other player, self = to self
    
#------------ MOVE ----------------#

def move(player, selected_move):

  if player == "p1":
    if movesdata[selected_move]['target'] == "self":
      target = "p1"
    else: 
      target = "p2"
  else:
    if movesdata[selected_move]['target'] == "self":
      target = "p2"
    else:
      target = "p1"


  
  if check_moveHit(player, selected_move):
    if player == "p1":
      if movesdata[selected_move]['category'] != 'Status': 
        do_damage('p1', target, selected_move)
        
      if "boosts" in movesdata[selected_move]:
        do_statChange('p1', target, selected_move)

      if movesdata[selected_move]["secondary"] != None:
        do_secondary(player, target, selected_move)
        
    else:
        
      if movesdata[selected_move]['category'] != 'Status':  
        do_damage('p2', target, selected_move)
      else: 
        return 1
         #DO STATUS
        #will add remaining turns, percentage to break free (thaw for freeze), and % damage done each turn to player_stats dictionary. There may be more that I'm missing, but I know that those three are critical.
        # Also, add this ^ to the p1 case. Haha.
      if "boosts" in movesdata[selected_move]:
        do_statChange('p2', target, selected_move)
        
      if movesdata[selected_move]["secondary"] != None:
        do_secondary(player, target, selected_move)

#------------ Select Move ---------------#

def select_move(player):
  newline = "\n"
  if player == "p1": 
    fore = Fore.RED 
  else: fore = Fore.BLUE

  fore2 = Fore.LIGHTYELLOW_EX

  valid_move = False
  while valid_move == False:
    player_moves = eval(f'{player}_moves')
    selected_move = input(f"""{fore}Player {player[-1]}, your moves are: 
{(", ".join(player_moves))}
For information on a move, type '/data [move]'.
{fore2}Select your move: """)
    
    #checks for valid move and /data
    if eval(f"(selected_move.title()) not in {player}_moves"):
      if "/data" in selected_move:
        selected_move = (re.sub(reSymbols,"", selected_move)).lower()
        selected_move = re.sub("'", "", selected_move)
        selected_move = selected_move[4:]
        print(selected_move)
        
        try:
          move_blurb = f"{movesdata[selected_move[5:]]['shortDesc']}\nBase Power: {movesdata[selected_move[5:]]['basePower']}"
          print('\n' + Fore.RESET + move_blurb + '\n')
        except: print("Invalid input. Please re-type.\n")

      
      else: print("Move not valid. Please re-type.\n")
    else: 
      selected_move = (re.sub(reSymbols,"", selected_move)).lower()
      selected_move = re.sub("'", "", selected_move)
      valid_move = True

  return selected_move

#--------------------------------#

def checkWin():
  if p1_stats['p1_hp'] == 0:
    print(Fore.CYAN + "P2 Won!")
    return False
  elif p2_stats['p2_hp'] == 0:
    print(Fore.CYAN + "P1 Won!")
    return False
    
#---------------------------#
  
def do_turn(player):
  
  tell_TurnStart()
  move(player, select_move(player))
  
#------------------------------------------------#
def do_battle():
  global in_battle
  in_battle = True

  while in_battle == True:
    for player in find_TurnOrder():
      if checkWin() == False: 
        in_battle = False
        break
      do_turn(player)


#------------------- main ---------------------#

if __name__ == "__main__":

  init_globals()

  if ask_gameMode() == "2":
    give_randomPokemon()
  else: 
    if ask_selectPKMN() == 'test':
      p1_pokemon = 'abomasnow'; p1_pokemonName = pokedex[p1_pokemon]['name']; p1_level = 50; p1_nature = 'Adamant'; p2_pokemon = 'raikou'; p2_pokemonName = pokedex[p2_pokemon]['name']; p2_level = 40; p2_nature = 'Serious'
  
  init_stats()
  #print(f"\nP1 Stats: {p1_stats}")
  #print(f"\nP2 Stats: {p2_stats}")
  
#prints "X vs Y" (cosmetic) 
  print("\n",p1_pokemonName, "vs", p2_pokemonName,"\n")

  moveSetting = ask_moveSettings()
  
  p1_moves = []
  p2_moves = []
  init_movesets(moveSetting, 'p1');init_movesets(moveSetting,'p2')
  p1_stats.update({'p1_status' : None, 'p1_statusTurnCount' : 0, 'p1_statusChanceThaw' : 0});
  p2_stats.update({'p2_status' : None, 'p2_statusTurnCount' : 0, 'p2_statusChanceThaw' : 0}) 
  
  do_battle()

#5.23.23 vjerovatno neće prenijeti na VB. previše i previše različito (želim da ovo ostane bazirano na tekstu. smiješno je)
