import re
import json

html_path = r"d:\Campusplacement\campusplacement\campusplacement\templates\student\practice.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

sections = ['logic', 'dsa', 'cs_core', 'hr']
pools = {}

for sec in sections:
    # Find the question-list div for this section
    start_tag = f'<div id="{sec}" class="tab-content">'
    if start_tag not in content and sec == 'logic':
        # wait, maybe it doesn't match exactly. Let's use regex
        pass

    # Actually, let's just use regex to find each section
    pattern = re.compile(rf'<div id="{sec}" class="tab-content.*?>.*?<div class="question-list">(.*?)</div>\s*<div class="result-display"', re.DOTALL)
    match = pattern.search(content)
    if not match:
        print(f"Could not find section {sec}")
        continue
    
    questions_html = match.group(1)
    
    # parse questions
    q_pattern = re.compile(r'<div class="question-card">.*?<div class="question-text">\d+\.\s*(.*?)</div>.*?<div class="options-grid">(.*?)</div>\s*</div>', re.DOTALL)
    
    pool = []
    for q_match in q_pattern.finditer(questions_html):
        q_text = q_match.group(1).strip()
        options_html = q_match.group(2)
        
        opt_pattern = re.compile(r'<button class="option-btn" onclick="selectOption\(this\)"(?: data-is-correct="(true)")?>(.*?)</button>', re.DOTALL)
        options = []
        for o_match in opt_pattern.finditer(options_html):
            is_correct = bool(o_match.group(1))
            opt_text = o_match.group(2).strip()
            options.append({"text": opt_text, "correct": is_correct})
        
        pool.append({"q": q_text, "options": options})
        
    pools[sec] = pool

