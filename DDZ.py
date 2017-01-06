#-*- coding: utf-8 -*-
import random
from enum import Enum
import itertools
from cardcolor import UseStyle
BASE_SCORE = 10


    

class CardSuits(Enum):
    HERATS = 0
    DIAMONDS = 1
    SPADES = 2
    CLUBS = 3

class Card_Type(Enum):
    SINGLE_CARD = 0#单牌  
    DOUBLE_CARD = 1#对子  
    THREE_CARD  = 2#3不带  
    BOMB_CARD   = 3#炸弹  
    THREE_ONE_CARD =4#3带1  
    THREE_TWO_CARD  = 5 #3带2  
    BOMB_TWO_CARD = 6#四个带2张单牌  
    BOMB_TWOOO_CARD = 7#四个带2对  
    CONNECT_CARD = 8 #连牌  
    COMPANY_CARD = 9#连队  
    AIRCRAFT_CARD = 10#飞机不带  
    AIRCRAFT_SINGLE_CARD = 11#飞机带单牌  
    AIRCRAFT_DOUBLE_CARD = 12#飞机带对子  
    ERROR_CARD    =13 #错误的牌型  
    
card_color = {CardSuits.HERATS:'red',CardSuits.DIAMONDS:'green',CardSuits.SPADES:'blue',CardSuits.CLUBS:'cyan','JOKER':'purple'}

class Card():
    
    def __init__(self,index,suit,value,color):
        self.index = index
        self.suit  =  suit
        self.value = value
        self.color = color

#     def __str__(self):
#         return  '[index]: ' + str(self.index) + ' [suit]: ' +str(self.suit) + ' [value]: '+str(self.value)

#     def __str__(self):
#         return  '[' +str(self.suit) + ' '+str(self.value)+']'
    def __str__(self):
        return  str(self.value)

