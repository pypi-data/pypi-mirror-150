#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: luna
"""


import numpy as np
from sklearn.metrics import confusion_matrix, adjusted_rand_score


###################
##Data generation##
###################

def gen_beta_nonoverlap(p,a,k):
    q = a.shape[1]        # number of significant variables
    beta = np.zeros((p,k))
    beta[0:q,:] = a.T
    return beta



def gen_var_nonoverlap(n,p,prop,k,e,beta):
    sigma = np.zeros(p*p).reshape(p,p)
    for i in range(p):
        for j in range(p):
            sigma[i][j]=0.5**abs(i-j)
    nprop = np.round(prop*n).astype(int)
    ntmp = np.insert(np.cumsum(nprop),0,0)
    X = np.random.multivariate_normal(np.array([0]*p),sigma,n).T
    Y = np.array(())   
    group = np.array(())
    err = np.array(())
    for i in range(k):
        err_tmp = e * np.random.randn(nprop[i])
        Y = np.append(Y,X[:,ntmp[i]:ntmp[i+1]].T.dot(beta[:,i].T) + err_tmp)
        group = np.append(group, np.ones(nprop[i])*i+1)
        err = np.append(err, err_tmp)
    group = group.astype(int)
    return Y, X, group, err



def gen_beta_overlap(p,a,npro,k):
    q = a.shape[1]        
    weight_overlap = np.random.uniform(size = npro)
    beta = np.zeros((p,k+npro))
    a1 = a.copy()
    for i in range(len(weight_overlap)):  
        a_overlap = a[0,:] * weight_overlap[i] + a[1,:] * (1-weight_overlap[i])
        a1 = np.append(a1,a_overlap).reshape(-1,q)
    beta[0:q,:] = a1.T
    return beta,weight_overlap


def gen_var_overlap(n,p,prop,k,e,beta):
    sigma = np.zeros(p*p).reshape(p,p)
    for i in range(p):
        for j in range(p):
            sigma[i][j]=0.5**abs(i-j)
    nprop = np.round(prop*n).astype(int)
    ntmp = np.insert(np.cumsum(nprop),0,0)
    X = np.random.multivariate_normal(np.array([0]*p),sigma,n).T
    Y = np.array(())   
    group = np.array(())
    err = np.array(())
    for i in range(k):
        err_tmp = e * np.random.randn(nprop[i])
        Y = np.append(Y,X[:,ntmp[i]:ntmp[i+1]].T.dot(beta[:,i].T) + err_tmp)
        group = np.append(group, np.ones(nprop[i])*i+1)
        err = np.append(err, err_tmp)
    err_tmp = e * np.random.randn(nprop[-1])
    #overlap
    Y = np.append(Y,(X[:,n-nprop[-1]:]*beta[:,k:]).sum(axis=0) + err_tmp)
    err = np.append(err, err_tmp)
    group = np.append(group, np.ones(nprop[-1])*(k+1))
    #group_pf[i] = np.argmax(weight_pf.iloc[:,i]) + 1
    group = group.astype(int)
    return Y, X, group, err



#####################
##Evaluation matrix##
#####################

def sse_calculate_hard(beta0, group1,X,Y):
    n = X.shape[1]
    group_set = np.unique(group1)
    resi2 = np.zeros(n)
    for l in range(len(group_set)):
        X_tmp = X[:,group1 == group_set[l]]
        Y_tmp = Y[group1 == group_set[l]]
        resi2[group1 == group_set[l]] = (Y_tmp - beta0[:,l].dot(X_tmp))**2  
    resi_update = resi2.sum()
    return resi_update


def sse_calculate_soft(beta0, weight,X,Y):
    beta_indi = beta0.dot(weight)
    resi2 = sum((Y - (beta_indi*X).sum(axis = 0))**2)
    return resi2

   
def rmse_multi_hard(beta, beta_hat, group_hat,n,p,prop):    
    beta_kk = np.ones((n,p))
    beta_true = np.ones((int(n*prop[0]),p))*beta[:,0]
    for kk in range(1,beta.shape[1]):
        beta_true = np.vstack((beta_true,np.ones((int(n*prop[kk]),p))*beta[:,kk]))
    for kk in range(0,len(np.unique(group_hat))):
        beta_kk[group_hat == kk+1,:] = beta_hat[:,kk]
    rmse = np.sqrt(((beta_true-beta_kk)**2).sum()/n/p)
    
    return rmse


def rmse_multi_soft(beta, beta_hat, weight_hat,n,k,prop,p): 
    beta_true = np.ones((int(n*prop[0]),p))*beta[:,0]
    for kk in range(1,k):
        beta_true = np.vstack((beta_true,np.ones((int(n*prop[kk]),p))*beta[:,kk]))
    beta_true = np.vstack((beta_true,beta[:,k:].T))
    beta_est = beta_hat.dot(weight_hat)
    rmse = np.sqrt(((beta_true-beta_est.T)**2).sum()/n/p)
    
    return rmse

