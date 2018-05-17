import numpy
import sys


def TmPoints():
    pass
    """
    Name:total points by team

    """


def OREB_perc():
    pass
    """
    Name:Total Offensive Rebounds Percentage

    """


def TmPoss(TmFGA,TmOREB,oppDREB,TmFTA,TmFGM,TmTOV):
    """
    Name: Total Team Possesion
    Returns: the total team possession based on parameters
    Arguments:
        FGA: field goals attemped
        TmOREB: Team Total Offensive Rebounds (double check)
        oppDREB:  Opponent Total Defensive Rebounds (double check)
        FTA: free throw attemped
        FGM: field goals made


    Depend? No
    check status: Yes
    level: 1
    """
    if(TmOREB+oppDREB) == 0:
        return float(TmFGA*(TmFGA-TmFGM)*1.07+TmTOV + 0.4*TmFTA)
    else:
        return float(TmFGA-(TmOREB/(TmOREB+oppDREB))*(TmFGA-TmFGM)*1.07+TmTOV + 0.4*TmFTA)




def OppPoss(OppFGA,OppOREB,TmDREB,OppFTA,OppFGM,OppTOV):
    """
    Name: Opponent Total Team Possesion
    Returns: the total opponent possession based on parameters
    Arguments:
        OppFGA: opponent field goals attemped
        OppOREB: opponent team Total Offensive Rebounds (double check)
        TmDREB:  Total Defensive Rebounds (double check)
        OppFTA: opponent free throw attemped
        OppFGM: opponent field goals made


    Depend? No
    check status: Yes
    level: 1

    """
    if(OppOREB+TmDREB) == 0:
        return float(OppFGA*(OppFGA-OppFGM)*1.07+OppTOV + 0.4*OppFTA)
    else:
        return float(OppFGA-(OppOREB/(OppOREB+TmDREB))*(OppFGA-OppFGM)*1.07+OppTOV + 0.4*OppFTA)





def TmORTG (TmPoints, TmPoss):
    """
    Name: Team Offensive Rating
    Returns: the team offensice rating based on parameters
    Arguments:
        TmPoints: total points by team
        TmPoss: total team possestion

    Depend? Yes
    check status: Yes
    level: 2
    """
    if TmPoss == 0:
        return 0.0
    return float(100*(TmPoints/TmPoss))



def PProd(PProdFG, PProdAst,FTM,TmOREB,
          TmScorPoss,TmOREBWgt,TmPlay_pect,PProdOREB):
    """
    Name: Individual Points Produced
    Returns: the individual points produced based on parameters
    Arguments:
        PProdFG: points produced FG part
        PProdAst: points produced AST part
        FTM: free throw made
        TmOREB: Team Total Offensive Rebounds(double check)
        TmScorPoss:  Team score poss
        TmOREBWgt: team OREB weight
        TmPlay: team play
        PProdOREB: points produced OREB part

    Depend? Yes
    check status: Yes
    level: 5

    """
    if TmScorPoss == 0:
        return float((PProdFG+PProdAst+FTM)*(1*TmOREBWgt*TmPlay_pect)+PProdOREB)
    else:
        return float((PProdFG+PProdAst+FTM)*(1-(TmOREB/TmScorPoss)
                                         *TmOREBWgt*TmPlay_pect)+PProdOREB)


def PProdFG(FGM,PTS,FTM,FGA,qAST,FGM_3):
    """
    Name: Points Produced Field Goal Part
    Returns: the Points Produced Field Goal Part based on parameters
    Arguments:
        FGM: field goals made
        PTS: points (double check)
        FTM: free throws made
        FGA: field goals attemped
        qAST: q AST
        FGM_3: 3 poitns field goal made

    Depend? Yes
    check status: Yes (different results from excel sheet)
    level: 3
    """
    if FGA == 0:
        return float(2*(FGM+0.5*FGM_3)*1-0.5*0.0*qAST)
    else:
        return float(2*(FGM+0.5*FGM_3)*1-0.5*((PTS-FTM)/(2*FGA))*qAST)




