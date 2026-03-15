#!/usr/bin/env python3
"""
智能 PDF 阅读器 - 为快速书籍掌握而设计

功能特点：
- 策略性阅读：只提取关键信息，节省 Token
- 智能检测：自动识别文本型/扫描型 PDF
- OCR 支持：扫描版 PDF 自动 OCR 识别（使用 PaddleOCR）
- 目录提取：快速获取书籍结构
- 章节精读：按需读取特定内容
- 搜索定位：基于关键词快速找到相关内容

使用方法：
    python pdf_reader.py <pdf_path> [选项]

示例：
    # 获取全书概览（推荐首次使用）
    python pdf_reader.py book.pdf --overview
    
    # 提取目录结构（扫描版自动 OCR）
    python pdf_reader.py book.pdf --toc --ocr
    
    # 读取特定章节（智能识别章节边界）
    python pdf_reader.py book.pdf --pages 10-20
    
    # OCR 特定页面
    python pdf_reader.py book.pdf --ocr-pages 1-5
    
    # 搜索关键词并显示上下文
    python pdf_reader.py book.pdf --search "Python" --context 3
    
    # 生成结构化学习大纲
    python pdf_reader.py book.pdf --outline

注意：
    如果未安装依赖，请先运行 install.py
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

# 配置常量
MAX_OVERVIEW_PAGES = 15  # 概览模式最大读取页数
MAX_TEXT_LENGTH_PER_PAGE = 3000  # 每页最大字符数（防止图表页）
CONTEXT_PAGES_DEFAULT = 2  # 搜索时默认上下文页数
OCR_DPI = 300  # OCR 时 PDF 转图片的分辨率


class PaddleOCRWrapper:
    """PaddleOCR 包装器 - 扫描版 PDF 的文字识别"""
    
    def __init__(self, use_gpu: bool = False, lang: str = 'ch'):
        self.ocr = None
        self.use_gpu = use_gpu
        self.lang = lang
        self._initialized = False
    
    def _init_ocr(self):
        """延迟初始化 OCR"""
        if self._initialized:
            return
        
        try:
            from paddleocr import PaddleOCR
            print(f"🔄 正在初始化 PaddleOCR (语言: {self.lang})...")
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang=self.lang,
                show_log=False,
                use_gpu=self.use_gpu
            )
            self._initialized = True
            print("✅ PaddleOCR 初始化完成")
        except ImportError:
            print("❌ PaddleOCR 未安装")
            print("   请运行: python install.py")
            raise
    
    def ocr_image(self, image_path: str) -> str:
        """识别图片中的文字"""
        self._init_ocr()
        
        try:
            result = self.ocr.ocr(image_path, cls=True)
            if not result or not result[0]:
                return ""
            
            # 提取文本（按行）
            texts = []
            for line in result[0]:
                if line:
                    texts.append(line[1][0])  # text content
            
            return '\n'.join(texts)
        except Exception as e:
            return f"[OCR 失败: {e}]"
    
    def ocr_pdf_page(self, pdf_path: str, page_num: int, dpi: int = OCR_DPI) -> str:
        """
        OCR PDF 的指定页面
        
        Args:
            pdf_path: PDF 文件路径
            page_num: 页码（0-based）
            dpi: 转换分辨率，越高越清晰但越慢
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            return "[需要安装 PyMuPDF: pip install pymupdf]"
        
        temp_img = None
        try:
            # 打开 PDF
            doc = fitz.open(pdf_path)
            if page_num >= len(doc):
                return "[页码超出范围]"
            
            page = doc[page_num]
            
            # PDF 页面转为图片（提高分辨率以获得更好的 OCR 效果）
            zoom = dpi / 72  # 72 是 PDF 默认 DPI
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # 保存临时图片
            import tempfile
            temp_img = tempfile.mktemp(suffix='.png')
            pix.save(temp_img)
            doc.close()
            
            # OCR 识别
            text = self.ocr_image(temp_img)
            
            return text
            
        except Exception as e:
            return f"[OCR 错误: {e}]"
        finally:
            # 清理临时文件
            if temp_img and os.path.exists(temp_img):
                try:
                    os.remove(temp_img)
                except:
                    pass


