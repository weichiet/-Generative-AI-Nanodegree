# 💬 Build Your Own Custom Chatbot

## 📌 Project Overview

This project focuses on building a **custom OpenAI-powered chatbot** tailored to a specific domain or dataset. Unlike frameworks like LangChain, you'll build the chatbot from scratch using core Python libraries such as `openai` and `pandas`, giving you a deeper understanding of how language models can be customized and deployed in real-world scenarios.

---

## 🎯 What You'll Build

By the end of this project, you will have created a **domain-specific chatbot** powered by OpenAI’s API. You will:

- ✅ Select and justify a relevant dataset
- ✅ Prepare and clean the dataset for use in prompting
- ✅ Integrate the dataset into a custom chatbot workflow
- ✅ Demonstrate the impact of customization by comparing responses with and without the custom data

---

## 📚 Dataset Options

You may use one of the provided datasets or choose your own:

### 🔹 Provided Datasets
- `2023_fashion_trends.csv`: Articles and quotes related to 2023 fashion trends
- `character_descriptions.csv`: Fictional character profiles from various media
- `nyc_food_scrap_drop_off_sites.csv`: Info on food scrap drop-off locations in NYC

### 🔹 Custom Dataset (Optional)
You are encouraged to use your own dataset (min. 20 rows of text data). Examples:
- Wikipedia articles (via API)
- Web-scraped documents
- Personal document collections

> 📌 Note: OpenAI models perform best on text-based data. Avoid datasets focused heavily on numbers or logical calculations.

---

## 🧠 Customization Scenario

To demonstrate the value of your custom chatbot, you’ll define a **use-case scenario** where this chatbot would be useful. You’ll show that the model’s responses improve meaningfully with the inclusion of custom data by:

1. Writing a brief explanation of your scenario and dataset at the start of the notebook.
2. Demonstrating comparative Q&A examples at the end—before and after customization.

---

## 🔧 Project Instructions

All work is performed in `project.ipynb`, where you will complete the following tasks:

### 1️⃣ Choose a Dataset and Define the Scenario
Describe your chosen dataset and explain why it is appropriate for customizing the chatbot.

### 2️⃣ Prepare the Dataset
Reformat and clean the data as needed so it can be loaded into a `pandas` DataFrame with a column named `"text"`.

### 3️⃣ Integrate the Dataset into the Chatbot
Incorporate your dataset into the custom chatbot codebase. This step connects your data to the prompt generation logic.

### 4️⃣ Evaluate Customization with Q&A
Write at least two questions and compare the chatbot’s answers before and after the customization to show the difference in performance.

---

## 📂 Deliverables

All relevant outputs are located in the [`/deliverables`](./deliverables) folder, including:

- ✅ The dataset
- 🤖 Chatbot code and responses in Jupyter Notebook
---