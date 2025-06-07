import json
import os
import time
import random 
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, WebDriverException

# Define the output directory
OUTPUT_DIR = r"C:\Users\Victus\Desktop\New folder (2)"

# Path to the manually downloaded ChromeDriver
CHROMEDRIVER_PATH = r"C:\Users\Victus\Desktop\New folder (2)\chromedriver-win64\chromedriver.exe"

# List of test URLs (ALL YOUR PROVIDED LINKS)
test_urls = [
    # "https://fekrbekr.com/onlinetests/mbti-test/",
    # "https://fekrbekr.com/onlinetests/mmpi-test/",
    # "https://fekrbekr.com/onlinetests/cattell-test/",
    # "https://fekrbekr.com/onlinetests/neo-test/",
    # "https://fekrbekr.com/onlinetests/neopir-test/",
    # "https://fekrbekr.com/onlinetests/disc-test/",
    # "https://fekrbekr.com/onlinetests/archetype-test/", # Testing archetype
    # "https://fekrbekr.com/onlinetests/archetypemen-test/", # Testing archetypemen
    # "https://fekrbekr.com/onlinetests/epqadults-test/",
    # "https://fekrbekr.com/onlinetests/mcmi4-test/",
    # "https://fekrbekr.com/onlinetests/gwpq-test/",
    # "https://fekrbekr.com/onlinetests/typeab-test/",
    # "https://fekrbekr.com/onlinetests/holland-test/",
    # "https://fekrbekr.com/onlinetests/mii-test/",
    "https://fekrbekr.com/onlinetests/msq-test/",
    # "https://fekrbekr.com/onlinetests/eqbaron-test/",
    # "https://fekrbekr.com/onlinetests/sei-test/",
    # "https://fekrbekr.com/onlinetests/ocq-test/",
    # "https://fekrbekr.com/onlinetests/beckdepression-test/",
    # "https://fekrbekr.com/onlinetests/ghq-test/",
    # "https://fekrbekr.com/onlinetests/couplesrel-test/",
    # "https://fekrbekr.com/onlinetests/selfconfidence-test/",
    # "https://fekrbekr.com/onlinetests/hisa-test/",
    # "https://fekrbekr.com/onlinetests/ocd-test/",
    # "https://fekrbekr.com/onlinetests/mbsrq-test/",
    # "https://fekrbekr.com/onlinetests/rrs-test/",
    # "https://fekrbekr.com/onlinetests/posthinking-test/",
    # "https://fekrbekr.com/onlinetests/reldurability-test/",
    # "https://fekrbekr.com/onlinetests/spousecognition-test/",
    # "https://fekrbekr.com/onlinetests/foresight-test/",
    # "https://fekrbekr.com/onlinetests/childintelligence-test/",
    # "https://fekrbekr.com/onlinetests/hillperfectionism-test/",
    # "https://fekrbekr.com/onlinetests/becksuicide-test/",
    # "https://fekrbekr.com/onlinetests/piq-test/",
    # "https://fekrbekr.com/onlinetests/spin-test/",
    # "https://fekrbekr.com/onlinetests/scl90r-test/",
    # "https://fekrbekr.com/onlinetests/yemsq-test/",
    # "https://fekrbekr.com/onlinetests/bei-test/",
    # "https://fekrbekr.com/onlinetests/pwbs-test/",
    # "https://fekrbekr.com/onlinetests/csq-test/"
]

