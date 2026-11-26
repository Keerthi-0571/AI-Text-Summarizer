# Assignment 1: Prompt Design & Evaluation

**Skill Nexis | LLM Development | Week 1**

**Name:** K S Keerthi

---

## Part 1. Key concepts

### Tokens

A token is the small piece of text a language model actually reads and writes. It can be a whole short word, part of a longer word, a number, or a punctuation mark. A tokenizer splits text into tokens and maps each one to an ID number. In English, one token is roughly three-quarters of a word, so 100 words is about 130 tokens. Models are priced, limited and measured in tokens, not words. Rare words, code and some languages split into more tokens than common English words do.

**Example:** "Summarization is useful." might become `Summar` `ization` ` is` ` useful` `.`

### Context window

The context window is the maximum number of tokens a model can consider at one time. It includes everything: the instructions, the pasted text, the earlier conversation, and the answer the model is writing. If the input is too long, it must be shortened, split into chunks or truncated, and anything outside the window is invisible to the model. This is why my summarizer splits long documents into chunks (the model I used reads about 1,024 tokens at once).

### Inference

Inference is using an already-trained model to produce output. The model is not learning anything at this point. It reads the prompt, then predicts one token at a time, each based on all the tokens before it, until it reaches a stop condition. Settings such as temperature, beam search and maximum length control how it picks tokens. Training (changing the model's weights) is separate and far more expensive than inference.

### Hallucination

A hallucination is output that sounds fluent and confident but is false, unsupported by the source, or invented. It happens because a language model is trained to predict plausible text, not to check facts, so it will still produce an answer when it lacks the information. Typical cases are invented numbers, names, quotes or citations. Ways to reduce it: tell the model to use only the supplied text, allow it to say "not stated", supply source documents (RAG), and verify important claims against the source.

---

## Part 2. Prompts for four task types

For each task, there is a **basic prompt** (short and vague) and an **improved prompt** (clear task, format and constraints).

### 1. Summarization

- **Basic:** `Summarize this.`
- **Improved:** `Summarize the text below in exactly 2 sentences for a general reader. Keep all numbers and names that matter. Use only facts stated in the text. Do not add opinions.`

### 2. Extraction

- **Basic:** `Get the details from this.`
- **Improved:** `Extract the information from the text below. Use only the specified fields. If a detail is missing, write "Not specified". Do not calculate or assume missing information.`

### 3. Classification

- **Basic:** `Classify this.`
- **Improved:** `Classify the sentiment of the text below using only one of these labels: Positive, Negative, Mixed. Return only the label. Do not provide an explanation.`

### 4. Question answering

- **Basic:** `Answer this question.`
- **Improved:** `Answer the question using only the information in the passage. If the answer is not stated, write "Not stated". Return only the answer, without explanation.`

---

## Part 3. Basic vs improved prompts on ten examples

**How to run this:** Each input was tested using the same model. The basic prompt was tested first, followed by the improved prompt in a new chat each time. The outputs were recorded and evaluated using the criteria in Part 4.

**Model used:** GPT-6 (ChatGPT)

### The ten test cases

**S1. Summarization**

> The town council voted 6 to 3 on Tuesday to add protected bike lanes along Mill Street, a 2.4 km stretch between the station and the market. Construction will start in April and cost about 1.8 million dollars, paid mostly by a regional transport grant. Shop owners worried about losing 40 parking spaces, so the council promised to build a new car park behind the market by next summer.

**Reference points:** 6–3 vote, Mill Street, 2.4 km, starts in April, 1.8 million dollars, 40 parking spaces lost, new car park by next summer.

**S2. Summarization**

> A software company released version 4.0 of its note-taking app on Monday. The update adds offline mode, faster search, and a shared-folders feature for teams of up to 25 people. The free plan keeps its 100-note limit, but the paid plan drops from 8 dollars to 6 dollars a month. Some users complained on forums that the new design hides the export button, and the company said it will move it back in version 4.1.

**Reference points:** version 4.0, offline mode, faster search, shared folders (up to 25), free plan 100 notes, price 8 → 6 dollars, export button complaint, fix in 4.1.

**S3. Summarization**

> Heavy rain is expected across the coastal districts from Thursday evening to Saturday morning, with up to 120 mm falling in some places. The weather office has issued an orange alert and advised fishermen not to go to sea. Schools in two districts will close on Friday. Officials said rivers are not yet at danger level but will be monitored, and the alert may be upgraded if rain continues past Saturday.

**Reference points:** coastal districts, Thursday evening to Saturday morning, up to 120 mm, orange alert, fishermen advised not to go to sea, schools in two districts closed Friday, rivers not yet at danger level, alert may be upgraded.

**E1. Extraction**

Fields: `Presenter`, `Topic`, `Date`, `Time`, `Venue`, `Preparation`.

> Hi team, just confirming that Priya will present the quarterly results on 14 March at 10:30 AM in Meeting Room B. Please bring your reports.

**Expected:** Presenter = Priya, Topic = Quarterly results, Date = 14 March, Time = 10:30 AM, Venue = Meeting Room B, Preparation = Bring reports.

**E2. Extraction**

Fields: `Order Number`, `Customer`, `Order Date`, `Items`, `Total Amount`, `Order Status`.

> Order #4821 was placed by Daniel Lee on 8 June. It contains 3 wireless keyboards at $25 each and 2 USB hubs at $12 each. The order status is Processing.

**Expected:** Order Number = #4821, Customer = Daniel Lee, Order Date = 8 June, Items = 3 wireless keyboards at $25 each and 2 USB hubs at $12 each, Total Amount = Not specified, Order Status = Processing.

**C1. Classification**

Labels: Positive, Negative, Mixed.

> The battery lasts two full days and the screen is gorgeous.

**Expected:** Positive.

**C2. Classification**

Labels: Positive, Negative, Mixed.

> Great, another update that deletes all my saved settings. Love that.

**Expected:** Negative (sarcasm).

**C3. Classification**

Labels: Positive, Negative, Mixed.

> The delivery arrived on time, but the box was crushed and one of the three items was missing.

**Expected:** Mixed.

**Q1. Question answering**

> Passage: The Riverside Library opened in 1998 and holds about 42,000 books. It is open Monday to Saturday from 9 AM to 6 PM and is closed on Sundays.

**Question:** What time does the library close on Saturday?

**Expected:** 6 PM.

**Q2. Question answering**

> Passage: The Riverside Library opened in 1998 and holds about 42,000 books. It is open Monday to Saturday from 9 AM to 6 PM and is closed on Sundays.

**Question:** Who is the head librarian?

**Expected:** Not stated. Any name would be unsupported by the passage.

### Results table

Use **Y / N** for each cell, following the criteria in Part 4.

| # | Task | Basic: correct? | Basic: followed instructions? | Improved: correct? | Improved: followed instructions? | What changed / notes |
|---|---|:---:|:---:|:---:|:---:|---|
| S1 | Summarization | Y | Y | Y | Y | Both retained important facts; improved followed the exact 2-sentence requirement. |
| S2 | Summarization | Y | Y | Y | Y | Both retained key details; improved gave a clearer 2-sentence summary. |
| S3 | Summarization | N | Y | N | Y | Basic reversed the fishermen's instruction; improved omitted or generalized important details. |
| E1 | Extraction | Y | Y | Y | Y | Both extracted meeting details; improved followed the specified field format. |
| E2 | Extraction | Y | Y | Y | Y | Basic calculated $99; improved returned Not specified because calculation was prohibited. |
| C1 | Classification | Y | Y | Y | Y | Both correctly classified positive sentiment; improved returned only the label. |
| C2 | Classification | Y | Y | Y | Y | Both correctly identified negative sarcasm; improved returned only the label. |
| C3 | Classification | Y | Y | Y | Y | Both correctly identified mixed sentiment; improved returned only the label. |
| Q1 | Question answering | Y | Y | Y | Y | Both correctly answered 6 PM; improved followed the answer-only instruction. |
| Q2 | Question answering | Y | Y | Y | Y | Both correctly identified that the answer was not stated; improved followed the answer-only instruction. |
| | **Total (out of 10)** | **9/10** | **10/10** | **9/10** | **10/10** | |

**Note on the basic prompt for E1, E2, C and Q rows:** The basic prompt is the short version from Part 2, followed by the same input. The basic prompt does not state the label set or field names, while the improved prompt provides clearer instructions.

---

## Part 4. Recording errors

### Marking criteria

- **Correct?** Y if every fact in the output is supported by the input and matches the expected answer (or covers the reference points for summaries). N if any fact is wrong, invented or missing.
- **Followed instructions?** Y if the output obeyed every constraint in that prompt (for example, "exactly 2 sentences", "only the label", or the required field format). For the basic prompt, there are few explicit constraints, so judge only against the task itself.

### Error types to look for

| Type | Description | Example |
|---|---|---|
| Factual error | A wrong number, name or claim | Says 2.4 million instead of 1.8 million dollars |
| Hallucination | Invents something not in the input | Names a head librarian in Q2 |
| Omission | Leaves out an important point | Drops the "40 parking spaces" concern in S1 |
| Format violation | Ignores the requested format | Adds a sentence after "reply with only the label" |
| Length violation | Wrong number of sentences or words | Gives 4 sentences when 2 were requested |
| Misreading | Misses tone, sarcasm or intent | Labels C2 as Positive |

### Error log

| # | Prompt (basic / improved) | Error type | What went wrong |
|---|---|---|---|
| 1 | S3 Basic | Misreading / Factual error | Changed "fishermen advised not to go to sea" into "stay at sea", reversing the meaning. |
| 2 | S3 Improved | Omission | Did not explicitly preserve the fishing advice and omitted the information that rivers were not yet at danger level. |

### Findings

The improved prompts made the model's responses more structured and specific, especially in extraction, classification and question answering. Both basic and improved prompts performed correctly in most experiments. However, the S3 basic summary contained a factual error by reversing the fishermen's safety instruction. The improved S3 summary avoided that reversal but still omitted some important details. No hallucinated librarian name appeared in Q2 because both prompts correctly returned that the information was not stated. In future, I would use more specific instructions, preserve all important facts and verify generated summaries against the original text.

---

## Part 5. Prompting vs RAG vs fine-tuning

| | **Prompting** | **RAG (Retrieval-Augmented Generation)** | **Fine-tuning** |
|---|---|---|---|
| **What it is** | Giving a model instructions, examples and context in the prompt | Searching a document collection for relevant passages and adding them to the prompt before the model answers | Training the model further on your own examples so its weights change |
| **What changes** | Only the input | The input (with retrieved text added) | The model itself |
| **Best for** | Quick tasks, formatting, changing tone, trying ideas | Answers that must rely on private, specific or frequently changing documents | Consistent style, format or behaviour on a narrow, repeated task |
| **Knowledge updates** | Add new text to the prompt by hand | Update the document store; no retraining | Requires retraining on new data |
| **Cost and effort** | Lowest; no setup | Medium; needs a document store and search | Highest; needs good training data, compute and testing |
| **Hallucination risk** | Higher for facts the model doesn't know | Lower, because answers can be tied to retrieved sources and cited | Does not fix missing knowledge; can still invent facts |
| **Main limit** | Context window size; results depend on wording | Quality depends on retrieval; irrelevant passages hurt the answer | Needs data and upkeep; hard to correct a single wrong fact |

**How to choose:** Start with prompting. If the model needs facts it doesn't have, such as company policies or recent documents, add RAG. If it knows the facts but keeps getting the style, format or behaviour wrong despite good prompts, consider fine-tuning. The three approaches also combine: a fine-tuned model can be used with RAG and a carefully written prompt.

**Connection to my project:** The summarizer uses a pretrained model as it is, with decoding settings (length limits and beam search) controlling generation. It does not use RAG or fine-tuning. Long inputs are handled by chunking, which is a workaround for the context window limit.