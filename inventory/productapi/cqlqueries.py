from cassandra.cluster import Cluster
a=12
class ProductCQL:
    aa=a
    cluster=Cluster(['127.0.0.1'])
    session =cluster.connect()
    rr=None
    m=['media','media1', 'media player dj200usb pinto']
    session.prepare("SELECT * FROM model1.product_list WHERE pname = ?")
    # def __init__(self,d):
        # CREATE_PROCUST="CREATE TABLE model1.product_list1 ( pname text ,color text , category text , dname text ,pid uuid , required_iteams frozen<set <text >> ,PRIMARY KEY (pname , required_iteams, color  )) WITH CLUSTERING ORDER BY (required_iteams ASC ) ;"
    def getd(self):
        f=[]
        for pname in 
        self.rr=self.session.execute("SELECT * FROM model1.product_list1;")
        return set([r.pname for r in self.rr])
if __name__ == "__main__":
    p=ProductCQL()
    print(p.getd())
    print(p.getd())
    p1=ProductCQL()
    print(p1.getd())
        