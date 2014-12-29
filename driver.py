from loveletter import Game
from loveletter import GameException
import random

random.seed(0)

ll = Game("AA","BB","CC","DD")

# def print_table():
#   print ll.PLAYERS[ll.get_curr_player_index()].name+"'s turn"
#   print "dead players : "+str(ll.get_dead_players())
#   print "immu players : "+str(ll.get_immuned_players())
#   for i in range(0, 4):
#     print str(i) + " " + ll.PLAYERS[i].name + "\t" + ll.PLAYERS[i].card1.name + "      \t" + ll.PLAYERS[i].card2.name
#   for i in range(0, 4):
#     print str(i) + " " + ll.PLAYERS[i].name + "\t" + str(ll.get_private_info(i))


print "players playing game:"
for i in range(0, 4):
  print ll.PLAYERS[i].name

# print "deck:"
# for card in ll.get_deck().cards:
#   print card.name


def test1():
	print "==========================="

	# seed 0
	ll.start()
	ll.print_deck()

	print "starting player:" + ll.PLAYERS[ll.get_curr_player_index()].name
	print "burned card:" + ll.get_burned_card().name

	# print_table()
	# ll.print_table();
	# ll.play_card(0,2,3)
	try:
		ll.play_card(0,1,3)
	except GameException: pass
	try:
		ll.play_card(0,1,2,-1)
	except GameException: pass
	try:
		ll.play_card(0,1,2,8)
	except GameException: pass
	try:
		ll.play_card(0,1,2,8)
	except GameException: pass
	# ll.play_card(1,1,0,8)
	ll.play_card(1,1,2,8)
	ll.play_card(2,2,3)
	ll.play_card(3,1,0)
	ll.play_card(0,2)
	# # print_table()
	try: 
		ll.play_card(1,1,0,8) 
	except GameException: pass
	ll.play_card(1,2) 
	try:
		ll.play_card(2,1,0)
	except GameException: pass
	try:
		ll.play_card(2,1,2)
	except GameException: pass
	ll.play_card(2,1,3)
	ll.play_card(0,2,2)
	ll.play_card(1,2,0)


def test2():
	# seed 52
	ll.start()

	print "starting player:" + ll.PLAYERS[ll.__curr_player_index].name
	print "burned card:" + ll.__burned_card.name
	print_table()
	ll.play_card(1,2,2)
	print_table()
	ll.play_card(2,2,2)






test1()