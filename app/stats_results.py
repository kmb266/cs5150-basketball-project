import advanced_stat as function;
import numpy;


def stats_calculation(data):
	#print "Number of players: " + str(len(data["data"]))
	#print "Calculating advanced stats:"
	for player in data["data"]:
		#print "--Calculating stats for " + player["name"]
		games = player["games"]
		team_id = player["team"]
		for game_id, box_score in games.items():
			#print "----Calculating game " + str(game_id)
			# Player values
			AST = box_score["AST"]
			BLK = box_score["BLK"]
			DREB = box_score["DREB"]
			FGM_2 = box_score["FG"]
			FGA_2 = box_score["FGA"]
			FGM_3 = box_score["3PT"]
			FGA_3 = box_score["FGA3"]
			FGA = FGA_2 + FGA_3
			if FGA == 0:
				FGA = 1
			FGM = FGM_2 + FGM_3
			FTA = box_score["FTA"]
			if FTA == 0:
				FTA = 1
			FTM = box_score["FT"]
			MIN = abs(box_score["MIN"])
			if MIN == 0:
				continue
			OREB = box_score["OREB"]
			PF = box_score["PF"]
			PTS = box_score["PTS"]
			STL = box_score["STL"]
			TOV = box_score["TO"]
			TREB = box_score["REB"]

			OREB_perc = 1

			opponent_id = box_score["away"]
			if team_id == opponent_id:
				opponent_id = box_score["home"]

			# Team values
			team_boxscore = data["teamOverall"][opponent_id]["games"][game_id]
			TmAST = team_boxscore["AST"]
			TmPoints = team_boxscore["PTS"]
			TmPTS = TmPoints
			TmFGA = team_boxscore["FGA"]
			TmOREB = team_boxscore["OREB"]
			TmDREB = team_boxscore["DREB"]
			TmFTA  = team_boxscore["FTA"]
			TmSTL = team_boxscore["STL"]
			TmFTM = team_boxscore["FT"]
			TmFGM = team_boxscore["FG"]
			TmFGA = team_boxscore["FGA"]
			TmTOV = team_boxscore["TO"]
			Tm3PM = team_boxscore["3PT"]
			TmMIN = 200 #team_boxscore["MIN"]
			TmPF = team_boxscore["PF"]
			TmTREB = team_boxscore["REB"]
			TmBLK = team_boxscore["BLK"]

			# Opponent team values
			opponent_boxscore = data["teamOverall"][opponent_id]["games"][game_id]
			OppPTS = opponent_boxscore["PTS"]
			OppDREB = opponent_boxscore["DREB"]
			OppTREB = opponent_boxscore["REB"]
			OppOREB = opponent_boxscore["OREB"]
			OppFGM = opponent_boxscore["FG"]
			OppFGA = opponent_boxscore["FGA"]
			OppFTA = opponent_boxscore["FTA"]
			OppPTS = opponent_boxscore["PTS"]
			OppFTM = opponent_boxscore["FT"]
			OppTOV = opponent_boxscore["TO"]
			Opp3PA = opponent_boxscore["3PT"]
			OppSTL = opponent_boxscore["STL"]
			OppAST = opponent_boxscore["AST"]
			OppBLK = opponent_boxscore["BLK"]
			OppPF = opponent_boxscore["PF"]
			OppMIN = 200

			GmPTS = OppPTS + TmPoints
			GmFGM = OppFGM + TmFGM
			GmFTM = OppFTM + TmFTM
			GmFGA = OppFGA + TmFGA
			GmFTA = OppFTA + TmFTA
			GmDREB = OppDREB + TmDREB
			GmOREB = OppOREB + TmOREB
			GmAST = OppAST + TmAST
			GmSTL = OppSTL + TmSTL
			GmBLK = OppBLK + TmBLK
			GmPF = OppPF + TmPF
			GmTO = OppTOV + TmTOV

				#first level calculation
			TmPoss = function.TmPoss(TmFGA,TmOREB,OppDREB,TmFTA,TmFGM,TmTOV)
			OppPoss = function.OppPoss(OppFGA,OppOREB,TmDREB,OppFTA,OppFGM,OppTOV)
			PProdAst = function.PProdAst(TmFGM, FGM, Tm3PM, TmPTS, TmFTM, PTS, FGA, AST, FGM_3,FTM, TmFGA)
			q5 = function.q5(TmAST,AST,TmFGM)
			q12 = function.q12(TmAST,TmMIN,MIN,AST,TmFGM,FGM)
			ASTPart =  function.ASTPart(TmPTS,TmFTM,PTS,FTM,TmFGA,FGA,AST)
			FTPart = function.FTPart(FTM,FTA)
			TmScorPoss = function.TmScorPoss(TmFGM,TmFTM,TmFTA)
			TmOREB_pect = function.TmOREB_pect(TmOREB,OppTREB,OppDREB)
			TmPlay = function.TmPlay(TmFGA,TmFTA,TmTOV)
			FTmPoss = function.FTmPoss(FTM,FTA)
			DOREB_perc = function.DOREB_perc(OppOREB,TmDREB)
			DFG_perc = function.DFG_perc(OppFGM,OppFGA)
			eFG_perc = function.eFG_perc(FGM,FGA,FGM_3)
			Turnover_perc = function.Turnover_perc(TOV,FGA,FTA)
			FTr = function.FTr(FTA,FGA)
			FG_2_perc = function.FG_2_perc(FGM_2,FGA_2)
			FG_3_perc = function.FG_3_perc(FGM_3,FGA_3)
			FGr_2 = function.FGr_2(FGA_2,FGA)
			FGr_3 = function.FGr_3(FGA_3,FGA)
			Usage_Rate = function.Usage_Rate(FGA,FTA,TOV,TmMIN,MIN,TmFGA,TmFTA,TmTOV)
			ASTPart = function.AST_perc(AST,MIN,TmMIN,TmFGM,FGM)
			ASTr = function.ASTr(AST,FGM)
			AST_Ratio = function.AST_Ratio(AST,FGA,FTA,TOV)
			OppPtsPScorPoss = function.OppPtsPScorPoss(OppPTS,OppFGM,OppFTM,OppFTA)
			TS_perc = function.TS_perc(PTS,FGA,FTA)
			Total_REB_pect = function.Total_REB_pect (TREB,TmMIN,MIN,TmTREB,OppTREB)
			BLK_perc = function.BLK_perc(BLK,TmMIN,MIN,OppFGA,Opp3PA)
			Game_Score = function.Game_Score(PTS,FGM,FGA,FTA,FTM,OREB,DREB,STL,AST,BLK,PF,TOV)
			PIE = function.PIE(PTS,FGM,FTM,FGA,FTA,DREB,OREB,AST,STL,BLK,PF,TOV,GmPTS,GmFGM,GmFTM,GmFGA,GmFTA,GmDREB,GmOREB,GmAST,GmSTL,GmBLK,GmPF,GmTO)

			#adding results to dictionary
			#data["TmPoss"] = TmPoss
			#data["OppPoss"] = OppPoss
			#data["PProdAst"] = PProdAst
			#data["q5"] = q5
			#data["q12"] = q12
			#data["ASTPart"] = ASTPart
			#data["FTPart"] = FTPart
			#data["TmScorPoss"] = TmScorPoss
			#data["TmOREB_pect"] = TmOREB_pect
			#data["TmPlay"] = TmPlay
			#data["FTmPoss"] = FTmPoss
			#data["DOREB_perc"] = DOREB_perc
			#data["DFG_perc"] = DFG_perc
			#data["eFG_perc"] = eFG_perc
			#data["Turnover_perc"] = Turnover_perc
			#data["FTr"] = FTr
			#data["FG_2_perc"] = FG_2_perc
			#data["FG_3_perc"] = FG_3_perc
			#data["FGr_2"] = FGr_2
			#data["FGr_3"] = FGr_3

			box_score["Usage_Rate"] = Usage_Rate
			box_score["PIE"] = PIE
			box_score["Game_Score"] = Game_Score
			#data["ASTPart"] = ASTPart
			#data["ASTr"] = ASTr
			#data["AST_Ratio"] = AST_Ratio
			#data["OppPtsPScorPoss"] = OppPtsPScorPoss
			#data["TS_perc"] = TS_perc
			#data["Total_REB_pect"] = Total_REB_pect
			#data["BLK_perc"] = BLK_perc
			#data["Game_Score"] = Game_Score
			#data["PIE"] = PIE

			#second level calculation
			TmORTG = function.TmORTG (TmPoints, TmPoss)
			qAST = function.qAST(MIN,TmMIN,q12,q5)
			TmPlay_pect = function.TmPlay_pect(TmScorPoss, TmFGA,TmFTA,TmTOV)
			FGmPoss = function.FGmPoss(FGA,FGM,TmOREB_pect)
			Team_Floor_Percentage = function.Team_Floor_Percentage(TmScorPoss, TmPoss)
			TmDRTG = function.TmDRTG(OppPTS,TmPoss)
			FMwt = function.FMwt(DFG_perc,DOREB_perc)
			STL_perc = function.STL_perc(STL,TmMIN,MIN,OppPoss)
			Pace = function.Pace(TmPoss,OppPoss,TmMIN)

			#adding results to dictionary
			#data["TmORTG"] = TmORTG
			#data["qAST"] = qAST
			#data["TmPlay_pect"] = TmPlay_pect
			#data["FGmPoss"] = FGmPoss
			#data["Team_Floor_Percentage"] = Team_Floor_Percentage
			#data["TmDRTG"] = TmDRTG
			#data["FMwt"] = FMwt
			#data["Pace"] = Pace
			#data["STL_perc"] = STL_perc

			#third level calculation
			PProdFG = function.PProdFG(FGM,PTS,FTM,FGA,qAST,FGM_3)
			FGPart = function.FGPart(FGM,PTS,FTM,FGA,qAST)
			TmOREBWgt = function.TmOREBWgt(TmOREB_pect,TmPlay_pect)
			Stops_1 = function.Stops_1(STL,BLK,FMwt,DOREB_perc,DREB)
			Stops_2 = function.Stops_2(OppFGA,OppFGM,TmBLK,TmMIN,FMwt,DOREB_perc,OppTOV,TmSTL,MIN,PF,TmPF,OppFTA,OppFTM)

			#adding results to dictionary
			#data["PProdFG"] = PProdFG
			#data["FGPart"] = FGPart
			#data["TmOREBWgt"] = TmOREBWgt
			#data["Stops_1"] = Stops_1
			#data["Stops_2"] = Stops_2

			#forth level calculation
			PProdOREB = function.PProdOREB(OREB,TmOREBWgt,TmPlay_pect,TmPTS,TmFGM,TmFTM,TmFTA)
			OREBPart = function.OREBPart(OREB,TmOREBWgt,TmPlay_pect)
			Stops = function.Stops(Stops_1,Stops_2)

			#adding results to dictionary
			#data["PProdOREB"] = PProdOREB
			#data["OREBPart"] = OREBPart
			#data["Stops"] = Stops

			#fifth level calculation
			PProd = function.PProd(PProdFG, PProdAst,FTM,TmOREB,TmScorPoss,TmOREBWgt,TmPlay_pect,PProdOREB)
			ScPoss = function.ScPoss(FGPart,ASTPart,FTPart,TmOREB,TmScorPoss,TmOREBWgt,TmPlay_pect,OREBPart)
			Stop_perc = function.Stop_perc(Stops,OppMIN,TmPoss,MIN)

			#adding results to dictionary
			#data["PProd"] = PProd
			#data["ScPoss"] = ScPoss
			#data["Stop_perc"] = Stop_perc

			#sixth level calculation
			TotPoss = function.TotPoss(ScPoss,FGmPoss,FTmPoss,TOV)
			DRTG = function.DRTG(TmDRTG,OppPtsPScorPoss,Stop_perc)

			#adding results to dictinory
			#data["TotPoss"] = TotPoss
			#data["DRTG"] = DRTG

			#seventh level calculation
			Individual_Offensize_Rating = function.Individual_Offensize_Rating(PProd, TotPoss)
			Individual_Floor_Percentage = function.Individual_Floor_Percentage(ScPoss,TotPoss)

			#adding results to dictinory
			#data["Individual_Offensize_Rating"] = Individual_Offensize_Rating
			#data["Individual_Floor_Percentage"] = Individual_Floor_Percentage

	return data
