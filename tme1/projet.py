from itertools import permutations

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
dimacs_championship_schedule = generate_dimacs_championship_schedule(4,3)
dimacs_version = dimacs_format(dimacs_championship_schedule)

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
def codage(ne, j, x, y):
    return j * ne**2 + x * ne + y + 1

#changer les valeurs ici
ne = 4 
j = 1   
x = 2   
y = 0   
encoded = codage(ne, j, x, y)

''' Question 3.'''
def decodage(k, ne):
    k -= 1
    j = k // (ne**2)
    remainder = k % (ne**2)
    x = remainder // ne
    y = remainder % ne
    return j, x, y
decoded = decodage(encoded, ne)

print(f'Test codage/decodage: {decodage(codage(ne,j,x,y), ne) == (j,x,y)}') #test

''' EXERCICE 3'''
''' Question 1.'''
def au_moins_un_vrai(variables):
    clause = [str(v) for v in variables] + ["0"]
    return [" ".join(clause)]

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
    for equipe in range(1, ne+1):
        for jour in range(1, nj+1):
            home = [codage(jour, equipe, ne, adversaire) for adversaire in range(1, ne+1) if adversaire != equipe]
            ext = [codage(jour, equipe, adversaire, ne) for adversaire in range(1, ne+1) if adversaire != equipe]

            contraintes_C1.extend(au_plus_un_vrai(home + ext)) #dimacs_f(clause)
    return contraintes_C1

print("C1")
contraintes_C1 = encoderC1(ne=3, nj=4)
print(f'contraintes: {contraintes_C1} \nnombre de contraintes: {len(contraintes_C1)}')
# ici pour 3 equipes et 4 jours on a 72 contraintes

def encoderC2(ne, nj):
    clauses = []
    for x in range(ne):
        for y in range(ne):
            if x != y:
                list_match = [codage(ne, j, x, y) for j in range(nj)]
                clauses.extend(au_moins_un_vrai(list_match))
                clauses.extend(au_plus_un_vrai(list_match))
    return clauses
print("C2")
contraintes_C2 = encoderC2(3,4)
print(f'contraintes: {contraintes_C2} \nnombre de contraintes: {len(contraintes_C2)}')
