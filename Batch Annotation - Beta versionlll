#This is a beta version
# Need PubMed ID (CSV file),  PubDictionaries dictionary name, and PubAnnotation account information 

import time
import requests
import re
import pandas as pd
from requests.auth import HTTPBasicAuth  # For basic authentication

# Step 1: Fetch Journal Article Text from PubAnnotation
def get_article_text(journal_id):
    url = f"https://pubannotation.org/projects/"Your_Project_Name"/docs/sourcedb/PubMed/sourceid/{journal_id}"  # Replace with your PubAnnotation project name
    
    try:
        timeout_value = 10  # Set a consistent timeout value
        response = requests.get(url, timeout=timeout_value)
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.text
    except requests.Timeout:
        print(f"⏳ Timeout fetching article {journal_id}. Retrying...")
        return None
    except requests.RequestException as e:
        print(f"⚠️ Error fetching article {journal_id}: {e}")
        return None

# Step 2: Submit Text to PubDictionaries API and Wait for Annotation Results
def fetch_annotations_from_pubdictionaries(journal_text):
    dict_url = "https://pubdictionaries.org/text_annotation.json"
    payload = {
        "dictionary": "Lectin_function,Lectin_gene,Lectin_name",  #Replace with your PubDictionaries dictionary names
        "text": journal_text
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        timeout_value = 10  # Set a consistent timeout value
        response = requests.post(dict_url, json=payload, headers=headers, timeout=timeout_value)
        
        if response.status_code == 201:  # Request accepted, but queued
            task_status = response.json()
            task_id = task_status.get("task_id")
            
            if not task_id:
                print("⚠️ Error: No task ID found in response.")
                return None
            
            # Poll API until results are ready
            annotation_result = None
            retries = 0
            while retries < 70:  # Max retries
                time.sleep(5)  # Increased wait time
                try:
                    result_response = requests.get(f"https://pubdictionaries.org/annotation_tasks/{task_id}", timeout=timeout_value)
                    if result_response.status_code == 200:
                        annotation_result = result_response.json()
                        if "annotations" in annotation_result:
                            return annotation_result
                    elif result_response.status_code == 202:
                        print("🔄 Annotation task still in queue. Waiting...")
                    else:
                        print(f"⚠️ Error fetching annotation results: {result_response.status_code}")
                        return None
                except requests.Timeout:
                    print("⏳ Timeout waiting for annotations. Retrying...")
                retries += 1

            print("⚠️ Max retries reached. Annotation task not completed.")
            return None

        elif response.status_code == 200:  # Immediate response with annotations
            return response.json()
        else:
            print(f"⚠️ Error fetching annotations: {response.status_code}, {response.text}")
            return None

    except requests.Timeout:
        print("⏳ Timeout connecting to PubDictionaries. Skipping...")
        return None
    except requests.RequestException as e:
        print(f"⚠️ Error connecting to PubDictionaries: {e}")
        return None

# Step 3: Extract and Format Annotations
def extract_annotations(journal_text, annotation_data):
    annotations = []

    if "annotations" not in annotation_data:
        print("⚠️ No annotations found in response.")
        return []

    for entry in annotation_data["annotations"]:
        term = entry["word"]
        dictionary_type = entry["dictionary"]
        
        for match in re.finditer(rf"\b{re.escape(term)}\b", journal_text, re.IGNORECASE):
            start, end = match.start(), match.end()
            annotations.append({
                "begin": start,
                "end": end,
                "obj": dictionary_type
            })

    return annotations

# Step 4: Submit Annotations to PubAnnotation
def submit_annotations(journal_id, annotations):
    email = "12345@edu.ac.jp"  # Your account Email for PubAnnotation
    password = "Writeyourpaper"  # Your account PW for PubAnnotation
    
    url = f"https://pubannotation.org/projects/Lectin_function/docs/sourcedb/PubMed/sourceid/{journal_id}/annotations.json"
    
    payload = {"annotations": annotations}
    headers = {"Content-Type": "application/json"}
    
    try:
        timeout_value = 10  # Set a consistent timeout value
        response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(email, password), timeout=timeout_value)
        
        if response.status_code == 200:
            print(f"✅ Annotations submitted successfully for {journal_id}!")
        else:
            print(f"⚠️ Error submitting annotations: {response.status_code}, {response.text}")

    except requests.Timeout:
        print(f"⏳ Timeout submitting annotations for {journal_id}. Skipping...")
    except requests.RequestException as e:
        print(f"⚠️ Error submitting annotations for {journal_id}: {e}")

# Step 5: Run the Annotation Process
def main():
    try:
        df = pd.read_csv("PubMed_ID_list.csv")  # Ensure the correct file path of your PubMed ID CSV file
        journal_ids = df["journal_id"].tolist()  # Make sure the column name of the list is call "journal_id"
    except Exception as e:
        print(f"⚠️ Error reading CSV file: {e}")
        return
    
    for journal_id in journal_ids:
        print(f"\n🔄 Processing journal ID: {journal_id}")
        journal_text = get_article_text(journal_id)
        
        if journal_text:
            annotation_data = fetch_annotations_from_pubdictionaries(journal_text)
            
            if annotation_data:
                annotations = extract_annotations(journal_text, annotation_data)
                
                if annotations:
                    submit_annotations(journal_id, annotations)
                else:
                    print(f"⚠️ No relevant annotations found for {journal_id}")
            else:
                print(f"⏭️ Skipping submission for {journal_id} due to missing annotation data.")

if __name__ == "__main__":
    main()


