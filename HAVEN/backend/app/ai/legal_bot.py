"""HAVEN Legal Knowledge Base.

Encodes the spec's `legal_kb.json`: Indian women's rights acts, the FIR process,
property/custody rights, and national legal-aid resources. This is served to the
legal bot for retrieval-augmented answers and is also exposed via the
knowledge-base lookup used by the legal router.
"""

LEGAL_KNOWLEDGE_BASE = {
    "acts": [
        {
            "id": "dowry_prohibition_1961",
            "name": "Dowry Prohibition Act, 1961",
            "keywords": ["dowry", "streedhan", "stridhan", "gift", "bride price"],
            "key_points": [
                "Giving, taking or demanding dowry is a punishable offence.",
                "Streedhan (gifts given to the woman) remains the woman's property; "
                "Misuse of a spouse's streedhan can be a criminal offence.",
                "A woman can (also) file under this Act independently of a divorce case.",
            ],
            "sections": [3, 4, 5],
            "penalties": "Imprisonment up to 5 years and a fine (for demanding dowry).",
            "how_to_file": "File a complaint with the local police or the district "
                           "women's cell / National Commission for Women.",
        },
        {
            "id": "protection_dv_2005",
            "name": "Protection of Women from Domestic Violence Act, 2005",
            "keywords": ["domestic", "violence", "abuse", "husband", "family", "498a"],
            "key_points": [
                "Applies to married and unmarried women living in a domestic "
                "relationship (including live-in).",
                "Covers physical, sexual, verbal, emotional and economic abuse, "
                "and dowry-related harassment.",
                "A woman can obtain protection orders, residence orders, monetary "
                "relief and custody orders.",
                "Can be filed by the woman, or by any person on her behalf, "
                "including a Protection Officer or a service provider.",
            ],
            "sections": ["498A", "406", "420"],
            "penalties": "Breach of a protection order can lead to imprisonment "
                         "up to 1 year (IPC 188 / Act provisions).",
            "how_to_file": "Approach the Protection Officer or the nearest police "
                           "station, or file directly in the Magistrate's court.",
        },
        {
            "id": "posh_2013",
            "name": "Sexual Harassment of Women at Workplace Act, 2013 (POSH)",
            "keywords": ["workplace", "office", "harassment", "colleague", "boss",
                         "work", "posh"],
            "key_points": [
                "Prohibits sexual harassment of women at the workplace.",
                "Employers with 10+ employees must constitute an Internal "
                "Complaints Committee (ICC).",
                "Covers physical contact, advances, requests for sexual favours, "
                "verbal/non-verbal conduct of sexual nature.",
                "A woman can file an internal complaint or approach the Local "
                "Committee if no ICC exists.",
            ],
            "sections": [],
            "penalties": "Employer penalties for non-compliance; workplace action "
                         "against the harasser plus potential criminal/IPC action.",
            "how_to_file": "File a written complaint with the Internal Complaints "
                           "Committee within 3 months of the incident.",
        },
        {
            "id": "ipc_women_safety",
            "name": "Indian Penal Code — provisions on women's safety",
            "keywords": ["ipc", "molestation", "eve teasing", "outraging modesty",
                         "assault", "sexual", "rape", "354", "355", "375"],
            "key_points": [
                "Section 354: Assault or use of criminal force to outrage a woman's "
                "modesty — imprisonment up to 2+ years.",
                "Section 354A: Sexual harassment — up to 3 years.",
                "Section 375: Rape — imprisonment for a minimum of 10 years, "
                "extending to life imprisonment.",
                "Section 509: Word, gesture or act intended to insult the modesty "
                "of a woman.",
            ],
            "sections": ["354", "354A", "355", "375", "509", "498A"],
            "penalties": "See individual IPC sections; penalties include "
                         "imprisonment from 2 years to life.",
            "how_to_file": "Lodge an FIR at the police station of the area where "
                           "the incident occurred. Zero FIR can be filed at any station.",
        },
        {
            "id": "hindu_succession_1956",
            "name": "Hindu Succession Act, 1956 (property & inheritance)",
            "keywords": ["property", "inheritance", "widow", "daughters", "succession",
                         "house", "land", "ancestral"],
            "key_points": [
                "Daughters have equal coparcenary rights in ancestral property "
                "(amended 2005).",
                "A widow has an inheritable interest in her deceased husband's "
                "property.",
                "Equal rights for daughters and sons in their parents' "
                "self-acquired property in the absence of a valid will.",
            ],
            "sections": [6, 8, 14, 15],
            "penalties": "Civil remedy; rights can be enforced through a civil suit.",
            "how_to_file": "Consult a family lawyer; claims can be raised in civil "
                           "court or through a partition suit.",
        },
    ],
    "procedures": [
        {
            "id": "file_fir",
            "title": "How to file an FIR",
            "keywords": ["fir", "complaint", "police", "report", "register",
                         "file a case"],
            "steps": [
                "Go to the nearest police station and ask to register an FIR.",
                "State that you want an FIR to be registered; describe the incident "
                "clearly (dates, places, people involved).",
                "You have the right to get a free copy of the FIR.",
                "If the police refuse, file a Zero FIR at any station or "
                "approach a Magistrate / the Superintendent of Police (under "
                "Section 154 / 156 CrPC) or the National Commission for Women.",
                "Keep a copy safe; consider legal aid (free legal aid is a "
                "fundamental right under Article 39A).",
            ],
        },
        {
            "id": "protection_order",
            "title": "Protection & residence orders under the DV Act, 2005",
            "keywords": ["protection order", "restraining", "stay away", "residence",
                         "eviction"],
            "steps": [
                "File an application before the Magistrate under the DV Act, 2005.",
                "The court can pass a protection order (restrain the respondent "
                "from approaching or contacting you).",
                "A residence order can stop the respondent from entering the shared "
                "household and can direct alternate accommodation.",
                "A violation of a protection order is punishable by imprisonment.",
            ],
        },
        # __PROC__
    ],
    "rights": [
        {
            "category": "property_rights",
            "rights": [
                "Streedhan (dowry/gifts given to the woman) belongs to the woman; "
                "demanding or taking it away is illegal.",
                "Daughters and sons have equal property rights under the Hindu "
                "Succession Act.",
                "A widow has legal inheritance rights in her husband's property.",
            ],
        },
        {
            "category": "protection_rights",
            "rights": [
                "Right to live free of domestic violence (DV Act, 2005).",
                "Right to a safe workplace free of sexual harassment (POSH Act, 2013).",
                "Right to file a Zero FIR regardless of jurisdiction.",
                "Right to legal aid (Article 39A) and free legal services under "
                "the Legal Services Authorities Act, 1987.",
            ],
        },
    ],
    "resources": {
        "national": [
            "National Commission for Women (NCW) — 1800-120-1947",
            "AASRA (crisis counselling) — 91-9820466726",
            "iCall (counselling) — 9152987821",
            "Women Helpline — 181 (24/7 national helpline)",
            "Emergency (Police/Ambulance) — 112",
        ],
        "state_specific": [],
    },
}

