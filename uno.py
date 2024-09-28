import random

# This game uses a total deck of 108 cards
def cardDeck():
    deck = []
    #Type of cards we'll work with are:
    wild_cards= ['wild', 'wild draw four'] 
    colors = ['🔴 red', '🔵 blue', '🟢 green', '🟡 yellow']
    special_cards = ['skip', 'reverse', 'draw two']
    
    # Add wild and wild draw cards to the deck
    # There are 4 wild cards and 4 wild draw four cards
    for i in range(4):
        deck.append('wild')
        deck.append('wild draw four')
    
    # Add number cards to the deck
    for color in colors:
        # There are 19 red, 19 blue, 19 green, and 19 yellow cards numbered 0 to 9 and 1 to 9
        for number in range(10):
            deck.append(f'{color} {number}') #for the 0 to 9 cards
            if number != 0: #for the 1 to 9 cards
                deck.append(f'{color} {number}')
    
    # Add special cards to the deck
    for color in colors:
        # Each color has 2 of each special card
        for card in special_cards:
            deck.append(f'{color} {card}')
            deck.append(f'{color} {card}')
    
    #Shuffle the deck
    random.shuffle(deck)
    
    return deck
#initiate the function
deck = cardDeck()

#Deal cards to each player. Each player starts with 7 cards.
def dealCards(deck, player):
    for i in range(7):
        player.append(deck.pop())
        
#One card must be in the discard pile
discardPile = [deck.pop()]

#This game will be between 2 players, the user and the computer.     
userHand= []
computerHand= []
#Deal the card to each player
dealCards(deck, userHand)
dealCards(deck, computerHand)

#Game intro
print("🎉 Hi and welcome to the game of UNO! 🎉")
user_name = input("Please enter your name: ").capitalize()

#Game rules:
#A function for drawing cards from the deck
def draw_card(player,cardQuantity): 
    global deck, discardPile
    for i in range (cardQuantity):
        if not deck: #If the deck is empty
            print("Reshuffling...")
            deck = discardPile[:-1]  # transferes the discard pile to the deck but leaves the top discard card behind
            random.shuffle(deck) #Reshuffles the discard pile to form a deck
            discardPile = [discardPile[-1]]  
        player.append(deck.pop())
        
#This function checks if a carde can be played        `
def Card_validation(player_card, discard_card):
    played_card = player_card.split()
    card_on_discard = discard_card.split()
    
    if played_card[0] == "wild" or played_card[0] == "wild draw four": #Checks for wild cards
        return True 
    
    if card_on_discard[0] == "wild" or card_on_discard[0] == "wild draw four": #Checks for wild cards
        return True 
    
    # Checks if the cards match by color or number
    if played_card[0] == card_on_discard[0] or played_card[1] == card_on_discard[1]:
        return True
    
    return False


# This function handles the effects of special cards
def user_special_card(card, player, opponent_name):
    #When a player uses the Draw two card, next player draws 2 cards from the deck and misses their turn
    if "draw two" in card:
        print(f"{user_name} played a Draw Two! Computer must draw 2 cards and skip their turn.")
        draw_card(computerHand, 2)
        return True  # Skip turn
    
    elif "reverse" in card:
        print (f"{user_name} played a Reverse! Computer must skip their turn")
        return True #Current player plays again
    
    #When a player uses the skip card, the next player loses their turn
    elif "skip" in card:
        print(f"{user_name} played a Skip! Computer must skip their turn.")
        return True  # Skip turn
    
    #When a player uses the wild card, that player chooses the next color to be played
    elif "wild" in card:
        #player chooses the next color
        print("You played a Wild card! Choose a color by entering the number:") # Display the color options with their corresponding numbers
        color_options = {
            1: "🔴 red",
            2: "🔵 blue",
            3: "🟢 green",
            4: "🟡 yellow"
        }
        for number, color in color_options.items():
            print(f"{number}: {color}")  # Show color choices
        
        chosen_color_number = input("Enter the number of your chosen color: ").strip()
        
        # Validate chosen color
        if chosen_color_number.isdigit() and int(chosen_color_number) in color_options:
            chosen_color = color_options[int(chosen_color_number)].split()[0]  # Get the emoji part
            discardPile.append("wild")
            print(f"The new color is {chosen_color}.")
        
        #When a player uses the wild draw four card, same as wild card + the next player draws 4 cards and misses their turn
        if "wild draw four" in card:
            print(f"Computer must draw 4 cards and skip their turn.")
            draw_card(computerHand, 4)
            discardPile.append("wild draw four")
            return True  # Skip turn
        
    return False  # Continue normally

