import pandas as pd
import math
import numpy as np
from colorama import Fore, Back, Style

def orderData(data, answerCol):
    for col in data.columns:
        if len(data[col]) == len(pd.unique(data[col])):
            data = data.drop(col, axis = 1)
    features = [feat for feat in data]
    features.remove(answerCol)
    return data, features

class Node:
    def __init__(self):
        self.children = []
        self.value = ""
        self.isLeaf = False
        self.pred = ""
        self.answerCol = ""
        self.pred_id = 999999
        self.countAns = {}

def entropy(data):
    answers = data[answerCol].unique()
    prob = []
    for ans in answers:
        prob.append(sum(data[answerCol]==ans)/len(data[answerCol]))
    tot = 0
    for p in prob:
        tot += p * math.log(p, 2)
    return -tot

def info_gain(data, feature):
    uniq = np.unique(data[feature])
    gain = entropy(data)
    for u in uniq:
        subdata = data[data[feature] == u]
        subEntropy = entropy(subdata)
        gain -= (float(len(subdata)) / float(len(data))) * subEntropy
    return gain

def id3_bg(data, features, answerCol):
    root = Node()

    max_gain = 0
    max_feat = ""
    for feature in features:
        gain = info_gain(data, feature)
        if gain > max_gain:
            max_gain = gain
            max_feat = feature
    root.value = max_feat
    if max_feat != "":
        uniq = np.unique(data[max_feat])
        for u in uniq:
            subdata = data[data[max_feat] == u]
            if entropy(subdata) == 0.0:
                newNode = Node()
                newNode.isLeaf = True
                newNode.value = u
                newNode.pred = np.unique(subdata[answerCol])
                newNode.answerCol = answerCol
                newNode.pred_id = np.where(data[answerCol].unique()==newNode.pred)[0][0]
                root.children.append(newNode)
            else:
                dummyNode = Node()
                dummyNode.value = u
                new_features = features.copy()
                new_features.remove(max_feat)
                child = id3_bg(subdata, new_features, answerCol)
                dummyNode.children.append(child)
                dummyNode.answerCol = answerCol
                answers = data[answerCol].unique()
                for ans in answers:
                    count = sum(subdata[answerCol]==ans)
                    dummyNode.countAns[ans] = count
                root.children.append(dummyNode)
             
        return root

def ID3(data, answerCol):
    data, features = orderData(data, answerCol)
    return id3_bg(data, features, answerCol)

def printTree(root: Node, depth=0):
    Bold, Underline='\033[1m', '\033[4m'
    treeColors = [(Fore.BLACK, Back.CYAN),(Fore.WHITE, Back.MAGENTA),(Fore.WHITE,Back.BLUE),(Fore.BLACK,Back.YELLOW)]
    ansColors = [(Fore.BLACK, Back.GREEN),(Fore.WHITE, Back.RED)]
    n=0
    while root != None and n<1:
        for i in range(depth):
            print("\t", end="")
        print(f'{treeColors[depth%len(treeColors)][0]}'+
              f'{treeColors[depth%len(treeColors)][1]}'+root.value+f'{Style.RESET_ALL}', end="")
        if root.isLeaf:
            print(" -> ", f'{Bold}{Underline}{ansColors[root.pred_id%len(ansColors)][0]}{ansColors[root.pred_id%len(ansColors)][1]}'
                  +'['+f'{root.answerCol}'+': '+f'{root.pred[0]}'+']'+f'{Style.RESET_ALL}')

        else:
            if root.children == [None]:
                print(" -> ", f'{Bold}{Underline}{Fore.WHITE}{Back.BLACK}'+"Uncertain"+" "
                      +f'{root.countAns}'+f'{Style.RESET_ALL}')
        print()
        for child in root.children:
            printTree(child, depth + 1)
        n += 1