#!/usr/bin/bash

##### Perform the b-factor analysis.

### ATP
time python3 bfactorAnalysis/code/main.py globalData/standalone_atp_01-04-22 ATP 0.01 globalData/standalone_atp_01-04-22.txt globalData/structFiles_atp_01-04-22/ 0.9 ligandAny 3.5 1> bfactorAnalysis/results2/ATP/anyATP.out 2> bfactorAnalysis/results2/ATP/anyATPErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_atp_01-04-22 ATP 0.01 globalData/standalone_atp_01-04-22.txt globalData/structFiles_atp_01-04-22/ 0.5 ligandAvg 3.5 1> bfactorAnalysis/results2/ATP/avgATP.out 2> bfactorAnalysis/results2/ATP/avgATPErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_atp_01-04-22 ATP 0.01 globalData/standalone_atp_01-04-22.txt globalData/structFiles_atp_01-04-22/ 0.9 ligandPlusAny 3.5 1> bfactorAnalysis/results2/ATP/anyATPPlus.out 2> bfactorAnalysis/results2/ATP/anyATPPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_atp_01-04-22 ATP 0.01 globalData/standalone_atp_01-04-22.txt globalData/structFiles_atp_01-04-22/ 0.5 ligandPlusAvg 3.5 1> bfactorAnalysis/results2/ATP/avgATPPlus.out 2> bfactorAnalysis/results2/ATP/avgATPPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_atp_01-04-22 ATP 0.01 globalData/standalone_atp_01-04-22.txt globalData/structFiles_atp_01-04-22/ 0.9 otherAny 3.5 1> bfactorAnalysis/results2/ATP/anyATPOther.out 2> bfactorAnalysis/results2/ATP/anyATPOtherErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_atp_01-04-22 ATP 0.01 globalData/standalone_atp_01-04-22.txt globalData/structFiles_atp_01-04-22/ 0.5 otherAvg 3.5 1> bfactorAnalysis/results2/ATP/avgATPOther.out 2> bfactorAnalysis/results2/ATP/avgATPOtherErr.err


### ADP
time python3 bfactorAnalysis/code/main.py globalData/standalone_adp_07-22-22 ADP 0.01 globalData/standalone_adp_07-22-22.txt globalData/structFiles_adp_07-22-22/ 0.9 ligandAny 3.5 1> bfactorAnalysis/results2/ADP/anyADP.out 2> bfactorAnalysis/results2/ADP/anyADPErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_adp_07-22-22 ADP 0.01 globalData/standalone_adp_07-22-22.txt globalData/structFiles_adp_07-22-22/ 0.5 ligandAvg 3.5 1> bfactorAnalysis/results2/ADP/avgADP.out 2> bfactorAnalysis/results2/ADP/avgADPErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_adp_07-22-22 ADP 0.01 globalData/standalone_adp_07-22-22.txt globalData/structFiles_adp_07-22-22/ 0.9 ligandPlusAny 3.5 1> bfactorAnalysis/results2/ADP/anyADPPlus.out 2> bfactorAnalysis/results2/ADP/anyADPPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_adp_07-22-22 ADP 0.01 globalData/standalone_adp_07-22-22.txt globalData/structFiles_adp_07-22-22/ 0.5 ligandPlusAvg 3.5 1> bfactorAnalysis/results2/ADP/avgADPPlus.out 2> bfactorAnalysis/results2/ADP/avgADPPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_adp_07-22-22 ADP 0.01 globalData/standalone_adp_07-22-22.txt globalData/structFiles_adp_07-22-22/ 0.9 otherAny 3.5 1> bfactorAnalysis/results2/ADP/anyADPOther.out 2> bfactorAnalysis/results2/ADP/anyADPOtherErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_adp_07-22-22 ADP 0.01 globalData/standalone_adp_07-22-22.txt globalData/structFiles_adp_07-22-22/ 0.5 otherAvg 3.5 1> bfactorAnalysis/results2/ADP/avgADPOther.out 2> bfactorAnalysis/results2/ADP/avgADPOtherErr.err