# Add 10 dummy/new questions to each pool to ensure dynamic selection
new_qs = {
    'logic': [
        {"q": "If A is B's brother, B is C's sister, and C is D's father, how is D related to A?", "options": [{"text": "A) Nephew/Niece", "correct": True}, {"text": "B) Cousin", "correct": False}, {"text": "C) Uncle", "correct": False}, {"text": "D) Brother", "correct": False}]},
        {"q": "Find the next number in the sequence: 5, 10, 20, 40, ...", "options": [{"text": "A) 50", "correct": False}, {"text": "B) 60", "correct": False}, {"text": "C) 80", "correct": True}, {"text": "D) 100", "correct": False}]},
        {"q": "If 'APPLE' is coded as 'EQTPI', how is 'MANGO' coded?", "options": [{"text": "A) QERKS", "correct": True}, {"text": "B) PERKS", "correct": False}, {"text": "C) QDRKS", "correct": False}, {"text": "D) REQSK", "correct": False}]},
        {"q": "A clock shows 3:15. What is the angle between the hour and minute hands?", "options": [{"text": "A) 0 degrees", "correct": False}, {"text": "B) 7.5 degrees", "correct": True}, {"text": "C) 15 degrees", "correct": False}, {"text": "D) 22.5 degrees", "correct": False}]},
        {"q": "Choose the odd one out.", "options": [{"text": "A) Square", "correct": False}, {"text": "B) Circle", "correct": True}, {"text": "C) Rectangle", "correct": False}, {"text": "D) Triangle", "correct": False}]},
        {"q": "If all roses are flowers and some flowers are red, which is true?", "options": [{"text": "A) All roses are red", "correct": False}, {"text": "B) Some roses are red", "correct": False}, {"text": "C) No roses are red", "correct": False}, {"text": "D) Cannot be determined", "correct": True}]},
        {"q": "A man is facing North. He turns 90 degrees clockwise, then 135 degrees counter-clockwise. Which direction is he facing?", "options": [{"text": "A) North-East", "correct": False}, {"text": "B) North-West", "correct": True}, {"text": "C) South-East", "correct": False}, {"text": "D) South-West", "correct": False}]},
        {"q": "Which word cannot be formed from 'MEASUREMENT'?", "options": [{"text": "A) MASTER", "correct": False}, {"text": "B) MANTLE", "correct": True}, {"text": "C) SUMMIT", "correct": False}, {"text": "D) ASSURE", "correct": False}]},
        {"q": "In a row of 20 people, A is 5th from the left and B is 8th from the right. How many people are between them?", "options": [{"text": "A) 5", "correct": False}, {"text": "B) 6", "correct": False}, {"text": "C) 7", "correct": True}, {"text": "D) 8", "correct": False}]},
        {"q": "Complete the series: 1, 4, 9, 16, 25, ...", "options": [{"text": "A) 30", "correct": False}, {"text": "B) 32", "correct": False}, {"text": "C) 36", "correct": True}, {"text": "D) 40", "correct": False}]}
    ],
    'dsa': [
        {"q": "Which data structure uses LIFO?", "options": [{"text": "A) Queue", "correct": False}, {"text": "B) Stack", "correct": True}, {"text": "C) Array", "correct": False}, {"text": "D) Tree", "correct": False}]},
        {"q": "What is the time complexity of binary search?", "options": [{"text": "A) O(1)", "correct": False}, {"text": "B) O(n)", "correct": False}, {"text": "C) O(log n)", "correct": True}, {"text": "D) O(n log n)", "correct": False}]},
        {"q": "Which tree traversal visits the root node last?", "options": [{"text": "A) Pre-order", "correct": False}, {"text": "B) In-order", "correct": False}, {"text": "C) Post-order", "correct": True}, {"text": "D) Level-order", "correct": False}]},
        {"q": "A graph without cycles is called a:", "options": [{"text": "A) Tree", "correct": True}, {"text": "B) Cyclic graph", "correct": False}, {"text": "C) Complete graph", "correct": False}, {"text": "D) Bipartite graph", "correct": False}]},
        {"q": "Which algorithm is used to find the minimum spanning tree?", "options": [{"text": "A) Dijkstra's", "correct": False}, {"text": "B) Bellman-Ford", "correct": False}, {"text": "C) Kruskal's", "correct": True}, {"text": "D) Floyd-Warshall", "correct": False}]},
        {"q": "What is a hash collision?", "options": [{"text": "A) Two keys hashing to the same index", "correct": True}, {"text": "B) A missing key", "correct": False}, {"text": "C) An empty hash table", "correct": False}, {"text": "D) A full hash table", "correct": False}]},
        {"q": "Which sorting algorithm is the fastest on a nearly sorted array?", "options": [{"text": "A) Quick Sort", "correct": False}, {"text": "B) Merge Sort", "correct": False}, {"text": "C) Insertion Sort", "correct": True}, {"text": "D) Selection Sort", "correct": False}]},
        {"q": "A queue is implemented using two stacks. What is the time complexity of dequeue?", "options": [{"text": "A) O(1)", "correct": False}, {"text": "B) Amortized O(1)", "correct": True}, {"text": "C) O(n)", "correct": False}, {"text": "D) O(n^2)", "correct": False}]},
        {"q": "Which data structure is best for a priority queue?", "options": [{"text": "A) Array", "correct": False}, {"text": "B) Linked List", "correct": False}, {"text": "C) Heap", "correct": True}, {"text": "D) Stack", "correct": False}]},
        {"q": "What is the worst-case time complexity of accessing an element in a binary search tree?", "options": [{"text": "A) O(1)", "correct": False}, {"text": "B) O(log n)", "correct": False}, {"text": "C) O(n)", "correct": True}, {"text": "D) O(n log n)", "correct": False}]}
    ],
    'cs_core': [
        {"q": "What does SQL stand for?", "options": [{"text": "A) Structured Query Language", "correct": True}, {"text": "B) Simple Query Language", "correct": False}, {"text": "C) Sequential Query Language", "correct": False}, {"text": "D) Standard Query Language", "correct": False}]},
        {"q": "Which layer of the OSI model does TCP operate on?", "options": [{"text": "A) Network Layer", "correct": False}, {"text": "B) Transport Layer", "correct": True}, {"text": "C) Data Link Layer", "correct": False}, {"text": "D) Application Layer", "correct": False}]},
        {"q": "What is virtual memory?", "options": [{"text": "A) RAM", "correct": False}, {"text": "B) Cache", "correct": False}, {"text": "C) Hard disk space used as RAM", "correct": True}, {"text": "D) Cloud storage", "correct": False}]},
        {"q": "Which scheduling algorithm gives the minimum average waiting time?", "options": [{"text": "A) FCFS", "correct": False}, {"text": "B) SJF", "correct": True}, {"text": "C) Round Robin", "correct": False}, {"text": "D) Priority", "correct": False}]},
        {"q": "What is an IP address?", "options": [{"text": "A) A physical address", "correct": False}, {"text": "B) A logical address", "correct": True}, {"text": "C) A MAC address", "correct": False}, {"text": "D) A domain name", "correct": False}]},
        {"q": "Which of the following is a NoSQL database?", "options": [{"text": "A) MySQL", "correct": False}, {"text": "B) PostgreSQL", "correct": False}, {"text": "C) MongoDB", "correct": True}, {"text": "D) Oracle", "correct": False}]},
        {"q": "What is the purpose of a firewall?", "options": [{"text": "A) To speed up the network", "correct": False}, {"text": "B) To block unauthorized access", "correct": True}, {"text": "C) To store data", "correct": False}, {"text": "D) To compile code", "correct": False}]},
        {"q": "What is thrashing in an OS?", "options": [{"text": "A) Excessive swapping of pages", "correct": True}, {"text": "B) A fast process execution", "correct": False}, {"text": "C) Disk failure", "correct": False}, {"text": "D) A network collision", "correct": False}]},
        {"q": "Which HTTP method is idempotent?", "options": [{"text": "A) POST", "correct": False}, {"text": "B) PUT", "correct": True}, {"text": "C) PATCH", "correct": False}, {"text": "D) CONNECT", "correct": False}]},
        {"q": "What is a primary key?", "options": [{"text": "A) A non-unique identifier", "correct": False}, {"text": "B) A unique identifier for a record", "correct": True}, {"text": "C) A reference to another table", "correct": False}, {"text": "D) A sorted index", "correct": False}]}
    ],
    'hr': [
        {"q": "How should you dress for a professional interview?", "options": [{"text": "A) Casual attire", "correct": False}, {"text": "B) Professional/Business attire", "correct": True}, {"text": "C) Gym clothes", "correct": False}, {"text": "D) Party wear", "correct": False}]},
        {"q": "What is the best way to handle a question you don't know the answer to?", "options": [{"text": "A) Make up an answer", "correct": False}, {"text": "B) Ignore the question", "correct": False}, {"text": "C) Admit you don't know but explain how you would find out", "correct": True}, {"text": "D) Change the subject", "correct": False}]},
        {"q": "Why is it important to ask questions at the end of an interview?", "options": [{"text": "A) To waste time", "correct": False}, {"text": "B) To show your interest and engagement", "correct": True}, {"text": "C) To complain about the process", "correct": False}, {"text": "D) To test the interviewer", "correct": False}]},
        {"q": "How soon should you send a thank-you email after an interview?", "options": [{"text": "A) Within 24 hours", "correct": True}, {"text": "B) After a week", "correct": False}, {"text": "C) Never", "correct": False}, {"text": "D) After a month", "correct": False}]},
        {"q": "What is an appropriate response to 'Tell me about yourself'?", "options": [{"text": "A) Your life story from childhood", "correct": False}, {"text": "B) Your hobbies and personal life", "correct": False}, {"text": "C) A brief summary of your professional background and skills", "correct": True}, {"text": "D) Your political views", "correct": False}]},
        {"q": "How should you describe your previous employer?", "options": [{"text": "A) Complain about their faults", "correct": False}, {"text": "B) Share confidential information", "correct": False}, {"text": "C) Speak respectfully and focus on what you learned", "correct": True}, {"text": "D) Refuse to talk about them", "correct": False}]},
        {"q": "What is the key to answering behavioral questions?", "options": [{"text": "A) Giving vague answers", "correct": False}, {"text": "B) Using the STAR method", "correct": True}, {"text": "C) Memorizing scripted answers", "correct": False}, {"text": "D) Focusing only on results", "correct": False}]},
        {"q": "How do you handle a salary expectation question early in the interview?", "options": [{"text": "A) Demand a specific high number", "correct": False}, {"text": "B) Refuse to answer", "correct": False}, {"text": "C) Provide a realistic range based on research", "correct": True}, {"text": "D) Say you'll take whatever they offer", "correct": False}]},
        {"q": "What does a good resume look like?", "options": [{"text": "A) 5 pages long with all details", "correct": False}, {"text": "B) Concise, error-free, and tailored to the job", "correct": True}, {"text": "C) Filled with graphics and bright colors", "correct": False}, {"text": "D) Written in a single paragraph", "correct": False}]},
        {"q": "How do you prepare for a technical interview?", "options": [{"text": "A) Wing it", "correct": False}, {"text": "B) Memorize a textbook", "correct": False}, {"text": "C) Review fundamentals, practice coding, and understand your resume projects", "correct": True}, {"text": "D) Only focus on HR questions", "correct": False}]}
    ]
}

