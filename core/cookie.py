class Cookie:
    def __init__(self):
        self.__cookie = {}

    def set(self, name, value, maxAge=None,expires=None,
            domain=None, path='/', httpOnly=None, sameSite='Lax', secure=None):
        
        cookie = f'Set-Cookie: {name}={value}; Path={path}'

        if maxAge:
            cookie += f'; Max-Age={maxAge}'
        if expires:
            cookie += f'; Expires={expires}'
        if domain:
            cookie += f'; Domain={domain}'
        if httpOnly:
            cookie += f'; HttpOnly'
        if secure:
            cookie += f'; Secure'

        if sameSite == None:
            cookie += '; SameSite=None'
            if not secure:
                cookie += '; Secure'
        else:
            cookie += f'; SameSite={sameSite}'
        
        
        self.__cookie[name] = cookie

    @property
    def isEmpty(self):
        if self.__cookie == {}:
            return True
        return False

    def get(self, name):
        return self.__cookie[name]
    
    def get_all(self):
        return self.__cookie
    
    def to_string(self):
        return '\r\n'.join([self.__cookie[key] for key in self.__cookie.keys()])
    
    @staticmethod
    def parse(raw_cookies):
        if raw_cookies == None:
            return {}

        cookies = {}
        for cookie in raw_cookies.split(';'):
            name, value = cookie.strip().split('=')
            cookies[name] = value
        return cookies