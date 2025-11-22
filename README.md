## 📌 Overview 

Project Name:	Employee Of The Month (EOTM)	

Purpose:	Generate sales-style PDF catalogs. Scrapes product pages and exports PDF.	Works on any site with similar product pages.

## 🧰 Installation & Requirements (TSV)

Included Dependencies:	reportlab, bs4, requests, pillow	(Python libraries)

## 🔗 How to Provide Product URLs (TSV)
-Input 5 example product URLs	

-Enter when prompted	

-Must be actual product detail pages	

-Should contain title & description

-Key Rule	URLs **must be product detail pages**	Example (Correct): https://site.com/item/123	Incorrect: category/cart/home pages

## 📁 Optional Menu URL (TSV)
Optional Input:	Provide a category/catalog page |	Example: https://site.com/products	
  -If unsure, leave blank	
  
  -Improves discovery automatically

### Purpose	Allows auto discovery of matching product links	& finds more detail URLs	based on detected URL pattern

## 🔄 Workflow (TSV)
Step 1	Detect URL pattern	Tool reads your 5 URLs	No config needed	Used to find more products

Step 2	Start scraping	Collects title, description, image, author	Resume-safe: saved to cache.json	Stops duplication

Step 3	Cache usage	Saves and loads progress	Allows stopping and restarting	No lost work

Step 4	PDF generation	Only after scraping completes	Output in output_pdfs/catalog.pdf	📌 PDFs do NOT appear during scraping

## 📄 PDF Output (TSV)
Title, author, description, image	-- alter as per your industry

  Location:	catalog.pdf	is saved to output_pdfs/	Generated automatically after scraping	

## 🤖 🌟 Optional LLM Summaries (Highly Recommended!)
-Feature:	Optional AI-based summaries	

-Triggered by answering **Y** in terminal	✨ Strongly improves the brochure created

-Recommendation:	**Highly recommended**	

-Makes description shorter + clearer	

-Best for catalogs shared publicly

-Fallback	Works **without any external AI**	

-Local summarizer included	

-Can upgrade later to GPT/Claude/Local Models

## Local LLM (Phi-3-mini-4k-instruct-q4.gguf)				

Download Model:	Get the GGUF file from HuggingFace	https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf	
  -You may need a HuggingFace account

Choose File:	Download the quantized version	Phi-3-mini-4k-instruct-q4.gguf	
  -Q4 is faster on CPU

Placement:	Copy the file into your project’s root folder	
  -Same folder as eotm.py and /engine/	Do NOT store inside /engine/

Verification:	Model must be at the top-level directory

## 🗂 Internal File Responsibilities (TSV)

-eotm.py	Main executable	Run this to start tool	python eotm.py

-autodetect.py	Detect product URL structure	Learns pattern from your 5 URLs	No editing required

-scrape.py	Scrape product links + details	Finds & extracts data automatically	Uses detected pattern

-pdf_generator.py	Generate PDF catalog	Outputs academic PDF	PDF only after scraping completes

-utils.py	Extract text + images	No CSS selectors needed	Heuristic extraction

-cache.py	Store scraping progress	Saves and loads cache.json	Supports resume scraping

-llm.py	Optional AI summary	Shortens long text 💬	Make PDF more readable
