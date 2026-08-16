import threading
import time

def run_book_generation_pipeline(book_id):
    """
    Runs the 2-pass book generation pipeline asynchronously in a background thread.
    Currently uses modular mock/template generators so it works out-of-the-box
    without requiring LLM API keys.
    """
    thread = threading.Thread(target=_pipeline_worker, args=(book_id,))
    thread.daemon = True
    thread.start()

def _pipeline_worker(book_id):
    from books.models import Book, Chapter, GenerationStatus, GenerationLog
    
    try:
        book = Book.objects.get(id=book_id)
        
        # --- PASS 1: DRAFTING OUTLINE ---
        book.status = GenerationStatus.OUTLINE_DRAFTING
        book.current_pass = 1
        book.progress_percentage = 10
        book.current_step_description = "Drafting book title & chapter outline..."
        book.save()
        
        GenerationLog.objects.create(
            book=book, pass_number=1, message="Pass 1 Started: Drafting outline & table of contents"
        )
        time.sleep(1) # Simulate initial processing

        # Generate Title & Outline based on premise
        premise_first_words = " ".join(book.premise.split()[:4]).capitalize()
        book.title = f"The Chronicles of {premise_first_words}" if len(premise_first_words) > 0 else "The AI Journey"
        book.summary = f"An immersive {book.get_book_type_display().lower()} built around the premise: '{book.premise}'."
        book.save()

        # --- PASS 1: GENERATING CHAPTERS ---
        book.status = GenerationStatus.CHAPTER_DRAFTING
        book.progress_percentage = 25
        book.current_step_description = "Generating Pass 1 chapter drafts..."
        book.save()

        target_count = book.target_chapters
        for i in range(1, target_count + 1):
            ch_title = f"Beginning of the Journey - Part {i}" if i == 1 else f"Unfolding Events - Part {i}"
            outline_sum = f"In this chapter, the story explores themes related to '{book.premise}' (Phase {i})."
            
            # Pass 1 draft content template
            pass1_draft = (
                f"Chapter {i}: {ch_title}\n\n"
                f"The morning sun broke over the horizon as the journey began. {book.premise}.\n\n"
                f"Every step forward revealed new twists and turns. Inspired by the spirit of {book.style_reference or 'classic storytelling'}, "
                f"the characters navigated through challenges and discoveries. This initial draft establishes the core narrative arc for part {i}.\n\n"
                f"As dusk fell, the path ahead remained uncertain, setting the stage for what was yet to come."
            )

            chapter, created = Chapter.objects.get_or_create(
                book=book,
                number=i,
                defaults={
                    'title': ch_title,
                    'outline_summary': outline_sum,
                    'pass1_content': pass1_draft,
                    'is_polished': False
                }
            )

            progress = 25 + int((i / target_count) * 35) # 25% to 60%
            book.progress_percentage = progress
            book.current_step_description = f"Drafted Chapter {i} of {target_count} (Pass 1)"
            book.save()
            
            GenerationLog.objects.create(
                book=book, pass_number=1, message=f"Drafted Chapter {i}: {ch_title}"
            )
            time.sleep(0.5)

        # Pass 1 Complete
        book.status = GenerationStatus.PASS1_COMPLETE
        book.progress_percentage = 60
        book.current_step_description = "Pass 1 complete. Starting Pass 2 review & quality polish..."
        book.save()

        GenerationLog.objects.create(
            book=book, pass_number=1, message="Pass 1 Completed successfully!"
        )
        time.sleep(1)

        # --- PASS 2: REVIEW & POLISH ---
        book.status = GenerationStatus.REVIEWING_PASS2
        book.current_pass = 2
        book.save()

        GenerationLog.objects.create(
            book=book, pass_number=2, message="Pass 2 Started: Analyzing consistency, tone, and prose quality"
        )

        chapters = book.chapters.all()
        total_ch = chapters.count()

        for idx, chapter in enumerate(chapters, start=1):
            # Review and refine pass 1 text
            review_notes = (
                f"Pass 2 Quality Review: Checked plot consistency against main premise. "
                f"Enhanced descriptive prose and tone alignment ({book.style_reference or 'standard tone'})."
            )
            
            pass2_polished = (
                f"Chapter {chapter.number}: {chapter.title}\n\n"
                f"Golden sunlight streamed across the landscape, marking a memorable beginning. {book.premise}.\n\n"
                f"With every deliberate step, the atmosphere resonated with depth and character. Drawing clear inspiration from {book.style_reference or 'timeless literature'}, "
                f"the narrative unfolded with vivid detail, seamless dialogue, and elevated prose quality.\n\n"
                f"As twilight embraced the horizon, the resolution of this chapter left an indelible impression."
            )

            chapter.pass2_content = pass2_polished
            chapter.pass2_review_notes = review_notes
            chapter.is_polished = True
            chapter.save()

            progress = 60 + int((idx / total_ch) * 38) # 60% to 98%
            book.progress_percentage = progress
            book.current_step_description = f"Polished Chapter {idx} of {total_ch} (Pass 2 Review)"
            book.save()

            GenerationLog.objects.create(
                book=book, pass_number=2, message=f"Reviewed & polished Chapter {idx}"
            )
            time.sleep(0.5)

        # --- COMPLETED ---
        book.status = GenerationStatus.COMPLETED
        book.progress_percentage = 100
        book.current_step_description = "Book generation fully completed and ready for export!"
        book.save()

        GenerationLog.objects.create(
            book=book, pass_number=2, message="Pass 2 Complete: Book finalized successfully!"
        )

    except Exception as e:
        try:
            book = Book.objects.get(id=book_id)
            book.status = GenerationStatus.FAILED
            book.current_step_description = f"Error during generation: {str(e)}"
            book.save()
            GenerationLog.objects.create(
                book=book, pass_number=book.current_pass, message=f"Generation failed: {str(e)}"
            )
        except Exception:
            pass