# --- Dictionary for test-specific configurations ---
TEST_CONFIGS = {
    "mbti": {
        "option_selector_candidates": ["div.tileradio label", "div.tileradio2 label"],
        "value_attribute": "value",   
        "value_type": "str",          
        "option_text_selector": "div.box",
        "json_structure": "single_question",
        "extra_option_data": { 
            "attribute": "data-score",
            "type": "int",
            "field_name": "score"
        },
        "value_mapping_strategy": "order_from_left_1", 
    },
    "mmpi": {
        "option_selector_candidates": ["div.tileradio label", "div.tileradio2 label"],
        "value_attribute": "value",
        "value_type": "int", 
        "option_text_selector": "div.box",
        "json_structure": "single_question",
        "value_mapping_strategy": "order_from_left_0", 
    },
    "disc": {
        "option_selector_candidates": ["div#disc-test.tileradio label"],
        "value_attribute": "value", 
        "value_type": "str",
        "option_text_selector": "div.box", 
        "json_structure": "dual_question",
        "actual_options_selector": "div#disc-test.tileradio > div:not([id]):not([class])",
        "value_mapping_strategy": "order_from_left_1", 
    },
    "archetype": {
        "option_selector_candidates": ["div.tileradio label", "div[class*='radio_button_container'] label", "div.eachques label"], # Improved selectors
        "value_attribute": "value",
        "value_type": "int",
        "option_text_selector": "span", # Text is in span for archetypes
        "json_structure": "single_question",
        "value_mapping_strategy": "none", # Use original values
    },
    "archetypemen": {
        "option_selector_candidates": ["div.tileradio2 label", "div[class*='radio_button_container'] label", "div.eachques label"], # Improved selectors
        "value_attribute": "value",
        "value_type": "int",
        "option_text_selector": "span", # Text is in span for archetypemen
        "json_structure": "single_question",
        "value_mapping_strategy": "none", 
    },
    "sei": { 
        "option_selector_candidates": ["div.tileradio2 label", "div.tileradio label"],
        "value_attribute": "value", 
        "value_type": "int",
        "option_text_selector": "div.box",
        "json_structure": "single_question",
        "value_mapping_strategy": "order_from_right_0", 
    },
    "csq": { 
        "option_selector_candidates": ["div.tileradio2 label", "div.tileradio label"],
        "value_attribute": "value",
        "value_type": "int",
        "option_text_selector": "div.box",
        "json_structure": "single_question",
        "value_mapping_strategy": "order_from_right_0", 
    },
    "DEFAULT": {
        "option_selector_candidates": ["div.tileradio2 label", "div.tileradio label", "label"],
        "value_attribute": "value",
        "value_type": "int",
        "option_text_selector": "div.box",
        "json_structure": "single_question",
        "value_mapping_strategy": "none", 
    }
}

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized") 
    
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)
    return driver

def find_elements_robustly(parent_element, css_selectors):
    """Tries a list of CSS selectors to find elements until one works."""
    for selector in css_selectors:
        try:
            elements = parent_element.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                return elements, selector 
        except NoSuchElementException:
            continue
    return [], None 

