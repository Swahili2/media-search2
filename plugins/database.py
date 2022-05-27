import datetime
from info import DB2

class Database:

    def __init__(self, db1):
        self.db1 = db1
        self.col = self.db1.admins
        self.fls = self.db1.acc

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            descp = True,
            ban_status=dict(
                status = 'normal',
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )
    def new_acc(self, id,user_id,file_id,db_name,tme):
        return dict(
            id=id,
            user_id=user_id,
            file_id = file_id,
            db_name = db_name,
            ban_status=dict(
                ban_duration=tme,
                banned_on=datetime.date.today().isoformat(),
            )
        )
    async def add_acc(self, id):
        user = self.new_acc(id,user_id,file_id,db_name,tme)
        await self.fls.insert_one(user)
    async def add_admin(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_admin_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False
   
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users
    async def get_user(self,id):
        all_users = self.col.find({'id': id})
        return all_users
    
    async def delete_admin(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            status = 'normal',
            is_banned=False,
            ban_duration= 0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason,sts):
        ban_status = dict(
            status = sts,
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            status = 'normal',
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        user = await self.col.find_one({'id': int(id)})
        return user.get('ban_status', default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users


db = Database(DB2)
