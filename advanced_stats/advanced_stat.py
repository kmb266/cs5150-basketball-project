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





