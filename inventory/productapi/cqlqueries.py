from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory
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
    session.row_factory=dict_factory    
    m=['media1', 'media player dj200usb pinto','media']
    sp=session.prepare("SELECT dname , pid FROM model1.product_list1 WHERE pname = ?")
    # def __init__(self,d):
        # CREATE_PROCUST="CREATE TABLE model1.product_list1 ( pname text ,color text , category text , dname text ,pid uuid , required_iteams frozen<set <text >> ,PRIMARY KEY (pname , required_iteams, color  )) WITH CLUSTERING ORDER BY (required_iteams ASC ) ;"
    def get_product(self):
        f=[]
        rf=[]
        for pname in self.m:
            ff=self.session.execute_async(self.sp,(pname,))
            f.append(ff)
        for rpname in f:
            r1=rpname.result()
            # if not r1:
                # raise NotFound("user not found")
            rf.append(r1.one())
        self.rr=self.session.execute("SELECT * FROM model1.product_list1;")
        return [r for r in rf]
    
    def prduct_list(self):
        sp= self.session.prepare("SELECT dname , pid FROM model1.product_list1 WHERE pname = ?")
        a=self.session.execute("SELECT dname , pid FROM model1.product_list1 ;")
        return a.all()
if __name__ == "__main__":
    p=ProductCQL()
    # print(p.getd())
    print(p.prduct_list())