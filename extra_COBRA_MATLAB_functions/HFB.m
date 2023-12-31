function [numb,res,names] = HFB(model,flux_vector)

%
% [numb,res,names] = HFB(model,flux_vector)
%
% Function calculates the High-Flux Backbone.  Note that if two or more 
%              reactions have the same (max) rate for a metabolite, all are
%              potentially included in the HFB. This function uses the
%              COBRA Toolbox.
%
%
%VARIABLES:
% model        contains the COBRA Toolbox formatted constrain-based model
% flux_vector  contains the COBRA Toolbox formatted vector of fluxes from 
%              which the HFB will be extracted
%
% numb         returns the number of reactions participating in the HFB
% res          is a vector of all reactions, with 0 (no) or 1 (yes)
%              denoting if that reaction was part of the HFB
% names        is a vector of reaction names of only the HFB participants
%
%
%EXAMPLE USE:
%  data = optimizeCbModel(model,'max');
%  [numb res names] = HFB(model,data.x);
%
% Please cite the following paper:
%      E. Almaas, B. Kovacs, T. Vicsek, Z.N. Oltvai and A.-L. Barab�si. 
%      �Global organization of metabolic fluxes in the bacterium 
%       Escherichia coli.� Nature 427, 839 (2004).
%

mets = size(model.mets,1);
rxns = size(model.rxns,1);

prod_cand = zeros(rxns,1);
pp        = 0;
cons_cand = zeros(rxns,1);
pc        = 0;

%First, find all largest consuming and producing reactions
for i=1:mets
    j    = find(model.S(i,:));
    n    = size(j,2);
    bigp = +1e-7;   %Numerical cut-off for fluxes to be considered nonzero
    bign = -1e-7;
    indp = zeros(1,200);
    fp   = 0;
    indn = zeros(1,200);
    fn   = 0;
    if n > 0
        %Loop over all the reactions metabolite i participates in.
        for k=1:n
            value = model.S(i,j(k))*flux_vector(j(k));
            if (value >= bigp)
                %Metabolite is a product
                if (value == bigp)
                    fp       = fp + 1;
                    indp(fp) = j(k);
                else
                    fp       = 1;
                    bigp     = value;
                    indp(fp) = j(k);
                end
            elseif (value < bign)
                %Metabolite is a substrate
                if (value == bign)
                    fn       = fn + 1;
                    indn(fn) = j(k);
                else
                    fn       = 1;
                    bign     = value;
                    indn(fn) = j(k);
                end
            end
        end
        
        %Take care of any producing reaction candidates identified
        if (fp > 0)
            for l=1:fp
                if (ismember(indp(l),prod_cand))
                else
                    pp = pp + 1;
                    prod_cand(pp) = indp(l);
                end
            end
        end
        
        %Take care of any consuming reaction candidates identified
        if (fn > 0)
            for l=1:fn
                if (ismember(indn(l),cons_cand))
                else
                    pc = pc + 1;
                    cons_cand(pc) = indn(l);
                end
            end
        end
    end
end

res = zeros(rxns,1);

%Consolidate the two candidate lists: for a reaction to be member of the
%   HFB, it must be a maximal production and consumption reaction, not
%   necessarily for same metabolite.

for i=1:pp
    if (ismember(prod_cand(i),cons_cand))
        res(prod_cand(i)) = 1;
    end
end

numb = size(find(res),1);

names = model.rxns(find(res));










