# -*- coding: utf-8 -*-
# readline_test.py
import os

def hugoToJekyll():
    githubHome = '/Users/juilcho/workspace/github/hahafamilia.github.io'
    d1 = os.listdir(githubHome + '/docs')
    for d in d1:
        # print(d)
        if '.md' in d: continue
        d2 = os.listdir(githubHome + '/docs/' + d)
        for f in d2:
            rname =  d + '/' + f
            wname = "./" + rname + "2"
            fw = open(wname, 'w')
            fr = open(rname, 'r')
            fw.write('---\n')
            fw.write('layout: default\n')
            fw.write('nav_exclude: true\n')
            fw.write('parent: ' + d + '\n')
            lines = fr.readlines()
            start = None
            for line in lines[1:]:
                if 'date' in line or 'hidden' in line:
                    continue
                fw.write(line)
            fr.close()
            fw.close
            os.remove(rname)
            os.rename(wname, rname)

def removeWithoutIndex():
    githubHome = '/Users/juilcho/workspace/github/hahafamilia.github.io'
    d1 = os.listdir(githubHome + '/docs')
    for d in d1:
        # print(d)
        if '.md' in d: continue
        d2 = os.listdir(githubHome + '/docs/' + d)
        for f in d2:
            rname =  d + '/' + f
            # if 'index.md' not in rname: 
            #     os.remove(rname)
            if '_index.md' in rname: 
                os.remove(rname)


if __name__ == '__main__':
    # removeWithoutIndex()
    hugoToJekyll()
# /Users/juilcho/workspace/github/hahafamilia.github.io/script/migration.py