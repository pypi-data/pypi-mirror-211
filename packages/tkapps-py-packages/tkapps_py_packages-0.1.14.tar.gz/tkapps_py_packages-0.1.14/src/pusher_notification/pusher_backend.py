import uuid
import pusher, os,requests,time


class Notify:
    def __init__(self):
        self.pusher_client = pusher.Pusher(
            app_id=os.getenv('PUSHER_APP_ID'),
            key=os.getenv('PUSHER_KEY'),
            secret=os.getenv('PUSHER_SECRET'),
            cluster=os.getenv('PUSHER_CLUSTER'),
            ssl=True)

    def check_online_status(self,username):
        user_status = self.pusher_client.channel_info(f'private-{username}')
        status = user_status.get('occupied', False)
        return status

    def send_message(self,username,event_name,message):
        self.pusher_client.trigger(f'private-{username}', event_name, {'message': message})

    def store_data(self,username,event_name,message):
        data = {"id":str(uuid.uuid4()),"username": username,"is_read": False, "timestamp": time.time(), "message": message,"event":event_name}
        x = requests.post(os.getenv('ES_URL'), json=data)

    def trigger_pusher(self,username,event_name,message):
        try:
            is_user_online=self.check_online_status(username)
            if is_user_online:
                self.send_message(username,event_name,message)
            else:
                self.store_data(username,event_name,message)
        except Exception as err:
            print("notification could not be triggered as: {}".format(str(err)))