for sec in sections:
    pools[sec].extend(new_qs[sec])

# Now generate JS strings for these pools
js_pools = ""
for sec in sections:
    js_pools += f"const {sec}Pool = {json.dumps(pools[sec], indent=4)};\n\n"

# Create the load function templates
js_functions = ""
for sec in sections:
    func_name = f"load{sec.capitalize()}Questions"
    js_functions += f"""
    function {func_name}() {{
        const tabContent = document.getElementById('{sec}');
        const listDiv = document.getElementById('{sec}-question-list');
        const resultDisplay = tabContent.querySelector('.result-display');
        
        tabContent.classList.remove('submitted');
        resultDisplay.style.display = 'none';
        tabContent.querySelector('.submit-btn').style.display = 'block';
        tabContent.querySelector('.retry-btn').style.display = 'none';

        const shuffled = [...{sec}Pool].sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, 10);
        
        listDiv.innerHTML = '';
        selected.forEach((qObj, index) => {{
            let optionsHtml = '';
            qObj.options.forEach(opt => {{
                optionsHtml += `<button class="option-btn" onclick="selectOption(this)" ${{opt.correct ? 'data-is-correct="true"' : ''}}>${{opt.text}}</button>`;
            }});

            listDiv.innerHTML += `
                <div class="question-card">
                    <div class="question-text">${{index + 1}}. ${{qObj.q}}</div>
                    <div class="options-grid">
                        ${{optionsHtml}}
                    </div>
                </div>
            `;
        }});
    }}
"""

