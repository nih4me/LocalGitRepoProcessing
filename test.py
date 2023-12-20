from git import Repo
from git.cmd import Git

import json
import sys, getopt

PROG_NAME = sys.argv[0]

# Results
results = {}

def get_commit_ids(repo_path, skip=None, outputDir=None):
    repo = Repo(repo_path)
    commits = []
    data = repo.git.execute(['git', 'log', '--pretty=oneline'])
    for c in data.split('\n'):
        c = str(c)
        if skip != None:
            p = False
            for s in skip.split(','):
                if s in c:
                    p = True
                    continue
            if p:
                continue
        c = c.split(' ')
        c = {
            'id': c[0],
            'message': ' '.join(c[1:])
        }
        commits.append(c)
    if outputDir != None:
        with open(outputDir, 'w', encoding='utf-8') as f:
            json.dump(commits, f, ensure_ascii=False, indent=4)
    return commits

def main(argv):
    repo_path = './uemacs'
    skip = 'fix,bug'
    output_dir = None
    try:
        opts, args = getopt.getopt(argv, 'hr:s:i:o:', ['help', 'repo', 'skip', 'input', 'output'])
    except getopt.GetoptError:
        print('%s -r <repo dir> -s <skip keywords> -o <output directory>' % (PROG_NAME))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('%s -r <repo dir> -s <skip keywords> -o <output directory>' % (PROG_NAME))
            sys.exit()
        elif opt in ('-r', '--repo'):
            repo_path = arg
        elif opt in ('-s', '--skip'):
            skip = arg
        elif opt in ('-o', '--output'):
            output_dir = arg

    commits = get_commit_ids(repo_path, skip=skip, outputDir=output_dir)
    print(commits)

if __name__ == '__main__':
    main(sys.argv[1:])