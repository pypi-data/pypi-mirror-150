
def oracle():
	import onecard
	from onecard import oneCardFunc
	from clear import clear
	import random
	# MENU
	while True:
		clear()
		menu = input('''
	 --- THE ORACLE OF HAILEY'S DIAMOND ---

	 Main Menu

	 a) Card list

	 1) Pick one card
	 2) Pick more than one card
	 3) Past, present, future
	 4) Elemental spread
	 5) Celtic cross
	 6) Spread of the Week
	 7) Yes or No

	 ctrl+c to exit

		 >>> ''')


		# card list
		if menu == 'a':
			clear()
			with open('cards.txt', 'r') as x:
				cards = [line.rstrip('\n') for line in x]

			print ('\n --- The Major Arcana ---\n\n ', '\n  '.join(cards[0:22]),
			'\n\n\n --- Matter ---\n\n ', '\n  '.join(cards[23:36]),
			'\n\n\n --- Mind ---\n\n ', '\n  '.join(cards[37:50]),
			'\n\n\n --- Emotion ---\n\n ', '\n  '.join(cards[51:64]),
			'\n\n\n --- Will ---\n\n ', '\n  '.join(cards[65:78]),
			'\n\n\n --- Spirit ---\n\n ', '\n  '.join(cards[79:92]))

			input('\n	Press enter to return to main menu')


		# pick one card
		elif menu == '1':
			clear()
			print('\n', oneCardFunc())
			input('\n	Press enter to return to main menu')

		# pick more than one card
		elif menu == '2':
			# get card amount
			num = 93
			while num > 92 and type(num) == int:
				clear()
				try:
					num = int(input('\n How many cards? (max 92)\n\n	 >>> '))
				except Exception:
					pass

				# print cards
			clear()
			with open('cards.txt', 'r') as x:
				cards = [line.rstrip('\n') for line in x]

			cards = random.sample(cards, num)
			print ('\n'.join(cards))

			input('\n	Press enter to return to main menu')

		# past, present, future
		elif menu == '3':
			clear()
			print(f'\n	Past:	{oneCardFunc()}\n')
			print(f' Present:	{oneCardFunc()}\n')
			print(f'  Future:	{oneCardFunc()}\n')

			input('\n	Press enter to return to main menu')


		# elemental spread
		elif menu == '4':
			clear()
			print(f'\n   Matter:	{oneCardFunc()}\n')
			print(f'	 Mind:	{oneCardFunc()}\n')
			print(f'  Emotion:	{oneCardFunc()}\n')
			print(f'	 Will:	{oneCardFunc()}\n')
			print(f'   Spirit:	{oneCardFunc()}\n')

			input('\n	Press enter to return to main menu')


		# celtic cross
		elif menu == '5':
			clear()
			print(f'\n  General focus:	{oneCardFunc()}\n')
			print(f'   Interference:	{oneCardFunc()}\n')
			print(f' What is hidden:	{oneCardFunc()}\n')
			print(f'  What is known:	{oneCardFunc()}\n')
			print(f'		   Past:	{oneCardFunc()}\n')
			print(f'		 Future:	{oneCardFunc()}\n')
			print(f'	Perspective:	{oneCardFunc()}\n')
			print(f'	Environment:	{oneCardFunc()}\n')
			print(f'		  Ideal:	{oneCardFunc()}\n')
			print(f'		Outcome:	{oneCardFunc()}\n')

			input('\n	Press enter to return to main menu')


		# spread of the week
		elif menu == '6':
			clear()
			print(f'\n Theme of the Week:	{oneCardFunc()}\n')
			print(f'\n		   Tuesday:	{oneCardFunc()}\n')
			print(f'		 Wednesday:	{oneCardFunc()}\n')
			print(f'		  Thursday:	{oneCardFunc()}\n')
			print(f'			Friday:	{oneCardFunc()}\n')
			print(f'		  Saturday:	{oneCardFunc()}\n')
			print(f'			Sunday:	{oneCardFunc()}\n')
			print(f'			Monday:	{oneCardFunc()}\n')
			input('\n	Press enter to return to main menu')


		# yes or no
		elif menu == '7':
			clear()
			yn = random.choice([0, 1])

			if yn == 0:
				print('\n No')
			else:
				print('\n Yes')
			input('\n	Press enter to return to main menu')
oracle()