def computer_special_card(card, player, opponent_name):
    #When a player uses the Draw two card, next player draws 2 cards from the deck and misses their turn
    if "draw two" in card:
        print(f"{player} played a Draw Two! {user_name} must draw 2 cards and skip their turn.")
        draw_card(userHand, 2)
        return True  # Skip turn
    
    elif "reverse" in card:
        print (f"{player} played a Reverse! {user_name} must skip their turn")
        return True #Current player plays again
    
    #When a player uses the skip card, the next player loses their turn
    elif "skip" in card:
        print(f"{player} played a Skip! {user_name} must skip their turn.")
        return True  # Skip turn
    
    #When a player uses the wild card, that player chooses the next color to be played
    elif "wild" in card:
        # Player chooses a color
        colors= ['red', 'blue', 'green', 'yellow']
        chosen_color = random.choice(colors)
        card = f"{chosen_color} Wild"
        discardPile.append("wild")
        print(f"The new color is {chosen_color}.")
        
        #When a player uses the wild draw four card, same as wild card + the next player draws 4 cards and misses their turn
        if "wild draw four" in card:
            print(f"{user_name} must draw 4 cards and skip their turn.")
            draw_card(userHand, 4)
            discardPile.append("wild draw four")
            return True  # Skip turn
        
    return False

#Players take turns matching a card from their hand to the discard pile card based on number or color
#Game loop for the user
while True: #The game will keep going as long as the below conditions are still true
    print(f"Card on discard pile: {discardPile[-1]}") #Prints what card is currently the top card on the discard pile
    print(f"My cards:{userHand}") #Prints out your hand cards
    
    for index, card in enumerate(userHand): #assign a number to each card
        print(f"{index + 1}: {card}")
        
    possible_Usermoves=[] #A list of possible cards you can play
    for card in userHand:#checks each card in the userHand list to see which ones meet the card_validation conditions.
        if Card_validation(card, discardPile[-1]):
            possible_Usermoves.append(card)
            #The cards that meet the condition are added to the possible_moves list
    if possible_Usermoves:
        print(f"Here are your possible options:{possible_Usermoves}")
        user_cardChoice= input("Choose a card to play:").lower()
        
        if user_cardChoice.isdigit() and 1 <= int(user_cardChoice) <= len(userHand):
            card_index = int(user_cardChoice) - 1  # Convert to zero-based index
            user_cardChoice = userHand[card_index]  # Get the actual card
            userHand.remove(user_cardChoice) #Removes the card from the user's hand card
            discardPile.append(user_cardChoice) #Adds the chosen card to the discard pile
            print(f"Card played: {user_cardChoice}")
            
            # Check for special card effects
            if user_special_card(user_cardChoice, "User", computerHand):
                continue  # Skip the computer's turn if a special card was played
        else:
            print("invalid input.Please try again")
            continue
        
    else:
        print("You have no possible choices. Draw a card from the deck.")
        userHand.append(deck.pop())
    
    #Checks if the user has won  
    if not userHand:
        print(f"Congratulations {user_name}!! YOU WON!")
        break
    
#Game loop for the computer
    # Computer's turn
    print("Computer's turn...")
    possible_computerMoves = [card for card in computerHand if Card_validation(card, discardPile[-1])]
    if possible_computerMoves:
        computer_cardChoice = random.choice(possible_computerMoves)
        computerHand.remove(computer_cardChoice)
        discardPile.append(computer_cardChoice)
        print(f"Computer played {computer_cardChoice}")
        
        # Handle computer's special card
        if computer_special_card(computer_cardChoice, "Computer", userHand):
            continue  # Skip the user's turn if a special card was played
    else:
        print("Computer draws a card.")
        computerHand.append(deck.pop())
        
    # Check if computer won
    if not computerHand:
        print("GAME OVER! YOU LOST 😞")
        break