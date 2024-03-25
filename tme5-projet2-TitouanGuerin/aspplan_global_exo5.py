from parseur_exo4 import parsePDDLDomainToASP, parsePDDLProblemToASP, parseAction

''' A PARTIR DE L'EXO 4 ON VA ESSAYER DE GENERER UN PLAN POUR LES FICHIERS PDDL'''
import subprocess

def generate_minimal_plan(domain_file, problem_file, contraintes, max_steps=10):
    # Premièrement, la fonction prend en entrée les chemins vers les fichiers du domaine et du problème PDDL,
    # ainsi que les contraintes supplémentaires en format texte pour le solveur ASP et un nombre maximal d'étapes à tester.

    # Génération du programme ASP à partir des fichiers PDDL.
    # Cette étape convertit le domaine et le problème PDDL en leur équivalent ASP,
    # permettant ainsi d'utiliser un solveur ASP pour la planification.
    asp_domain = parsePDDLDomainToASP(domain_file)
    asp_problem = parsePDDLProblemToASP(problem_file)
    full_asp = asp_domain + asp_problem + contraintes

    # Le programme ASP complet est ensuite sauvegardé dans un fichier.
    filename = "programme_asp_exo5.lp"
    with open(filename, "w") as file:
        file.write(full_asp)

    # La boucle tente de trouver un plan en augmentant progressivement le nombre d'étapes.
    for steps in range(1, max_steps + 1):
        print(f"Trying to find a plan with {steps} step(s)...")
        # Construction de la commande pour Clingo avec un nombre limité d'étapes
        command = f"clingo {filename} --const n={steps}"
        # Exécution de Clingo
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Vérification si un plan a été trouvé
        if "UNSATISFIABLE" not in process.stdout:
            print(f"Plan found with {steps} step(s)!")
            print(process.stdout)
            return process.stdout
        else:
            print(process.stdout)
 
    print("No plan found within the step limit.")
    return None

asp_domaine =  parsePDDLDomainToASP('blockWorld-domain.pddl')

asp_probleme = parsePDDLProblemToASP('blockWorld-problem.pddl')

#contraintes
contraintes = """
% tout ce qui est défini par init(P) est établi comme vrai au temps 0
holds(P,0) :- init(P).

% La règle force l'exécution d'une et une seule action parmi toutes les actions possibles à chaque instant 'T', sauf au dernier instant 'n'
1 { perform(A,T) : action(A) } 1 :- time(T), T != n.

% une action 'A' ne peut avoir lieu à l'instant 'T' que si toutes ses préconditions 'P' sont satisfaites à cet instant
:- perform(A,T), not holds(P,T), pre(A,P), action(A), pred(P), time(T).

% si une action 'A' est exécutée à l'instant 'T', tous les effets positifs de cette action sont vrais au temps T+1
holds(P,T+1) :- perform(A,T), add(A,P), action(A), pred(P), time(T).

% un prédicat 'P' qui est vrai à l'instant 'T' reste vrai à T+1 sauf si une action effectuée à 'T' l'annule
holds(P,T+1) :- holds(P,T), not del(A,P), perform(A,T), action(A), pred(P), time(T).

% La règle garantit qu'aucune paire d'actions différentes ne peut être exécutée au même moment
:- perform(A1,T), perform(A2,T), action(A1), action(A2), A1 != A2, time(T).

% tous les prédicats définissant le but doivent être vrais à l'instant final 'n'
:- not holds(P,n), but(P), pred(P).

% Déclaration des objets (problem)
#const n=10.
time(0..n).

#show perform/2.
"""
generate_minimal_plan('blockWorld-domain.pddl', 'blockWorld-problem.pddl', contraintes)
