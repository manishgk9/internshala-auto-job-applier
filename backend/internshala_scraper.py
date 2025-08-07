import os
import pickle
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import resume_handler
import json
from selenium.common.exceptions import NoSuchElementException
from google import genai
class InternShalaScraper:
    def __init__(self,username=None,password=None,save_cookie=False,headless=False,gimini_token=None):
        options = uc.ChromeOptions()
        self.username=username
        self.password=password
        self.save_cookie=save_cookie
        self.gimini_token=gimini_token
        self.headless=headless
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-features=VizDisplayCompositor")
        self.client = genai.Client(api_key=gimini_token)if gimini_token else None
        self.driver=uc.Chrome(options=options)
        self.driver.set_window_size(830, 680)
        if os.path.exists('internshala_cookies.pkl'):
            self._load_cookie()
            # time.sleep(1)

            if 'login' in self.driver.current_url.lower():
                self._login()
        else:
            self._login()

    def get_driver(self):
        return self.driver
        
    
    def search_internship_or_job(self,query='e.g. Design, Mumbai, Infosys',page=1):
        url=self._helper_query_url(query,page=page)
        plceholder="e.g. Design, Mumbai, Infosys"
        result=[]
        if query==plceholder or len(query)<3:
            raise ValueError('Please provide a valid search query.')
        
        if url.rstrip('/').lower() in self.driver.current_url.rstrip('/').lower():
                html_data=self.driver.page_source
                return self._helper_internships_or_jobs_scraper(html_data)
        self.driver.get(url)
        self._behave_like_human(3,5)
        try:
            WebDriverWait(self.driver,timeout=8).until(EC.presence_of_element_located((By.ID, "internship_list_container")))
            # self._behave_like_human(1,2)
            html_data=self.driver.page_source
            result=self._helper_internships_or_jobs_scraper(html_data)
            return result
        except Exception as e:
            print(f'Data is not found {e}')
            return result
    
    def get_maching_jobs(self,page_number=1):
            url=f"https://internshala.com/jobs/matching-preferences/page-{page_number}/"
            if url.rstrip('/').lower() in self.driver.current_url.rstrip('/').lower():
                html_data=self.driver.page_source
                return self._helper_internships_or_jobs_scraper(html_data)
            self.driver.get(url)
            self._behave_like_human(3,5)
            try:
                WebDriverWait(self.driver,timeout=10).until(EC.presence_of_element_located((By.ID,'internship_list_container')))
                # self._behave_like_human(1,2)
                html_data=self.driver.page_source
                return self._helper_internships_or_jobs_scraper(html_data)
            except Exception as e:
                print(f"Error loading internship list: {e}")
                return []
    def quit(self):
        self.driver.quit()
    # Extract internship details
    def apply_job_or_int(self,job_url):
        if not self.gimini_token:
            print('please provide a gimini token !')
            return False
    # if not job_url.rstrip('/').lower() in internshala_bot.driver.current_url.rstrip('/').lower():
    #     
        self.driver.get(job_url)
        if not self._helper_is_apply_btn_clicable():  
            print("⏭ Skipping job, already applied.")
            return True

        try:
            time.sleep(2)
            # driver=self.driver
            html=self.driver.page_source
            
            job_detail=self._scrape_job_detail(html)
            if not job_detail:
                print('unable to locate the questionare..')
                return False
            position=job_detail['position']
            skills=job_detail['skills']
            company=job_detail['company']
            about=job_detail['about']
            int_or_job='job'
            self._behave_like_human(1.1,2)
            try:
                apply_btn = WebDriverWait(self.driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply now')]")))
                apply_btn.click()
            except Exception as e:
                print(f'found this after clicking,{e}')
                return False
            self._behave_like_human(1.3,2.5)
            if self.driver.current_url.rstrip('/').lower() in "https://internshala.com/student/resume?detail_source=resume_intermediate".rstrip('/').lower():
                proceed_btn = self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-large.education_incomplete.proceed-btn")
                proceed_btn.click()
                if BeautifulSoup(self.driver.page_source,'html.parser').find('div',{'id','external-job-modal'}):
                    print('it can not be apply threw here it riderect u from internshala.. ')
                    return False
                self._behave_like_human(1.3,2.5)
            if BeautifulSoup(self.driver.page_source,'html.parser').find('div',{'id','external-job-modal'}):
                    print('it can not be apply threw here it riderect u from internshala.. ')
                    return False
            if self._trying_to_solve_assignment(position,about,skills,company,int_or_job):
                return True
            # no locating element
            # pprint(response)
            
            
            print("Applied successfully.")
        except Exception as e:
            print(f"Error during apply: {e}")
            return False


    def _helper_query_url(self,query='',page=1):
        if page==1:
            url=f"https://internshala.com/jobs/keywords-{query}"
            return url
        else:
            return f"https://internshala.com/jobs/keywords-{query}/page-{page}/"

    def _helper_internships_or_jobs_scraper(self,html_data,):
        soup = BeautifulSoup(html_data, 'html.parser')
        individual_class="container-fluid individual_internship view_detail_button visibilityTrackerItem"
        internship_class="container-fluid individual_internship easy_apply button_easy_apply_t visibilityTrackerItem"
        internship_list=soup.find('div',{"id":"internship_list_container"})
        choose_class=None
        if soup.find('div',{'class',individual_class}):
            choose_class=individual_class
        else:
            choose_class=internship_class
        if internship_list:
            internships=internship_list.find_all('div',{"class":choose_class})
            internship_data=[]
            for internship in internships:
                internship_id = internship.get('internshipid')
                employment_type = internship.get('employment_type')

                temp_data = {
                    'id': internship_id,
                    'employment_type': employment_type,
                    'title': internship.find('h3').get_text(strip=True),
                    'url': "https://internshala.com" + internship.find('a').get('href')}

                # Company name and logo
                company_name_tag = internship.find('p', class_='company-name')
                logo_tag = internship.find('img')
                temp_data['company_name'] = company_name_tag.get_text(strip=True) if company_name_tag else None
                temp_data['internship_logo'] = logo_tag.get('src') if logo_tag else None

                # Locations
                locations_tag = internship.find('p', class_='locations')
                locations = [a.get_text(strip=True) for a in locations_tag.find_all('a')] if locations_tag else []
                temp_data['locations'] = locations

                # Salary
                salary_tag = internship.find('span', class_='desktop')
                salary = salary_tag.get_text(strip=True).replace('â‚¹ ', '') if salary_tag else None
                temp_data['salary'] = salary

                # Experience
                experience_tags = internship.find_all('div', class_='row-1-item')
                experience = experience_tags[1].find('span').get_text(strip=True) if len(experience_tags) > 1 else None
                temp_data['experience'] = experience

                # Posted time
                posted_tag = internship.find('div', class_='status-inactive')
                posted_at = posted_tag.find('span').get_text(strip=True) if posted_tag else None
                temp_data['posted_at'] = posted_at
                # temp_data
                internship_data.append(temp_data)
            return internship_data
        else:
            return []
            
        
    def _behave_like_human(self,start_time=2.2,end_time=5):
        if start_time > end_time:
            start_time, end_time = end_time, start_time
        wait_time=random.uniform(start_time, end_time)
        print(f"Waiting for {wait_time:.2f} seconds like a human...")
        time.sleep(wait_time)

    def _scrape_job_detail(self,html_content: str):
        if not html_content:
            raise ValueError("HTML content cannot be empty.")

        soup = BeautifulSoup(html_content, 'html.parser')

        job_details = {
            'position': None,
            'company': None,
            'skills': [],
            'location': None,
            'salary': None,
            'experience': None,
            'openings': None,
            'about':None
        }

        # Extract Position
        position_tag = soup.select_one('.individual_internship_header .profile')
        if position_tag:
            job_details['position'] = position_tag.get_text(strip=True)

        # Extract Company
        company_tag = soup.select_one('.individual_internship_header .company_name a')
        if company_tag:
            job_details['company'] = company_tag.get_text(strip=True)

        # Extract Skills
        skills_tags = soup.select('.round_tabs_container .round_tabs')
        if skills_tags:
            job_details['skills'] = [tag.get_text(strip=True) for tag in skills_tags]

        # Extract Location
        location_tag = soup.select_one('#location_names a')
        if location_tag:
            job_details['location'] = location_tag.get_text(strip=True)
        else:
            # Fallback for 'Work from home' which is not a link
            wfh_tag = soup.find('span', string='Work from home')
            if wfh_tag:
                job_details['location'] = wfh_tag.get_text(strip=True)

        # Extract Salary
        salary_tag = soup.select_one('.salary .desktop')
        if salary_tag:
            job_details['salary'] = salary_tag.get_text(strip=True)

        # Extract Experience
        experience_tag = soup.select_one('.job-experience-item .item_body.desktop-text')
        if experience_tag:
            job_details['experience'] = experience_tag.get_text(strip=True)

        # Extract Openings
        openings_tag = soup.find('h3', string='Number of openings')
        if openings_tag and openings_tag.next_sibling:
            openings_text = openings_tag.next_sibling.get_text(strip=True)
            try:
                job_details['openings'] = int(openings_text)
            except (ValueError, TypeError):
                job_details['openings'] = openings_text
        about_tag=soup.find('div',class_="text-container")
        about=about_tag.get_text(strip=True) if about_tag else None
        job_details['about']=about
        return job_details

    def _fill_form(self,gimini_data,cover_letter_flag=False):
        # Handle cover letter if present
        if cover_letter_flag:
            try:
                cover_letter = gimini_data.get("cover_latter", None)
                if cover_letter:
                    try:
                        # Find the textarea
                        cover_textarea = self.driver.find_element(By.ID, "cover_letter")
                        
                        # Make the textarea visible using JavaScript
                        self.driver.execute_script("arguments[0].style.display = 'block';", cover_textarea)

                        # Clear and send keys
                        cover_textarea.clear()
                        cover_textarea.send_keys(cover_letter)
                        print("Cover letter filled successfully.")
                    except NoSuchElementException:
                        print("Cover letter textarea not found.")
            except Exception as e:
                print(f"Error filling cover letter: {e}")
        for q in gimini_data["questions"]:
            try:
                q_type = q["type"]
                unique_id = q["unique_id"]
                value = q["value"]

                if q_type == "number":
                    try:
                        input_elem = self.driver.find_element(By.ID, unique_id)
                        input_elem.clear()
                        input_elem.send_keys(str(value))
                    except NoSuchElementException:
                        print(f"Number input with id {unique_id} not found.")

                elif q_type == "option":
                    try:
                    # Try selecting option based on ID and value
                        if unique_id=='confirm_availability':
                            continue
                        radio = self.driver.find_element(By.XPATH, f'//input[@id="{unique_id}"][@value="{value}"]')
                        self.driver.execute_script("arguments[0].click();", radio)
                    except:
                        # If not found, try fallback: click first available "Yes"
                        yes_radio = self.driver.find_element(By.XPATH, f'//input[@id="{unique_id}"][@value="yes"]')
                        self.driver.execute_script("arguments[0].click();", yes_radio)

                elif q_type == "textarea":
                    try:
                        textarea = self.driver.find_element(By.ID, unique_id)
                        textarea.clear()
                        textarea.send_keys(value)
                    except NoSuchElementException:
                        print(f"Textarea with id {unique_id} not found.")
            
                elif q_type == "radio":
                    if unique_id == "confirm_availability" or q['label'].lower()=="Confirm your availability".lower():
                        try:
                            radio = self.driver.find_element(By.XPATH, f'//input[@id="{unique_id}"][@value="{value}"]')
                            self.driver.execute_script("arguments[0].click();", radio)
                            continue  # continue using the flow only if confirm_availability is clicked
                        except:
                            print(f"Confirm availability radio with id {unique_id} not found for value '{value}'.")
                            continue  # skip this iteration

                    try:
                        radio = self.driver.find_element(By.XPATH, f'//input[@id="{unique_id}"][@value="{value}"]')
                        self.driver.execute_script("arguments[0].click();", radio)
                    except:
                        print(f"Radio input with id {unique_id} not found for value '{value}'.")

        

                elif q_type == "select":
                    # try:
                    #         dropdown = self.driver.find_element(By.ID, f"{unique_id}_chosen")
                    #         dropdown.click()
                    #         option = self.driver.find_element(By.XPATH, f"//li[text()='{value}']")
                    #         option.click()
                    # except Exception as e:
                    #     print(f"Error select", e)
                    try:
                        timeout=5
                        dropdown_trigger = WebDriverWait(self.driver, timeout).until(
                            EC.element_to_be_clickable((By.ID, f"{unique_id}_chosen"))
                        )
                        dropdown_trigger.click()
                        time.sleep(0.3)  # short wait to open the dropdown

                        # Locate the dropdown options container
                        dropdown_container = WebDriverWait(self.driver, timeout).until(
                            EC.presence_of_element_located((By.XPATH, f"//div[@id='{unique_id}_chosen']//div[contains(@class,'chosen-drop')]"))
                        )

                        # Select the desired option by visible
                        option = dropdown_container.find_element(By.XPATH, f".//li[normalize-space()='{value}']")
                        option.click()

                        # print(f"Successfully selected '{value}' for {unique_id}")
                    except Exception as e:
                        print(f"Error selecting '{value}' for {unique_id}: {e}")

            except Exception as e:
                print(f"Error processing question {q.get('question', 'unknown')}: {e}")
                continue


# scrape_job_data_simple(html)
    def _trying_to_solve_assignment(self,position,about,skills,company,int_or_job):
        # now we need for data for further aprocesses
        # html_data=driver.page_source
        page=self.driver.page_source
        form_container=BeautifulSoup(page,'html.parser').find('div',id='form-container')
        # if this container 0 elment and it has no cover latter then direct apply
        # class="questions-container"
        
        # focus on only custom resume and aditional questions

        prompt=resume_handler.form_field_question_prompt(position,skills,company,int_or_job,about,form_container)

        # pprint(prompt)
        print('|................................................|')
        # sp=BeautifulSoup(page,'html.parser')
        # print(internshala_bot.driver.current_url)
        # (sp.find_all('button',class_="btn btn-primary top_apply_now_cta"))
        cover_letter=False
        if form_container.find('textarea',{'id':'cover_letter'}):
            cover_letter=True
            print('cover letter is required !')
        # else:
            # print('cover letter is not required !')
        if form_container.find('input',{"name":"confirm_availability"}):
            print('confirm availability is required !')
        # else:
        #     print('confirm availability is not required !')
        # submit
        is_direct_apply=len(form_container.find('div',{'class':"questions-container"}))==1 if True else False
        # print(is_direct_apply)
        if  cover_letter!=True and is_direct_apply==True:
            print("appling to job no assignment found.")
            submit=self.driver.find_element(By.ID,'submit')
            time.sleep(1)
            submit.submit()
            return True

            # 
        print("Sending request to gimini here..")
        # print(prompt)
        res=self._gimini_response(prompt)
        respond_data=json.loads(res.strip('`').replace('json\n', '', 1))
        print(respond_data)
        self._fill_form(respond_data,cover_letter_flag=cover_letter)
        try:
            submit_btn=self.driver.find_element(By.ID,'submit')
            submit_btn.click()
            if submit_btn:
                print('the application submitted successfully..')
            return True
        except Exception as e:
            print('something whent wrong..')
            return False
        

    def _helper_is_apply_btn_clicable(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        container = soup.find('div', class_='buttons_container')

        if container:
            button = container.find('button')
            if button:
                btn_text = button.get_text(strip=True).lower()
                if "already applied" in btn_text:
                    return False
                elif "apply now" in btn_text:
                    return True
        print("Could not determine apply status")
        return False
    
    def _gimini_response(self,gimini_prompt):
        try:
            response = self.client.models.generate_content(model="gemini-2.5-flash",contents=gimini_prompt)
            if response:
                return response.text
        except Exception as e:
            return f'Exception found in gimin side. {e}'

    def _login(self):
        if not self.username and not self.password:
                raise ValueError("Username and password are required for login")
        
        url="https://internshala.com/login/user"
        self.driver.get(url)
        self._behave_like_human(1,2.5)
        timeout=5
        try:
            email_field=WebDriverWait(self.driver,timeout,poll_frequency=0.6).until(
                EC.presence_of_element_located((By.ID,'email'))
            )
            self._behave_like_human()
            email_field.send_keys(self.username)
            
            password_field=WebDriverWait(self.driver,timeout,poll_frequency=0.6).until(
                EC.presence_of_element_located((By.ID,'password'))
            )
            password_field.send_keys(self.password)
            self._behave_like_human()

            submit_btn=WebDriverWait(self.driver,timeout,poll_frequency=0.6).until(
                EC.presence_of_element_located((By.ID,'login_submit'))
            )
            self._behave_like_human()
            submit_btn.click()
            self._behave_like_human(1,2.5)
            if self.save_cookie:
                self._store_cookie()
        except Exception as e:
            raise ValueError("Email and password fields are not found !")

    def _load_cookie(self):
        filename = "internshala_cookies.pkl"
        try:
            if os.path.exists(filename):
                with open(filename, "rb") as f:
                    cookies = pickle.load(f)
                self.driver.get("https://internshala.com")
                self._behave_like_human(1.5,2.5)
                for cookie in cookies:
                    if 'expiry' in cookie and not isinstance(cookie['expiry'], (int, float)):
                        del cookie['expiry']
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
                self._behave_like_human(1,2)
                print(f"[✔] Cookies loaded from {filename}")
            else:
                print(f"[!] Cookie file not found at: {filename}")
        except Exception as e:
            print(f"[!] Could not load cookies: {e}")


    def _store_cookie(self):
            if self.save_cookie:
                filename ="internshala_cookies.pkl"
                cookies = self.driver.get_cookies()
                with open(filename, "wb") as f:
                    pickle.dump(cookies, f)
                print(f"[✔] Cookies saved to {filename}")
