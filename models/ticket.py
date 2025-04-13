from datetime import datetime
from database.db_connection import DatabaseConnection

class Ticket:
    def __init__(self, data=None):
        self.id = data.get('id') if data else None
        self.type_id = data.get('type_id', 2)  
        self.user_i = data.get('user_i', 4)
        self.client_id = data.get('client_id', 0)
        self.source_id = data.get('source_id', 4)
        self.department_id = data.get('department_id', 1)
        self.reason_id = data.get('reason_id', 2)  # Новое подключение
        self.reason_text = data.get('reason_text', 'Новое подключение')
        self.date_add = data.get('date_add', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.info = data.get('info')
        self.ext_info = data.get('ext_info', 'Заявка от продажника')
        self.phone = data.get('phone')
        
        self.performer_id = data.get('performer_id', 1)  
        self.result_id = data.get('result_id', 0) 

        self.status_id = data.get('status_id', 1) 
        
        self.city_id = data.get('city_id', 51) 
        self.tech_comment = data.get('tech_comment', 0) 
        self.other_comment = data.get('other_comment', 0) 
        self.removed = data.get('removed', 0) 
        self.created_at = data.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.updated_at = data.get('updated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))



    @classmethod
    def create(cls, ticket_data):
        db = DatabaseConnection()
        try:
            db.connect()
            
            query = """
            INSERT INTO requests 
            (
            type_id, 
            user_id, 
            client_id, 
            source_id, 
            department_id, 
            reason_id, 
            reason_text, 
            date_add, 
            info, 
            ext_info, 
            phone, 
            performer_id, 
            result_id, 
            status_id, 
            city_id,
            tech_comment, 
            other_comment, 
            removed, 
            created_at, 
            updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                ticket_data.type_id,
                ticket_data.user_i,
                ticket_data.client_id,
                ticket_data.source_id,
                ticket_data.department_id,
                ticket_data.reason_id,
                ticket_data.reason_text,
                ticket_data.date_add,
                ticket_data.info,
                ticket_data.ext_info,
                ticket_data.phone,
                ticket_data.performer_id,
                ticket_data.result_id,
                ticket_data.status_id,
                ticket_data.city_id,
                ticket_data.tech_comment,
                ticket_data.other_comment,
                ticket_data.removed,
                ticket_data.created_at,
                ticket_data.updated_at
            )
            
            ticket_id = db.execute_query(query, params)
            ticket_data.id = ticket_id
            return ticket_data
        finally:
            db.disconnect()