def extract_questions_and_options_structure(driver, url, test_config):
    try:
        driver.get(url)
        print(f"--- مرحله 1: در حال استخراج ساختار سوالات برای {url} ---")
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.eachques"))
        )
        
        total_questions_element = driver.find_element(By.ID, "questionnaire")
        total_questions = int(total_questions_element.get_attribute("data-quesno"))
        print(f"تعداد کل سوالات برای استخراج ساختار شناسایی شد: {total_questions}")

        questions_structure = []
        
        for ques_num in range(1, total_questions + 1):
            try:
                current_ques_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.eachques[id='ques{ques_num}']"))
                )
                
                question_text = current_ques_element.find_element(By.CLASS_NAME, "eachquestext").text.strip()
                
                raw_options_data = [] 
                
                option_selector_candidates = test_config.get("option_selector_candidates", TEST_CONFIGS["DEFAULT"]["option_selector_candidates"])
                option_labels, used_selector = find_elements_robustly(current_ques_element, option_selector_candidates)

                if not option_labels:
                    print(f"هشدار: هیچ label گزینه‌ای برای سوال {ques_num} با سلکتورهای پیش‌فرض پیدا نشد. تلاش برای استخراج گزینه‌ها ممکن است شکست بخورد.")
                    option_labels = current_ques_element.find_elements(By.CSS_SELECTOR, "label") 

                # Special handling for DISC (dual_question structure)
                if test_config.get("json_structure") == "dual_question" and test_config.get("test_id") == "disc":
                    disc_options_raw_text_elements = current_ques_element.find_elements(By.CSS_SELECTOR, test_config["actual_options_selector"])
                    disc_options_raw_texts = [opt.text.strip() for opt in disc_options_raw_text_elements if opt.text.strip()]
                    
                    all_disc_radio_inputs_a = current_ques_element.find_elements(By.CSS_SELECTOR, "input[type='radio'][name^='ans'][name$='a']")
                    
                    if len(disc_options_raw_texts) == len(all_disc_radio_inputs_a):
                        for i in range(len(disc_options_raw_texts)):
                            option_value = all_disc_radio_inputs_a[i].get_attribute("value")
                            final_value = i # For DISC, map to 0,1,2,3 from left
                            raw_options_data.append({"value": final_value, "text": disc_options_raw_texts[i]})
                    else:
                        print(f"هشدار: عدم تطابق در تعداد گزینه‌های DISC برای سوال {ques_num}. استفاده از متن خام به عنوان گزینه.")
                        for i, text in enumerate(disc_options_raw_texts):
                             raw_options_data.append({"value": i, "text": text}) # Fallback to 0,1,2,3 for text as value

                else: # Generic handling for other tests (CSQ, MBTI, SEI, Archetype, etc.)
                    for label in option_labels:
                        try:
                            input_element = label.find_element(By.CSS_SELECTOR, "input[type='radio']")
                            
                            value_attr_name = test_config.get("value_attribute", TEST_CONFIGS["DEFAULT"]["value_attribute"])
                            value_type = test_config.get("value_type", TEST_CONFIGS["DEFAULT"]["value_type"])
                            option_text_selector = test_config.get("option_text_selector", TEST_CONFIGS["DEFAULT"]["option_text_selector"])

                            option_value_raw = input_element.get_attribute(value_attr_name)
                            option_text_element = label.find_element(By.CSS_SELECTOR, option_text_selector)
                            option_text = option_text_element.text.strip()
                            
                            current_option_data = {"text": option_text}

                            # Set original_value as fallback for 'value' if no mapping strategy
                            if option_value_raw is not None:
                                try:
                                    if value_type == "int":
                                        current_option_data["value"] = int(option_value_raw)
                                    else:
                                        current_option_data["value"] = option_value_raw
                                except (ValueError, TypeError):
                                    current_option_data["value"] = None # Original value invalid
                            else:
                                current_option_data["value"] = None # No original value in HTML

                            # Handle extra data for options
                            extra_data_config = test_config.get("extra_option_data")
                            if extra_data_config:
                                extra_attr_raw = input_element.get_attribute(extra_data_config["attribute"])
                                if extra_attr_raw:
                                    try:
                                        if extra_data_config["type"] == "int":
                                            current_option_data[extra_data_config["field_name"]] = int(extra_attr_raw)
                                        else:
                                            current_option_data[extra_data_config["field_name"]] = extra_attr_raw
                                    except (ValueError, TypeError):
                                        current_option_data[extra_data_config["field_name"]] = None
                            
                            if option_text: 
                                raw_options_data.append(current_option_data)
                        except NoSuchElementException:
                            # This can happen if the label doesn't contain expected input/text element. Skip this label.
                            continue 
                        except Exception as ex:
                            print(f"خطا در پردازش label برای سوال {ques_num}: {ex}")
                            continue 
                    
                # --- Step 2: Apply value mapping strategy to raw_options_data ---
                final_options = []
                num_options = len(raw_options_data)
                
                value_mapping_strategy = test_config.get("value_mapping_strategy", TEST_CONFIGS["DEFAULT"]["value_mapping_strategy"])

                if value_mapping_strategy == "order_from_right_0":
                    for i, opt_data in enumerate(raw_options_data):
                        opt_data["value"] = num_options - 1 - i 
                    raw_options_data.reverse() 
                elif value_mapping_strategy == "order_from_left_0":
                    for i, opt_data in enumerate(raw_options_data):
                        opt_data["value"] = i 
                elif value_mapping_strategy == "order_from_right_1":
                    for i, opt_data in enumerate(raw_options_data):
                        opt_data["value"] = num_options - i 
                    raw_options_data.reverse() 
                elif value_mapping_strategy == "order_from_left_1":
                    for i, opt_data in enumerate(raw_options_data):
                        opt_data["value"] = i + 1 
                # If strategy is "none", 'value' is already set to original_value in Step 1, so no change needed here.

                final_options = raw_options_data # The raw_options_data is now processed and becomes final_options


                if not final_options:
                    print(f"هشدار: هیچ گزینه‌ای برای سوال {ques_num} در هنگام استخراج ساختار پیدا نشد.")
                
                # --- JSON structure based on config ---
                current_json_structure_type = test_config.get("json_structure", TEST_CONFIGS["DEFAULT"]["json_structure"])

                if current_json_structure_type == "single_question":
                    questions_structure.append({
                        "question_id": ques_num,
                        "text": question_text,
                        "scale": test_config.get("scale", "GenericScale"), 
                        "options": final_options
                    })
                elif current_json_structure_type == "dual_question":
                    questions_structure.append({
                        "question_id": f"q{ques_num}a",
                        "text": f"{question_text} (بهترین توصیف)",
                        "scale": test_config.get("scale", "DISC"), 
                        "options": final_options 
                    })
                    questions_structure.append({
                        "question_id": f"q{ques_num}b",
                        "text": f"{question_text} (بدترین توصیف)",
                        "scale": test_config.get("scale", "DISC"), 
                        "options": final_options 
                    })

                # Move to the next question
                if ques_num < total_questions:
                    try:
                        next_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.nextques"))
                        )
                        next_button.click()
                        time.sleep(0.5) 
                    except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as click_e:
                        print(f"هشدار: مشکل در کلیک 'پرسش بعدی' برای سوال {ques_num}: {click_e}. تلاش برای اسکرول و کلیک مجدد.")
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                            time.sleep(0.5) 
                            next_button.click()
                            time.sleep(0.5)
                        except Exception as e_retry:
                            print(f"خطا در تلاش مجدد برای کلیک 'پرسش بعدی' برای سوال {ques_num}: {e_retry}. به سوال بعدی می‌رویم یا متوقف می‌شویم.")
                            if ques_num + 1 <= total_questions:
                                try:
                                    WebDriverWait(driver, 5).until(
                                        EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.eachques[id='ques{ques_num + 1}']"))
                                    )
                                except TimeoutException:
                                    print(f"خطای زمان‌بندی: سوال بعدی {ques_num + 1} بعد از مشکل کلیک پیدا نشد. این مرحله متوقف می‌شود.")
                                    break
                            else:
                                break 

            except TimeoutException:
                print(f"خطای زمان‌بندی: سوال {ques_num} در هنگام استخراج ساختار پیدا نشد. این مرحله متوقف می‌شود.")
                break
            except Exception as e:
                print(f"خطا در هنگام استخراج ساختار برای سوال {ques_num}: {e}")
                print(f"URL: {url}, Test ID: {test_config.get('test_id')}, سوال فعلی: {ques_num}")
                break
        
        return questions_structure, total_questions
    
    except TimeoutException as e:
        print(f"خطای زمان‌بندی هنگام بارگذاری {url} برای استخراج ساختار: {e}")
        return [], 0
    except Exception as e:
        print(f"خطا در واکشی {url} برای استخراج ساختار: {e}")
        return [], 0