class OCREnhancedPDFReader(SmartPDFReader):
    """增强版 PDF 阅读器，支持 OCR"""
    
    def __init__(self, pdf_path: str, use_ocr: bool = False, ocr_lang: str = 'ch'):
        super().__init__(pdf_path)
        self.ocr_wrapper = None
        if use_ocr or not self.info.is_text_based:
            self.ocr_wrapper = PaddleOCRWrapper(lang=ocr_lang)
    
    def _extract_text(self, page_idx: int, max_length: int = MAX_TEXT_LENGTH_PER_PAGE, 
                     use_ocr: bool = False) -> str:
        """
        提取文本，支持 OCR 回退
        
        Args:
            page_idx: 页面索引
            max_length: 最大字符数
            use_ocr: 是否强制使用 OCR
        """
        # 先尝试普通提取
        text = super()._extract_text(page_idx, max_length)
        
        # 如果内容太少或是强制 OCR，尝试 OCR
        if (use_ocr or len(text.strip()) < 50) and self.ocr_wrapper:
            if not text.strip() or use_ocr:
                print(f"   🔄 第 {page_idx+1} 页使用 OCR 识别...")
                ocr_text = self.ocr_wrapper.ocr_pdf_page(self.pdf_path, page_idx)
                if ocr_text and not ocr_text.startswith('['):
                    return ocr_text[:max_length]
        
        return text


@dataclass
class PDFInfo:
    """PDF 基本信息"""
    total_pages: int
    is_text_based: bool
    has_bookmarks: bool
    title: Optional[str] = None
    author: Optional[str] = None


