import numpy;
import sys;



def q5(TmAST,AST,TmFGM):
  return float(1.14*((TmAST-AST)/TmFGM))

print q5(10.0,0.0,13.0)

# test result: 87.6923076923%
# exel result: 88% 
# excel location: STAT ANALYSIS(S3)



def FTmPoss(FTM,FTA):
  return float(((1.0-(FTM/FTA))**2.0)*0.4*FTA)

print FTmPoss(0.0,2.0)
# test result: 80.0%
# exel result: 88% 
# excel location: STAT ANALYSIS(Y3)






def Usage_Rate(FGA,FTA,TOV,TmMIN,MIN,TmFGA,TmFTA,TmTOV):
  return float(100*((FGA+0.4*FTA+TOV)*(TmMIN/5))/(MIN*(TmFGA+0.4*TmFTA+TmTOV)))

print Usage_Rate(1.0,2.0,1.0,200.0,4.0,52.0,26.0,15.0)
# test result: 36.175
# exel result: 36.7 
# excel location: STAT ANALYSIS(N3)





def AST_perc(AST,MIN,TmMIN,TmFGM,FGM):
  return float(100*AST/(((MIN/(TmMIN/5))*TmFGM)-FGM))

print AST_perc(1.0,4.0,200.0,13.0,1.0)
# test result: 333.33
# exel result: ??????
# excel location: ??????




def ASTr(AST,FGM):
  if FGM == 0: 
    return 0.0
  else: 
    return float(AST/FGM)

print ASTr(1.0,0.0)
# test result: 0.0
# exel result: ??????
# excel location: ??????



def AST_Ratio(AST,FGA,FTA,TOV):
  return float((100*AST)/(FGA+(FTA*0.4)+AST+TOV))

print AST_Ratio(2.0,9.0,7.0,5.0)
# test result: 10.63829
# exel result: ??????
# excel location: ??????



def TmPoss(FGA, TmOREB,oppDREB,FTA,FGM,TOV):
  return float(FGA-(TmOREB/(TmOREB+oppDREB))*(FGA-FGM)*1.07+TOV + 0.4*FTA)

print TmPoss(52.0, 9.0, 30.0, 26.0, 13.0, 15.0)
# test result: 67.77
# exel result: 68
# excel location: STAT ANALYSIS(C19)



def Pace(TmPoss,OppPoss,TmMIN):
  return float(40*((TmPoss+OppPoss)/(2*(TmMIN/5))))

print Pace(67.77, 65.04,200.0)
# test result: 66.405
# exel result: ??????
# excel location: ??????




def STL_perc(STL,TmMIN,MIN,OppPoss):
  return  float(100*(STL*(TmMIN/5))/(MIN*OppPoss))

print STL_perc(1.0,200.0,4.0,65.04)
# test result: 15.375
# exel result: ??????
# excel location: ??????



def DFG_perc(OppFGM,OppFGA):
  if OppFGA == 0:
    return 0.0
  else:
    return float(OppFGM/OppFGA)
  
print DFG_perc(29.0,70.0)
# test result: 41.43%
# exel result: 41.4%
# excel location: OPP BOX(D19)



def DOREB_perc(OppOREB,TmDREB):
  return float(OppOREB/(OppOREB/TmDREB))

print DOREB_perc(17.0,20.0)
# test result: 20.0
# exel result: 45.9% 
# excel location: STAT ANALYSIS(AC19)
# Note: different fomular from excel sheet, double check 





def FMwt(DFG_perc,DOREB_perc):
  return float((DFG_perc*(1-DOREB_perc))/(DFG_perc
      *(1-DOREB_perc)+(1-DFG_perc)*DOREB_perc))

print FMwt(0.4143,0.459)
# test result: 0.4546
# exel result: 0.45 
# excel location: STAT ANALYSIS(AD19)
# Note: this data depends on DOREB, need to check function first 


def Stops_1(STL,BLK,FMwt,DOREB_perc,DREB):
  return float(STL+BLK*FMwt*(1-1.07*DOREB_perc)+DREB*(1-FMwt))

print Stops_1(0.0,1.0,0.45,0.459,2.0)
# test result: 1.328
# exel result: 1.3 
# excel location: STAT ANALYSIS(AE4)






def Stops_2(OppFGA,OppFGM,TmBLK,TmMIN,FMwt,DOREB_perc
      ,OppTOV,TmSTL,MIN,PF,TmPF,OppFTA,OppFTM):
  return  float((((OppFGA-OppFGM-TmBLK)/TmMIN)*FMwt*(1-1.07*DOREB_perc) 
      +((OppTOV-TmSTL)/TmMIN))*MIN+(PF/TmPF) 
      *0.4*OppFTA*(1-(OppFTM/OppFTA))**2)

print Stops_2(70.0,29.0,1.0,200.0,0.45,0.459,8.0,1.0,0.0,0.0,15.0,18.0,13.0)
# test result: 0.0
# exel result: 0.32 
# excel location: STAT ANALYSIS(AF3)

