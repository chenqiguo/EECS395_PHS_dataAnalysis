import csv
from timeDomain import timeDomain
from frequencyDomain import frequencyDomain
from DFA import dfa
from DFA import scalingExponent
from multiScaleEntropy import sampEn
rr = []
with open('rr_dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if row[0] == '1':
                rr.append(float(row[3]))

[ANN,SDNN,pNN50,pNN20,rMSSD] = timeDomain(rr)

#print([ANN,SDNN,pNN50,pNN20,rMSSD])

#DFA
[scales, F, alpha] = scalingExponent(rr, 5, 1000, 20, 1, 2, 0)

r = 0.2 * SDNN
#rr = rr[0:1000]
entropy = sampEn(rr, 2, r)
print(entropy)

#freqDomainFeats = frequencyDomain(rr)
#print(freqDomainFeats)
