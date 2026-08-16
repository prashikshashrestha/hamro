import os
import io
from django.core.files.base import ContentFile

def generate_pdf_export(book):
    """
    Generates a PDF document for a given book using ReportLab.
    Returns bytes of the PDF file.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'BookTitle',
            parent=styles['Title'],
            fontSize=28,
            leading=34,
            spaceAfter=20
        )
        subtitle_style = ParagraphStyle(
            'BookSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            leading=18,
            alignment=1, # Centered
            spaceAfter=40
        )
        heading_style = ParagraphStyle(
            'ChapterHeading',
            parent=styles['Heading1'],
            fontSize=20,
            leading=24,
            spaceBefore=20,
            spaceAfter=15
        )
        body_style = ParagraphStyle(
            'BookBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=16,
            spaceAfter=12
        )

        story = []

        # Title Page
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph(book.title, title_style))
        if book.style_reference:
            story.append(Paragraph(f"In the style of: {book.style_reference}", subtitle_style))
        story.append(PageBreak())

        # Chapters
        for chapter in book.chapters.all():
            story.append(Paragraph(f"Chapter {chapter.number}: {chapter.title}", heading_style))
            content_text = chapter.final_content or "No content generated yet."
            
            paragraphs = content_text.split('\n\n')
            for p_text in paragraphs:
                if p_text.strip():
                    story.append(Paragraph(p_text.strip(), body_style))
            
            story.append(PageBreak())

        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
    except Exception as e:
        # Fallback basic PDF text generator if reportlab has issues
        buffer = io.BytesIO()
        text_content = f"{book.title}\n\n"
        for ch in book.chapters.all():
            text_content += f"Chapter {ch.number}: {ch.title}\n\n{ch.final_content}\n\n"
        buffer.write(text_content.encode('utf-8'))
        return buffer.getvalue()


def generate_epub_export(book):
    """
    Generates an EPUB document for a given book using ebooklib.
    Returns bytes of the EPUB file.
    """
    try:
        from ebooklib import epub

        book_epub = epub.EpubBook()
        book_epub.set_identifier(str(book.id))
        book_epub.set_title(book.title)
        book_epub.set_language('en')

        # Intro chapter
        c_intro = epub.EpubHtml(title='Title Page', file_name='title.xhtml', lang='en')
        c_intro.content = f'<h1>{book.title}</h1><p><em>Generated with AI Book Generator</em></p>'
        book_epub.add_item(c_intro)

        spine = ['nav', c_intro]
        toc = []

        for chapter in book.chapters.all():
            file_name = f'chap_{chapter.number}.xhtml'
            c = epub.EpubHtml(title=f'Chapter {chapter.number}: {chapter.title}', file_name=file_name, lang='en')
            
            paragraphs_html = ''.join([f'<p>{p.strip()}</p>' for p in (chapter.final_content or "").split('\n\n') if p.strip()])
            c.content = f'<h2>Chapter {chapter.number}: {chapter.title}</h2>{paragraphs_html}'
            
            book_epub.add_item(c)
            toc.append(c)
            spine.append(c)

        book_epub.toc = toc
        book_epub.add_item(epub.EpubNcx())
        book_epub.add_item(epub.EpubNav())
        book_epub.spine = spine

        buffer = io.BytesIO()
        epub.write_epub(buffer, book_epub, {})
        data = buffer.getvalue()
        buffer.close()
        return data
    except Exception as e:
        buffer = io.BytesIO()
        buffer.write(f"EPUB Export fallback for {book.title}".encode('utf-8'))
        return buffer.getvalue()