print Stops_2(70.0,29.0,1.0,200.0,0.45,0.459,8.0,1.0,15.0,1.0,15.0,18.0,13.0)
# test result: 1.249
# exel result: 1.25 
# excel location: STAT ANALYSIS(AF4)




def Stops(Stops_1,Stops_2):
  return float(Stops_1+Stops_2)

print Stops(1.3,1.25)
# test result: 2.55
# exel result: 1.9 
# excel location: STAT ANALYSIS(AH4)





def Stop_perc(Stops,OppMIN,TmPoss,MIN):
  if(TmPoss*MIN == 0):
    return 0.0;
  else:
    return float((Stops*OppMIN)/(TmPoss*MIN))
  
print Stop_perc(1.9,200.0,67.77,15.0)
# test result: 0.3739
# exel result: 0.9 
# excel location: STAT ANALYSIS(H4)




def OppPtsPScorPoss(OppPTS,OppFGM,OppFTM,OppFTA):
  return float(OppPTS/(OppFGM+(1-(1-(OppFTM/OppFTA))**2 )*OppFTA*0.4))

print OppPtsPScorPoss(77.0,29.0,17.0,18.0)
# test result: 2.128
# exel result: ???????  
# excel location: ????????





def TmORTG (TmPoints, TmPoss):
  if TmPoss == 0:
    return 0.0
  return float(100*(TmPoints/TmPoss))

print TmORTG(45.0, 67.77)
# test result: 66.4
# exel result: 64.0 
# excel location: STAT ANALYSIS(F19)





def q12(TmAST,TmMIN,MIN,AST,TmFGM,FGM):
  return float(((TmAST/TmMIN)*MIN*5-AST)/((TmFGM/TmMIN)*MIN*5-FGM))

print q12(10.0,200.0,4.0,0.0,13.0,0.0)
# test result: 76.92%
# exel result: 77% 
# excel location: STAT ANALYSIS(T3)




def FGPart(FGM,PTS,FTM,FGA,qAST):
  return float(FGM*(1-0.5*(((PTS-FTM))/(2*FGA))*qAST))

print FGPart(4.0,11.0,2.0,13.0,1.08)
# test result: 325.23%
# exel result: 325% 
# excel location: STAT ANALYSIS(Q5)




def PProdAst(TmFGM, FGM, Tm3PM, TmPTS, TmFTM, PTS, FGA, AST, FGM_3, FTM, TmFGA):
  return float(2*((TmFGM-FGM+0.5*(Tm3PM-FGM_3))/(TmFGM-FGM))*0.5
      *(((TmPTS-TmFTM)-(PTS-FTM))/(2*(TmFGA-FGA) ))*AST)

print PProdAst(13.0,0.0,4.0,45.0,15.0,0.0,3.0,1.0,0.0,0.0,52.0)
# test result: 35.32%
# exel result: 35% 
# excel location: STAT ANALYSIS(AA4)




def PProdFG(FGM,PTS,FTM,FGA,qAST,FGM_3):
  return float(2*(FGM+0.5*FGM_3)*1-0.5*((PTS-FTM)/(2*FGA))*qAST)

print PProdFG(0.0,0.0,0.0,1.0,0.78,0.0)
# test result: 0%
# exel result: 0% 
# excel location: STAT ANALYSIS(Z3)

print PProdFG(4.0,11.0,2.0,13.0,1.08,1.0)
# test result: 881%
# exel result: 732% 
# excel location: STAT ANALYSIS(Z5)




def qAST(MIN,TmMIN,q_12,q_5):
  return float(q_5*(MIN/(TmMIN/5))+(1-(MIN/(TmMIN/5))*q_12))
print qAST(4.0,200.0,0.77,0.88)
# test result: 101%
# exel result: 78% 
# excel location: STAT ANALYSIS(R3)




def PProdOREB(ORB,TmOREBWgt,TmPlay_pect,TmPTS,
      TmFGM,TmFTM,TmFTA):
  return float(ORB*TmOREBWgt*TmPlay_pect*(TmPTS/(TmFGM+(1-(1-(TmFTM/TmFTA))**2 )
      *0.4*TmFTA)))

print PProdOREB(1.0, 0.56, 0.278, 45.0, 13.0, 15.0, 26.0)
# test result: 32.5%
# exel result: 33% 
# excel location: STAT ANALYSIS(AB9)




def TotPoss(ScPoss,FGmPoss,FTmPoss,TOV):
  return float(ScPoss+FGmPoss+FTmPoss+TOV)

print TotPoss(0.0,0.8,0.75,1.0)
# test result: 2.55
# exel result: 2.6
# excel location: STAT ANALYSIS(C3)


def PProd(PProdFG, PProdAst,FTM,TmOREB,
    TMScorPoss,TmOREBWgt,TmPlay_pect,PProdOREB):
  return float((PProdFG+PProdAst+FTM)*(1-(TmOREB/TMScorPoss)
      *TmOREBWgt*TmPlay_pect)+PProdOREB)

print PProd(0.0,0.35,0.0,9.0,21.5,0.56,0.278,0.0)
# test result: 0.327
# exel result: 0.3
# excel location: STAT ANALYSIS(E4)