class SmartPDFReader:
    """智能 PDF 阅读器"""
    
    def __init__(self, pdf_path: str, use_ocr: bool = False, ocr_lang: str = 'ch'):
        self.pdf_path = Path(pdf_path)
        self.pdf = None
        self.info = None
        self.use_ocr = use_ocr
        self.ocr_wrapper = None
        self._load_pdf()
        
        # 如果是扫描版或强制使用 OCR，初始化 OCR
        if use_ocr or (self.info and not self.info.is_text_based):
            self.ocr_wrapper = PaddleOCRWrapper(lang=ocr_lang)
    
    def _load_pdf(self):
        """加载 PDF 文件"""
        try:
            import pdfplumber
        except ImportError:
            print("错误: 需要安装 pdfplumber")
            print("运行: pip install pdfplumber")
            print("或者运行: python install.py")
            sys.exit(1)
        
        if not self.pdf_path.exists():
            print(f"错误: 文件不存在: {self.pdf_path}")
            sys.exit(1)
        
        try:
            self.pdf = pdfplumber.open(str(self.pdf_path))
            self.info = self._analyze_pdf()
        except Exception as e:
            print(f"错误: 无法打开 PDF: {e}")
            sys.exit(1)
    
    def _analyze_pdf(self) -> PDFInfo:
        """分析 PDF 类型和基本信息"""
        total_pages = len(self.pdf.pages)
        
        # 检测是否为文本型 PDF（采样前 5 页）
        sample_pages = min(5, total_pages)
        text_pages = 0
        
        for i in range(sample_pages):
            text = self.pdf.pages[i].extract_text()
            if text and len(text.strip()) > 100:
                text_pages += 1
        
        is_text_based = text_pages >= 2  # 至少 2 页有文本
        
        # 检查是否有书签/目录
        has_bookmarks = False
        try:
            # 尝试提取大纲（部分 PDF 支持）
            toc = self.pdf.outline
            has_bookmarks = bool(toc)
        except:
            pass
        
        return PDFInfo(
            total_pages=total_pages,
            is_text_based=is_text_based,
            has_bookmarks=has_bookmarks
        )
    
    def _extract_text(self, page_idx: int, max_length: int = MAX_TEXT_LENGTH_PER_PAGE,
                     force_ocr: bool = False) -> str:
        """
        安全提取单页文本，支持 OCR 回退
        
        Args:
            page_idx: 页面索引
            max_length: 最大字符数
            force_ocr: 强制使用 OCR
        """
        if page_idx < 0 or page_idx >= self.info.total_pages:
            return ""
        
        # 先尝试普通提取
        try:
            text = self.pdf.pages[page_idx].extract_text()
            text = text.strip() if text else ""
        except Exception:
            text = ""
        
        # 如果内容太少或强制 OCR，尝试 OCR
        if (force_ocr or len(text) < 50) and self.ocr_wrapper:
            if not text or force_ocr:
                print(f"   🔄 第 {page_idx+1} 页使用 OCR 识别...")
                try:
                    ocr_text = self.ocr_wrapper.ocr_pdf_page(str(self.pdf_path), page_idx)
                    if ocr_text and not ocr_text.startswith('['):
                        text = ocr_text
                except Exception as e:
                    if not text:
                        text = f"[OCR 失败: {e}]"
        
        # 限制长度
        if len(text) > max_length:
            text = text[:max_length] + "\n... [内容过长，已截断]"
        
        return text
    
    def _find_toc_pages(self) -> List[int]:
        """智能查找目录页"""
        toc_candidates = []
        
        # 通常目录在前 30 页
        search_range = min(30, self.info.total_pages)
        
        toc_keywords = [
            "目录", "contents", "目次", "table of contents",
            "chapter", "章", "第1章", "第一章", "1.1", "1.2"
        ]
        
        for i in range(search_range):
            text = self._extract_text(i, max_length=2000)
            text_lower = text.lower()
            
            score = 0
            for keyword in toc_keywords:
                if keyword.lower() in text_lower:
                    score += 1
            
            # 检测目录特征：包含页码数字和章节标题
            page_number_pattern = r'\d+\s*$'  # 行尾数字（页码）
            lines_with_numbers = len(re.findall(page_number_pattern, text, re.MULTILINE))
            
            if lines_with_numbers > 5:  # 多行有页码数字
                score += 2
            
            if score >= 2:
                toc_candidates.append((i, score))
        
        # 按分数排序，返回最可能是目录的页面
        toc_candidates.sort(key=lambda x: x[1], reverse=True)
        return [idx for idx, _ in toc_candidates[:5]]  # 最多返回 5 页候选
    
    def _detect_chapter_boundaries(self) -> List[Tuple[int, str]]:
        """检测章节边界"""
        boundaries = []
        
        # 章节标题模式（中英文）
        chapter_patterns = [
            r'^第[\d一二三四五六七八九十]+章\s+',  # 第一章、第1章
            r'^Chapter\s+\d+',  # Chapter 1
            r'^\d+\.\d+\s+',  # 1.1、2.3
            r'^第[\d一二三四五六七八九十]+节\s+',  # 第一节
            r'^Section\s+\d+',  # Section 1
        ]
        
        # 采样检测（每 20 页检查一次以提高效率）
        sample_interval = max(1, self.info.total_pages // 20)
        
        for i in range(0, min(self.info.total_pages, 200), sample_interval):
            text = self._extract_text(i, max_length=1500)
            lines = text.split('\n')[:10]  # 只看前 10 行
            
            for line in lines:
                line = line.strip()
                for pattern in chapter_patterns:
                    if re.match(pattern, line, re.IGNORECASE):
                        boundaries.append((i, line))
                        break
        
        return boundaries
    
    def get_overview(self) -> str:
        """
        获取全书概览（战略级预览）
        
        提取内容：
        - 封面/标题页信息
        - 前言/序言核心观点
        - 目录结构
        - 结语/总结
        """
        sections = []
        sections.append(f"📚 《{self.pdf_path.stem}》概览\n")
        sections.append(f"总页数: {self.info.total_pages} | 类型: {'文本型' if self.info.is_text_based else '扫描型(可能需要OCR)'}\n")
        sections.append("=" * 50 + "\n")
        
        if not self.info.is_text_based:
            sections.append("⚠️  警告: 此 PDF 可能是扫描版，文字提取效果可能不佳\n")
            sections.append("建议: 使用 OCR 工具预处理，或手动输入关键内容\n\n")
        
        # 1. 尝试提取标题页信息（前 3 页）
        sections.append("【封面/标题页信息】\n")
        for i in range(min(3, self.info.total_pages)):
            text = self._extract_text(i, max_length=2000)
            if text and len(text.strip()) > 50:
                sections.append(f"--- 第 {i+1} 页 ---\n{text}\n")
                if i >= 1:  # 最多显示 2 页
                    break
        
        # 2. 查找并提取目录
        sections.append("\n【目录结构】\n")
        toc_pages = self._find_toc_pages()
        if toc_pages:
            for page_idx in toc_pages[:2]:  # 最多 2 页目录
                text = self._extract_text(page_idx, max_length=4000)
                sections.append(f"--- 第 {page_idx+1} 页 (目录) ---\n{text}\n")
        else:
            sections.append("未能自动识别目录页\n")
        
        # 3. 提取章节边界
        sections.append("\n【章节检测】\n")
        chapters = self._detect_chapter_boundaries()
        if chapters:
            sections.append("检测到以下章节:\n")
            for page, title in chapters[:10]:  # 最多显示 10 个
                sections.append(f"  第 {page+1} 页: {title[:50]}...\n")
        else:
            sections.append("未能自动检测章节结构\n")
        
        # 4. 尝试提取结语（最后 5 页）
        sections.append("\n【结语/总结】\n")
        start_page = max(0, self.info.total_pages - 5)
        for i in range(self.info.total_pages - 1, start_page - 1, -1):
            text = self._extract_text(i, max_length=2000)
            if text and ("总结" in text or "结语" in text or "conclusion" in text.lower()):
                sections.append(f"--- 第 {i+1} 页 ---\n{text}\n")
                break
        
        return "".join(sections)
    
    def get_toc(self) -> str:
        """提取并格式化目录"""
        toc_pages = self._find_toc_pages()
        
        if not toc_pages:
            return "未能自动识别目录页。尝试手动指定页码范围查看。\n"
        
        result = ["📑 目录\n", "=" * 50 + "\n\n"]
        
        for page_idx in toc_pages:
            text = self._extract_text(page_idx, max_length=5000)
            result.append(f"--- 第 {page_idx+1} 页 ---\n{text}\n\n")
        
        return "".join(result)
    
    def get_pages(self, start: int, end: Optional[int] = None, max_chars: int = 10000) -> str:
        """
        读取指定页范围
        
        Args:
            start: 起始页（1-based）
            end: 结束页（1-based），默认为 start
            max_chars: 最大返回字符数（防止超出上下文限制）
        """
        if end is None:
            end = start
        
        # 转换为 0-based
        start_idx = max(0, start - 1)
        end_idx = min(self.info.total_pages, end)
        
        if start_idx >= end_idx:
            return "错误: 无效的页码范围\n"
        
        result = [f"📖 第 {start}-{end} 页内容\n", "=" * 50 + "\n\n"]
        total_chars = 0
        
        for i in range(start_idx, end_idx):
            text = self._extract_text(i)
            page_content = f"--- 第 {i+1} 页 ---\n{text}\n\n"
            
            if total_chars + len(page_content) > max_chars:
                result.append(f"\n... [已达到最大字符限制 {max_chars}，停止提取]\n")
                break
            
            result.append(page_content)
            total_chars += len(page_content)
        
        return "".join(result)
    
    def search(self, keyword: str, context_pages: int = CONTEXT_PAGES_DEFAULT) -> str:
        """
        搜索关键词并显示上下文
        
        Args:
            keyword: 搜索关键词
            context_pages: 匹配页前后各读取多少页
        """
        results = []
        
        # 扫描所有页面（限制前 200 页以提高速度）
        search_limit = min(200, self.info.total_pages)
        
        for i in range(search_limit):
            text = self._extract_text(i, max_length=3000)
            if keyword.lower() in text.lower():
                results.append(i)
        
        if not results:
            return f"未找到关键词: '{keyword}'\n"
        
        # 合并相近的匹配结果
        merged_ranges = []
        current_start = results[0]
        current_end = results[0]
        
        for page in results[1:]:
            if page <= current_end + context_pages * 2:
                current_end = page
            else:
                merged_ranges.append((current_start, current_end))
                current_start = page
                current_end = page
        merged_ranges.append((current_start, current_end))
        
        # 生成结果
        output = [f"🔍 搜索 '{keyword}' 找到 {len(results)} 处匹配\n", "=" * 50 + "\n\n"]
        
        for start, end in merged_ranges[:5]:  # 最多显示 5 个区域
            # 添加上下文
            display_start = max(0, start - context_pages)
            display_end = min(self.info.total_pages, end + context_pages + 1)
            
            output.append(f"【匹配区域: 第 {start+1}-{end+1} 页】\n")
            output.append(self.get_pages(display_start + 1, display_end, max_chars=5000))
            output.append("\n" + "-" * 50 + "\n\n")
        
        if len(merged_ranges) > 5:
            output.append(f"... 还有 {len(merged_ranges) - 5} 个匹配区域未显示\n")
        
        return "".join(output)
    
    def get_outline(self) -> str:
        """生成结构化学习大纲"""
        outline = []
        outline.append(f"📋 《{self.pdf_path.stem}》学习大纲\n")
        outline.append("=" * 50 + "\n\n")
        
        # 基本信息
        outline.append(f"📊 基本信息\n")
        outline.append(f"  - 总页数: {self.info.total_pages}\n")
        outline.append(f"  - PDF 类型: {'文本型' if self.info.is_text_based else '扫描型'}\n")
        outline.append(f"  - 书签: {'有' if self.info.has_bookmarks else '无'}\n\n")
        
        # 章节结构
        outline.append("📑 章节结构\n")
        chapters = self._detect_chapter_boundaries()
        
        if chapters:
            for i, (page, title) in enumerate(chapters[:20], 1):  # 最多 20 章
                outline.append(f"  {i}. 第 {page+1} 页 - {title[:60]}\n")
        else:
            outline.append("  未能自动检测，建议手动浏览\n")
        
        outline.append("\n")
        
        # 建议的学习路径
        outline.append("🎯 建议学习路径\n")
        outline.append("  阶段1 - 快速预览:\n")
        outline.append(f"    - 阅读第 1-3 页（前言/导论）\n")
        outline.append(f"    - 查看目录页\n")
        outline.append(f"    - 浏览最后 3 页（总结）\n\n")
        
        if chapters:
            outline.append("  阶段2 - 核心章节:\n")
            # 假设前 3 个检测到的章节是核心
            for i, (page, title) in enumerate(chapters[:3], 1):
                outline.append(f"    {i}. {title[:40]} (第 {page+1} 页起)\n")
        
        outline.append("\n  阶段3 - 按需深入:\n")
        outline.append("    - 使用 --search 查找特定主题\n")
        outline.append("    - 使用 --chapter 精读特定章节\n")
        
        return "".join(outline)
    
    def close(self):
        """关闭 PDF"""
        if self.pdf:
            self.pdf.close()


def setup_encoding():
    """设置输出编码"""
    import sys
    import io
    # 确保 stdout 使用 utf-8 编码
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    setup_encoding()
    
    parser = argparse.ArgumentParser(
        description="智能 PDF 阅读器 - 策略性提取关键内容，节省 Token",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 获取全书概览（首次使用推荐）
  python pdf_reader.py book.pdf --overview
  
  # 提取目录（扫描版自动使用 OCR）
  python pdf_reader.py book.pdf --toc --ocr
  
  # 读取指定页（强制 OCR）
  python pdf_reader.py book.pdf --pages 10-20 --ocr
  
  # 搜索关键词
  python pdf_reader.py book.pdf --search "Python" --context 2
  
  # 生成学习大纲
  python pdf_reader.py book.pdf --outline
        """
    )
    
    parser.add_argument("pdf_path", help="PDF 文件路径")
    
    # 主要功能选项
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--overview", "-o", action="store_true",
                      help="获取全书概览（推荐首次使用）")
    group.add_argument("--toc", "-t", action="store_true",
                      help="提取目录结构")
    group.add_argument("--pages", "-p", metavar="RANGE",
                      help="读取指定页范围，如: 10-20 或 15")
    group.add_argument("--search", "-s", metavar="KEYWORD",
                      help="搜索关键词")
    group.add_argument("--outline", action="store_true",
                      help="生成结构化学习大纲")
    
    # 附加选项
    parser.add_argument("--context", "-c", type=int, default=CONTEXT_PAGES_DEFAULT,
                       help=f"搜索时的上下文页数（默认: {CONTEXT_PAGES_DEFAULT}）")
    parser.add_argument("--output", "-O", metavar="FILE",
                       help="输出到文件（默认输出到控制台）")
    
    # OCR 选项
    parser.add_argument("--ocr", action="store_true",
                       help="启用 OCR（扫描版 PDF 自动启用）")
    parser.add_argument("--ocr-lang", default="ch",
                       help="OCR 语言 (ch: 中文, en: 英文, ch+en: 中英混合)")
    parser.add_argument("--dpi", type=int, default=OCR_DPI,
                       help=f"OCR 分辨率 (默认: {OCR_DPI})")
    
    args = parser.parse_args()
    
    # 初始化阅读器（支持 OCR）
    reader = SmartPDFReader(args.pdf_path, use_ocr=args.ocr, ocr_lang=args.ocr_lang)
    
    try:
        # 执行对应功能
        if args.overview:
            result = reader.get_overview()
        elif args.toc:
            result = reader.get_toc()
        elif args.pages:
            if "-" in args.pages:
                start, end = map(int, args.pages.split("-"))
            else:
                start = int(args.pages)
                end = start
            result = reader.get_pages(start, end)
        elif args.search:
            result = reader.search(args.search, args.context)
        elif args.outline:
            result = reader.get_outline()
        else:
            result = "请指定一个操作选项"
        
        # 输出结果
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"结果已保存到: {args.output}")
        else:
            print(result)
        
        # 打印使用提示
        print("\n" + "=" * 50)
        print("💡 提示:")
        print("  - 使用 --overview 获取全书概览")
        print("  - 使用 --search 查找特定内容")
        print("  - 使用 --pages 精读特定章节")
        
    finally:
        reader.close()


if __name__ == "__main__":
    main()
