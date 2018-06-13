import pip

try:  # check if wxpy is installed
    __import__('wxpy')
except:  # otherwise pip install wxpy
    pip.main(['install', 'wxpy'])

from wxpy import *


NO = ['N', 'n', 'No', 'no', 'NO']
YES = ['Y', 'y', 'Yes', 'yes', 'YES']


def getYN(prompt):
    YN = ''
    ALL = YES + NO
    while YN not in ALL:
        YN = input(prompt)
    return YN


class GM:
    def __init__(self):
        self.bot = Bot(cache_path=True)  # Bot initialized

    def run(self):
        return self.search_group() and self.delete_or_keep() and self.search_member() and self.sayounara()

    def search_group(self):
        group_name = input('请输入群名关键词：')
        group_list = self.bot.groups().search(group_name)
        len_group = len(group_list)
        if len_group == 0:
            YN = getYN('没有匹配到任何微信群。重新尝试？[Y/N] ')
            if YN in YES:
                return self.search_group()
            else:
                return False
        elif len_group == 1:
            self.group = group_list[0]
            print('匹配成功：{}'.format(self.group.name))
            return True
        else:
            print('共匹配到 {} 个群：'.format(len_group))
            valid_index = [str(i + 1) for i in range(len_group)]
            for i, group in zip(valid_index, group_list):
                print('[{}] {}'.format(i, group.name))
            selected_index = input('请选择：')
            while selected_index not in valid_index:
                YN = getYN('选项错误，请在 1 - {} 中选择。重新尝试？[Y/N] '.format(len_group))
                if YN in NO:
                    return False
                else:
                    selected_index = input('请选择：')
            selected_index = int(selected_index)
            self.group = group_list[selected_index - 1]
            print('匹配成功：{}'.format(self.group.name))
            return True

    def delete_or_keep(self):
        print('请选择操作：')
        valid_index = ['1', '2']
        print('[1] 根据关键词删除群成员')
        print('[2] 根据关键词保留群成员')
        selected_index = input('请选择：')
        while selected_index not in valid_index:
            YN = getYN('选项错误，请在 1 - 2 中选择。重新尝试？[Y/N] ')
            if YN in NO:
                return False
            else:
                selected_index = input('请选择：')
        self.dok = int(selected_index)
        return True

    def search_member(self):
        if self.dok == 1:
            member_name = input('请输入群成员关键词：')
        else:
            member_name = input('请输入群成员关键词：')
        self.members = self.group.members.search(member_name)
        n_members = len(self.members)
        if n_members == 0:
            YN = getYN('没有匹配到任何群成员。重新尝试？[Y/N] ')
            if YN in YES:
                return self.search_member()
            else:
                return False
        else:
            enum = getYN('匹配成功：被选中群成员共 {} 名，是否全部打印？[Y/N] '.format(len(self.members)))
        if enum in YES:
            for member in self.members:
                print(member.name)
        return True

    def sayounara(self):
        n_rm = len(self.members) if self.dok == 1 else len(self.group.members) - len(self.members) - 1
        YN = getYN('确认执行删除 {} 名群成员的操作？[Y/N] '.format(n_rm))
        if YN in YES:
            if self.dok == 1:
                self.group.remove_members(self.members)
                print('操作成功：共 {} 名群成员被删除，余 {} 人'.format(n_rm, len(self.group.members) - n_rm))
            else:
                names = [member.name for member in self.members] + [self.bot.self.name]
                rm = [member for member in self.group.members if member.name not in names]
                self.group.remove_members(rm)
                print('操作成功：共 {} 名群成员被删除，余 {} 人'.format(n_rm, len(self.group.members) - n_rm))
            return True
        else:
            return False


gm = GM()
try:
    result = gm.run()
except:
    result = False
if result:
    print('完毕，哔哔（˵˚ ω ˚˵）')
else:
    print('再见了您嘞（╯ ‵ □′）╯︵┴─┴')
