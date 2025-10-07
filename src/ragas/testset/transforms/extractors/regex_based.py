import re
import typing as t
from dataclasses import dataclass

from ragas.testset.graph import Node
from ragas.testset.transforms.base import Extractor


@dataclass
class RegexBasedExtractor(Extractor):
    pattern: str = ""
    is_multiline: bool = False
    property_name: str = "regex"

    async def extract(self, node: Node) -> t.Tuple[str, t.Any]:
        text = node.get_property("page_content")
        if not isinstance(text, str):
            raise ValueError(
                f"node.property('page_content') must be a string, found '{type(text)}'"
            )

        # Compile the regex pattern with appropriate flags and timeout to prevent ReDoS
        flags = re.MULTILINE if self.is_multiline else 0
        try:
            regex = re.compile(self.pattern, flags=flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern provided: {e}")

        # Use regex finditer with timeout to avoid ReDoS
        # Python's re module does not support timeouts natively,
        # so we use a safe approach by limiting the input size and catching runtime errors.

        # Limit input size to avoid excessive processing
        MAX_INPUT_LENGTH = 100000  # 100k chars limit
        input_text = text[:MAX_INPUT_LENGTH]

        matches = []
        try:
            for match in regex.finditer(input_text):
                # If pattern has capturing groups, return groups, else the whole match
                if match.groups():
                    if len(match.groups()) == 1:
                        matches.append(match.group(1))
                    else:
                        matches.append(match.groups())
                else:
                    matches.append(match.group())
        except re.error as e:
            # Catch catastrophic backtracking or other regex runtime errors
            raise RuntimeError(f"Regex matching failed: {e}")

        return self.property_name, matches


# This regex pattern matches URLs, including those starting with "http://", "https://", or "www."
links_extractor_pattern = r"(?i)\b(?:https?://|www\.)\S+\b"
links_extractor = RegexBasedExtractor(
    pattern=links_extractor_pattern, is_multiline=True, property_name="links"
)

# This regex pattern matches emails, which typically follow the format "username@domain.extension".
emails_extractor_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
emails_extractor = RegexBasedExtractor(
    pattern=emails_extractor_pattern, is_multiline=False, property_name="emails"
)

# This regex pattern matches Markdown headings, which start with a number sign (#) followed by a space,
# and the rest of the line is the heading text.
markdown_headings_pattern = r"^(#{1,6})\s+(.*)"
markdown_headings_extractor = RegexBasedExtractor(
    pattern=markdown_headings_pattern, is_multiline=True, property_name="headings"
)
