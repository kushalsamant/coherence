import requests
import json

# Get commits for the file
commits_url = "https://api.github.com/repos/kushalsamant/kushalsamant.github.io/commits?path=docs/history.md&per_page=5"
response = requests.get(commits_url)
commits = response.json()

output = []
output.append(f"Found {len(commits)} commits for history.md")
output.append("\n" + "="*80 + "\n")

# Get file content from each commit
for i, commit in enumerate(commits):
    sha = commit['sha']
    message = commit['commit']['message']
    date = commit['commit']['author']['date']
    
    output.append(f"Commit {i+1}: {sha[:7]}")
    output.append(f"Message: {message}")
    output.append(f"Date: {date}")
    
    # Get file content at this commit
    file_url = f"https://api.github.com/repos/kushalsamant/kushalsamant.github.io/contents/docs/history.md?ref={sha}"
    file_response = requests.get(file_url)
    
    if file_response.status_code == 200:
        file_data = file_response.json()
        import base64
        content = base64.b64decode(file_data['content']).decode('utf-8')
        output.append(f"\nContent ({len(content)} chars):")
        output.append("-" * 80)
        output.append(content)
        output.append("-" * 80)
        
        # Save the first (most recent) commit's content
        if i == 0:
            with open('docs/history.md', 'w', encoding='utf-8') as f:
                f.write(content)
            output.append(f"\n✓ Saved most recent version to docs/history.md")
    else:
        output.append(f"Could not fetch file content: {file_response.status_code}")
    
    output.append("\n" + "="*80 + "\n")
    if i >= 2:  # Only show first 3 commits
        break

# Write output to file
with open('history_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('\n'.join(output))