def PProdAst(TmFGM, FGM, Tm3PM, TmPTS, TmFTM, PTS, FGA, AST, FGM_3,FTM, TmFGA):
    """
        Name: Points Produced Assist Part
        Returns: the Points Produced Assist Part based on parameters
        Arguments:
            TmFGM: team field goal made
            FGM: field goal made
            Tm3PM: team 3 points
            TmPTS: team points
            TmFTM: team free throw made
            PTS: points
            FGA: field goal made
            AST: assist
            FGM_3: 3 point shot makes
            FTM: free throw made

        Depend? No
        check status: Yes
        level: 1

        """
    try:
        return float(2*((TmFGM-FGM+0.5*(Tm3PM-FGM_3))/(TmFGM-FGM))*0.5
                 *(((TmPTS-TmFTM)-(PTS-FTM))/(2*(TmFGA-FGA) ))*AST)
    except:
        return 0.0


def PProdOREB(ORB,TmOREBWgt,TmPlay_pect,TmPTS,
              TmFGM,TmFTM,TmFTA):
    """
    Name: Points Produced Total Offensive Rebounds Part
    Returns: the Points Produced Total Offensive Rebounds Part based on parameters
    Arguments:
        ORB: Rebounds
        TmOREBWgt: team OREB weight
        TmPlay: team play
        TmPTS: team points
        TmFGM: team field goal made
        TmFTM: team free throw made
        TmFTA: team free theow attemped

    Depend? Yes
    check status: Yes
    level: 4

    """
    try:
        return float(ORB*TmOREBWgt*TmPlay_pect*(TmPTS/(TmFGM+(1-(1-(TmFTM/TmFTA))**2 )
                                                   *0.4*TmFTA)))
    except:
        return 0.0


def TotPoss(ScPoss,FGmPoss,FTmPoss,TOV):
    """
    Name: Individual Total Possession
    Returns: the Individual Total Possession based on parameters
    Arguments:
        ScPoss: Scoring Possessions
        FGmPoss: Field Goal Missed Possessions
        FTmPoss: Free Throw Missed Possessions
        TOV: trunovers (available since the 1977-78 season in the NBA)

    Depend? Yes
    check status: Yes
    level: 6
    """
    try:
        return float(ScPoss+FGmPoss+FTmPoss+TOV)
    except:
        return 0.0



def ScPoss(FGPart,ASTPart,FTPart,TmOREB,
           TmScorPoss,TmOREBWgt,TmPlay_pect,OREBPart):
    """
    Name: Scoring Possessions
    Returns: the Scoring Possessions based on parameters
    Arguments:
        FGPart: field goal part (double check)
        ASTPart: assist part (double check)
        FTPart: free throw part (double check)
        TmOREB: team Total Offensive Rebounds
        TmScorPoss: team scoring sossessions
        TmOREBWgt: team Total Offensive Rebounds weight
        TmPlay: team play
        OREBPart: Total Offensive Rebounds part

    Depend? Yes
    check status: Yes
    level: 5
    """
    if TmScorPoss == 0:
        return float((FGPart+ASTPart+FTPart)*(1
                                          *TmOREBWgt*TmPlay_pect)+OREBPart)
    else:
        return float((FGPart+ASTPart+FTPart)*(1-(TmOREB/TmScorPoss)
                                          *TmOREBWgt*TmPlay_pect)+OREBPart)




def FGPart(FGM,PTS,FTM,FGA,qAST):
    """
    Name: Field Goal Part
    Returns: the Field Goal Part based on parameters
    Arguments:
        FGM: Fieldgoals made
        PTS: points
        FTM: free throw made
        FGA: field goal made
        qAST: qAST

        Depend? Yes
        check status: Yes
        level: 3

    """
    if FGA == 0:
        return float(FGM*(1-0.5*0.0*qAST))
    else:
        return float(FGM*(1-0.5*((PTS-FTM)/(2*FGA))*qAST))




