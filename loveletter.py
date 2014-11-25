import random
import sys

class LoveLetterCard:
  name = ''
  value = 0
  description = ''
  def __init__(self, name, value, description):
    self.name = name
    self.value = value
    self.description = description
    return

NULL_CARD     = LoveLetterCard("null",0,"null")
CARD_GUARD    = LoveLetterCard("Guard",1,"Name a non-Guard card and choose another player, if that person has that card, he or she is out of the round.")
CARD_PRIEST   = LoveLetterCard("Priest",2,"Look at another player's hand.")
CARD_BARON    = LoveLetterCard("Baron",3,"You and another player secretly compare hands. The player with the lower value is out of the round.")
CARD_HANDMAID = LoveLetterCard("Handmaid",4,"Until your next turn, ignore all effects from other players' cards.")
CARD_PRINCE   = LoveLetterCard("Prince",5,"Choose any player (including yourself) to discard his or her hand and draw a new card.")
CARD_KING     = LoveLetterCard("King",6,"Trade hands with another player of your choice.")
CARD_COUNTESS = LoveLetterCard("Countess",7,"If you have this card and the King or Prince is in your hand, you must discard this card.")
CARD_PRINCESS = LoveLetterCard("Princess",8,"If you discard this card, you are out of the round.")

def get_card_for_value(cardValue):
  if cardValue == 1:
    return CARD_GUARD
  elif cardValue == 2:
    return CARD_PRIEST
  elif cardValue == 3:
    return CARD_BARON
  elif cardValue == 4:
    return CARD_HANDMAID
  elif cardValue == 5:
    return CARD_PRINCE
  elif cardValue == 6:
    return CARD_KING
  elif cardValue == 7:
    return CARD_COUNTESS
  elif cardValue == 8:
    return CARD_PRINCESS
  else:
    raise Exception("cannot get card name for " + str(cardValue))



class LoveLetterDeck:
  cards = []
  def __init__(self):
    self.cards.append(CARD_GUARD)
    self.cards.append(CARD_GUARD)
    self.cards.append(CARD_GUARD)
    self.cards.append(CARD_GUARD)
    self.cards.append(CARD_GUARD)
    self.cards.append(CARD_PRIEST)
    self.cards.append(CARD_PRIEST)
    self.cards.append(CARD_BARON)
    self.cards.append(CARD_BARON)
    self.cards.append(CARD_HANDMAID)
    self.cards.append(CARD_HANDMAID)
    self.cards.append(CARD_PRINCE)
    self.cards.append(CARD_PRINCE)
    self.cards.append(CARD_KING)
    self.cards.append(CARD_COUNTESS)
    self.cards.append(CARD_PRINCESS)
    return





class LoveLetterPlayer:
  name = ""
  card1 = NULL_CARD
  card2 = NULL_CARD
  def __init__(self, name):
    self.name = name
    return
  def receive_card(self, card):
    if self.card1 == NULL_CARD:
      self.card1 = card
    elif self.card2 == NULL_CARD:
      self.card2 = card
    else:
      raise Exception("too many card in hand!")
    return
  def remove_card(self, card_index):
    if card_index == 1:
      # swap the cards
      self.card1 = self.card2
      self.card2 = NULL_CARD
    elif card_index == 2:
      self.card2 = NULL_CARD
  def has_card(self, cardValue):
    if self.card1.value == cardValue:
      return True
    elif self.card2.value == cardValue:
      return True
    return False
  def swap_card(self):
    tempcard = self.card1
    self.card1 = self.card2
    self.card2 = tempcard





class LoveLetterGameException(Exception):
  __is_public = False
  __message = ''
  def __init__(self,message,is_public=False):
    self.__is_public = __is_public
    self.__message = message

class LoveLetterGameAnswer:

  pass

