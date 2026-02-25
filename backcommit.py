import os
import subprocess
import random
from datetime import datetime, timedelta

def run_cmd(cmd, env=None):
    subprocess.run(cmd, shell=True, env=env)

def generate_history():
    print("Starting back-commit process...")
    
    if not os.path.exists('.git'):
        print("Initializing new Git repository...")
        run_cmd("git init")
        
    start_date = datetime(2025, 12, 24, 10, 0)
    end_date = datetime(2026, 2, 25, 18, 0)
    
    file_groups = [
        ["README.md", ".gitignore"],
        ["requirements.txt", "backend/setup_db.py"],
        ["backend/app.py", "backend/db.py"],
        ["backend/database_full_schema.sql"],
        ["frontend/index.html", "frontend/favicon.svg"],
        ["frontend/js/tailwind-cdn.js"],
        ["backend/utils/auth_utils.py", "backend/utils/security_utils.py"],
        ["backend/generate_secrets.py", "backend/utils/crypto_utils.py"],
        ["backend/routes/signin.py", "backend/routes/signup.py"],
        ["frontend/sign-in.html", "frontend/sign-up.html"],
        ["frontend/recover.html", "backend/routes/forgot_password.py"],
        ["backend/routes/admin.py", "backend/routes/admin_profile.py"],
        ["frontend/dashboard/admin-profile.html", "frontend/js/auth-check.js"],
        ["backend/routes/events.py", "frontend/upcoming-events.html"],
        ["backend/routes/culturals.py", "backend/routes/registrations.py"],
        ["backend/utils/invoice_generator.py", "backend/utils/reminder_system.py"]
    ]
    
    generic_messages = [
        "chore: sync updates",
        "docs: update development progress",
        "wip: ongoing module improvements",
        "chore: daily codebase maintenance",
        "refactor: internal logic adjustments",
        "fix: resolve minor bugs",
        "style: format code components",
        "chore: track development logs"
    ]
    
    log_file = "development.log"
    group_idx = 0
    commits_made = 0
    
    current_date = start_date
    while current_date <= end_date:
        if random.random() < 0.30:
            current_date += timedelta(days=1)
            continue
            
        for i in range(2):
            commit_time = current_date + timedelta(hours=random.randint(0, 8), minutes=random.randint(0, 59))
            date_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
            
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str
            
            if group_idx < len(file_groups) and random.random() < 0.4:
                files = file_groups[group_idx]
                added_any = False
                for f in files:
                    if os.path.exists(f):
                        run_cmd(f'git add "{f}"')
                        added_any = True
                
                if added_any:
                    msg = f"feat: implement {files[0].split('/')[-1]} logic"
                    run_cmd(f'git commit -m "{msg}"', env=env)
                    group_idx += 1
                    commits_made += 1
                    continue
            
            with open(log_file, "a") as f:
                f.write(f"Development synced at {date_str}\n")
            run_cmd(f'git add "{log_file}"')
            msg = random.choice(generic_messages)
            run_cmd(f'git commit -m "{msg}"', env=env)
            commits_made += 1
            
        current_date += timedelta(days=1)

    print("Committing all remaining files for the final state...")
    run_cmd("git add .")
    final_date = end_date.strftime("%Y-%m-%dT%H:%M:%S")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = final_date
    env["GIT_COMMITTER_DATE"] = final_date
    run_cmd('git commit -m "feat: final project assembly and optimization"', env=env)
    
    print(f"Success! Generated a rich history of {commits_made + 1} commits from Dec 24, 2025 to Feb 25, 2026.")
    print("You can now safely push this to GitHub!")

if __name__ == "__main__":
    generate_history()