def qAST(MIN,TmMIN,q_12,q_5):
    """
    Name: percentage of field goals assisted by teammates while
    the player of interest is in the game plus the expected
    rate of assists per field goals made for the player of interest
    Returns: the qAST based on parameters
    Arguments:
        MIN:  MIN
        TmMIN: team MIN

        Depend? Yes
        check status: Yes
        level: 2
    """
    try:
        a1 = (MIN/TmMIN)/5
        return a1*q_5 + ((1-a1)*q_12)
    except:
        return 0.0



def q5(TmAST,AST,TmFGM):
    """
    Name: q5
    Returns: the q5 based on parameters
    Arguments:
        TmAST: team assist
        AST: assist
        TmFGM: team field goal made

        Depend? No
        check status: Yes
        level: 1

    """
    if(TmFGM == 0):
        return float(1.14*0.0)
    else:
        return float(1.14*((TmAST-AST)/TmFGM))




def q12(TmAST,TmMIN,MIN,AST,TmFGM,FGM):
    """
    Name: q12
    Returns: the q12 based on parameters
    Arguments:
        TmAST: team assist
        TmMIN: Team MIN
        MIN: MIN
        AST: assist
        TmFGM: team field goal made
        FGM: field goal made

        Depend? No
        check status: Yes
        level: 1

    """
    if(TmMIN == 0):
        return float (AST/FGM)
    else:
        return float(((TmAST/TmMIN)*MIN*5-AST)/((TmFGM/TmMIN)*MIN*5-FGM))



def ASTPart(TmPTS,TmFTM,PTS,FTM,TmFGA,FGA,AST):
    """
    Name: Assist Part
    Returns: the assist part based on parameters
    Arguments:
        TmPTS: team points
        TmFTM: team free throw made
        PTS: points
        FTM: free throw made
        TmFGA: team field goal attemped
        FGA: field goal attemped
        AST: assist


        Depend? No
        check status: Yes
        level: 1

    """
    if(TmFGA - FGA) == 0:
        return 0.0
    else:
        return 0.5*(((TmPTS-TmFTM)-(PTS-FTM))/(2*(TmFGA-FGA)))*AST



def FTPart(FTM,FTA):
    """
    Name: Free Throw Part
    Returns: the free throw part based on parameters
    Arguments:
        FTM: free throw made
        FTA: free throw attemped

        Depend? No
        check status: Yes
        level: 1

    """
    if FTA == 0:
        return 0.0
    else:
        return float((1-(1-(FTM/FTA))**2 )*0.4*FTA)



def TmScorPoss(TmFGM,TmFTM,TmFTA):
    """
    Name: Team Scoring Possession
    Returns: the Team Scoring Possession based on parameters
    Arguments:
        TmFGM: team field goal made
        TmFTM: team free throw made
        TmFTA: team three throw attemped

        Depend? No
        check status: Yes
        level: 1

    """
    if TmFTA == 0:
        return float(TmFGM+0.0*TmFTA*0.4)
    else:
        return float(TmFGM+(1-(1-(TmFTM/TmFTA))**2)*TmFTA*0.4)



def TmOREBWgt(TmOREB_pect,TmPlay_pect):
    """
    Name: Team Total Offensive Rebounds Weight
    Returns: the Team Total Offensive Rebounds Weight based on parameters
    Arguments:
        TmOREB: team Total Offensive Rebounds
        TmPlay: team play

        Depend? Yes
        check status: Yes
        level: 3

    """
    try:
        return float(((1-TmOREB_pect)*TmPlay_pect)/((1-TmOREB_pect)
                                                *TmPlay_pect+TmOREB_pect*(1-TmPlay_pect)))
    except:
        return 0.0


def TmOREB_pect(TmOREB,OppTREB,OppDREB):
    """
    Name: Team Total Offensive Rebounds Weight Percentage
    Returns: the Team Total Offensive Rebounds Weight Percentage based on parameters
    Arguments:
        TmOREB: team Total Offensive Rebounds
        OppTREB:  Opponent TREB

        Depend? No
        check status: Yes
        level: 1

    """
    try:
        return float(TmOREB/(TmOREB+OppDREB))
    except:
        return 0.0


