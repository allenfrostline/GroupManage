# GroupManage

GroupManage 是我在 [wxpy](https://github.com/youfou/wxpy) 基础上的一个minimal的封装，只完成了一种功能：微信群踢人。具体来说，是根据群名片（如果没有则为用户本身微信名）筛选需要删除/保留的群成员，然后进行一键踢人。所有操作都在终端根据指令完成，且需要群主权限。支持 Python 版本为 3.x。另外，短时间内微信首次登陆将自动缓存，所以可以多次登陆。

具体界面略（没来得及存下来。。。）