def complete_test_and_extract_results(driver, url, total_questions, test_config):
    try:
        driver.get(url)
        print(f"--- مرحله 2: در حال پاسخ دادن به سوالات و استخراج نتایج برای {url} ---")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.eachques"))
        )

        for ques_num in range(1, total_questions + 1):
            try:
                current_ques_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.eachques[id='ques{ques_num}']"))
                )
                
                if test_config.get("json_structure") == "dual_question" and test_config.get("test_id") == "disc":
                    radio_inputs_a = current_ques_element.find_elements(By.CSS_SELECTOR, f"input[type='radio'][name='ans{ques_num}a']")
                    radio_inputs_b = current_ques_element.find_elements(By.CSS_SELECTOR, f"input[type='radio'][name='ans{ques_num}b']")
                    
                    if radio_inputs_a:
                        random_option_a = random.choice(radio_inputs_a)
                        driver.execute_script("arguments[0].click();", random_option_a)
                        print(f"به سوال {ques_num}a پاسخ داده شد (مقدار تصادفی: {random_option_a.get_attribute('value')}).")
                    else:
                        print(f"هشدار: هیچ ورودی رادیویی برای سوال {ques_num}a پیدا نشد. نمی‌توان پاسخ داد.")

                    if radio_inputs_b:
                        random_option_b = random.choice(radio_inputs_b)
                        driver.execute_script("arguments[0].click();", random_option_b)
                        print(f"به سوال {ques_num}b پاسخ داده شد (مقدار تصادفی: {random_option_b.get_attribute('value')}).")
                    else:
                        print(f"هشدار: هیچ ورودی رادیو برای سوال {ques_num}b پیدا نشد. نمی‌توان پاسخ داد.")

                else: # single_question structure (CSQ, MBTI, SEI, Archetype, etc.)
                    radio_inputs = current_ques_element.find_elements(By.CSS_SELECTOR, f"input[type='radio'][name^='ans{ques_num}']")
                    
                    if not radio_inputs:
                        print(f"هشدار: هیچ ورودی رادیویی برای سوال {ques_num} پیدا نشد. نمی‌توان پاسخ داد.")
                        continue
                    
                    random_option = random.choice(radio_inputs)
                    driver.execute_script("arguments[0].click();", random_option)
                    print(f"به سوال {ques_num} پاسخ داده شد (مقدار تصادفی: {random_option.get_attribute('value')}).")
                
                # If not the last question, click 'Next'
                if ques_num < total_questions:
                    try:
                        next_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.nextques"))
                        )
                        next_button.click()
                        time.sleep(0.5)
                    except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as click_e:
                        print(f"هشدار: مشکل در کلیک 'پرسش بعدی' برای سوال {ques_num}: {click_e}. تلاش برای اسکرول و کلیک مجدد.")
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                            time.sleep(0.5) 
                            next_button.click()
                            time.sleep(0.5)
                        except Exception as e_retry:
                            print(f"خطا در تلاش مجدد برای کلیک 'پرسش بعدی' برای سوال {ques_num}: {e_retry}. به سوال بعدی می‌رویم یا متوقف می‌شویم.")
                            if ques_num + 1 <= total_questions:
                                try:
                                    WebDriverWait(driver, 5).until(
                                        EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.eachques[id='ques{ques_num + 1}']"))
                                    )
                                except TimeoutException:
                                    print(f"خطای زمان‌بندی: سوال بعدی {ques_num + 1} بعد از مشکل کلیک پیدا نشد. این مرحله متوقف می‌شود.")
                                    break
                            else:
                                break 
                else:
                    print("به سوال آخر رسید. در حال کلیک روی 'اتمام آزمون'...")
                    finish_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "finish-test"))
                    )
                    finish_button.click()
                    time.sleep(3)
                    print("روی 'اتمام آزمون' کلیک شد. در حال انتظار برای نتایج...")
                    
            except TimeoutException:
                print(f"خطای زمان‌بندی در حین پاسخ دادن/ناوبری برای سوال {ques_num}. نمی‌توان آزمون را تکمیل کرد.")
                return None
            except Exception as e:
                print(f"خطا در حین پاسخ دادن/ناوبری برای سوال {ques_num}: {e}")
                return None
        
        results = {}
        try:
            # Common check for results page being loaded (questions disappear)
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.eachques[id='ques1']")) 
            )
            print("با موفقیت به صفحه نتایج هدایت شد (سوالات ناپدید شده‌اند).")
            
            results["status"] = "Test Completed, results page reached."
            results["note"] = f"Please implement specific result parsing for {test_config.get('test_id')} by inspecting its results page HTML."

            # Example: Try to extract a common "result-summary" div if it exists
            try:
                common_result_summary = driver.find_element(By.CSS_SELECTOR, "#result-summary, .test-result-summary, .results-panel")
                results["summary_text"] = common_result_summary.text.strip()
            except NoSuchElementException:
                results["summary_text"] = "Common result summary element not found. Specific parsing needed."

        except TimeoutException:
            print("زمان‌بندی انتظار برای صفحه/بخش نتایج به پایان رسید. نتایج قابل استخراج نبودند.")
            results["status"] = "Test Completed, but results extraction timed out."
        except Exception as e:
            print(f"خطایی در حین استخراج نتایج رخ داد: {e}")
            results["status"] = f"Test Completed, but error during result extraction: {e}"

        return results
    
    except Exception as e:
        print(f"خطا در تکمیل آزمون و استخراج نتایج: {e}")
        return None