### GTP
time python3 bfactorAnalysis/code/main.py globalData/standalone_gtp_01-04-22 GTP 0.01 globalData/standalone_gtp_01-04-22.txt globalData/structFiles_gtp_01-04-22/ 0.9 ligandAny 3.5 1> bfactorAnalysis/results2/GTP/anyGTP.out 2> bfactorAnalysis/results2/GTP/anyGTPErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gtp_01-04-22 GTP 0.01 globalData/standalone_gtp_01-04-22.txt globalData/structFiles_gtp_01-04-22/ 0.5 ligandAvg 3.5 1> bfactorAnalysis/results2/GTP/avgGTP.out 2> bfactorAnalysis/results2/GTP/avgGTPErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gtp_01-04-22 GTP 0.01 globalData/standalone_gtp_01-04-22.txt globalData/structFiles_gtp_01-04-22/ 0.9 ligandPlusAny 3.5 1> bfactorAnalysis/results2/GTP/anyGTPPlus.out 2> bfactorAnalysis/results2/GTP/anyGTPPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gtp_01-04-22 GTP 0.01 globalData/standalone_gtp_01-04-22.txt globalData/structFiles_gtp_01-04-22/ 0.5 ligandPlusAvg 3.5 1> bfactorAnalysis/results2/GTP/avgGTPPlus.out 2> bfactorAnalysis/results2/GTP/avgGTPPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gtp_01-04-22 GTP 0.01 globalData/standalone_gtp_01-04-22.txt globalData/structFiles_gtp_01-04-22/ 0.9 otherAny 3.5 1> bfactorAnalysis/results2/GTP/anyGTPOther.out 2> bfactorAnalysis/results2/GTP/anyGTPOtherErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gtp_01-04-22 GTP 0.01 globalData/standalone_gtp_01-04-22.txt globalData/structFiles_gtp_01-04-22/ 0.5 otherAvg 3.5 1> bfactorAnalysis/results2/GTP/avgGTPOther.out 2> bfactorAnalysis/results2/GTP/avgGTPOtherErr.err


### GDP
time python3 bfactorAnalysis/code/main.py globalData/standalone_gdp_01-04-22 GDP 0.01 globalData/standalone_gdp_01-04-22.txt globalData/structFiles_gdp_01-04-22/ 0.9 ligandAny 3.5 1> bfactorAnalysis/results2/GDP/anyGDP.out 2> bfactorAnalysis/results2/GDP/anyGDPErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gdp_01-04-22 GDP 0.01 globalData/standalone_gdp_01-04-22.txt globalData/structFiles_gdp_01-04-22/ 0.5 ligandAvg 3.5 1> bfactorAnalysis/results2/GDP/avgGDP.out 2> bfactorAnalysis/results2/GDP/avgGDPErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gdp_01-04-22 GDP 0.01 globalData/standalone_gdp_01-04-22.txt globalData/structFiles_gdp_01-04-22/ 0.9 ligandPlusAny 3.5 1> bfactorAnalysis/results2/GDP/anyGDPPlus.out 2> bfactorAnalysis/results2/GDP/anyGDPPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gdp_01-04-22 GDP 0.01 globalData/standalone_gdp_01-04-22.txt globalData/structFiles_gdp_01-04-22/ 0.5 ligandPlusAvg 3.5 1> bfactorAnalysis/results2/GDP/avgGDPPlus.out 2> bfactorAnalysis/results2/GDP/avgGDPPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gdp_01-04-22 GDP 0.01 globalData/standalone_gdp_01-04-22.txt globalData/structFiles_gdp_01-04-22/ 0.9 otherAny 3.5 1> bfactorAnalysis/results2/GDP/anyGDPOther.out 2> bfactorAnalysis/results2/GDP/anyGDPOtherErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_gdp_01-04-22 GDP 0.01 globalData/standalone_gdp_01-04-22.txt globalData/structFiles_gdp_01-04-22/ 0.5 otherAvg 3.5 1> bfactorAnalysis/results2/GDP/avgGDPOther.out 2> bfactorAnalysis/results2/GDP/avgGDPOtherErr.err


