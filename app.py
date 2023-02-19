from flask import Flask, jsonify, request

app = Flask(__name__)

# Define a route to handle incoming ticket requests
@app.route('/ticket', methods=['POST'])
def assign_ticket():
    # Get the ticket data from the request body
    ticket_data = request.json

    # Assign the ticket to the next available person based on Round Robin Principle
    assigned_to = round_robin_assign()

    # Update the assigned person's list of tickets
    people[assigned_to]['tickets'].append(ticket_data)

    # Return a JSON response with the assigned person's ID
    return jsonify({'assigned_to': assigned_to})

# Define a data model for the ticket and user objects
class Ticket:
    def __init__(self, ticket_id, issue_description, assigned_to, raised_by):
        self.ticket_id = ticket_id
        self.issue_description = issue_description
        self.assigned_to = assigned_to
        self.raised_by = raised_by

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.tickets = []

# Create a data store for the user objects
people = {
    '1': User('1', 'John'),
    '2': User('2', 'Jane'),
    '3': User('3', 'Bob'),
    '4': User('4', 'Alice'),
    '5': User('5', 'Steve')
}

# Implement Round Robin Principle to assign tickets to people
def round_robin_assign():
    for user_id in people.keys():
        if not people[user_id]['tickets']:
            return user_id
    # If all people have tickets assigned, start over from the beginning
    first_user_id = next(iter(people))
    return first_user_id

# Define a route to retrieve the list of tickets assigned to a user
@app.route('/user/<user_id>', methods=['GET'])
def get_user_tickets(user_id):
    if(request.method == 'GET'):
        return jsonify({'tickets': people[user_id]['tickets']})

if __name__ == "__main__":
    app.run(debug=True)