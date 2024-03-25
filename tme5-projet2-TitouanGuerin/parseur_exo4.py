from pddl.formatter import domain_to_string, problem_to_string
from pddl import parse_domain
import re
from pyparsing import OneOrMore, nestedExpr

import re


def parseAction(elem):
    action_str = ""
    
    # tirets sont supprimés pour le formatage ASP
    # pour convertir le nom de l'action en un identifiant conforme aux conventions de nommage ASP.
    action_name = elem[1].replace('-', '')
    
    # Les paramètres de l'action sont récupérés et formatés.
    # Chaque paramètre est transformé en majuscule pour suivre une convention de nommage claire et est préfixé par son type.
    params_index = [i+1 for i, x in enumerate(elem) if x == ':parameters'][0]
    params_list = elem[params_index]
    params_str = ", ".join([f"{param[1:].upper()}" for param in params_list if param.startswith('?')])
    block_str = ", ".join([f"block({param[1:].upper()})" for param in params_list if param.startswith('?')])
    # La déclaration de l'action dans le format ASP inclut ses paramètres et leurs types.
    action_str += f"\naction({action_name}({params_str})) :- {block_str}.\n" if params_str else f"action({action_name}).\n"
    
    # Extraction et formatage des préconditions
    # Si plusieurs préconditions sont présentes (indiquées par 'and'), chacune est traitée séparément.
    # Si une précondition est 'handempty', elle est traitée comme un cas spécial sans paramètres.
    pre_index = [i+1 for i, x in enumerate(elem) if x == ':precondition'][0]
    preconditions = elem[pre_index]
    if preconditions[0] == 'and':
        # Gestion des multiples préconditions
        for pre in preconditions[1:]:
            if pre[0] == 'handempty':
                action_str += f"pre({action_name}, handempty) :- action({action_name}({params_str})).\n"
            else:
                pre_params = ", ".join([f"{p[1:].upper()}" for p in pre[1:]])
                action_str += f"pre({action_name}({params_str}), {pre[0]}({pre_params})) :- action({action_name}({params_str})).\n"
    else:
        # Gestion d'une seule précondition sans 'and'
        pre = preconditions
        if pre[0] == 'handempty':
            action_str += f"pre({action_name}, handempty) :- action({action_name}({params_str})).\n"
        else:
            pre_params = ", ".join([f"{p[1:].upper()}" for p in pre[1:]])
            action_str += f"pre({action_name}({params_str}), {pre[0]}({pre_params})) :- action({action_name}({params_str})).\n"
    
    # Extraction et formatage des effets
    # Les effets de l'action sont traités de manière similaire aux préconditions.
    # Les effets sont séparés en 'ajoutés' et 'supprimés' selon qu'ils sont précédés de 'not'.
    effect_index = [i+1 for i, x in enumerate(elem) if x == ':effect'][0]
    effects = elem[effect_index]
    if effects[0] == 'and':
        # Gestion des multiples effets
        for effect in effects[1:]:
            eff_params = ", ".join([f"{p[1:].upper()}" for p in effect[1][1:]]) if effect[0] == 'not' else ", ".join([f"{p[1:].upper()}" for p in effect[1:]])
            effect_str = f"{effect[1][0]}({eff_params})" if effect[0] == 'not' else f"{effect[0]}({eff_params})"
            effect_type = "del" if effect[0] == 'not' else "add"
            action_str += f"{effect_type}({action_name}({params_str}), {effect_str}) :- action({action_name}({params_str})).\n"
    else:
        # Gestion d'un seul effet sans 'and'
        effect = effects
        eff_params = ", ".join([f"{p[1:].upper()}" for p in effect[1:]])
        effect_str = f"{effect[0]}({eff_params})"
        effect_type = "add"
        action_str += f"{effect_type}({action_name}({params_str}), {effect_str}) :- action({action_name}({params_str})).\n"

    return action_str

