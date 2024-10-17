class Cookie:
    def __init__(self):
        self.__cookies = {}

    def set(self, name, value, maxAge=None,expires=None,
            domain=None, path=None, httpOnly=None, sameSite='Lax', secure=None):
        
        cookie = {
            name: value
        }

        if path:
            cookie['Path'] = str(path)
        if maxAge:
            cookie['Max-Age'] = str(maxAge)
        if expires:
            cookie['Expires'] = str(expires)
        if domain:
            cookie['Domain'] = str(domain)
        if httpOnly:
            cookie['HttpOnly'] = True
        if secure:
            cookie['Secure'] = True

        if sameSite == None:
            cookie['SameSite'] = 'None'
            if not secure:
                cookie['Secure'] = True
        else:
            cookie['SameSite'] = str(sameSite)
        
        
        self.__cookies[name] = cookie

    @property
    def isEmpty(self):
        if self.__cookies == {}:
            return True
        return False

    def __getitem__(self, key):
        return self.__cookies[key]
    
    def __str__(self):
        return str(self.__cookies)
    
    def get(self, key):
        return self.__cookies.get(key)
    
    def all(self):
        return self.__cookies
    
    def to_string(self):
        all_cookies = []
        for data in self.__cookies.values():
            cookie = []
            for key, val in data.items():
                if val == True:
                    cookie.append(key)
                else:
                    cookie.append(f'{key}={val}')
            cookie = f'Set-Cookie: ' + '; '.join(cookie)
            all_cookies.append(cookie)
        return '\r\n'.join(all_cookies)
    
    @staticmethod
    def parse(raw_cookies):
        if raw_cookies == None:
            return {}

        cookies = {}
        for cookie in raw_cookies.split(';'):
            if '=' in cookie:
                name, value = cookie.strip().split('=')
            else:
                name = cookie.strip()
                value = True
            cookies[name] = value
        return cookies