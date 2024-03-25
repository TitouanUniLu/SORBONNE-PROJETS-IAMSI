%%% MONDE DES BLOCS (DOMAIN) %%%

%%% Déclaration des prédicats (domain) %%%
pred(on(X,Y)) :- block(X),block(Y).
pred(ontable(X)) :- block(X).
pred(clear(X)) :- block(X).
pred(handempty).
pred(holding(X)) :- block(X).

action(pickup(X)) :- block(X).
pre(pickup(X), clear(X)) :- action(pickup(X)).
pre(pickup(X), ontable(X)) :- action(pickup(X)).
pre(pickup, handempty) :- action(pickup(X)).
del(pickup(X), ontable(X)) :- action(pickup(X)).
del(pickup(X), clear(X)) :- action(pickup(X)).
del(pickup(X), handempty()) :- action(pickup(X)).
add(pickup(X), holding(X)) :- action(pickup(X)).



action(putdown(X)) :- block(X).
pre(putdown(X), holding(X)) :- action(putdown(X)).
del(putdown(X), holding(X)) :- action(putdown(X)).
add(putdown(X), ontable(X)) :- action(putdown(X)).
add(putdown(X), clear(X)) :- action(putdown(X)).
add(putdown(X), handempty()) :- action(putdown(X)).



action(stack(X, Y)) :- block(X), block(Y).
pre(stack(X, Y), holding(X)) :- action(stack(X, Y)).
pre(stack(X, Y), clear(Y)) :- action(stack(X, Y)).
del(stack(X, Y), holding(X)) :- action(stack(X, Y)).
del(stack(X, Y), clear(Y)) :- action(stack(X, Y)).
add(stack(X, Y), handempty()) :- action(stack(X, Y)).
add(stack(X, Y), on(X, Y)) :- action(stack(X, Y)).



action(unstack(X, Y)) :- block(X), block(Y).
pre(unstack(X, Y), on(X, Y)) :- action(unstack(X, Y)).
pre(unstack(X, Y), clear(X)) :- action(unstack(X, Y)).
pre(unstack, handempty) :- action(unstack(X, Y)).
add(unstack(X, Y), holding(X)) :- action(unstack(X, Y)).
add(unstack(X, Y), clear(Y)) :- action(unstack(X, Y)).
del(unstack(X, Y), on(X, Y)) :- action(unstack(X, Y)).
del(unstack(X, Y), handempty()) :- action(unstack(X, Y)).



%%% PROBLEME %%%
%%% Domaine: blockWorld %%%

%%% Declaration of objects (problem)%%%
block(a).
block(b).
block(c).
block(d).

%%% Etat initial %%%
init(clear(c)).
init(on(c,d)).
init(ontable(d)).
init(clear(b)).
init(on(b,a)).
init(ontable(a)).
init(handempty).

%%% But %%%
but(on(a,b)).
but(on(b,c)).
but(on(c,d)).
but(ontable(d)).
but(handempty).

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