def TmPlay(TmFGA,TmFTA,TmTOV):
    """
    Name: Team Play
    Returns: the Team Play based on parameters
    Arguments:
        TmFGA: team field goal attemped
        TmFTA: team free throw attemped
        TmTOV: team turnover

        Depend? No
        check status: Yes
        level: 1

    """
    try:
        return float(TmFGA+TmFTA*0.4+TmTOV)
    except:
        return 0.0

def TmPlay_pect(TmScorPoss, TmFGA,TmFTA,TmTOV):
    """
    Name: Team Play percentage
    Returns: the Team Play Percentageg based on parameters
    Arguments:
        TmScorPoss: Team Scoring Possession
        TmFGA: team field goal attemped
        TmFTA: team free throw attemped
        TmTOV: team turnover

        Depend? Yes
        check status: Yes
        level: 2

    """
    try:
        return float(TmScorPoss/(TmFGA+TmFTA*0.4+TmTOV))
    except:
        return 0.0


def OREBPart(OREB,TmOREBWgt,TmPlay_pect):
    """
    Name: Offensive Rebound Part
    Returns: the Offensive Rebound Part based on parameters
    Arguments:
        OREB: Total Offensive Rebounds
        TmOREBWgt: Team Total Offensive Rebounds Weight
        TmPlay_pect: Team Play percentage

        Depend? Yes
        check status: Yes
        level: 4

    """
    try:
        return float(OREB*TmOREBWgt*TmPlay_pect)
    except:
        return 0.0


def FGmPoss(FGA,FGM,TmOREB_pect):
    """
    Name: Field Goal Missed Possessions
    Returns: the Field Goal Missed Possessions based on parameters
    Arguments:
        FGA: field goal attemped
        FGM: field goal made
        TmOREB_pect: Team Total Offensive Rebounds Weight Percentage

        Depend? Yes
        check status: Yes
        level: 2

    """
    try:
        return (FGA-FGM)*(1-1.07*TmOREB_pect)
    except:
        return 0.0


def FTmPoss(FTM,FTA):
    """
    Name: Free Throw Missed Possessions
    Returns: the free throw missed possesssions based on parameters
    Arguments:
        FTM: free throw made
        FTA: free throw attemped

        Depend? No
        check status: Yes
        level: 1

    """
    try:
        return float(((1-(FTM/FTA))**2)*0.4*FTA)
    except:
        return 0.0


def Individual_Offensize_Rating(PProd, TotPoss):
    """
    Name: Individual Offensize Rating
    Returns: the Individual Offensize Rating based on parameters
    Arguments:
        PProd: Individual Points Produced
        TotPoss: Individual Total Possession

        Depend? Yes
        check status: Yes
        level: 7

    """
    try:
        if TotPoss == 0:
            return 0.0
        else:
            return 100*(PProd/TotPoss)
    except:
        return 0.0


def Individual_Floor_Percentage(ScPoss,TotPoss):
    """
    Name: Individual Floor Percentage
    Returns: the Individual Floor Percentage based on parameters
    Arguments:
        ScPoss: Scoring Possessions
        TotPoss: Individual Total Possession

        Depend? Yes
        check status: Yes
        level: 7

    """
    try:
        if TotPoss == 0:
            return 0.0
        else:
            return float(ScPoss/TotPoss)
    except:
        return 0.0


def Team_Floor_Percentage(TmScorPoss, TmPoss):
    """
    Name: Team Floor Percentage
    Returns: the Team Floor Percentage based on parameters
    Arguments:
        ScPoss: Scoring Possessions
        TotPoss: Individual Total Possession

        Depend? Yes
        check status: Yes
        level: 2

    """
    try:
        if TmPoss == 0:
            return 0.0
        else:
            return float(TmScorPoss/TmPoss)
    except:
        return 0.0


