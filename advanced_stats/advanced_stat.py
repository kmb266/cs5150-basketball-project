import nmpy; 
import sys; 
import arithmetic; 


def TmPoints
def TmPoss(FGA, TmOREB, oppDREB, FTA,FGM):
	return FGA-(TmOREB/(TmOREB+oppDREB))*(FGA-FGM)*1.07+TOV + 0.4*FTA
def Team_Offensive_Rating (TmPoints, TmPoss):
	return 100*(TmPoints/TmPoss)




def PProd(PProdFG, PProdAst,FTM,TmOREB,
		TMScorPoss,TmOREBWgt,TmPlay,PProdOREB):
	return (PProdFG+PProdAst+FTM)*(1-(TmOREB/TMScorPoss)
			*TmOREBWgt*TmPlay_pect)+PProdOREB


def PProdFG(FGM,PTS,,FTM,FGA,qAST):
	return 2*(FGM+0.5*3PM)*1-0.5*((PTS-FTM)/(2*FGA))*qAST


def PProdAst(TmFGM, FGM, Tm3PM, TmPTS, TmFTM, PTS, FGA, AST):
	return 2*((TmFGM-FGM+0.5*(Tm3PM-3PM))/(TmFGM-FGM))*0.5
			*(((TmPTS-TmFTM)-(PTS-FTM))/(2*(TmFGA-FGA) ))*AST


def PProdOREB(ORB, TmOREBWgt,TmPlay, TmPTS, 
			TmFGM,TmFTM,TmFTA,TmFTA):
	return ORB*TmOREBWgt*TmPlay_pect*(TmPTS/(TmFGM+(1-(1-(TmFTM/TmFTA))^2 )
			*0.4*TmFTA))






def TotPoss(ScPoss,FGmPoss,FTmPoss,TOV):
	return ScPoss+FGmPoss+FTmPoss+TOV



def ScPoss(FGPart,ASTPart,FTPart,TmOREB,
			TmScorPoss,TmOREBWgt,TmPlay,OREBPart):
	return (FGPart+ASTPart+FTPart)*(1-(TmOREB/TmScorPoss)
		*TmOREBWgt*TmPlay_pect)+OREBPart


def FGPart(FGM,PTS,FTM,FGA,qAST):
	return FGM*(1-0.5*(((PTS-FTM))/(2*FGA))*qAST)


def qAST(MIN,TmMin,TmMIN):
	return (MIN/(TmMin/5))*q_5+(1-(MIN/(TmMIN/5))*q_12)


