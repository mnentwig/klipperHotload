def demotest(self, gcmd):
    self.log("demotest")
    
def funA(self, gcmd): 
    CHECK = gcmd.get("CHECK", default=None)

    ourId = "a/b/funA"
    if CHECK is not None:
        if CHECK != ourId:
            raise gcmd.error("expected "+CHECK+" but called "+ourId)
    self.log("called "+ourId)    

def funB(self, gcmd): 
    CHECK = gcmd.get("CHECK", default=None)

    ourId = "a/b/funB"
    if CHECK is not None:
        if CHECK != ourId:
            raise gcmd.error("expected "+CHECK+" but called "+ourId)
    self.log("called "+ourId)    