# Grounded Policy Bot

## Student

Matthew Podraza

## Topic

This bot answers questions about Central Piedmont Community College attendance policy.

## Source

Central Piedmont Policy 3.09 Attendance:  
https://www.cpcc.edu/policies-and-procedures/policies/309-attendance

## How to run

Install packages with: `pip install -r requirements.txt`

Run the tests with: `python test_retriever.py`

Run the app with: `streamlit run grounded_bot.py`

## Retrieval design

The retriever uses TF-IDF and cosine similarity. The analyzer converts text to lowercase, extracts words, applies simple stemming, and adds bigrams.

The eight questions that should retrieve produced scores from 0.357 to 0.755. The five questions that should be refused produced scores from 0.121 to 0.240.

Based on this printed evidence, I set the similarity threshold to 0.30. This places the threshold above the highest refusal score of 0.240 and below the lowest correct retrieval score of 0.357.

The automated result was: `PASS: 13/13 retrieval tests`

## Grounding and refusal behavior

If retrieval returns an empty list, the program returns the refusal directly without creating a Groq client or calling the model.

Exact refusal message:

> I don't have enough information in the provided knowledge base to answer that.

When retrieval succeeds, the prompt tells the model to use only the retrieved knowledge, not use outside knowledge, and not guess dates, amounts, percentages, or other numbers. The retrieved context and the student's question are inside separate labeled boundaries.

Sources are displayed under every supported answer. Source attribution also helps diagnose errors. No retrieved sources indicates a retrieval failure. An unsupported answer displayed with relevant sources would instead indicate a grounding-prompt or generation failure.

## Hallucination tests

These five questions are close to the attendance topic, but their answers are not contained in the knowledge chunks.

### Test 1

Question: Does attendance change my final grade?

Actual response:

> I don't have enough information in the provided knowledge base to answer that.

### Test 2

Question: Can I appeal an attendance decision?

Actual response:

> I don't have enough information in the provided knowledge base to answer that.

### Test 3

Question: Are online courses required to record attendance?

Actual response:

> I don't have enough information in the provided knowledge base to answer that.

### Test 4

Question: Can my parent view my attendance?

Actual response:

> I don't have enough information in the provided knowledge base to answer that.

### Test 5

Question: Will an absence lower my grade?

Actual response:

> I don't have enough information in the provided knowledge base to answer that.

## Changes made after testing

- I changed the threshold from the starter value of 0.0 to 0.30 using the printed score evidence.
- I wrote each knowledge chunk as one self-contained fact using words a student would naturally use.
- I included phrases such as "miss class," "attendance rules," "religious absence," "make up work," and "military absences" so student questions retrieve the correct chunks.
- I added a short circuit so an empty retrieval never calls the model.
- I strengthened the grounding prompt to forbid outside knowledge and guessing numbers.
- I added an exact refusal message.
- I clearly separated retrieved context from the student's question.
- I displayed the source under each supported answer.

## What I would improve with more time

With more time, I would expand the knowledge base with additional official attendance-policy details and add more varied test questions. I would also improve the interface by keeping a visible question-and-answer history while continuing to show the source for every supported answer.
