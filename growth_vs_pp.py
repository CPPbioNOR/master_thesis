import cobra

pp_bounds = [0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000]
model_name = 'test_sehhm.xml'

#input:
#1) list of floats representing the upper bound of the protein pool (pp)
#2) string of model name

#output:
#1) list of max growth rates corresponding to the pp bounds
#2) printing the same information in a pretty way to terminal
def pp_bounds_to_growth(model_name, pp_bounds):
    growth_list = []
    mod = cobra.io.read_sbml_model(model_name)
    original_upper_bound = mod.reactions.get_by_id("ER_pool_TG_").upper_bound   #storing original pp upper bound
    max_growth = mod.optimize().objective_value
    print(f"The model has a default pp upper bound of {original_upper_bound} and a max growth rate of {max_growth}.")
    
    for bound in pp_bounds:
        mod.reactions.get_by_id("ER_pool_TG_").upper_bound = bound
        max_growth = mod.optimize().objective_value
        growth_list.append(max_growth)
        print(f"A pp of: {bound} gives a max growth rate of: {max_growth}.")

    mod.reactions.get_by_id("ER_pool_TG_").upper_bound = original_upper_bound
    print(f"After running the function, the model has an upper pp bound of {mod.reactions.get_by_id('ER_pool_TG_').upper_bound}")
    return growth_list

growth = pp_bounds_to_growth(model_name, pp_bounds)
print(growth)