# HTML replacement
for sec in sections:
    pattern = re.compile(rf'(<div id="{sec}" class="tab-content.*?>.*?<div class="question-list").*?(<div class="result-display")', re.DOTALL)
    replacement = rf'\1 id="{sec}-question-list">\n                    </div>\n                    \2'
    content = pattern.sub(replacement, content)

    pattern_btn = re.compile(rf'(<div id="{sec}".*?<div class="submit-section"[^>]*>)\s*<button class="btn-portal"[^>]*onclick="submitTest\(\'{sec}\'\)".*?</button>\s*</div>', re.DOTALL)
    
    # We will replace the button section with the new generic one
    def repl_btn(m):
        prefix = m.group(1)
        return prefix + f"""
                        <button class="btn-portal submit-btn" style="background: var(--primary); color: white; padding: 12px 24px; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; transition: 0.3s;" onclick="submitTest('{sec}')"><i class="fas fa-check-double"></i> Submit Test</button>
                        <button class="btn-portal retry-btn" style="display: none; background: #f59e0b; color: white; padding: 12px 24px; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; transition: 0.3s;" onclick="load{sec.capitalize()}Questions()"><i class="fas fa-sync-alt"></i> Take New Test</button>
                    </div>"""
    content = pattern_btn.sub(repl_btn, content)

# update the submitTest function
old_submit_code = """        // Handle buttons based on whether it is the quant tab
        if (tabId === 'quant') {
            tabContent.querySelector('.submit-btn').style.display = 'none';
            tabContent.querySelector('.retry-btn').style.display = 'block';
        } else {
            tabContent.querySelector('.submit-section').style.display = 'none';
        }"""
new_submit_code = """        tabContent.querySelector('.submit-btn').style.display = 'none';
        tabContent.querySelector('.retry-btn').style.display = 'block';"""
content = content.replace(old_submit_code, new_submit_code)

# Insert the pools and functions into JS
# Find the end of quantPool and insert there
quant_pool_end = content.find("function loadQuantQuestions()")
content = content[:quant_pool_end] + js_pools + js_functions + content[quant_pool_end:]

# Update DOMContentLoaded
old_init = """    document.addEventListener("DOMContentLoaded", function() {
        loadQuantQuestions();
    });"""
new_init = """    document.addEventListener("DOMContentLoaded", function() {
        loadQuantQuestions();
        loadLogicQuestions();
        loadDsaQuestions();
        loadCs_coreQuestions();
        loadHrQuestions();
    });"""
content = content.replace(old_init, new_init)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete.")
