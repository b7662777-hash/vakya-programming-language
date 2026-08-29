"""Vākya Mini Browser Engine.

Parses HTML tokens, constructs DOM tree representations, and provides
navigation history controls and text-mode layout formatting.
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from .http_client import fetch_url


@dataclass
class DOMNode:
    tag: str
    text: str = ""
    attrs: Dict[str, str] = field(default_factory=dict)
    children: List["DOMNode"] = field(default_factory=list)

    def is_text_node(self) -> bool:
        return self.tag == "#text"

    def count_nodes(self) -> int:
        count = 1
        for child in self.children:
            count += child.count_nodes()
        return count


class HTMLParser:
    """Resilient HTML parser for the Mini Browser."""
    SELF_CLOSING = {"br", "hr", "img", "input", "meta", "link"}

    @classmethod
    def parse(cls, html: str) -> DOMNode:
        root = DOMNode(tag="html")
        stack: List[DOMNode] = [root]

        # Token pattern: comments, tags, or text
        token_pattern = re.compile(r"<!--[\s\S]*?-->|<[^>]+>|[^<]+")
        pos = 0

        for match in token_pattern.finditer(html):
            token = match.group(0)

            if token.startswith("<!--"):
                # Skip comments
                continue

            elif token.startswith("</"):
                # Closing tag e.g. </h1>
                tag_name = token[2:-1].strip().lower().split()[0] if token[2:-1].strip() else ""
                # Pop stack until matching tag is found or root is reached
                if len(stack) > 1:
                    idx = len(stack) - 1
                    while idx > 0 and stack[idx].tag != tag_name:
                        idx -= 1
                    if idx > 0:
                        stack = stack[:idx]

            elif token.startswith("<"):
                # Opening or self-closing tag e.g. <h1 class="title">
                raw_tag = token[1:-1].strip()
                if not raw_tag:
                    continue
                parts = raw_tag.split(None, 1)
                tag_name = parts[0].lower().rstrip("/")
                attrs = {}
                if len(parts) > 1:
                    attr_str = parts[1].rstrip("/")
                    attr_matches = re.findall(r'([a-zA-Z0-9_-]+)(?:=["\']([^"\']*)["\'])?', attr_str)
                    for k, v in attr_matches:
                        attrs[k.lower()] = v

                node = DOMNode(tag=tag_name, attrs=attrs)
                stack[-1].children.append(node)

                is_self_closing = raw_tag.endswith("/") or tag_name in cls.SELF_CLOSING
                if not is_self_closing:
                    stack.append(node)

            else:
                # Text node
                text = token.strip()
                if text:
                    # Clean up multiple whitespace
                    clean_text = " ".join(text.split())
                    text_node = DOMNode(tag="#text", text=clean_text)
                    stack[-1].children.append(text_node)

        return root


class MiniBrowserEngine:
    """Coordinates navigation, HTTP fetch, HTML parsing, and DOM rendering."""

    def __init__(self):
        self.history: List[str] = []
        self.current_index: int = -1
        self.current_url: str = ""
        self.current_status: int = 0
        self.current_headers: Dict[str, str] = {}
        self.current_html: str = ""
        self.current_dom: Optional[DOMNode] = None

    def navigate(self, url: str) -> DOMNode:
        url = url.strip()
        status, body, headers = fetch_url(url)

        # Truncate forward history on new navigation
        if self.current_index + 1 < len(self.history):
            self.history = self.history[: self.current_index + 1]

        self.history.append(url)
        self.current_index = len(self.history) - 1
        self.current_url = url
        self.current_status = status
        self.current_headers = headers
        self.current_html = body
        self.current_dom = HTMLParser.parse(body)
        return self.current_dom

    def back(self) -> Optional[DOMNode]:
        if self.can_go_back():
            self.current_index -= 1
            url = self.history[self.current_index]
            status, body, headers = fetch_url(url)
            self.current_url = url
            self.current_status = status
            self.current_headers = headers
            self.current_html = body
            self.current_dom = HTMLParser.parse(body)
            return self.current_dom
        return None

    def forward(self) -> Optional[DOMNode]:
        if self.can_go_forward():
            self.current_index += 1
            url = self.history[self.current_index]
            status, body, headers = fetch_url(url)
            self.current_url = url
            self.current_status = status
            self.current_headers = headers
            self.current_html = body
            self.current_dom = HTMLParser.parse(body)
            return self.current_dom
        return None

    def reload(self) -> Optional[DOMNode]:
        if self.current_url:
            status, body, headers = fetch_url(self.current_url)
            self.current_status = status
            self.current_headers = headers
            self.current_html = body
            self.current_dom = HTMLParser.parse(body)
            return self.current_dom
        return None

    def can_go_back(self) -> bool:
        return self.current_index > 0

    def can_go_forward(self) -> bool:
        return self.current_index + 1 < len(self.history)

    def render_text_view(self) -> str:
        """Format the parsed DOM tree into a clean terminal/text representation."""
        if not self.current_dom:
            return "(No page loaded)"

        lines: List[str] = []

        def traverse(node: DOMNode, depth: int = 0):
            if node.tag == "#text":
                if node.text:
                    lines.append("  " * depth + node.text)
                return

            if node.tag in ("h1", "h2", "h3"):
                lines.append("")
                heading_marker = "#" * (int(node.tag[1]) + 1)
                text_content = " ".join(c.text for c in node.children if c.tag == "#text")
                lines.append(f"{heading_marker} {text_content}".strip())
                for child in node.children:
                    if child.tag != "#text":
                        traverse(child, depth)
                return

            if node.tag == "p":
                lines.append("")
                for child in node.children:
                    traverse(child, depth)
                return

            if node.tag == "li":
                lines.append("  * " + " ".join(c.text for c in node.children if c.tag == "#text"))
                for child in node.children:
                    if child.tag != "#text":
                        traverse(child, depth + 1)
                return

            if node.tag == "a":
                href = node.attrs.get("href", "#")
                text = " ".join(c.text for c in node.children if c.tag == "#text") or href
                lines.append(f"[{text}]({href})")
                return

            for child in node.children:
                traverse(child, depth)

        traverse(self.current_dom)
        return "\n".join(lines).strip()
