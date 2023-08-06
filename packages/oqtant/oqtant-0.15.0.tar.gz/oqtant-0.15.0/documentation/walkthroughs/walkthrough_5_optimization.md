# Oqtant Walkthrough 4: BEC Experimentation

### This walkthrough reviews authorizing an Oqtant session and an example of optimization for BEC. ###

For more information about Oqtant refer to our documentation: https://gitlab.com/infleqtion/albert/oqtant/-/blob/main/README.md

*Batch job functionality is available for users with a subscription tier of EXPLORER or INNOVATOR.*

# Sign into Oqtant

## Before you can view and submit jobs you must first sign into your Oqtant account

Run the below cell to be re-directed to our login page and provide your account credentials. Once authenticated you can safely close out that tab and return to this notebook.


```python
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from matplotlib import pyplot as plt
from scipy.optimize import minimize
from warnings import catch_warnings
from warnings import simplefilter
from scipy.stats import norm
from lmfit import Model
import numpy as np
import inspect
import copy
from oqtant.oqtant_client import get_oqtant_client
from oqtant.util.auth import get_user_token
from bert_schemas import job as JobSchema
from oqtant.schemas.job import (
    OqtantJob,
    Gaussian_dist_2D,
    TF_dist_2D,
    bimodal_dist_2D,
    round_sig
)
import csv

token = get_user_token()
```

## Creating a Oqtant Client Instance ##

### After successful login, create an authorized session with the Oqtant Client ###
- the oqtant_client interacts with the albert server to perform remote lab functions. 
- the oqtant_client object also contains all the jobs which have been submitted, run, or loaded (from database or file) during this python session


```python
oqtant_client = get_oqtant_client(token)
```

## Define a cost function for optimization ## 

A cost function is a metric calculated for the system of interest which is lowered over time via some optimization script 

Larger value = Good:  Condensed and total atom number, condensate fraction 
Smaller value = Good: Thermal atom number, temperature 

Ad hoc Cost function: **C = (Nth*T)/Nc**

### cost_func_5D ### 
This cost function is for a 5-dimensional optimization space, where the 5 dimensions are the RF corner frequencies.

### cost_func_9D ### 
This cost function is for a 9-dimensional optimization space, where the 9 dimensions are the RF corner frequencies and the RF powers.


```python
costs_9D = []
costs_5D = []

default_bec_job = {
    "name": "Example Ultracold Matter Generator Job",
    "job_type": "BEC",
    "inputs": [
        {
            "values": {
                "time_of_flight_ms": 8.0,
                "image_type": "TIME_OF_FLIGHT",
                "end_time_ms": 0.0,
                "rf_evaporation": {
                    "frequencies_mhz": [17.0, 8.0, 4.0, 1.2, 0.045],
                    "powers_mw": [500.0, 500.0, 475.0, 360.0, 220.0],
                    "interpolation": "LINEAR",
                    "times_ms": [-1600, -1200, -800, -400, 0],
                },
                "optical_barriers": None,
                "optical_landscape": None,
                "lasers": None,
            },
        }
    ],
}

def cost_func_9D(RF_freqs_RF_powers):
    RF_freqs = RF_freqs_RF_powers[:5]
    RF_powers = RF_freqs_RF_powers[5:] # this needs to have 5 powers in it now
    default_bec_job["inputs"][0]["values"]["rf_evaporation"]["frequencies_mhz"] = RF_freqs
    default_bec_job["inputs"][0]["values"]["rf_evaporation"]["powers_mw"] = RF_powers
    albert_job = oqtant_client.generate_oqtant_job(job=default_bec_job)
    [job_id] = oqtant_client.run_jobs(job_list=[albert_job], track_status=True)
    job_output = oqtant_client.active_jobs[job_id].inputs[0].output.values
    Nth = job_output.thermal_atom_number
    T = job_output.temperature_uk
    Nc = job_output.condensed_atom_number+1
    C = (Nth*T)/Nc
    costs_9D.append(C)
    return C

def cost_func_5D(RF_freqs, RF_powers = [500, 475, 450, 400, 400]): # added 5th power to default
    default_bec_job["inputs"][0]["values"]["rf_evaporation"]["frequencies_mhz"] = RF_freqs
    default_bec_job["inputs"][0]["values"]["rf_evaporation"]["powers_mw"] = RF_powers
    albert_job = oqtant_client.generate_oqtant_job(job=default_bec_job)
    [job_id] = oqtant_client.run_jobs(job_list=[albert_job], track_status=True)
    job_output = oqtant_client.active_jobs[job_id].inputs[0].output.values
    Nth = job_output.thermal_atom_number
    T = job_output.temperature_uk
    Nc = job_output.condensed_atom_number
    C = (Nth*T)/Nc
    costs_5D.append(C)
    return C
```

