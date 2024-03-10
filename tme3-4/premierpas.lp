% conges. 
% temps_libre :- conges. 
% sortie_cine :- temps_libre, conges.
% OUTPUT AVEC CLINGO
% Reading from premierpas.lp
% Solving...
% Answer: 1
% conges temps_libre sortie_cine
% SATISFIABLE

% p :- not q.
% q :- not r.
% OUTPUT AVEC CLINGO
% Reading from premierpas.lp
% premierpas.lp:12:6-11: info: atom does not occur in any rule head:
%   not r
% 
% Solving...
% Answer: 1
% q
% SATISFIABLE

% p :- not q.
% q :- not p.
% r :- p.
% r :- q.
% OUTPUT AVEC CLINGO
% Reading from premierpas.lp
% Solving...
% Answer: 1
% p r
% Answer: 2
% q r
% SATISFIABLE

% p :- not q.
% q :- not p.
% r :- not r.
% r :- p.
% OUTPUT AVEC CLINGO
% Reading from premierpas.lp
% Solving...
% Answer: 1
% p r
% SATISFIABLE