# WHO Recommendations for AI Mental Health vs. EU AI Act High-Risk Classification
## Structured Regulatory Comparison (2026)

**Sources:**
- WHO/Delft Digital Ethics Centre pre-summit recommendations (20 March 2026)
- EU AI Act Regulation 2024/1689, Article 6 + Annex III (high-risk obligations effective 2 August 2026, medical devices delayed to 2 August 2028)

---

## 1. FRAMEWORK OVERVIEW

| Dimension | WHO Recommendations (March 2026) | EU AI Act High-Risk Classification (2026) |
|---|---|---|
| **Issuer** | WHO, facilitated by Delft Digital Ethics Centre; 30+ global specialists | European Commission / EU co-legislators |
| **Nature** | Advisory / soft-law guidance | Binding regulation with legal penalties |
| **Effective Date** | March 2026 (non-binding) | Phased: prohibited practices Feb 2025; high-risk obligations Aug 2026; medical-device AI Aug 2028 |
| **Geographic Scope** | Global (member-state adoption encouraged) | EU/EEA (extraterritorial for providers serving EU users) |
| **Target Audience** | Governments, industry, academia, health ministries | AI providers, deployers, importers, distributors operating in EU |

---

## 2. RECOMMENDATION-BY-RECOMMENDATION ANALYSIS

### WHO Rec 1: Treat all generative AI as a public mental health concern

| Aspect | WHO Position | EU AI Act Position | Alignment |
|---|---|---|---|
| **Scope** | All generative AI systems (broad, population-wide) | Only AI systems meeting specific high-risk criteria in Annex III or Annex I product-safety laws | **Partial misalignment** |
| **Rationale** | Generative AI usage, especially by youth for emotional support, is a population-level mental health determinant | Risk-based: only systems that pose significant risk to health, safety, or fundamental rights are regulated | Divergent framing |
| **Classification trigger** | Any generative AI with mental health impact (regardless of intended purpose) | Intended purpose must fall within enumerated high-risk categories (e.g., medical devices, health insurance risk assessment, employment decisions) | **Major gap** |
| **Enforcement** | Voluntary; calls for government and industry response | Mandatory conformity assessment, CE marking, EU database registration, fines up to EUR 35M or 7% global turnover | **Enforcement gap** |

**Key Gap:** WHO takes a universalist stance -- all generative AI is a mental health concern by virtue of its societal reach. The EU AI Act is purpose-specific: a general-purpose chatbot that is not *intended* for health evaluation or treatment would likely be classified as limited or minimal risk, not high-risk. This leaves a large category of general-purpose AI tools (e.g., ChatGPT used informally for emotional support) outside high-risk obligations, creating a regulatory blind spot that WHO explicitly aims to close.

---

### WHO Rec 2: Incorporate mental health metrics in AI evaluations

| Aspect | WHO Position | EU AI Act Position | Alignment |
|---|---|---|---|
| **What to measure** | Psychological well-being, long-term outcomes, emotional dependence | Accuracy, robustness, cybersecurity; risk management system; training data quality | **Partial overlap** |
| **Evaluation framework** | AI impact assessments with mental health-specific indicators | Fundamental Rights Impact Assessment (FRIA) for public-sector deployers; provider-conducted risk assessment | Overlap on process, divergence on content |
| **Longitudinal tracking** | Explicitly required ("track long-term outcomes such as emotional dependence") | Not explicitly required; obligations focus on pre-market conformity and ongoing monitoring of known risks | **Gap in temporal scope** |
| **Specificity to mental health** | Central focus; calls for dedicated metrics on attachment, dependency, crisis response | No mental-health-specific evaluation criteria; health AI evaluated under general safety/efficacy framework | **Specificity gap** |
| **Crisis referral** | Calls for consensus on "crisis referral frameworks and accountability systems" | Human oversight required but no specific mandate for crisis escalation protocols in mental health contexts | **Critical gap** |

