import os, sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,ROOT)
from qrb.graph_response import three_c_matrix, complete_antiferro_supports
from qrb.resource_cost import minimum_negativity_from_radius

FIG=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','figures'))
os.makedirs(FIG,exist_ok=True)

# Fig. 3: exact 3-emitter bodies. Quantum exposed points from top eigenvectors;
# separable boundary from three planar equatorial Bloch vectors.
rng=np.random.default_rng(20260826)
qpts=[]
for _ in range(6000):
    c=rng.normal(size=3)
    c/=np.linalg.norm(c)
    C=three_c_matrix(*c)
    vals,vecs=np.linalg.eigh(C)
    v=vecs[:,-1]
    qpts.append([2*v[0]*v[1],2*v[0]*v[2],2*v[1]*v[2]])
qpts=np.asarray(qpts)

phi=np.linspace(0,2*np.pi,90,endpoint=False)
spts=[]
for a in phi:
    for b in phi:
        spts.append([0.5*np.cos(a),0.5*np.cos(b),0.5*np.cos(a-b)])
spts=np.asarray(spts)

fig=plt.figure(figsize=(6.4,5.5))
ax=fig.add_subplot(111,projection='3d')
ax.scatter(qpts[:,0],qpts[:,1],qpts[:,2],s=2,alpha=0.14,label='quantum exposed boundary')
ax.scatter(spts[::3,0],spts[::3,1],spts[::3,2],s=2,alpha=0.17,label='separable elliptope boundary')
ax.scatter([1,2/3],[0,2/3],[0,2/3],s=38,marker='x',label='entangled examples')
ax.set_xlabel(r'$r_{12}$')
ax.set_ylabel(r'$r_{13}$')
ax.set_zlabel(r'$r_{23}$')
ax.set_title('Three-emitter fixed-marginal response bodies')
ax.legend(loc='upper left',fontsize=8)
ax.view_init(elev=23,azim=39)
fig.tight_layout()
for ext in ['png','pdf']:
    fig.savefig(os.path.join(FIG,f'fig3_three_emitter_bodies.{ext}'),dpi=240 if ext=='png' else None,bbox_inches='tight')
plt.close(fig)

# Fig. 4: exact frustrated complete-graph support gap
Ns=np.arange(3,21)
hq=[]; hs=[]; ratio=[]
for n in Ns:
    q,s=complete_antiferro_supports(int(n)); hq.append(q);hs.append(s);ratio.append(q/s)
fig,ax=plt.subplots(figsize=(6.4,4.2))
ax.plot(Ns,hq,'o-',label=r'$h_Q(-K_N)$')
ax.plot(Ns,hs,'s-',label=r'$h_{\rm sep}(-K_N)$')
ax.set_xlabel('number of meta-atoms $N$')
ax.set_ylabel('support value')
ax.set_title('Exact frustrated collective-response advantage')
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()
for ext in ['png','pdf']:
    fig.savefig(os.path.join(FIG,f'fig4_frustrated_supports.{ext}'),dpi=240 if ext=='png' else None,bbox_inches='tight')
plt.close(fig)

# Fig. 5: exact resource cost for two-emitter response radius
r=np.linspace(0,1,301)
neg=np.array([minimum_negativity_from_radius(x) for x in r])
fig,ax=plt.subplots(figsize=(6.4,4.0))
ax.plot(r,neg,lw=2)
ax.axvline(0.5,ls='--',lw=1)
ax.set_xlabel(r'response radius $r$')
ax.set_ylabel(r'minimum negativity $\mathcal{N}_{\min}(r)$')
ax.set_title('Exact entanglement cost of the two-emitter response')
ax.grid(alpha=0.25)
fig.tight_layout()
for ext in ['png','pdf']:
    fig.savefig(os.path.join(FIG,f'fig5_resource_cost.{ext}'),dpi=240 if ext=='png' else None,bbox_inches='tight')
plt.close(fig)

print('generated v0.2 figures in',FIG)