def TmDRTG(OppPTS,TmPoss):
    """
    Name: Team Defensive Rating
    Returns: the Team Defensive Rating based on parameters
    Arguments:
        OppPTS: Opponent points
        TmPoss: Total Team Possesion

        Depend? Yes
        check status: Yes
        level: 2

    """
    try:
        if TmPoss == 0:
            return 0.0
        else:
            return float(100*(OppPTS/TmPoss))
    except:
        return 0.0


def DRTG(TmDRTG,OppPtsPScorPoss,Stop_perc):
    """
    Name: Individual Defensive Rating
    Returns: the Individual Defensive Rating based on parameters
    Arguments:
        TmDRTG: Team Defensive Rating
        OppPtsPScorPoss: Opponent Points Per Scoring Possession
        Stop_perc: Stop percentage (double check)

        Depend? Yes
        check status: Yes
        level: 6

    """
    try:
        return float(TmDRTG+0.2*(100*OppPtsPScorPoss*(1-Stop_perc)-TmDRTG))
    except:
        return 0.0



def OppPtsPScorPoss(OppPTS,OppFGM,OppFTM,OppFTA):
    """
    Name: Opponent Points Per Scoring Possession
    Returns: the Opponent Points Per Scoring Possession based on parameters
    Arguments:
        OppPTS: Opponent points
        OppFGM: Opponent field goal made
        OppFTM: Opponent free throw made
        OppFTA: Opponent free throw attemped

        Depend? No
        check status: Yes
        level: 1

    """
    try:
        return float(OppPTS/(OppFGM+(1-(1-(OppFTM/OppFTA))**2 )*OppFTA*0.4))
    except:
        return 0.0


def Stop_perc(Stops,OppMIN,TmPoss,MIN):
    """
    Name: Stop Percentage
    Returns: the stop percentage based on parameters
    Arguments:
        Stops: Stops
        OppMIN: Opponenet MIN
        TmPoss: Total Team Possesion
        MIN: MIN

        Depend? Yes
        check status: Yes (answers are different from excel sheet)
        level: 5

    """
    try:
        if(TmPoss*MIN == 0):
            return 0.0;
        else:
            return float((Stops*OppMIN)/(TmPoss*MIN))
    except:
        return 0.0


def Stops(Stops_1,Stops_2):
    """
    Name: Stops
    Returns: the Stops based on parameters
    Arguments:
        Stops_1: stop 1
        Stops_2: stop 2

        Depend? Yes
        check status: Yes (different results from excel)
        level: 4

    """
    try:
        return float(Stops_1+Stops_2)
    except:
        return 0.0


def Stops_1(STL,BLK,FMwt,DOREB_perc,DREB):
    """
    Name: Stops_1 (double check)
    Returns: the Stops_1 based on parameters
    Arguments:
        STL: Total steals
        BLK: Total blocks
        FMwt: FMwt
        DOREB_perc: Total Defensive Rebounds Percentage (double check)
        DREB: Total defensive rebounds

        Depend? Yes
        check status: Yes
        level: 3

    """
    try:
        return float(STL+BLK*FMwt*(1-1.07*DOREB_perc)+DREB*(1-FMwt))
    except:
        return 0.0


def FMwt(DFG_perc,DOREB_perc):
    """
    Name: FMwt
    Returns: the FMwt based on parameters
    Arguments:
        DFG_perc: deffensive rate percentage
        DOREB_perc: Total Defensive Rebounds Percentage (double check)

        Depend? Yes
        check status: Yes
        level: 2

    """
    try:
        return float((DFG_perc*(1-DOREB_perc))/(DFG_perc
                                            *(1-DOREB_perc)+(1-DFG_perc)*DOREB_perc))
    except:
        return 0.0


def DOREB_perc(OppOREB,TmDREB):
    """
    Name: Total Defensive Rebounds Percentage
    Returns: the Total Defensive Rebounds Percentage based on parameters
    Arguments:
        OppOREB: Opponent Total offensive rebounds
        TmDREB: Team Total defensive rebounds

        Depend? No
        check status: Yes
        level: 1


    """
    try:
        return float(OppOREB/(OppOREB+TmDREB))
    except:
        return 0.0


