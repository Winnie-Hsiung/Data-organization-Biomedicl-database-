#Use keyword to search PubMed article

import pandas as pd
from Bio import Entrez
from Bio import Medline

# Step 1: Set up your email for NCBI
Entrez.email = "XXX@ucb.edu"  # Replace with your actual email

# Step 2: Function to search PubMed using a keyword
def search_pubmed(keyword, max_results=20000):
    """Search PubMed for articles matching the keyword and return a list of PMIDs."""
    try:
        handle = Entrez.esearch(db="pubmed", term=keyword, retmax=max_results)
        record = Entrez.read(handle)
        pmids = record["IdList"]
        return pmids
    except Exception as e:
        print(f"⚠️ Error searching PubMed: {e}")
        return []

# Step 3: Fetch article details using Medline
def fetch_pubmed_articles(pmids):
    """Retrieve article details from PubMed using PMIDs and Medline format."""
    articles = []
    
    try:
        handle = Entrez.efetch(db="pubmed", id=",".join(pmids), rettype="medline", retmode="text")
        records = Medline.parse(handle)

        for record in records:
            articles.append({
                "PubMed_ID": record.get("PMID", ""),
                "Title": record.get("TI", ""),
                "Authors": "; ".join(record.get("AU", [])),
                "Abstract": record.get("AB", ""),
                "Keywords": "; ".join(record.get("OT", [])),
                "Journal": record.get("JT", ""),
                "Conclusions": "",  # Not always available in PubMed
                "Methods": "",
                "Results": "",
                "Copyrights": record.get("CI", ""),
                "DOI": record.get("LID", "").split()[0] if "LID" in record else "",
                "Publication_Date": record.get("DP", "")
            })

    except Exception as e:
        print(f"⚠️ Error fetching articles: {e}")

    return articles

# Step 4: Save results to CSV
def save_to_csv(article_list, file_name="file_path_searching results.csv"): #Replace of your file path for result csv
    """Save the list of articles to a CSV file."""
    if article_list:
        df = pd.DataFrame(article_list)
        df.to_csv(file_name, index=False)
        print(f"✅ Results saved to {file_name}")
    else:
        print("⚠️ No data to save.")

# Step 5: Main Execution
def main():
    keyword = input("Enter a keyword to search PubMed: ")
    max_results = int(input("Enter the number of results to fetch (default 50): ") or 50)
    
    print(f"🔍 Searching PubMed for '{keyword}'...")
    pmids = search_pubmed(keyword, max_results)

    if pmids:
        print(f"✅ Found {len(pmids)} articles. Fetching details...")
        articles = fetch_pubmed_articles(pmids)
        save_to_csv(articles)
    else:
        print("⚠️ No articles found.")

if __name__ == "__main__":
    main()
