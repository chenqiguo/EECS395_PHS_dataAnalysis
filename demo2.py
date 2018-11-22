"""demo2 by Chenqi, reference to demo by Sylvia, used to test and combine each analytical methods.
   This script dealing with hear rate related data.
   Note: Since the rr_dataset.csv file combined day1 and day2's data, this code used the length of day1 and day2 data to split day1 and day2!
         This can be improved if the rr_dataset.csv file was split into rr_dataset_day1.csv and rr_dataset_day2.csv
         The helping dictionary: help_dict_day1 = {patient_id: data_length}, help_dict_day2 = {patient_id: data_length} (patient_id type:string)
   This demo stores the analytical results for each of 9 patient in the dictionary, indexed by patient_id(type:string):
   1) timeDomain_results_day1 = {patient_id: [ANN,SDNN,pNN50,pNN20,rMSSD]} (day2 same as day1)
   2) DFA_results_day1 = {patient_id: [scales, F, alpha]} (Note: each DFA plot are stored under the specific file for debug) (day2 same as day1)
   3) sampEn_results_day1 = {patient_id: entropy} (Note: this will takes quite a long time!) (day2 same as day1)
   4) frequencyDomain_results_day1 = {patient_id: {'VLF_Power': vlf_NU_log, 'LF_Power': lf_NU_log, 'HF_Power': hf_NU_log, 'LF/HF': lfhfRation_log}} (day2 same as day1)
   5) poincareSTD_results_day1 = {patient_id: {'SD1': SD1, 'SD2': SD2}}"""

import csv
from timeDomain import timeDomain
from frequencyDomain import frequencyDomain
from DFA import dfa
from DFA import scalingExponent
from multiScaleEntropy import sampEn
from poincare import plotPoincare, eclipseFittingMethod

# helping dictionary: index of data in rr_dataset.csv
# help_dict_day1 = {patient_id: [start_index, end_index]}
help_dict_day1 = {'1': 8254, '2': 2213, '3': 1503, '4': 10124, '5': 6648, '6': 133, '7': 212, '8': 322, '9': 2213}
#help_dict_day2 = {'1': 1523, '2': 2429, '3': 4337, '4': 871, '5': 0, '6': 3103, '7': 578, '8': 7743, '9': 2429}


def process_csv_rr(fileName):
    rrs = {} # rrs = {patient_id: [rr1, rr2, rr3, ...]}, note: patient_id is string, rr is float
    header_flag = True
    for i in range(1, 10):  # 9 patients in total
        p_id = str(i)
        #print(p_id)
        tmp_rr = []
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if header_flag:
                    header_flag = False
                else:
                    if row[0] == p_id:
                        tmp_rr.append(float(row[3]))
        rrs[p_id] = tmp_rr
        #print(tmp_rr)
        #print(len(tmp_rr))
    return rrs

def demo_timeDomain(rrs):
    timeDomain_results = {} # timeDomain_results = {patient_id: [ANN,SDNN,pNN50,pNN20,rMSSD]}
    for i in range(1, 10):  # 9 patients in total
        p_id = str(i)
        if len(rrs[p_id]) != 0:
            [ANN, SDNN, pNN50, pNN20, rMSSD] = timeDomain(rrs[p_id])
            timeDomain_results[p_id] = [ANN, SDNN, pNN50, pNN20, rMSSD]
        else:
            timeDomain_results[p_id] = []
    return timeDomain_results

def demo_DFA(rrs, plot_flag):
    DFA_results = {} # DFA_results = {patient_id: [scales, F, alpha]}
    for i in range(1, 10):  # 9 patients in total
        p_id = str(i)
        if len(rrs[p_id]) >= 1000:
            [scales, F, alpha] = scalingExponent(rrs[p_id], 5, 1000, 20, 1, 2, plot_flag)
            DFA_results[p_id] = [scales, F, alpha]
        elif len(rrs[p_id]) != 0:
            [scales, F, alpha] = scalingExponent(rrs[p_id], 5, len(rrs[p_id]), 20, 1, 2, plot_flag)
            DFA_results[p_id] = [scales, F, alpha]
        else: # len(rrs[p_id]) == 0:
            DFA_results[p_id] = []
    return DFA_results

def demo_sampEn(rrs, timeDomain_results):
    sampEn_results = {} # sampEn_results = {patient_id: entropy}
    for i in range(1, 10):  # 9 patients in total
        p_id = str(i)
        if len(rrs[p_id]) == 0:
            sampEn_results[p_id] = None
            continue
        SDNN = timeDomain_results[p_id][1]
        r = 0.2 * SDNN
        entropy = sampEn(rrs[p_id], 2, r)
        sampEn_results[p_id] = entropy
    return sampEn_results

