import numpy;
import sys;



def q5(TmAST,AST,TmFGM):
  return float(1.14*((TmAST-AST)/TmFGM))

print q5(10.0,0.0,13.0)

# test result: 0.876923076923
# exel result: 88% 
# excel location: STAT ANALYSIS(S3)



def FTmPoss(FTM,FTA):
  return float(((1.0-(FTM/FTA))**2.0)*0.4*FTA)

print FTmPoss(0.0,2.0)
# test result: 0.8
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