def _find_act(query: str) -> dict | None:
    text = query.lower()
    best = None
    best_score = 0
    for act in LEGAL_KNOWLEDGE_BASE["acts"]:
        score = sum(1 for k in act["keywords"] if k in text)
        if score > best_score:
            best_score, best = score, act
    return best if best_score else None


def _find_procedure(query: str) -> dict | None:
    text = query.lower()
    for proc in LEGAL_KNOWLEDGE_BASE["procedures"]:
        if any(k in text for k in proc["keywords"]):
            return proc
    return None


def _format_act(act: dict) -> str:
    lines = [f"**{act['name']}**"]
    for point in act["key_points"]:
        lines.append(f"• {point}")
    if act.get("penalties"):
        lines.append(f"Penalties: {act['penalties']}")
    lines.append(f"How to file: {act['how_to_file']}")
    return "\n".join(lines)


def _format_procedure(proc: dict) -> str:
    lines = [f"**{proc['title']}**"]
    for i, step in enumerate(proc["steps"], 1):
        lines.append(f"{i}. {step}")
    return "\n".join(lines)


def generate_legal_response(query: str, language: str = "en") -> dict:
    """Retrieve the most relevant legal guidance for a user query.

    Returns a dict mirroring the spec's legal bot payload (response, sources,
    resources, disclaimer).
    """
    act = _find_act(query)
    procedure = _find_procedure(query)

    parts = []
    sources = []

    if act:
        parts.append(_format_act(act))
        sources.append({"act": act["name"], "sections": act["sections"]})
    if procedure:
        parts.append(_format_procedure(procedure))

    if not parts:
        parts.append(
            "I can help you understand Indian women's rights and the steps to seek "
            "protection. You can ask about domestic violence, dowry, workplace "
            "harassment, filing an FIR, or property/inheritance rights."
        )

    resources = LEGAL_KNOWLEDGE_BASE["resources"]
    resources_text = "\n".join(f"• {r}" for r in resources["national"])

    response = "\n\n".join(parts) + f"\n\n**Legal aid & helplines:**\n{resources_text}"
    if language != "en":
        response += (
            "\n\n(Please note: detailed guidance is available in English. A live "
            "translation into your language can be added in production.)"
        )

    return {
        "response": response,
        "sources": sources,
        "resources": resources["national"],
        "disclaimer": "This is general information, not legal advice. "
                      "Consult a lawyer or a women's commission for your specific case.",
        "language": language,
    }