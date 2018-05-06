import advanced_stat; 
import numpy;


def stats_calculation(data):
	for dic in data:

		#get basic data 

		AST = 1
		BLK = 1
		DREB = 1
		FGM = 1 
		FGA = 1  
		FTA = 1
		FGM_2 =1 
		FGA_2 = 1 
		FGM_3 = 1  
		FGA_3 = 1 
		FTM = 1   
		MIN = 1 
		ORE = 1 
		OREB_perc = 1 
		OppDREB = 1 
		OppTREB = 1 
		OppOREB = 1 
		OppFGM = 1 
		OppFGA = 1 
		OppFTA = 1 
		OppPTS
		OppFTM = 1 
		OppTOV = 1 
		Opp3PA = 1 
		PF = 1 
		PTS = 1 
		STL = 1
		TmAST = 1  
		TmPoints = 1 
		TmFGA = 1 
		TmOREB = 1 
		TmDREB = 1 
		TmFTA  = 1
		TmSTL = 1 
		TmFTM = 1
		TmFGM = 1
		TmFGA = 1
		TmTOV = 1
		Tm3PM = 1
		TmMIN = 1
		TmPF = 1 
		TmTREB = 1 
		TOV = 1 
		TREB = 1 


		#first level calculation 
		TmPoss = TmPoss(TmFGA,TmOREB,oppDREB,TmFTA,TmFGM,TmTOV) 
		PProdAst = PProdAst(TmFGM, FGM, Tm3PM, TmPTS, TmFTM, PTS, FGA, AST, FGM_3,FTM, TmFGA)
		q5 = q5(TmAST,AST,TmFGM)
		q12 = q12(TmAST,TmMIN,MIN,AST,TmFGM,FGM)
		ASTPart =  ASTPart(TmPTS,TmFTM,PTS,FTM,TmFGA,FGA,AST)
		FTPart = FTPart(FTM,FTA)
		TmScorPoss = TmScorPoss(TmFGM,TmFTM,TmFTA)
		TmOREB_pect = TmOREB_pect(TmOREB,OppTREB,OppDREB)
		TmPlay = TmPlay(TmFGA,TmFTA,TmTOV)
		FTmPoss = FTmPoss(FTM,FTA)
		DOREB_perc = DOREB_perc(OppOREB,TmDREB)
		DFG_perc = DFG_perc(OppFGM,OppFGA)
		eFG_perc = eFG_perc(FGM,FGA,FGM_3)
		Turnover_perc = Turnover_perc(TOV,FGA,FTA)
		FTr = FTr(FTA,FGA)
		FG_2_perc = FG_2_perc(FGM_2,FGA_2)
		FG_3_perc = FG_3_perc(FGM_3,FGA_3)
		FGr_2 = FGr_2(FGA_2,FGA)
		FGr_3 = FGr_3(FGA_3,FGA)
		Usage_Rate = Usage_Rate(FGA,FTA,TOV,TmMIN,MIN,TmFGA,TmFTA,TmTOV)
		ASTPart = AST_perc(AST,MIN,TmMIN,TmFGM,FGM)
		ASTr = ASTr(AST,FGM)
		AST_Ratio = AST_Ratio(AST,FGA,FTA,TOV)
		OppPtsPScorPoss = OppPtsPScorPoss(OppPTS,OppFGM,OppFTM,OppFTA)
		TS_perc = TS_perc(PTS,FGA,FTA)
		Total_REB_pect = Total_REB_pect (TREB,TmMIN,MIN,TmTREB,OppTREB)
		BLK_perc = BLK_perc(BLK,TmMIN,MIN,OppFGA,Opp3PA)
		Game_Score = Game_Score(PTS,FGM,FGA,FTA,FTM,ORE,DREB,STL,AST,BLK,PF,TOV)
		PIE = PIE(PTS,FGM,FTM,FGA,FTA,DREB,OREB,AST,STL,BLK,PF,TO,GmPTS,GmFGM,GmFTM,GmFGA,GmFTA,GmDREB,GmOREB,GmAST,GmSTL,GmBLK,GmPF,GmTO)


		#second level calculation 
		TmORTG = TmORTG (TmPoints, TmPoss)
		qAST = qAST(MIN,TmMIN,q_12,q_5)
		TmPlay_pect = TmPlay_pect(TmScorPoss, TmFGA,TmFTA,TmTOV)
		FGmPoss = FGmPoss(FGA,FGM,TmOREB_pect)
		Team_Floor_Percentage = Team_Floor_Percentage(TmScorPoss, TmPoss)
		TmDRTF = TmDRTG(OppPTS,TmPoss)
		Stop_perc = Stop_perc(Stops,OppMIN,TmPoss,MIN)
		FMwt = FMwt(DFG_perc,DOREB_perc)


		#third level calculation 
		





	return [TmPoss, PProdAst,]
