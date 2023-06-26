function OnModel = AllOn(model,lowbound)
%
%USAGE:
%  OnModel = AllOn(model,lowbound)
%
%DESCRIPTION
% AllOn - function to turn on all inputs and outputs (ie. exchange 
%         reacttions) in a metabolic model. The upper bound for all
%         exchange reactions is set to 1000.
%
%INPUT
%  model       A COBRA formatted metabolic model
%
%  lowbound    The lower flux value to be assigned all exchange reactions.
%                 Should be a number < 0.
%
%OUTPUT
%  OnModel     A COBRA formatted model, now with all exchange reactions set
%               to having lower bound equal to lowbound.
%
%
%  Eivind Almaas 18/2/2011

m    = findExcRxns(model,0,0);
EX   = find(m > 0.5);
EXno = size(EX,1);
OnModel = model;
for i=1:EXno
    OnModel = changeRxnBounds(OnModel,model.rxns(EX(i)),lowbound,'l');
    OnModel = changeRxnBounds(OnModel,model.rxns(EX(i)),1000,'u');
end
