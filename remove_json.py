import json
import os

def remove_only_original_value_from_complex_structure(directory_or_filepath):
    """
    Removes ONLY the 'original_value' key from items within the 'options' list,
    which are themselves nested inside the 'questions' list, in JSON files.
    The 'value' key will be preserved.

    Args:
        directory_or_filepath (str): The path to the directory containing the JSON files,
                                      or the full path to a single JSON file.
    """
    def process_file(filepath):
        try:
            with open(filepath, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                modified = False # پرچمی برای نشان دادن اینکه آیا فایل تغییر کرده است

                # بررسی می‌کنیم که آیا 'questions' کلید در داده‌ها وجود دارد و یک لیست است
                if "questions" in data and isinstance(data["questions"], list):
                    # روی هر سوال در لیست 'questions' حلقه می‌زنیم
                    for question in data["questions"]:
                        # بررسی می‌کنیم که آیا 'options' کلید در سوال وجود دارد و یک لیست است
                        if isinstance(question, dict) and "options" in question and isinstance(question["options"], list):
                            # روی هر آیتم option در لیست 'options' حلقه می‌زنیم
                            for option_item in question["options"]:
                                # بررسی می‌کنیم که آیا 'original_value' در آیتم option وجود دارد
                                if isinstance(option_item, dict) and "original_value" in option_item:
                                    del option_item["original_value"] # فقط کلید 'original_value' را حذف می‌کنیم
                                    modified = True # تغییر اعمال شده است

                if modified:
                    f.seek(0)  # رفتن به ابتدای فایل
                    json.dump(data, f, indent=4, ensure_ascii=False) # داده‌های تغییر یافته را می‌نویسیم
                    f.truncate()  # حذف بخش‌های اضافی در صورت کوچک شدن فایل
                    print(f"Successfully processed and modified: {filepath}")
                else:
                    print(f"'original_value' not found in 'questions' -> 'options' for: {filepath} (no change)")

        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {filepath}")
        except Exception as e:
            print(f"An error occurred while processing {filepath}: {e}")

    # تعیین اینکه ورودی یک دایرکتوری است یا یک فایل تکی
    if os.path.isdir(directory_or_filepath):
        # پردازش تمام فایل‌های JSON در دایرکتوری
        for filename in os.listdir(directory_or_filepath):
            if filename.endswith(".json"):
                filepath = os.path.join(directory_or_filepath, filename)
                process_file(filepath)
    elif os.path.isfile(directory_or_filepath) and directory_or_filepath.endswith(".json"):
        # پردازش یک فایل JSON تکی
        process_file(directory_or_filepath)
    else:
        print(f"Error: '{directory_or_filepath}' is neither a valid directory nor a JSON file.")


# --- نحوه استفاده از اسکریپت ---
if __name__ == "__main__":
    # --- گزینه 1: پردازش یک فایل JSON تکی ---
    # مسیر کامل فایل JSON خود را در اینجا جایگزین کنید
    # مثال: r"C:\\Users\\Victus\\Desktop\\New folder (2)\\beckdepression_test_data.json"
    single_file_path = r"" # این خط را برای فایل خاص خودت به‌روز کن

    # --- گزینه 2: پردازش تمام فایل‌های JSON در یک دایرکتوری ---
    # مسیر پوشه حاوی فایل‌های JSON خود را در اینجا جایگزین کنید
    # مثال: r"C:\\Users\\Victus\\Desktop\\New folder (2)"
    json_files_directory = "" # این خط را اگر پوشه‌ای از فایل‌ها داری به‌روز کن

    print(f"--- در حال پردازش یک فایل تکی: {single_file_path} ---")
    remove_only_original_value_from_complex_structure(single_file_path)

    print(f"\n--- در حال پردازش تمام فایل‌ها در یک دایرکتوری: {json_files_directory} (در صورت وجود) ---")
    remove_only_original_value_from_complex_structure(json_files_directory)

    print("\nپردازش تمام فایل‌ها/دایرکتوری‌های مشخص شده به پایان رسید.")