class LoveLetterGame:
  MUST_TARGET_ANOTHER  = [1,2,3,6]
  PLAYERS = []

  __burned_card = NULL_CARD
  __curr_player_index = 0
  __immuned_players = []
  __dead_players = []
  __deck = None
  __game_over = False
  __info = ["=="]
  __private_info = []

  # for 3 players
  def __init__(self, name1, name2, name3):
    self.PLAYERS.append(LoveLetterPlayer(name1))
    self.PLAYERS.append(LoveLetterPlayer(name2))
    self.PLAYERS.append(LoveLetterPlayer(name3))
    self.PLAYERS.append(LoveLetterPlayer('nobody'))
    __dead_players.append(3)

  # for 4 players
  def __init__(self, name1, name2, name3, name4):
    self.PLAYERS.append(LoveLetterPlayer(name1))
    self.PLAYERS.append(LoveLetterPlayer(name2))
    self.PLAYERS.append(LoveLetterPlayer(name3))
    self.PLAYERS.append(LoveLetterPlayer(name4))



  # handling info
  def __add_info(self,info):
    print "publ        :"+info
    if isinstance(info,basestring):
      self.__info.append(info)
    else:
      self.__info.append(str(info))
  def __add_private_info(self,player_index,info):
    print "priv player"+str(player_index)+":"+info
    self.__private_info[player_index].append(info)


  # private helper functions
  def __shuffle_deck(self):
    for i in range(0,len(self.__deck.cards)):
      randpos = random.randint(i,len(self.__deck.cards)-1)
      temp = self.__deck.cards[i]
      self.__deck.cards[i] = self.__deck.cards[randpos]
      self.__deck.cards[randpos] = temp
    return
  def __burn_card(self):
    self.__burned_card = self.__deck.cards.pop()
    return
  def __give_card_from_deck(self,player_index):
    if player_index in self.__dead_players:
      raise Exception("a zombie trying to draw a card!?!?!")
    if len(self.__deck.cards) is 0:
      return False
    card = self.__deck.cards.pop()
    self.PLAYERS[player_index].receive_card(card)
    self.__add_private_info(player_index,"You just got a "+card.name)
    return True
  def __next_player(self):
    self.__curr_player_index += 1
    self.__curr_player_index %= 4
    if self.__curr_player_index in self.__dead_players:
      self.__next_player()
      return
    self.__add_info(self.PLAYERS[self.__curr_player_index].name + "'s turn")
    if self.__curr_player_index in self.__immuned_players:
      self.__add_info("One turn has passed, "+self.PLAYERS[self.__curr_player_index].name+" is no longer immuned")
      self.__immuned_players.remove(self.__curr_player_index)
    if self.__give_card_from_deck(self.__curr_player_index) is False:
      self.__add_info("Deck is drawned out, game over!")
      self.__game_over()
    return
  def __game_over(self):
    self.__add_info("=== Game Over ===")
    self.__add_info("The burned card was " + self.__burn_card.name)
    self.__game_over = True
    for i in range(4):
      assert self.PLAYERS.card2 is NULL_CARD
    winner = None
    highestValue = 0
    for i in range(4):
      currPlayer = self.PLAYERS[i]
      currCard = currPlayer.card1
      if currCard.value > 0:
        self.__add_info(currPlayer.name+" has a "+currCard.name)
      else:
        self.__add_info(currPlayer.name+" was eliminated.")
      if currCard.value > highestValue:
        highestValue = currCard.value
        winner = self.PLAYERS[i]
    self.__add_info("The winner is "+winner.name+". Congratulations!")
    return

  # some functions for testing
  def print_deck(self):
    print "deck:"
    for card in self.__deck.cards:
      print card.name
  def get_curr_player_index(self):
    return self.__curr_player_index
  def get_burned_card(self):
    return self.__burned_card
  def get_dead_players(self):
    return self.__dead_players
  def get_immuned_players(self):
    return self.__immuned_players
  def get_info(self):
    return self.__info
  def get_private_info(self,p_index):
    return self.__private_info[p_index]










  # start the game
  def start(self):
    # init some variables
    for i in range(4):
      self.__private_info.append([])
    self.__deck = LoveLetterDeck()
    self.__shuffle_deck()
    self.__game_over = False


    # starting the game logic
    self.__burn_card()
    self.__curr_player_index = random.randint(0,3)
    for i in range(0,4):
      self.__give_card_from_deck(i)
    self.__next_player()
    return 



  # play a card
  def play_card(self, player_index, card_index, target_index=None, guess=None):

    # verify game state
    if self.__game_over == True :
      raise LoveLetterGameException("game is not running")

    # verify player index
    if player_index in self.__dead_players :
      raise LoveLetterGameException("you are dead")
    if self.__curr_player_index != player_index:
      raise LoveLetterGameException("it's not your turn!")

    # verify card index
    if card_index == 1 :
      card_played = self.PLAYERS[player_index].card1
      card_holded = self.PLAYERS[player_index].card2
    elif card_index == 2:
      card_played = self.PLAYERS[player_index].card2
      card_holded = self.PLAYERS[player_index].card1
    else:
      raise LoveLetterGameException("card valid index are 1 and 2")

    assert card_played is not NULL_CARD:
    assert card_holded is not NULL_CARD:

    # verify target index
    if target_index < 0 or target_index > 3 :
      raise LoveLetterGameException("target range must be between 0 to 4")
    if target_index in self.__dead_players :
      raise LoveLetterGameException("target is dead")

    available_targets = [0,1,2,3]
    available_targets = [t for t in available_targets if t not in self.__dead_players]
    available_targets = [t for t in available_targets if t not in self.__immuned_players]

    if target_index is None :
      if card_played in self.MUST_TARGET_ANOTHER and available_targets:
        raise LoveLetterGameException("you must target someone")
      else:
        target_index = player_index

    target_card = self.PLAYERS[target_index].card1

    if card_played.value == 1 : ##########################################################################################################   1

      # verify guess index
      if isinstance(guess,int):
        if guess < 1 or guess > 8:
          raise LoveLetterGameException("please enter a guess between 1 and 7")
        elif guess is 1:
          raise LoveLetterGameException("cannot guess a guard")
      else:
        raise LoveLetterGameException("please enter a guess as an integer")

      self.__add_info("Card Played::"+self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)

      card_name = get_card_for_value(guess).name
      self.__add_info(self.PLAYERS[player_index].name+" is guessing that "+self.PLAYERS[target_index].name+" has "+card_name)

      if self.PLAYERS[target_index].has_card(guess):
        self.PLAYERS[target_index].remove_card(1)
        self.__dead_players.append(target_index)
        self.__add_info(self.PLAYERS[target_index].name+" has "+cardName+" and is eliminated")
        self.__add_private_info(target_index," you are eliminated by a Guard played by "+self.PLAYERS[player_index].name)
      else:
        self.__add_info("player "+self.PLAYERS[target_index].name+" does not have "+cardName)

    elif card_played.value == 2 : ##########################################################################################################   2

      self.__add_info("Card Played::"+self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)

      self.__add_info(self.PLAYERS[player_index].name+" looked at "+self.PLAYERS[target_index].name+"'s hand, info sent through private message")
      self.__add_private_info(player_index,"Your priest secretly telling you that "+self.PLAYERS[target_index].name+" has a "+target_card.name)
      self.__add_private_info(target_index,"Your "+target_card.name+" has been seen by "+self.PLAYERS[player_index].name)

    elif card_played.value == 3 : ##########################################################################################################   3

      self.__add_info("Card Played::"+self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)

      self.__add_info(self.PLAYERS[player_index].name+" and "+self.PLAYERS[target_index].name+" are secretly comparing hands.")

      target_hand_value = target_card.value
      player_hand_value = card_holded.value
      self.__add_private_info(player_index,"you have a "+cardInHand.name+" and your opponent has a "+target_card.name)
      self.__add_private_info(target_index,"you have a "+target_card.name+" and your opponent has a "+cardInHand.name)
      winner_index = -1
      loser_index = -1
      if target_hand_value > player_hand_value:
        winner_index = target_index
        loser_index = player_index
      elif target_hand_value < player_hand_value:
        winner_index = player_index
        loser_index = target_index
      if winner_index != loser_index:
        self.__add_info(self.PLAYERS[winner_index].name+" wins! "+self.PLAYERS[loser_index].name+" is eliminated")
        self.PLAYERS[loser_index].remove_card(1)
        self.__dead_players.append(loser_index)
      else:
        self.__add_info("It was a tie, nobody eliminated.")

    elif card_played.value == 4 : ##########################################################################################################   4
      self.__add_info("Card Played::"+self.PLAYERS[player_index].name+" played "+card_played.name)

      self.__add_info(self.PLAYERS[player_index].name+" is immuned for one turn!")
      self.__immuned_players.append(player_index)

    elif card_played.value == 5 : ##########################################################################################################   5
      if self.PLAYERS[player_index].has_card(7):
        raise LoveLetterGameException("you must play your countess")

      self.__add_info("Card Played::"+self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)

      self.__add_info(self.PLAYERS[player_index].name+" choose "+self.PLAYERS[target_index].name+" to discard his/her hand and to draw a new card")

      if target_card.value == 8:
        self.__add_info(self.PLAYERS[target_index].name+" discarded the princess and is out of the game.")
        if card_index == 2:
          card_index = 1
        self.PLAYERS[target_index].remove_card(1)
        self.__dead_players.append(target_index)


      # TODO
      raise Exception("TODO")

    elif card_played.value == 6 : ##########################################################################################################   6
      if self.PLAYERS[player_index].has_card(7):
        raise LoveLetterGameException("you must play your countess")

      self.__add_info("Card Played::"+self.PLAYERS[player_index].name+" played "+card_played.name)

      if card_index == 1:
        self.PLAYERS[player_index].remove_card(2)
      else:
        self.PLAYERS[player_index].remove_card(1)
      self.PLAYERS[target_index].remove_card(1)
      self.PLAYERS[player_index].receive_card(target_card)
      self.__add_private_info(player_index,"you just traded hands with "+self.PLAYERS[target_index].name+" and you got a "+target_card.name)
      self.PLAYERS[target_index].receive_card(cardInHand)
      self.__add_private_info(target_index,"you just traded hands with "+self.PLAYERS[player_index].name+" and you got a "+cardInHand.name)
      self.__add_info(self.PLAYERS[player_index].name+" and "+self.PLAYERS[target_index].name+" just traded hands")


    elif card_played.value == 7 : ##########################################################################################################   7
      self.__add_info("Card Played::"+self.PLAYERS[player_index].name+" played "+card_played.name)
      self.__add_info(self.PLAYERS[player_index].name+" played Countess and nothing happens.")

    elif card_played.value == 8 : ##########################################################################################################   8
      self.__add_info("Card Played::"+self.PLAYERS[player_index].name+" played "+card_played.name)
      self.__add_info(self.PLAYERS[player_index].name+" played Princess and is eliminated.")
      self.__dead_players.append(player_index)

    else
      raise LoveLetterGameException("played unknown card"+card_played.name,is_public=yes)

    self.PLAYERS[player_index].remove_card(card_index)
    self.__next_player()
    # todo: check if deck is empty, game over

    pass












  def old_play(self, player_index, card_index, target_index=None, guess=None):
    if target_index is None :
      target_index = player_index

    card_played = NULL_CARD
    if self.gameOver == True :
      self.__add_info(self.PLAYERS[player_index].name+": game is over")
      return 3
    if player_index in self.__dead_players :
      self.__add_info(self.PLAYERS[player_index].name+": you are dead")
      return 3
    if target_index > 3 or target_index < 0:
      self.__add_info(self.PLAYERS[player_index].name+": invalid target")
      return 3
    if target_index in self.__dead_players :
      self.__add_info(self.PLAYERS[player_index].name+": target is dead")
      return 3
    if self.__curr_player_index != player_index:
      self.__add_info(self.PLAYERS[player_index].name+": it's not your turn!")
      return 3



    if target_index == player_index:
      if card_played.value in self.MUST_TARGET_ANOTHER  :
        self.__add_info(self.PLAYERS[player_index].name+": cannot target yourself")
        return 3

    target_card = self.PLAYERS[target_index].card1


    if card_played.value == 1 : ##########################################################################################################   1
      if not isinstance(guess, int) :
        self.__add_info("when playing a guard, please add what you are guessing")
        return 3
      if guess == 1:
        self.__add_info("cannot guess guard, try again")
        return 3
      elif guess >= 2 and guess <= 8 :
        self.__add_info(self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)

        if target_index in self.__immuned_players:
          self.__add_info(self.PLAYERS[target_index].name+" is immuned!")

        else:
          cardName = self.deck.getNameForValue(guess)
          self.__add_info(self.PLAYERS[player_index].name+" is guessing "+self.PLAYERS[target_index].name+" has "+cardName)
          if self.PLAYERS[target_index].has_card(guess):
            self.PLAYERS[target_index].remove_card(1)
            self.__dead_players.append(target_index)
            self.__add_info(self.PLAYERS[target_index].name+" had "+cardName+" and is eliminated")
            self.__add_private_info(target_index," you are eliminated by a Guard played by "+self.PLAYERS[player_index].name)

          else:
            self.__add_info("player "+self.PLAYERS[target_index].name+" does not have "+cardName)


      else:
        self.__add_info("invalid guess, please try again")
        return 3
    elif card_played.value == 2 : ##########################################################################################################   2
      self.__add_info(self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)

      if target_index in self.__immuned_players:
        self.__add_info(self.PLAYERS[target_index].name+" is immuned!")

      else:
        self.__add_info(self.PLAYERS[player_index].name+" looked at "+self.PLAYERS[target_index].name+"'s hand, info sent through private message")
        self.__add_private_info(player_index,"Your priest secretly telling you that "+self.PLAYERS[target_index].name+" has a "+target_card.name)
        self.__add_private_info(target_index,"Your "+target_card.name+" has been seen by "+self.PLAYERS[player_index].name)


    elif card_played.value == 3 : ##########################################################################################################   3
      self.__add_info(self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)
  
      if target_index in self.__immuned_players:
        self.__add_info(self.PLAYERS[target_index].name+" is immuned!")

      else:
        self.__add_info(self.PLAYERS[player_index].name+" and "+self.PLAYERS[target_index].name+" are secretly comparing hands.")
        targetHandValue = target_card.value
        playerHandValue = cardInHand.value
        self.__add_private_info(player_index,"you have a "+cardInHand.name+" and your opponent has a "+target_card.name)
        self.__add_private_info(target_index,"you have a "+target_card.name+" and your opponent has a "+cardInHand.name)
        winnerIndex = -1
        loserIndex = -1
        if targetHandValue > playerHandValue:
          winnerIndex = target_index
          loserIndex = player_index
        elif targetHandValue < playerHandValue:
          winnerIndex = player_index
          loserIndex = target_index
        if winnerIndex != loserIndex:
          self.__add_info(self.PLAYERS[winnerIndex].name+" wins! "+self.PLAYERS[loserIndex].name+" is eliminated")
          self.PLAYERS[loserIndex].remove_card(1)
          self.__dead_players.append(loserIndex)
        else:
          self.__add_info("It was a tie, nobody eliminated.")


    elif card_played.value == 4 : ##########################################################################################################   4
      self.__add_info(self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)

      self.__add_info(self.PLAYERS[player_index].name+" is immuned for one turn!")
      self.__immuned_players.append(player_index)


    elif card_played.value == 5 : ##########################################################################################################   5
      if self.PLAYERS[player_index].has_card(7):
        self.__add_private_info(player_index,"you must play your countess")
        return 4
      self.__add_info(self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)

      if target_index in self.__immuned_players:
        self.__add_info(self.PLAYERS[target_index].name+" is immuned!")

      else:
        self.__add_info(self.PLAYERS[player_index].name+" choose "+self.PLAYERS[target_index].name+" to discard his/her hand and to draw a new card")
        if target_index != player_index:
          if self.PLAYERS[target_index].has_card(8):
            self.PLAYERS[target_index].remove_card(1)
            self.__add_private_info(target_index,self.PLAYERS[player_index].name+" made you discard your princess, you are now eliminated")
            self.__add_info(self.PLAYERS[target_index].name+" just discarded a princess and is now eliminated")
            self.__dead_players.append(target_index)
          else:
            self.PLAYERS[target_index].remove_card(1)
            self.__add_private_info(target_index,self.PLAYERS[player_index].name+" made you discard your hand and draw a new card")
            if self.__give_card_from_deck(target_index) == False:
              self.__add_private_info(target_index,"deck is empty, you are eliminated by a Prince played by "+self.PLAYERS[player_index].name)
              self.__add_info(self.PLAYERS[target_index].name+" just discarded the last card and there is no more card to draw, therefore, he/she is eliminated")
              self.__dead_players.append(target_index)
            self.__add_info(self.PLAYERS[target_index].name+" just discarded a "+target_card.name)
        else:
          self.__add_private_info(player_index,"you discarded your "+cardInHand.name)
          if card_index == 1:
            self.PLAYERS[player_index].remove_card(2)
            self.__give_card_from_deck(player_index)
          else :
            self.PLAYERS[player_index].remove_card(1)
            self.__give_card_from_deck(player_index)
            self.PLAYERS[player_index].swap_card()

    elif card_played.value == 6 : ##########################################################################################################   6
      if self.PLAYERS[player_index].has_card(7):
        self.__add_private_info(player_index,"you must play your countess")
        return 4
      self.__add_info(self.PLAYERS[player_index].name+" played "+card_played.name+" on "+self.PLAYERS[target_index].name)

      if target_index in self.__immuned_players:
        self.__add_info(self.PLAYERS[target_index].name+" is immuned!")

      else:
        if card_index == 1:
          self.PLAYERS[player_index].remove_card(2)
        else:
          self.PLAYERS[player_index].remove_card(1)
        self.PLAYERS[target_index].remove_card(1)
        self.PLAYERS[player_index].receive_card(target_card)
        self.__add_private_info(player_index,"you just traded hands with "+self.PLAYERS[target_index].name+" and you got a "+target_card.name)
        self.PLAYERS[target_index].receive_card(cardInHand)
        self.__add_private_info(target_index,"you just traded hands with "+self.PLAYERS[player_index].name+" and you got a "+cardInHand.name)
        self.__add_info(self.PLAYERS[player_index].name+" and "+self.PLAYERS[target_index].name+" just traded hands")


    elif card_played.value == 7 : ##########################################################################################################   7
      self.__add_info(self.PLAYERS[player_index].name+" played Countess and nothing happens.")



    elif card_played.value == 8 : ##########################################################################################################   8
      self.__add_private_info(player_index,"you cannot play the princess")
      return 4

    else :
      self.__add_info("player"+str(player_index)+" played an unknown card")
      return 3

    print "============================================"
    self.PLAYERS[player_index].remove_card(card_index)
    self.__next_player()
    # todo: check if deck is empty, game over
