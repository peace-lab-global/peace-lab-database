#!/usr/bin/env python3
"""
Fix remaining broken links using directory-level file matching.
For each broken link, look at actual files in the same directory and find the best match.
"""
import os, re, sys
from difflib import SequenceMatcher

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SKIP_DIRS = {'.git', '.venv', '.qoder', '.claude', '.github', '__pycache__',
             'node_modules', '.pages', '.storybook', '.playwright-cli'}


def get_words(name):
    """Extract lowercase words from a name (CamelCase, snake_case, hyphenated)."""
    # Remove extension
    name = re.sub(r'\.\w+$', '', name)
    # Split on hyphens and underscores
    segments = re.split(r'[-_]', name)
    words = []
    for seg in segments:
        parts = re.findall(r'[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|[0-9]+', seg)
        words.extend([p.lower() for p in parts if p])
    return words


def similarity(a, b):
    """Quick similarity score between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def build_dir_file_map(directory):
    """Return list of .md files in a directory (not recursive)."""
    if not os.path.isdir(directory):
        return []
    try:
        return [f for f in os.listdir(directory) if f.endswith('.md') and f != 'INDEX.md']
    except:
        return []


def find_best_match(old_name, candidates):
    """Find the best matching file among candidates for an old filename."""
    old_base = re.sub(r'\.\w+$', '', old_name)
    old_words = set(get_words(old_base))
    
    if not old_words:
        return None
    
    best_score = 0
    best_match = None
    
    for cand in candidates:
        cand_base = re.sub(r'\.\w+$', '', cand)
        cand_words = set(get_words(cand_base))
        
        # Word overlap score
        if not cand_words:
            continue
        overlap = len(old_words & cand_words)
        union = len(old_words | cand_words)
        word_score = overlap / union if union > 0 else 0
        
        # Also try character-level similarity on the full names
        char_score = similarity(old_base, cand_base)
        
        # Combined score (weighted towards word overlap)
        score = 0.6 * word_score + 0.4 * char_score
        
        if score > best_score and score > 0.3:
            best_score = score
            best_match = cand
    
    return best_match if best_score > 0.3 else None


def main():
    sections = [d for d in os.listdir(BASE) if re.match(r'^0[1-7]-', d)]
    
    total_fixed = 0
    total_links_fixed = 0
    
    for section in sections:
        section_dir = os.path.join(BASE, section)
        for root, dirs, files in os.walk(section_dir):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if not f.endswith('.md'):
                    continue
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                except:
                    continue
                
                original = content
                links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
                file_links_fixed = 0
                
                for text, path in links:
                    if path.startswith('http') or path.startswith('#') or path.startswith('mailto:'):
                        continue
                    clean_path = path.split('#')[0]
                    fragment = path[len(clean_path):]
                    if not clean_path:
                        continue
                    
                    resolved = os.path.normpath(os.path.join(root, clean_path))
                    exists = (os.path.exists(resolved) or
                             os.path.exists(resolved + '.md') or
                             os.path.exists(os.path.join(resolved, 'INDEX.md')))
                    if exists:
                        continue
                    
                    # Broken link - try to fix
                    segments = clean_path.rstrip('/').split('/')
                    trailing_slash = clean_path.endswith('/')
                    
                    # Process segments
                    new_segments = []
                    current_base = root
                    any_fixed = False
                    
                    for seg_idx, seg in enumerate(segments):
                        if not seg or seg == '.' or seg == '..':
                            new_segments.append(seg)
                            if seg == '..':
                                current_base = os.path.dirname(current_base)
                            continue
                        
                        candidate = os.path.join(current_base, seg)
                        if os.path.exists(candidate) or os.path.exists(candidate + '.md'):
                            new_segments.append(seg)
                            if os.path.isdir(candidate):
                                current_base = candidate
                            continue
                        
                        # Try to find match among siblings
                        is_last = (seg_idx == len(segments) - 1)
                        
                        if os.path.isdir(current_base):
                            siblings = os.listdir(current_base)
                            
                            # Filter to relevant type
                            if is_last and seg.endswith('.md'):
                                # Looking for a file
                                file_siblings = [s for s in siblings if s.endswith('.md') and s != 'INDEX.md']
                                match = find_best_match(seg, file_siblings)
                                if match:
                                    new_segments.append(match)
                                    any_fixed = True
                                    continue
                            elif is_last and not seg.endswith('.md'):
                                # Could be a directory or file without .md
                                dir_siblings = [s for s in siblings if os.path.isdir(os.path.join(current_base, s))]
                                # Try exact-ish match first
                                seg_lower = seg.lower().replace('-', '').replace('_', '')
                                for d in dir_siblings:
                                    d_lower = d.lower().replace('-', '').replace('_', '')
                                    if d_lower == seg_lower:
                                        new_segments.append(d)
                                        current_base = os.path.join(current_base, d)
                                        any_fixed = True
                                        break
                                else:
                                    # Try fuzzy match
                                    match = find_best_match(seg, dir_siblings)
                                    if match:
                                        new_segments.append(match)
                                        current_base = os.path.join(current_base, match)
                                        any_fixed = True
                                        continue
                                    # Also try file match
                                    file_siblings = [s for s in siblings if s.endswith('.md')]
                                    match = find_best_match(seg + '.md', file_siblings)
                                    if match:
                                        new_segments.append(match)
                                        any_fixed = True
                                        continue
                            else:
                                # Middle segment - looking for directory
                                dir_siblings = [s for s in siblings if os.path.isdir(os.path.join(current_base, s))]
                                seg_lower = seg.lower().replace('-', '').replace('_', '')
                                for d in dir_siblings:
                                    d_lower = d.lower().replace('-', '').replace('_', '')
                                    if d_lower == seg_lower:
                                        new_segments.append(d)
                                        current_base = os.path.join(current_base, d)
                                        any_fixed = True
                                        break
                                else:
                                    match = find_best_match(seg, dir_siblings)
                                    if match:
                                        new_segments.append(match)
                                        current_base = os.path.join(current_base, match)
                                        any_fixed = True
                                        continue
                        
                        new_segments.append(seg)
                    
                    if any_fixed:
                        new_path = '/'.join(new_segments)
                        if trailing_slash and not new_path.endswith('/'):
                            new_path += '/'
                        new_path += fragment
                        old_link = f'[{text}]({path})'
                        new_link = f'[{text}]({new_path})'
                        content = content.replace(old_link, new_link)
                        file_links_fixed += 1
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as fh:
                        fh.write(content)
                    total_fixed += 1
                    total_links_fixed += file_links_fixed
    
    print(f"Files with links fixed: {total_fixed}")
    print(f"Total links fixed: {total_links_fixed}")
    
    # Verify remaining broken links
    broken_count = 0
    for section in sections:
        for root, dirs, files in os.walk(os.path.join(BASE, section)):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                if f != 'INDEX.md':
                    continue
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                except:
                    continue
                links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
                for text, path in links:
                    if path.startswith('http') or path.startswith('#') or path.startswith('mailto:'):
                        continue
                    clean_path = path.split('#')[0]
                    if not clean_path:
                        continue
                    resolved = os.path.normpath(os.path.join(root, clean_path))
                    exists = (os.path.exists(resolved) or
                             os.path.exists(resolved + '.md') or
                             os.path.exists(os.path.join(resolved, 'INDEX.md')))
                    if not exists:
                        broken_count += 1
    
    print(f"Remaining broken links in INDEX.md: {broken_count}")


if __name__ == '__main__':
    main()
