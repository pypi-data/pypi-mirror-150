import nonebot
import time
import json
import pathlib
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Event, FriendRequestEvent
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, on_request
#from nonebot import get_driver
#from .config import Config                         这三条待开发ing~
#plugin_config = Config.parse_obj(get_driver().config)

# 获取超寄用户的id
super_id = nonebot.get_driver().config.superusers


# 超级用户推送添加机器人好友请求事件
add_friend = on_request(priority=1, block=True)


@add_friend.handle()
async def add_friend(event: FriendRequestEvent):
    try:
        with open(pathlib.Path(__file__).with_name("set.json"), "r", encoding="utf-8") as f:
            obj = json.load(f)
        qq = obj["add_qq_req_list"]["qq"]
        add_req = json.loads(event.json())
        add_qq = add_req["user_id"]
        qq.append(add_qq)
        comment = add_req["comment"]
        flag = add_req["flag"]
        realtime = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(add_req["time"]))
        obj["add_qq_req_list"]["qq"] = qq
        obj["add_qq_req_list"]["flag"] = flag
        with open(pathlib.Path(__file__).with_name("set.json"), "w", encoding="utf-8") as f1:
            json.dump(obj, f1, indent=4)
        for su_qq in super_id:
            await nonebot.get_bot().send_msg(user_id=int(su_qq),
                                             message=f"QQ：{add_qq}请求添加罐头为好友!\n请求添加时间：{realtime}\n验证信息为：{comment}")
    except Exception as e:
        for su_qq in super_id:
            await nonebot.get_bot().send_msg(user_id=int(su_qq), message=f"罐头坏掉了\n错误信息：{e}")

# 超级用户使用，同意好友添加机器人请求
agree_qq_add = on_command("同意", permission=SUPERUSER)


@agree_qq_add.handle()
async def agree_qq_add(event: Event):
    try:
        with open(pathlib.Path(__file__).with_name("set.json"), "r", encoding="utf-8") as f:
            obj = json.load(f)
        qq = obj["add_qq_req_list"]["qq"]
        flag = obj["add_qq_req_list"]["flag"]
        user_id = int(event.get_user_id())
        agree_id = int(str(event.get_message()).split("同意")[-1])          #在QQ上同意时请加上申请人QQ号
        if agree_id in qq:
            await nonebot.get_bot().send(user_id=user_id, message=f"机器人成功添加QQ:{agree_id}为好友！", event=event)
            await nonebot.get_bot().set_friend_add_request(flag=flag, approve=True, remark="")
            qq.remove(agree_id)
            flag = ""
            obj["add_qq_req_list"]["qq"] = qq
            obj["add_qq_req_list"]["flag"] = flag
            with open(pathlib.Path(__file__).with_name("set.json"), "w", encoding="utf-8") as f1:
                json.dump(obj, f1, indent=4)

        else:
            await nonebot.get_bot().send(user_id=user_id, message=f"QQ:{agree_id}不在好友申请列表！", event=event)
    except Exception as e:
        for su_qq in super_id:
            await nonebot.get_bot().send_msg(user_id=int(su_qq), message=f"罐头出错了\n错误信息：{e}")