## Set bounds for optimization ## 

Bounds will prevent invalid jobs parameters from being submitted to the job runner.


```python
bnds_5d = ((0,50),(0,50),(0,50),(0,50),(0,50))
bnds_9d = ((0,50),(0,50),(0,50),(0,50),(0,50),(0,500),(0,500),(0,500),(0,500))
```

## Choose an optimization algorithm ##

Here, I chose a truncated Newton method (TNC). TNC uses a truncated Newton algorithm to minimize a function with variables subject to bounds. Within scipy.optimize.minimize there are several options for optimizers which allow for bounded variables:  

 - L-BFGS-B 
 - TNC
 - COBYLA
 - SLSQP
 
 
 ## Provide initial conditions and max iterations ##
 
 I chose the web app default parameters for a mixed cloud for the x0 initial conditions. Specify iterations with **options={'maxiter':10}**. Note that each iteration may involve several evaluations of the cost function (which means several jobs), so setting **'maxiter':30** will not run within a single 24 hour period. 


```python
#res_5d = minimize(cost_func_5D, method="TNC", bounds=bnds_5d, x0 = np.array([17,8,4,1.2,0.05]), options={'maxiter':10})
#res_9d = minimize(cost_func_10D, method="TNC", 
#                   x0 = np.array([17,8,4,1.2,0.07,500,475,450,400]), bounds = bnds_9d,options={'maxiter':10})

#print("optimization results freq tuning only:")
#print(res_5d)

#print("optimization results freq and power tuning:")
#print(res_9d)
```

## Bayesian Optimization with a Gaussian Process model ##


## Extract and shape the training data: ##

X_train_array-like of shape (n_samples, n_features) or list of object
Feature vectors or other representations of training data (also required for prediction).

y_train_array-like of shape (n_samples,) or (n_samples, n_targets)
Target values in training data (also required for prediction)

## Define a new target cost function ##


```python
def cost(Nc, Nth, T):
    C = (Nth*T)/Nc
    return C
```


```python
X_global_train = []
y_global_train = []
with open('output.csv', newline='') as csvfile:
    r = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in r:
        if len(row)==26:
            
            rf_a_mhz = float(row[4][:-1])
            rf_b_mhz = float(row[6][:-1])
            rf_c_mhz = float(row[8][:-1])
            rf_d_mhz = float(row[10][:-1])
            rf_e_mhz = float(row[12][:-1])
            pow_a_mw = float(row[14][:-1])
            pow_b_mw = float(row[16][:-1])
            pow_c_mw = float(row[18][:-1])
            pow_d_mw = float(row[20][:-27])
            
            condensed_atom_number = round(float(row[23][:-1]))
            thermal_atom_number = round(float(row[21][:-1]))
            temperature_uk = float(row[25][:-2])
            if temperature_uk > 0 and condensed_atom_number > 100:
                X_global_train.append([rf_a_mhz,
                                       rf_b_mhz,
                                       rf_c_mhz,
                                       rf_d_mhz,
                                       rf_e_mhz,
                                      pow_a_mw, 
                                      pow_b_mw, 
                                      pow_c_mw, 
                                      pow_d_mw])
                y_global_train.append(cost(condensed_atom_number, thermal_atom_number, temperature_uk))

#X_global_train = np.asarray(X_global_train)
#y_global_train = np.asarray(y_global_train)

                
```


