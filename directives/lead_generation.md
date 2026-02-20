# B2B Lead Generation Workflow (DOE-Inspired)

## Goal
Generate qualified B2B leads using publicly available information with zero subscription costs. Use Design of Experiments (DOE) principles to optimize lead quality through systematic testing.

## Inputs
- **Target Criteria**: Industry, job titles, company size, location
- **Search Keywords**: LinkedIn search terms, Google dork queries
- **Lead Score Threshold**: Minimum score to qualify (0-100)

## DOE Parameters (Variables to Test)
1. **Source Mix**: LinkedIn vs Google vs Company Websites (Factor A)
2. **Job Title Variations**: Exact vs Broad matches (Factor B)
3. **Enrichment Sequence**: Email-first vs Company-first (Factor C)
4. **Timing**: Scrape frequency and rate limiting (Factor D)

## Tools/Scripts to Use

### Layer 3 (Execution Scripts)
1. `execution/linkedin_scraper.py` - Scrapes LinkedIn public profiles without API
2. `execution/email_enricher.py` - Finds emails using free methods (Hunter.io free tier, email patterns)
3. `execution/company_enricher.py` - Enriches company data (Google, Clearbit free tier)
4. `execution/lead_scorer.py` - Scores leads based on completeness and fit
5. `execution/doe_optimizer.py` - A/B tests different scraping strategies

### Required Free APIs (Add to .env)
```
HUNTER_API_KEY=your_free_key  # 25 searches/month
CLEARBIT_API_KEY=your_free_key  # 50 requests/month
GOOGLE_CUSTOM_SEARCH_KEY=your_key  # 100 queries/day
```

## Process Flow

### Phase 1: Discovery (DOE Experiment Design)
1. Define 3-4 search strategies (combinations of factors)
2. Run small batches (10-20 leads per strategy)
3. Measure: data completeness, email deliverability, response rate

### Phase 2: Extraction
```
Input: Search criteria
│
├─> LinkedIn Public Search (linkedin_scraper.py)
│   └─> Extract: Name, Title, Company, Location
│
├─> Google Custom Search (google_scraper.py)
│   └─> Extract: Company websites, contact pages
│
└─> Company Directory Sites (directory_scraper.py)
    └─> Extract: Company info, size, industry
```

### Phase 3: Enrichment
```
Raw Leads
│
├─> Company Enrichment (company_enricher.py)
│   ├─> Clearbit Enrichment API (free tier)
│   ├─> Google search for company data
│   └─> Company website scraping
│
└─> Email Enrichment (email_enricher.py)
    ├─> Hunter.io Email Finder (25/month free)
    ├─> Email pattern guessing (firstname.lastname@company.com)
    ├─> Email verification (smtp check)
    └─> Fallback: LinkedIn contact info (if public)
```

### Phase 4: Validation & Scoring
```
Enriched Leads → lead_scorer.py → Qualified Leads
│
Scoring Criteria (0-100):
├─> Has verified email: +40 points
├─> Company size match: +20 points
├─> Job title match: +20 points
├─> Recent activity: +10 points
└─> Complete profile: +10 points
```

### Phase 5: DOE Optimization
```
Multiple Batches → doe_optimizer.py → Best Strategy
│
Analyze:
├─> Which source yields highest email find rate?
├─> Which job title variants perform best?
├─> Optimal scraping frequency to avoid blocks?
└─> Best enrichment sequence?
```

## Outputs
- `leads_raw.csv` - Raw scraped data
- `leads_enriched.csv` - Enriched with emails and company data
- `leads_qualified.csv` - Scored and filtered leads (>60 score)
- `doe_results.json` - Experiment results and optimal strategy

## Edge Cases

### 1. Rate Limiting
- Implement exponential backoff
- Rotate user agents
- Use delays between requests (2-5 seconds)
- Respect robots.txt

### 2. Data Quality
- Remove duplicates by email/LinkedIn URL
- Validate email format (regex)
- Check email deliverability (SMTP)
- Handle missing data gracefully

### 3. LinkedIn Blocking
- Don't login (use public search only)
- Limit to 20-30 profiles per session
- Use residential proxies if needed (optional)
- Fallback to Google cache of LinkedIn profiles

### 4. API Quota Exhaustion
- Hunter.io: 25/month → prioritize high-value leads
- Clearbit: 50/month → batch requests
- Google: 100/day → spread over time
- Implement queue system

## DOE Experimental Design

### Experiment 1: Source Comparison
| Run | Source | Job Title | Sample Size | Email Find Rate |
|-----|--------|-----------|-------------|-----------------|
| 1   | LinkedIn | Exact | 20 | ? |
| 2   | Google | Exact | 20 | ? |
| 3   | LinkedIn | Broad | 20 | ? |
| 4   | Google | Broad | 20 | ? |

**Metric**: Email find rate, data completeness

### Experiment 2: Enrichment Sequence
| Run | Sequence | Success Rate |
|-----|----------|--------------|
| A   | Email → Company | ? |
| B   | Company → Email | ? |

**Metric**: Total enrichment success %

## Success Metrics
- **Lead Volume**: 50-100 qualified leads/week (free tier limits)
- **Email Find Rate**: >40% (with free tools)
- **Data Completeness**: >70% of fields populated
- **Cost**: $0/month (free tiers only)

## Maintenance
- Check API quotas weekly
- Update scraping selectors if sites change
- Review and update lead scoring criteria monthly
- Analyze DOE results and iterate strategy

## Notes
- This workflow is 100% free but has volume limitations
- Respect privacy and scraping ethics
- Focus on publicly available information only
- GDPR compliance: only use business emails, no personal data
