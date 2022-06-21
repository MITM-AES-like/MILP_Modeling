#!/bin/bash

import sys, getopt
from datetime import datetime
import time
from Basic_Guess import *
from gurobipy import *

KS_GUESS = 0
TWO_RULES = 0
CD_BOTH = 0

class Vars_generator:
    @staticmethod
    def genVars_O_SB(r, colori):
        if r >= 0:
            return ['O_SB_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
        else:
            return ['O_SB_' + str(colori) + '_' + str(j) + '_r_minus' + str(-r) for j in range(MatN)]
    @staticmethod
    def genVars_I_MC(r, colori):
        return ['I_MC_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]

    @staticmethod
    def genVars_AK_MC_Rule(r):
        return ['AK_MC_Rule_' + str(j) + '_r' + str(r) for j in range(ColN)]

    @staticmethod
    def genVars_Enc_isWhite(r):
        return ['Enc_isWhite_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_EncSK_isWhite(r):
        return ['EncSK_isWhite_' + str(j) + '_r' + str(r) for j in range(MatN)]

    @staticmethod
    def genVars_Enc_GuessBlue(r):
        return ['Enc_GuessBlue_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_Enc_GuessRed_(r):
        return ['Enc_GuessRed__' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_Enc_GuessBoth(r):
        return ['Enc_GuessBoth_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_AK_ConsumedDeg_Blue(r):
        return ['CD_AK_Blue_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_AK_ConsumedDeg_Red_(r):
        return ['CD_AK_Red__' + str(j) + '_r' + str(r) for j in range(MatN)]

    @staticmethod
    def genVars_I_MCAK_SupP_Blue(r, colori):
        return ['I_MCAK_SupP_Blue_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_I_MCAK_SupP_Red_(r, colori):
        return ['I_MCAK_SupP_Red__' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_M_MCAK_SupP_Blue(r, colori):
        return ['M_MCAK_SupP_Blue_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_M_MCAK_SupP_Red_(r, colori):
        return ['M_MCAK_SupP_Red__' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_O_MCAK_SupP_Blue(r, colori):
        return ['O_MCAK_SupP_Blue_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_O_MCAK_SupP_Red_(r, colori):
        return ['O_MCAK_SupP_Red__' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]

    @staticmethod
    def genVars_EncSK_SupP_Blue_AND(r, colori):
        return ['EncSK_SupP_Blue_AND_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_EncSK_SupP_Blue_OR_(r, colori):
        return ['EncSK_SupP_Blue_OR__' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_EncSK_SupP_Red__AND(r, colori):
        return ['EncSK_SupP_Red__AND_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_EncSK_SupP_Red__OR_(r, colori):
        return ['EncSK_SupP_Red__OR__' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]

    @staticmethod
    def genVars_MC_SupP_Blue_ColExistWhite(r):
        return ['MC_SupP_Blue_ColExistWhite_' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_SupP_Red__ColExistWhite(r):
        return ['MC_SupP_Red__ColExistWhite_' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_SupP_Blue_ColAllGray(r):
        return ['MC_SupP_Blue_ColAllGray_' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_SupP_Red__ColAllGray(r):
        return ['MC_SupP_Red__ColAllGray_' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_SupP_Blue_SumGray(r):
        return ['G_SupP_Blue_SumGray_' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_SupP_Red__SumGray(r):
        return ['G_SupP_Red__SumGray_' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_ConsumedDeg_Blue(r):
        return ['G_CD_MC_Blue_' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_ConsumedDeg_Red_(r):
        return ['G_CD_MC_Red__' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_ConsumedDeg_Blue_Rule1(r):
        return ['G_CD_MC_Blue_Rule1_' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_ConsumedDeg_Red__Rule1(r):
        return ['G_CD_MC_Red___Rule1' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_ConsumedDeg_Blue_Rule0(r):
        return ['G_CD_MC_Blue_Rule0_' + str(j) + '_r' + str(r) for j in range(ColN)]
    @staticmethod
    def genVars_MC_ConsumedDeg_Red__Rule0(r):
        return ['G_CD_MC_Red___Rule0' + str(j) + '_r' + str(r) for j in range(ColN)]

    @staticmethod
    def genVars_SK_O_SB(r, colori):
        return ['SK_O_SB_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_I_MC(r, colori):
        return ['SK_I_MC_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_I_MC_SupP_Blue(r, colori):
        return ['SK_I_MC_SupP_Blue_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_I_MC_SupP_Red_(r, colori):
        return ['SK_I_MC_SupP_Red__' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_SupP_Blue(r, colori):
        return ['SK_SupP_Blue_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_SupP_Red_(r, colori):
        return ['SK_SupP_Red__' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_isWhite(r):
        return ['SK_isWhite_' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_GuessBlue(r):
        return ['SK_GuessBlue_' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_GuessRed_(r):
        return ['SK_GuessRed__' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_GuessBoth(r):
        return ['SK_GuessBoth_' + str(j) + '_r' + str(r) for j in range(KeyCellN)]
    @staticmethod
    def genVars_SK_MC_SupP_Blue_ColExistWhite(r):
        return ['SK_MC_SupP_Blue_ColExistWhite_' + str(j) + '_r' + str(r) for j in range(KSColN)]
    @staticmethod
    def genVars_SK_MC_SupP_Red__ColExistWhite(r):
        return ['SK_MC_SupP_Red__ColExistWhite_' + str(j) + '_r' + str(r) for j in range(KSColN)]
    @staticmethod
    def genVars_SK_MC_SupP_Blue_ColAllGray(r):
        return ['SK_MC_SupP_Blue_ColAllGray_' + str(j) + '_r' + str(r) for j in range(KSColN)]
    @staticmethod
    def genVars_SK_MC_SupP_Red__ColAllGray(r):
        return ['SK_MC_SupP_Red__ColAllGray_' + str(j) + '_r' + str(r) for j in range(KSColN)]
    @staticmethod
    def genVars_SK_MC_SupP_Blue_SumGray(r):
        return ['G_SK_SupP_Blue_SumGray_' + str(j) + '_r' + str(r) for j in range(KSColN)]
    @staticmethod
    def genVars_SK_MC_SupP_Red__SumGray(r):
        return ['G_SK_SupP_Red__SumGray_' + str(j) + '_r' + str(r) for j in range(KSColN)]
    @staticmethod
    def genVars_SK_MC_ConsumedDeg_Blue(r):
        return ['G_SK_CD_MC_Blue_' + str(j) + '_r' + str(r) for j in range(KSColN)]
    @staticmethod
    def genVars_SK_MC_ConsumedDeg_Red_(r):
        return ['G_SK_CD_MC_Red__' + str(j) + '_r' + str(r) for j in range(KSColN)]

    @staticmethod
    def genVars_Match_I_MC_Enc_White(r):
        return ['Match_I_MC_Enc_White_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_Match_O_MC_Enc_White(r):
        return ['Match_O_MC_Enc_White_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_Match_SK_White(r):
        return ['Match_SK_White_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_Match_EncOrSK_White(r):
        return ['Match_EncOrSK_White_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_Match_EncSK_AND(r, colori):
        return ['Match_EncSK_AND_' + str(colori) + '_' + str(j) + '_r' + str(r) for j in range(MatN)]
    @staticmethod
    def genVars_Match_Exist_Blue():
        return ['Match_Exist_Blue_' + str(j) for j in range(ColN)]
    @staticmethod
    def genVars_Match_Exist_Red_():
        return ['Match_Exist_Red__' + str(j) for j in range(ColN)]
    @staticmethod
    def genVars_Match_Exist_More():
        return ['Match_Exist_More_' + str(j) for j in range(ColN)]
    @staticmethod
    def genVars_Match_Exist_Filter():
        return ['Match_Exist_Filter_' + str(j) for j in range(ColN)]
    @staticmethod
    def genVar_Match_Counted():
        return ['G_Match_Counted_' + str(j) for j in range(ColN)]

    @staticmethod
    def genVars_degree_forward():
        return ['deg_f' + str(j) for j in range(MatN)]
    @staticmethod
    def genVars_degree_backward():
        return ['deg_b' + str(j) for j in range(MatN)]
    @staticmethod
    def genVars_degree_forward_key():
        return ['degSk_f' + str(j) for j in range(KeyCellN)]
    @staticmethod
    def genVars_degree_backward_key():
        return ['degSk_b' + str(j) for j in range(KeyCellN)]


class Constraints_generator_():
    def __init__(self,
        total_round,
        initial_round,
        initial_round_key,
        matching_round):
        self.ini_r = initial_round
        self.mat_r = matching_round
        self.TR = total_round
        self.ini_k = initial_round_key

    @staticmethod
    def genConstraints_Constant(pre, A, con):
        constr = []
        for x in A:
            constr = constr + [pre + x + ' = ' + str(con)]
        return constr

    def Separate_without_Guess(self,
        pre,
        In_1_i,
        In_2_i,
        SupP_Blue_1_i,
        SupP_Blue_2_i,
        SupP_Red__1_i,
        SupP_Red__2_i,
        In_isWhite_i):
        constr = []
        constr = constr + BasicTools.N_OR_(pre, [In_1_i, In_2_i], In_isWhite_i)
        constr = constr + [pre + SupP_Blue_1_i + ' + ' + In_isWhite_i + ' = 1']
        constr = constr + [pre + SupP_Blue_2_i + ' - ' + In_2_i + ' = 0']
        constr = constr + [pre + SupP_Red__2_i + ' - ' + SupP_Blue_1_i + ' = 0']
        constr = constr + [pre + SupP_Red__1_i + ' - ' + In_1_i + ' = 0']
        return constr

    def Separate_with_Guess(self,
        pre,
        In_1_i,
        In_2_i,
        SupP_Blue_1_i,
        SupP_Blue_2_i,
        SupP_Red__1_i,
        SupP_Red__2_i,
        In_isWhite_i,
        GuessBlue_i,
        GuessRed__i,
        GuessBoth_i):
        constr = []
        constr = constr + BasicTools.N_OR_(pre, [In_1_i, In_2_i], In_isWhite_i)
        constr = constr + [pre + GuessBlue_i + ' + ' + GuessRed__i + ' + ' + GuessBoth_i + ' - ' + In_isWhite_i + ' <= 0']
        constr = constr + [pre + SupP_Blue_1_i + ' - ' + GuessBlue_i + ' - ' + GuessRed__i + ' - ' + GuessBoth_i + ' + ' + In_isWhite_i + ' = 1']
        constr = constr + [pre + SupP_Blue_2_i + ' - ' + In_2_i + ' - ' + GuessRed__i + ' = 0']
        constr = constr + [pre + SupP_Red__2_i + ' - ' + SupP_Blue_1_i + ' = 0']
        constr = constr + [pre + SupP_Red__1_i + ' - ' + In_1_i + ' - ' + GuessBlue_i + ' = 0']
        return constr

    def ARK_with_Guess(self,
        pre,
        Enc_SupP_Blue_1_i,
        Enc_SupP_Blue_2_i,
        Enc_SupP_Red__1_i,
        Enc_SupP_Red__2_i,
        SK__SupP_Blue_1_i,
        SK__SupP_Blue_2_i,
        SK__SupP_Red__1_i,
        SK__SupP_Red__2_i,
        EncSK_SupP_Blue_1_i,
        EncSK_SupP_Blue_2_i,
        EncSK_SupP_Red__1_i,
        EncSK_SupP_Red__2_i,
        GuessBlue_i,
        GuessRed__i,
        GuessBoth_i,
        CD_ARK_Blue_i,
        CD_ARK_Red__i,
        EncSK_isWhite_i,
        EncSK_SupP_Blue_AND_1_i,
        EncSK_SupP_Blue_AND_2_i,
        EncSK_SupP_Blue_OR__1_i,
        EncSK_SupP_Blue_OR__2_i,
        EncSK_SupP_Red__AND_1_i,
        EncSK_SupP_Red__AND_2_i,
        EncSK_SupP_Red__OR__1_i,
        EncSK_SupP_Red__OR__2_i):
        constr = []
        constr = constr + BasicTools.N_AND(pre, [Enc_SupP_Blue_1_i, SK__SupP_Blue_1_i], EncSK_isWhite_i)
        constr = constr + [pre + GuessBlue_i + ' + ' + GuessRed__i + ' + ' + GuessBoth_i + ' - ' + EncSK_isWhite_i + ' <= 0']
        #
        constr = constr + BasicTools.AND(pre, [Enc_SupP_Blue_2_i, SK__SupP_Blue_2_i], EncSK_SupP_Blue_AND_2_i)
        constr = constr + BasicTools.OR_(pre, [Enc_SupP_Blue_2_i, SK__SupP_Blue_2_i], EncSK_SupP_Blue_OR__2_i)
        constr = constr + [pre + CD_ARK_Blue_i + ' + ' + EncSK_SupP_Blue_OR__2_i + ' <= 1']
        constr = constr + [pre + CD_ARK_Blue_i + ' + ' + EncSK_isWhite_i + ' <= 1']
        constr = constr + [pre + EncSK_SupP_Blue_1_i + ' + ' + EncSK_isWhite_i + ' - ' + GuessBlue_i + ' - ' + GuessRed__i + ' - ' + GuessBoth_i + ' = 1']
        constr = constr + [pre + EncSK_SupP_Blue_2_i + ' - ' + EncSK_SupP_Blue_AND_2_i + ' - ' + CD_ARK_Blue_i + ' - ' + GuessRed__i + ' = 0']
        #
        constr = constr + BasicTools.AND(pre, [Enc_SupP_Red__1_i, SK__SupP_Red__1_i], EncSK_SupP_Red__AND_1_i)
        constr = constr + BasicTools.OR_(pre, [Enc_SupP_Red__1_i, SK__SupP_Red__1_i], EncSK_SupP_Red__OR__1_i)
        constr = constr + [pre + CD_ARK_Red__i + ' + ' + EncSK_SupP_Red__OR__1_i + ' <= 1']
        constr = constr + [pre + CD_ARK_Red__i + ' + ' + EncSK_isWhite_i + ' <= 1']
        constr = constr + [pre + EncSK_SupP_Red__2_i + ' + ' + EncSK_isWhite_i + ' - ' + GuessBlue_i + ' - ' + GuessRed__i + ' - ' + GuessBoth_i + ' = 1']
        constr = constr + [pre + EncSK_SupP_Red__1_i + ' - ' + EncSK_SupP_Red__AND_1_i + ' - ' + CD_ARK_Red__i + ' - ' + GuessBlue_i + ' = 0']
        return constr

    def ARK_without_Guess(self,
        pre,
        Enc_SupP_Blue_1_i,
        Enc_SupP_Blue_2_i,
        Enc_SupP_Red__1_i,
        Enc_SupP_Red__2_i,
        SK__SupP_Blue_1_i,
        SK__SupP_Blue_2_i,
        SK__SupP_Red__1_i,
        SK__SupP_Red__2_i,
        EncSK_SupP_Blue_1_i,
        EncSK_SupP_Blue_2_i,
        EncSK_SupP_Red__1_i,
        EncSK_SupP_Red__2_i,
        CD_ARK_Blue_i,
        CD_ARK_Red__i,
        EncSK_isWhite_i,
        EncSK_SupP_Blue_AND_1_i,
        EncSK_SupP_Blue_AND_2_i,
        EncSK_SupP_Blue_OR__1_i,
        EncSK_SupP_Blue_OR__2_i,
        EncSK_SupP_Red__AND_1_i,
        EncSK_SupP_Red__AND_2_i,
        EncSK_SupP_Red__OR__1_i,
        EncSK_SupP_Red__OR__2_i):
        constr = []
        constr = constr + BasicTools.N_AND(pre, [Enc_SupP_Blue_1_i, SK__SupP_Blue_1_i], EncSK_isWhite_i)
        #
        constr = constr + BasicTools.AND(pre, [Enc_SupP_Blue_2_i, SK__SupP_Blue_2_i], EncSK_SupP_Blue_AND_2_i)
        constr = constr + BasicTools.OR_(pre, [Enc_SupP_Blue_2_i, SK__SupP_Blue_2_i], EncSK_SupP_Blue_OR__2_i)
        constr = constr + [pre + CD_ARK_Blue_i + ' + ' + EncSK_SupP_Blue_OR__2_i + ' <= 1']
        constr = constr + [pre + CD_ARK_Blue_i + ' + ' + EncSK_isWhite_i + ' <= 1']
        constr = constr + [pre + EncSK_SupP_Blue_1_i + ' + ' + EncSK_isWhite_i + ' = 1']
        constr = constr + [pre + EncSK_SupP_Blue_2_i + ' - ' + EncSK_SupP_Blue_AND_2_i + ' - ' + CD_ARK_Blue_i + ' = 0']
        #
        constr = constr + BasicTools.AND(pre, [Enc_SupP_Red__1_i, SK__SupP_Red__1_i], EncSK_SupP_Red__AND_1_i)
        constr = constr + BasicTools.OR_(pre, [Enc_SupP_Red__1_i, SK__SupP_Red__1_i], EncSK_SupP_Red__OR__1_i)
        constr = constr + [pre + CD_ARK_Red__i + ' + ' + EncSK_SupP_Red__OR__1_i + ' <= 1']
        constr = constr + [pre + CD_ARK_Red__i + ' + ' + EncSK_isWhite_i + ' <= 1']
        constr = constr + [pre + EncSK_SupP_Red__2_i + ' + ' + EncSK_isWhite_i + ' = 1']
        constr = constr + [pre + EncSK_SupP_Red__1_i + ' - ' + EncSK_SupP_Red__AND_1_i + ' - ' + CD_ARK_Red__i + ' = 0']
        return constr

    @staticmethod
    def gensubConstraints_MC_SupP__Blue(
        pre,
        I_MC_SupP_Blue_1_coli,
        I_MC_SupP_Blue_2_coli,
        I_MC_SupP_Blue_ColExistWhite_coli,
        I_MC_SupP_Blue_ColAllGray_coli,
        O_MC_SupP_Blue_1_coli,
        O_MC_SupP_Blue_2_coli,
        G_SupP_Blue_SumGray_coli,
        G_CD_MC_Blue_coli):
        constr = []
        constr = constr + BasicTools.N_AND(pre, I_MC_SupP_Blue_1_coli, I_MC_SupP_Blue_ColExistWhite_coli)
        constr = constr + BasicTools.AND(pre, I_MC_SupP_Blue_2_coli, I_MC_SupP_Blue_ColAllGray_coli)
        constr = constr + [pre + BasicTools._plusTerms(O_MC_SupP_Blue_1_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Blue_ColExistWhite_coli + ' = ' + str(RowN)]
        constr = constr + [pre + BasicTools._plusTerms(O_MC_SupP_Blue_2_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Blue_ColExistWhite_coli + ' <= ' + str(RowN)]
        constr = constr + [pre + G_SupP_Blue_SumGray_coli + ' - ' + BasicTools.minusTerms(I_MC_SupP_Blue_2_coli) + ' - ' + BasicTools.minusTerms(O_MC_SupP_Blue_2_coli) + ' = 0']
        constr = constr + [pre + G_SupP_Blue_SumGray_coli + ' - ' + str(BranchN) + ' ' + I_MC_SupP_Blue_ColAllGray_coli + ' <= ' + str(SumIOMC - BranchN)]
        constr = constr + [pre + G_SupP_Blue_SumGray_coli + ' - ' + str(SumIOMC) + ' ' + I_MC_SupP_Blue_ColAllGray_coli + ' >= 0']
        constr = constr + [pre + G_CD_MC_Blue_coli + ' - ' + BasicTools.minusTerms(O_MC_SupP_Blue_2_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Blue_ColAllGray_coli + ' = 0']
        return constr

    @staticmethod
    def gensubConstraints_MC_SupP__Red(
        pre,
        I_MC_SupP_Red__1_coli,
        I_MC_SupP_Red__2_coli,
        I_MC_SupP_Red__ColExistWhite_coli,
        I_MC_SupP_Red__ColAllGray_coli,
        O_MC_SupP_Red__1_coli,
        O_MC_SupP_Red__2_coli,
        G_SupP_Red__SumGray_coli,
        G_CD_MC_Red__coli):
        constr = []
        constr = constr + BasicTools.N_AND(pre, I_MC_SupP_Red__2_coli, I_MC_SupP_Red__ColExistWhite_coli)
        constr = constr + BasicTools.AND(pre, I_MC_SupP_Red__1_coli, I_MC_SupP_Red__ColAllGray_coli)
        constr = constr + [pre + BasicTools._plusTerms(O_MC_SupP_Red__2_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Red__ColExistWhite_coli + ' = ' + str(RowN)]
        constr = constr + [pre + BasicTools._plusTerms(O_MC_SupP_Red__1_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Red__ColExistWhite_coli + ' <= ' + str(RowN)]
        constr = constr + [pre + G_SupP_Red__SumGray_coli + ' - ' + BasicTools.minusTerms(I_MC_SupP_Red__1_coli) + ' - ' + BasicTools.minusTerms(O_MC_SupP_Red__1_coli) + ' = 0']
        constr = constr + [pre + G_SupP_Red__SumGray_coli + ' - ' + str(BranchN) + ' ' + I_MC_SupP_Red__ColAllGray_coli + ' <= ' + str(SumIOMC - BranchN)]
        constr = constr + [pre + G_SupP_Red__SumGray_coli + ' - ' + str(SumIOMC) + ' ' + I_MC_SupP_Red__ColAllGray_coli + ' >= 0']
        constr = constr + [pre + G_CD_MC_Red__coli + ' - ' + BasicTools.minusTerms(O_MC_SupP_Red__1_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Red__ColAllGray_coli + ' = 0']
        return constr


    def genConstraints_of_forwardRound(self, r):
        if r < self.TR - 1            : 
            next_r                    = r + 1
        else                          : # the last round, next round the 0
            next_r                    = 0
        O_SB_1                     = Vars_generator.genVars_O_SB(r, 1)
        O_SB_2                     = Vars_generator.genVars_O_SB(r, 2)
        I_MC_1                     = Vars_generator.genVars_I_MC(r, 1)
        I_MC_2                     = Vars_generator.genVars_I_MC(r, 2)
        O_SB_next_r_1              = Vars_generator.genVars_O_SB(next_r, 1)
        O_SB_next_r_2              = Vars_generator.genVars_O_SB(next_r, 2)
        #
        I_MCAK_SupP_Blue_1         = Vars_generator.genVars_I_MCAK_SupP_Blue(r, 1)
        I_MCAK_SupP_Blue_2         = Vars_generator.genVars_I_MCAK_SupP_Blue(r, 2)
        I_MCAK_SupP_Red__1         = Vars_generator.genVars_I_MCAK_SupP_Red_(r, 1)
        I_MCAK_SupP_Red__2         = Vars_generator.genVars_I_MCAK_SupP_Red_(r, 2)
        M_MCAK_SupP_Blue_1         = Vars_generator.genVars_M_MCAK_SupP_Blue(r, 1)
        M_MCAK_SupP_Blue_2         = Vars_generator.genVars_M_MCAK_SupP_Blue(r, 2)
        M_MCAK_SupP_Red__1         = Vars_generator.genVars_M_MCAK_SupP_Red_(r, 1)
        M_MCAK_SupP_Red__2         = Vars_generator.genVars_M_MCAK_SupP_Red_(r, 2)
        O_MCAK_SupP_Blue_1         = Vars_generator.genVars_O_MCAK_SupP_Blue(r, 1)
        O_MCAK_SupP_Blue_2         = Vars_generator.genVars_O_MCAK_SupP_Blue(r, 2)
        O_MCAK_SupP_Red__1         = Vars_generator.genVars_O_MCAK_SupP_Red_(r, 1)
        O_MCAK_SupP_Red__2         = Vars_generator.genVars_O_MCAK_SupP_Red_(r, 2)
        #
        Enc_isWhite                = Vars_generator.genVars_Enc_isWhite(r)
        EncSK_isWhite              = Vars_generator.genVars_EncSK_isWhite(r)
        #
        Enc_GuessBlue              = Vars_generator.genVars_Enc_GuessBlue(r)
        Enc_GuessRed_              = Vars_generator.genVars_Enc_GuessRed_(r)
        Enc_GuessBoth              = Vars_generator.genVars_Enc_GuessBoth(r)
        CD_AK_Blue                 = Vars_generator.genVars_AK_ConsumedDeg_Blue(r)
        CD_AK_Red_                 = Vars_generator.genVars_AK_ConsumedDeg_Red_(r)
        #
        EncSK_SupP_Blue_OR__1      = Vars_generator.genVars_EncSK_SupP_Blue_OR_(r, 1)
        EncSK_SupP_Blue_OR__2      = Vars_generator.genVars_EncSK_SupP_Blue_OR_(r, 2)
        EncSK_SupP_Blue_AND_1      = Vars_generator.genVars_EncSK_SupP_Blue_AND(r, 1)
        EncSK_SupP_Blue_AND_2      = Vars_generator.genVars_EncSK_SupP_Blue_AND(r, 2)
        EncSK_SupP_Red__OR__1      = Vars_generator.genVars_EncSK_SupP_Red__OR_(r, 1)
        EncSK_SupP_Red__OR__2      = Vars_generator.genVars_EncSK_SupP_Red__OR_(r, 2)
        EncSK_SupP_Red__AND_1      = Vars_generator.genVars_EncSK_SupP_Red__AND(r, 1)
        EncSK_SupP_Red__AND_2      = Vars_generator.genVars_EncSK_SupP_Red__AND(r, 2)
        #
        MC_SupP_Blue_ColExistWhite = Vars_generator.genVars_MC_SupP_Blue_ColExistWhite(r)
        MC_SupP_Red__ColExistWhite = Vars_generator.genVars_MC_SupP_Red__ColExistWhite(r)
        MC_SupP_Blue_ColAllGray    = Vars_generator.genVars_MC_SupP_Blue_ColAllGray(r)
        MC_SupP_Red__ColAllGray    = Vars_generator.genVars_MC_SupP_Red__ColAllGray(r)
        G_SupP_Blue_SumGray        = Vars_generator.genVars_MC_SupP_Blue_SumGray(r)
        G_SupP_Red__SumGray        = Vars_generator.genVars_MC_SupP_Red__SumGray(r)
        G_CD_MC_Blue               = Vars_generator.genVars_MC_ConsumedDeg_Blue(r)
        G_CD_MC_Red_               = Vars_generator.genVars_MC_ConsumedDeg_Red_(r)
        G_CD_MC_Blue_Rule1         = Vars_generator.genVars_MC_ConsumedDeg_Blue_Rule1(r)
        G_CD_MC_Red__Rule1         = Vars_generator.genVars_MC_ConsumedDeg_Red__Rule1(r)
        G_CD_MC_Blue_Rule0         = Vars_generator.genVars_MC_ConsumedDeg_Blue_Rule0(r)
        G_CD_MC_Red__Rule0         = Vars_generator.genVars_MC_ConsumedDeg_Red__Rule0(r)
        #
        SK_I_MC_SupP_Blue_1        = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 1)
        SK_I_MC_SupP_Blue_2        = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 2)
        SK_I_MC_SupP_Red__1        = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 1)
        SK_I_MC_SupP_Red__2        = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 2)
        SK_SupP_Blue_1             = Vars_generator.genVars_SK_SupP_Blue(r, 1)
        SK_SupP_Blue_2             = Vars_generator.genVars_SK_SupP_Blue(r, 2)
        SK_SupP_Red__1             = Vars_generator.genVars_SK_SupP_Red_(r, 1)
        SK_SupP_Red__2             = Vars_generator.genVars_SK_SupP_Red_(r, 2)
        SK_G_CD_MC_Blue            = Vars_generator.genVars_SK_MC_ConsumedDeg_Blue(r)
        SK_G_CD_MC_Red_            = Vars_generator.genVars_SK_MC_ConsumedDeg_Red_(r)
        #
        AK_MC_Rule                 = Vars_generator.genVars_AK_MC_Rule(r)
        #
        constr = []
        # - Constraints for ShiftRows
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(O_SB_1), I_MC_1)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(O_SB_2), I_MC_2)
        # - Constraints for MixColumns and AddRoundKey
        for coli in range(ColN):
            Enc_1_coli                 = column(I_MC_1, coli)
            Enc_2_coli                 = column(I_MC_2, coli)
            I_MCAK_SupP_Blue_1_coli    = column(I_MCAK_SupP_Blue_1, coli)
            I_MCAK_SupP_Blue_2_coli    = column(I_MCAK_SupP_Blue_2, coli)
            I_MCAK_SupP_Red__1_coli    = column(I_MCAK_SupP_Red__1, coli)
            I_MCAK_SupP_Red__2_coli    = column(I_MCAK_SupP_Red__2, coli)
            M_MCAK_SupP_Blue_1_coli    = column(M_MCAK_SupP_Blue_1, coli)
            M_MCAK_SupP_Blue_2_coli    = column(M_MCAK_SupP_Blue_2, coli)
            M_MCAK_SupP_Red__1_coli    = column(M_MCAK_SupP_Red__1, coli)
            M_MCAK_SupP_Red__2_coli    = column(M_MCAK_SupP_Red__2, coli)
            O_MCAK_SupP_Blue_1_coli    = column(O_MCAK_SupP_Blue_1, coli)
            O_MCAK_SupP_Blue_2_coli    = column(O_MCAK_SupP_Blue_2, coli)
            O_MCAK_SupP_Red__1_coli    = column(O_MCAK_SupP_Red__1, coli)
            O_MCAK_SupP_Red__2_coli    = column(O_MCAK_SupP_Red__2, coli)
            SK_I_MC_SupP_Blue_1_coli   = column(SK_I_MC_SupP_Blue_1, coli)
            SK_I_MC_SupP_Blue_2_coli   = column(SK_I_MC_SupP_Blue_2, coli)
            SK_I_MC_SupP_Red__1_coli   = column(SK_I_MC_SupP_Red__1, coli)
            SK_I_MC_SupP_Red__2_coli   = column(SK_I_MC_SupP_Red__2, coli)
            SK_SupP_Blue_1_coli        = column(SK_SupP_Blue_1, coli)
            SK_SupP_Blue_2_coli        = column(SK_SupP_Blue_2, coli)
            SK_SupP_Red__1_coli        = column(SK_SupP_Red__1, coli)
            SK_SupP_Red__2_coli        = column(SK_SupP_Red__2, coli)
            Enc_isWhite_coli           = column(Enc_isWhite, coli)
            EncSK_isWhite_coli         = column(EncSK_isWhite, coli)
            Enc_GuessBlue_coli         = column(Enc_GuessBlue, coli)
            Enc_GuessRed__coli         = column(Enc_GuessRed_, coli)
            Enc_GuessBoth_coli         = column(Enc_GuessBoth, coli)
            CD_AK_Blue_coli            = column(CD_AK_Blue, coli)
            CD_AK_Red__coli            = column(CD_AK_Red_, coli)
            #
            EncSK_SupP_Blue_OR__1_coli = column(EncSK_SupP_Blue_OR__1, coli)
            EncSK_SupP_Blue_OR__2_coli = column(EncSK_SupP_Blue_OR__2, coli)
            EncSK_SupP_Blue_AND_1_coli = column(EncSK_SupP_Blue_AND_1, coli)
            EncSK_SupP_Blue_AND_2_coli = column(EncSK_SupP_Blue_AND_2, coli)
            EncSK_SupP_Red__OR__1_coli = column(EncSK_SupP_Red__OR__1, coli)
            EncSK_SupP_Red__OR__2_coli = column(EncSK_SupP_Red__OR__2, coli)
            EncSK_SupP_Red__AND_1_coli = column(EncSK_SupP_Red__AND_1, coli)
            EncSK_SupP_Red__AND_2_coli = column(EncSK_SupP_Red__AND_2, coli)
            #
            if TWO_RULES == 1:
                AK_MC_Rule_coli = AK_MC_Rule[0]
            elif TWO_RULES == 2:
                AK_MC_Rule_coli = AK_MC_Rule[coli]
            else:
                AK_MC_Rule_coli = AK_MC_Rule[coli]
                if r >= self.ini_k:
                    constr = constr + [SK_G_CD_MC_Blue[coli] + ' + ' + SK_G_CD_MC_Red_[coli] + ' + ' + AK_MC_Rule_coli + ' >= 1']
                    constr = constr + [SK_G_CD_MC_Blue[coli] + ' + ' + SK_G_CD_MC_Red_[coli] + ' + ' + str(SumIOMC) + ' ' + AK_MC_Rule_coli + ' <= ' + str(SumIOMC)]
                else:
                    constr = constr + [SK_G_CD_MC_Blue[coli] + ' + ' + SK_G_CD_MC_Red_[coli] + ' - ' + AK_MC_Rule_coli + ' >= 0']
                    constr = constr + [SK_G_CD_MC_Blue[coli] + ' + ' + SK_G_CD_MC_Red_[coli] + ' - ' + str(SumIOMC) + ' ' + AK_MC_Rule_coli + ' <= ' + str(0)]
            #
            G_CD_MC_Blue_coli = G_CD_MC_Blue[coli]
            G_CD_MC_Red__coli = G_CD_MC_Red_[coli]
            # - AK-then-MC
            pre = AK_MC_Rule_coli + ' = 1 -> '
            if TWO_RULES == 2:
                G_CD_MC_Blue_coli = G_CD_MC_Blue_Rule1[coli]
                G_CD_MC_Red__coli = G_CD_MC_Red__Rule1[coli]
            for bi in range(RowN):
                constr = constr + self.Separate_without_Guess(
                    pre,
                    Enc_1_coli[bi],
                    Enc_2_coli[bi],
                    I_MCAK_SupP_Blue_1_coli[bi],
                    I_MCAK_SupP_Blue_2_coli[bi],
                    I_MCAK_SupP_Red__1_coli[bi],
                    I_MCAK_SupP_Red__2_coli[bi],
                    Enc_isWhite_coli[bi])
                constr = constr + self.ARK_with_Guess(
                    pre,
                    I_MCAK_SupP_Blue_1_coli[bi],
                    I_MCAK_SupP_Blue_2_coli[bi],
                    I_MCAK_SupP_Red__1_coli[bi],
                    I_MCAK_SupP_Red__2_coli[bi],
                    SK_I_MC_SupP_Blue_1_coli[bi],
                    SK_I_MC_SupP_Blue_2_coli[bi],
                    SK_I_MC_SupP_Red__1_coli[bi],
                    SK_I_MC_SupP_Red__2_coli[bi],
                    M_MCAK_SupP_Blue_1_coli[bi],
                    M_MCAK_SupP_Blue_2_coli[bi],
                    M_MCAK_SupP_Red__1_coli[bi],
                    M_MCAK_SupP_Red__2_coli[bi],
                    Enc_GuessBlue_coli[bi],
                    Enc_GuessRed__coli[bi],
                    Enc_GuessBoth_coli[bi],
                    CD_AK_Blue_coli[bi],
                    CD_AK_Red__coli[bi],
                    EncSK_isWhite_coli[bi],
                    EncSK_SupP_Blue_AND_1_coli[bi],
                    EncSK_SupP_Blue_AND_2_coli[bi],
                    EncSK_SupP_Blue_OR__1_coli[bi],
                    EncSK_SupP_Blue_OR__2_coli[bi],
                    EncSK_SupP_Red__AND_1_coli[bi],
                    EncSK_SupP_Red__AND_2_coli[bi],
                    EncSK_SupP_Red__OR__1_coli[bi],
                    EncSK_SupP_Red__OR__2_coli[bi])
            constr = constr + self.gensubConstraints_MC_SupP__Blue(
                pre,
                M_MCAK_SupP_Blue_1_coli,
                M_MCAK_SupP_Blue_2_coli,
                MC_SupP_Blue_ColExistWhite[coli],
                MC_SupP_Blue_ColAllGray[coli],
                O_MCAK_SupP_Blue_1_coli,
                O_MCAK_SupP_Blue_2_coli,
                G_SupP_Blue_SumGray[coli],
                G_CD_MC_Blue_coli)
            #
            constr = constr + self.gensubConstraints_MC_SupP__Red(
                pre,
                M_MCAK_SupP_Red__1_coli,
                M_MCAK_SupP_Red__2_coli,
                MC_SupP_Red__ColExistWhite[coli],
                MC_SupP_Red__ColAllGray[coli],
                O_MCAK_SupP_Red__1_coli,
                O_MCAK_SupP_Red__2_coli,
                G_SupP_Red__SumGray[coli],
                G_CD_MC_Red__coli)
            #
            # - MC-then-AK
            pre = AK_MC_Rule_coli + ' = 0 -> '
            if TWO_RULES == 2:
                G_CD_MC_Blue_coli = G_CD_MC_Blue_Rule0[coli]
                G_CD_MC_Red__coli = G_CD_MC_Red__Rule0[coli]
            for bi in range(RowN):
                constr = constr + self.Separate_with_Guess(
                    pre,
                    Enc_1_coli[bi],
                    Enc_2_coli[bi],
                    I_MCAK_SupP_Blue_1_coli[bi],
                    I_MCAK_SupP_Blue_2_coli[bi],
                    I_MCAK_SupP_Red__1_coli[bi],
                    I_MCAK_SupP_Red__2_coli[bi],
                    Enc_isWhite_coli[bi],
                    Enc_GuessBlue_coli[bi],
                    Enc_GuessRed__coli[bi],
                    Enc_GuessBoth_coli[bi])
            constr = constr + self.gensubConstraints_MC_SupP__Blue(
                pre,
                I_MCAK_SupP_Blue_1_coli,
                I_MCAK_SupP_Blue_2_coli,
                MC_SupP_Blue_ColExistWhite[coli],
                MC_SupP_Blue_ColAllGray[coli],
                M_MCAK_SupP_Blue_1_coli,
                M_MCAK_SupP_Blue_2_coli,
                G_SupP_Blue_SumGray[coli],
                G_CD_MC_Blue_coli)
            #
            constr = constr + self.gensubConstraints_MC_SupP__Red(
                pre,
                I_MCAK_SupP_Red__1_coli,
                I_MCAK_SupP_Red__2_coli,
                MC_SupP_Red__ColExistWhite[coli],
                MC_SupP_Red__ColAllGray[coli],
                M_MCAK_SupP_Red__1_coli,
                M_MCAK_SupP_Red__2_coli,
                G_SupP_Red__SumGray[coli],
                G_CD_MC_Red__coli)
            for bi in range(RowN):
                constr = constr + self.ARK_without_Guess(
                    pre,
                    M_MCAK_SupP_Blue_1_coli[bi],
                    M_MCAK_SupP_Blue_2_coli[bi],
                    M_MCAK_SupP_Red__1_coli[bi],
                    M_MCAK_SupP_Red__2_coli[bi],
                    SK_SupP_Blue_1_coli[bi],
                    SK_SupP_Blue_2_coli[bi],
                    SK_SupP_Red__1_coli[bi],
                    SK_SupP_Red__2_coli[bi],
                    O_MCAK_SupP_Blue_1_coli[bi],
                    O_MCAK_SupP_Blue_2_coli[bi],
                    O_MCAK_SupP_Red__1_coli[bi],
                    O_MCAK_SupP_Red__2_coli[bi],
                    CD_AK_Blue_coli[bi],
                    CD_AK_Red__coli[bi],
                    EncSK_isWhite_coli[bi],
                    EncSK_SupP_Blue_AND_1_coli[bi],
                    EncSK_SupP_Blue_AND_2_coli[bi],
                    EncSK_SupP_Blue_OR__1_coli[bi],
                    EncSK_SupP_Blue_OR__2_coli[bi],
                    EncSK_SupP_Red__AND_1_coli[bi],
                    EncSK_SupP_Red__AND_2_coli[bi],
                    EncSK_SupP_Red__OR__1_coli[bi],
                    EncSK_SupP_Red__OR__2_coli[bi])
            if TWO_RULES == 2:
                constr = constr + [G_CD_MC_Blue[coli] + ' - ' + G_CD_MC_Blue_Rule0[coli] + ' <= 0']
                constr = constr + [G_CD_MC_Blue[coli] + ' - ' + G_CD_MC_Blue_Rule1[coli] + ' <= 0']
                constr = constr + [G_CD_MC_Blue[coli] + ' - ' + G_CD_MC_Blue_Rule1[coli] + ' - ' + str(RowN) + ' ' +  AK_MC_Rule_coli + ' >= -' + str(RowN)]
                constr = constr + [G_CD_MC_Blue[coli] + ' - ' + G_CD_MC_Blue_Rule0[coli] + ' - ' + str(RowN) + ' ' +  AK_MC_Rule_coli + ' >= 0']
                constr = constr + [G_CD_MC_Red_[coli] + ' - ' + G_CD_MC_Red__Rule0[coli] + ' <= 0']
                constr = constr + [G_CD_MC_Red_[coli] + ' - ' + G_CD_MC_Red__Rule1[coli] + ' <= 0']
                constr = constr + [G_CD_MC_Red_[coli] + ' - ' + G_CD_MC_Red__Rule1[coli] + ' - ' + str(RowN) + ' ' +  AK_MC_Rule_coli + ' >= -' + str(RowN)]
                constr = constr + [G_CD_MC_Red_[coli] + ' - ' + G_CD_MC_Red__Rule0[coli] + ' - ' + str(RowN) + ' ' +  AK_MC_Rule_coli + ' >= 0']
        pre = ''
        for bi in range(MatN):
            constr = constr + MITMPreConstraints.Determine_Allone(pre, [O_MCAK_SupP_Blue_1[bi], O_MCAK_SupP_Red__1[bi]], O_SB_next_r_1[bi])
            constr = constr + MITMPreConstraints.Determine_Allone(pre, [O_MCAK_SupP_Blue_2[bi], O_MCAK_SupP_Red__2[bi]], O_SB_next_r_2[bi])
        if CD_BOTH == 0:
            for i in range(MatN):
                constr = constr + [CD_AK_Blue[i] + ' = 0']
            for i in range(ColN):
                constr = constr + [G_CD_MC_Blue[i] + ' = 0']
                constr = constr + [G_CD_MC_Blue_Rule1[i] + ' = 0']
                constr = constr + [G_CD_MC_Blue_Rule0[i] + ' = 0']
        return constr

    def genConstraints_of_backwardRound(self, r):
        if r < self.TR - 1            : 
            next_r                    = r + 1
        else                          : # the last round, next round the 0
            next_r                    = 0
        O_SB_1                     = Vars_generator.genVars_O_SB(r, 1)
        O_SB_2                     = Vars_generator.genVars_O_SB(r, 2)
        I_MC_1                     = Vars_generator.genVars_I_MC(r, 1)
        I_MC_2                     = Vars_generator.genVars_I_MC(r, 2)
        O_SB_next_r_1              = Vars_generator.genVars_O_SB(next_r, 1)
        O_SB_next_r_2              = Vars_generator.genVars_O_SB(next_r, 2)
        #
        I_MCAK_SupP_Blue_1         = Vars_generator.genVars_I_MCAK_SupP_Blue(r, 1)
        I_MCAK_SupP_Blue_2         = Vars_generator.genVars_I_MCAK_SupP_Blue(r, 2)
        I_MCAK_SupP_Red__1         = Vars_generator.genVars_I_MCAK_SupP_Red_(r, 1)
        I_MCAK_SupP_Red__2         = Vars_generator.genVars_I_MCAK_SupP_Red_(r, 2)
        O_MCAK_SupP_Blue_1         = Vars_generator.genVars_O_MCAK_SupP_Blue(r, 1)
        O_MCAK_SupP_Blue_2         = Vars_generator.genVars_O_MCAK_SupP_Blue(r, 2)
        O_MCAK_SupP_Red__1         = Vars_generator.genVars_O_MCAK_SupP_Red_(r, 1)
        O_MCAK_SupP_Red__2         = Vars_generator.genVars_O_MCAK_SupP_Red_(r, 2)
        M_MCAK_SupP_Blue_1         = Vars_generator.genVars_M_MCAK_SupP_Blue(r, 1)
        M_MCAK_SupP_Blue_2         = Vars_generator.genVars_M_MCAK_SupP_Blue(r, 2)
        M_MCAK_SupP_Red__1         = Vars_generator.genVars_M_MCAK_SupP_Red_(r, 1)
        M_MCAK_SupP_Red__2         = Vars_generator.genVars_M_MCAK_SupP_Red_(r, 2)
        #
        Enc_isWhite                = Vars_generator.genVars_Enc_isWhite(r)
        EncSK_isWhite              = Vars_generator.genVars_EncSK_isWhite(r)
        #
        Enc_GuessBlue              = Vars_generator.genVars_Enc_GuessBlue(r)
        Enc_GuessRed_              = Vars_generator.genVars_Enc_GuessRed_(r)
        Enc_GuessBoth              = Vars_generator.genVars_Enc_GuessBoth(r)
        CD_AK_Blue                 = Vars_generator.genVars_AK_ConsumedDeg_Blue(r)
        CD_AK_Red_                 = Vars_generator.genVars_AK_ConsumedDeg_Red_(r)
        #
        EncSK_SupP_Blue_OR__1      = Vars_generator.genVars_EncSK_SupP_Blue_OR_(r, 1)
        EncSK_SupP_Blue_OR__2      = Vars_generator.genVars_EncSK_SupP_Blue_OR_(r, 2)
        EncSK_SupP_Blue_AND_1      = Vars_generator.genVars_EncSK_SupP_Blue_AND(r, 1)
        EncSK_SupP_Blue_AND_2      = Vars_generator.genVars_EncSK_SupP_Blue_AND(r, 2)
        EncSK_SupP_Red__OR__1      = Vars_generator.genVars_EncSK_SupP_Red__OR_(r, 1)
        EncSK_SupP_Red__OR__2      = Vars_generator.genVars_EncSK_SupP_Red__OR_(r, 2)
        EncSK_SupP_Red__AND_1      = Vars_generator.genVars_EncSK_SupP_Red__AND(r, 1)
        EncSK_SupP_Red__AND_2      = Vars_generator.genVars_EncSK_SupP_Red__AND(r, 2)
        #
        MC_SupP_Blue_ColExistWhite = Vars_generator.genVars_MC_SupP_Blue_ColExistWhite(r)
        MC_SupP_Red__ColExistWhite = Vars_generator.genVars_MC_SupP_Red__ColExistWhite(r)
        MC_SupP_Blue_ColAllGray    = Vars_generator.genVars_MC_SupP_Blue_ColAllGray(r)
        MC_SupP_Red__ColAllGray    = Vars_generator.genVars_MC_SupP_Red__ColAllGray(r)
        G_SupP_Blue_SumGray        = Vars_generator.genVars_MC_SupP_Blue_SumGray(r)
        G_SupP_Red__SumGray        = Vars_generator.genVars_MC_SupP_Red__SumGray(r)
        G_CD_MC_Blue               = Vars_generator.genVars_MC_ConsumedDeg_Blue(r)
        G_CD_MC_Red_               = Vars_generator.genVars_MC_ConsumedDeg_Red_(r)
        G_CD_MC_Blue_Rule1         = Vars_generator.genVars_MC_ConsumedDeg_Blue_Rule1(r)
        G_CD_MC_Red__Rule1         = Vars_generator.genVars_MC_ConsumedDeg_Red__Rule1(r)
        G_CD_MC_Blue_Rule0         = Vars_generator.genVars_MC_ConsumedDeg_Blue_Rule0(r)
        G_CD_MC_Red__Rule0         = Vars_generator.genVars_MC_ConsumedDeg_Red__Rule0(r)
        #
        SK_I_MC_SupP_Blue_1        = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 1)
        SK_I_MC_SupP_Blue_2        = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 2)
        SK_I_MC_SupP_Red__1        = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 1)
        SK_I_MC_SupP_Red__2        = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 2)
        SK_SupP_Blue_1             = Vars_generator.genVars_SK_SupP_Blue(r, 1)
        SK_SupP_Blue_2             = Vars_generator.genVars_SK_SupP_Blue(r, 2)
        SK_SupP_Red__1             = Vars_generator.genVars_SK_SupP_Red_(r, 1)
        SK_SupP_Red__2             = Vars_generator.genVars_SK_SupP_Red_(r, 2)
        SK_G_CD_MC_Blue            = Vars_generator.genVars_SK_MC_ConsumedDeg_Blue(r)
        SK_G_CD_MC_Red_            = Vars_generator.genVars_SK_MC_ConsumedDeg_Red_(r)
        #
        AK_MC_Rule                 = Vars_generator.genVars_AK_MC_Rule(r)
        #
        constr = []
        # - Constraints for ShiftRows
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(O_SB_1), I_MC_1)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(O_SB_2), I_MC_2)
        # - Constraints for MixColumns and AddRoundKey
        for coli in range(ColN):
            Enc_1_coli                 = column(O_SB_next_r_1, coli)
            Enc_2_coli                 = column(O_SB_next_r_2, coli)
            O_MCAK_SupP_Blue_1_coli    = column(O_MCAK_SupP_Blue_1, coli)
            O_MCAK_SupP_Blue_2_coli    = column(O_MCAK_SupP_Blue_2, coli)
            O_MCAK_SupP_Red__1_coli    = column(O_MCAK_SupP_Red__1, coli)
            O_MCAK_SupP_Red__2_coli    = column(O_MCAK_SupP_Red__2, coli)
            M_MCAK_SupP_Blue_1_coli    = column(M_MCAK_SupP_Blue_1, coli)
            M_MCAK_SupP_Blue_2_coli    = column(M_MCAK_SupP_Blue_2, coli)
            M_MCAK_SupP_Red__1_coli    = column(M_MCAK_SupP_Red__1, coli)
            M_MCAK_SupP_Red__2_coli    = column(M_MCAK_SupP_Red__2, coli)
            I_MCAK_SupP_Blue_1_coli    = column(I_MCAK_SupP_Blue_1, coli)
            I_MCAK_SupP_Blue_2_coli    = column(I_MCAK_SupP_Blue_2, coli)
            I_MCAK_SupP_Red__1_coli    = column(I_MCAK_SupP_Red__1, coli)
            I_MCAK_SupP_Red__2_coli    = column(I_MCAK_SupP_Red__2, coli)
            SK_SupP_Blue_1_coli        = column(SK_SupP_Blue_1, coli)
            SK_SupP_Blue_2_coli        = column(SK_SupP_Blue_2, coli)
            SK_SupP_Red__1_coli        = column(SK_SupP_Red__1, coli)
            SK_SupP_Red__2_coli        = column(SK_SupP_Red__2, coli)
            SK_I_MC_SupP_Blue_1_coli   = column(SK_I_MC_SupP_Blue_1, coli)
            SK_I_MC_SupP_Blue_2_coli   = column(SK_I_MC_SupP_Blue_2, coli)
            SK_I_MC_SupP_Red__1_coli   = column(SK_I_MC_SupP_Red__1, coli)
            SK_I_MC_SupP_Red__2_coli   = column(SK_I_MC_SupP_Red__2, coli)
            Enc_isWhite_coli           = column(Enc_isWhite, coli)
            EncSK_isWhite_coli         = column(EncSK_isWhite, coli)
            Enc_GuessBlue_coli         = column(Enc_GuessBlue, coli)
            Enc_GuessRed__coli         = column(Enc_GuessRed_, coli)
            Enc_GuessBoth_coli         = column(Enc_GuessBoth, coli)
            CD_AK_Blue_coli            = column(CD_AK_Blue, coli)
            CD_AK_Red__coli            = column(CD_AK_Red_, coli)
            #
            EncSK_SupP_Blue_OR__1_coli = column(EncSK_SupP_Blue_OR__1, coli)
            EncSK_SupP_Blue_OR__2_coli = column(EncSK_SupP_Blue_OR__2, coli)
            EncSK_SupP_Blue_AND_1_coli = column(EncSK_SupP_Blue_AND_1, coli)
            EncSK_SupP_Blue_AND_2_coli = column(EncSK_SupP_Blue_AND_2, coli)
            EncSK_SupP_Red__OR__1_coli = column(EncSK_SupP_Red__OR__1, coli)
            EncSK_SupP_Red__OR__2_coli = column(EncSK_SupP_Red__OR__2, coli)
            EncSK_SupP_Red__AND_1_coli = column(EncSK_SupP_Red__AND_1, coli)
            EncSK_SupP_Red__AND_2_coli = column(EncSK_SupP_Red__AND_2, coli)
            #
            if TWO_RULES == 1:
                AK_MC_Rule_coli = AK_MC_Rule[0]
            elif TWO_RULES == 2:
                AK_MC_Rule_coli = AK_MC_Rule[coli]
            else:
                AK_MC_Rule_coli = AK_MC_Rule[coli]
                if r >= self.ini_k:
                    constr = constr + [SK_G_CD_MC_Blue[coli] + ' + ' + SK_G_CD_MC_Red_[coli] + ' - ' + AK_MC_Rule_coli + ' >= 0']
                    constr = constr + [SK_G_CD_MC_Blue[coli] + ' + ' + SK_G_CD_MC_Red_[coli] + ' - ' + str(SumIOMC) + ' ' + AK_MC_Rule_coli + ' <= ' + str(0)]
                else:
                    constr = constr + [SK_G_CD_MC_Blue[coli] + ' + ' + SK_G_CD_MC_Red_[coli] + ' + ' + AK_MC_Rule_coli + ' >= 1']
                    constr = constr + [SK_G_CD_MC_Blue[coli] + ' + ' + SK_G_CD_MC_Red_[coli] + ' + ' + str(SumIOMC) + ' ' + AK_MC_Rule_coli + ' <= ' + str(SumIOMC)]
            #
            G_CD_MC_Blue_coli = G_CD_MC_Blue[coli]
            G_CD_MC_Red__coli = G_CD_MC_Red_[coli]
            # - AK-then-MC
            pre = AK_MC_Rule_coli + ' = 1 -> '
            if TWO_RULES == 2:
                G_CD_MC_Blue_coli = G_CD_MC_Blue_Rule1[coli]
                G_CD_MC_Red__coli = G_CD_MC_Red__Rule1[coli]
            for bi in range(RowN):
                constr = constr + self.Separate_without_Guess(
                    pre,
                    Enc_1_coli[bi],
                    Enc_2_coli[bi],
                    O_MCAK_SupP_Blue_1_coli[bi],
                    O_MCAK_SupP_Blue_2_coli[bi],
                    O_MCAK_SupP_Red__1_coli[bi],
                    O_MCAK_SupP_Red__2_coli[bi],
                    Enc_isWhite_coli[bi])
                constr = constr + self.ARK_with_Guess(
                    pre,
                    O_MCAK_SupP_Blue_1_coli[bi],
                    O_MCAK_SupP_Blue_2_coli[bi],
                    O_MCAK_SupP_Red__1_coli[bi],
                    O_MCAK_SupP_Red__2_coli[bi],
                    SK_SupP_Blue_1_coli[bi],
                    SK_SupP_Blue_2_coli[bi],
                    SK_SupP_Red__1_coli[bi],
                    SK_SupP_Red__2_coli[bi],
                    M_MCAK_SupP_Blue_1_coli[bi],
                    M_MCAK_SupP_Blue_2_coli[bi],
                    M_MCAK_SupP_Red__1_coli[bi],
                    M_MCAK_SupP_Red__2_coli[bi],
                    Enc_GuessBlue_coli[bi],
                    Enc_GuessRed__coli[bi],
                    Enc_GuessBoth_coli[bi],
                    CD_AK_Blue_coli[bi],
                    CD_AK_Red__coli[bi],
                    EncSK_isWhite_coli[bi],
                    EncSK_SupP_Blue_AND_1_coli[bi],
                    EncSK_SupP_Blue_AND_2_coli[bi],
                    EncSK_SupP_Blue_OR__1_coli[bi],
                    EncSK_SupP_Blue_OR__2_coli[bi],
                    EncSK_SupP_Red__AND_1_coli[bi],
                    EncSK_SupP_Red__AND_2_coli[bi],
                    EncSK_SupP_Red__OR__1_coli[bi],
                    EncSK_SupP_Red__OR__2_coli[bi])
            constr = constr + self.gensubConstraints_MC_SupP__Blue(
                pre,
                M_MCAK_SupP_Blue_1_coli,
                M_MCAK_SupP_Blue_2_coli,
                MC_SupP_Blue_ColExistWhite[coli],
                MC_SupP_Blue_ColAllGray[coli],
                I_MCAK_SupP_Blue_1_coli,
                I_MCAK_SupP_Blue_2_coli,
                G_SupP_Blue_SumGray[coli],
                G_CD_MC_Blue_coli)
            #
            constr = constr + self.gensubConstraints_MC_SupP__Red(
                pre,
                M_MCAK_SupP_Red__1_coli,
                M_MCAK_SupP_Red__2_coli,
                MC_SupP_Red__ColExistWhite[coli],
                MC_SupP_Red__ColAllGray[coli],
                I_MCAK_SupP_Red__1_coli,
                I_MCAK_SupP_Red__2_coli,
                G_SupP_Red__SumGray[coli],
                G_CD_MC_Red__coli)
            #
            # - MC-then-AK
            pre = AK_MC_Rule_coli + ' = 0 -> '
            if TWO_RULES == 2:
                G_CD_MC_Blue_coli = G_CD_MC_Blue_Rule0[coli]
                G_CD_MC_Red__coli = G_CD_MC_Red__Rule0[coli]
            for bi in range(RowN):
                constr = constr + self.Separate_with_Guess(
                    pre,
                    Enc_1_coli[bi],
                    Enc_2_coli[bi],
                    O_MCAK_SupP_Blue_1_coli[bi],
                    O_MCAK_SupP_Blue_2_coli[bi],
                    O_MCAK_SupP_Red__1_coli[bi],
                    O_MCAK_SupP_Red__2_coli[bi],
                    Enc_isWhite_coli[bi],
                    Enc_GuessBlue_coli[bi],
                    Enc_GuessRed__coli[bi],
                    Enc_GuessBoth_coli[bi])
            constr = constr + self.gensubConstraints_MC_SupP__Blue(
                pre,
                O_MCAK_SupP_Blue_1_coli,
                O_MCAK_SupP_Blue_2_coli,
                MC_SupP_Blue_ColExistWhite[coli],
                MC_SupP_Blue_ColAllGray[coli],
                M_MCAK_SupP_Blue_1_coli,
                M_MCAK_SupP_Blue_2_coli,
                G_SupP_Blue_SumGray[coli],
                G_CD_MC_Blue_coli)
            #
            constr = constr + self.gensubConstraints_MC_SupP__Red(
                pre,
                O_MCAK_SupP_Red__1_coli,
                O_MCAK_SupP_Red__2_coli,
                MC_SupP_Red__ColExistWhite[coli],
                MC_SupP_Red__ColAllGray[coli],
                M_MCAK_SupP_Red__1_coli,
                M_MCAK_SupP_Red__2_coli,
                G_SupP_Red__SumGray[coli],
                G_CD_MC_Red__coli)
            for bi in range(RowN):
                constr = constr + self.ARK_without_Guess(
                    pre,
                    M_MCAK_SupP_Blue_1_coli[bi],
                    M_MCAK_SupP_Blue_2_coli[bi],
                    M_MCAK_SupP_Red__1_coli[bi],
                    M_MCAK_SupP_Red__2_coli[bi],
                    SK_I_MC_SupP_Blue_1_coli[bi],
                    SK_I_MC_SupP_Blue_2_coli[bi],
                    SK_I_MC_SupP_Red__1_coli[bi],
                    SK_I_MC_SupP_Red__2_coli[bi],
                    I_MCAK_SupP_Blue_1_coli[bi],
                    I_MCAK_SupP_Blue_2_coli[bi],
                    I_MCAK_SupP_Red__1_coli[bi],
                    I_MCAK_SupP_Red__2_coli[bi],
                    CD_AK_Blue_coli[bi],
                    CD_AK_Red__coli[bi],
                    EncSK_isWhite_coli[bi],
                    EncSK_SupP_Blue_AND_1_coli[bi],
                    EncSK_SupP_Blue_AND_2_coli[bi],
                    EncSK_SupP_Blue_OR__1_coli[bi],
                    EncSK_SupP_Blue_OR__2_coli[bi],
                    EncSK_SupP_Red__AND_1_coli[bi],
                    EncSK_SupP_Red__AND_2_coli[bi],
                    EncSK_SupP_Red__OR__1_coli[bi],
                    EncSK_SupP_Red__OR__2_coli[bi])
            if TWO_RULES == 2:
                constr = constr + [G_CD_MC_Blue[coli] + ' - ' + G_CD_MC_Blue_Rule0[coli] + ' <= 0']
                constr = constr + [G_CD_MC_Blue[coli] + ' - ' + G_CD_MC_Blue_Rule1[coli] + ' <= 0']
                constr = constr + [G_CD_MC_Blue[coli] + ' - ' + G_CD_MC_Blue_Rule1[coli] + ' - ' + str(RowN) + ' ' +  AK_MC_Rule_coli + ' >= -' + str(RowN)]
                constr = constr + [G_CD_MC_Blue[coli] + ' - ' + G_CD_MC_Blue_Rule0[coli] + ' - ' + str(RowN) + ' ' +  AK_MC_Rule_coli + ' >= 0']
                constr = constr + [G_CD_MC_Red_[coli] + ' - ' + G_CD_MC_Red__Rule0[coli] + ' <= 0']
                constr = constr + [G_CD_MC_Red_[coli] + ' - ' + G_CD_MC_Red__Rule1[coli] + ' <= 0']
                constr = constr + [G_CD_MC_Red_[coli] + ' - ' + G_CD_MC_Red__Rule1[coli] + ' - ' + str(RowN) + ' ' +  AK_MC_Rule_coli + ' >= -' + str(RowN)]
                constr = constr + [G_CD_MC_Red_[coli] + ' - ' + G_CD_MC_Red__Rule0[coli] + ' - ' + str(RowN) + ' ' +  AK_MC_Rule_coli + ' >= 0']
        pre = ''
        for bi in range(MatN):
            constr = constr + MITMPreConstraints.Determine_Allone(pre, [I_MCAK_SupP_Blue_1[bi], I_MCAK_SupP_Red__1[bi]], I_MC_1[bi])
            constr = constr + MITMPreConstraints.Determine_Allone(pre, [I_MCAK_SupP_Blue_2[bi], I_MCAK_SupP_Red__2[bi]], I_MC_2[bi])
        if CD_BOTH == 0:
            for i in range(MatN):
                constr = constr + [CD_AK_Red_[i] + ' = 0']
            for i in range(ColN):
                constr = constr + [G_CD_MC_Red_[i] + ' = 0']
                constr = constr + [G_CD_MC_Red__Rule1[i] + ' = 0']
                constr = constr + [G_CD_MC_Red__Rule0[i] + ' = 0']
        return constr

    def genConstraints_KeySchedule_forward(self, r):
        assert r <= self.TR
        SK_O_SB_1                     = Vars_generator.genVars_SK_O_SB(r, 1)
        SK_O_SB_2                     = Vars_generator.genVars_SK_O_SB(r, 2)
        SK_I_MC_1                     = Vars_generator.genVars_SK_I_MC(r, 1)
        SK_I_MC_2                     = Vars_generator.genVars_SK_I_MC(r, 2)
        #
        SK_I_MC_SupP_Blue_1           = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 1)
        SK_I_MC_SupP_Blue_2           = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 2)
        SK_I_MC_SupP_Red__1           = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 1)
        SK_I_MC_SupP_Red__2           = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 2)
        #
        SK_isWhite                    = Vars_generator.genVars_SK_isWhite(r)
        SK_GuessBlue                  = Vars_generator.genVars_SK_GuessBlue(r)
        SK_GuessRed_                  = Vars_generator.genVars_SK_GuessRed_(r)
        SK_GuessBoth                  = Vars_generator.genVars_SK_GuessBoth(r)
        #
        SK_MC_SupP_Blue_ColExistWhite = Vars_generator.genVars_SK_MC_SupP_Blue_ColExistWhite(r)
        SK_MC_SupP_Red__ColExistWhite = Vars_generator.genVars_SK_MC_SupP_Red__ColExistWhite(r)
        SK_MC_SupP_Blue_ColAllGray    = Vars_generator.genVars_SK_MC_SupP_Blue_ColAllGray(r)
        SK_MC_SupP_Red__ColAllGray    = Vars_generator.genVars_SK_MC_SupP_Red__ColAllGray(r)
        SK_G_SupP_Blue_SumGray        = Vars_generator.genVars_SK_MC_SupP_Blue_SumGray(r)
        SK_G_SupP_Red__SumGray        = Vars_generator.genVars_SK_MC_SupP_Red__SumGray(r)
        SK_G_CD_MC_Blue               = Vars_generator.genVars_SK_MC_ConsumedDeg_Blue(r)
        SK_G_CD_MC_Red_               = Vars_generator.genVars_SK_MC_ConsumedDeg_Red_(r)
        #
        SK_SupP_Blue_1                = Vars_generator.genVars_SK_SupP_Blue(r, 1)
        SK_SupP_Blue_2                = Vars_generator.genVars_SK_SupP_Blue(r, 2)
        SK_SupP_Red__1                = Vars_generator.genVars_SK_SupP_Red_(r, 1)
        SK_SupP_Red__2                = Vars_generator.genVars_SK_SupP_Red_(r, 2)
        SK_O_SB_next_r_1              = Vars_generator.genVars_SK_O_SB(r + 1, 1)
        SK_O_SB_next_r_2              = Vars_generator.genVars_SK_O_SB(r + 1, 2)
        #
        constr = []
        # - Constraints for ShiftRows
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(SK_O_SB_1), SK_I_MC_1)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(SK_O_SB_2), SK_I_MC_2)
        # - Constraints for MixColumns
        for coli in range(KSColN):
            SK_1_coli                = column(SK_I_MC_1, coli)
            SK_2_coli                = column(SK_I_MC_2, coli)
            SK_I_MC_SupP_Blue_1_coli = column(SK_I_MC_SupP_Blue_1, coli)
            SK_I_MC_SupP_Blue_2_coli = column(SK_I_MC_SupP_Blue_2, coli)
            SK_I_MC_SupP_Red__1_coli = column(SK_I_MC_SupP_Red__1, coli)
            SK_I_MC_SupP_Red__2_coli = column(SK_I_MC_SupP_Red__2, coli)
            SK_SupP_Blue_1_coli      = column(SK_SupP_Blue_1, coli)
            SK_SupP_Blue_2_coli      = column(SK_SupP_Blue_2, coli)
            SK_SupP_Red__1_coli      = column(SK_SupP_Red__1, coli)
            SK_SupP_Red__2_coli      = column(SK_SupP_Red__2, coli)
            SK_isWhite_coli          = column(SK_isWhite, coli)
            SK_GuessBlue_coli        = column(SK_GuessBlue, coli)
            SK_GuessRed__coli        = column(SK_GuessRed_, coli)
            SK_GuessBoth_coli        = column(SK_GuessBoth, coli)
            pre = ''
            for bi in range(KSRowN):
                if KS_GUESS == 1:
                    constr = constr + self.Separate_with_Guess(
                        pre,
                        SK_1_coli[bi],
                        SK_2_coli[bi],
                        SK_I_MC_SupP_Blue_1_coli[bi],
                        SK_I_MC_SupP_Blue_2_coli[bi],
                        SK_I_MC_SupP_Red__1_coli[bi],
                        SK_I_MC_SupP_Red__2_coli[bi],
                        SK_isWhite_coli[bi],
                        SK_GuessBlue_coli[bi],
                        SK_GuessRed__coli[bi],
                        SK_GuessBoth_coli[bi])
                else:
                    constr = constr + self.Separate_without_Guess(
                        pre,
                        SK_1_coli[bi],
                        SK_2_coli[bi],
                        SK_I_MC_SupP_Blue_1_coli[bi],
                        SK_I_MC_SupP_Blue_2_coli[bi],
                        SK_I_MC_SupP_Red__1_coli[bi],
                        SK_I_MC_SupP_Red__2_coli[bi],
                        SK_isWhite_coli[bi])
            constr = constr + self.gensubConstraints_MC_SupP__Blue(
                pre,
                SK_I_MC_SupP_Blue_1_coli,
                SK_I_MC_SupP_Blue_2_coli,
                SK_MC_SupP_Blue_ColExistWhite[coli],
                SK_MC_SupP_Blue_ColAllGray[coli],
                SK_SupP_Blue_1_coli,
                SK_SupP_Blue_2_coli,
                SK_G_SupP_Blue_SumGray[coli],
                SK_G_CD_MC_Blue[coli])
            #
            constr = constr + self.gensubConstraints_MC_SupP__Red(
                pre,
                SK_I_MC_SupP_Red__1_coli,
                SK_I_MC_SupP_Red__2_coli,
                SK_MC_SupP_Red__ColExistWhite[coli],
                SK_MC_SupP_Red__ColAllGray[coli],
                SK_SupP_Red__1_coli,
                SK_SupP_Red__2_coli,
                SK_G_SupP_Red__SumGray[coli],
                SK_G_CD_MC_Red_[coli])
        pre = ''
        for bi in range(KeyCellN):
            constr = constr + MITMPreConstraints.Determine_Allone(pre, [SK_SupP_Blue_1[bi], SK_SupP_Red__1[bi]], SK_O_SB_next_r_1[bi])
            constr = constr + MITMPreConstraints.Determine_Allone(pre, [SK_SupP_Blue_2[bi], SK_SupP_Red__2[bi]], SK_O_SB_next_r_2[bi])
        if CD_BOTH == 0:
            for i in range(ColN):
                constr = constr + [SK_G_CD_MC_Blue[i] + ' = 0']
        return constr

    def genConstraints_KeySchedule_backward(self, r):
        assert r <= self.TR
        SK_O_SB_1                     = Vars_generator.genVars_SK_O_SB(r, 1)
        SK_O_SB_2                     = Vars_generator.genVars_SK_O_SB(r, 2)
        SK_I_MC_1                     = Vars_generator.genVars_SK_I_MC(r, 1)
        SK_I_MC_2                     = Vars_generator.genVars_SK_I_MC(r, 2)
        #
        SK_I_MC_SupP_Blue_1           = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 1)
        SK_I_MC_SupP_Blue_2           = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 2)
        SK_I_MC_SupP_Red__1           = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 1)
        SK_I_MC_SupP_Red__2           = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 2)
        #
        SK_isWhite                    = Vars_generator.genVars_SK_isWhite(r)
        SK_GuessBlue                  = Vars_generator.genVars_SK_GuessBlue(r)
        SK_GuessRed_                  = Vars_generator.genVars_SK_GuessRed_(r)
        SK_GuessBoth                  = Vars_generator.genVars_SK_GuessBoth(r)
        #
        SK_MC_SupP_Blue_ColExistWhite = Vars_generator.genVars_SK_MC_SupP_Blue_ColExistWhite(r)
        SK_MC_SupP_Red__ColExistWhite = Vars_generator.genVars_SK_MC_SupP_Red__ColExistWhite(r)
        SK_MC_SupP_Blue_ColAllGray    = Vars_generator.genVars_SK_MC_SupP_Blue_ColAllGray(r)
        SK_MC_SupP_Red__ColAllGray    = Vars_generator.genVars_SK_MC_SupP_Red__ColAllGray(r)
        SK_G_SupP_Blue_SumGray        = Vars_generator.genVars_SK_MC_SupP_Blue_SumGray(r)
        SK_G_SupP_Red__SumGray        = Vars_generator.genVars_SK_MC_SupP_Red__SumGray(r)
        SK_G_CD_MC_Blue               = Vars_generator.genVars_SK_MC_ConsumedDeg_Blue(r)
        SK_G_CD_MC_Red_               = Vars_generator.genVars_SK_MC_ConsumedDeg_Red_(r)
        #
        SK_SupP_Blue_1                = Vars_generator.genVars_SK_SupP_Blue(r, 1)
        SK_SupP_Blue_2                = Vars_generator.genVars_SK_SupP_Blue(r, 2)
        SK_SupP_Red__1                = Vars_generator.genVars_SK_SupP_Red_(r, 1)
        SK_SupP_Red__2                = Vars_generator.genVars_SK_SupP_Red_(r, 2)
        SK_O_SB_next_r_1              = Vars_generator.genVars_SK_O_SB(r + 1, 1)
        SK_O_SB_next_r_2              = Vars_generator.genVars_SK_O_SB(r + 1, 2)
        #
        constr = []
        # - Constraints for ShiftRows
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(SK_O_SB_1), SK_I_MC_1)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(SK_O_SB_2), SK_I_MC_2)
        # - Constraints for MixColumns
        for coli in range(KSColN):
            SK_1_coli                = column(SK_O_SB_next_r_1, coli)
            SK_2_coli                = column(SK_O_SB_next_r_2, coli)
            SK_I_MC_SupP_Blue_1_coli = column(SK_I_MC_SupP_Blue_1, coli)
            SK_I_MC_SupP_Blue_2_coli = column(SK_I_MC_SupP_Blue_2, coli)
            SK_I_MC_SupP_Red__1_coli = column(SK_I_MC_SupP_Red__1, coli)
            SK_I_MC_SupP_Red__2_coli = column(SK_I_MC_SupP_Red__2, coli)
            SK_SupP_Blue_1_coli      = column(SK_SupP_Blue_1, coli)
            SK_SupP_Blue_2_coli      = column(SK_SupP_Blue_2, coli)
            SK_SupP_Red__1_coli      = column(SK_SupP_Red__1, coli)
            SK_SupP_Red__2_coli      = column(SK_SupP_Red__2, coli)
            SK_isWhite_coli          = column(SK_isWhite, coli)
            SK_GuessBlue_coli        = column(SK_GuessBlue, coli)
            SK_GuessRed__coli        = column(SK_GuessRed_, coli)
            SK_GuessBoth_coli        = column(SK_GuessBoth, coli)
            pre = ''
            for bi in range(KSRowN):
                if KS_GUESS == 1:
                    constr = constr + self.Separate_with_Guess(
                        pre,
                        SK_1_coli[bi],
                        SK_2_coli[bi],
                        SK_SupP_Blue_1_coli[bi],
                        SK_SupP_Blue_2_coli[bi],
                        SK_SupP_Red__1_coli[bi],
                        SK_SupP_Red__2_coli[bi],
                        SK_isWhite_coli[bi],
                        SK_GuessBlue_coli[bi],
                        SK_GuessRed__coli[bi],
                        SK_GuessBoth_coli[bi])
                else:
                    constr = constr + self.Separate_without_Guess(
                        pre,
                        SK_1_coli[bi],
                        SK_2_coli[bi],
                        SK_SupP_Blue_1_coli[bi],
                        SK_SupP_Blue_2_coli[bi],
                        SK_SupP_Red__1_coli[bi],
                        SK_SupP_Red__2_coli[bi],
                        SK_isWhite_coli[bi])                
            constr = constr + self.gensubConstraints_MC_SupP__Blue(
                pre,
                SK_SupP_Blue_1_coli,
                SK_SupP_Blue_2_coli,
                SK_MC_SupP_Blue_ColExistWhite[coli],
                SK_MC_SupP_Blue_ColAllGray[coli],
                SK_I_MC_SupP_Blue_1_coli,
                SK_I_MC_SupP_Blue_2_coli,
                SK_G_SupP_Blue_SumGray[coli],
                SK_G_CD_MC_Blue[coli])
            #
            constr = constr + self.gensubConstraints_MC_SupP__Red(
                pre,
                SK_SupP_Red__1_coli,
                SK_SupP_Red__2_coli,
                SK_MC_SupP_Red__ColExistWhite[coli],
                SK_MC_SupP_Red__ColAllGray[coli],
                SK_I_MC_SupP_Red__1_coli,
                SK_I_MC_SupP_Red__2_coli,
                SK_G_SupP_Red__SumGray[coli],
                SK_G_CD_MC_Red_[coli])
        pre = ''
        for bi in range(KeyCellN):
            constr = constr + MITMPreConstraints.Determine_Allone(pre, [SK_I_MC_SupP_Blue_1[bi], SK_I_MC_SupP_Red__1[bi]], SK_I_MC_1[bi])
            constr = constr + MITMPreConstraints.Determine_Allone(pre, [SK_I_MC_SupP_Blue_2[bi], SK_I_MC_SupP_Red__2[bi]], SK_I_MC_2[bi])
        if CD_BOTH == 0:
            for i in range(ColN):
                constr = constr + [SK_G_CD_MC_Red_[i] + ' = 0']
        return constr

    def genConstraints_ini_degree(self):
        O_SB_1    = Vars_generator.genVars_O_SB(self.ini_r, 1)
        O_SB_2    = Vars_generator.genVars_O_SB(self.ini_r, 2)
        SK_O_SB_1 = Vars_generator.genVars_SK_O_SB(self.ini_k, 1)
        SK_O_SB_2 = Vars_generator.genVars_SK_O_SB(self.ini_k, 2)
        #
        d1        = Vars_generator.genVars_degree_forward()
        d2        = Vars_generator.genVars_degree_backward()
        #
        d1_key    = Vars_generator.genVars_degree_forward_key()
        d2_key    = Vars_generator.genVars_degree_backward_key()
        #
        constr = []
        #
        for j in range(MatN):
            constr = constr + [O_SB_1[j] + ' + ' + O_SB_2[j] + ' >= 1']
            constr = constr + [d1[j] + ' + ' + O_SB_2[j] + ' = 1']
            constr = constr + [d2[j] + ' + ' + O_SB_1[j] + ' = 1']
        for j in range(KeyCellN):
            constr = constr + [SK_O_SB_1[j] + ' + ' + SK_O_SB_2[j] + ' >= 1']
            constr = constr + [d1_key[j] + ' + ' + SK_O_SB_2[j] + ' = 1']
            constr = constr + [d2_key[j] + ' + ' + SK_O_SB_1[j] + ' = 1']
        return constr

    def genConstraints_matching_round(self):
        r                          = self.mat_r
        if self.mat_r < self.TR - 1: 
            next_r                 = self.mat_r + 1
        else                       : 
            next_r                 = 0
        #
        O_SB_1               = Vars_generator.genVars_O_SB(r, 1)
        O_SB_2               = Vars_generator.genVars_O_SB(r, 2)
        I_MC_1               = Vars_generator.genVars_I_MC(r, 1)
        I_MC_2               = Vars_generator.genVars_I_MC(r, 2)
        O_SB_next_r_1        = Vars_generator.genVars_O_SB(next_r, 1)
        O_SB_next_r_2        = Vars_generator.genVars_O_SB(next_r, 2)
        #
        SK_I_MC_SupP_Blue_1  = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 1)
        SK_I_MC_SupP_Blue_2  = Vars_generator.genVars_SK_I_MC_SupP_Blue(r, 2)
        SK_I_MC_SupP_Red__1  = Vars_generator.genVars_SK_I_MC_SupP_Red_(r, 1)
        SK_SupP_Blue_1       = Vars_generator.genVars_SK_SupP_Blue(r, 1)
        SK_SupP_Blue_2       = Vars_generator.genVars_SK_SupP_Blue(r, 2)
        SK_SupP_Red__1       = Vars_generator.genVars_SK_SupP_Red_(r, 1)
        #
        Match_I_MC_Enc_White = Vars_generator.genVars_Match_I_MC_Enc_White(r)
        Match_O_MC_Enc_White = Vars_generator.genVars_Match_O_MC_Enc_White(r)
        Match_SK_White       = Vars_generator.genVars_Match_SK_White(r)
        #
        Match_EncOrSK_White  = Vars_generator.genVars_Match_EncOrSK_White(r)
        Match_EncSK_AND_1    = Vars_generator.genVars_Match_EncSK_AND(r, 1)
        Match_EncSK_AND_2    = Vars_generator.genVars_Match_EncSK_AND(r, 2)
        #
        Match_Exist_Blue     = Vars_generator.genVars_Match_Exist_Blue()
        Match_Exist_Red_     = Vars_generator.genVars_Match_Exist_Red_()
        Match_Exist_More     = Vars_generator.genVars_Match_Exist_More()
        Match_Exist_Filter   = Vars_generator.genVars_Match_Exist_Filter()
        G_Match_Counted      = Vars_generator.genVar_Match_Counted()
        #
        constr = []
        # - Constraints for ShiftRow
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(O_SB_1), I_MC_1)
        constr = constr + MITMPreConstraints.equalConstraints(ShiftRow(O_SB_2), I_MC_2)
        #
        pre = ''
        for bi in range(MatN):
            constr = constr + MITMPreConstraints.Determine_Allzero(pre, [I_MC_1[bi], I_MC_2[bi]], Match_I_MC_Enc_White[bi])
        for bi in range(MatN):
            constr = constr + MITMPreConstraints.Determine_Allzero(pre, [O_SB_next_r_1[bi], O_SB_next_r_2[bi]], Match_O_MC_Enc_White[bi])
        #
        if (self.mat_r + 1) <= self.ini_k: #use SK
            for bi in range(MatN):
                constr = constr + [pre + Match_SK_White[bi] + ' + ' + SK_SupP_Blue_1[bi] + ' = 1']
            for bi in range(MatN):
                constr = constr + MITMPreConstraints.Determine_ExistOne(pre, [Match_O_MC_Enc_White[bi], Match_SK_White[bi]], Match_EncOrSK_White[bi]) # White
            for bi in range(MatN):
                constr = constr + MITMPreConstraints.Determine_Allone(pre, [O_SB_next_r_1[bi], SK_SupP_Red__1[bi]], Match_EncSK_AND_1[bi]) # Blue or Gray
                constr = constr + MITMPreConstraints.Determine_Allone(pre, [O_SB_next_r_2[bi], SK_SupP_Blue_2[bi]], Match_EncSK_AND_2[bi]) # Red or Gray
            for coli in range(ColN):
                I_MC_1_coli               = column(I_MC_1, coli)
                I_MC_2_coli               = column(I_MC_2, coli)
                Match_I_MC_Enc_White_coli = column(Match_I_MC_Enc_White, coli)
                Match_EncOrSK_White_coli  = column(Match_EncOrSK_White, coli)
                Match_EncSK_AND_1_coli    = column(Match_EncSK_AND_1, coli)
                Match_EncSK_AND_2_coli    = column(Match_EncSK_AND_2, coli)
                constr = constr + [str(RowN + 1) + ' ' + Match_Exist_More[coli] + 
                ' + ' + BasicTools._plusTerms(Match_EncOrSK_White_coli + Match_I_MC_Enc_White_coli) + ' <= ' + str(SumIOMC)]
                constr = constr + [str(RowN) + ' ' + Match_Exist_More[coli] + 
                ' + ' + BasicTools._plusTerms(Match_EncOrSK_White_coli + Match_I_MC_Enc_White_coli) + ' >= ' + str(RowN)]
                constr = constr + [Match_Exist_More[coli] + ' = 1 -> ' + G_Match_Counted[coli] + ' + ' + BasicTools._plusTerms(Match_EncOrSK_White_coli + Match_I_MC_Enc_White_coli) + ' = ' + str(RowN)]
                constr = constr + [Match_Exist_More[coli] + ' = 0 -> ' + G_Match_Counted[coli] + ' = 0']

        else: ## if (self.mat_r + 1) > self.ini_k, use SK_I_MC
            for bi in range(MatN):
                constr = constr + [pre + Match_SK_White[bi] + ' + ' + SK_I_MC_SupP_Blue_1[bi] + ' = 1']
            for bi in range(MatN):
                constr = constr + MITMPreConstraints.Determine_ExistOne(pre, [Match_I_MC_Enc_White[bi], Match_SK_White[bi]], Match_EncOrSK_White[bi]) # White
            for bi in range(MatN):
                constr = constr + MITMPreConstraints.Determine_Allone(pre, [I_MC_1[bi], SK_I_MC_SupP_Red__1[bi]], Match_EncSK_AND_1[bi]) # Blue or Gray
                constr = constr + MITMPreConstraints.Determine_Allone(pre, [I_MC_2[bi], SK_I_MC_SupP_Blue_2[bi]], Match_EncSK_AND_2[bi]) # Red or Gray
            for coli in range(ColN):
                O_MC_1_coli               = column(O_SB_next_r_1, coli)
                O_MC_2_coli               = column(O_SB_next_r_2, coli)
                Match_O_MC_Enc_White_coli = column(Match_O_MC_Enc_White, coli)
                Match_EncOrSK_White_coli  = column(Match_EncOrSK_White, coli)
                Match_EncSK_AND_1_coli    = column(Match_EncSK_AND_1, coli)
                Match_EncSK_AND_2_coli    = column(Match_EncSK_AND_2, coli)
                constr = constr + [str(RowN + 1) + ' ' + Match_Exist_More[coli] + 
                ' + ' + BasicTools._plusTerms(Match_EncOrSK_White_coli + Match_O_MC_Enc_White_coli) + ' <= ' + str(SumIOMC)]
                constr = constr + [str(RowN) + ' ' + Match_Exist_More[coli] + 
                ' + ' + BasicTools._plusTerms(Match_EncOrSK_White_coli + Match_O_MC_Enc_White_coli) + ' >= ' + str(RowN)]
                constr = constr + [Match_Exist_More[coli] + ' = 1 -> ' + G_Match_Counted[coli] + ' + ' + BasicTools._plusTerms(Match_EncOrSK_White_coli + Match_O_MC_Enc_White_coli) + ' = ' + str(RowN)]
                constr = constr + [Match_Exist_More[coli] + ' = 0 -> ' + G_Match_Counted[coli] + ' = 0']
        return constr

    def genConstraints_additional(self):
        constr      = []
        CD_Blue     = []
        CD_Red      = []
        CD_Blue_KAD = []
        CD_Red_KAD  = []
        for r in range(0, self.TR):
            if r != self.mat_r:
                CD_Blue = CD_Blue + Vars_generator.genVars_MC_ConsumedDeg_Blue(r)
                CD_Red = CD_Red + Vars_generator.genVars_MC_ConsumedDeg_Red_(r)
                CD_Blue_KAD = CD_Blue_KAD + Vars_generator.genVars_AK_ConsumedDeg_Blue(r)
                CD_Red_KAD = CD_Red_KAD + Vars_generator.genVars_AK_ConsumedDeg_Red_(r)
        CD_Blue_KS = []
        CD_Red_KS  = []
        for r in range(0, self.TR):
            CD_Blue_KS = CD_Blue_KS + Vars_generator.genVars_SK_MC_ConsumedDeg_Blue(r)
            CD_Red_KS = CD_Red_KS + Vars_generator.genVars_SK_MC_ConsumedDeg_Red_(r)
        Wg_Blue_KS = []
        Wg_Red_KS  = []
        Wg_Both_KS = []
        if KS_GUESS == 1:
            for r in range(0, self.TR):
                Wg_Blue_KS = Wg_Blue_KS + Vars_generator.genVars_SK_GuessBlue(r)
                Wg_Red_KS = Wg_Red_KS + Vars_generator.genVars_SK_GuessRed_(r)
                Wg_Both_KS = Wg_Both_KS + Vars_generator.genVars_SK_GuessBoth(r)
        Wg_Blue = []
        Wg_Red  = []
        Wg_Both = []
        for r in range(0, self.TR):
            if r != self.mat_r:
                Wg_Blue = Wg_Blue + Vars_generator.genVars_Enc_GuessBlue(r)
                Wg_Red = Wg_Red + Vars_generator.genVars_Enc_GuessRed_(r)
                Wg_Both = Wg_Both + Vars_generator.genVars_Enc_GuessBoth(r)
        Wg_Blue = Wg_Blue + Wg_Blue_KS
        Wg_Red = Wg_Red + Wg_Red_KS
        Wg_Both = Wg_Both + Wg_Both_KS

        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()

        d1_key = Vars_generator.genVars_degree_forward_key()
        d2_key = Vars_generator.genVars_degree_backward_key()

        Deg1 = 'GDeg1'
        Deg2 = 'GDeg2'

        if len(CD_Blue + CD_Blue_KAD + CD_Blue_KS + Wg_Red) > 0:
            constr = constr + [Deg1 + ' - ' + BasicTools.minusTerms(d1 + d1_key) + ' + ' + BasicTools._plusTerms(CD_Blue + CD_Blue_KAD + CD_Blue_KS + Wg_Red) + ' = 0']
        else:
            constr = constr + [Deg1 + ' - ' + BasicTools.minusTerms(d1 + d1_key) + ' = 0']

        if len(CD_Red + CD_Red_KAD + CD_Red_KS + Wg_Blue) > 0:
            constr = constr + [Deg2 + ' - ' + BasicTools.minusTerms(d2 + d2_key) + ' + ' + BasicTools._plusTerms(CD_Red + CD_Red_KAD + CD_Red_KS + Wg_Blue) + ' = 0']
        else:
            constr = constr + [Deg2 + ' - ' + BasicTools.minusTerms(d2 + d2_key) + ' = 0']

        constr = constr + [Deg1 + ' >= 1']
        constr = constr + [Deg2 + ' >= 1']

        G_Match_Counted = Vars_generator.genVar_Match_Counted()
        GM = 'GMat'
        constr = constr + [GM + ' - ' + BasicTools.minusTerms(G_Match_Counted) + ' + ' + BasicTools._plusTerms(Wg_Red + Wg_Blue + Wg_Both) + ' = 0']
        constr = constr + [GM + ' >= 1']

        return [constr, Deg1, Deg2, GM]

    def genConstraints_total(self):
        constr = []

        # State
        if self.mat_r < self.ini_r:
            for r in range(self.ini_r, self.TR):
                constr = constr + self.genConstraints_of_forwardRound(r)

            for r in range(0, self.mat_r):
                constr = constr + self.genConstraints_of_forwardRound(r)

            constr = constr + self.genConstraints_matching_round()

            for r in range(self.mat_r + 1, self.ini_r):
                constr = constr + self.genConstraints_of_backwardRound(r)

        if self.mat_r > self.ini_r:
            for r in range(self.ini_r, self.mat_r):
                constr = constr + self.genConstraints_of_forwardRound(r)

            constr = constr + self.genConstraints_matching_round()

            for r in range(self.mat_r + 1, self.TR):
                constr = constr + self.genConstraints_of_backwardRound(r)

            for r in range(0, self.ini_r):
                constr = constr + self.genConstraints_of_backwardRound(r)

        # KeySchedule
        for r in range(0, self.ini_k):
            constr = constr + self.genConstraints_KeySchedule_backward(r)
        for r in range(self.ini_k, self.TR + 1):
            constr = constr + self.genConstraints_KeySchedule_forward(r)

        # Degree
        constr = constr + self.genConstraints_ini_degree()

        # Matching and Additional
        constr = constr + self.genConstraints_additional()[0]

        return constr

    def genModel(self, filename):
        V = set([])
        constr = list([])
        constr = constr + self.genConstraints_total()
        V = BasicTools.getVariables_From_Constraints(constr)
        fid = open(filename + '.lp', 'w')
        fid.write('Maximize' + '\n')
        constr = constr + ['GObj - GDeg1 <= 0']
        constr = constr + ['GObj - GDeg2 <= 0']
        constr = constr + ['GObj - GMat <= 0']
        fid.write('GObj' + '\n')
        '''
        if self.ini_r < self.mat_r:
            constr = constr + ['GDeg1 - GDeg2 >= 0']
            constr = constr + ['GMat - GDeg2 >= 0']
        else:
            constr = constr + ['GDeg2 - GDeg1 >= 0']
            constr = constr + ['GMat - GDeg1 >= 0']
        if self.ini_r < self.mat_r:
            fid.write('GDeg2' + '\n')
        else:
            fid.write('GDeg1' + '\n')
        '''
        fid.write('\n')
        fid.write('Subject To')
        fid.write('\n')
        for c in constr:
            fid.write(c)
            fid.write('\n')
        GV = []
        BV = []
        for v in V:
            if v[0] == 'G':
                GV.append(v)
            else:
                BV.append(v)
        fid.write('Binary' + '\n')
        for bv in BV:
            fid.write(bv + '\n')
        fid.write('Generals' + '\n')
        for gv in GV:
            fid.write(gv + '\n')
        fid.close()

def cmd(fpath, TotalRound, InitRound, InitKRound, MatchRound):
    for TR in range(int(TotalRound), int(TotalRound)+1):
        resultf = open(fpath + '/Result_r' + str(TR) + '.txt', 'w+')
        resultf.write('%6s, %6s, %6s, %6s: %6s (%6s, %6s, %6s); %10s secs\n' %
                     ('TR', 'ini_r', 'ini_k', 'mat_r', 'Obj', 'DoF1', 'DoF2', 'DoM', 'Time'))
        best = 0
        start = time.time()
        mat_start = int(MatchRound)
        matr_list = [(mat_start+i)%TR for i in range(TR)]
        init_start = int(InitRound)
        initr_list = [(init_start+i)%TR for i in range(TR)]
        initk_start = int(InitKRound)
        initrk_list = [(initk_start+i)%TR for i in range(TR)]
        for mat_r in matr_list:
            for ini_r in initr_list:
                for ini_k in initrk_list:
                    if mat_r != ini_r:
                        startt = time.time()
                        filename = 'TR' + str(TR) + '_ini' + str(ini_r) + '_inikr' + str(ini_k) + '_matr' + str(mat_r)
                        A = Constraints_generator_(TR, ini_r, ini_k, mat_r)
                        A.genModel(fpath + filename)
                        Model = read(fpath + filename + '.lp')
                        Model.setParam(GRB.Param.SolFiles, fpath + filename + '_all')
                        Model.setParam(GRB.Param.Threads, 8)
                        Model.optimize()
                        elapsedt = (time.time() - startt)
                        if Model.SolCount > 0:
                            Model.write(fpath + filename + '.sol')
                            solFile = open(fpath + filename + '.sol', 'r')
                            Sol = dict()
                            for line in solFile:
                                if line[0] != '#':
                                    temp = line
                                    temp = temp.split()
                                    Sol[temp[0]] = round(float(temp[1]))
                            DoF1 = Sol['GDeg1']
                            DoF2 = Sol['GDeg2']
                            DoM  = Sol['GMat']
                            Obj = math.min(DoF1,DoF2,DoM)
                            if Obj > best:
                                best = Obj
                            resultf.write('%6d, %6d, %6d, %6d: %6d (%6d, %6d, %6d); %10f secs\n' % 
                                            (TR, ini_r, ini_k, mat_r, Obj, DoF1, DoF2, DoM, elapsedt))
                            resultf.flush()
                        else:
                            resultf.write('%6d, %6d, %6d, %6d: %6s (%6s, %6s, %6s); %10f secs\n' % 
                                    (TR, ini_r, ini_k, mat_r, '-', '-', '-', '-', elapsedt))
                            resultf.flush()
        elapsed = (time.time() - start)
        resultf.write('Best Obj: ' + str(best) + '\n')
        resultf.write('Total time (secs): ' + str(elapsed) + '\n')
        resultf.close()

if __name__ == "__main__":
    cmd(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
