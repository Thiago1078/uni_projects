from socket import *
from subprocess import * 

luggage_cost = 50
carry_on_cost = 20

tickets_bank = {'economy_tickets_left': 120,
          'business_tickets_left': 30,
}

cost_dict = {'business_ticket_cost': 200,
             'economy_ticket_cost': 80,
}

def validate_order(ticket_class, passenger_count, luggage_count, carry_on_count): 
    
    if ticket_class == 'business':
        ticket_cost = cost_dict['business_ticket_cost']
        tickets_left = tickets_bank['business_tickets_left']
        remove_from = 'business_tickets_left'
    elif ticket_class == 'economy':
        ticket_cost = cost_dict['economy_ticket_cost']
        tickets_left = tickets_bank['economy_tickets_left']
        remove_from = 'economy_tickets_left'

    max_luggage = passenger_count * 2
    print(f"max luggage is {max_luggage}")
    max_carry_on = passenger_count
    print(f"max carry ons are {max_carry_on}")
    enough_tickets = (tickets_left - passenger_count) >= 0
    print(f"after deducting passenger count, remaining is {tickets_left - passenger_count}.")

    valid = (luggage_count <= max_luggage) and (carry_on_count <= max_carry_on) and enough_tickets

    cost = 0
    cost += passenger_count*ticket_cost
    cost += luggage_count*luggage_cost
    cost += carry_on_count*carry_on_cost

    ticket_confirmation = f"Your ticket of {passenger_count} {ticket_class} class tickets and {luggage_count} luggage bags and {carry_on_count} carry-ons is valid. Cost is {cost}. There are {tickets_left - passenger_count} {ticket_class} class tickets left."

    if valid: 
        new_ticket_amount = tickets_left - passenger_count
        return ticket_confirmation, remove_from, new_ticket_amount

    else: 
        ticket_confirmation = f"Your ticket is invalid. We have {tickets_left} {ticket_class} class tickets left."
        new_ticket_amount = tickets_left
        return ticket_confirmation, remove_from, new_ticket_amount

def no_more_tickets(): 
    if (tickets_bank['business_tickets_left'] == 0) and (tickets_bank['economy_tickets_left'] == 0): 
        return True
    else: 
        return False

# STUDENTS: randomize this port number (use same one that client uses!)
serverPort = 12000

# create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))

# server begins listening for incoming TCP requests
serverSocket.listen(1)

# output to console that server is listening 
print ("The Airplane Ticket Server running over TCP is ready to receive ... ")

server_stays_open = True

while server_stays_open:
    # server waits for incoming requests; new socket created on return
    connectionSocket, addr = serverSocket.accept()

    acknowledge_request = connectionSocket.recv(1024)

    valid_classes = ['business', 'economy']

    while True: 
        connectionSocket.send("What is the class of ticket you want? 'business' or 'economy'?".encode("utf-8"))
        ticket_class = connectionSocket.recv(1024).decode("utf-8")

        if ticket_class in valid_classes:
            print(f"Customer sent {ticket_class} for class of tickets.")
            break

        connectionSocket.send("Sorry, that was an invalid response. Try again. ".encode("utf-8"))
    
    while True: 
        connectionSocket.send("How many passengers? Type an integer. ".encode("utf-8"))
        passenger_count = connectionSocket.recv(1024).decode("utf-8")
        print(f"Customer sent {passenger_count} passenger count.")

        try: 
            passenger_count = int(passenger_count)
            break 
        except: 
            pass

        connectionSocket.send("Sorry, that was an invalid response. Try again.".encode("utf-8"))

    while True:
        connectionSocket.send("How many luggage? Type an integer. ".encode("utf-8"))
        luggage_count = connectionSocket.recv(1024).decode("utf-8")
        print(f"Customer sent {luggage_count} luggage count.")
    
        try: 
            luggage_count = int(luggage_count)
            break 
        except: 
            pass

        connectionSocket.send("Sorry, that was an invalid response. Try again.".encode("utf-8"))
        
    while True:
        connectionSocket.send("How many carry-ons? Type an integer. ".encode("utf-8"))
        carry_on_count = int(connectionSocket.recv(1024).decode("utf-8"))
        print(f"Customer sent {carry_on_count} for carry-on count.")

        try: 
            carry_on_count = int(carry_on_count)
            break 
        except: 
            pass

        connectionSocket.send("Sorry, that was an invalid response. Try again.".encode("utf-8"))

    ticket_confirmation, ticket_class, new_ticket_amount = validate_order(ticket_class=ticket_class, passenger_count=passenger_count, luggage_count=luggage_count, carry_on_count=carry_on_count)

    tickets_bank[ticket_class] = new_ticket_amount

    connectionSocket.send(ticket_confirmation.encode("utf-8"))

    print(f"Sent to customer:\n {ticket_confirmation}")
    print("Ready for next ticket...")
    
    if no_more_tickets():
        print("All tickets were sold! Goodbye. Shutting down server.")
        connectionSocket.send("All tickets were sold! Goodbye.".encode("utf-8"))
        connectionSocket.close()
        server_stays_open = False