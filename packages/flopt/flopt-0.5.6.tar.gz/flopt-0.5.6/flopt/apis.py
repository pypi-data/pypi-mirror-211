import flopt.convert

def load_mps(mps_file):
    import pulp
    pulp_var, pulp_prob = pulp.LpProblem.fromMPS(mps_file)
    prob = flopt.convert.pulp_to_flopt(pulp_prob)
    return prob

