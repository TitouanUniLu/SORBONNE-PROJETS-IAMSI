from itertools import permutations

def generate_dimacs_championship_schedule(ne, ns):
    n_teams = ne #nombre d'equipes
    n_days = 2 * ns #nombre de jours

    # generer les equipes
    equipes = [i for i in range(1,n_teams+1)]
    print(f'liste de toutes les equipes: {equipes}')

    #toutes les permutations des equipes
    toutes_combinaisons = list(permutations(equipes, 2))

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
            equipe1, equipe2 = match
            # Assigner des identifiants aux équipes
            id1, id2 = get_equipe_id(equipe1), get_equipe_id(equipe2)
            # Ajouter une clause pour chaque match
            dimacs_clauses.append((id1, id2))

    # Construire la chaîne DIMACS
    dimacs_string = f"p cnf {len(equipe_ids)} {len(dimacs_clauses)}\n"
    for clause in dimacs_clauses:
        dimacs_string += f"{clause[0]} {clause[1]} 0\n"

    return dimacs_string[:-1] #je retire juste la derniere ligne a cause du \n
    

#exemple, j'ai verifie a la main et j'ai les meme resultats
dimacs_championship_schedule = generate_dimacs_championship_schedule(4, 3)
dimacs_version = dimacs_format(dimacs_championship_schedule)

#save results
with open("championat.dimacs", "w") as file:
    file.write(dimacs_version)