### NAD
time python3 bfactorAnalysis/code/main.py globalData/standalone_nad_01-04-22 NAD 0.01 globalData/standalone_nad_01-04-22.txt globalData/structFiles_nad_01-04-22/ 0.9 ligandAny 3.5 1> bfactorAnalysis/results2/NAD/anyNAD.out 2> bfactorAnalysis/results2/NAD/anyNADErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_nad_01-04-22 NAD 0.01 globalData/standalone_nad_01-04-22.txt globalData/structFiles_nad_01-04-22/ 0.5 ligandAvg 3.5 1> bfactorAnalysis/results2/NAD/avgNAD.out 2> bfactorAnalysis/results2/NAD/avgNADErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_nad_01-04-22 NAD 0.01 globalData/standalone_nad_01-04-22.txt globalData/structFiles_nad_01-04-22/ 0.9 ligandPlusAny 3.5 1> bfactorAnalysis/results2/NAD/anyNADPlus.out 2> bfactorAnalysis/results2/NAD/anyNADPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_nad_01-04-22 NAD 0.01 globalData/standalone_nad_01-04-22.txt globalData/structFiles_nad_01-04-22/ 0.5 ligandPlusAvg 3.5 1> bfactorAnalysis/results2/NAD/avgNADPlus.out 2> bfactorAnalysis/results2/NAD/avgNADPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_nad_01-04-22 NAD 0.01 globalData/standalone_nad_01-04-22.txt globalData/structFiles_nad_01-04-22/ 0.9 otherAny 3.5 1> bfactorAnalysis/results2/NAD/anyNADOther.out 2> bfactorAnalysis/results2/NAD/anyNADOtherErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_nad_01-04-22 NAD 0.01 globalData/standalone_nad_01-04-22.txt globalData/structFiles_nad_01-04-22/ 0.5 otherAvg 3.5 1> bfactorAnalysis/results2/NAD/avgNADOther.out 2> bfactorAnalysis/results2/NAD/avgNADOtherErr.err


### FAD
time python3 bfactorAnalysis/code/main.py globalData/standalone_fad_01-04-22 FAD 0.01 globalData/standalone_fad_01-04-22.txt globalData/structFiles_fad_01-04-22/ 0.9 ligandAny 3.5 1> bfactorAnalysis/results2/FAD/anyFAD.out 2> bfactorAnalysis/results2/FAD/anyFADErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_fad_01-04-22 FAD 0.01 globalData/standalone_fad_01-04-22.txt globalData/structFiles_fad_01-04-22/ 0.5 ligandAvg 3.5 1> bfactorAnalysis/results2/FAD/avgFAD.out 2> bfactorAnalysis/results2/FAD/avgFADErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_fad_01-04-22 FAD 0.01 globalData/standalone_fad_01-04-22.txt globalData/structFiles_fad_01-04-22/ 0.9 ligandPlusAny 3.5 1> bfactorAnalysis/results2/FAD/anyFADPlus.out 2> bfactorAnalysis/results2/FAD/anyFADPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_fad_01-04-22 FAD 0.01 globalData/standalone_fad_01-04-22.txt globalData/structFiles_fad_01-04-22/ 0.5 ligandPlusAvg 3.5 1> bfactorAnalysis/results2/FAD/avgFADPlus.out 2> bfactorAnalysis/results2/FAD/avgFADPlusErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_fad_01-04-22 FAD 0.01 globalData/standalone_fad_01-04-22.txt globalData/structFiles_fad_01-04-22/ 0.9 otherAny 3.5 1> bfactorAnalysis/results2/FAD/anyFADOther.out 2> bfactorAnalysis/results2/FAD/anyFADOtherErr.err
time python3 bfactorAnalysis/code/main.py globalData/standalone_fad_01-04-22 FAD 0.01 globalData/standalone_fad_01-04-22.txt globalData/structFiles_fad_01-04-22/ 0.5 otherAvg 3.5 1> bfactorAnalysis/results2/FAD/avgFADOther.out 2> bfactorAnalysis/results2/FAD/avgFADOtherErr.err

