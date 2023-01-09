from cassandra.cluster import Cluster

# class DatabaseError(Exception):
#     """
#     The base error that functions in this module will raise when things go
#     wrong.
#     """
#     pass


# class NotFound(DatabaseError):
#     pass


# class InvalidDictionary(DatabaseError):
#     pass

class ProductCQL:
    
    cluster=Cluster(['127.0.0.1'])
    session =cluster.connect()
    m=['media1', 'media player dj200usb pinto','media']
    sp=session.prepare("SELECT * FROM model1.product_list1 WHERE pname = ?")
    # def __init__(self,d):
        # CREATE_PROCUST="CREATE TABLE model1.product_list1 ( pname text ,color text , category text , dname text ,pid uuid , required_iteams frozen<set <text >> ,PRIMARY KEY (pname , required_iteams, color  )) WITH CLUSTERING ORDER BY (required_iteams ASC ) ;"
    def getd(self):
        f=[]
        rf=[]
        for pname in self.m:
            ff=self.session.execute_async(self.sp,(pname,))
            f.append(ff)
        for rpname in f:
            r1=rpname.result()
            # if not r1:
                # raise NotFound("user not found")
            rf.append(r1.all())
        self.rr=self.session.execute("SELECT * FROM model1.product_list1;")
        return [r for r in rf]
if __name__ == "__main__":
    p=ProductCQL()
    print(p.getd())