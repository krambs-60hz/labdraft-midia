# Trilha original gerada por síntese (sem samples, sem direitos de terceiros).
import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, sys
SR=44100; DUR=float(sys.argv[2]) if len(sys.argv)>2 else 26.87; VAR=int(sys.argv[3]) if len(sys.argv)>3 else 0
BPM=[120,110,124,116,104,128][VAR%6]; BEAT=60/BPM; N=int(SR*DUR)
L=np.zeros(N); R=np.zeros(N)
def f(m): return 440*2**((m-69)/12)
def env(n,a=0.005,r=0.1):
    e=np.ones(n); na=max(1,int(a*SR)); nr=max(1,int(r*SR)); e[:na]=np.linspace(0,1,na); e[-nr:]*=np.linspace(1,0,nr); return e
def add(sig,t,gl=1,gr=1):
    i=int(t*SR); j=min(N,i+len(sig));
    if i>=N: return
    L[i:j]+=sig[:j-i]*gl; R[i:j]+=sig[:j-i]*gr
def saw(fr,n): t=np.arange(n)/SR; return 2*((t*fr)%1)-1
def lp(x,fc): b,a=ss.butter(2,fc/(SR/2)); return ss.lfilter(b,a,x)
# Am  F  C  G
PROG=[([[57,60,64],[53,57,60],[48,52,55],[55,59,62]],[45,41,48,43]),
 ([[50,53,57],[46,50,53],[53,57,60],[48,52,55]],[38,46,41,48]),
 ([[52,55,59],[48,52,55],[55,59,62],[50,54,57]],[40,48,43,50]),
 ([[48,51,55],[44,48,51],[51,55,58],[46,50,53]],[36,44,39,46]),
 ([[57,60,64],[55,59,62],[53,57,60],[52,56,59]],[45,43,41,40]),
 ([[54,57,61],[50,54,57],[57,61,64],[52,56,59]],[42,50,45,52])]
CH,ROOT=PROG[VAR%6]
bars=int(DUR/(4*BEAT))+1
rng=np.random.default_rng(7+VAR)
for b in range(bars):
    t0=b*4*BEAT; c=CH[b%4]; r=ROOT[b%4]
    # pad
    n=int(4*BEAT*SR)
    pad=sum(saw(f(m)*d,n) for m in c for d in (0.997,1.003))/6
    pad=lp(pad,1400 if b>=2 else 800)*env(n,0.25,0.4)*0.22
    add(pad,t0,1,0.85); add(pad,t0+0.01,0.85,1)
    # baixo em colcheias a partir do compasso 1
    if b>=1:
        for k in range(8):
            nn=int(BEAT/2*SR*0.9); t=np.arange(nn)/SR
            s=(np.sin(2*np.pi*f(r-12)*t)*0.7+lp(saw(f(r-12),nn),500)*0.4)*env(nn,0.003,0.05)*0.42
            add(s,t0+k*BEAT/2)
    # bateria a partir do compasso 1
    if b>=1:
        for k in range(4):
            nn=int(0.35*SR); t=np.arange(nn)/SR
            kick=np.sin(2*np.pi*(50+90*np.exp(-t*35))*t)*np.exp(-t*9)*0.9
            add(kick,t0+k*BEAT)
            hn=int(0.05*SR); hat=ss.lfilter(*ss.butter(2,7000/(SR/2),'high'),rng.standard_normal(hn))*np.exp(-np.arange(hn)/SR*90)*0.18
            add(hat,t0+k*BEAT+BEAT/2,0.8,1)
            if b>=(2 if DUR<20 else 3) and k in (1,3):
                sn=int(0.2*SR); clap=ss.lfilter(*ss.butter(2,[1200/(SR/2),5000/(SR/2)],'band'),rng.standard_normal(sn))*np.exp(-np.arange(sn)/SR*22)*0.5
                add(clap,t0+k*BEAT)
    # arpejo a partir do compasso 4
    if b>=(2 if DUR<20 else 4):
        notes=c+[c[0]+12]
        for k in range(16):
            m=notes[[0,1,2,3,2,1,2,3][k%8]]+12; nn=int(BEAT/4*SR*0.95); t=np.arange(nn)/SR
            s=(np.sin(2*np.pi*f(m)*t)+0.3*np.sin(4*np.pi*f(m)*t))*env(nn,0.002,0.08)*0.11
            pan=0.6+0.4*(k%2); add(s,t0+k*BEAT/4,pan,1.6-pan)
mix=np.stack([L,R],1)
fade=np.ones(N); fi=int(0.4*SR); fo=int(2.2*SR); fade[:fi]=np.linspace(0,1,fi); fade[-fo:]=np.linspace(1,0,fo)
mix*=fade[:,None]; mix=np.tanh(mix*1.1); mix/=np.abs(mix).max()/0.89
wf.write(sys.argv[1],SR,(mix*32767).astype(np.int16))
