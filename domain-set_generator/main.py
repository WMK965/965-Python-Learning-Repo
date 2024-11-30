import os


domesticlist = 'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/ChinaMax/ChinaMax_Domain.txt'
oversealist = 'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Global/Global_Domain.txt'

os.system(f'curl -o -k --ssl-no-revoke ./domestic-ori.txt {domesticlist}')
os.system(f'curl -o -k --ssl-no-revoke ./oversea-ori.txt {oversealist}')


def modifyconf(ori, out):
    with open(ori, 'r') as f:
        lines = f.readlines()
        f2 = open(out, 'w')
        for line in lines:
            if line[0] == '#':
                continue
            elif line[0] == '.':
                f2.write(line[1:])
            else:
                f2.write(line)
        f2.close()


modifyconf('domestic-ori.txt', 'domestic_domainlist.conf')
modifyconf('oversea-ori.txt', 'oversea_domainlist.conf')
