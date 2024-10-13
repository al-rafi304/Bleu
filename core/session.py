import threading
import uuid
import time

class Session:
    def __init__(self, manager, id, data:dict={}):
        self.id = id
        self.data = data
        self.expire = 86400
        self.created_at = time.time()
        self.__manager = manager
    
    def get(self, key):
        return self.data.get(key)
    
    def add(self, key, value):
        self.data[key] = value

    def destory(self):
        self.__manager.destory(self.id)
        return None

class SessionManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, secret=None):
        if not self._initialized:
            self.secret = secret
            self.__sessions = {}

            self._initialized = True
    
    def get_session(self, id):
        return self.__sessions.get(id)
    
    def create_session(self):
        id = self.__gen_id()
        session = Session(manager=self, id=id)
        self.__sessions[id] = session
        return session
    
    def destroy_session(self, id):
        session = self.__sessions.get(id)
        print(f"Deleting session: {id}\nData: {session}")
        if not session:
            raise KeyError(f"Key '{id}' not found in sessions[]")
        
        del self.__sessions[id]
    
    def middleware(self, req, res, next):
        session_id = req.cookie.get('session')
        session = self.get_session(session_id)
        expired = req.session.expire < time.time() - req.session.created_at

        if session_id and session:
            if expired:
                self.destroy_session(session.id)
                session = self.create_session(req)
                res.set_cookie(name='session', value=session.id)
            req.session = session
        else:
            session = self.create_session()
            res.set_cookie(name='session', value=session.id)
            req.session = session

        next()
    
    def __gen_id(self):
        return str(uuid.uuid4())