**Key Gap:** The EU AI Act's evaluation framework is general-purpose. It requires risk management, data quality, transparency, human oversight, accuracy, and robustness -- but none of these are specifically calibrated for mental health outcomes. WHO's recommendation that evaluations track "emotional dependence" and "long-term outcomes" introduces clinical concepts (attachment, dependency, therapeutic alliance) that have no equivalent in EU AI Act conformity assessments. The EU framework would assess whether a mental health AI is technically robust; the WHO framework would assess whether it is psychologically safe over time.

---

### WHO Rec 3: Involve clinicians and people with lived experience in development

| Aspect | WHO Position | EU AI Act Position | Alignment |
|---|---|---|---|
| **Co-design requirement** | Explicit: "co-designed with mental health experts and people with lived experience" | Human oversight required, but no mandate for participatory design or lived-experience involvement | **Gap** |
| **Clinical oversight** | Mental health professionals integral to design, testing, and deployment | Human oversight = ability to intervene, override, or halt the system; does not require clinical professionals specifically | Partial alignment |
| **User involvement** | People with lived mental health experience as co-designers | No explicit requirement for user involvement in development | **Gap** |
| **Oversight model** | Clinical governance (therapeutic standards, professional accountability) | Technical governance (conformity assessment, documentation, post-market monitoring) | **Paradigm difference** |

**Key Gap:** The EU AI Act's "human oversight" (Article 14) is framed as technical operability -- a competent person must be able to understand, monitor, and override the system. WHO demands something deeper: that the system be *built with* clinicians and service users from the ground up. The EU model ensures a human can pull the plug; the WHO model ensures clinicians and patients helped design the system in the first place. This is a fundamental difference between procedural oversight and participatory governance.

---

## 3. ENFORCEMENT COMPARISON

| Enforcement Dimension | WHO Recommendations | EU AI Act |
|---|---|---|
| **Legal status** | Non-binding guidance | Binding EU regulation |
| **Penalties** | None specified | Up to EUR 35M / 7% global turnover (prohibited practices); up to EUR 15M / 3% for lesser violations |
| **Compliance mechanism** | Voluntary adoption by member states; independent investment in testing | Mandatory conformity assessment, CE marking, registration in EU database, post-market monitoring |
| **Oversight body** | Proposed: global network of academic institutions; national health ministries | National competent authorities; European AI Office; European AI Board |
| **Accountability for harm** | Calls for "accountability systems" (undefined) | Product liability, AI-specific liability provisions, potential criminal sanctions under national law |
| **Market access control** | Not addressed | Pre-market conformity assessment required; CE mark required for market entry |
| **Transparency** | Implied (through evaluation and co-design) | Explicit: users must be informed when interacting with AI; technical documentation must be available |
| **Incident reporting** | Not specified | Serious incident reporting to national authorities required |

---

## 4. CRITICAL GAPS AND MISALIGNMENTS

### Gap 1: General-purpose AI used informally for mental health
- **WHO:** Covers all generative AI regardless of intended purpose
- **EU AI Act:** Only covers AI with a *specific* high-risk intended purpose
- **Impact:** Millions of users turning to general-purpose chatbots for emotional support fall outside EU high-risk classification. This is the largest regulatory gap between the two frameworks.

### Gap 2: Long-term psychological outcomes
- **WHO:** Explicitly requires tracking emotional dependence, attachment, and longitudinal mental health effects
- **EU AI Act:** Post-market monitoring focuses on technical performance, not psychological trajectory
- **Impact:** A mental health AI could pass all EU conformity assessments while still causing slow-onset psychological dependency that neither framework currently catches.

### Gap 3: Crisis escalation and suicide prevention
- **WHO:** Calls for crisis referral frameworks
- **EU AI Act:** No specific mandate for crisis protocols; AI tools for suicide prevention/crisis detection are high-risk (triggering more scrutiny) but no specific crisis-handling standards exist
- **Impact:** An AI chatbot encountering a suicidal user has no EU-mandated minimum response standard, even though the system may be classified as high-risk.

