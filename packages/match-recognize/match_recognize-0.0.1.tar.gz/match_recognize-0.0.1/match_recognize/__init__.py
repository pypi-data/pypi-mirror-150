import numpy as np
import pandas as pd
import operator
import warnings
warnings.filterwarnings('ignore')
from automata.fa.nfa import NFA


class match_recognize:
    
    def partition_handling(text):
        start = "PARTITION BY "
        end = "\n"
        grouping = txt[txt.find(start)+len(start):txt.rfind(end)].split('\n')[0]
        grouping_list = grouping.split(",")
        grouping_list = [i.strip() for i in grouping_list]
        return grouping_list
    
    def order_handling(text):
        start = "ORDER BY "
        end = "\n"
        ordering = txt[txt.find(start)+len(start):txt.rfind(end)].split('\n')[0]
        ordering_list = ordering.split(",")
        ordering_list = [i.strip() for i in ordering_list]
        return ordering_list
    
    def define_handling(text):
        start = "DEFINE"
        end = ")"
        txt = text[text.find(start)+len(start):text.rfind(end)]
        txt = txt.replace("\n", "")
        txt = txt.replace("   ", "")
        txt = txt.replace("  ", "")
        txt = txt.replace("\t", "")
        txt_list = txt.split(",")
        return txt_list
    
    def definition_splitting(define_text):
        dict_ = {}
        for i in define_text:
            key_ = i.split('AS')[0].lstrip()
            value_ = i.split('AS')[1].lstrip()
            dict_[key_]=value_
        return dict_
    
    def splitting_define(text):
        before_ = text[text.find('')+len(''):text.rfind(check_operand(text))].replace(" ", "")
        operand_ = check_operand(text)
        after_caluse= text[text.find(check_operand(text))+len(check_operand(text)):text.rfind('')].replace(" ", "")
        after_ = after_caluse[after_caluse.find('(')+len('('):after_caluse.rfind(')')].replace(")", "")
        return before_, operand_, after_
    
    def check_operand(text):
        final_operand = ''
        if text.find('<') != -1:
            return '<'
        elif text.find('<=') != -1:
            return '<='
        elif text.find('>') != -1:
            return '>'
        elif text.find('>=') != -1:
            return '>='
        elif text.find('=') != -1:
            return '='
        elif text.find('!=') != -1:
            return '!='
        else:
            print('error in check_operand')
    
    def get_truth(inp, relate, cut):
        ops = {'>': operator.gt,
               '<': operator.lt,
               '>=': operator.ge,
               '<=': operator.le,
               '=': operator.eq,
               '!=': operator.ne}
        return ops[relate](inp, cut)


    def prev_handling(df, column1_, operator_, column2_):
        a = []
        for i, row in df.iterrows():
            if(i != 0):
                a.append(df.loc[i] if get_truth(row[column1_], operator_, df.iloc[i-1][column2_]) else None)
        return pd.DataFrame([i for i in a if i is not None], columns = ['ID', 'PRODUCT', 'TSTAMP', 'UNITS_SOLD']).reset_index(drop = True)

    def assembly_func(text, df):
        df_ = df
        dict_ = {}
        text = definition_splitting(define_handling(txt))
        for keys, values in text.items():
            column1_, operator_, column2_ = splitting_define(values)
            df1 = prev_handling(df_, column1_, operator_, column2_)
            dict_[keys] = df1

        return dict_
    
    firsts_ = {}
    lasts_ = {}
    dictionary_ = assembly_func(definition_splitting(define_handling(txt)), df)
    for keys, values in dictionary_.items():
        up_first = pd.DataFrame(columns = df.columns)
        up_last = pd.DataFrame(columns = df.columns)
        for i in range(len(values)):

            if i == 0:
                up_first = up_first.append(values.iloc[i])
            else:
                if values.ID[i]-1 != values.ID[i-1]:
                    up_first = up_first.append(values.iloc[i])
                    up_last = up_last.append(values.iloc[i-1])
            if i == len(values)-1:
                up_last = up_last.append(values.iloc[i])

        firsts_[keys] = up_first
        lasts_[keys] = up_last
    
    def MEASURES_handling(text):
        start = "MEASURES"
        end = "PATTERN"
        txt = text[text.find(start)+len(start):text.rfind(end)]
        txt = txt.replace("\n ", "")
        txt = txt.replace("   ", "")
        txt = txt.replace("  ", "")
        txt = txt.replace("\t", "")
        txt_list = txt.split(",")
        return txt_list
    
    def expression_detection(txt):
        txt[txt.find("PATTERN")+len("PATTERN"):txt.rfind(")")]
        l = (txt.split("PATTERN ("))[1].split(")")[0].strip().split(" ")
        star_list = [i.strip()[:-1] for i in l if '*' in i]
        plus_list = [i.strip()[:-1] for i in l if '+' in i]
        return star_list, plus_list
    
    def match_final(txt):
        col = [val[val.find(" AS ")+len(" AS "):val.rfind("")] for val in MEASURES_handling(txt)]
        output_ = pd.DataFrame(columns = col)
        star_list, plus_list = expression_detection(txt)
        [val[val.find(" AS ")+len(" AS "):val.rfind("")] for val in MEASURES_handling(txt)]
        partitioning = partition_handling(txt)
        ordering = order_handling(txt)
        for i in MEASURES_handling(txt):
            val = i
            first_ = pd.DataFrame(columns = df.columns)
            last_ = pd.DataFrame(columns = df.columns)
            # need to apply the +/* change here as well as the negation
            for keys, values in dictionary_.items():
                values = values.sort_values(ordering).reset_index(drop = True)
                if(keys.strip() in plus_list):
                    if i.find(keys.strip()) != -1 and val[val.find("")+len(""):val.rfind("(")].lower() == 'last':
                        output_[val[val.find(" AS ")+len(" AS "):val.rfind("")]] = lasts_[keys][val[val.find(".")+len("."):val.rfind(")")]].tolist()
                    if i.find(keys.strip()) != -1 and val[val.find("")+len(""):val.rfind("(")].lower() == 'first':
                        output_[partitioning] = firsts_[keys][partitioning].reset_index(drop = True)
                        output_[val[val.find(" AS ")+len(" AS "):val.rfind("")]] = firsts_[keys][val[val.find(".")+len("."):val.rfind(")")]].tolist()            
        output_ = output_[partitioning+col]
        return output_
    
    def match_recognize(df,txt):
        star_list, plus_list = expression_detection(txt)
        aa = [i for i in list(dictionary_.keys())]
        output_ = match_final(txt)
        for i in star_list:
            for j in list(dictionary_.keys()):
                if(i in j):
                    pat_date = dictionary_[aa[i in j]]['TSTAMP'][0]
                    act_output = output_[(output_.peak_tstamp<pat_date) & (pat_date<output_.end_tstamp)]
                else:
                    act_output = output_
        return act_output
    
    def match_automata(txt, txt_):
        splitted_checked = [chr(ord('`')+i+1) for i in range(len(txt_.strip().split(" ")))]
        nfa_string = ''.join([str(elem) for elem in splitted_checked])
        dicto = {}
        pattern_ = (txt.split("PATTERN ("))[1].split(")")[0].strip().split(" ")
        pattern_ = [i[:-1] for i in pattern_]
        pattern_rep = [chr(ord('`')+i+1) for i in range(len(pattern_))]
        star_list_ = [pattern_rep[i] for i in range(len(pattern_)) if a[i] in star_list]
        plus_list_ = [pattern_rep[i] for i in range(len(pattern_)) if a[i] in plus_list]
        set_ = set([ f'q{i}' for i in range(len(set(star_list + plus_list)))])
        qs = list(set_)
        qs.sort()
        for i in range(len(qs)):
            subdict = {}
            if i == 0 & len(qs) != 1:
                for j in range(len(plus_list_)):
                    subdict[plus_list_[j]] = {qs[j+1]}
                dicto[qs[i]] = subdict

            elif i != len(qs)-1:
                for x in pattern_rep:
                    if x == plus_list_[-1]:
                        subdict[x] = {qs[i+1]}
                    else:
                        subdict[x] = {qs[i]}
                dicto[qs[i]] = subdict
            else:

                for j in range(len(plus_list_)):
                    subdict[plus_list_[-1]] = {qs[j-1]}
                dicto[qs[i]] = subdict

        nfa = NFA(
            states=set([ f'q{i}' for i in range(len(set(star_list + plus_list))+1)]),
            input_symbols=set(pattern_rep),
            transitions= dicto
            ,
            initial_state='q0',
            final_states={'q2'}
        )
        if nfa.accepts_input(nfa_string):
            return 'accepted'
        else:
            return 'rejected'