def q5(1.14*(TmAST,AST,TmFGM):
	return 1.14*((TmAST-AST)/TmFGM)


def q12(TmAST,TmMIN,MIN,AST,TmFGM,FGM):
	return ((TmAST/TmMIN)*MIN*5-AST)/((TmFGM/TmMIN)*MIN*5-FGM)


def ASTPart(TmPTS,TmFTM,PTS,FTM,TmFGA,FGA,AST):
	return 0.5*(((TmPTS-TmFTM)-(PTS-FTM))/(2*(TmFGA-FGA) ))*AST


def FTPart(FTM,FTA):
	return (1-(1-(FTM/FTA))^2 )*0.4*FTA


def TmOREBWgt(TmFGM,TmFTM,TmFTA):
	return TmFGM+(1-(1-(TmFTM/TmFTA))^2 )*TmFTA*0.4


def TmOREBWgt(TmOREB,TmPlay):
	return ((1-TmOREB_pect)*TmPlay_pect)/((1-TmOREB_pect)
			*TmPlay_pect+TmOREB_pect*(1-TmPlay_pect))

def TmOREB_pect(TmOREB,OppTREB):
	return TmOREB/(TmOREB+(OppTREB-OppDREB))


def TmPlay(TmFGA,TmFTA,TmTOV):
	return TmFGA+TmFTA*0.4+TmTOV


def TmPlay_pect(TmScorPoss, TmFGA,TmFTA,TmTOV):
	return TmScorPoss/(TmFGA+TmFTA*0.4+TmTOV)



def OREBPart(OREB,TmOREBWgt,TmPlay_pect):
	return OREB*TmOREBWgt*TmPlay_pect


def FGmPoss(FGA,FGM,TmOREB_pect):
	return (FGA-FGM)*(1-1.07*TmOREB_pect)


def FTmPoss(FTM,FTA):
	return ((1-(FTM/FTA))^2 )*0.4*FTA


def Individual_Offensize_Rating(PProd, TotPoss):
	return 100*(PProd/TotPoss)




def Individual_Floor_Percentage(ScPoss,TotPoss):
	return ScPoss/TotPoss


def Team_Floor_Percentage(TmScorPoss, TmPoss):
	return TmScorPoss/TmPoss



def TmDRTG(OppPTS,TmPoss): 
	return 100*(OppPTS/TmPoss)


def DRTG(TmDRTG,OppPtsPScorPoss,top_perc,mDRTG):
	return TmDRTG+0.2*(100*OppPtsPScorPoss*(1-Stop_perc)-TmDRTG)	



def OppPtsPScorPoss(OppPTS,OppFGM,OppFTM,OppFTA):
	return OppPTS/(OppFGM+(1-(1-(OppFTM/OppFTA))^2 )*OppFTA*0.4)



def Stop_perc(Stops,OppMIN,TmPoss,MIN):
	return (Stops*OppMIN)/(TmPoss*MIN)




def Stops(Stops_1,Stops_2):
	return Stops_1+Stops_2



def Stops_1(STL,BLK,FMwt,DOREB_perc,DREB,FMwt):
	return STL+BLK*FMwt*(1-1.07*DOREB_perc)+DREB*(1-FMwt)




def FMwt(DFG_perc,DOREB_perc,DFG_perc):
	return (DFG_perc*(1-DOREB_perc))/(DFG_perc
			*(1-DOREB_perc)+(1-DFG_perc)*DOREB_perc)




def DOREB_perc(OppOREB,TmDREB):
	return OppOREB/(OppOREB/TmDREB)


def DFG_perc(OppFGM,OppFGA):
	return OppFGM/OppFGA



def Stops_2(OppFGA,OppFGM,TmBLK,TmMIN,FMwt,DOREB_perc
			,OppTOV,TmSTL,MIN,PF,TmPF,OppFTA,OppFTM):
	return  (((OppFGA-OppFGM-TmBLK)/TmMIN)*FMwt*(1-1.07*DOREB_perc)
			+((OppTOV-TmSTL)/TmMIN))*MIN+(PF/TmPF)
			*0.4*OppFTA*(1-(OppFTM/OppFTA))^2




def eFG_perc(FGM,FGA):
	return (FGM+0.5*3PM)/FGA 



def Turnover_perc(TOV,FGA,FTA,TOV):
	return TOV/(FGA+0.4*FTA+TOV)


def FTr(FTA,FGA):
	return FTA/FGA


def FG_2_perc(FGM_2,FGA_2):
	return FGM_2/FGA_2



def FG_3_perc(FGM_3/FGA_3):
	return FGM_3/FGA_3


def FGr_2(FGA_2,FGA):
	return FGA_2/FGA


def FGr_3(FGA_3,FGA):
	return FGA_3/FGA



def Usage_Rate(FGA,FTA,TOV,TmMIN,MIN,TmFGA,TmFTA,TmTOV):
	return 100*((FGA+0.4*FTA+TOV)*(TmMIN/5))/(MIN*(TmFGA+0.4*TmFTA+TmTOV))



def AST_perc(AST,MIN,TmMIN,TmFGM,FGM):
	return 100*AST/(((MIN/(TmMIN/5))*TmFGM)-FGM)



def ASTr(AST,FGM):
	return AST/FGM


def AST_Ratio(AST,FGA,FTA,TOV):
	return (100*AST)/(FGA+(FTA*0.4)+AST+TOV)


def TS_perc(PTS,FGA,FTA):
	return PTS/(2*(FGA+0.4*FTA))


def Total_REB(TREB,TmMIN,MIN,TmTREB,OppTREB):
	return 100*(TREB*(TmMIN/5))/(MIN*(TmTREB+OppTREB))


def STL_perc(STL,TmMIN,MIN,OppPoss):
	return  100*(STL*(TmMIN/5))/(MIN*OppPoss)



def BLK_perc(BLK,TmMIN,MIN,OppFGA,Opp3PA):
	return 100*(BLK*(TmMIN/5))/(MIN*(OppFGA-Opp3PA))



def Game_Score(PTS,FGM,FGA,FTA,FTM,ORE,DREB,STL,AST,BLK,PF,TOV):
	return PTS+0.4*FGM-0.7*FGA-0.4
	*(FTA-FTM)+0.7*ORE-0.3*DREB+STL
	+0.7*AST+0.7*BLK-0.4*PF-TOV



def Pace(TmPoss,OppPoss,TmMIN):
	return 40*((TmPoss+OppPoss)/(2*(TmMIN/5)))


def PIE(PTS,FGM,FTM,FGA,FTA,DREB,OREB,AST,STL,BLK
	,PF,TO,GmPTS,GmFGM,GmFTM,GmFGA,GmFTA,GmDREB
	,GmOREB,GmAST,GmSTL,GmBLK,GmPF,GmTO):
	return (PTS+FGM+FTM-FGA-FTA+DREB+(0.5*OREB)+AST+STL
		+(0.5*BLK)-PF-TO)/(GmPTS+GmFGM+GmFTM-GmFGA
		-GmFTA+GmDREB+(0.5*GmOREB)+GmAST+GmSTL+(0.5*GmBLK)-GmPF-GmTO)





