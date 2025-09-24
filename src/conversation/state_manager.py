# src/conversation/state_manager.py

class ConversationManager:
    """
    Manages the state and flow of the lead qualification conversation.
    """
    def __init__(self):
        # Define the conversation flow as a series of states
        self.flow = {
            'START': {
                'message': "Hi there! Welcome to Serri - I'm Zen. To start, what industry are you in?",
                'next_state': 'AWAITING_INDUSTRY'
            },
            'AWAITING_INDUSTRY': {
                'save_as': 'industry',
                'message': "Got it. And how many employees does your company have? (e.g., 1-50, 51-250, 250+)",
                'next_state': 'AWAITING_SIZE'
            },
            'AWAITING_SIZE': {
                'save_as': 'company_size',
                'message': "Thanks. Are you the decision-maker for automation solutions?",
                'next_state': 'AWAITING_AUTHORITY'
            },
            'AWAITING_AUTHORITY': {
                'save_as': 'is_decision_maker',
                'message': "Great. And which of these best describes your needs? (Lead Generation, Sales Automation, Customer Support, or All)",
                'next_state': 'AWAITING_NEEDS'
            },
            'AWAITING_NEEDS': {
                'save_as': 'needs',
                'message': "Awesome! It sounds like Serri could be a great fit. Let's schedule your free demo. You can click on 'Book a Demo' in the top-right.",
                'next_state': 'QUALIFIED_COMPLETE'
            },
            'QUALIFIED_COMPLETE': {
                'message': "Is there anything else I can help you with? You can ask me any question about Serri's features.",
                'next_state': 'END' # Or loop back to a general Q&A state
            },
        }

    def handle_message(self, session: dict, user_message: str) -> dict:
        """
        Processes a user's message based on their current conversation state.

        Args:
            session (dict): The user's current session {'state': str, 'data': dict}.
            user_message (str): The message from the user.

        Returns:
            dict: The updated session.
        """
        current_state = session.get('state', 'START')

        if current_state in self.flow:
            state_info = self.flow[current_state]

            # Save the user's previous answer if needed
            if 'save_as' in state_info:
                session['data'][state_info['save_as']] = user_message

            # Prepare the next message and update the state
            session['response'] = state_info['message']
            session['state'] = state_info['next_state']
        else:
            # If the state is unknown or the flow is finished, provide a default response
            session['response'] = "I'm not sure how to respond to that. Can you please clarify?"
        
        return session
    
# src/conversation/state_manager.py

class ConversationManager:
    def __init__(self):
        self.flow = {
            'START': {
                'message': ("Hi there! Welcome to Serri - I'm Zen. How can I assist you today?\n"
                            "1. Tell me about Serri\n"
                            "2. How can Serri help my business?\n"
                            "3. Schedule a Demo"),
                'next_state': 'AWAITING_MENU_CHOICE'
            },
            'AWAITING_MENU_CHOICE': {
                'handler': self.handle_menu_choice
            },
            'AWAITING_INDUSTRY': {
                'save_as': 'industry',
                'message': "Got it. And how many employees does your company have? (e.g., 1-50, 51-250, 250+)",
                'next_state': 'AWAITING_SIZE'
            },
            'AWAITING_SIZE': {
                'save_as': 'company_size',
                'message': "Thanks. Are you the decision-maker for automation solutions?",
                'next_state': 'AWAITING_AUTHORITY'
            },
            'AWAITING_AUTHORITY': {
                'save_as': 'is_decision_maker',
                'message': "Great. Which of these best describes your needs? (Lead Generation, Sales Automation, Customer Support, or All)",
                'next_state': 'AWAITING_NEEDS'
            },
            'AWAITING_NEEDS': {
                'save_as': 'needs',
                'message': "Awesome! It sounds like Serri could be a great fit. Let's schedule your free demo. You can click on 'Book a Demo' in the top-right.",
                'next_state': 'QUALIFIED_COMPLETE'
            },
            'QUALIFIED_COMPLETE': {
                'message': "Is there anything else I can help you with? You can ask me any question about Serri's features.",
                'next_state': 'GENERAL_QA'
            },
        }

    def handle_menu_choice(self, session: dict, user_message: str) -> dict:
        """Handles the user's selection from the main menu."""
        choice = user_message.strip()
        if '1' in choice or 'tell me' in choice.lower():
            session['state'] = 'GENERAL_QA'
            session['response'] = "Of course. What would you like to know about Serri?"
        elif '2' in choice or 'help my business' in choice.lower():
            # Start the qualification flow
            next_state_info = self.flow['AWAITING_INDUSTRY']
            session['state'] = 'AWAITING_SIZE' # Set state for the *next* step
            session['response'] = next_state_info['message']
        elif '3' in choice or 'schedule' in choice.lower():
            session['state'] = 'QUALIFIED_COMPLETE'
            session['response'] = "Great! You can schedule a demo by clicking the 'Book a Demo' link."
        else:
            session['response'] = "Sorry, I didn't understand that. Please choose an option from the menu."
        return session

    def handle_message(self, session: dict, user_message: str) -> dict:
        current_state = session.get('state', 'START')

        if current_state in self.flow:
            state_info = self.flow[current_state]
            
            if 'handler' in state_info:
                # Use a dedicated handler function for complex logic like menus
                session = state_info['handler'](session, user_message)
            else:
                # Standard state transition
                if 'save_as' in state_info:
                    session['data'][state_info['save_as']] = user_message
                session['response'] = state_info['message']
                session['state'] = state_info['next_state']
        else:
            session['response'] = "I'm not sure how to respond to that."
        
        return session