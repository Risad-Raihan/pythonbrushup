# text_renderer.py
# ------------------------------------------------------------
# Converts structured research JSON into a styled .txt report
# ------------------------------------------------------------

from typing import Dict, List


LINE_WIDTH = 60
DIVIDER = "-" * LINE_WIDTH
HEADER = "=" * LINE_WIDTH


class TextRenderer:
    def render(self, data: Dict) -> str:
        """
        Render structured research data into a styled text report.
        """

        lines: List[str] = []

        # --------------------------------------------------
        # Header
        # --------------------------------------------------
        lines.append(HEADER)
        lines.append(data["title"].upper())
        lines.append(HEADER)
        lines.append("")

        # --------------------------------------------------
        # Query
        # --------------------------------------------------
        lines.append("QUERY")
        lines.append("-----")
        lines.append(data["query"])
        lines.append("")

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------
        lines.append("SUMMARY")
        lines.append("-------")
        lines.extend(self._wrap_text(data["summary"]))
        lines.append("")

        # --------------------------------------------------
        # Sections
        # --------------------------------------------------
        for idx, section in enumerate(data["sections"], start=1):
            lines.append(DIVIDER)
            lines.append(f"SECTION {idx} — {section['heading'].upper()}")
            lines.append("-" * (len(lines[-1])))
            
            # Simple bullet section
            if "points" in section:
                for point in section["points"]:
                    lines.append(f"• {point}")

            # Subsection-based section
            elif "subsections" in section:
                for subsection in section["subsections"]:
                    lines.append(f"[{subsection['label'].upper()}]")
                    for point in subsection["points"]:
                        lines.append(f"• {point}")
                    lines.append("")

            lines.append("")

        # --------------------------------------------------
        # Sources
        # --------------------------------------------------
        lines.append(DIVIDER)
        lines.append("SOURCES")
        lines.append("-------")

        for idx, source in enumerate(data["sources"], start=1):
            lines.append(f"[{idx}] {source['title']}")
            lines.append(f"    {source['url']}")
            lines.append("")

        # --------------------------------------------------
        # Footer
        # --------------------------------------------------
        lines.append(HEADER)
        lines.append("END OF REPORT")
        lines.append(HEADER)

        return "\n".join(lines)

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _wrap_text(self, text: str) -> List[str]:
        """
        Wrap long text into terminal-friendly lines.
        """
        words = text.split()
        lines = []
        current = []

        for word in words:
            if len(" ".join(current + [word])) <= LINE_WIDTH:
                current.append(word)
            else:
                lines.append(" ".join(current))
                current = [word]

        if current:
            lines.append(" ".join(current))

        return lines