### Gap 4: Sycophancy and clinical harm
- **WHO:** Implicitly addressed through clinical co-design (clinicians would catch sycophantic patterns)
- **EU AI Act:** No specific provision for sycophancy, hallucination in clinical contexts, or agentic misalignment in mental health
- **Impact:** Emerging research (including the ASL-MH framework) identifies sycophancy, false reassurance, and delusion reinforcement as distinct harms that neither framework specifically addresses.

### Gap 5: Vulnerability classification
- **WHO:** Treats all users of generative AI as potentially vulnerable (especially youth)
- **EU AI Act:** Recognizes psychiatric patients as vulnerable persons (elevating scrutiny) but does not extend this to general users of AI for emotional support
- **Impact:** A teenager using ChatGPT for daily emotional regulation is not protected by high-risk classification, despite WHO's recognition that such use constitutes a public mental health concern.

---

## 5. AREAS OF STRONG ALIGNMENT

| Area | How Both Frameworks Align |
|---|---|
| **Human oversight** | Both require meaningful human involvement in AI decision-making |
| **Risk-based approach** | Both recognize that AI in health contexts warrants elevated scrutiny |
| **Transparency** | Both emphasize the need for users to understand AI involvement |
| **Data quality** | Both recognize the importance of representative, high-quality training data |
| **Cross-sector governance** | Both acknowledge the need for multi-stakeholder governance (though WHO emphasizes clinicians, EU emphasizes technical compliance bodies) |
| **Recognition of health AI as sensitive** | EU classifies health AI as high-risk; WHO classifies all generative AI as a health concern -- both treat AI in health as requiring special attention |

---

## 6. SYNTHESIS: COMPLEMENTARITY VS. CONFLICT

The two frameworks are not in conflict but operate at different levels of abstraction:

- **EU AI Act** = **Hard regulatory floor** -- sets minimum legal requirements for AI systems that meet specific high-risk criteria, with enforceable penalties and market-access controls.
- **WHO Recommendations** = **Soft policy ceiling** -- articulates a broader vision of what responsible AI for mental health should look like, including clinical, social, and longitudinal dimensions that hard regulation does not yet capture.

**The EU AI Act could adopt WHO's recommendations as:**
1. Sector-specific implementing acts or delegated acts under Article 7 (amending Annex III)
2. Standards developed by CEN/CENELEC for mental health AI conformity assessment
3. Guidance from the European AI Office on interpreting "health, safety, and fundamental rights" to include psychological well-being

**WHO's recommendations could be operationalized through:**
1. National adoption of EU AI Act-style classification extended to cover general-purpose AI used for mental health
2. WHO-backed international standards for mental health AI evaluation (analogous to IEC 62304 for medical device software)
3. The proposed global network of academic institutions serving as independent testing bodies

---

## 7. SUMMARY MATRIX

| WHO Recommendation | EU AI Act Coverage | Alignment Level | Primary Gap |
|---|---|---|---|
| **Rec 1:** All generative AI = mental health concern | Limited to intended-purpose high-risk systems | LOW | General-purpose AI for emotional support falls outside EU scope |
| **Rec 2:** Mental health metrics in evaluations | General safety/robustness metrics; no mental-health-specific criteria | MEDIUM | No longitudinal psychological outcome tracking; no dependency metrics |
| **Rec 3:** Clinician + user co-design | Human oversight (technical); no participatory design mandate | LOW-MEDIUM | Procedural oversight vs. participatory governance |

---

*Analysis compiled from WHO pre-summit guidance (March 2026), EU AI Act Articles 6-14 and Annex III, European Commission guidance on high-risk classification (May-June 2026), and the ASL-MH framework for AI safety in mental health.*
