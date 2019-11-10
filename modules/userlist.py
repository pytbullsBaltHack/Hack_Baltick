
class VisitorState(object):
    id = 0
    lastframe = None
    registered = False
    
    def __init__(self,id,frameid):
        self.id = id
        self.lastframe = frameid
        self.registered = False
        return
    

class UserList(object):
    base = []

    def __init__(self):
        self.base = []
        return
        
    def addvisitor(self,uid,frameid):
        self.base.append(VisitorState(uid,frameid))
        
        return
        
    def checkvisitor(self,uid,frameid):
        for u in self.base:
            if(u.id == uid):
                dist = frameid - u.lastframe
                
                if(dist > 40):
                    u.registered = True
                    
                u.lastframe = frameid
                return u.registered
                
        return False
    