#!/usr/bin/env python3
"""
ERA-Engine API Documentation Generator

Reads C# source files with XML doc comments and generates
MkDocs-compatible Markdown API reference pages.

Usage:
    uv run python3 gen_api_docs.py <source_dir> <output_dir>
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass, field

# ---- Data models ----

@dataclass
class ParamDoc:
    name: str
    description: str

@dataclass
class MemberDoc:
    name: str
    kind: str            # "method", "property", "field"
    declaration: str      # Full declaration line (e.g. "public static T GetOrAddNode<T>(Node parent)")
    return_type: str      # Return type (e.g. "T", "void", "Array<string>")
    summary: str
    params: list[ParamDoc] = field(default_factory=list)
    returns: str = ""
    remarks: str = ""
    example: str = ""
    access_modifier: str = "public"
    is_static: bool = False
    is_obsolete: bool = False
    obsolete_msg: str = ""

@dataclass
class TypeDoc:
    name: str
    kind: str            # "class", "struct", "enum", "interface"
    full_name: str
    summary: str
    remarks: str = ""
    example: str = ""
    base_type: str = ""
    members: list[MemberDoc] = field(default_factory=list)

@dataclass
class NamespaceDoc:
    name: str
    types: list[TypeDoc] = field(default_factory=list)


# ---- XML comment parser ----

def parse_xml_comment(text: str) -> dict:
    """Parse /// XML doc comment text."""
    result = {"summary": "", "remarks": "", "example": "", "returns": "", "params": []}

    lines = []
    for line in text.split('\n'):
        s = line.strip()
        if s.startswith('///'):
            s = s[3:].strip()
        lines.append(s)
    xml = '\n'.join(lines)

    tags = ['summary', 'remarks', 'example', 'returns']
    for tag in tags:
        m = re.search(f'<{tag}>(.*?)</{tag}>', xml, re.DOTALL)
        if m:
            result[tag] = _clean_inline(m.group(1))

    for m in re.finditer(r'<param\s+name="([^"]*)"\s*>(.*?)</param>', xml, re.DOTALL):
        result["params"].append(ParamDoc(name=m.group(1), description=_clean_inline(m.group(2))))
    for m in re.finditer(r'<param\s+name="([^"]*)"\s*/>', xml):
        result["params"].append(ParamDoc(name=m.group(1), description=""))

    return result


