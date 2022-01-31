from hashlib import new


class Node:
    def __init__(self, field, my_hand, oponnent_qtd, left, right, value = 0):
        self.field = field
        self.my_hand = my_hand
        self.oponnent_qtd = oponnent_qtd
        self.left = left
        self.right = right
        self.value = value

class Minimax:
    def __init__(self):
        self.pieces = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [1,2], [1,3], [1,4], [1,5], [1,6], [2,3], [2,4], [2,5], [2,6], [3,4], [3,5], [3,6], [4,5], [4,6], [5,6]]

    def end_game(self, hand1, oponnent_qtd):
        if hand1 == []:
            return 1
        elif oponnent_qtd == 0:
            return -1
        else:
            return 0

    def max_part(self, node):
        end = self.end_game(node.my_hand, node.oponnent_qtd)
        if end != 0:
            node.value = end
            return node

        plays = []
        new_field = list(node.field)
        for piece in self.pieces:
            if piece in node.field:
                pass

            elif piece[0] == node.left:
                new_field.append(piece)
                #                               Campo                    Mão           Mão Oponente     Left       Right          Play       Value
                plays.append(Node(new_field, node.my_hand, node.oponnent_qtd-1, piece[1], node.right, 0))
                new_field.remove(piece)

            elif piece[1] == node.left:
                new_field.append(piece)
                #                               Campo                    Mão           Mão Oponente     Left       Right          Play       Value
                plays.append(Node(new_field, node.my_hand , node.oponnent_qtd-1, piece[0], node.right, 0))
                new_field.remove(piece)
            
            elif piece[0] == node.right:
                new_field.append(piece)
                #                               Campo                    Mão           Mão Oponente     Left       Right          Play       Value
                plays.append(Node(new_field, node.my_hand , node.oponnent_qtd-1, node.left, piece[1], 0))
                new_field.remove(piece)
            
            elif piece[1] == node.right:
                new_field.append(piece)
                #                               Campo                    Mão           Mão Oponente     Left       Right          Play       Value
                plays.append(Node(new_field, node.my_hand , node.oponnent_qtd-1, node.left, piece[0], 0))
                new_field.remove(piece)
        
        if plays != []:
            for i in range(len(plays)):
                plays[i].value = self.min_part(plays[i]).value

            play = plays[0]
            for i in range(len(plays)):
                if plays[i].value > play.value:
                    play = plays[i]

            return play
        
        else:
            node.value = -1
            return node



    def min_part(self, node):
        end = self.end_game(node.my_hand, node.oponnent_qtd)
        if end != 0:
            node.value = end
            return node

        plays = []
        new_field = list(node.field)
        for i in range(len(node.my_hand)):
            piece = node.my_hand[i]

            if piece[0] == node.left:
                new_hand = list(node.my_hand)
                new_hand.remove(piece)
                new_field.append(piece)
                #                               Campo                    Mão                               Mão Oponente     Left       Right         Play        Value
                plays.append(Node(new_field, new_hand, node.oponnent_qtd, piece[1], node.right, 0))
                new_field.remove(piece)

            elif piece[1] == node.left:
                new_hand = list(node.my_hand)
                new_hand.remove(piece)
                new_field.append(piece)
                #                               Campo                    Mão                               Mão Oponente     Left       Right          Play       Value
                plays.append(Node(new_field, new_hand, node.oponnent_qtd, piece[0], node.right, 0))
                new_field.remove(piece)
                
            if piece[0] == node.right:
                new_hand = list(node.my_hand)
                new_hand.remove(piece)
                new_field.append(piece)
                #                               Campo                    Mão                               Mão Oponente     Left       Right   Value
                plays.append(Node(new_field, new_hand, node.oponnent_qtd, node.left, piece[1], 0))
                new_field.remove(piece)
                
            elif piece[1] == node.right:
                new_hand = list(node.my_hand)
                new_hand.remove(piece)
                new_field.append(piece)
                #                               Campo                    Mão                               Mão Oponente     Left       Right   Value
                plays.append(Node(new_field, new_hand, node.oponnent_qtd, node.left, piece[0], 0))
                new_field.remove(piece)

        if plays != []:
            for i in range(len(plays)):
                plays[i].value = self.max_part(plays[i]).value
                
            play = plays[0]
            
            for i in range(len(plays)):
                if plays[i].value < play.value:
                    play = plays[i]
                    
            return play

        else:
            node.value = 1
            return node


    def minimax(self, field, my_hand, oponnent_qtd, left, right):
        new_field = list(field)
        new_hand = list(my_hand)
        print(new_field)
        print(new_hand)
        raiz = Node(new_field,new_hand,oponnent_qtd,left,right)
        play = self.min_part(raiz)
        for piece in play.my_hand:
            my_hand.remove(piece)
        piece = my_hand[0]
        print(piece)
        if piece[0] == left:
            return [piece, 'Left']
        if piece[1] == left:
            return [piece, 'Left']
        if piece[0] == right:
            return [piece, 'Right']
        if piece[1] == right:
            return [piece, 'Right']
