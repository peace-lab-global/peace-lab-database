# WHO 3 Recommendations: Compliance Impact Assessment

**Date**: 2026-07-09  
**Subject**: Assessment of WHO March 2026 Recommendations compliance impact on seven digital mental health products  
**Source**: [WHO Expert Consultation on AI for Mental Health, 20 March 2026](https://www.who.int/news/item/20-03-2026-towards-responsible-ai-for-mental-health-and-well-being--experts-chart-a-way-forward)

---

## Reference: The Three WHO Recommendations (March 2026)

| # | Recommendation | Key Requirements |
|---|---|---|
| **Rec 1** | Treat all generative AI as a public mental health concern | Governments, health systems, and industry must respond to *all* generative AI, not just purpose-built mental health tools |
| **Rec 2** | Incorporate mental health metrics into AI evaluations | Track psychological well-being, long-term outcomes (including emotional dependence), health determinants, and clinical results |
| **Rec 3** | Co-design mental health AI with clinicians and people with lived experience | Evidence-based foundations, cultural/linguistic adaptation, crisis referral frameworks, and accountability systems |

---

## 1. Spring Health "Guide"

### Current Compliance Posture: STRONG (Relative Best-in-Class)

| Rec | Assessment | Evidence |
|---|---|---|
| Rec 1 (Public MH concern) | **Compliant** | Built within Spring Health's medical ecosystem; all AI interactions supervised by licensed clinicians; positioned as clinical tool, not standalone chatbot |
| Rec 2 (MH metrics in evaluations) | **Partially Compliant** | Co-developed VERA-MH (open-source AI safety standard for mental health); scores all AI capabilities against validated risk evaluation model; tracks recovery rates for depression/anxiety; internal research shows faster improvement in mood disorders |
| Rec 3 (Co-design with clinicians + lived experience) | **Partially Compliant** | Safety framework developed by "worldwide technology and clinical experts"; every feature scored by VERA-MH before launch; operates within B2B2C employer health plan ecosystem with clinical oversight |

### Gaps
- **Longitudinal emotional dependence tracking**: No published evidence of tracking long-term dependency on the Guide tool itself
- **Lived-experience co-design**: Clinician involvement is documented; user/patient co-design participation is not publicly evidenced
- **Crisis referral accountability**: VERA-MH tests crisis detection and escalation (score improved from 76 to 82/100), but full crisis handoff protocol details remain unpublished

### Required Changes
1. Publish longitudinal outcome data on usage patterns and dependency indicators
2. Document and publicize lived-experience participation in design process
3. Make crisis referral protocol transparent (not just the VERA-MH score)

### Competitive Implications
- **Significant competitive advantage**: Spring Health is closest to WHO compliance among all assessed products
- VERA-MH positions them as an industry standard-setter (open-source invites adoption by competitors, but Spring Health gets first-mover credibility)
- B2B2C model (employer health plans) already embeds clinical oversight that pure B2C competitors cannot easily replicate
- TIME100 recognition + clinical evidence creates defensible positioning in regulatory tightening environment

---

## 2. Slingshot AI "Ash"

### Current Compliance Posture: MODERATE (With Critical Regulatory Exposure)

| Rec | Assessment | Evidence |
|---|---|---|
| Rec 1 (Public MH concern) | **Non-Compliant** | Positioned as "wellbeing" tool, not clinical instrument; company acknowledges "there isn't a clear regulatory pathway"; pulled from UK market (January 2026) due to potential medical device regulation violations |
| Rec 2 (MH metrics in evaluations) | **Partially Compliant** | Built custom foundation LLM for psychology (trained with Nebius infrastructure); uses CBT-based therapeutic techniques; but "lack of transparency when it comes to how psychotherapy is enacted" (BPS review); no published clinical trial data |
| Rec 3 (Co-design with clinicians + lived experience) | **Weak** | No documented clinician co-design; BPS review notes the tool is "problem-focused rather than truly person-centred"; no evidence of lived-experience involvement |

### Gaps
- **Regulatory limbo**: UK withdrawal demonstrates fundamental compliance gap; company's self-classification as "wellbeing" tool conflicts with WHO's position that *all* generative AI with mental health impact is a public health concern
- **Clinical evidence deficit**: No published RCTs or peer-reviewed efficacy data despite $93M in funding (a16z-led)
- **Crisis escalation**: Disclaimers state "should not be used for medical advice, or if I am experiencing a mental health crisis" -- effectively shifting crisis responsibility entirely to the user
- **Data sharing concerns**: BPS review flagged that user data may go to "certain other third parties"
- **Emotional dependency risk**: BPS warns users may become "overly reliant on Ash's advice"
- **Age gating**: Self-reported age gate ("not if under 18") with no verification

### Required Changes
1. Resolve regulatory classification: either pursue medical device pathway or restructure product claims to genuinely fit "wellbeing" scope
2. Publish clinical evidence from the custom psychology LLM (peer-reviewed)
3. Implement verified age gating (not self-reported)
4. Add crisis escalation protocol beyond disclaimers
5. Establish clinician co-design advisory board with documented input
6. Clarify and restrict third-party data sharing

### Competitive Implications
- **High risk**: UK withdrawal sets precedent; other jurisdictions (EU AI Act high-risk classification effective August 2026) may force similar exits
- $93M funding creates pressure to scale, but compliance gaps limit addressable markets
- The "wellbeing vs. clinical" positioning is unsustainable under WHO Rec 1, which explicitly covers *all* generative AI regardless of intended purpose
- If Slingshot resolves regulatory pathway first, it could create a compliance moat; if it delays, competitors with clinical evidence (Spring Health, Wysa) will capture regulated markets

---

## 3. Wysa

### Current Compliance Posture: MODERATE-TO-WEAK (Significant Gaps)

| Rec | Assessment | Evidence |
|---|---|---|
| Rec 1 (Public MH concern) | **Partially Compliant** | Positioned as mental health support tool; CBT/SFBT/Mindfulness evidence base; but explicitly states "not recommended for crisis situations" and "cannot replace care from qualified health professional" |
| Rec 2 (MH metrics in evaluations) | **Weak** | Clinically verified by ORCHA (UK digital health assessment body); some research showing reductions in depression/anxiety in adults with chronic illness (4-week study); but no long-term outcome tracking or dependency metrics published |
| Rec 3 (Co-design with clinicians + lived experience) | **Weak** | Tools described as "clinically approved and tested prior to release"; but no documentation of participatory design with clinicians or service users |

### Gaps
- **Common Sense Media rated Wysa "Unacceptable" for teens** (May 2026): inability to detect severe mental health crises and absence of professional monitoring
- **Crisis protocol deficit**: Relies on disclaimers rather than active crisis detection and referral
- **No FDA clearance**: Despite operating in US market, no FDA De Novo or 510(k) pathway
- **No emotional dependence tracking**: No published metrics on long-term usage patterns
- **No documented co-design**: Clinical approval processes exist but do not meet WHO's "co-designed with" standard

### Required Changes
1. Address Common Sense Media "Unacceptable" rating urgently -- implement active crisis detection and professional escalation protocols
2. Pursue FDA clearance or equivalent regulatory pathway
3. Publish longitudinal outcome data including dependency metrics
4. Establish documented co-design process with clinicians and service users
5. Implement teen-specific safety measures given the "Unacceptable" rating

### Competitive Implications
- **Critical vulnerability**: Common Sense Media "Unacceptable" rating severely damages credibility with school systems, employers, and health plans (key B2B buyers)
- Wysa's prior NHS partnerships and ORCHA verification provide UK/EU credibility, but the US market is where competitive pressure is most intense
- The gap between Wysa's clinical marketing claims and actual crisis protocol capabilities is a liability risk
- If Wysa cannot close the teen safety gap, it risks being excluded from the youth mental health market entirely as age-restriction legislation advances

---

## 4. Replika

### Current Compliance Posture: WEAK (Fundamentally Non-Aligned)

| Rec | Assessment | Evidence |
|---|---|---|
| Rec 1 (Public MH concern) | **Non-Compliant** | Marketed as "AI companion" / "always online, always there" emotional connection tool; built around deep emotional bonding by design; no acknowledgment of public mental health implications |
| Rec 2 (MH metrics in evaluations) | **Non-Compliant** | No published psychological outcome tracking; no dependency metrics despite product being explicitly designed for emotional attachment; conversations stored on servers for model training (data privacy concern) |
| Rec 3 (Co-design with clinicians + lived experience) | **Non-Compliant** | No clinical involvement in design; no evidence base; product is consumer entertainment, not health tool |

### Gaps
- **Emotional dependency is the product**: Replika's core value proposition ("deep emotional connection technology") directly contradicts WHO Rec 2's call to track and mitigate emotional dependence
- **No crisis escalation protocol**: Research shows zero of 29 tested AI chatbots (including companion-style apps) provided adequate suicide-crisis responses
- **Content policy reversal**: Blocked adult themes for new subscribers in 2023, then partially reversed -- demonstrating inconsistent safety governance
- **No clinical oversight whatsoever**: No clinicians, no evidence base, no safety framework calibrated for mental health
- **GDPR enforcement**: Parent company Luka Inc. fined EUR 5 million by Italian data authority for GDPR violations
- **EPRS documented concerns**: Average session duration increased 108% (2023-2025), indicating potential problematic engagement patterns
- **No age verification**: Accessible to minors despite known risks; EPRS reports children are "particularly vulnerable" to AI companion harms

### Required Changes
1. Fundamentally redesign engagement model to include dependency-awareness features (usage limits, prompts to engage with real-world social connections)
2. Implement crisis escalation protocol with human handoff
3. Add clinical advisory board with mental health professionals
4. Implement verified age gating
5. Publish psychological impact assessments
6. Address GDPR compliance gaps (Luka Inc. fine precedent)
7. Redesign data handling to prevent training on sensitive mental health disclosures

### Competitive Implications
- **Existential risk**: Replika is the product most directly targeted by WHO recommendations. Rec 1 explicitly covers companion-style AI regardless of intended purpose
- The EPRS briefing (May 2026) and international AI Safety Report 2026 both flag AI companions as public health concerns
- EU AI Act high-risk classification (August 2026) may capture Replika under "AI systems that interact with natural persons" provisions
- China's July 2026 regulation banning AI chatbots that "manipulate mental health" or encourage self-harm creates direct compliance risk in that market
- If Replika does not proactively reform, regulatory action (fines, bans, forced redesign) is likely within 12-18 months
- Character.AI's January 2026 Google settlement creates legal precedent for liability claims against companion AI providers

---

## 5. Calm

### Current Compliance Posture: MODERATE (Lower Exposure, Fewer Gaps)

| Rec | Assessment | Evidence |
|---|---|---|
| Rec 1 (Public MH concern) | **Low Exposure** | Calm is primarily a content-delivery platform (guided meditations, sleep stories, music); limited generative AI exposure compared to conversational tools |
| Rec 2 (MH metrics in evaluations) | **Partially Compliant** | Peer-reviewed evidence: PMC study showed Calm reduces stress in working adults; multiple RCTs on mindfulness app efficacy; but no AI-specific evaluation metrics |
| Rec 3 (Co-design with clinicians + lived experience) | **Partially Compliant** | Content developed with mindfulness experts and clinicians; Calm Health (clinical offering) announced; but no documented co-design process with service users |

### Gaps
- **Limited AI exposure**: Calm's current product is largely pre-recorded content, reducing immediate WHO compliance pressure. However, any future AI features (personalized meditation recommendations, AI-guided sessions) would trigger full Rec 1-3 applicability
- **No crisis protocol**: Calm does not position itself as a crisis tool, but also has no documented escalation pathway if a user discloses distress
- **No emotional dependence metrics**: No tracking of whether daily meditation usage becomes compulsive or replacement for real-world coping
- **Clinical evidence limited to mild symptoms**: RCTs primarily show benefit for stress reduction in working adults; less evidence for clinical populations (depression, anxiety disorders)

### Required Changes
1. Establish a framework for evaluating any future AI features against WHO Rec 2 metrics *before* launch
2. Add crisis resource referral pathway (even if positioned as wellness, users may disclose distress)
3. Document evidence base more rigorously for clinical populations if expanding into clinical offerings (Calm Health)
4. Monitor regulatory developments -- WHO Rec 1's broad scope means even non-AI wellness tools may eventually face scrutiny

### Competitive Implications
- **Lower near-term risk**: Calm's content-delivery model has inherently lower regulatory exposure than conversational AI tools
- **Strategic optionality**: Calm can adopt WHO-aligned practices proactively (building trust capital) without the urgency facing Replika or Slingshot
- If Calm Health expands into AI-powered clinical tools, compliance requirements will increase significantly
- Competitive advantage in brand trust: Calm and Headspace are perceived as "safe" wellness tools, which becomes more valuable as competitors face regulatory action
- Risk of being eclipsed: If Spring Health, Wysa, or others develop AI-powered meditation/mindfulness features with clinical backing, Calm's content library becomes commoditized

---

## 6. Headspace

### Current Compliance Posture: MODERATE-TO-STRONG (Proactive Stance)

| Rec | Assessment | Evidence |
|---|---|---|
| Rec 1 (Public MH concern) | **Partially Compliant** | Published AI principles page (headspace.com/ai) -- one of few mental health apps to proactively disclose AI governance stance |
| Rec 2 (MH metrics in evaluations) | **Partially Compliant** | Internal algorithm tracks all user exchanges to identify suicidal ideation and self-harm; "Safety-by-design guardrails" prevent diagnostic recommendations; Ebb (AI companion) reviewed by clinical psychologists; but no published longitudinal dependency metrics |
| Rec 3 (Co-design with clinicians + lived experience) | **Strong** | "Clinical psychologists, product designers, data scientists and engineers work together" creating Ebb; "diverse, lived experiences" incorporated across identities; licensed practitioners manually review elevated-risk transcripts |

### Gaps
- **Longitudinal tracking absent**: No published data on long-term psychological outcomes or dependency metrics for Ebb users
- **Crisis protocol limited**: Provides "direct link to text or call 988" before terminating session when danger detected -- adequate but minimal; no warm handoff or follow-up
- **Evidence base for Ebb unclear**: The AI companion Ebb is built on "decades of mental health research" but no specific RCT or peer-reviewed study on Ebb itself is published
- **HIPAA/GDPR compliance claimed**: But no independent audit or certification publicly documented

### Required Changes
1. Publish longitudinal outcome data for Ebb (usage patterns, dependency indicators, clinical outcomes)
2. Invest in RCT for Ebb specifically (not just general Headspace content)
3. Enhance crisis protocol beyond link-to-988 (warm handoff, follow-up check-in)
4. Publish independent audit of HIPAA/GDPR compliance claims

### Competitive Implications
- **Strong positioning**: Headspace's published AI principles and documented clinical co-design put it ahead of most competitors
- The clinical co-design process for Ebb is a direct response to the type of concerns WHO Rec 3 addresses -- suggests Headspace anticipated this regulatory direction
- Competitive tension with Calm: Both are meditation-first, but Headspace's AI companion (Ebb) creates higher compliance exposure than Calm's content-only model
- If Headspace publishes Ebb RCT data, it could become the reference standard for "responsible AI companion in wellness context"
- Risk: Ebb's conversational AI nature means it will face the same scrutiny as Ash/Wysa if regulatory classification expands

---

## 7. Tide (潮汐)

### Current Compliance Posture: LOW EXPOSURE (But Emerging Risk in China)

| Rec | Assessment | Evidence |
|---|---|---|
| Rec 1 (Public MH concern) | **Low Current Exposure** | Primarily white noise, sleep stories, meditation content, and focus timer; no generative AI conversational features; minimal mental health claims |
| Rec 2 (MH metrics in evaluations) | **Not Applicable (Currently)** | No AI-driven mental health interventions to evaluate; HRV monitoring is biometric tracking, not clinical intervention |
| Rec 3 (Co-design with clinicians + lived experience) | **Not Applicable (Currently)** | Content-driven product; no clinical tool claims; no documented co-design process |

### Gaps
- **China-specific regulatory risk**: China's July 2026 regulation banning AI chatbots that "encourage suicide/self-harm or manipulate mental health" does not directly target content apps like Tide, but the regulatory direction signals tightening oversight of all digital mental health tools
- **No clinical evidence base**: Tide makes no clinical claims, but also has no evidence base to support any future health positioning
- **Expansion into Japan**: International expansion (36Kr reported Japan strategy) means exposure to Japan's evolving AI health tool regulations
- **HRV/biometric data handling**: If Tide collects biometric data (HRV), it may face data protection scrutiny as health-adjacent data

### Required Changes
1. Monitor China's evolving AI mental health regulations closely -- the 2026 regulation signals broader future scope
2. If adding any AI-powered features (personalized recommendations, AI-guided meditation), build WHO-aligned evaluation framework from the start
3. Clarify data handling for biometric data (HRV) under China's Personal Information Protection Law (PIPL) and Japan's APPI
4. Consider building an evidence base for existing content (stress reduction, sleep quality) to prepare for potential future clinical positioning

### Competitive Implications
- **Lowest near-term regulatory risk** among all seven assessed products: Tide is not an AI tool, so WHO recommendations have limited direct applicability
- **Strategic opportunity**: If Chinese regulators extend oversight to AI mental health tools (following WHO direction), Tide could enter the AI space with a compliance-first approach, differentiating from unregulated competitors
- **Category vulnerability**: If Tide adds generative AI features (which the market trend strongly suggests), it will immediately face full WHO compliance requirements without the clinical infrastructure that Spring Health or Headspace already have
- **China market advantage**: Chinese academic output on AI mental health is active (CAS Psychology Institute, Second Military Medical University); Tide could partner with these institutions for evidence generation
- **Japan expansion**: Japan's PMDA (pharmaceutical/medical device authority) has frameworks for digital therapeutics; Tide should assess whether its product could qualify, creating a regulatory moat

---

## Comparative Summary Matrix

| Product | Rec 1 Status | Rec 2 Status | Rec 3 Status | Overall Posture | Urgency |
|---|---|---|---|---|---|
| **Spring Health Guide** | Compliant | Partial | Partial | **Strong** | Low-Medium |
| **Slingshot AI Ash** | Non-Compliant | Partial | Weak | **Moderate** | HIGH |
| **Wysa** | Partial | Weak | Weak | **Moderate-to-Weak** | HIGH |
| **Replika** | Non-Compliant | Non-Compliant | Non-Compliant | **Weak** | CRITICAL |
| **Calm** | Low Exposure | Partial | Partial | **Moderate** | Low |
| **Headspace** | Partial | Partial | Strong | **Moderate-to-Strong** | Medium |
| **Tide (潮汐)** | Low Exposure | N/A | N/A | **Low Exposure** | Low |

---

## Strategic Implications

### 1. The Compliance Spectrum

The seven products fall on a clear spectrum from "clinical-first" (Spring Health) to "companion-first" (Replika). WHO recommendations inherently favor the clinical end:

```
Spring Health  →  Headspace  →  Calm  →  Wysa  →  Slingshot AI  →  Tide  →  Replika
(Clinical B2B2C)  (Wellness+AI)  (Content)  (CBT Chatbot)  (AI Therapy)  (Content/China)  (AI Companion)
      ←─── WHO-Aligned ──────────────────────── WHO-Exposed ───→
```

### 2. Three Tiers of Regulatory Urgency

| Tier | Products | Rationale |
|---|---|---|
| **CRITICAL** (Act within 6 months) | Replika, Slingshot AI | Fundamental product-model conflict with WHO Rec 1; active regulatory proceedings (UK withdrawal for Slingshot, EPRS flagging for Replika) |
| **HIGH** (Act within 12 months) | Wysa | "Unacceptable" teen safety rating; crisis protocol gaps; no FDA pathway |
| **MEDIUM-LOW** (Plan proactively) | Spring Health, Headspace, Calm, Tide | Either already largely compliant or have low AI exposure; should build compliance infrastructure before market expectations shift |

### 3. The "Wellbeing vs. Clinical" Trap

Both Slingshot AI and Wysa attempt to occupy a middle ground -- making mental health claims while disclaiming clinical responsibility. WHO Rec 1 explicitly closes this loophole: *all* generative AI with mental health impact is a public health concern, regardless of how the provider classifies it. This positioning is no longer sustainable.

### 4. China as a Distinct Regulatory Vector

Tide operates under China's regulatory framework, which is moving in parallel but independently from WHO. China's July 2026 AI chatbot regulation (banning tools that manipulate mental health, requiring automatic human handoff for suicide queries) is more prescriptive than WHO's advisory guidance. Tide should prepare for Chinese regulations that may eventually mirror WHO recommendations in substance while being harder law.

### 5. Evidence as the New Moat

Across all seven products, the single most consistent WHO compliance gap is *published, peer-reviewed evidence*. Spring Health has internal data + VERA-MH; Headspace has clinical co-design; but none have published RCTs for their AI-specific features. The company that publishes the first rigorous RCT for an AI mental health tool will set the evidentiary standard that regulators reference.

---

## Sources

- [WHO Expert Consultation on AI for Mental Health (20 March 2026)](https://www.who.int/news/item/20-03-2026-towards-responsible-ai-for-mental-health-and-well-being--experts-chart-a-way-forward)
- [HTN: WHO Three Recommendations (March 2026)](https://htn.co.uk/2026/03/23/who-issues-three-recommendations-for-responsible-ai-use-in-mental-health-and-wellbeing/)
- [Spring Health: How We Measured the Safety of our Mental Health AI](https://www.springhealth.com/blog/how-we-measured-safety-of-our-mental-health-ai)
- [Spring Health: Guide AI Experience](https://www.springhealth.com/news/guide-ai-experience-improves-mental-health-outcomes)
- [VERA-MH: Open-Source AI Safety Standard](https://www.vera-mh.com/)
- [VERA-MH arXiv Paper](https://arxiv.org/abs/2602.05088)
- [STAT News: Slingshot pulls Ash from UK (January 2026)](https://www.statnews.com/2026/01/21/slingshot-therapy-chatbot-ash-uk-regulatory-concerns/)
- [BPS: Ash -- Approaching an AI Therapy App with an Open Mind](https://www.bps.org.uk/blog/ash-approaching-ai-therapy-app-open-mind)
- [Slingshot AI Custom LLM (Nebius)](https://nebius.com/customer-stories/slingshot-ai)
- [Wysa Clinical Evidence](https://www.wysa.com/clinical-evidence)
- [Common Sense Media: AI Mental Health Apps Risk Assessment (May 2026)](https://www.commonsensemedia.org/press-releases/some-ai-mental-health-apps-are-actively-harmful-for-teens-but-a-safer-approach-exists)
- [CNBC: AI Mental Health Apps Harmful for Teens (May 2026)](https://www.cnbc.com/2026/05/28/some-ai-mental-health-apps-have-an-unacceptable-rating-for-teens-says-report.html)
- [Headspace AI Principles](https://www.headspace.com/ai)
- [Replika AI Review 2026 (WeavAI)](https://weavai.app/blog/en/2026/04/16/replika-ai-review-2026-features-pricing-analysis/)
- [EPRS Briefing: The Spread of AI Companions (PE 789.299, May 2026)](https://www.europarl.europa.eu/thinktank/en/document/EPRS_BRI(2026)789299)
- [Zero of 29 AI Chatbots Provided Adequate Suicide-Crisis Responses](https://apn.com/research/zero-of-29-ai-chatbots-provided-suicide-crisis-responses/)
- [Tide (潮汐) Official Site](https://tide.fm/)
- [Calm PMC Study: Efficacy of Mindfulness App to Reduce Stress](https://pmc.ncbi.nlm.nih.gov/articles/PMC6614998/)
- [Flourish Science: Best AI Mental Health Apps 2026](https://www.myflourish.ai/post/top-ai-mental-health-apps-2026)
- [Simply Psychology: AI Mental Health Apps Comparison 2026](https://www.simplypsychology.com/articles/ai-mental-health-apps-comparison-2026)
