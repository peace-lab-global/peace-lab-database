import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..'))
DOCS_DIR = os.path.join(SCRIPT_DIR, 'docs')

SKIP = {
    '.git', '.venv', 'node_modules', '__pycache__', 'site',
    'Visualization', '.claude', '.codebuddy', '.qoder', '.trae',
    'Tools', 'Project', '_meta', 'Web', '.DS_Store',
}

MD_FILES = {'README.md', 'TAXONOMY.md', 'GLOSSARY.md', 'CONTRIBUTING.md'}

os.makedirs(DOCS_DIR, exist_ok=True)

for entry in os.listdir(DOCS_DIR):
    p = os.path.join(DOCS_DIR, entry)
    if os.path.islink(p):
        os.remove(p)

for name in sorted(os.listdir(REPO_ROOT)):
    if name in SKIP or name.startswith('.') or name.startswith('W') or name == '.pages':
        continue
    src = os.path.join(REPO_ROOT, name)
    dst = os.path.join(DOCS_DIR, name)
    if os.path.isdir(src):
        rel = os.path.relpath(src, DOCS_DIR)
        os.symlink(rel, dst)
        print(f"  linked dir: {name}")
    elif name in MD_FILES:
        rel = os.path.relpath(src, DOCS_DIR)
        os.symlink(rel, dst)
        print(f"  linked file: {name}")

index_src = os.path.join(SCRIPT_DIR, '..', 'landing.md')
index_dst = os.path.join(DOCS_DIR, 'index.md')
# Only create symlink if index.md does not already exist as a real file
if not os.path.exists(index_dst):
    if os.path.exists(index_src):
        rel = os.path.relpath(os.path.abspath(index_src), DOCS_DIR)
        os.symlink(rel, index_dst)
        print(f"  linked landing page")
else:
    print(f"  skipped: index.md already exists")

print("Done.")
