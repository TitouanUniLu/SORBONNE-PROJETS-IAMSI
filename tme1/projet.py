from itertools import permutations
import subprocess
import time

''' EXERCICE 1'''
def generate_dimacs_championship_schedule(ne, ns):
    n_teams = ne #nombre d'equipes
    n_days = 2 * ns #nombre de jours

    # generer les equipes
    equipes = [i for i in range(1,n_teams+1)] #je pars pas de zero mais de 1 ici
    print(f'liste de toutes les equipes: {equipes}')

    #toutes les permutations des equipes
    toutes_combinaisons = list(permutations(equipes, 2))
    print(f'toutes les combinaisons d\'equipes {toutes_combinaisons}')

    #creation du dico qui va contenir tous les matchs par jour
    all_matchs = {}
    day_incr = 1
    while day_incr <= n_days:
        all_matchs[f'jour{day_incr}'] = ''
        day_incr+=1

    #fonction pour determiner si deux tuple ont un elem en commun (utile pour savoir si deux matchs dans la meme journee sont possible)
    def have_common_element(tuple1, tuple2):
        set1 = set(tuple1)
        set2 = set(tuple2)
        return bool(set1.intersection(set2))
    
    #fonction pour determiner qui peut jouer dans la meme journee sans avoir de conflit
    def find_no_common_elements_sequence(elements, sequence=[]):
        if not elements:
            return sequence

        current_element = elements[0]
        rest_elements = elements[1:]

        next_element = next((elem for elem in rest_elements if not have_common_element(current_element, elem)), None)

        if next_element is not None:
            sequence.extend([current_element, next_element]) #on ajoute ici
            return find_no_common_elements_sequence([elem for elem in rest_elements if elem != next_element], sequence)
        else:
            no_match = 'empty'
            sequence.extend([current_element, no_match])
            #si on ne peut pas trouver d'element suivant, revenir en arriere
            return find_no_common_elements_sequence(rest_elements, sequence)
    res = find_no_common_elements_sequence(toutes_combinaisons)

    index = 0
    for jour in all_matchs:
        #extraire deux matchs pour chaque jour
        matches_for_jour = res[index:index+2]
        all_matchs[jour] = matches_for_jour
        index += 2

    print(f'listes des matchs pour chaque jour: {all_matchs}')

    
    return all_matchs

def dimacs_format(journees):
    dimacs_clauses = []
    equipe_ids = {}
    next_id = 1

    def get_equipe_id(equipe):
        nonlocal next_id
        if equipe not in equipe_ids:
            equipe_ids[equipe] = next_id
            next_id += 1
        return equipe_ids[equipe]

    for _, matches in journees.items():
        for match in matches:
            if match != 'empty':
                equipe1, equipe2 = match
                # Assigner des identifiants aux équipes
                id1, id2 = get_equipe_id(equipe1), get_equipe_id(equipe2)
                # Ajouter une clause pour chaque match
                dimacs_clauses.append((id1, id2))
            '''
            pour le moment si un des deux match ne se produit pas je skip mais faut peut etre changer plus tard
            '''

    # Construire la chaîne DIMACS
    dimacs_string = f"p cnf {len(equipe_ids)} {len(dimacs_clauses)}\n"
    for clause in dimacs_clauses:
        dimacs_string += f"{clause[0]} {clause[1]} 0\n"

    return dimacs_string[:-1] #je retire juste la derniere ligne a cause du \n
    

''' si le nombre de semaines donne est trop petit alors on pourra pas avoir tous les matchs. Il y en aura le max pr le nombre de semaines mais pas tous '''
# dimacs_championship_schedule = generate_dimacs_championship_schedule(4,3)
# dimacs_version = dimacs_format(dimacs_championship_schedule)

#save results
# with open("championat.dimacs", "w") as file:
#     file.write(dimacs_version)

''' EXERCICE 2'''
'''
Question 1. La formule du nombre total de variables propositionnelles est le produit du nombre total de jours nj et du nombre total d'équipes ne.
Cela garantit que chaque combinaison de chaque équipe et chaque match de la journée est représenté.
nombre de variables = nj x ne**2
'''

''' Question 2.'''
def codage(ne, nj, j, x, y):
    return j * ne**2 + x * ne + y + 1

#encoded = codage(ne, nj, j, x, y)