class DDZ(object):
    '''
    Doudizhu Class
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cards_index=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,  
                19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,  
                36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]
        
        self.card_values = [3,4,5,6,7,8,9,10,'J','Q','K','A',2,'JokerBig','JokerSmall']
        self.player_scores = [10,10,10,10]
        self.score = 0
        self.multi = 1
        self.rob_score = 1
        self.cards_list= []
        self.round = 1
        self.players = [[],[],[],[]]
        self.landlord_id = 1
        self.card_right = 1
        self.play_record = []
        self.play_step = 0
        self.play_sequence = 0
        self.winner = 1
    def generate_cards(self):
        card_index = 0
        for card_name in itertools.product(self.card_values[:-2],CardSuits.__members__):
            self.cards_list.append(Card(card_index,card_name[1],card_name[0],card_color[CardSuits.__getitem__(card_name[1])]))
            card_index +=1
            
        self.cards_list.append(Card(card_index,self.card_values[-1],self.card_values[-1],card_color['JOKER']))
        card_index +=1
        self.cards_list.append(Card(card_index,self.card_values[-1],self.card_values[-2],card_color['JOKER']))
        
        for c in self.cards_list:
            pass#print c  

    def shuffle(self):
        random.shuffle(self.cards_index)
        #cut cards x 3
        for _ in range(3):
            n=random.randint(1,54)  
            b=self.cards_index[:n]  
            c=self.cards_index[n:]  
            self.cards_index=c+b   

    def deal(self):
        self.players[1]=self.cards_index[:-3:3]  
        self.players[2]=self.cards_index[1:-3:3]  
        self.players[3]=self.cards_index[2:-3:3]  
        self.Left=self.cards_index[-3:]
        
    def sort(self):
        self.players[1].sort()  
        self.players[2].sort()  
        self.players[3].sort()  
    
    
    def rob_landlord(self):
        self.multi *= 2
        
    def get_colorful_card_name(self,n):
        card_list = []
        if n == -1:
            for _ in self.Left:
                card_list.append( (self.cards_list[_].value,self.cards_list[_].color))
        else:
            for _ in self.players[n]:
                card_list.append( (self.cards_list[_].value,self.cards_list[_].color))
        return card_list
    
    
    def get_card_name(self,n):
        if n == -1:
            for _ in self.Left:
                print UseStyle(self.cards_list[_],fore=self.cards_list[_].color),
        else:
            for _ in self.players[n]:
                print UseStyle(self.cards_list[_],fore=self.cards_list[_].color),
                
        card_values=map(lambda x:x.value, map(lambda x:self.cards_list[x],self.players[n]) ) 

        return card_values
        #print card_values

        
    def trans_value(self,x):
        if x in '12345678910': 
            return int(x)
        else:
            return x
        
    def str_to_value(self,card_list):
        return  map(self.trans_value,card_list)
        
    def judge_cards_exists(self,card_list,player):
        card_list =self.str_to_value(card_list)
        current_player_card_list = self.players [player] #getattr(self, 'Player'+str(player))
        card_values=map(lambda x:x.value, map(lambda x:self.cards_list[x],current_player_card_list) )  
        #card_values=map(lambda x:str(x),card_values)
        
        for card_value in  card_list:
            if card_value in card_values:
                index =  card_values.index(card_value)
                del card_values[index]
                #print card_value,card_values
            else:
                return False
        return True
    
    def card_to_indexes(self, card_list,player):
        card_list =self.str_to_value(card_list)
        current_player_card_list = self.players[player] #getattr(self, 'Player'+str(player))
        card_index_values=map(lambda x:(x.index,x.value), map(lambda x:self.cards_list[x],current_player_card_list) ) 
        card_values=map(lambda x:x.value, map(lambda x:self.cards_list[x],current_player_card_list) ) 
#         print card_index_values
#         print card_values
        card_index_list = []
        for card_value in  card_list:
            if card_value in card_values:
                index =  card_values.index(card_value)
#                 print index,card_index_values[index][0]
                card_index_list.append(card_index_values[index][0])
                del card_values[index]
                del card_index_values[index]
        print 'card_index_list:',card_index_list,card_list
        return  card_index_list
                
    def judge_type(self,card_value_list):
#         if not self.judge_cards_exists(card_value_list,2):
#             print 'Fail'
#             return 
        #print 'card_value_list',card_value_list
        #cards_indexes = self.card_to_indexes(card_value_list,player_id)
        card_value_list = self.str_to_value(card_value_list)
        judge_value = 0 

        length = len(card_value_list)
        if length >= 5:
            # 检查是否为顺子
            for i in xrange(1, length):
                card = card_value_list[i]
                pre_card = card_value_list[i-1]
                #print self.card_values.index(card),card
                if self.card_values.index(card) != self.card_values.index(pre_card) + 1 or self.card_values.index(card) > self.card_values.index('A'):
                    break
            else:
                judge_value = card_value_list[0]
 
                return Card_Type.CONNECT_CARD,judge_value,length

            # 检查是否为连对
            for i in xrange(0, length-2, 2):
                if card_value_list[i] != card_value_list[i+1] or self.card_values.index(card_value_list[i]) + 1 != self.card_values.index(card_value_list[i+2]):
                    break
            else:
                judge_value = card_value_list[0]
 
                return Card_Type.COMPANY_CARD,judge_value,length
 
            # 检查是否为飞机
            card_dict = {}
            for card in card_value_list:
                if card in card_dict:
                    card_dict[card] += 1
                else:
                    card_dict[card] = 1
#             print card_dict,'card_dict'
            three_count = 0
            one_count = 0
            two_count = 0
            four_count = 0
            for key in card_dict:
                if card_dict[key] == 3:
                    three_count += 1
                elif card_dict[key] == 4:
                    four_count += 1
                elif card_dict[key] == 2:
                    two_count += 1
                else:
                    one_count += card_dict[key]
            
            if three_count == 2 and one_count==2:
                for key in card_dict:
                    if card_dict[key] == 3:
                        judge_value = key
                        break

                return Card_Type.AIRCRAFT_SINGLE_CARD,judge_value,length

            if three_count == 2 and two_count==2:
                for key in card_dict:
                    if card_dict[key] == 3:
                        judge_value = key
                        break
                return Card_Type.AIRCRAFT_DOUBLE_CARD,judge_value,length
            
            if three_count == 2:
                for key in card_dict:
                    if card_dict[key] == 3:
                        judge_value = key
                        break
                return Card_Type.AIRCRAFT_CARD,judge_value,length

            # 检查是否为三带一
            if three_count ==1 and  two_count == 1:
                for key in card_dict:
                    if card_dict[key] == 3:
                        judge_value = key
                        break
                return Card_Type.THREE_TWO_CARD,judge_value,length

            # 检查是否为四带二
            
            if four_count  == 1 and two_count == 2 :
                for key in card_dict:
                    if card_dict[key] == 4:
                        judge_value = key
                        break

                return  Card_Type.BOMB_TWOOO_CARD,judge_value,length
            if four_count * 2 == one_count and one_count != 0:
                for key in card_dict:
                    if card_dict[key] == 4:
                        judge_value = key
                        break

                return  Card_Type.BOMB_TWO_CARD,judge_value,length
 
        elif length == 4:
            # 检查是否为炸弹
            if card_value_list[0] == card_value_list[1] == card_value_list[2] == card_value_list[3]:
                judge_value = card_value_list[0]
                self.multi *= 2 # Send MSG
                return Card_Type.BOMB_CARD,judge_value,length
 
            # 检查是否为三带一
            elif card_value_list[0] == card_value_list[1] == card_value_list[2] or card_value_list[1] == card_value_list[2] == card_value_list[3]:
                judge_value = card_value_list[1]

                return Card_Type.THREE_ONE_CARD,judge_value,length
        elif length ==3:
            if card_value_list[0] == card_value_list[1] == card_value_list[2] :
                judge_value = card_value_list[0]
                return Card_Type.THREE_CARD,judge_value,length
            
        elif length == 2:
            # 检查是否是王炸

            if (card_value_list[0] == 'JokerSmall' and card_value_list[1] == 'JokerBig') or \
               (card_value_list[0] == 'JokerBig' and card_value_list[1] == 'JokerSmall'):

                return Card_Type.BOMB_CARD,judge_value,length
 
            # 检查是否是对子
            elif card_value_list[0] == card_value_list[1]:
                judge_value = card_value_list[0]

                return Card_Type.DOUBLE_CARD,judge_value,length
 
        elif length == 1:
            # 检查是否是单张
            judge_value = card_value_list[0]

            return Card_Type.SINGLE_CARD,judge_value,length

        return Card_Type.ERROR_CARD

    def compare(self,card1,card2):
        #print card1,card2
        print 'CARD_TYPE',self.judge_type(card2)[0]
        if  self.judge_type(card1)[0] == self.judge_type(card2)[0]:
            print 'Same Type'
            if self.card_values.index(self.judge_type(card1)[1]) <  self.card_values.index(self.judge_type(card2)[1]):
                return True
            else:
                return False

            if self.judge_type(card2)[0] == Card_Type.BOMB_CARD:
                print 'Compare BOMB'
            else:
                print 'Compare Value'
                
        else:
            if self.judge_type(card2)[0] == Card_Type.BOMB_CARD:
                return True

    def judge_win(self):
        for player_id in range(1,4):
            print 'LEFT CARDS',len(self.players[player_id]),self.players[player_id]
            if len(self.players[player_id]) == 0:
                self.winner = player_id
                return False
        return True
    
    def remove_card(self,index_list,player):
        for index in index_list:
            del self.players[player][self.players[player].index(index)]

    #出牌
    def play_card(self,card_str,player):
        
        if not self.judge_cards_exists(card_str, player):
            print 'No exists Cards' 
            return
        else :
            if self.judge_type(card_str) == Card_Type.ERROR_CARD:
                print 'Wrong Card Type'
                return
            else:
                if self.play_step == 0 or self.card_right == player:
                    print 'Player:',player,'[',card_str,']'
                    self.remove_card(self.card_to_indexes(card_str, player),player)
                    self.play_record.append(card_str)
                else :
                    if self.compare(self.play_record[self.play_step-1],card_str):
                        self.play_record.append(card_str)
                        print 'Player:',player,'[',card_str,']'
                        self.card_right =  player
                    else:
                        print 'Smaller Than Before'
                        return
        self.play_step +=1
        self.play_sequence +=1
        
            
    def rob_the_landlord(self,n,rob_score):
        if self.score == 0 and (rob_score > 3  or rob_score < 1):
            self.score = 3
            self.landlord_id = n
        elif rob_score == 0 :
            self.score = rob_score 
            self.landlord_id = n
        elif self.score >= rob_score or self.score == 3:
            return 
        else :

            self.score = rob_score
            self.landlord_id = n
            
        self.multi *= 2

    def passby(self):
        self.play_sequence +=1
        #self.card_right =  self.card_right+1 % 3

    def compute_score(self):
        score = BASE_SCORE * self.multi

        if self.winner == self.landlord_id:
            self.player_scores[self.winner] += score * 2
            for player_id in range(1,3):
                if player_id != self.landlord_id:
                    self.player_scores[player_id] -= score
                    
        if self.winner != self.landlord_id:
            self.player_scores[self.winner] -= score * 2
            for player_id in range(1,3):
                print self.player_scores[player_id]
                if player_id != self.landlord_id:
                    self.player_scores[player_id] += score
                    
        print 'MULTI:',self.multi
        print 'BASESCORE:',score
        print self.player_scores

    def play(self):
        print 'Deal Cards'
        self.generate_cards()
        self.shuffle()
        self.deal()
        self.sort()
        #print self.get_colorful_card_name(1)
        self.get_card_name(1)
        print 
        self.get_card_name(2)
        print 
        self.get_card_name(3)
        print 
        print 'Rob Landlord'
        while self.score !=3:
            
            print self.play_sequence %3+1,'ROB!'
            rob_score = raw_input(">>")
            self.rob_the_landlord(self.play_sequence %3 +1,int(rob_score))
            self.play_sequence +=1
            
        print 'Compute score'
        print '[',self.multi,self.landlord_id,self.score,']'
        self.card_right = self.landlord_id
        self.play_sequence = self.card_right -1
        print 'Show 3 Cards' 
        self.get_card_name(-1)
        print 
        print 'Deal Cards 3'
        self.players[self.landlord_id] += self.Left
        self.sort()
        print 'Play Card'

        while self.judge_win():
            print 'CURRENT RIGHT USER:',self.card_right
            print 'Player',self.play_sequence %3+1,'Please Input'
            print 'CURRENT CARDLIST'
            self.get_card_name(self.play_sequence %3+1)
            input_cmd = raw_input(">>")

            if self.play_step == 0 and input_cmd == 'pass':
                print 'Please play your card or lose'
                input_cmd = raw_input(">>")
                if input_cmd == 'pass':
                    print 'Landlord Lose  Set 0 score' 
                    self.player_scores[self.landlord_id] = 0
                    break
            #print 'Player:',self.card_right,'出牌'
            if input_cmd == 'pass':
                self.passby()
            else:
                self.play_card(input_cmd.split(),self.play_sequence %3+1)
            print 'play_record',self.play_record
            self.get_card_name(self.play_sequence %3+1)
            
        print 'Compute Score' 
        self.compute_score()




# ddz.card_to_indexes('3 4 5 6 7'.split(),2)
# ddz.play_card(('A 10').split(),2)
# print
# print '*'*20,'TEST','*'*20
# print ddz.judge_type('3 4 5 6 7'.split())  #min
# print ddz.judge_type('5 5 6 6 7 7'.split()) #min
# print ddz.judge_type('3 3 3 4 4 4 '.split()) #3min
# print ddz.judge_type('3 3 3 5 5 5 A J'.split()) #3min
# print ddz.judge_type('3 3 3 5 5 5 A A K K'.split()) #3min　#wrong
# print ddz.judge_type('4 4 4 4 A J'.split()) #4
# print ddz.judge_type('4 4 4 4 A A J J'.split()) #4
# print ddz.judge_type('A A A A'.split()) #4
# print ddz.judge_type('A A A K'.split()) #3
# print ddz.judge_type('A A A Q Q'.split()) #3
# print ddz.judge_type('JokerBig JokerSmall'.split()) #
# print ddz.judge_type('JokerBig'.split()) #min
# print '*'*20,'TEST','*'*20

# print ddz.compare('A A A Q Q'.split(),'K K K  9 9'.split())
# print ddz.compare('10 10 10 Q Q'.split(),'K K K  9 9'.split())
# print ddz.compare('10 10 10 Q Q'.split(),'K K K K'.split())
# print ddz.compare('4 4 4 4 5 6'.split(),'7 7 7 7 8 9'.split())

ddz = DDZ()
ddz.play()
