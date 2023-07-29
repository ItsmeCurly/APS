DATE_REGEXES = [
    r"\b\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2]\d|3[0-1])\b",
    r"\b(?:0[1-9]|[1-2]\d|3[0-1])/(?:0[1-9]|1[0-2])/\d{4}\b",
    r"\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[1-2]\d|3[0-1])/\d{4}\b",
    r"\b\d{4}/(?:0[1-9]|1[0-2])/(?:0[1-9]|[1-2]\d|3[0-1])\b",
    r"\b(?:0[1-9]|[1-2]\d|3[0-1])\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:0[1-9]|[1-2]\d|3[0-1]),\s+\d{4}\b",
    r"\b(?:0[1-9]|[1-2]\d|3[0-1])-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(?:0[1-9]|[1-2]\d|3[0-1]),\s+\d{4}\b",
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:0?[1-9]|[12]\d|3[01])(?:st|nd|rd|th)?,\s+\d{4}\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(?:0?[1-9]|[1-2]\d|3[01])\s+\d{4}\b",
]