def DFG_perc(OppFGM,OppFGA):
    """
    Name: Defensive percentage
    Returns: the Defensive percentage based on parameters
    Arguments:
        OppFGM: Opponent field goal made
        OppFGA: Opponent field goal attemped

        Depend? No
        check status: Yes
        level: 1

    """
    try:
        if OppFGA == 0:
            return 0.0
        else:
            return float(OppFGM/OppFGA)
    except:
        return 0.0


def Stops_2(OppFGA,OppFGM,TmBLK,TmMIN,FMwt,DOREB_perc
            ,OppTOV,TmSTL,MIN,PF,TmPF,OppFTA,OppFTM):
    """
    Name: Stops 2
    Returns: the Stops 2 based on parameters
    Arguments:
        OppFGA: Opponent field goal attemped
        OppFGM: Opponent field goal made
        TmBLK: Team total blocks
        TmMIN: Team MIN
        FMwt: FMwt
        DOREB_perc: Total Defensive Rebounds Percentage (double check)
        OppTOV: Opponent turnover
        TmSTL: Team total steals
        MIN: MIN
        PF: total personal fouls
        TmPF: total team fouls
        OppFTA: Opponent free throw attemped
        OppFTM: Opponent free throw made

        Depend? Yes
        check status: Yes
        level: 3

    """
    try:
        return  float((((OppFGA-OppFGM-TmBLK)/TmMIN)*FMwt*(1-1.07*DOREB_perc)
                   +((OppTOV-TmSTL)/TmMIN))*MIN+(PF/TmPF)
                  *0.4*OppFTA*(1-(OppFTM/OppFTA))**2)
    except:
        return 0.0


def eFG_perc(FGM,FGA,FGM_3):
    """
    Name: effective fieldgoal percentage
    Returns: the effective fieldgoal percentage based on parameters
    Arguments:
        FGM: Fieldgoals made
        FGA: Fieldgoals attempted
        FGM_3: 3 point shot makes

        Depend? No
        check status: Yes
        level: 1

    """
    try:
        return (FGM+0.5*FGM_3)/FGA
    except:
        return 0.0


def Turnover_perc(TOV,FGA,FTA):
    """
        Name: Trunovers percentage
        Returns: the trunovers percentage based on parameters
        Arguments:
            TOV: trunovers (available since the 1977-78 season in the NBA)
            FGA: field goals attemped
            FTA: free throws attemped

        Depend? No
        check status: Yes
        level: 1

        """
    try:
        return float(TOV/(FGA+0.4*FTA+TOV))
    except:
        return 0.0


def FTr(FTA,FGA):
    """
    Name: Free Throw Rate
    Returns: the free throw rate based on parameters
    Arguments:
        FTA: free throws attemped
        FGA: free goals attemped


    Depend? No
    check status: Yes
    level: 1

    """
    try:
        if FGA == 0:
            return 0.0
        else:
            return FTA/FGA
    except:
        return 0.0


def FG_2_perc(FGM_2,FGA_2):
    """
    Name: 2FG Percentage
    Returns: the 2FG percentage based on parameters
    Arguments:
        FGM_2: two-points field goals made
        FGA_2: two-points field goals attemped

    Depend? No
    check status: Yes
    level: 1
    """
    try:
        if FGA_2 == 0:
            return 0.0
        else:
            return FGM_2/FGA_2
    except:
        return 0.0

def FG_3_perc(FGM_3,FGA_3):
    """
    Name: 3FG Percentage
    Returns: the 3FG percentage based on parameters
    Arguments:
        FGM_3: three-points field goals made
        FGA_3: three-points field goals attemped

    Depend? No
    check status: Yes
    level: 1

    """
    try:
        if FGA_3 == 0:
            return 0.0
        else:
            return FGM_3/FGA_3
    except:
        return 0.0


def FGr_2(FGA_2,FGA):
    """
    Name: 2FG Rate (FG%)
    Returns: the 2FG rate based on parameters
    Arguments:
        FGA_2: two-points field goals attemped
        FGA: field goal attempted

    Depend? No
    check status: Yes
    level: 1

    """
    try:
        if FGA == 0:
            return 0.0
        else:
            return float(FGA_2/FGA)
    except:
        return 0.0


