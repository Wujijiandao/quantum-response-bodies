import json, os, sys
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)
from qrb.graph_response import (
    complete_antiferro_supports, complete_antiferro_matrix, quantum_support_xy,
    separable_support_xy, three_quantum_support, in_three_separable_body
)
from qrb.resource_cost import minimum_negativity_from_radius, negativity, optimal_x_state_for_radius

out={}
out['triangle']={
    'hQ_ferro': three_quantum_support(1,1,1),
    'hQ_frustrated': three_quantum_support(-1,-1,-1),
    'bell_pair_point_separable': bool(in_three_separable_body([1,0,0])),
}
rows=[]
for n in range(3,9):
    hq,hs=complete_antiferro_supports(n)
    hq_num=quantum_support_xy(complete_antiferro_matrix(n))
    # numeric classical check only through n=7 to keep runtime modest
    hs_num=separable_support_xy(complete_antiferro_matrix(n), seed=100+n) if n<=7 else None
    rows.append({'N':n,'hQ_exact':hq,'hQ_numeric':hq_num,'hSep_exact':hs,'hSep_numeric':hs_num,'ratio':hq/hs})
out['complete_frustrated']=rows
out['resource_cost']=[]
for r in np.linspace(0.5,1.0,6):
    rho=optimal_x_state_for_radius(float(r))
    out['resource_cost'].append({'r':float(r),'N_formula':minimum_negativity_from_radius(r),'N_achiever':negativity(rho)})

path=os.path.join(os.path.dirname(__file__),'..','..','results','v020_theorem_checks.json')
with open(path,'w',encoding='utf-8') as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
print('wrote',path)
