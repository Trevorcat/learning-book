#!/usr/bin/env python3
"""
书籍分析助手 - 与 Quick Book Mastery Skill 配合使用

功能：
- 分析 PDF 书籍的可读性
- 为四阶段学习流程提取关键内容
- 生成学习计划建议

使用方法：
    python book_analyzer.py <pdf_path> [阶段]

阶段选项：
    stage1  - 准备阶段：提取书名、作者、简介
    stage2  - 概览阶段：提取目录、核心框架
    stage3  - 深入阶段：提取关键章节摘要
    stage4  - 巩固阶段：生成复习要点
"""

import argparse
import json
import sys
from pathlib import Path


class BookAnalyzer:
    """书籍分析器"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.reader = None
        self._init_reader()
    
    def _init_reader(self):
        """初始化 PDF 阅读器"""
        try:
            from pdf_reader import SmartPDFReader
            self.reader = SmartPDFReader(self.pdf_path)
        except ImportError:
            print("错误: 需要 pdf_reader.py 在同一目录")
            sys.exit(1)
        except Exception as e:
            print(f"错误: 无法初始化: {e}")
            sys.exit(1)
    
    def stage1_preparation(self) -> dict:
        """
        阶段1：准备与目标设定
        
        提取信息用于：
        - 确认书籍信息
        - 评估学习难度
        - 设定时间预期
        """
        result = {
            "stage": "准备阶段",
            "book_info": {},
            "readability": {},
            "recommendations": []
        }
        
        # 基本信息
        result["book_info"] = {
            "filename": self.pdf_path.stem,
            "total_pages": self.reader.info.total_pages,
            "is_text_based": self.reader.info.is_text_based,
            "has_bookmarks": self.reader.info.has_bookmarks
        }
        
        # 可读性评估
        if self.reader.info.is_text_based:
            result["readability"] = {
                "level": "良好",
                "note": "文本型PDF，可以直接提取内容",
                "suggested_time_per_page": "2-3分钟（深度学习）"
            }
        else:
            result["readability"] = {
                "level": "困难",
                "note": "扫描型PDF，文字提取可能不准确",
                "suggestion": "建议使用OCR工具，或手动输入关键内容"
            }
        
        # 时间估算
        total_pages = self.reader.info.total_pages
        if total_pages < 200:
            result["time_estimate"] = {
                "quick": "30分钟",
                "standard": "1-2小时",
                "deep": "3-4小时"
            }
        elif total_pages < 400:
            result["time_estimate"] = {
                "quick": "1小时",
                "standard": "2-3小时",
                "deep": "5-6小时"
            }
        else:
            result["time_estimate"] = {
                "quick": "1-2小时",
                "standard": "3-4小时",
                "deep": "建议分多次学习"
            }
        
        # 推荐的学习方案
        result["recommendations"] = [
            "快速版(30-60分钟): 适合了解概貌、筛选书籍",
            "标准版(1-2小时): 适合系统掌握核心内容",
            "深度版(3+小时): 适合精读、准备分享或考试"
        ]
        
        return result
    
    def stage2_overview(self) -> dict:
        """
        阶段2：概览与框架构建
        
        提取：
        - 目录结构
        - 章节分布
        - 核心主题识别
        """
        result = {
            "stage": "概览阶段",
            "toc_found": False,
            "chapters": [],
            "key_sections": [],
            "framework": {}
        }
        
        # 查找目录
        toc_pages = self.reader._find_toc_pages()
        result["toc_found"] = len(toc_pages) > 0
        result["toc_pages"] = [p + 1 for p in toc_pages[:3]]
        
        # 检测章节
        chapters = self.reader._detect_chapter_boundaries()
        result["chapters_detected"] = len(chapters)
        
        for page, title in chapters[:15]:  # 最多 15 章
            result["chapters"].append({
                "page": page + 1,
                "title": title[:80]
            })
        
        # 提取前言/导论（通常是前 5 页）
        intro_text = ""
        for i in range(min(5, self.reader.info.total_pages)):
            text = self.reader._extract_text(i, max_length=2000)
            if "前言" in text or "序言" in text or "导论" in text or "介绍" in text:
                intro_text += text[:1500] + "\n"
        
        result["introduction_preview"] = intro_text[:1000] if intro_text else "未能提取前言内容"
        
        # 提取结尾总结（最后 3 页）
        conclusion_text = ""
        for i in range(self.reader.info.total_pages - 1, 
                       max(self.reader.info.total_pages - 4, -1), -1):
            text = self.reader._extract_text(i, max_length=2000)
            if "总结" in text or "结语" in text or "结论" in text:
                conclusion_text += text[:1500] + "\n"
        
        result["conclusion_preview"] = conclusion_text[:1000] if conclusion_text else "未能提取结语内容"
        
        # 框架建议
        if result["chapters"]:
            mid = len(result["chapters"]) // 2
            result["framework_suggestion"] = {
                "part1": f"第1-{mid}章：基础/理论部分",
                "part2": f"第{mid+1}-{len(result['chapters'])}章：应用/深入部分"
            }
        
        return result
    
    def stage3_deep_dive(self, chapter_idx: int = 0) -> dict:
        """
        阶段3：深入与理解
        
        提取特定章节内容用于深度分析
        """
        result = {
            "stage": "深入阶段",
            "chapter_analysis": {},
            "key_concepts": [],
            "questions": []
        }
        
        chapters = self.reader._detect_chapter_boundaries()
        
        if not chapters or chapter_idx >= len(chapters):
            result["error"] = "无法找到指定章节"
            return result
        
        # 获取章节范围
        start_page = chapters[chapter_idx][0]
        end_page = chapters[chapter_idx + 1][0] if chapter_idx + 1 < len(chapters) else min(
            start_page + 20, self.reader.info.total_pages
        )
        
        chapter_title = chapters[chapter_idx][1]
        
        # 提取章节内容（限制页数）
        content_pages = []
        max_pages = min(10, end_page - start_page)  # 最多读 10 页
        
        for i in range(start_page, start_page + max_pages):
            text = self.reader._extract_text(i, max_length=2500)
            content_pages.append({
                "page": i + 1,
                "text": text
            })
        
        result["chapter_analysis"] = {
            "title": chapter_title,
            "start_page": start_page + 1,
            "end_page": end_page,
            "pages_read": len(content_pages),
            "content": content_pages[:3]  # 只返回前 3 页详细内容
        }
        
        # 生成苏格拉底式提问建议
        result["questions"] = [
            "这个章节的核心论点是什么？",
            "作者用什么证据支持这个论点？",
            "这个概念与你已知的知识有什么联系？",
            "如果向别人解释这一章，你会怎么说？",
            "这一章中你最不确定的概念是什么？"
        ]
        
        return result
    
    def stage4_consolidation(self) -> dict:
        """
        阶段4：巩固与应用
        
        生成复习计划和要点
        """
        result = {
            "stage": "巩固阶段",
            "review_plan": {},
            "key_takeaways": [],
            "action_items": []
        }
        
        # 间隔重复计划
        result["review_plan"] = {
            "day_1": "学习后1天：快速回顾核心概念",
            "day_3": "学习后3天：主动回忆练习",
            "day_7": "学习后1周：完成自测清单",
            "day_30": "学习后1个月：总结应用心得"
        }
        
        # 获取章节标题作为要点提示
        chapters = self.reader._detect_chapter_boundaries()
        result["key_takeaways"] = [
            f"第{idx+1}章要点: {title[:50]}..." 
            for idx, (_, title) in enumerate(chapters[:10])
        ]
        
        # 行动建议
        result["action_items"] = [
            "完成费曼复述：用自己的话解释核心概念",
            "建立概念关联图：将新知识与已知知识连接",
            "实际应用：在项目中尝试使用学到的内容",
            "教授他人：向朋友/同事分享你的学习成果"
        ]
        
        return result
    
    def close(self):
        """关闭阅读器"""
        if self.reader:
            self.reader.close()


def format_output(data: dict, format_type: str = "text") -> str:
    """格式化输出"""
    if format_type == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    # 文本格式
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"📚 {data.get('stage', '分析结果')}")
    lines.append(f"{'='*60}\n")
    
    def format_dict(d, indent=0):
        for key, value in d.items():
            if key == "stage":
                continue
            
            prefix = "  " * indent
            
            if isinstance(value, dict):
                lines.append(f"{prefix}【{key}】")
                format_dict(value, indent + 1)
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    lines.append(f"{prefix}【{key}】")
                    for item in value[:10]:  # 最多显示 10 项
                        if isinstance(item, dict):
                            for k, v in item.items():
                                lines.append(f"{prefix}  - {k}: {v}")
                        else:
                            lines.append(f"{prefix}  - {item}")
                else:
                    lines.append(f"{prefix}【{key}】")
                    for item in value[:10]:
                        lines.append(f"{prefix}  • {item}")
            else:
                lines.append(f"{prefix}{key}: {value}")
        
        if indent == 0:
            lines.append("")
    
    format_dict(data)
    return "\n".join(lines)


def setup_encoding():
    """设置输出编码"""
    import sys
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    setup_encoding()
    
    parser = argparse.ArgumentParser(
        description="书籍分析助手 - 配合 Quick Book Mastery Skill 使用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 阶段1：准备（获取书籍信息）
  python book_analyzer.py book.pdf stage1
  
  # 阶段2：概览（提取目录框架）
  python book_analyzer.py book.pdf stage2
  
  # 阶段3：深入（分析特定章节）
  python book_analyzer.py book.pdf stage3 --chapter 0
  
  # 阶段4：巩固（生成复习计划）
  python book_analyzer.py book.pdf stage4
  
  # JSON 格式输出
  python book_analyzer.py book.pdf stage2 --json
        """
    )
    
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument("stage", choices=["stage1", "stage2", "stage3", "stage4"],
                       help="学习阶段")
    parser.add_argument("--chapter", "-c", type=int, default=0,
                       help="阶段3使用的章节索引（从0开始）")
    parser.add_argument("--json", "-j", action="store_true",
                       help="输出 JSON 格式")
    parser.add_argument("--output", "-o", help="输出到文件")
    
    args = parser.parse_args()
    
    # 执行分析
    analyzer = BookAnalyzer(args.pdf_path)
    
    try:
        if args.stage == "stage1":
            result = analyzer.stage1_preparation()
        elif args.stage == "stage2":
            result = analyzer.stage2_overview()
        elif args.stage == "stage3":
            result = analyzer.stage3_deep_dive(args.chapter)
        elif args.stage == "stage4":
            result = analyzer.stage4_consolidation()
        
        # 格式化输出
        output = format_output(result, "json" if args.json else "text")
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"结果已保存到: {args.output}")
        else:
            print(output)
        
        # 输出使用建议
        if args.stage == "stage1":
            print("\n💡 下一步: 运行 `stage2` 提取目录结构")
        elif args.stage == "stage2":
            print("\n💡 下一步: 运行 `stage3 --chapter 0` 开始深入第一章")
        
    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