def FGr_3(FGA_3,FGA):
    """
    Name: 3FG Rate (3P%)
    Returns: the 3FG rate based on parameters
    Arguments:
        FGA_3: three-points field goals attemped
        FGA: field goal attempted

    Depend? No
    check status: Yes
    level: 1

    """
    try:
        if FGA == 0:
            return 0.0
        else:
            return float(FGA_3/FGA)
    except:
        return 0.0



def Usage_Rate(FGA,FTA,TOV,TmMIN,MIN,TmFGA,TmFTA,TmTOV):
    """
    Name: Usage Rate
    Returns: the usage rate based on parameters
    Arguments:
        FGA: field goal attemped
        FTA: free throw attemped
        TOV: turnover
        TmMIN: Team MIN
        MIN: MIN
        TmFGA: team field goal attemped
        TmFTA: team free throw attemped
        TmTOV: team turnover

    Depend? No
    check status: Yes
    level: 1

    """
    try:
        return float(100*((FGA+0.4*FTA+TOV)*(TmMIN/5))/(MIN*(TmFGA+0.4*TmFTA+TmTOV)))
    except:
        return 0.0


def AST_perc(AST,MIN,TmMIN,TmFGM,FGM):
    """
    Name: Assist Percentage (Individual)
    Returns: the Assist Percentage based on parameters
    Arguments:
        AST: assist
        MIN: minutes
        TmMIN: team minutes
        TmFGM: team field goal made
        FGM: field goal made

    Depend? No
    check status: Yes (cannot find in excel, used NBA data)
    level: 1

    """
    try:
        return float(100*AST/(((MIN/(TmMIN/5))*TmFGM)-FGM))
    except:
        return 0.0


def ASTr(AST,FGM):
    '''
        Name: Assists Rate
        Returns: the assists rate based on parameters
        Arguments:
            AST: assists
            FGM: filed goals made

        Depend? No
        check status: Yes (cannot find in excel)
        level: 1

    '''
    try:
        if FGM == 0:
            return 0.0
        else:
            return float(AST/FGM)
    except:
        return 0.0



def AST_Ratio(AST,FGA,FTA,TOV):
    """
    Name: Assists Ratio
    Returns: the assists ratio based on parameters
    Arguments:
        AST: assists
        FGA: filed goals attemped
        FTA: free throws attemped
        TOV: trunovers (available since the 1977-78 season in the NBA)

    Depend? No
    check status: Yes(cannot find in excel)
    level: 1

    """
    try:
        return float((100*AST)/(FGA+(FTA*0.4)+AST+TOV))
    except:
        return 0.0


def TS_perc(PTS,FGA,FTA):
    """
    Name: True Shooting percentage
    Returns: the True Shooting percentage based on parameters
    Arguments:
        PTS: points
        FGA: filed goals attemped
        FTA: free throws attemped

    Depend? No
    check status: Yes
    level: 1

    """
    try:
        return float(PTS/(2*(FGA+0.4*FTA)))
    except:
        return 0.0


def Total_REB_pect (TREB,TmMIN,MIN,TmTREB,OppTREB):
    """
    Name: Total rebound percentage
    Returns: the Total Total rebound percentage based on parameters
    Arguments:
        TREB: personal total recound
        TmMIN: team MIN
        MIN: MIN
        TmTREB:  team TREB
        OppTREB:  Opponent TREB(check! team or individual)

    Depend? No
    check status: Yes (cannot find in excel, used NBA data to test)
    level: 1

    """
    try:
        return 100*(TREB*(TmMIN/5))/(MIN*(TmTREB+OppTREB))
    except:
        return 0.0



