import datetime

class memory:

    def __init__(self, max_history=5):
        """Initialisation de la memoire (Pour chaque utilisateur)"""
        self.conversations = {}
        self.max_history = max_history
        self.last_message_time = {} 

    def manage(self, user_id, message_content):
        """Gestion de la memoire (Pour chaque utilisateur)"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        self.conversations[user_id].append(message_content) 
        self.last_message_time[user_id] = datetime.datetime.now()
        if user_id in self.conversations and len(self.conversations[user_id]) > 10:
         del self.conversations[user_id][:10]  
        if len(self.conversations[user_id]) > self.max_history:
         del self.conversations[user_id][:self.max_history] 
        context = self.conversations[user_id]
        self.conversations[user_id].append(context) 
        self.conversations[user_id] = self.conversations[user_id][-self.max_history:]
        return context
    
    def clear_context(self, inactive_time_threshold=3600):
            """Netoyage du cahe (Pour chaque utilisateur)"""
            current_time = datetime.datetime.now()
            inactive_users = [user_id for user_id, last_message_time in self.last_message_time.items()
                if (current_time - last_message_time).total_seconds() > inactive_time_threshold]
            for user_id in inactive_users:
               del self.conversations[user_id]
               del self.last_message_time[user_id]

    def get_history(self, user_id): 
        """Recuperer l'historie d'un utilisateur"""
        return self.conversations.get(user_id, []) 