''' Question 3.'''
def decodage(k, ne):
    y = (k - 1) % ne
    x = ((k - 1 - y) // ne) % ne
    j = (k - 1 - y - x * ne) // (ne * ne)
    return j, x, y
#decoded = decodage(encoded, ne)

#print(f'Test codage/decodage: {decodage(encoded, ne) == (j,x,y)}') #test

''' EXERCICE 3'''
def au_moins_un_vrai(variables):
    cl = [str(var) for var in variables] + ["0"]
    return [" ".join(cl)]

def au_plus_un_vrai(variables):
    clauses = []
    n = len(variables)
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append(f"{-variables[i]} {-variables[j]} 0")
    return clauses
   

# print(f'Test question 1.1:\n {au_moins_un_vrai([1,2,3,4])}')
# print(f'Test question 1.2:\n {au_plus_un_vrai([1,2,3,4])}')

def dimacs_f(l):
    s = ''
    for elem in l:
        s += str(elem) + ' '
    s += '0'
    return s

''' Question 2.'''
def encoderC1(ne, nj):
    contraintes_C1 = []
    # Pour chaque équipe et chaque jour
    for jour in range(nj):
        for equipe in range(ne):
            home = [codage(ne, nj, jour, equipe, adversaire) for adversaire in range(ne) if adversaire != equipe]
            ext = [codage(ne, nj, jour, adversaire, equipe) for adversaire in range(ne) if adversaire != equipe]

            contraintes_C1.extend(au_plus_un_vrai(home + ext)) #dimacs_f(clause)
    return contraintes_C1

# print("C1")
# contraintes_C1 = encoderC1(ne, nj)
# print(f'contraintes: {contraintes_C1} \nnombre de contraintes: {len(contraintes_C1)}')
# ici pour 3 equipes et 4 jours on a 72 contraintes

def encoderC2(ne, nj):
    clauses = []
    for x in range(ne):
        for y in range(ne):
            if x != y:
                list_match = [codage(ne, nj, j, x, y) for j in range(nj)]
                clauses.extend(au_moins_un_vrai(list_match))
                clauses.extend(au_plus_un_vrai(list_match))
    return clauses
# print("C2")
# contraintes_C2 = encoderC2(ne,nj)
# print(f'contraintes: {contraintes_C2} \nnombre de contraintes: {len(contraintes_C2)}')

def encoder(ne, nj, ext_exo5=None):
    contraintes = encoderC1(ne, nj) + encoderC2(ne, nj)
    if ext_exo5 is not None:
        contraintes.extend(encoderC3(ne, nj)) # + encoderC4(ne, nj)
    with open("championnat.cnf", "w") as f:
        f.write(f"p cnf {ne**2 * nj - 1} {len(contraintes)}\n")
        # Ecrire les contraintes
        for contrainte in contraintes:
            f.write(contrainte + "\n")
    return contraintes

# encodedC12 = encoder(ne,nj)
# print(f'contraintes: {encodedC12} \nnombre de contraintes: {len(encodedC12)}')

def decoder(output_file, ne, nj, team_names_file=None):
    if team_names_file != None:
        with open(team_names_file, "r") as f:
            team_names = [line.strip() for line in f]
    else:
        team_names = None

    with open(output_file, "r") as f:
        output_lines = f.readlines()

    output = output_lines[0].split()

    if "UNSAT" in output: return "UNSAT"

    planning = {jour+1: [] for jour in range(nj)}
    for var in output:
        if int(var) > 0:
            j,x,y=decodage(int(var),ne)
            if team_names != None:
                planning[j+1].append((team_names[x], team_names[y]))
            else: planning[j+1].append((x,y))

    return planning

def call_glucose(glucose, timeout):
    try:
        # Run the command with a timeout
        return subprocess.run(glucose, shell=True, timeout=timeout, capture_output=True)
    except subprocess.TimeoutExpired:
        print("glucose execution timed out")
        return None
    except Exception as e:
        print(f"Error while running glucose: {e}")
        return None

# d = decoder('output.cnf',ne,nj)
# print(f'planning = {d}')

def joli_affichage(planning):
    print("Schedule:")
    for jour, matches in planning.items():
        print(f"Jour {jour}:")
        for match in matches:
            print(f"  Equipe {match[0]} vs Equipe {match[1]}")

def optimisation(ne,nj_min,nj_max,timeout, extension=None):
    nj = nj_min
    not_found = True
    while nj <=nj_max and not_found:
        contraintes = encoder(ne,nj,extension)
        print(f'execution of {nj} days -')
        output = call_glucose('./glucose championnat.cnf output.cnf', timeout)
        if output is not None:
            print(output)
            planning = decoder('output.cnf', ne, nj, 'equipes.txt')
            if planning == "UNSAT":
                nj+=1
            else:
                print("FOUND CORRECT NJ", nj)
                joli_affichage(planning)
                not_found = False
                return nj
        else:
            nj+=1
    return False

def au_plus_k(var,k):
    clauses = []
    n = len(var)
    for i in range(int(k)+1, n+1):
        for c in permutations(var, i):
            clause = [str(v) for v in c] + ["0"]
            clauses.append(" ".join(clause))
    return clauses

def au_moins_k(var, k):
    n_var = [-x for x in var]
    return au_plus_k(n_var, len(var)-k)

def encoderC3(ne,nj,exterieur=0.5,domicile=0.4):
    contraintes = []
    nb_min_dom = nj * ne * domicile // 100
    nb_min_ext = ne * nj * exterieur // 100
    for i in range(ne):
        for j in range(ne):
            if i!=j:
                domicile_c = [codage(ne, nj, y, i, j) for y in range(1, nj, 2)]
                contraintes.extend(au_moins_k(domicile_c,nb_min_dom))
                exterieur_c = [codage(ne, nj, y, j, i) for y in range(1, nj, 2)]
                contraintes.extend(au_moins_k(exterieur_c,nb_min_ext))
    return contraintes

def encoderC4(ne,nj):
    contraintes = []
    for i in range(nj):
        for x in range(ne):
            domicile_c = [codage(ne, nj, i, x, y) for y in range(ne) if y!=x]
            contraintes.extend(au_plus_k(domicile_c,2))
            exterieur_c = [codage(ne, nj, i, y, x) for y in range(ne) if y!=x]
            contraintes.extend(au_plus_k(exterieur_c,2))
    return contraintes

TIMEOUT = 10

EXERCICE4 = False
if EXERCICE4:
    ne = 10
    nj_min = 10
    nj_max = 20
    print(f'pour ne={ne}, nj_min={nj_min}, nj_max={nj_max}, le nj optimal est {optimisation(ne,nj_min,nj_max,TIMEOUT)}')

EXERCICE5 = True
if EXERCICE5:
    ne = 8
    nj_min = 10
    nj_max = 20
    extension = True
    print(f'pour ne={ne}, nj_min={nj_min}, nj_max={nj_max}, le nj optimal est {optimisation(ne,nj_min,nj_max,TIMEOUT, extension)}')