def demo_frequencyDomain(rrs):
    frequencyDomain_results = {} # frequencyDomain_results = {patient_id: {'VLF_Power': vlf_NU_log, 'LF_Power': lf_NU_log, 'HF_Power': hf_NU_log, 'LF/HF': lfhfRation_log}}
    for i in range(1, 10):  # 9 patients in total
        p_id = str(i)
        if len(rrs[p_id]) == 0:
            frequencyDomain_results[p_id] = {}
            continue
        freqDomainFeats = frequencyDomain(rrs[p_id])
        frequencyDomain_results[p_id] = freqDomainFeats
    return frequencyDomain_results

def demo_plotPoincare(rrs):
    for i in range(1, 10):  # 9 patients in total
        p_id = str(i)
        if len(rrs[p_id]) == 0:
            continue
        plotPoincare(rrs[p_id])

def demo_poincareSTD(rrs):
    poincareSTD_results = {} # poincareSTD_results = {patient_id: {'SD1': SD1, 'SD2': SD2}}
    for i in range(1, 10):  # 9 patients in total
        p_id = str(i)
        if len(rrs[p_id]) == 0:
            poincareSTD_results[p_id] = {}
            continue
        tmp_dict = eclipseFittingMethod(rrs[p_id])
        poincareSTD_results[p_id] = tmp_dict
    return poincareSTD_results



if __name__ == "__main__":

    # process csv
    rrs = process_csv_rr('rr_dataset_time.csv') # rrs = {patient_id: [rr1, rr2, rr3, ...]}
    rrs_day1 = {} # rrs_day1 = {patient_id: [rr1 in day1, rr2 in day1, ...]}
    rrs_day2 = {}
    for i in range(1, 10):
        p_id = str(i)
        #print(p_id)
        day1_index = help_dict_day1[p_id]
        #day2_index = help_dict_day2[p_id]
        rrs_day1[p_id] = rrs[p_id][:day1_index+1]
        if day1_index == len(rrs[p_id]):
            rrs_day2[p_id] = []
            continue
        rrs_day2[p_id] = rrs[p_id][day1_index+1:]
        #print(len(rrs[p_id]))
        #print(len(rrs_day1[p_id]))
        #print(len(rrs_day2[p_id]))

    # time domain
    timeDomain_results = demo_timeDomain(rrs) # timeDomain_results = {patient_id: [ANN,SDNN,pNN50,pNN20,rMSSD]}
    timeDomain_results_day1 = demo_timeDomain(rrs_day1)
    timeDomain_results_day2 = demo_timeDomain(rrs_day2)
    #print(timeDomain_results)
    #print(timeDomain_results_day1)
    #print(timeDomain_results_day2)

    # DFA <-- you can modify this to save the plot
    plot_flag = 1 # plot DFA: 1; NOT plot DFA: 0
    DFA_results = demo_DFA(rrs, plot_flag) # DFA_results = {patient_id: [scales, F, alpha]}
    DFA_results_day1 = demo_DFA(rrs_day1, plot_flag)
    DFA_results_day2 = demo_DFA(rrs_day2, plot_flag)
    #print(DFA_results)
    #print(DFA_results_day1)
    #print(DFA_results_day2)

    # sample entropy <-- this will take a long time to run!
    sampEn_results = demo_sampEn(rrs, timeDomain_results) # sampEn_results = {patient_id: entropy}
    sampEn_results_day1 = demo_sampEn(rrs_day1, timeDomain_results_day1)
    sampEn_results_day2 = demo_sampEn(rrs_day2, timeDomain_results_day2)
    #print(sampEn_results)
    #print(sampEn_results_day1)
    #print(sampEn_results_day2)

    # frequency domain <-- this may take a long time to run if rr list is too long, and even may run out of memory!
    frequencyDomain_results = demo_frequencyDomain(rrs)
    frequencyDomain_results_day1 = demo_frequencyDomain(rrs_day1)
    frequencyDomain_results_day2 = demo_frequencyDomain(rrs_day2)
    #print(frequencyDomain_results)
    #print(frequencyDomain_results_day1)
    #print(frequencyDomain_results_day2)

    # poincare STD
    poincareSTD_results = demo_poincareSTD(rrs)
    poincareSTD_results_day1 = demo_poincareSTD(rrs_day1)
    poincareSTD_results_day2 = demo_poincareSTD(rrs_day2)
    #print(poincareSTD_results)
    #print(poincareSTD_results_day1)
    #print(poincareSTD_results_day2)

    # plot poincare <-- you can modify this to save the plot
    demo_plotPoincare(rrs)
    demo_plotPoincare(rrs_day1)
    demo_plotPoincare(rrs_day2)

    # some other analytics ...