def STL_perc(STL,TmMIN,MIN,OppPoss):
    """
    Name: Total Steals Percentage (Individual)
    Returns: the Total Steals Percentage based on parameters
    Arguments:
        STL: Total steals (check! team or individual)
        TmMIN: team MIN
        MIN: MIN
        OppPoss: Opponent Possesion

    Depend? Yes
    check status: Yes (cannot find in excel, used NBA data to test)
    level: 2

    """
    try:
        return float(100*(STL*(TmMIN/5))/(MIN*OppPoss))
    except:
        return 0.0


def BLK_perc(BLK,TmMIN,MIN,OppFGA,Opp3PA):
    """
    Name: Total Blocks Percentage
    Returns: the Total blocks Percentage based on parameters
    Arguments:
        BLK: Total blocks (check! team or individual)
        TmMIN: Team MIN
        MIN:  MIN
        OppFGA: Opponent field goal attemped
        Opp3PA: Opponent 3 points

    Depend? No
    check status: Yes (cannot find in excel, used NBA data to test)
    level: 1

    """
    try:
        return float(100*(BLK*(TmMIN/5))/(MIN*(OppFGA-Opp3PA)))
    except:
        return 0.0



def Game_Score(PTS,FGM,FGA,FTA,FTM,ORE,DREB,STL,AST,BLK,PF,TOV):
    '''
        Name: Game Score (individual)
        Returns: the game score based on parameters
        Arguments:
            PTS: Points
            FGM: field goal made
            FGA: field goal attemped
            FTA: free throw attemped
            FTM: free throw made
            ORE: Offensive Rebounds
            DREB: Total Offensive Rebounds
            STL: total steals
            AST: assist
            BLK: total blocks
            PF: total personal fouls
            TOV: turnover

        Depend? No
        check status: Yes (cannot find in excel sheet)
        level: 1

    '''
    try:
        return float(PTS+0.4*FGM-0.7*FGA-0.4
                 *(FTA-FTM)+0.7*ORE-0.3*DREB+STL
                 +0.7*AST+0.7*BLK-0.4*PF-TOV)
    except:
        return 0.0



def Pace(TmPoss,OppPoss,TmMIN):
    """
    Name: Pace
    Returns: the pace based on parameters
    Arguments:
        TmPoss: Total Team Possesion
        OppPoss: Opponent Possesion (check!) need calculation??-> use the same calculations as TmPoss
        TmMIN: team MIN


    Depend? Yes
    check status: Yes(cannot find in excel)
    level: 2

    """
    try:
        return float(40*((TmPoss+OppPoss)/(2*(TmMIN/5))))
    except:
        return 0.0


def PIE(PTS,FGM,FTM,FGA,FTA,DREB,OREB,AST,STL,BLK
        ,PF,TO,GmPTS,GmFGM,GmFTM,GmFGA,GmFTA,GmDREB
        ,GmOREB,GmAST,GmSTL,GmBLK,GmPF,GmTO):
    """
    Name: Player Impact Rate
    Returns: the Player Impact Rate based on parameters
    Arguments:
        PTS: points
        FGM: field goal made
        FTM: free throw made
        FGA: field goal attemped
        FTA: free throw attemped
        DREB: Total defensive rebounds
        OREB: Total offensive rebounds
        AST: assist
        STL: total steals
        BLK: total blocks
        PF: total personal fouls
        TO: total turnovers
        GmPTS: game points
        GmFGM: game field goal made
        GmFTM: game free throw made
        GmFGA: game field goal attemped
        GmFTA: game free throw attemped
        GmDREB: game Total defensive rebounds
        GmOREB: game Total offensive rebounds
        GmAST: game assist
        GmSTL: game total steals
        GmBLK: game total blocks
        GmPF: game total personal fouls
        GmTO: game total turnover

    Depend? No
    check status: No
    level: 1

    """
    try:
        return (PTS+FGM+FTM-FGA-FTA+DREB+(0.5*OREB)+AST+STL
            +(0.5*BLK)-PF-TO)/(GmPTS+GmFGM+GmFTM-GmFGA
                               -GmFTA+GmDREB+(0.5*GmOREB)+GmAST+GmSTL+(0.5*GmBLK)-GmPF-GmTO)
    except:
        return 0.0
