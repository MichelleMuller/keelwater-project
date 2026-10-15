# Brainstorm (raw, verbatim)

Original notes, unedited. Kept as working material. Organised version: [brainstorm-organised.md](brainstorm-organised.md).

---

1. Quick review of the data at hand to understand the size of the problem and if we’re building the right solution for it.   
2. To do that,   
   1. I’d first want to speak to a few customers directly to hear about their pain points (or speak to their account manager or listen to gong call recordings)  
      1. What is the main problem for the customer?  
      2. Why does it take so many hours?   
      3. What is the lifecycle of the claim? From sorting to paid in all cases.   
   2. Understand what is in the support tickets (are they just complaining about sorting? About many at once which is why we’re doing the bulk?   
   3. Competitor research (what does this competitor offer, how are they positioning this in their GTM, how can we offer something on par but then also take it a step further)  
      \>\>\> for this step, I would use AI for thematic analysis across the support tickets, and potentially to analyse customer conversations and summarise the competitive research. What I would do is set this up to keep collecting data, both from customer calls and support tickets to track if sentiment changes once we start rolling this out. 

      

      

      The key things I’m trying to understand is: 

1. A clear sense of the problem  
   1. Breakdown per customer  
   2.  Keelwater customers sorted 2.1M claims in the last twelve months.  
   3. Most are sorted quickly. The median time from a claim arriving to it being sorted is 11 minutes. \> how many claims and time  
   4. Some take much longer. 15% take more than four hours. \> how many claims and time across the year  
   5. 3.4% of claims are moved to a different pile within 30 days.

      1. What’s the path? From simple to complex or the other way around?

      2. Where do they get moved to most commonly? From simple to suspicious or the other way around?

2. A clear sense of minimum the solution would require  
   1. Deterministic versus probabilistic results  
   2. Is this the same across all customers or do we need to build some type of context for the user to fill in to make this their own  
   3. Why did we build the bulk solution?  
      1. Assumption: the highest number of claims are simple and therefore having a way   
      2. The bulk solution doesn’t have any fraud detection   
   4. What skills does the agent need in order to sort through these claims  
   5. What tools does the agent need in order to sort through these claims  
   6. How do we build them so they can hand off to one another   
3. What solutions do we already have  
   1. Bulk versus prototype  
      1. What models did the prototype use? If they’re LLMs that’s a huge   
   2. Fraud check  
      1. Passes fraud check \> simple  
      2. If it doesn’t \> escalate to more research   
   3. What are the signal of fraud?  
   4. 

3. For the automation piece,  
   1. How can we easily detect the 3 categories  
      1. Sort the data  
      2. False positives  
   2. What happens next  
      1. Useful to understand the architecture   
      2. Useful to understand where the value lies (ultimately this isn’t about sorting, it’s about getting the claim paid or rejected \= resolved status)

   

The customer problem is that a lot of claims come in at once, and then get stuck. 

In the best case scenario, 

* the simple ones are automatically sorted and then routed to get paid immediately.   
* The ones that need a closer look, are flagged with suggested next steps of following up with the customer to collect more data  
* The ones that require investigation, are routed to the team for investigation

**Prioritisation-wise** 

From the brief (or collected data), I know the following: 

1. Perceived value of the automated sorting is high  
2. 15% of the claims are the hard ones to solve for the human  
3. 3.4% is a fair false positive benchmark (?)   
4. That means at \~80% of claims should be relatively easy to sort

Questions I would ask before starting: 

1. What is in the prototype? What does it consider?   
   1. Is it trained on existing data   
   2. Can I use it in customer meetings to gauge if it’s going in the right direction and get validation?   
   3. This should help me understand a few things:   
      1. If the suggested UX in the prototype makes sense  
      2. If deterministic responses are necessary \- ie an incorrect sort is not acceptable \- ie is this a good use case for LLMs to handle and I can build an agent to do this work for me  
2. Does bulk sorting solve the problem? My assumption would be that it does not and moreover, does not deliver on the perceived value.   
   1. For us to win deals and retain customers, that probably would not solve the problem  
   2. Once we have the automated flows, do we still need bulk sorting or is then obsolete as a feature? When does that become useful? This is probably most useful for the “bulk” that is simple because they don’t need close review.   
   3. 

The most useful bit that I would use AI for, is to go in and do a quick dry run of sample data based on customer data (i.e. generate a data set that I can train a model or build a skillset with). 

I would then  

Based on the above, I would suggest we pause the work of bulk sorting and instead work on sorting: 

1. Evals  
2. LLM as a judge  
3. Run it on generate sample data   
4. Run a pilot for a few with customers to get feedback

The team: 

1. First share the full deck as part of a grooming debrief (preferably async if the team can work that way). Have a session with questions \- preferably with commercial, tech and design in the room.   
2. Design: once I understand that this is worth prioritising, I would ask the design team to take a stab at building this out as part of the UX, with a clear delineation of what comes next (sorting could be relatively simple

# **Bulk Sorting: Current State and Assumptions**

* Team is halfway through building bulk sorting, due to ship in 6 weeks  
* Key assumption: no tabular view exists today, handlers sort claims one by one  
  * If a table already existed, adding multi-select would not take 12 weeks total  
  * Building bulk sorting implies an API was needed to return all claims data at once  
* Bulk sorting \= tabular format \+ filters \+ multi-select, not just a checkbox  
* Filters act as a proto-ruleset: e.g. “show me all claims with every field filled in from a returning customer”  
  * Handler scans, selects all, pushes to simple bucket  
  * These filter actions become the dataset for future automation

# **Three Claim Buckets**

* Simple: all info present, no background check needed, process immediately  
  * Example: cracked windshield, \$600, no other parties  
* Needs a closer look: complex but not suspicious, multiple parties or large payout  
  * Example: car drives through a house, \$5,000, multiple claimants  
* Suspicious: anomaly signals, e.g. 7 claims from the same person in 3 months  
* Key insight: 4+ hours to sort a claim means it is not simple  
  * Customer distribution matters: some have 99% simple claims, others are mostly complex

# **Fraud Detection Strategy**

* \$2.3M across 6 open deals, including the top renewal customer (contract up in 5 months), all citing fraud as the blocker  
  * Assumption: fraud is the primary problem to solve, not deep research  
* Two customer scenarios:  
  * Customer knows fraud signals: enumerate signals as questions, feed to a calibrated decision model (e.g. Typesafe/Jev)  
  * Customer does not know fraud signals: unsupervised learning on historical claims \+ outcomes to surface features  
    * Risk: if only name, address, and background check are available, there may not be enough correct features to produce a statistically significant model  
* Example fraud signal inputs: background check result, prior claims history, car type, location, driving history, claim frequency  
* Calibrated decision model (Typesafe/Jev) returns structured outputs only: Boolean, range (0-1 score), or categorical  
  * No training needed upfront; model evaluates against a rubric of known questions  
  * Provenance tracked per decision: which data point, which sentence, drove which output

# **Data, Privacy, and Governance**

* Assumption: claims data contains PII (personal cars, personal injury), so Keelwater does not have access by default  
  * Cannot train directly on raw customer data without redaction  
  * Customers may not be legally permitted to share PII even if willing (GDPR in EU, equivalent in US)  
  * Verify exact regulations via Claude  
* Mitigation: auto-redact PII before data hits the model or is written to durable storage  
  * Can run as a local model on customer’s machine or in Keelwater’s system, in-memory only  
  * Validate whether this already exists in the current claims pipeline  
* Governance requirements before any automation goes live:  
  * Full audit log per claim: all data used, every decision, scores, final outcome  
  * Sign-off needed from IT, governance, and likely legal teams (not just the claims team)  
  * Customers and Keelwater agree on a performance threshold before going live

# **Validation, Rollout, and AI Usage**

* Bulk sorting as validation layer: ship in 6 weeks, show prototype to customers, confirm if it solves the simple-claim problem  
  * If bulk sorting works well for simple claims, auto-sort of simple claims becomes the next step  
  * Bulk sorting also surfaces which filters customers actually use, building the training signal  
* Fraud model validation: run blind cases through the model, have customers label outcomes, measure accuracy  
  * Beta group of customers needed who will participate in labeling  
* Use AI (thematic analysis of past calls and decisions) to reconstruct why bulk sorting was originally prioritized  
  * Avoids needing fresh customer interviews for context that likely already exists  
* Rule-based systems remain valid for simple-claim flow: no ML required at that stage  
* Typesafe/Jev recommended for structured fraud scoring; worth referencing in documentation

# **Next Steps**

* **Verify PII redaction capability in current claims pipeline**Confirm whether auto-redaction exists before any claims data is passed to a model.  
* **Research GDPR and US equivalent data-sharing rules for claims data**Use Claude to confirm what customers can and cannot legally share; shapes the entire data strategy.  
* **Schedule customer sessions around the bulk sorting prototype**6-week ship window is the right moment to validate whether bulk sorting solves the simple-claim problem and probe fraud signal knowledge.  
* **Review Typesafe documentation and calibrated decision model examples**Understand structured output format (Boolean, range, categorical) to assess fit for fraud scoring.

### **AI Workflow Setup**

* Build a context hub as the foundation for all AI-assisted work  
  * Store all research, transcripts, notes, and docs in one place  
  * Notion recommended: supports MCP, auto-transcription, and easy sharing  
* Use a git repo (not just a local directory) for version control and backup  
  * Connect to Notion, SharePoint, or other stakeholder-facing tools  
  * Lets team leads and designers access docs without explicit sharing each time  
* Teams preferred over Gong for customer calls  
  * Insurance carriers are Microsoft shops, so recordings live natively in the meeting chat  
  * Download transcript (TTF/plain text) and feed directly to the agent  
  * Gong still useful for historical calls before joining the company

### **Research Plan: Internal vs. External Data**

* Internal data (faster to action):  
  * The 18-month prototype: what was built, why it stopped  
  * Existing bulk sorting work: what was validated, customers lined up  
  * Last two years of Gong recordings  
  * Usage data, support tickets, pipeline, at-risk accounts  
  * Account manager feedback on customer complaints  
* External data (slower):  
  * Direct customer interviews to validate assumptions  
* Note: Gong recordings may not have all needed answers if reps never asked the right questions  
  * State assumptions explicitly where data is missing

### **Competitive and Market Analysis**

* Ask the agent: how mature is fraud detection for insurance claims?  
  * Are carriers likely to already have fraud models?  
  * What features matter specifically for automotive claims?  
* Check Hugging Face for open-weight models or datasets relevant to the problem  
* Analyze the competitor who released automatic sorting:  
  * What features and models do they claim to use?  
  * Identify their failure points to build counter-narratives  
* Use competitor positioning to find unclaimed ground  
  * If they focus on simple cases, target fraud detection or complex claims

### **Deck Structure**

1. Data gathering: understand the current state (prototype, bulk sort, Gong, pipeline)  
2. State assumptions based on what the data shows  
3. Phase 1: Bulk sorting track  
   * Go-to-market plan, success metrics, validation approach  
   * Analytics set up pre-launch; customer review sessions via CSMs  
4. Phase 2: Automated sorting track  
   * Note-taker and tech lead work directly with customers  
   * Competitor displacement strategy  
5. Solution detail: fraud detection model approach  
   * Use a type-safe calibrated decision model (not a deterministic program)  
   * Cover auditing, explainability, and tracing for customer-facing decisions  
   * ML path: training set \+ held-out validation set; ask Claude to explain the unsupervised learning loop  
6. Post-launch: ongoing product development cycle  
   * Sorting is phase one; full claims processing is phase two  
   * Carriers care about claim outcomes (paid or flagged), not sorting itself

### **Go-to-Market and Sales Enablement**

* Once context hub is built, use Notion agents to support sales:  
  * Battle cards, sales scenarios, objection handlers, value propositions  
  * Custom decks tailored to each customer’s specific problem subset  
  * Train AEs on customer-specific material  
* Segment customers by problem distribution (simple vs. complex vs. fraud-heavy)  
  * Use distribution to sharpen positioning and prioritize which segment to own

### **Next Steps**

1. **Set up git repo and context hub in Notion**  
   1. Seed with all research, transcripts, and docs as the foundation for all AI-assisted work on this project.  
2. **Ask the agent whether Gong has an MCP**  
   1. Determines whether Gong calls can be pulled programmatically or need manual download.  
3. **Research fraud detection maturity and open datasets**  
   1. Ask Claude about carrier fraud model prevalence, key automotive features, and check Hugging Face for relevant open-weight models or datasets.  
4. **Analyze competitor's automatic sorting release**  
   1. Identify claimed features and models, then map failure points to build differentiation narrative.  
5. **Draft the deck using the agreed structure**  
   1. Cover data gathering, assumptions, two tracks (bulk sort and automated sorting), solution detail, and post-launch roadmap.

6. 

