#const n=8. %par default c'est n = 8
%taille de l'echequier
ligne(1..n). 
col(1..n).

n { reine(I,J) : ligne(I), col(J) } n. % on a donc n reines

:- reine(I,J1), reine(I,J2), J1 != J2. % pas sur la meme colonne
:- reine(I1,J), reine(I2,J), I1 != I2. %pas sur la meme ligne
% contraintes pour les diagonales
:- reine(I,J), reine(II,JJ), (I,J) != (II,JJ), I+J == II+JJ.
:- reine(I,J), reine(II,JJ), (I,J) != (II,JJ), I-J == II-JJ.

% pour n = 6
% SATISFIABLE
% Models: 4

% pour n = 8
% SATISFIABLE
% Models: 92

% pour n = 10
% SATISFIABLE
% Models: 724

% pour n = 12
% 

%au dessus de 12 ca commence a prendre bcp de temps de calcul