def save_to_json(data, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"فایل JSON در {file_path} ذخیره شد.")

def main():
    driver = None 
    try:
        for url in test_urls:
            parsed_url = urlparse(url)
            test_id = parsed_url.path.split('/')[-2].replace('-test', '')
            test_name = f"تست {test_id.upper()}" 

            test_config = TEST_CONFIGS.get(test_id, TEST_CONFIGS["DEFAULT"]).copy()
            test_config["test_id"] = test_id 
            test_config["test_name"] = test_name 

            driver = setup_driver() 
            
            print(f"\n***** در حال پردازش آزمون: {test_name} ({url}) *****")

            # --- Phase 1: Extract question structure ---
            questions_structure, total_questions = extract_questions_and_options_structure(driver, url, test_config)
            
            if not questions_structure or total_questions == 0:
                print(f"--- در استخراج ساختار سوالات برای {url} شکست خورد. استخراج نتایج رد می‌شود. ---")
                driver.quit() 
                continue 

            # --- Phase 2: Complete the test and extract results ---
            test_results = complete_test_and_extract_results(driver, url, total_questions, test_config)

            final_json_data = {
                "test_id": test_id,
                "test_name": test_name,
                "language": "fa", 
                "questions": questions_structure,
                "results": test_results 
            }
            
            save_to_json(final_json_data, f"{test_id}_test_data.json")
            driver.quit() 
    
    except WebDriverException as e:
        print(f"خطای غیرمنتظره WebDriver رخ داد: {e}")
        if driver:
            driver.quit()
    except Exception as e:
        print(f"خطای غیرمنتظره در اجرای اصلی رخ داد: {e}")
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