def _clean_inline(text: str) -> str:
    text = re.sub(r'<see\s+cref="([^"]+)"\s*/>', r'`\1`', text)
    text = re.sub(r'<c>([^<]*)</c>', r'`\1`', text)
    text = re.sub(r'<paramref\s+name="([^"]+)"\s*/>', r'`\1`', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


# ---- C# declaration patterns ----

CLASS_PAT = re.compile(
    r'public\s+(partial\s+)?(static\s+)?(abstract\s+)?(sealed\s+)?'
    r'(class|struct|enum|interface)\s+(\w+)'
    r'(?:\s*:\s*([^{]+?))?(?=\s*[\s{]|$)'
)

# Match the full method declaration including access modifier
FULL_METHOD_PAT = re.compile(
    r'(public|private|protected|internal)\s+'
    r'(static\s+)?(override\s+)?(async\s+)?'
    r'(partial\s+)?'
    r'([\w<>\[\],\s?]+)\s+'            # return type (capture more chars for generics)
    r'(\w+(?:<[^>]*>)?)\s*\(([^)]*)\)'  # method name and params
)

PROPERTY_PAT = re.compile(
    r'(public|private|protected|internal)\s+'
    r'(static\s+)?'
    r'([\w<>\[\]]+)\s+'
    r'(\w+)\s*\{\s*(get|init)'
)


# ---- File parsing ----

def parse_file(filepath: Path) -> list[TypeDoc]:
    content = filepath.read_text(encoding='utf-8')
    ns_match = re.search(r'namespace\s+([\w.]+)\s*[;{]', content)
    namespace = ns_match.group(1) if ns_match else "(Global)"
    lines = content.split('\n')

    # Phase 1: index all /// comment blocks
    comments = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('///'):
            start = i
            raw = []
            while i < len(lines) and lines[i].strip().startswith('///'):
                s = lines[i].strip()
                if s.startswith('///'):
                    s = s[3:]
                raw.append(s)
                i += 1
            parsed = parse_xml_comment('\n'.join(raw))
            comments.append((start, i - 1, parsed))
        else:
            i += 1

    # Phase 2: scan all type declarations
    types = []
    for i, line in enumerate(lines):
        cm = CLASS_PAT.search(line)
        if not cm:
            continue
        kind = cm.group(5)
        name = cm.group(6)
        base_raw = cm.group(7) or ''
        base_types = []
        for bt in base_raw.split(','):
            bt = bt.strip()
            if bt and bt not in ('class', 'struct', 'enum', 'interface') and not bt.startswith('where'):
                base_types.append(bt)

        summary = ""
        remarks = ""
        example = ""
        for ci in range(len(comments) - 1, -1, -1):
            c_start, c_end, c_parsed = comments[ci]
            if c_end >= i - 4 and c_end < i:
                summary = c_parsed.get("summary", "")
                remarks = c_parsed.get("remarks", "")
                example = c_parsed.get("example", "")
                comments.pop(ci)
                break

        td = TypeDoc(
            name=name, kind=kind,
            full_name=f"{namespace}.{name}",
            summary=summary, remarks=remarks, example=example,
            base_type=', '.join(base_types),
        )
        td.members = _parse_members_in_body(lines, i, comments, name)
        types.append(td)

    return types


def _parse_members_in_body(lines, decl_line, comments, class_name):
    members = []

    brace_start = None
    for j in range(decl_line, min(decl_line + 10, len(lines))):
        if '{' in lines[j]:
            brace_start = j
            break
    if brace_start is None:
        return members

    depth = 0
    body_start = None
    for j in range(brace_start, len(lines)):
        depth += lines[j].count('{') - lines[j].count('}')
        if depth >= 1:
            body_start = j + 1
            break
    if body_start is None:
        return members

    depth = 1
    body_end = None
    for j in range(body_start, len(lines)):
        depth += lines[j].count('{') - lines[j].count('}')
        if depth <= 0:
            body_end = j
            break
    if body_end is None:
        body_end = len(lines)

    relevant_comments = []
    remaining = []
    for c in comments:
        c_start, c_end, _ = c
        if c_start >= body_start and c_end <= body_end:
            relevant_comments.append(c)
        else:
            remaining.append(c)
    comments[:] = remaining

    for _, (c_start, c_end, c_parsed) in enumerate(relevant_comments):
        summary = c_parsed.get("summary", "")
        params = c_parsed.get("params", [])
        returns = c_parsed.get("returns", "")
        remarks = c_parsed.get("remarks", "")
        example = c_parsed.get("example", "")

        if not summary and not params and not returns:
            continue

        for look in range(c_end + 1, min(c_end + 5, len(lines))):
            decl = lines[look].strip()

            is_obsolete = False
            obsolete_msg = ""
            if look > 0:
                m = re.search(r'\[Obsolete\("([^"]*)"\)\]', lines[look - 1].strip())
                if m:
                    is_obsolete = True
                    obsolete_msg = m.group(1)

            if decl.startswith('//') or decl.startswith('/*') or decl.startswith('*'):
                continue
            if not decl or decl == '{' or decl == '}':
                continue

            # Method?
            mm = FULL_METHOD_PAT.search(decl)
            if mm:
                method_name = mm.group(7)
                return_type = mm.group(6)
                params_text = mm.group(8)
                access = mm.group(1)
                is_static = bool(mm.group(2) and 'static' in mm.group(2))

                # Filter lifecycle methods
                if method_name in ('_Ready', '_Process', '_EnterTree', '_ExitTree',
                                   '_Input', '_UnhandledInput', '_Notification'):
                    continue

                # Clean return type and store as-is (backticks protect <>)
                return_type = return_type.strip()
                # Build full declaration
                params_text = params_text.strip()
                # Build full declaration
                decl_parts = [access]
                if is_static:
                    decl_parts.append("static")
                decl_parts.append(return_type)
                decl_parts.append(f"{method_name}({params_text})")

                # Handle generic constraints (where T : ...)
                constraint = ""
                for extra in range(look + 1, min(look + 3, len(lines))):
                    extra_line = lines[extra].strip()
                    if extra_line.startswith("where ") or extra_line.startswith("    where "):
                        constraint += " " + extra_line.rstrip(',')
                    elif extra_line.startswith('{') or extra_line.startswith(':') or not extra_line:
                        break
                full_decl = ' '.join(decl_parts) + constraint

                md = MemberDoc(
                    name=method_name, kind="method",
                    declaration=full_decl.strip(),
                    return_type=return_type,
                    summary=summary, params=params, returns=returns,
                    remarks=remarks, example=example,
                    access_modifier=access, is_static=is_static,
                    is_obsolete=is_obsolete, obsolete_msg=obsolete_msg,
                )
                members.append(md)
                break

            # Property?
            pm = PROPERTY_PAT.search(decl)
            if pm:
                prop_name = pm.group(4)
                prop_type = pm.group(3)
                access = pm.group(1)
                is_static = bool(pm.group(2) and 'static' in pm.group(2))

                decl_parts = [access]
                if is_static:
                    decl_parts.append("static")
                decl_parts.append(prop_type)
                decl_parts.append(f"{prop_name} {{ get; }}")

                md = MemberDoc(
                    name=prop_name, kind="property",
                    declaration=' '.join(decl_parts),
                    return_type=_escape_md(prop_type),
                    summary=summary, remarks=remarks, example=example,
                    access_modifier=access, is_static=is_static,
                    is_obsolete=is_obsolete, obsolete_msg=obsolete_msg,
                )
                members.append(md)
                break

    return members


# ---- Markdown generation ----

def _escape(text: str) -> str:
    """Escape for display in regular Markdown text (not code)."""
    return text.replace('<', '&lt;').replace('>', '&gt;').replace('|', '\\|')

def _code(text: str) -> str:
    """Wrap in backticks — do NOT escape <> so they render as angle brackets."""
    return f'`{text}`'

def _indent_continuation(text: str, indent: int = 2) -> str:
    """Indent continuation lines for Markdown list items (blank lines, multiline text)."""
    parts = str(text).split('\n')
    if len(parts) <= 1:
        return text
    pad = ' ' * indent
    return '\n'.join([parts[0]] + [f'{pad}{p}' for p in parts[1:]])


def member_to_md(m: MemberDoc) -> str:
    """Format a method/property as a Markdown subsection."""
    lines = []

    # Obsolete warning
    if m.is_obsolete:
        lines.append(f'> ⚠️ **废弃**: {_escape(m.obsolete_msg or "此成员已废弃")}')
        lines.append('')

    # Full declaration as a fenced code block with syntax highlighting
    lines.append('**声明**')
    lines.append('')
    lines.append('```csharp')
    lines.append(m.declaration)
    lines.append('```')
    lines.append('')

    # Return type
    if m.kind == "method" and m.return_type:
        lines.append(f'**返回类型**: {_code(m.return_type)}')
        lines.append('')

    # Summary
    if m.summary:
        lines.append(f'**说明**: {_escape(m.summary)}')
        lines.append('')

    # Parameters
    if m.params:
        lines.append('**参数**:')
        for p in m.params:
            desc = _escape(p.description) if p.description else ''
            if desc:
                lines.append(f'- {_code(p.name)}: {desc}')
            else:
                lines.append(f'- {_code(p.name)}')
        lines.append('')

    # Return value description
    if m.returns:
        lines.append(f'**返回值**: {_escape(m.returns)}')
        lines.append('')

    # Remarks
    if m.remarks:
        lines.append(f'**备注**: {_escape(m.remarks)}')
        lines.append('')

    # Example
    if m.example:
        lines.append('- **示例**:')
        lines.append('  ```csharp')
        for ln in m.example.split('\n'):
            lines.append(f'  {ln}')
        lines.append('  ```')

    return '\n'.join(lines)


def namespace_to_md(ns: NamespaceDoc) -> str:
    lines = [f"# {ns.name}", '']
    sorted_types = sorted(ns.types, key=lambda t: (
        0 if t.kind == 'class' else 1 if t.kind == 'struct' else 2 if t.kind == 'enum' else 3, t.name
    ))

    for td in sorted_types:
        anchor = td.full_name.replace('.', '-').replace('(', '-').replace(')', '')
        lines.append(f"## `{td.name}` {{#{anchor}}}")
        lines.append('')
        lines.append(f'**类型**: {td.kind}')
        if td.base_type:
            lines.append('')
            lines.append(f'**继承**: {td.base_type}')
        lines.append('')
        if td.summary:
            lines.append(td.summary)
            lines.append('')
        if td.remarks:
            lines.append('??? note "备注"')
            lines.append('')
            lines.append(f'    {_escape(td.remarks)}')
            lines.append('')

        if td.members:
            props = [m for m in td.members if m.kind == 'property']
            methods = [m for m in td.members if m.kind == 'method']

            if props:
                lines.append('---')
                lines.append('### 属性')
                lines.append('')
                for m in props:
                    lines.append(f'#### `{m.name}`')
                    lines.append('')
                    lines.append(member_to_md(m))
                    lines.append('')

            if methods:
                lines.append('---')
                lines.append('### 方法')
                lines.append('')
                for m in methods:
                    lines.append(f'#### `{m.name}`')
                    lines.append('')
                    lines.append(member_to_md(m))
                    lines.append('')

        lines.append('')
        lines.append('---')
        lines.append('')

    return '\n'.join(lines)


def build_index(ns_list):
    lines = [
        '# API 参考',
        '',
        '本章节由工具从源代码中的 XML 文档注释自动生成。',
        '',
        '## 命名空间',
        '',
        '| 命名空间 | 类型数 | 说明 |',
        '|:---------|:------|:-----|',
    ]
    for ns_name, desc, count in sorted(ns_list):
        filename = ns_name.lower().replace('.', '-').replace('(', '').replace(')', '')
        lines.append(f'| [{ns_name}]({filename}.md) | {count} | {desc} |')
    lines.extend(['', '---', '', '> 提示：文档自动生成，与主仓库 `main` 分支同步更新。'])
    return '\n'.join(lines)


# ---- Main ----

def main():
    NS_DESCRIPTIONS = {
        "EraEngine": "引擎根命名空间 — Logger、Utils 工具函数",
        "EraEngine.Core": "引擎核心 — Controller、GameManager、Service、Model 与 View",
    }

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)

    ns_map = {}
    files = sorted(src.rglob("*.cs"))
    files = [f for f in files if not any(p in str(f) for p in ['/obj/', '/bin/', '/Demo-'])]

    print(f"Scanning {len(files)} C# files in {src}...")
    for fp in files:
        try:
            types = parse_file(fp)
            for td in types:
                ns = '.'.join(td.full_name.split('.')[:-1])
                if ns not in ns_map:
                    ns_map[ns] = NamespaceDoc(name=ns)
                ns_map[ns].types.append(td)
        except Exception as e:
            print(f"  ⚠️  {fp.name}: {e}")

    entries = []
    for ns_name in sorted(ns_map.keys()):
        ns = ns_map[ns_name]
        count = len(ns.types)
        total_members = sum(len(t.members) for t in ns.types)
        has_content = any(t.summary or t.members for t in ns.types)
        filename = ns_name.lower().replace('.', '-').replace('(', '').replace(')', '') + ".md"

        if has_content:
            (dst / filename).write_text(namespace_to_md(ns), encoding='utf-8')
            print(f"  📦 {ns_name} ({count} types, {total_members} members) → {filename}")
            entries.append((ns_name, NS_DESCRIPTIONS.get(ns_name, f"{count} 个类型"), count))
        else:
            path = dst / filename
            if path.exists():
                path.unlink()

    idx_path = dst / "index.md"
    if not idx_path.exists():
        idx_path.write_text(build_index(entries), encoding='utf-8')

    print(f"\n✅ 完成！生成 {len(entries)} 个 namespace 页面")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: uv run python3 gen_api_docs.py <source_dir> <output_dir>")
        print("Example: uv run python3 gen_api_docs.py ../era-engine-edb/era-godot/Prototype/CspScript ./docs/api")
        sys.exit(1)
    main()