```python
# surrogate or approximation for the objective function
def surrogate(model, X):
    # catch any warning generated when making a prediction
    with catch_warnings():
        # ignore generated warnings
        simplefilter("ignore")
        return model.predict(X, return_std=True)
```

## Define an acquisition function ## 

This is a score assigned to each candidate sample on the domain. 

The surrogate function can be used as an acquisition (minimizing the surrogate is the goal after all)

OR

An acquisition function can be used. 3 common options:
- Probability of Improvement (PI).
- Expected Improvement (EI).
- Lower Confidence Bound (LCB).

Here I chose probability of improvement 

**PI = cdf((mu – best_mu) / stdev)**

Where PI is the probability of improvement, cdf() is the normal cumulative distribution function, mu is the mean of the surrogate function for a given sample x, stdev is the standard deviation of the surrogate function for a given sample x, and best_mu is the mean of the surrogate function for the best sample found so far.


```python
def acquisition(X, Xsamples, model):
    # calculate the best surrogate score found so far
    yhat, _ = surrogate(model, X)
    best = max(yhat)
    # calculate mean and stdev via surrogate function
    mu, std = surrogate(model, Xsamples)
    #mu = mu[:, 0]
    # calculate the probability of improvement
    probs = norm.cdf((mu - best) / (std+1E-9))
    return probs
```

## Define a domain ##

This is the domain of the samples. This one point where we inject prior knowledge of the system from previous experience


```python
domain = [(20.,15.),(12.,5.),(5.,2.),(1.9,0.2),(0.2,0.01),
          (500.,470.),(470.,460.),(459.,420.),(420.,350.)]

def rand_domain_sample(domain):
    scale = domain[0]-domain[1]
    random_number = np.random.uniform()+(1E-9)
    sample = scale*random_number+domain[1]
    return sample
```

## Define an optimizer on the acquisition function ##

Here I have chosen a random search over the domain, but other search algorithms can be used. 


```python
def optimize_acquisition(X, y, model, sample_population):
    # random search, generate random samples
    Xsamples = np.asarray([[rand_domain_sample(domain[i]) for i in range(len(X[0]))] for j in range(sample_population)])
    Xsamples = Xsamples.reshape(len(Xsamples), len(X[0]))
    # calculate the acquisition function for each sample
    scores = acquisition(X, Xsamples, model)
    # locate the index of the largest scores
    ix = np.argmax(scores)
    return Xsamples[ix]
```

## Perform the optimization ##


```python
#X = sample_domain
#y = np.asarray([cost_func_9D(x) for x in X])
#Oqtant_model = GPR()
#Oqtant_model.fit(X, y)

X = X_global_train
y = y_global_train
Oqtant_model = GPR()
Oqtant_model.fit(X_global_train, y_global_train)

cost = []

for i in range(20):
    # select the next point to sample
    x = optimize_acquisition(X, y, Oqtant_model, 500)
    print('x', x)
    # sample the point
    actual = cost_func_9D(x)
    cost.append(actual)
    # summarize the finding
    est, _ = surrogate(Oqtant_model, [x])
    print(x, est, actual)
    # add the data to the dataset
    X = np.vstack((X, [x]))
    y.append(actual)
    # update the model
    Oqtant_model.fit(X, y)
```


```python
# plot all samples and the final surrogate function
plt.plot(cost[5:])
#plt.yscale("log")
plt.xlabel("function evaluations")
plt.ylabel("Cost")
plt.title("20 evaluations, 500 surrogate samples, 335pm 5_5_21")
plt.savefig("335pm 5_5_21.png")
plt.show()
# best result
ix = np.argmax(y)
print('Best Result:'+str([X[ix], y[ix]]))
```
