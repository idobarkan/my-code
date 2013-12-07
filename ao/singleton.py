class singleton(object):
    """See Python cookbook (2nd edition) receipe 6.15 - Implementing the "Singleton" Design Pattern"""
    def __new__(cls,*a,**kw):
        """Make it a singleton"""
        if '_inst' not in vars(cls):
            cls._inst = super(singleton,cls).__new__(cls,*a,**kw)
        return cls._inst
