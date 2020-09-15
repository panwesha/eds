import pandas as pd
import numpy as np

from datetime import datetime
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
from scipy import optimize
from scipy import integrate

mpl.rcParams['figure.figsize'] = (16, 9)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', None)


sns.set(style="darkgrid")




from scipy import optimize
from scipy import optimize


def data_gathering():
    population_df = pd.read_csv('/Users/anweshapanda/ads_covid-19/data/raw/population_data.csv',sep=';', thousands=',')
    population_df = population_df.set_index(['country']).T
    df_analyse=pd.read_csv('/Users/anweshapanda/ads_covid-19/data/processed/all_country_flat_table.csv',sep=';')
    country_list = df_analyse.columns[1:]

    data_y = []
    t=[]
    for column in df_analyse.columns:
         data_y.append(np.array(df_analyse[column][75:]))

    t = np.arange(len(data_y))
    data_y_df = pd.DataFrame(data_y,index=df_analyse.columns).T
    data_y_df.to_csv('/Users/anweshapanda/ads_covid-19/data/processed/sir/ydata_SIR_data.csv',sep=';',index=False)
    optimized_df = pd.DataFrame(columns = df_analyse.columns[1:],
                     index = ['opt_beta', 'opt_gamma', 'std_dev_error_beta', 'std_dev_error_gamma'])

    t = []
    fitted_final_data = []

    global I0, N0, S0, R0
    for column in data_y_df.columns[1:]:
        I0 = data_y_df[column].loc[0]
        N0 = population_df[column].loc['population']
        S0 = N0-I0
        R0 = 0
        t  = np.arange(len(data_y_df[column]))

        popt=[0.4,0.1]

        fit_odeint(t, *popt)


        popt, pcov = optimize.curve_fit(fit_odeint, t, data_y_df[column], maxfev=5000)
        perr = np.sqrt(np.diag(pcov))


        optimized_df.at['opt_beta', column] = popt[0]
        optimized_df.at['opt_gamma', column] = popt[1]
        optimized_df.at['std_dev_error_beta', column] = perr[0]
        optimized_df.at['std_dev_error_gamma', column] = perr[1]

        fitted = fit_odeint(t, *popt)
        fitted_final_data.append(np.array(fitted))

    optimized_df.to_csv('/Users/anweshapanda/ads_covid-19/data/processed/sir/optimized_SIR_data.csv',sep=';',index=False)
    fitted_SIR_data_df = pd.DataFrame(fitted_final_data,index=df_analyse.columns[1:]).T
    fitted_SIR_data_df.to_csv('/Users/anweshapanda/ads_covid-19/data/processed/sir/fitted_SIR_data.csv',sep=';',index=False)
    print('Number of rows stored in optimized df:' +str(optimized_df.shape[0]))
    print('Number of rows stored in fitted_SIR_data:' +str(fitted_SIR_data_df.shape[0]))









def fit_odeint(t, beta, gamma):

    '''
    helper function for the integration
    '''
    return integrate.odeint(SIR_model_t, (S0, I0, R0, N0), t, args=(beta, gamma))[:,1]


def SIR_model_t(SIRN,t,beta,gamma):
    ''' Simple SIR model
    S: susceptible population
    t: time step, mandatory for integral.odeint
    I: infected people
    R: recovered people
    beta:

    overall condition is that the sum of changes (differnces) sum up to 0
    dS+dI+dR=0
    S+I+R= N (constant size of population)

    '''

    S,I,R,N=SIRN
    dS_dt=-beta*S*I/N          #S*I is the
    dI_dt=beta*S*I/N-gamma*I
    dR_dt=gamma*I
    dN_dt=0
    return dS_dt,dI_dt,dR_dt,dN_dt






if __name__ == '__main__':
    data_gathering()
