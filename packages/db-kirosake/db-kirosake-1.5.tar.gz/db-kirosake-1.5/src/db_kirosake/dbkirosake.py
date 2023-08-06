from github import Github
import json
import asyncio

class DBError(Exception):
    def __init__(self,message):
        super().__init__(message)

class DBKirosake():
    def __init__(self,access_token,repository):
        self.access_token=access_token
        self.repository=repository
        self.repo=Github(access_token).get_repo(repository)

    
    async def create_db(self,nameDB=None,folder=None,ids=None,database=None):
        if nameDB==None:
            raise DBError('Name database is not entered')
            return
        if folder==None:
            file=f'{str(nameDB)}/users.json'
        else:
            file=f'{str(nameDB)}/{str(folder)}/users.json'
        if ids==None:
            raise DBError('Folder to database file is not init')
            return
        if database==None:
            raise DBError('Content with database file is not')
            return
       
        try:
            file_content=self.repo.get_contents(file)
            db=file_content.decoded_content.decode()
            db=json.loads(db)
            if str(ids) in db:
                pass
            else:
                db[ids]=database
            json_object=json.dumps(db,indent=4)
            file_content = self.repo.get_contents(file)
            self.repo.update_file(file_content.path,'update', json_object, file_content.sha)
            return db
        except:
            db={}
            db[ids]=database
            json_object = json.dumps(db, indent = 4)
            self.repo.create_file(file,'init commit',json_object)
            return 'Create file {file.path}'


    async def insert_one(
        self,nameDB=None,
        folder=None,ids=None,
        insert=None,value=None,method=None):
            
        if nameDB==None:
            raise DBError('Name database is not entered')
            return
        if folder==None:
            file=f'{str(nameDB)}/users.json'
        else:
            file=f'{str(nameDB)}/{str(folder)}/users.json'
        if ids==None:
            raise DBError('Folder to database file is not init')
            return
        if insert==None:
            raise DBError('Content with database file is not')
            return
        if value==None:
            raise DBError('Value insert to file is not')
            return
        
        try:
            file_content=self.repo.get_contents(file)
            db=file_content.decoded_content.decode()
            db=json.loads(db)
            
            if method is None or method=='a' or method=='add':
                if isinstance(value, int) or isinstance(value, float):
                    db[str(ids)][str(insert)]=db[str(ids)][str(insert)]+value
                else:
                    db[str(insert)]=value
            elif method=='r' or method=='replace':
                if isinstance(value, int) or isinstance(value, float):
                    db[str(ids)][str(insert)]=value
                else:
                    db[str(insert)]=value
                    
            json_object=json.dumps(db,indent=4)
            
            self.repo.update_file(file_content.path,'comm', json_object, file_content.sha)
            return db
        except:
            raise DBError('Error')
        
        
    async def insert_many(
        self,nameDB=None,
        folder=None,ids=None,
        inserts=None,):
        if nameDB==None:
            raise DBError('Name database is not entered')
            return
        if folder==None:
            file=f'{str(nameDB)}/users.json'
        else:
            file=f'{str(nameDB)}/{str(folder)}/users.json'
        if ids==None:
            raise DBError('Folder to database file is not init')
            return
        if inserts==None:
            raise DBError('Content with database file is not')
            return
        
        try:
            file_content=self.repo.get_contents(file)
            db=file_content.decoded_content.decode()
            db=json.loads(db)
            
            for objectDB in inserts:
                try:
                    if inserts[objectDB][1]=='a' or inserts[objectDB][1]=='add':
                        db[str(ids)][str(objectDB)]+=inserts[objectDB][0]
                    elif inserts[objectDB][1]=='r' or inserts[objectDB][1]=='replace':
                        db[str(ids)][str(objectDB)]=inserts[objectDB][0]
                    #print(db[str(ids)][str(objectDB)])
                    
                except:
                    raise DBError(f"Object '{objectDB}' not found in database")
                    return
            json_object=json.dumps(db,indent=4)
            
            self.repo.update_file(file_content.path,'comm', json_object, file_content.sha)
            return db
        except:
            raise DBError('Error')
            
            
    async def get_sorted(self,nameDB=None,folder=None,key=None,reverse=True):
        if nameDB==None:
            raise DBError('Name database is not entered')
            return
        if folder==None:
            file=f'{str(nameDB)}/users.json'
        else:
            file=f'{str(nameDB)}/{str(folder)}/users.json'
        if key==None:
            raise DBError('Key with database file is not')
            return
        try:
            file_content=self.repo.get_contents(file)
            db=file_content.decoded_content.decode()
            db=json.loads(db)
            sortedDB=sorted(db.items(), key=lambda x: x[1][str(key)], reverse=reverse)
            return sortedDB
        except:
            raise DBError('Error')
            return


    async def get(self,nameDB=None,folder=None,ids=None):
        if nameDB==None:
            raise DBError('Name database is not entered')
            return
        if folder==None:
            file=f'{str(nameDB)}/users.json'
        else:
            file=f'{str(nameDB)}/{str(folder)}/users.json'
        
        file_content=self.repo.get_contents(file)
        db=file_content.decoded_content.decode()
        db=json.loads(db)
        if ids==None:
            return db
        else:
            return db[str(ids)]
        
    async def datainfo(self,nameDB=None,folder=None,ids=None):
        if nameDB==None:
            raise DBError('Name database is not entered')
            return
        if folder==None:
            file=f'{str(nameDB)}/users.json'
        else:
            file=f'{str(nameDB)}/{str(folder)}/users.json'
        if ids==None:
            raise DBError('Key with database file is not')
            return
        file_content=self.repo.get_contents(file)
        db=file_content.decoded_content.decode()
        db=json.loads(db)
        infoDB=[
            ('size_KB',file_content.size/1000),
            ('len',len(db))
        ]
        return infoDB
       
    async def deleted(self,nameDB=None,folder=None,ids=None):
        if nameDB==None:
            raise DBError('Name database is not entered')
            return
        if folder==None:
            file=f'{str(nameDB)}/users.json'
        else:
            file=f'{str(nameDB)}/{str(folder)}/users.json'
        if ids==None:
            raise DBError('Key with database file is not')
            return
        file_content=self.repo.get_contents(file)
        db=file_content.decoded_content.decode()
        db=json.loads(db)
        db.pop(str(ids))
        json_object=json.dumps(db,indent=4)
        
        self.repo.update_file(file_content.path,'comm', json_object, file_content.sha)