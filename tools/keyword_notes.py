from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SITE_LINK = "https://site-app-aiyouxi.com.cn"
KEYWORD_POOL = ["爱游戏", "游戏评测", "手游推荐", "爱游戏新作"]


@dataclass
class KeywordNote:
    keyword: str
    description: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def short_display(self) -> str:
        tag_part = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] {self.description[:30]}... | 标签: {tag_part}"

    def full_report(self) -> str:
        lines = [
            f"关键词: {self.keyword}",
            f"描述: {self.description}",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
            f"创建时间: {self.created_at}",
            f"关联站点: {SITE_LINK}",
        ]
        return "\n".join(lines)


@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote):
        self.notes.append(note)

    def search_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def display_all_short(self) -> str:
        if not self.notes:
            return "暂无笔记。"
        return "\n".join(f"{i+1}. {n.short_display()}" for i, n in enumerate(self.notes))

    def display_all_full(self) -> str:
        if not self.notes:
            return "暂无笔记。"
        return "\n---\n".join(n.full_report() for n in self.notes)


def build_sample_collection() -> NoteCollection:
    collection = NoteCollection()
    sample_data = [
        ("爱游戏", "一个专注于精品手游推荐与深度评测的平台", ["游戏", "推荐", "评测"]),
        ("手游评测", "针对热门手机游戏进行玩法、画面、剧情分析", ["手游", "分析"]),
        ("爱游戏新作", "爱游戏团队最新发掘的潜力手游", ["新游", "爱游戏"]),
    ]
    for kw, desc, tags in sample_data:
        collection.add_note(KeywordNote(keyword=kw, description=desc, tags=tags))
    return collection


if __name__ == "__main__":
    print("=== 关键词笔记示例 ===")
    print(f"主站点: {SITE_LINK}")
    print()

    notes = build_sample_collection()
    print("--- 简短列表 ---")
    print(notes.display_all_short())
    print()
    print("--- 完整详情 ---")
    print(notes.display_all_full())
    print()
    search_term = "爱游戏"
    results = notes.search_by_keyword(search_term)
    print(f"--- 搜索 '{search_term}' 结果 ---")
    for note in results:
        print(note.full_report())