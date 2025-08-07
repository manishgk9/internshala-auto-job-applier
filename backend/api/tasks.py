from celery import shared_task
from internshala_scraper import InternShalaScraper
from .models import AppliedJobs 

@shared_task
def apply_jobs_in_background(email, password, token, job_data):
    internshala_bot = InternShalaScraper(username=email, password=password, gimini_token=token, save_cookie=True)
    
    try:
        for job in job_data:
            job_id = job.get('job_id')
            title = job.get('job_title')
            company = job.get('company_name')
            url = job.get('url')

            applied = None
            try:
                existing_job = AppliedJobs.objects.filter(job_id=job_id).first()

                if existing_job and existing_job.status in ['applied', 'cancelled']:
                    print(f"Job {job_id} already handled with status: {existing_job.status}. Skipping.")
                    continue

                # If job exists and is still "processing", we should probably skip or wait
                if existing_job and existing_job.status == 'processing':
                    print(f"Job {job_id} is already being processed. Skipping to avoid duplication.")
                    continue

                # Create or update the job as "processing"
                if not existing_job:
                    applied = AppliedJobs.objects.create(
                        job_id=job_id,
                        job_title=title,
                        company_name=company,
                        url=url,
                        status="processing"
                    )
                else:
                    applied = existing_job
                    applied.status = 'processing'
                    applied.save()

                # Try applying
                is_applied = internshala_bot.apply_job_or_int(url)
                if is_applied:
                    print(f'Applied Successfully: {title} at {company}')
                    applied.status = 'applied'
                else:
                    print(f'Apply button still clickable. Marking as cancelled.')
                    applied.status = 'cancelled'
                applied.save()

            except Exception as e:
                print(f"Error while applying to job {job_id}: {str(e)}")
                if applied:
                    applied.status = 'cancelled'
                    applied.save()
                else:
                    # If job failed before creation
                    AppliedJobs.objects.create(
                        job_id=job_id,
                        job_title=title,
                        company_name=company,
                        url=url,
                        status="cancelled"
                    )
                continue

    finally:
        # Quit driver if exists
        if internshala_bot and hasattr(internshala_bot, 'driver'):
            try:
                internshala_bot.driver.quit()
                print("Driver closed.")
            except Exception as e:
                print(f"Error while quitting driver: {str(e)}")
        internshala_bot = None
