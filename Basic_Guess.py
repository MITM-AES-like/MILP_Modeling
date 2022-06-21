from abc import ABCMeta, abstractmethod
from functools import reduce
import math
import random

#from WhirlpoolParameters_small import *
from WhirlpoolParameters_real import *
#from WhirlpoolParameters_half import *

class BasicTools:

    @staticmethod
    def _plusTerms(in_vars):
        """
        >>> BasicTools._plusTerms(['x', 'y', 'z'])
        'x + y + z'
        >>> BasicTools._plusTerms(['x', 'y'])
        'x + y'
        >>> BasicTools._plusTerms(['x', 'y', 'z', 'a', 'b'])
        'x + y + z + a + b'
        >>>
        """
        t = ''
        for v in in_vars:
            t = t + v + ' + '
        return t[0:-3]

    @staticmethod
    def _combTerms(in_vars, op):
        """
        >>> BasicTools._combTerms(['x', 'y', 'z'])
        'x op y op z'
        >>> BasicTools._combTerms(['x', 'y'])
        'x op y'
        >>> BasicTools._combTerms(['x', 'y', 'z', 'a', 'b'])
        'x op y op z op a op b'
        >>>
        """
        t = ''
        for v in in_vars:
            t = t + v + op
        return t[0:-3]

    @staticmethod
    def minusTerms(in_vars):
        """
        >>> BasicTools.minusTerms(['x', 'y', 'z'])
        'x - y - z'
        >>> BasicTools.minusTerms(['x', 'y'])
        'x - y'
        >>> BasicTools.minusTerms(['x', 'y', 'z', 'a', 'b'])
        'x - y - z - a - b'
        >>>
        """
        t = ''
        for v in in_vars:
            t = t + v + ' - '
        return t[0:-3]

    @staticmethod
    def getVariables_From_Constraints(C):
        V = set([])
        for s in C:
            temp = s.strip()
            temp = temp.replace(' + ', '   ')
            temp = temp.replace(' - ', '   ')
            temp = temp.replace(' >= ', '   ')
            temp = temp.replace(' <= ', '   ')
            temp = temp.replace(' = ', '   ')
            temp = temp.replace(' -> ', '   ')
            temp = temp.replace(' AND ', '     ')
            temp = temp.replace(' OR ', '    ')
            temp = temp.replace(' MAX ', '     ')
            temp = temp.replace(' MIN ', '     ')
            temp = temp.replace(' , ', '   ')
            temp = temp.replace(' ( ', '   ')
            temp = temp.replace(' ) ', '   ')
            temp = temp.split()
            for v in temp:
                if not v.lstrip('-').isdecimal():
                    V.add(v)
        return V

    @staticmethod
    def AND(pre, V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [pre + V_out + ' - ' + BasicTools.minusTerms(V_in) + ' >= ' + str(1-m)]
        constr = constr + [pre + BasicTools._plusTerms(V_in) + ' - ' + str(m) + ' ' + V_out + ' >= 0']
        return constr

    @staticmethod
    def OR_(pre, V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [pre + str(m) + ' ' + V_out + ' - ' + BasicTools.minusTerms(V_in) + ' >= 0']
        constr = constr + [pre + V_out + ' - ' + BasicTools.minusTerms(V_in) + ' <= 0']
        return constr

    @staticmethod
    def N_AND(pre, V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [pre + V_out + ' + ' + BasicTools._plusTerms(V_in) + ' <= ' + str(m)]
        constr = constr + [pre + BasicTools._plusTerms(V_in) + ' + ' + str(m) + ' ' + V_out + ' >= ' + str(m)]
        return constr

    @staticmethod
    def N_OR_(pre, V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [pre + V_out + ' + ' + BasicTools._plusTerms(V_in) + ' >= 1']
        for j in range(m):
            constr = constr + [pre + V_in[j] + ' + ' + V_out + ' <= 1']
        return constr


class MITMPreConstraints:
    @staticmethod
    def Consume_degree(pre, Allone, V, cd): # Allone, V, cd are all binary in {0, 1}
        constr = []
        constr = constr + [pre + cd + ' - ' + V + ' <= 0']
        constr = constr + [pre + cd + ' - ' + V + ' + ' + Allone + ' >= 0']
        constr = constr + [pre + cd + ' + ' + V + ' + ' + Allone + ' <= 2']
        return constr

    @staticmethod
    def Determine_Allone(pre, V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [pre + V_out + ' - ' + BasicTools.minusTerms(V_in) + ' >= ' + str(1-m)]
        constr = constr + [pre + BasicTools._plusTerms(V_in) + ' - ' + str(m) + ' ' + V_out + ' >= 0']
        return constr

    @staticmethod
    def Determine_ExistZero(pre, V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [pre + V_out + ' + ' + BasicTools._plusTerms(V_in) + ' <= ' + str(m)]
        constr = constr + [pre + BasicTools._plusTerms(V_in) + ' + ' + str(m) + ' ' + V_out + ' >= ' + str(m)]
        return constr

    @staticmethod
    def Determine_Allzero(pre, V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [pre + V_out + ' + ' + BasicTools._plusTerms(V_in) + ' >= 1']
        for j in range(m):
            constr = constr + [pre + V_in[j] + ' + ' + V_out + ' <= 1']
        return constr

    @staticmethod
    def Determine_ExistOne(pre, V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [pre + str(m) + ' ' + V_out + ' - ' + BasicTools.minusTerms(V_in) + ' >= 0']
        constr = constr + [pre + V_out + ' - ' + BasicTools.minusTerms(V_in) + ' <= 0']
        return constr


    @staticmethod
    def XOR_Mat(
        pre,
        input1,
        input2,
        sk1,
        sk2,
        output1,
        output2,
        AZ):
        constr = []
        constr = constr + MITMPreConstraints.Determine_Allzero(pre, [sk1, sk2], AZ)
        constr = constr + [pre + input1 + ' - ' + output1 + ' >= 0']
        constr = constr + [pre + input2 + ' - ' + output2 + ' >= 0']
        constr = constr + [pre + AZ + ' - ' + input1 + ' + ' + output1 + ' >= 0']
        constr = constr + [pre + AZ + ' - ' + input2 + ' + ' + output2 + ' >= 0']
        constr = constr + [pre + output1 + ' + ' + AZ + ' <= 1']
        constr = constr + [pre + output2 + ' + ' + AZ + ' <= 1']
        return constr

    @staticmethod
    def OR_backward(
        pre,
        input1,
        input2,
        input1_MC_KAD,
        input2_MC_KAD,
        output):
        constr = []
        constr = constr + [pre + input1_MC_KAD + ' - ' + input2 + ' - ' + output + ' >= -1']
        constr = constr + [pre + input1 + ' + ' + input1_MC_KAD + ' - ' + output + ' >= 0']
        constr = constr + [pre + input1 + ' - ' + input2_MC_KAD + ' - ' + output + ' >= -1']
        constr = constr + [pre + ' - ' + input1 + ' + ' + input2 + ' + ' + output + ' >= 0']
        constr = constr + [pre + ' - ' + input1_MC_KAD + ' + ' + input2_MC_KAD + ' + ' + output + ' >= 0']
        constr = constr + [pre + ' - ' + input2 + ' - ' + input2_MC_KAD + ' - ' + output + ' >= -2']
        return constr

    @staticmethod
    def XOR_forward(
        pre,
        V1_in,
        V2_in,
        V1_out,
        V2_out,
        Allone1,
        Allone2,
        Allzero1,
        Consume):
        constr = []
        constr = constr + [pre + Consume + ' + ' + Allone1 + ' - ' + V1_out + ' = 0']
        constr = constr + [pre + V2_out + ' - ' + Allone2 + ' = 0']
        constr = constr + [pre + Allone1 + ' + ' + Allone2 + ' - ' + V1_out + ' >= 0']
        constr = constr + [pre + V1_out + ' - ' + Allone1 + ' >= 0']
        constr = constr + [pre + Allone1 + ' + ' + Allzero1 + ' - ' + V1_out + ' >= 0']
        constr = constr + MITMPreConstraints.Determine_Allone(pre, V1_in, Allone1)
        constr = constr + MITMPreConstraints.Determine_Allone(pre, V2_in, Allone2)
        constr = constr + MITMPreConstraints.Determine_Allzero(pre, V1_in, Allzero1)
        return constr

    @staticmethod
    def XOR_backward(
        pre,
        V1_in,
        V2_in,
        V1_out,
        V2_out,
        Allone1,
        Allone2,
        Allzero2,
        Consume):
        constr = []
        constr = constr + [pre + Consume + ' + ' + Allone2 + ' - ' + V2_out + ' = 0']
        constr = constr + [pre + V1_out + ' - ' + Allone1 + ' = 0']
        constr = constr + [pre + Allone1 + ' + ' + Allone2 + ' - ' + V2_out + ' >= 0']
        constr = constr + [pre + V2_out + ' - ' + Allone2 + ' >= 0']
        constr = constr + [pre + Allone2 + ' + ' + Allzero2 + ' - ' + V2_out + ' >= 0']
        constr = constr + MITMPreConstraints.Determine_Allone(pre, V1_in, Allone1)
        constr = constr + MITMPreConstraints.Determine_Allone(pre, V2_in, Allone2)
        constr = constr + MITMPreConstraints.Determine_Allzero(pre, V2_in, Allzero2)
        return constr

    @staticmethod
    def gensubConstraints_ifguess_backward(
        pre,
        input1,
        input2,
        out1,
        out2,
        wg):
        constr = []
        constr = constr + [pre + wg + ' - ' + out2 + ' + ' + input2 + ' = 0']
        constr = constr + [pre + wg + ' + ' + input1 + ' <= 1']
        constr = constr + [pre + out1 + ' - ' + input1 + ' = 0']
        return constr

    @staticmethod
    def gensubConstraints_ifguess_forward(
        pre,
        input1,
        input2,
        out1,
        out2,
        wg):
        return MITMPreConstraints.gensubConstraints_ifguess_backward(
            pre,
            input2,
            input1,
            out2,
            out1,
            wg)


    @staticmethod
    def equalConstraints(x, y):
        assert len(x) == len(y)
        c = []
        for i in range(0, len(x)):
            c = c + [x[i] + ' - ' + y[i] + ' = 0']
        return c

    @staticmethod
    def PermConstraints(Perm, x, y): # x[j] to y[Perm[j]]
        assert len(x) == len(y)
        c = []
        for i in range(0, len(x)):
            c = c + [x[i] + ' - ' + y[Perm[i]] + ' = 0']
        return c



# A[ 0], A[ 1], A[ 2], A[ 3], 
# A[ 4], A[ 5], A[ 6], A[ 7], 
# A[ 8], A[ 9], A[10], A[11], 
# A[12], A[13], A[14], A[15], 
def column(A, j):
    return [A[j + ColN * i] for i in range(RowN)]

# A[ 0], A[ 1], A[ 2], A[ 3], A[ 4], A[ 5], 
# A[ 6], A[ 7], A[ 8], A[ 9], A[10], A[11], 
# A[12], A[13], A[14], A[15], A[16], A[17], 
# A[18], A[19], A[20], A[21], A[22], A[23]
def column_KS(A, j):
    return [A[j + (KSColN * i)] for i in range(KSRowN)]

def ShiftRow(A):
    return [A[(ColN * j) + ((i + j) % ColN)] for j in range(RowN) for i in range(ColN)]

def ShiftRow_AES(A):
    return [A[ 0], A[ 1], A[ 2], A[ 3], \
            A[ 5], A[ 6], A[ 7], A[ 4], \
            A[10], A[11], A[ 8], A[ 9], \
            A[15], A[12], A[13], A[14]]

def prettyPrint(A):
    for i in range(RowN):
        print(A[i*ColN:(i+1)*ColN])
    print('\n')

def prettyPrintAES(A):
    print(A[0:4])
    print(A[4:8])
    print(A[8:12])
    print(A[12:16])
    print('\n')

def main():
    pass

if __name__ == '__main__':
    main()