#!/bin/bash
from os import system

import sys, getopt

from MITM_MILP_Whirlpool import * 

TWO_RULES = 0
KS_GUESS = 0
GUESS_BOTH = 0

class DrawDistinguisher():
    def __init__(self, solutionFile, TR, ini_r, ini_k, mat_r):
        print('in init()')
        solFile = open(solutionFile,'r')
        self.TR = TR
        self.ini_r = ini_r
        self.ini_k = ini_k
        self.mat_r = mat_r
        self.var_value_map = dict()
        for line in solFile:
            if line[0] != '#':
                temp = line
                #temp = temp.replace('-', ' ')
                temp = temp.split()
                self.var_value_map[temp[0]] = round(float(temp[1]))

    def draw(self,outputfile):
        A = Constraints_generator_(self.TR, self.ini_r, self.ini_k, self.mat_r)
        Solution = self.var_value_map
        fid = open(outputfile,'w')
        fid.write(
            '\\documentclass{standalone}' + '\n'
            '\\usepackage[usenames,dvipsnames]{xcolor}' + '\n'
            '\\usepackage{amsmath,amssymb,mathtools}' + '\n'
            '\\usepackage{tikz,calc,pgffor}' + '\n'
            '\\usepackage{xspace}' + '\n'
            '\\usetikzlibrary{crypto.symbols,patterns,calc}' + '\n'
            '\\tikzset{shadows=no}' + '\n'
            '\\input{macro}' + '\n')
        fid.write('\n\n')
        fid.write(
            '\\begin{document}' + '\n' +
            '\\begin{tikzpicture}[scale=0.2, every node/.style={font=\\boldmath\\bf}]' + '\n'
	        '\\everymath{\\scriptstyle}' + '\n'
	        '\\tikzset{edge/.style=->, >=stealth, arrow head=8pt, thick};' + '\n')
        fid.write('\n\n')

        RED = [0, 1]
        BLUE = [1, 0]
        GRAY = [1, 1]
        WHITE = [0, 0]
        #RULES = ['XOR-MC', 'MC,XOR', 'XOR,MC']
        RULES = ['MC-AK', 'AK-MC']

        Deg1 = 'GDeg1'
        Deg2 = 'GDeg2'
        GM = 'GMat'
        HO = RowN + RowN + RowN//2 #RowN + RowN + RowN
        WO = ColN #ColN

        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()

        d1_key = Vars_generator.genVars_degree_forward_key()
        d2_key = Vars_generator.genVars_degree_backward_key()

        guessBL = 0;
        guessRD = 0;
        guessBR = 0;

        forward_rounds = []
        backward_rounds = []
        if self.mat_r < self.ini_r:
            forward_rounds = list(range(self.ini_r, self.TR)) + list(range(0, self.mat_r))
            backward_rounds = list(range(self.mat_r + 1, self.ini_r))
        else:
            forward_rounds = list(range(self.ini_r, self.mat_r))
            backward_rounds = list(range(self.mat_r + 1, self.TR)) + list(range(0, self.ini_r))

        ini_d1 = 0
        ini_d2 = 0
        for g in range(MatN):
            ini_d1 = ini_d1 + Solution[d1[g]]
            ini_d2 = ini_d2 + Solution[d2[g]]
        ini_d1_key = 0
        ini_d2_key = 0
        for g in range(KeyCellN):
            ini_d1_key = ini_d1_key + Solution[d1_key[g]]
            ini_d2_key = ini_d2_key + Solution[d2_key[g]]

        for r in range(0, self.TR):
            input1_round = Vars_generator.genVars_O_SB(r, 1)
            input2_round = Vars_generator.genVars_O_SB(r, 2)

            input1_mix = Vars_generator.genVars_I_MC(r, 1)
            input2_mix = Vars_generator.genVars_I_MC(r, 2)

            SK1_mix = Vars_generator.genVars_SK_I_MC(r, 1)
            SK2_mix = Vars_generator.genVars_SK_I_MC(r, 2)

            I_MC_SupP_Blue_1 = Vars_generator.genVars_I_MCAK_SupP_Blue(r, 1)
            I_MC_SupP_Blue_2 = Vars_generator.genVars_I_MCAK_SupP_Blue(r, 2)
            I_MC_SupP_Red__1 = Vars_generator.genVars_I_MCAK_SupP_Red_(r, 1)
            I_MC_SupP_Red__2 = Vars_generator.genVars_I_MCAK_SupP_Red_(r, 2)
            M_MC_SupP_Blue_1 = Vars_generator.genVars_M_MCAK_SupP_Blue(r, 1)
            M_MC_SupP_Blue_2 = Vars_generator.genVars_M_MCAK_SupP_Blue(r, 2)
            M_MC_SupP_Red__1 = Vars_generator.genVars_M_MCAK_SupP_Red_(r, 1)
            M_MC_SupP_Red__2 = Vars_generator.genVars_M_MCAK_SupP_Red_(r, 2)
            O_MC_SupP_Blue_1 = Vars_generator.genVars_O_MCAK_SupP_Blue(r, 1)
            O_MC_SupP_Blue_2 = Vars_generator.genVars_O_MCAK_SupP_Blue(r, 2)
            O_MC_SupP_Red__1 = Vars_generator.genVars_O_MCAK_SupP_Red_(r, 1)
            O_MC_SupP_Red__2 = Vars_generator.genVars_O_MCAK_SupP_Red_(r, 2)

            SK1 = Vars_generator.genVars_SK_O_SB(r + 1, 1)
            SK2 = Vars_generator.genVars_SK_O_SB(r + 1, 2)

            SK_I_MC_SupP_Blue_1           = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 1)
            SK_I_MC_SupP_Blue_2           = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 2)
            SK_I_MC_SupP_Red__1           = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 1)
            SK_I_MC_SupP_Red__2           = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 2)
            SK_SupP_Blue_1                = Vars_generator.genVars_SK_SupP_Blue(r, 1)
            SK_SupP_Blue_2                = Vars_generator.genVars_SK_SupP_Blue(r, 2)
            SK_SupP_Red__1                = Vars_generator.genVars_SK_SupP_Red_(r, 1)
            SK_SupP_Red__2                = Vars_generator.genVars_SK_SupP_Red_(r, 2)
            SK_isWhite                = Vars_generator.genVars_SK_isWhite(r)

            GCDeg_MC_Blue = Vars_generator.genVars_MC_ConsumedDeg_Blue(r)
            GCDeg_MC_Red_ = Vars_generator.genVars_MC_ConsumedDeg_Red_(r)

            CDeg_ARK_Blue     = Vars_generator.genVars_AK_ConsumedDeg_Blue(r)
            CDeg_ARK_Red_     = Vars_generator.genVars_AK_ConsumedDeg_Red_(r)

            KS_MC_GuessBlue = Vars_generator.genVars_SK_GuessBlue(r)
            KS_MC_GuessRed_ = Vars_generator.genVars_SK_GuessRed_(r)
            KS_MC_GuessBoth = Vars_generator.genVars_SK_GuessBoth(r)
            SK_G_CD_MC_Blue = Vars_generator.genVars_SK_MC_ConsumedDeg_Blue(r)
            SK_G_CD_MC_Red_ = Vars_generator.genVars_SK_MC_ConsumedDeg_Red_(r)

            MC_GuessBlue      = Vars_generator.genVars_Enc_GuessBlue(r)
            MC_GuessRed_      = Vars_generator.genVars_Enc_GuessRed_(r)
            MC_GuessBoth      = Vars_generator.genVars_Enc_GuessBoth(r)

            AK_MC_Rule        = Vars_generator.genVars_AK_MC_Rule(r)

            if r < self.TR - 1:
                next_r = r + 1
            else: # the last round, next round the 0
                next_r = 0
            I_SB_next_r_1       = Vars_generator.genVars_O_SB(next_r, 1)
            I_SB_next_r_2       = Vars_generator.genVars_O_SB(next_r, 2)

            if True:
                O = 0
                ## SB
                fid.write('\\begin{scope}[yshift =' + str(- r * (RowN + HO) + RowN - RowN//4)+' cm, xshift =' + str(O * (ColN + WO))+' cm]'+'\n')
                for g in range(MatN):
                    row = (RowN - 1) - g//ColN
                    col = g % ColN
                    cell = [Solution[input1_round[g]], Solution[input2_round[g]]]
                    if cell == RED:
                        fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == BLUE:
                        fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == GRAY:
                        fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    else:
                        fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                if r == 0:
                    fid.write('\\coordinate (firstl) at ('+str(0)+','+str(RowN//2)+');' + '\n')
                fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                for i in range(1, RowN):
                    fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                for i in range(1, ColN):
                    fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize$\\SB^' + str(r) + '$};'+'\n')
    
                if self.mat_r < self.ini_r:  ###   -1 -f- 0 -f- mat_r -b- ini_r -f- TR
                    if r <= self.mat_r or (r >= self.ini_r): ## f
                        fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[above] {\\tiny SB} node[below] {\\tiny SR} +(' + str(WO) + ',' + '0);' + '\n')
                    else:
                        fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[above] {\\tiny SB} node[below] {\\tiny SR} +(' + str(WO) + ',' + '0);' + '\n')
                if self.mat_r > self.ini_r:  ###   -1 -b- 0 -b- ini_r -f- mat_r -b- TR
                    if r >= self.ini_r and r <= self.mat_r: ## f
                        fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[above] {\\tiny SB} node[below] {\\tiny SR} +(' + str(WO) + ',' + '0);' + '\n')
                    else:
                        fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[above] {\\tiny SB} node[below] {\\tiny SR} +(' + str(WO) + ',' + '0);' + '\n')
    
                if r == self.ini_r:
                    fid.write('\\path (' + str(ColN//2) + ',' + str(-0.8) + ') node {\\scriptsize$(+' + str(ini_d1) + '~\\DoFF,~+' + str(ini_d2) + '~\\DoFB)$};'+'\n')
                    fid.write('\\path (' + str(-2) + ',' + str(0.8) + ') node {\\scriptsize$\\StENC$};'+'\n')
    
                fid.write('\n'+'\\end{scope}'+'\n')
                fid.write('\n\n')

                O = O + 1
                ## MC
                fid.write('\\begin{scope}[yshift =' + str(- r * (RowN + HO) + RowN - RowN//4)+' cm, xshift =' + str(O * (ColN + WO))+' cm]'+'\n')
                for g in range(MatN):
                    row = (RowN - 1) - g//ColN
                    col = g % ColN
                    cell = [Solution[input1_mix[g]], Solution[input2_mix[g]]]
                    if cell == RED:
                        fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == BLUE:
                        fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == GRAY:
                        fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    else:
                        fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
    
                fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                for i in range(1, RowN):
                    fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                for i in range(1, ColN):
                    fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize$\MC^' + str(r) + '$};'+'\n')

                if r == self.mat_r:
                    if r == self.TR -1:
                        fid.write('\\draw[edge, -] (' + str(ColN) + ',' + str(ColN//2) + ') -- +(' + str(WO) + ',' + '0) node[fill=white, label={east:{\\tiny Match}}] (xor) {\\tiny MC};' + '\n')
                        fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') --  (xor);' + '\n')
                        #if r != self.TR - 1:
                        #    fid.write('\\draw[edge, ->] (' + str(ColN + WO) + ',' + str(RowN//2) + ') --  (xor);' + '\n')
                        fid.write('\\coordinate (xorb) at (xor.north);' + '\n')
                        fid.write('\\coordinate (xorr) at (xor.south);' + '\n')
                    else:
                        fid.write('\\draw[edge, -] (' + str(ColN) + ',' + str(ColN//2) + ') -- +(' + str(WO) + ',' + '0) node[fill=white, label= {north east:{\\tiny Match}}, fill=white] (xor) {\\tiny MC};' + '\n')
                        fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') --  (xor.west);' + '\n')
                        #if r != self.TR - 1:
                        #    fid.write('\\draw[edge, ->] (' + str(ColN + WO) + ',' + str(RowN//2) + ') --  (xor);' + '\n')
                        fid.write('\\coordinate (xorb) at (xor.north);' + '\n')
                        fid.write('\\coordinate (xorr) at (xor.south);' + '\n')
                    fid.write('\\path (' + str(ColN) + ',' + str(-0.8) + ') node {\\scriptsize Match $+' + str(Solution[GM]) + '~\\DoM$};' + '\n')
                    fid.write('\\path (' + str(-2) + ',' + str(-0.8) + ') node {\\scriptsize$\\EndFwd$};' + '\n')
                else:
                    CD_Blue_r = 0
                    CD_Red__r = 0
                    CD_Blue_KAD_r = 0
                    CD_Red__KAD_r = 0
                    for g in range(ColN):
                        CD_Blue_r = CD_Blue_r + Solution[GCDeg_MC_Blue[g]]
                        CD_Red__r = CD_Red__r + Solution[GCDeg_MC_Red_[g]]
                    for g in range(MatN):
                        CD_Blue_KAD_r = CD_Blue_KAD_r + Solution[CDeg_ARK_Blue[g]]
                        CD_Red__KAD_r = CD_Red__KAD_r + Solution[CDeg_ARK_Red_[g]]
                    fid.write('\\path (' + str((0*(ColN + WO) + WO//4)) + ',' + str(-2) + ') node {\\scriptsize$\\MCRULE (-' + str(CD_Blue_r) + '~\\DoFF,-' + str(CD_Red__r) + '~\\DoFB)$};'+'\n')
                    fid.write('\\path (' + str((0*(ColN + WO) + WO//4)-0.2) + ',' + str(-3.5) + ') node {\\scriptsize$\\XORRULE (-' + str(CD_Blue_KAD_r) + '~\\DoFF,-' + str(CD_Red__KAD_r) + '~\\DoFB)$};'+'\n')
                    rules = ''
                    if TWO_RULES == 0 or TWO_RULES == 2:
                        for g in range(ColN):
                            rules = rules + RULES[Solution[AK_MC_Rule[g]]] + ' '
                        rules = rules[0:-1]
                    else:
                        rules = rules + RULES[Solution[AK_MC_Rule[0]]]
                    #fid.write('\\path (' + str(2*(ColN + WO) + WO//2) + ',' + str(-RowN - 1.5) + ') node {\\tiny (' + rules + ')};'+'\n')

                fid.write('\n'+'\\end{scope}'+'\n')
                fid.write('\n\n')

                O = O + 1
                ## I_MC_SupP_
                fid.write('\\begin{scope}[yshift =' + str(- r * (RowN + HO))+' cm, xshift =' + str(O * (ColN + WO) + WO//2)+' cm]'+'\n')
                if r != self.mat_r:
                    fid.write('\\begin{scope}[yshift =' + str(+ RowN + 2)+' cm, xshift =' +str(0)+' cm]'+'\n')
                    for g in range(MatN):
                        row = (RowN - 1) - g//ColN
                        col = g % ColN
                        if ((r in forward_rounds) and (Solution[AK_MC_Rule[col]] == 1))  or ((r in backward_rounds) and (Solution[AK_MC_Rule[col]] == 0)):
                            cell = [Solution[M_MC_SupP_Blue_1[g]], Solution[M_MC_SupP_Blue_2[g]]]
                        if ((r in forward_rounds) and (Solution[AK_MC_Rule[col]] == 0))  or ((r in backward_rounds) and (Solution[AK_MC_Rule[col]] == 1)):
                            cell = [Solution[I_MC_SupP_Blue_1[g]], Solution[I_MC_SupP_Blue_2[g]]]
                        if cell == RED:
                            fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == BLUE:
                            fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == GRAY:
                            fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        else:
                            fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize$\MCBL^' + str(r) + '$};'+'\n')
                    for i in range(1, RowN):
                        fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                    for i in range(1, ColN):
                        fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize };'+'\n')
                    if r != self.mat_r and self.mat_r < self.ini_r:  ###   -1 -f- 0 -f- mat_r -b- ini_r -f- TR
                        fid.write('\\node[XOR,scale=0.6,label={below:{\\tiny $\AKMC$}}] (xormckb) at (' + str(-WO//2) + ',' + str(RowN//2) + ') {};' + '\n')
                        if r < self.mat_r or (r >= self.ini_r): ## f
                            fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[below] {\\tiny MC} +(' + str(WO) + ',' + '0);' + '\n')
                        else:
                            fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[below] {\\tiny MC} +(' + str(WO) + ',' + '0);' + '\n')
                    if r != self.mat_r and self.mat_r > self.ini_r:  ###   -1 -b- 0 -b- ini_r -f- mat_r -b- TR
                        fid.write('\\node[XOR,scale=0.6,label={below:{\\tiny $\AKMC$}}] (xormckb) at (' + str(-WO//2) + ',' + str(RowN//2) + ') {};' + '\n')
                        if r >= self.ini_r and r < self.mat_r: ## f
                            fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[below] {\\tiny MC} +(' + str(WO) + ',' + '0);' + '\n')
                        else:
                            fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[below] {\\tiny MC} +(' + str(WO) + ',' + '0);' + '\n')
                    fid.write('\n'+'\\end{scope}'+'\n')
                    fid.write('\n\n')

                    for g in range(MatN):
                        row = (RowN - 1) - g//ColN
                        col = g % ColN
                        if ((r in forward_rounds) and (Solution[AK_MC_Rule[col]] == 1))  or ((r in backward_rounds) and (Solution[AK_MC_Rule[col]] == 0)):
                            cell = [Solution[M_MC_SupP_Red__1[g]], Solution[M_MC_SupP_Red__2[g]]]
                        if ((r in forward_rounds) and (Solution[AK_MC_Rule[col]] == 0))  or ((r in backward_rounds) and (Solution[AK_MC_Rule[col]] == 1)):
                            cell = [Solution[I_MC_SupP_Red__1[g]], Solution[I_MC_SupP_Red__2[g]]]
                        if cell == RED:
                            fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == BLUE:
                            fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == GRAY:
                            fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        else:
                            fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\\path (' + str(ColN//2) + ',' + str(0 - 0.8) + ') node {\\scriptsize$\MCRD^' + str(r) + '$};'+'\n')
                    for i in range(1, RowN):
                        fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                    for i in range(1, ColN):
                        fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize };'+'\n')
                    if r != self.mat_r and self.mat_r < self.ini_r:  ###   -1 -f- 0 -f- mat_r -b- ini_r -f- TR
                        fid.write('\\node[XOR,scale=0.6,label={above:{\\tiny $\AKMC$}}] (xormckr) at (' + str(-WO//2) + ',' + str(RowN//2) + ') {};' + '\n')
                        if r < self.mat_r or (r >= self.ini_r): ## f
                            fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[above] {\\tiny MC} +(' + str(WO) + ',' + '0);' + '\n')
                            fid.write('\\draw[edge,  <-] (' + str(0) + ',' + str(RowN//2 + RowN + 2) + ') -- ++(' + str(-WO) + ', 0) -- ++(' + str(-0) + ', '+ str(-(RowN + 2)//2) + ');' + '\n')
                            fid.write('\\draw[edge,  <-] (' + str(0) + ',' + str(RowN//2) + ') -- ++(' + str(-WO) + ', 0) -- ++(' + str(-0) + ', '+ str(+(RowN + 2)//2) + ') -- ++(' + str(-WO//2) + ', '+ str(+0) + ');' + '\n')
                        else:
                            fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[above] {\\tiny MC} +(' + str(WO) + ',' + '0);' + '\n')
                            fid.write('\\draw[edge,  -] (' + str(0) + ',' + str(RowN//2 + RowN + 2) + ') -- ++(' + str(-WO) + ', 0) -- ++(' + str(-0) + ', '+ str(-(RowN + 2)//2) + ');' + '\n')
                            fid.write('\\draw[edge,  ->] (' + str(0) + ',' + str(RowN//2) + ') -- ++(' + str(-WO) + ', 0) -- ++(' + str(-0) + ', '+ str(+(RowN + 2)//2) + ') -- ++(' + str(-WO//2) + ', '+ str(+0) + ');' + '\n')
                    if r != self.mat_r and self.mat_r > self.ini_r:  ###   -1 -b- 0 -b- ini_r -f- mat_r -b- TR
                        fid.write('\\node[XOR,scale=0.6,label={above:{\\tiny $\AKMC$}}] (xormckr) at (' + str(-WO//2) + ',' + str(RowN//2) + ') {};' + '\n')
                        if r >= self.ini_r and r < self.mat_r: ## f
                            fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[above] {\\tiny MC} +(' + str(WO) + ',' + '0);' + '\n')
                            fid.write('\\draw[edge,  <-] (' + str(0) + ',' + str(RowN//2 + RowN + 2) + ') -- ++(' + str(-WO) + ', 0) -- ++(' + str(-0) + ', '+ str(-(RowN + 2)//2) + ');' + '\n')
                            fid.write('\\draw[edge,  <-] (' + str(0) + ',' + str(RowN//2) + ') -- ++(' + str(-WO) + ', 0) -- ++(' + str(-0) + ', '+ str(+(RowN + 2)//2) + ') -- ++(' + str(-WO//2) + ', '+ str(+0) + ');' + '\n')
                        else:
                            fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- node[above] {\\tiny MC} +(' + str(WO) + ',' + '0);' + '\n')
                            fid.write('\\draw[edge,  -] (' + str(0) + ',' + str(RowN//2 + RowN + 2) + ') -- ++(' + str(-WO) + ', 0) -- ++(' + str(-0) + ', '+ str(-(RowN + 2)//2) + ');' + '\n')
                            fid.write('\\draw[edge,  ->] (' + str(0) + ',' + str(RowN//2) + ') -- ++(' + str(-WO) + ', 0) -- ++(' + str(-0) + ', '+ str(+(RowN + 2)//2) + ') -- ++(' + str(-WO//2) + ', '+ str(+0) + ');' + '\n')
                else:
                    if r == self.TR - 1:
                        ys = 0
                        xs = ColN + WO
                    else:
                        ys = (3*RowN)//4
                        xs = ColN + WO #0
                    fid.write('\\begin{scope}[yshift =' + str(ys)+' cm, xshift =' +str(xs)+' cm]'+'\n')
                    for g in range(MatN):
                        row = (RowN - 1) - g//ColN
                        col = g % ColN
                        cell = [Solution[I_SB_next_r_1[g]], Solution[I_SB_next_r_2[g]]]
                        if cell == RED:
                            fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == BLUE:
                            fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == GRAY:
                            fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        else:
                            fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                    for i in range(1, RowN):
                        fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                    for i in range(1, ColN):
                        fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize$\SB^' + str(next_r) + '$};'+'\n')
                    if r == self.TR - 1:
                        fid.write('\\draw[edge, ->] (0,' + str(RowN//2) +') -- +(' + str(-(ColN))+ ', 0) -- (xor.south east);' + '\n')
                        fid.write('\\coordinate (lastr) at (' + str(ColN//2) + ',' + str(RowN//2) + ');' + '\n')
                        fid.write('\\draw (lastr) -| (' + str(ColN + ColN//2) + ',' + str(-ColN) + ') -| +(' + str(-4 * (ColN + WO) - WO) + ',' + str((self.TR - 1) * (RowN + HO) + (9*RowN)//4) + ') -- (firstl);' + '\n')
                    else:
                        fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize$\SB^' + str(next_r) + '$};'+'\n')
                        fid.write('\\draw[edge, ->] (0,' + str(RowN//2) +') -- +(' + str(-(ColN))+ ', 0) -- (xor.east);' + '\n')
                        fid.write('\\draw[edge,  -] (' + str(ColN) + ',' + str(RowN//2) + ') -| +(' + str(WO + WO//2) + ', '+ str(-(HO//2) - RowN//2) + ') -| +(' + str(-(O+2) * (ColN + WO)) + ', '+ str(-(HO) - RowN) + ') -- +(' + str(-(O+2) * (ColN + WO) + ColN//4) + ', '+ str(-(HO) - RowN) + ');' + '\n')
                    fid.write('\n'+'\\end{scope}'+'\n')
                    if r == self.TR - 1:
                        fid.write('\\begin{scope}[yshift =' + str(+ (6*RowN)//4)+' cm, xshift =' +str(ColN + WO)+' cm]'+'\n')
                        for g in range(MatN):
                            row = (RowN - 1) - g//ColN
                            col = g % ColN
                            cell = [1, 1]
                            if cell == RED:
                                fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                            elif cell == BLUE:
                                fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                            elif cell == GRAY:
                                fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                            else:
                                fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                        for i in range(1, RowN):
                            fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                        for i in range(1, ColN):
                            fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                        fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node (T) {\\scriptsize$T$};'+'\n')
                        fid.write('\\draw[edge, ->] (0,' + str(RowN//2) +') -- +(' + str(-(ColN))+ ', 0) -- (xor.north east);' + '\n')
                        fid.write('\n'+'\\end{scope}'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')
                fid.write('\n\n')

                O = O + 1
                ## O_MC_SupP_
                fid.write('\\begin{scope}[yshift =' + str(- r * (RowN + HO))+' cm, xshift =' + str(O * (ColN + WO) + WO//2)+' cm]'+'\n')
                if r != self.mat_r:
                    fid.write('\\begin{scope}[yshift =' + str(+ RowN + 2)+' cm, xshift =' +str(0)+' cm]'+'\n')
                    for g in range(MatN):
                        row = (RowN - 1) - g//ColN
                        col = g % ColN
                        if ((r in forward_rounds) and (Solution[AK_MC_Rule[col]] == 1))  or ((r in backward_rounds) and (Solution[AK_MC_Rule[col]] == 0)):
                            cell = [Solution[O_MC_SupP_Blue_1[g]], Solution[O_MC_SupP_Blue_2[g]]]
                        if ((r in forward_rounds) and (Solution[AK_MC_Rule[col]] == 0))  or ((r in backward_rounds) and (Solution[AK_MC_Rule[col]] == 1)):
                            cell = [Solution[M_MC_SupP_Blue_1[g]], Solution[M_MC_SupP_Blue_2[g]]]
                        if cell == RED:
                            fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == BLUE:
                            fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == GRAY:
                            fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        else:
                            fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize$\AKBL^' + str(r) + '$};'+'\n')
                    for i in range(1, RowN):
                        fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                    for i in range(1, ColN):
                        fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize };'+'\n')
                    if r != self.mat_r and self.mat_r < self.ini_r:  ###   -1 -f- 0 -f- mat_r -b- ini_r -f- TR
                        fid.write('\\node[XOR,scale=0.6,label={below:{\\tiny AK}}] (xorb) at (' + str(ColN + WO//2) + ',' + str(RowN//2) + ') {};' + '\n')
                        if r < self.mat_r or (r >= self.ini_r): ## f
                            fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- +(' + str(WO) + ',' + '0);' + '\n')
                        else:
                            fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- +(' + str(WO) + ',' + '0);' + '\n')
                    if r != self.mat_r and self.mat_r > self.ini_r:  ###   -1 -b- 0 -b- ini_r -f- mat_r -b- TR
                        fid.write('\\node[XOR,scale=0.6,label={below:{\\tiny AK}}] (xorb) at (' + str(ColN + WO//2) + ',' + str(RowN//2) + ') {};' + '\n')
                        if r >= self.ini_r and r < self.mat_r: ## f
                            fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- +(' + str(WO) + ',' + '0);' + '\n')
                        else:
                            fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- +(' + str(WO) + ',' + '0);' + '\n')
                    fid.write('\n'+'\\end{scope}'+'\n')
                    fid.write('\n\n')

                    for g in range(MatN):
                        row = (RowN - 1) - g//ColN
                        col = g % ColN
                        if ((r in forward_rounds) and (Solution[AK_MC_Rule[col]] == 1))  or ((r in backward_rounds) and (Solution[AK_MC_Rule[col]] == 0)):
                            cell = [Solution[O_MC_SupP_Red__1[g]], Solution[O_MC_SupP_Red__2[g]]]
                        if ((r in forward_rounds) and (Solution[AK_MC_Rule[col]] == 0))  or ((r in backward_rounds) and (Solution[AK_MC_Rule[col]] == 1)):
                            cell = [Solution[M_MC_SupP_Red__1[g]], Solution[M_MC_SupP_Red__2[g]]]
                        if cell == RED:
                            fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == BLUE:
                            fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        elif cell == GRAY:
                            fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                        else:
                            fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\\path (' + str(ColN//2) + ',' + str(0 - 0.8) + ') node {\\scriptsize$\AKRD^' + str(r) + '$};'+'\n')
                    for i in range(1, RowN):
                        fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                    for i in range(1, ColN):
                        fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize };'+'\n')
                    if r != self.mat_r and self.mat_r < self.ini_r:  ###   -1 -f- 0 -f- mat_r -b- ini_r -f- TR
                        fid.write('\\node[XOR,scale=0.6,label={above:{\\tiny AK}}] (xorr) at (' + str(ColN + WO//2) + ',' + str(RowN//2) + ') {};' + '\n')
                        if r < self.mat_r or (r >= self.ini_r): ## f
                            fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- +(' + str(WO) + ',' + '0);' + '\n')
                        else:
                            fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- +(' + str(WO) + ',' + '0);' + '\n')
                    if r != self.mat_r and self.mat_r > self.ini_r:  ###   -1 -b- 0 -b- ini_r -f- mat_r -b- TR
                        fid.write('\\node[XOR,scale=0.6,label={above:{\\tiny AK}}] (xorr) at (' + str(ColN + WO//2) + ',' + str(RowN//2) + ') {};' + '\n')
                        if r >= self.ini_r and r < self.mat_r: ## f
                            fid.write('\\draw[edge, ->] (' + str(ColN) + ',' + str(RowN//2) + ') -- +(' + str(WO) + ',' + '0);' + '\n')
                        else:
                            fid.write('\\draw[edge, <-] (' + str(ColN) + ',' + str(RowN//2) + ') -- +(' + str(WO) + ',' + '0);' + '\n')
                    fid.write('\\draw[edge,  -] (' + str(ColN + WO//2) + ',' + str(RowN//2 + RowN + 2) + ') -- +(' + str(WO//2) + ', 0) -- +(' + str(WO//2) + ', '+ str(-(RowN + 2)//2) + ');' + '\n')
                    if r != self.TR - 1:
                        fid.write('\\draw[edge,  -] (' + str(ColN + WO//2) + ',' + str(RowN//2) + ') -- +(' + str(WO//2) + ', 0) -- +(' + str(WO//2) + ', '+ str(+(RowN + 2)//2) + ') -- +(' + str(WO) + ', '+ str(+(RowN + 2)//2) + ') -| +(' + str(WO) + ', '+ str(-(HO)//2 + RowN//4) + ') -| +(' + str(-(O+1) * (ColN + WO) - (ColN//4)) + ', '+ str(-(HO) - RowN//4) + ') -- +(' + str(-(O+1) * (ColN + WO)) + ', '+ str(-(HO) - RowN//4) + ');' + '\n')
                    else:
                        fid.write('\\draw[edge,  -] (' + str(ColN + WO//2) + ',' + str(RowN//2) + ') -- +(' + str(WO//2) + ', 0) -- +(' + str(WO//2) + ', '+ str(+(RowN + 2)//2) + ') -- +(' + str(WO) + ', '+ str(+(RowN + 2)//2) + ') -| +(' + str(WO) + ', '+ str(-(HO)//2 + RowN//4) + ') -| ++(' + str(-(O+1) * (ColN + WO) - (ColN//2)) + ', '+ str(0) + ') |- (firstl);' + '\n')
                fid.write('\n'+'\\end{scope}'+'\n')
                fid.write('\n\n')

                O = O + 1
                ## MCSK
                fid.write('\\begin{scope}[yshift =' + str(- r * (RowN + HO))+' cm, xshift =' + str(O * (ColN + WO) + WO + WO)+' cm]'+'\n')
                fid.write('\\begin{scope}[yshift =' + str(+ RowN + 2)+' cm, xshift =' +str(0)+' cm]'+'\n')
                for g in range(MatN):
                    row = (RowN - 1) - g//ColN
                    col = g % ColN
                    cell = [Solution[SK_I_MC_SupP_Blue_1[g]], Solution[SK_I_MC_SupP_Blue_2[g]]]
                    if cell == RED:
                        fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == BLUE:
                        fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == GRAY:
                        fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    else:
                        fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                    for i in range(1, RowN):
                        fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                    for i in range(1, ColN):
                        fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                if r != self.mat_r:
                    fid.write('\\draw[edge, ->, dotted] (' + str(ColN//2) + ',' + str(RowN) + ') |- ++(0, 1.6) -| (xormckb);'+'\n')
                else:
                    fid.write('\\draw[edge, ->, dotted] (' + str(ColN//2) + ',' + str(RowN) + ') |- ++(0, 1.6) -| (xor);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')
                fid.write('\n\n')
                for g in range(MatN):
                    row = (RowN - 1) - g//ColN
                    col = g % ColN
                    cell = [Solution[SK_I_MC_SupP_Red__1[g]], Solution[SK_I_MC_SupP_Red__2[g]]]
                    if cell == RED:
                        fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == BLUE:
                        fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == GRAY:
                        fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    else:
                        fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                for i in range(1, RowN):
                    fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                for i in range(1, ColN):
                    fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize$\KMC^{' + str(r-1) + '}$};'+'\n')
                if r != self.mat_r:
                    fid.write('\\draw[edge, ->, dotted] (' + str(ColN//2) + ',' + str(0) + ') |- ++(0, -1.6) -| (xormckr);'+'\n')
                else:
                    fid.write('\\draw[edge, ->, dotted] (' + str(ColN//2) + ',' + str(0) + ') |- ++(0, -1.6) -| (xor);'+'\n')
                fid.write('\\coordinate (keyl) at ('+str(-2)+','+str(RowN + 1)+');' + '\n')
                if r + 1 <= self.ini_k:
                    dirarr = '<-'
                else:
                    dirarr = '->'
                fid.write('\\draw[edge, ' + dirarr + '] ('+str(RowN)+','+str(RowN//2)+')  -- node[above] {\\tiny MC} ++('+str(WO)+', 0);' + '\n')
                fid.write('\\draw[edge, ' + dirarr + '] ('+str(RowN)+','+str(RowN + 2 + RowN//2)+')  -- node[below] {\\tiny MC} ++('+str(WO)+', 0);' + '\n')
                if r != 0:
                    fid.write('\\draw ('+str(0)+','+str(RowN//2)+') -- ++(-1, 0) |- (keyl);' + '\n')
                    fid.write('\\draw ('+str(0)+','+str(RowN + 2 + RowN//2)+') -- ++(-1, 0) |- (keyl);' + '\n')
                    fid.write('\\draw[edge, ' + '-' + '] (keyr)  |- ++(' + str(0) + ',' + str(-RowN - 4) + ') -| (keyl);' + '\n')
                fid.write('\n'+'\\end{scope}'+'\n')
                fid.write('\n\n')

                O = O + 1
                ## SK
                fid.write('\\begin{scope}[yshift =' + str(- r * (RowN + HO))+' cm, xshift =' + str(O * (ColN + WO) + WO + WO)+' cm]'+'\n')
                fid.write('\\begin{scope}[yshift =' + str(+ RowN + 2)+' cm, xshift =' +str(0)+' cm]'+'\n')
                for g in range(MatN):
                    row = (RowN - 1) - g//ColN
                    col = g % ColN
                    cell = [Solution[SK_SupP_Blue_1[g]], Solution[SK_SupP_Blue_2[g]]]
                    if cell == RED:
                        fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == BLUE:
                        fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == GRAY:
                        fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    else:
                        fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                for i in range(1, RowN):
                    fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                for i in range(1, ColN):
                    fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                if r != self.mat_r:
                    fid.write('\\draw[edge, ->, dotted] (' + str(ColN//2) + ',' + str(RowN) + ') |- ++(0, +0.8) -| (xorb);'+'\n')
                else:
                    fid.write('\\draw[edge, ->, dotted] (' + str(ColN//2) + ',' + str(RowN) + ') |- ++(0, +0.8) -| (xor);'+'\n')
                fid.write('\n'+'\\end{scope}'+'\n')
                fid.write('\n\n')
                for g in range(MatN):
                    row = (RowN - 1) - g//ColN
                    col = g % ColN
                    cell = [Solution[SK_SupP_Red__1[g]], Solution[SK_SupP_Red__2[g]]]
                    if cell == RED:
                        fid.write('\\fill[\\BW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == BLUE:
                        fid.write('\\fill[\\FW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    elif cell == GRAY:
                        fid.write('\\fill[\\CW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    else:
                        fid.write('\\fill[\\UW] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                for i in range(1, RowN):
                    fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                for i in range(1, ColN):
                    fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                fid.write('\\path (' + str(ColN//2) + ',' + str(RowN + 0.5) + ') node {\\scriptsize$ k_' + str(r) + '$};'+'\n')
                if r != self.mat_r:
                    fid.write('\\draw[edge, ->, dotted] (' + str(ColN//2) + ',' + str(0) + ') |- ++(0, -0.8) -| (xorr);'+'\n')
                else:
                    fid.write('\\draw[edge, ->, dotted] (' + str(ColN//2) + ',' + str(0) + ') |- ++(0, -0.8) -| (xor);'+'\n')
                if r + 1 == self.ini_k:
                    fid.write('\\path (' + str(ColN//2) + ',' + str(-0.8) + ') node {\\scriptsize$(+' + str(ini_d1_key) + '~\\DoFF,~+' + str(ini_d2_key) + '~\\DoFB)$};'+'\n')
                    fid.write('\\path (' + str(ColN + 2) + ',' + str(0.8) + ') node {\\scriptsize$\\StKSA$};'+'\n')

                if r + 1 < self.TR:
                    CD1_KS = 0
                    CD2_KS = 0
                    for g in range(KSColN):
                        CD1_KS = CD1_KS + Solution[SK_G_CD_MC_Blue[g]]
                        CD2_KS = CD2_KS + Solution[SK_G_CD_MC_Red_[g]]
                    if r + 1 < self.ini_k:
                        fid.write('\\path (' + str(ColN//2) + ',' + str(-2) + ') node {\\scriptsize$(-' + str(CD1_KS) + '~\\DoFF,~-' + str(CD2_KS) + '~\\DoFB)$};'+'\n')
                    else:
                        fid.write('\\path (' + str(ColN//2) + ',' + str(-2) + ') node {\\scriptsize$(-' + str(CD1_KS) + '~\\DoFF,~-' + str(CD2_KS) + '~\\DoFB)$};'+'\n')
                if r != self.TR - 1:
                    fid.write('\\coordinate (keyr) at ('+str(ColN + 2)+','+str(RowN + 1)+');' + '\n')
                    fid.write('\\draw ('+str(ColN)+','+str(RowN//2)+') -- ++(+1, 0) |- (keyr);' + '\n')
                    fid.write('\\draw ('+str(ColN)+','+str(RowN + 2 + RowN//2)+') -- ++(+1, 0) |- (keyr);' + '\n')
                fid.write('\n'+'\\end{scope}'+'\n')
                fid.write('\n\n')

                ## WG
                if r != self.mat_r:
                    if r in forward_rounds:
                        xoff = 2 * (ColN + WO) + WO//2
                    elif r in backward_rounds:
                        xoff = 3 * (ColN + WO) + WO//2
                    fid.write('\\begin{scope}[yshift =' + str(- r * (RowN + HO))+' cm, xshift =' +str(xoff)+' cm]'+'\n')
                    for g in range(MatN):
                        row = (RowN - 1) - g//ColN
                        col = g % ColN
                        guess_red = Solution[MC_GuessRed_[g]]
                        if guess_red == 1:
                            guessRD += 1
                            fid.write('\\fill[pink] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                    for i in range(1, RowN):
                        fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                    for i in range(1, ColN):
                        fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                    CD_guess_blue = 0
                    CD_guess_red = 0
                    for g in range(MatN):
                        CD_guess_blue = CD_guess_blue + Solution[MC_GuessBlue[g]]
                        CD_guess_red = CD_guess_red + Solution[MC_GuessRed_[g]]
                    fid.write('\\path (' + str(-xoff + 3 * (ColN + WO)) + ',' + str(RowN  + 0.8) + ') node {\\scriptsize$(+' + str(CD_guess_red) + '~\\DoFBG,~+' + str(CD_guess_blue) + '~\\DoFFG)$};'+'\n')
                    fid.write('\n'+'\\end{scope}'+'\n')
                    fid.write('\n\n')
                    fid.write('\\begin{scope}[yshift =' + str(- r * (RowN + HO) + RowN + 2)+' cm, xshift =' +str(xoff)+' cm]'+'\n')
                    for g in range(MatN):
                        row = (RowN - 1) - g//ColN
                        col = g % ColN
                        guess_blue = Solution[MC_GuessBlue[g]]
                        if guess_blue == 1:
                            guessBL += 1
                            fid.write('\\fill[cyan] ('+str(col)+','+str(row)+') rectangle +(1,1);'+'\n')
                    fid.write('\\draw (0,0) rectangle (' + str(ColN) + ',' + str(RowN) + ');' + '\n')
                    for i in range(1, RowN):
                        fid.write('\\draw (' + str(0) + ',' + str(i) + ') rectangle (' + str(ColN) + ',' + str(0) + ');' + '\n')
                    for i in range(1, ColN):
                        fid.write('\\draw (' + str(i) + ',' + str(0) + ') rectangle (' + str(0) + ',' + str(RowN) + ');' + '\n')
                    fid.write('\n'+'\\end{scope}'+'\n')
                    fid.write('\n\n')
        ## Final
        fid.write('\\begin{scope}[yshift =' + str(- self.TR * (RowN + HO) + HO//2)+' cm, xshift =' +str(3 * (ColN + WO) + WO)+' cm]'+'\n')
        fid.write(
            '\\node[draw, thick, rectangle, text width=13.5cm, label={[shift={(-3.8,-0)}]\\footnotesize Config}] at (0, 0) {' + '\n'
		    '{\\footnotesize' + '\n'
		    '$\\bullet~(\\varInitBL,~\\varInitRD)~=~(' + str((ini_d1 + ini_d1_key)) + '~\\DoFF,~' + str((ini_d2 + ini_d2_key)) + '~\\DoFB)~$' + ' \n'
		    '$\\bullet~(\\varDoFBL,~\\varDoFRD,~\\varDoM,~\\varDoFGESSBL,~\\varDoFGESSRD,~\\varDoFGESSBR)~=~(' + 
            str(Solution[Deg1] + guessRD) + '~\\DoFF,~' + 
            str(Solution[Deg2] + guessBL) + '~\\DoFB,~' + 
            str(Solution[GM] + guessBL + guessRD + guessBR) + '~\\DoM,~' + 
            str(guessBL) + '~\\DoFFG,~' + 
            str(guessRD) + '~\\DoFBG,~' + 
            str(guessBR) + '~\\DoFFBG)~$' + '\\\ \n'
		    '$\\bullet~(\\varDoFBL-\\varDoFGESSRD,~\\varDoFRD-\\varDoFGESSBL,~\\varDoM-\\varDoFGESSBL-\\varDoFGESSRD-\\varDoFGESSBR)~=~(' + 
            str(Solution[Deg1]) + ',~' + 
            str(Solution[Deg2]) + ',~' + 
            str(Solution[GM]) + '~)$' + '\n'
		    '}' + '\n'
	        '};' + '\n'
            )
        fid.write('\n'+'\\end{scope}'+'\n')
        fid.write('\n\n')
        fid.write('\\end{tikzpicture}'+'\n\n'+'\\end{document}')
        fid.close()

#D = DrawDistinguisher('./Model4_R6_Simplified/TR6_ini3_inikr3_matr1_all_1.sol', 6,3,3,1); D.draw('./Model4_R6_Simplified/TR6_ini3_inikr3_matr1_all_1.tex'); system("pdflatex -output-directory='./Model4_R6_Simplified' ./Model4_R6_Simplified/TR6_ini3_inikr3_matr1_all_1.tex") 

D = DrawDistinguisher('./Model8_R6_Simplified/TR6_ini3_inikr3_matr1_all_8.sol', 6,3,3,1); D.draw('./Model8_R6_Simplified/TR6_ini3_inikr3_matr1_all_8.tex'); system("pdflatex -output-directory='./Model8_R6_Simplified' ./Model8_R6_Simplified/TR6_ini3_inikr3_matr1_all_8.tex") 
