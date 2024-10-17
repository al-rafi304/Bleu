import threading
import uuid
import time

class Session:
    def __init__(self, manager, id, data=None):
        self.id = id
        self.data = {} if data == None else data
        self.created_at = time.time()
        self.__manager = manager

    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __getitem__(self, key):
        return self.data[key]
    
    def get(self, key):
        return self.data.get(key)

    def destroy(self):
        self.__manager.destroy_session(self.id)
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

    def __init__(self, secret=None, expire = 86400):
        if not self._initialized:
            self.secret = secret
            self.__sessions = {}
            self.expire = expire

            self._initialized = True
    
    def get_session(self, id):
        return self.__sessions.get(id)
    
    def create_session(self):
        id = self.__gen_id()
        session = Session(manager=self, id=id)
        print("Created session: ", session.data)
        self.__sessions[id] = session
        return session
    
    def destroy_session(self, id):
        session = self.__sessions.get(id)
        print(f"Deleting session: {id}\nData: {session.data}")
        if not session:
            raise KeyError(f"Key '{id}' not found in sessions[]")
        
        del self.__sessions[id]
    
    def middleware(self, req, res, next):
        session_id = req.cookies.get('session')
        session = self.get_session(session_id)

        if session_id and session:
            if self.expire < time.time() - session.created_at:
                self.destroy_session(session.id)
                session = self.create_session()
                res.cookies.set(name='session', value=session.id, maxAge=self.expire)
        else:
            session = self.create_session()
            res.cookies.set(name='session', value=session.id, maxAge=self.expire)
        
        req.session = session

        return next()
    
    def __gen_id(self):
        return str(uuid.uuid4())