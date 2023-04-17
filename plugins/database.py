from datetime import datetime
import time
from info import DB2

class Database:

    def __init__(self, db1):
        self.db1 = db1
        self.col = self.db1.admins
        self.fls = self.db1.acc

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.now().isoformat(),
            db_status=dict(
                db_name = "SWAHILI GROUP MEDIA",
                descp = "Tunahusika na uuzaji wa muvi na sizon kal zilizotafsiriwa kwa bei ",
                phone_no = "0 halopesa https://t.me/swahiliupdates hrm45",
                ms_link= "link",
                muda = "kuipakua mda wowote bila kikomo...",
                g_1=  "hrm45",
                g_2 = "hrm45",
                g_3 = "hrm45",
                g_4 = "hrm45",
                g_5 = "hrm45",
                g_6 = "hrm45",
            ),
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.now().isoformat(),
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
                banned_on=datetime.now().isoformat(),
            )
        )
    async def add_acc(self, id,user_id,file_id,db_name,tme):
        user = self.new_acc(id,int(user_id),file_id,db_name,tme)
        await self.fls.insert_one(user)

    async def add_admin(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_admin_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def is_email_exist(self, id):
        filter={'user_id': int(id)}
        user = await self.fls.find_one(filter)
        return True if user else False

    async def is_acc_exist(self, id,file_id,db_name):
        filter={'user_id': int(id)}
        filter["file_id"]= file_id
        filter["db_name"]= int(db_name)
        user = await self.fls.find_one(filter)
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def get_all_acc(self):
        all_users = self.fls.find({})
        return all_users

    async def delete_acc(self, id):
        await self.fls.delete_many({'id': id})

    async def get_user(self,id):
        all_users = self.col.find({'id': id})
        return all_users

    async def get_acc(self,id):
        all_users = self.fls.find({'user_id': int(id)})
        return all_users

    async def delete_admin(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration= 0,
            banned_on=datetime.now().isoformat(),
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason,link):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.now().isoformat(),
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status,'db_status.ms_link':link}})
    async def get_db_status(self, id):
        default =dict(
                db_name = "SWAHILI GROUP MEDIA",
                descp = "Tunahusika na uuzaji wa muvi na sizon kal zilizotafsiriwa kwa bei chee",
                phone_no = "0 hrm45 halopesa",
                ms_link= "link",
                muda = "kuipakua mda wowote bila kikomo...",
                g_1= "hrm45",
                g_2 = "hrm45",
                g_3 = "hrm45",
                g_4= "hrm45",
                g_5 = "hrm45",
                g_6 = "hrm45",
            )
        user = await self.col.find_one({'id': int(id)})
        return user.get('db_status', default)
    async def update_db(self, user_id,ghi,ab):
        ab1,ab2=ghi.split(" ",1)
        ab[ab1] = ab2
        update_admin =dict(
                db_name = ab["db_name"],
                descp = ab["descp"],
                phone_no = ab["phone_no"],
                ms_link = ab["ms_link"],
                muda = ab["muda"],
                g_1 = ab["g_1"],
                g_2 = ab["g_2"],
                g_3 = ab["g_3"],
                g_4 = ab["g_4"],
                g_5 = ab["g_5"],
                g_6 = ab["g_6"],
            )
        await self.col.update_one({'id': user_id}, {'$set': {'db_status': update_admin}})
    
    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.now().isoformat(),
            ban_reason=''
        )
        user = await self.col.find_one({'id': int(id)})
        return user.get('ban_status', default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users


db = Database(DB2)
