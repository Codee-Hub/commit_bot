from git import Repo, Actor
from datetime import datetime, timedelta
import random
import argparse
import os

def generate_commits(days, max_commits, no_weekends, github_user, github_email):
    repo = Repo('.')
    commit_date_format = "%Y-%m-%d %H:%M:%S"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    repo.config_writer().set_value('user', 'name', github_user).release()
    repo.config_writer().set_value('user', 'email', github_email).release()
    
    if not os.path.exists('commit.txt'):
        with open('commit.txt', 'w') as f:
            f.write('Initial commit file.')

    current_date = start_date
    author = Actor(github_user, github_email)
    while current_date <= end_date:
        if no_weekends and current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue
        
        num_commits = random.randint(1, max_commits)
        for _ in range(num_commits):
            with open('commit.txt', 'a') as f:
                f.write(f'\nCommit on {current_date.strftime("%Y-%m-%d")}')
            repo.index.add(['commit.txt'])
            commit_message = f"Automated commit on {current_date.strftime('%Y-%m-%d')}"
            commit_date = current_date.strftime(commit_date_format)
            repo.index.commit(
                commit_message, 
                author=author, 
                committer=author, 
                author_date=commit_date,
                commit_date=commit_date
            )
        
        current_date += timedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate commits')
    parser.add_argument('--days', type=int, default=365, help='Number of days to generate commits for')
    parser.add_argument('--max_commits', type=int, default=10, help='Maximum number of commits per day')
    parser.add_argument('--no_weekends', action='store_true', help='Skip weekends')
    parser.add_argument('--github_user', required=True, help='GitHub username')
    parser.add_argument('--github_email', required=True, help='GitHub email')
    
    args = parser.parse_args()
    
    generate_commits(args.days, args.max_commits, args.no_weekends, args.github_user, args.github_email)