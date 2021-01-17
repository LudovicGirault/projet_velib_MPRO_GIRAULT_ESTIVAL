import matplotlib.pyplot as plt
import numpy as np
import copy

### Definition conditions initiales
etatInitial = np.zeros(25)
etatInitial[0] = 1
#etatInitial[0] = 20
#etatInitial[1] = 15
#etatInitial[2] = 17
#etatInitial[3] = 13
#etatInitial[4] = 18
#etatInitial[5] = 1   # transition stat 3 vers stat 4
#etatInitial[9] = 1   # transition stat 4 vers stat 3
#etatInitial[10] = 1  # transition stat 4 vers stat 5
#etatInitial[14] = 1  # transition stat 5 vers stat 4
#etatInitial[15] = 1  # etc
#etatInitial[19] = 1
#etatInitial[20] = 1
#etatInitial[24] = 1


Lambda = np.array([0,1./3.,1./5.,1./7.,1./7.,1./2.,0,1./2.,1./5.,1./5.,1./4.,1./2.,0,1./3.,1./3.,1./8.,1./6.,1./4.,0,1./2.,1./7.,1./7.,1./5.,1./2.,0])


tx_dep = np.array([2.8,3.7,5.5,3.5,4.6])/60

M_rout = np.array([[0,0.22,0.32,0.2,0.26],[0.17,0,0.34,0.21,0.28],[0.19,0.26,0,0.24,0.31],[0.17,0.22,0.33,0,0.28],[0.18,0.24,0.35,0.23,0]])



def DureeSejour(etat,Lambda,i,j):
	if etat[i] == 0:
		return -np.log(np.random.rand())/(Lambda[5*i+j]*etat[4+4*i+j]) , 2
	elif etat[4+4*i+j] == 0:
		return -np.log(np.random.rand())/tx_dep[i] , 1
	else :
		a= -np.log(np.random.rand())/tx_dep[i]
		b= -np.log(np.random.rand())/(Lambda[5*i+j]*etat[4+4*i+j])
		if a < b :
			return a, 1
		else :
			return b, 2

def nouvelEtat(etat,i,j,status)	:
	if status == 1 :
		etat[i] -=1
		etat[4+4*i+j] += 1
	else :
		etat[4+4*i+j] -=1
		etat[j] +=1
	return etat


def velib(T,Lambda,tx_dep,M_rout,etatInitial):
	etat = etatInitial
	trajectoire = [etatInitial[0:5]]
	temps = 0
	sauts = [0]
	proba_vide = [0,0,0,0,0]
	while temps < T:
		depart = [0,0,0,0,0]
		for t in range(0,5):
			depart[t] = -np.log(np.random.rand())/tx_dep[t]
		i = np.argmin(depart)
		j = np.random.choice(5,1,p=M_rout[i])[0] 
		while etat[i] == 0 and etat[4+4*i+j] == 0 :
			for t in range(0,5):
				depart[t] = -np.log(np.random.rand())/tx_dep[t]
			i = np.argmin(depart)
			j = np.random.choice(5,1,p=M_rout[i])[0]  
#		tij = 4+i*4+j
		tps, status = DureeSejour(etat,Lambda,i,j)
		temps += tps
		for stat in range(0,5):
			if etat[stat] == 0 :
				proba_vide[stat] += tps
#		print(etat,"toto")
		etat = nouvelEtat(etat,i,j,status)
#		print(etat,"alice")
		trajectoire += [copy.deepcopy(etat[0:5])]
#		print(trajectoire)
		sauts +=[temps]
	for stat in range(0,5):
		proba_vide[stat] = proba_vide[stat]/T
		print("La proba que la station ",stat +1, " soit vide est ", proba_vide[stat])
	return sauts,trajectoire

x,y = velib(10000,Lambda,tx_dep,M_rout,etatInitial)
#print(x,y)
plt.plot(x,y,drawstyle='steps-post')
plt.show()




#x,y=mm1(0.6,30,np.array([[1,0,0,0,0,0]]))

#plt.plot(x,y,drawstyle='steps-post')
#plt.show()
#plt.savefig('mm1Trajectoire.pdf')