def parsePDDLDomainToASP(filename):
    with open(filename, "r") as file:
        content = file.read()

    # Nettoyage du contenu PDDL (suppression des commentaires)
    content = re.sub(r';.*?\n', " ", content)  
    # Utilisation de pyparsing pour créer une structure imbriquée basée sur les parenthèses
    content = OneOrMore(nestedExpr()).parseString(content)

    asp_str = "%%% MONDE DES BLOCS (DOMAIN) %%%\n"
    
    # Parcours des éléments du domaine pour extraire prédicats et actions
    for elem in content[0]:
        if elem[0] == ':predicates':
            asp_str += "\n%%% Déclaration des prédicats (domain) %%%\n"
            for pred in elem[1:]:
                pred_name = pred[0]
                # Gérer les paramètres et les types
                if len(pred) > 1:
                    params = ""
                    conditions = []
                    for i in range(1, len(pred), 3):
                        var_name = pred[i][1:].upper()  # Extraire et formater le nom de la variable
                        var_type = pred[i+2] # Extraire le type de variable
                        params += f"{var_name}," # Construire la chaîne de paramètres
                        conditions.append(f"{var_type}({var_name})") # Construire les conditions de type
                    params = params[:-1]  # Enlever la dernière virgule
                    conditions_str = ','.join(conditions) # Joindre les conditions de type en une seule chaîne
                    # Générer et ajouter la déclaration de prédicat au code ASP
                    asp_str += f"pred({pred_name.lower()}({params})) :- {conditions_str}.\n"
                else:
                    # Générer et ajouter la déclaration de prédicat sans paramètres au code ASP
                    asp_str += f"pred({pred_name.lower()}).\n"
        # Appel a parseAction pour traiter les actions
        if elem[0] == ':action':
            asp_str += parseAction(elem) + "\n\n"

    return asp_str

# same logique !
def parsePDDLProblemToASP(filename):
    with open(filename, "r") as file:
        content = file.read()

    content = re.sub(r';.*?\n', " ", content)  # Nettoyage du contenu
    content = OneOrMore(nestedExpr()).parseString(content)

    asp_str = "\n%%% PROBLEME %%%\n"

    # Itérer sur les éléments du problème pour traiter domaine, objets, état initial et but
    for elem in content[0]:
        # Traiter le domaine
        if elem[0] == ':domain':
            domain = elem[1]
            asp_str += f"%%% Domaine: {domain} %%%\n"
        # Traiter les objets
        elif elem[0] == ':objects':
            asp_str += "\n%%% Declaration of objects (problem)%%%\n"
            recording_type = False
            object_type = ""
            
            for item in elem[1:]:
                if item == '-':
                    recording_type = True
                elif recording_type:
                    recording_type = False  
                else:
                    asp_str += f"{elem[-1]}({item.lower()}).\n"
        # Traiter l'état initial
        elif elem[0] == ':init':
            asp_str += "\n%%% Etat initial %%%\n"
            for state in elem[1:]:
                # Construire la chaîne représentant l'état
                if state[0] == 'not':
                    state_str = 'not(' + ','.join(state[1]) + ')'
                else:
                    state_str = state[0] + ('(' + ','.join(state[1:]) + ')' if state[0].lower() != 'handempty' else '')
                asp_str += f"init({state_str.lower()}).\n"
        # Traiter le but
        elif elem[0] == ':goal':
            asp_str += "\n%%% But %%%\n"
            but = elem[1]
            if but[0] == 'and': # Si plusieurs buts sont définis avec 'and'
                for g in but[1:]:
                    if g[0] == 'not':
                        but_str = 'not(' + ','.join(g[1]) + ')'
                    else:  # Si un seul but est défini
                        but_str = g[0] + ('(' + ','.join(g[1:]) + ')' if g[0].lower() != 'handempty' else '')
                    asp_str += f"but({but_str.lower()}).\n"
            else:
                if but[0] == 'not':
                    but_str = 'not(' + ', '.join(but[1]) + ')'
                else:
                    but_str = but[0] + ('(' + ','.join(but[1:]) + ')' if but[0].lower() != 'handempty' else '')
                asp_str += f"but({but_str.lower()}).\n"
    
    return asp_str


# Ici on mets le fichier pddl a utiliser
asp_domaine =  parsePDDLDomainToASP('blockWorld-domain.pddl')

asp_probleme = parsePDDLProblemToASP('blockWorld-problem.pddl')

full_asp = asp_domaine + asp_probleme


filename = "programme_asp_exo4.lp"  # Chemin vers le fichier à sauvegarder
with open(filename, "w") as file:
    file.write(full_asp)



