"""Local-first, timestamped engineering-video evidence index.

Only caller-supplied subtitles are parsed. Public accessibility is not treated as
permission to reuse copyrighted media or subtitles.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from dataclasses import dataclass
from urllib.parse import urlparse
from typing import Iterable


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _url(value: str, label: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{label} must be an absolute HTTP(S) URL")


def _seconds(value: str) -> float:
    parts = value.strip().replace(",", ".").split(":")
    try:
        nums = [float(p) for p in parts]
    except ValueError as exc:
        raise ValueError(f"invalid timestamp: {value}") from exc
    if len(nums) == 2:
        return nums[0] * 60 + nums[1]
    if len(nums) == 3:
        return nums[0] * 3600 + nums[1] * 60 + nums[2]
    raise ValueError(f"invalid timestamp: {value}")


@dataclass(frozen=True)
class VideoSegment:
    start_seconds: float
    end_seconds: float
    text: str
    source_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.start_seconds < 0 or self.end_seconds <= self.start_seconds or not self.text.strip():
            raise ValueError("a video segment requires 0 <= start < end and non-empty text")
        object.__setattr__(self, "source_refs", tuple(self.source_refs))
        for ref in self.source_refs:
            _url(ref, "source reference")


@dataclass(frozen=True)
class EngineeringVideo:
    source_id: str
    title: str
    url: str
    tool_id: str
    language: str
    rights_basis: str
    transcript: str
    segments: tuple[VideoSegment, ...]
    upstream_repo: str | None = None
    upstream_revision: str | None = None
    license_id: str | None = None
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.title.strip() or not self.tool_id.strip():
            raise ValueError("source_id, title and tool_id are required")
        if not self.rights_basis.strip():
            raise ValueError("rights_basis is required; public accessibility is not a reuse license")
        _url(self.url, "video URL")
        if self.upstream_repo:
            _url(self.upstream_repo, "upstream repository")
        object.__setattr__(self, "segments", tuple(self.segments))
        object.__setattr__(self, "tags", tuple(self.tags))
        last_start = -1.0
        for segment in self.segments:
            if segment.start_seconds < last_start:
                raise ValueError("video segments must be ordered")
            last_start = segment.start_seconds

    @property
    def transcript_sha256(self) -> str:
        return _digest(self.transcript)

    @property
    def record_sha256(self) -> str:
        value = {"source_id": self.source_id, "title": self.title, "url": self.url, "tool_id": self.tool_id,
                 "language": self.language, "rights_basis": self.rights_basis,
                 "transcript_sha256": self.transcript_sha256, "upstream_repo": self.upstream_repo,
                 "upstream_revision": self.upstream_revision, "license_id": self.license_id,
                 "tags": list(self.tags),
                 "segments": [{"start": s.start_seconds, "end": s.end_seconds, "text": s.text,
                               "source_refs": list(s.source_refs)} for s in self.segments]}
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return _digest(raw)


def parse_vtt(text: str, *, source_refs: Iterable[str] = ()) -> tuple[VideoSegment, ...]:
    """Parse caller-supplied WebVTT captions and preserve exact cue timing."""
    refs = tuple(source_refs)
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n"))
    cue = re.compile(r"(?P<start>(?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})\s+-->\s+(?P<end>(?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})")
    results = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines or lines[0].startswith(("WEBVTT", "NOTE", "STYLE", "REGION")):
            continue
        index = next((i for i, line in enumerate(lines) if "-->" in line and cue.search(line)), None)
        if index is None:
            continue
        match = cue.search(lines[index])
        assert match is not None
        caption = html.unescape(re.sub(r"<[^>]+>", "", " ".join(lines[index+1:]))).strip()
        if caption:
            results.append(VideoSegment(_seconds(match.group("start")), _seconds(match.group("end")), caption, refs))
    return tuple(results)


@dataclass(frozen=True)
class VideoHit:
    source_id: str
    title: str
    video_url: str
    tool_id: str
    start_seconds: float
    end_seconds: float
    text: str
    source_refs: tuple[str, ...]
    transcript_sha256: str


class VideoKnowledgeIndex:
    def __init__(self) -> None:
        self._videos: dict[str, EngineeringVideo] = {}

    def add(self, video: EngineeringVideo) -> None:
        old = self._videos.get(video.source_id)
        if old and old.record_sha256 != video.record_sha256:
            raise ValueError(f"source_id already exists with changed provenance: {video.source_id}")
        self._videos.setdefault(video.source_id, video)

    def get(self, source_id: str) -> EngineeringVideo:
        return self._videos[source_id]

    def search(self, query: str, *, tool_id: str | None = None, limit: int = 10) -> tuple[VideoHit, ...]:
        if limit < 1:
            raise ValueError("limit must be positive")
        terms = {w for w in re.findall(r"[\w+#.-]+", query.casefold()) if len(w) > 1}
        if not terms:
            return ()
        scored = []
        for video in self._videos.values():
            if tool_id and video.tool_id != tool_id:
                continue
            meta = set(re.findall(r"[\w+#.-]+", (video.title + " " + video.tool_id + " " + " ".join(video.tags)).casefold()))
            meta_score = len(terms & meta)
            matches = []
            for segment in video.segments:
                words = set(re.findall(r"[\w+#.-]+", segment.text.casefold()))
                score = len(terms & words)
                if score:
                    matches.append((-3 * score - meta_score, segment.start_seconds, segment))
            if not matches and meta_score and video.segments:
                segment = video.segments[0]
                matches.append((-meta_score, segment.start_seconds, segment))
            for score, start, segment in matches:
                scored.append((score, video.source_id, start, video, segment))
        scored.sort(key=lambda item: item[:3])
        return tuple(VideoHit(v.source_id, v.title, v.url, v.tool_id, s.start_seconds, s.end_seconds,
                              s.text, s.source_refs, v.transcript_sha256)
                     for _, _, _, v, s in scored[:limit])

    def manifest(self) -> dict[str, object]:
        videos = []
        for source_id, video in sorted(self._videos.items()):
            videos.append({"source_id": source_id, "title": video.title, "url": video.url,
                           "tool_id": video.tool_id, "language": video.language, "rights_basis": video.rights_basis,
                           "license_id": video.license_id, "upstream_repo": video.upstream_repo,
                           "upstream_revision": video.upstream_revision, "transcript_sha256": video.transcript_sha256,
                           "record_sha256": video.record_sha256,
                           "segments": [{"start_seconds": s.start_seconds, "end_seconds": s.end_seconds,
                                         "text": s.text, "source_refs": list(s.source_refs)} for s in video.segments]})
        payload = {"schema": "nexent.engineering-video-index/v1", "videos": videos}
        payload["index_sha256"] = _digest(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
        return payload
