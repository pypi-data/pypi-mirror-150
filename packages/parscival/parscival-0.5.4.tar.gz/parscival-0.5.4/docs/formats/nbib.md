# PubMed Nbib Parsing

## PubMed XML tags

```
# @see https://dtd.nlm.nih.gov/ncbi/pubmed/
# @see https://www.nlm.nih.gov/bsd/licensee/elements_descriptions.html

- Abstract
- Affiliation
- ArticleIdList
- ArticleTitle
- Author
- Chemical
- CitationSubset
- CommentsCorrections
- DateCompleted
- DateCreated
- Grant
- ISOAbbreviation
- ISSN
- ISSNLinking
- Issue
- Language
- MedlineJournalInfo
- MedlinePgn
- MeshHeading
- NameOfSubstance
- PMID
- PubDate
- PublicationType
- RefSource
- Title
- Volume
```

## CorText PubMed tags

```
- @[map] Abstract
- @[map] Affiliation
- @[map] ArticleTitle
- @[map] Author
- @[par] Author_firstname         <== Author // x[1]                    // (0,n)
- @[par] Author_name              <== Author // [x[0]+' '+x[2]]         // (0,n)
- %[map] CitationSubset           // States the subset(s) for which the MEDLINE record was created
- %[map] CommentsCorrections      // Contains the citation information for an associated publication's citation
- $[map] Chemical
- $[map] Chemical/NameOfSubstance
- @[map] DateCompleted
- @[map] DateCreated
- @[par] doi                      <== ArticleIdList // if '/'           // (0,1)
- @[map] Grant
- @[par] ISIpubdate               <== PubDate // [0][:4]                // (0,1)
- @[map] ISOAbbreviation
- @[map] ISSN
- @[map] ISSNLinking              // ISSNLinking indicates the linking ISSN (Electronic | Print)
- @[map] Issue
- @[map] Journal                  <== MedlineJournalInfo/Title          // (0,1)
- @[map] Language
- @[map] MedlineJournalInfo
- @[map] MedlinePgn
- @[map] MeshHeading
- @[map] MeshHeading_Description  <== MeshHeading                       // (0,1)
- @[pmt] original_filename        <== corpus_file // clean filename     // (0,1)
- @[par] PMID                     <== PMID   // [0][0]                  // (0,1)
- @[map] PubDate
- @[map] PublicationType
- %[map] RefSource                // Provides the reference string for the associated publication
- @[map] Title
- @[map] Volume
```

## CorText extra tags

```
- dates
- authors_names
- authors_fullname
- affiliations_name
- affiliations_address
- affiliations_country
- affiliations
```

## PubMed nbib tags

```
# https://pubmed.ncbi.nlm.nih.gov/help/#pubmed-format
# https://docs.jabref.org/v/v4/import-export/knowledge/medlineris

- [map] AB       Abstract                            // English language abstract taken directly from the published article
- [map] AD       Affiliation                         // Author or corporate author addresses
- [par] AU       Author                              // Authors List
- [par] AID      doi (if '[doi]')                    // Article ID values supplied by the publisher
- [map] CRDT     DateCreated                         // The date the citation record was first created
- [map] DCOM     DateCompleted                       // NLM internal processing completion date
- [map] DP       PubDate                             // The date the article was published
- [map] FAU      Author_name,Author_firstname        // Full Author Names
- [map] GR       Grant                               // Research grant numbers, contract numbers, or both
- [map] IP       Issue                               // The number of the issue
- [map] IS       ISSN                                // International Standard Serial Number of the journal
- [par] IS       ISSNLinking '(Electronic|Linking)'  // International Standard Serial Number of the journal
- [map] JT       Journal/Title                       // Full journal title from NLM cataloging data
- [map] LA       Language                            // The language in which the article was published
- [map] MH       MeshHeading_Description             // NLM Medical Subject Headings (MeSH) controlled vocabulary
- [map] PG       Pagination/MedlinePgn               // The full pagination of the article
- [map] PMID     PMID                                // Unique number assigned to each PubMed citation
- [map] PT       PublicationType                     // The type of material the article represents
- [par] RN       Chemical,/NameOfSubstance           // Includes chemical, protocol or disease terms. May also a number assigned by the Enzyme Commission or by the Chemical Abstracts Service.
- [map] TA       ISOAbbreviation                     // Standard journal title abbreviation
- [map] TI       ArticleTitle                        // The title of the article
- [map] VI       Volume                              // Volume number of the journal
```

## Mapping tags profile

| Qualifier   | Source | Target                    | Cardinality | Type      | Mapping | Process Tasks | Dimension |
| ----------- | ------ | ------------------------- | ----------- | --------- | ------- | ------------- | --------- |
| `repeated`  | `FAU`  | `Author_name`             | `{1,n}`     | `text`    | `par`   | `[CUST]`      | `[actor]` |
| `optional`  | `DP`   | `ISIpubdate`              | `{0,1}`     | `integer` | `par`   | `[YYYY]`      | `[time]`  |
| `requiered` | `TI`   | `ArticleTitle`            | `{1,1}`     | `text`    | `map`   | `[NONE]`      | `[topic]` |
| `optional`  | `AB`   | `Abstract`                | `{0,1}`     | `text`    | `fmt`   | `[PARAG]`     | `[topic]` |
| `repeated`  | `AD`   | `Affiliation`             | `{1,n}`     | `text`    | `map`   | `[CUST]`      | `[geo]`   |
| `repeated`  | `RH`   | `MeshHeading_Description` | `{0,n}`     | `text`    | `par`   | `[CUST]`      | `[topic]` |

ToDo
- Add 'Parse delimeter' column

## Process Tasks and Formats

- `[CHOMP]`: Remove leading and trailing blank lines
- `[PARAG]`: Remove leading and trailing blank but keeping text paragraphs
- `[YYYY]` : Four digits year
- `[CUST]`: Custom parser

## Mappings

Illustration below show a list of mappings between `PubMed XML`, `CorTex Graph` and `PubMed Nbib` formats.

```
Legend:

map: raw mapping
par: parsing mapping
fmt: format mapping
pmt: derived from parsing
xxx: no mapping available
```

```{mermaid}

  %%{ init: {
      'theme': 'base',
      'themeVariables': {
        'fontSize': '10px',
        'fontFamily': 'Inconsolata'}
      }
  }%%

  graph LR
      Abstract_PM(Abstract)                               ---|map|Abstract_CT(Abstract)
      Affiliation_PM(Affiliation)                         ---|map|Affiliation_CT(Affiliation)
      ArticleTitle_PM(ArticleTitle)                       ---|map|ArticleTitle_CT(ArticleTitle)
      Author_PM(Author)                                   ---|map|Author_CT(Author)
      Author_PM(Author)                                   ---|par|Author_firstname_CT(Author_firstname)
      Author_PM(Author)                                   ---|par|Author_name_CT(Author_name)
      ArticleIdList_PM(ArticleIdList)                     ---|par|doi_CT(doi)
      CitationSubset_PM(CitationSubset)                   ---|map|CitationSubset_CT(CitationSubset)
      CommentsCorrections_PM(CommentsCorrections)         ---|map|CommentsCorrections_CT(CommentsCorrections)
      Chemical_PM(Chemical)                               ---|map|Chemical_CT(Chemical)
      NameOfSubstance_PM(Chemical/NameOfSubstance)        ---|map|NameOfSubstance_CT(Chemical/NameOfSubstance)
      DateCompleted_PM(DateCompleted)                     ---|map|DateCompleted_CT(DateCompleted)
      DateCreated_PM(DateCreated)                         ---|map|DateCreated_CT(DateCreated)
      Grant_PM(Grant)                                     ---|map|Grant_CT(Grant)
      PubDate_PM(PubDate)                                 ---|par|ISIpubdate_CT(ISIpubdate)
      ISOAbbreviation_PM(ISOAbbreviation)                 ---|map|ISOAbbreviation_CT(ISOAbbreviation)
      ISSN_PM(ISSN)                                       ---|map|ISSN_CT(ISSN)
      ISSNLinking_PM(ISSNLinking)                         ---|map|ISSNLinking_CT(ISSNLinking)
      Issue_PM(Issue)                                     ---|map|Issue_CT(Issue)
      Language_PM(Language)                               ---|map|Language_CT(Language)
      Title_PM(Title)                                     ---|map|Journal_CT(Journal)
      MedlinePgn_PM(MedlinePgn)                           ---|map|MedlinePgn_CT(MedlinePgn)
      MeshHeading_PM(MeshHeading)                         ---|map|MeshHeading_CT(MeshHeading)
      MeshHeading_PM(MeshHeading)                         ---|map|MeshHeading_Description_CT(MeshHeading_Description)
      PMID_PM(PMID)                                       ---|map|PMID_CT(PMID)
      PubDate_PM(PubDate)                                 ---|map|PubDate_CT(PubDate)
      PublicationType_PM(PublicationType)                 ---|map|PublicationType_CT(PublicationType)
      RefSource_PM(RefSource)                             ---|map|RefSource_CT(RefSource)
      Volume_PM(Volume)                                   ---|map|Volume_CT(Volume)
      PARSING_PM("@")                                     ---|zzz|original_filename_CT(original_filename)

      Abstract_CT(Abstract)                               ---|fmt|AB_NB(AB)
      Affiliation_CT(Affiliation)                         ---|par|AD_NB(AD)
      ArticleTitle_CT(ArticleTitle)                       ---|map|TI_NB(TI)
      Author_CT(Author)                                   ---|map|AU_NB(AU)
      Author_firstname_CT(Author_firstname)               ---|par|FAU_NB(FAU)
      Author_name_CT(Author_name)                         ---|par|FAU_NB(FAU)
      CitationSubset_CT(CitationSubset)                   ---|xxx|NOTHING_NB(.)
      CommentsCorrections_CT(CommentsCorrections)         ---|xxx|NOTHING_NB(.)
      Chemical_CT(Chemical)                               ---|par|RN_NB(RN)
      NameOfSubstance_CT(Chemical/NameOfSubstance)        ---|par|RN_NB(RN)
      DateCompleted_CT(DateCompleted)                     ---|map|DCOM_NB(DCOM)
      DateCreated_CT(DateCreated)                         ---|map|CRDT_NB(CRDT)
      doi_CT(doi)                                         ---|par|AID_NB("AID['doi']")
      Grant_CT(Grant)                                     ---|map|GR_NB(GR)
      ISIpubdate_CT(ISIpubdate)                           ---|par|DP_NB(DP)
      ISOAbbreviation_CT(ISOAbbreviation)                 ---|map|TA_NB(TA)
      ISSN_CT(ISSN)                                       ---|map|IS_NB(IS)
      ISSNLinking_CT(ISSNLinking)                         ---|par|IS_NB(IS)
      Issue_CT(Issue)                                     ---|map|IP_NB(IP)
      Journal_CT(Journal)                                 ---|map|JT_NB(JT)
      Language_CT(Language)                               ---|map|LA_NB(LA)
      MedlinePgn_CT(MedlinePgn)                           ---|par|PG_NB(PG)
      MeshHeading_CT(MeshHeading)                         ---|par|MH_NB(MH)
      MeshHeading_Description_CT(MeshHeading_Description) ---|par|MH_NB(MH)
      PMID_CT(PMID)                                       ---|map|PMID_NB(PMID)
      PubDate_CT(PubDate)                                 ---|map|DP_NB(DP)
      PublicationType_CT(PublicationType)                 ---|map|PT_NB(PT)
      RefSource_CT(RefSource)                             ---|xxx|NOTHING_NB(.)
      Volume_CT(Volume)                                   ---|map|VI_NB(VI)
      original_filename_CT(original_filename)             ---|zzz|PARSING_NB("@")


      subgraph PubMed XML
        direction LR

        Abstract_PM
        Affiliation_PM
        ArticleIdList_PM
        ArticleTitle_PM
        Author_PM
        Chemical_PM
        CitationSubset_PM
        CommentsCorrections_PM
        DateCompleted_PM
        DateCreated_PM
        Grant_PM
        ISOAbbreviation_PM
        ISSN_PM
        ISSNLinking_PM
        Issue_PM
        Language_PM
        MedlinePgn_PM
        MeshHeading_PM
        NameOfSubstance_PM
        PMID_PM
        PubDate_PM
        PublicationType_PM
        RefSource_PM
        Title_PM
        Volume_PM

        PARSING_PM
      end

      subgraph CorText
        Abstract_CT
        Affiliation_CT
        ArticleTitle_CT
        Author_CT
        Author_firstname_CT
        Author_name_CT
        CitationSubset_CT
        CommentsCorrections_CT
        Chemical_CT
        NameOfSubstance_CT
        DateCompleted_CT
        DateCreated_CT
        doi_CT
        Grant_CT
        ISIpubdate_CT
        ISOAbbreviation_CT
        ISSN_CT
        ISSNLinking_CT
        Issue_CT
        Journal_CT
        Language_CT
        MedlinePgn_CT
        MeshHeading_CT
        MeshHeading_Description_CT
        original_filename_CT
        PMID_CT
        PubDate_CT
        PublicationType_CT
        RefSource_CT
        Volume_CT
      end

      subgraph PubMed NBIB
        direction RL

        AB_NB
        AD_NB
        AU_NB
        AID_NB
        CRDT_NB
        DCOM_NB
        DP_NB
        FAU_NB
        GR_NB
        IP_NB
        IS_NB
        IS_NB
        JT_NB
        LA_NB
        MH_NB
        PG_NB
        PMID_NB
        PT_NB
        RN_NB
        TA_NB
        TI_NB
        VI_NB

        NOTHING_NB
        PARSING_NB
      end
```

### Mapping questions

- `OT`: `Keywords`
- `??`: `NameOfSubstance`


## CorText Graph Format

| Field       | Value                                | Type             | Description              |
| ----------- | ------------------------------------ | ---------------- | ------------------------ |
| `file`      | `sourceFile(fieldName)`              | `text`           | source file for the data |
| `id`        | `fieldName.doc[0,n-1]`               | `integer`        | ID of each document      |
| `rank`      | `fieldName.doc[id][0,m-1]`           | `integer`        | field cardinal index     |
| `parserank` | `fieldName.doc[id][rank][0,p-1]`     | `integer`        | parsed cardinal index    |
| `data`      | `fieldName.doc[id][rank][parserank]` | `[text,integer]` | parsed data              |

### Templates

#### SQLite DB

```sql
CREATE TABLE {{field_id}} (
  file text,
  id integer,
  rank integer,
  parserank integer,
  data {{field_type}}
);

INSERT INTO {{field_id}} VALUES ({{file}}, {{id}}, {{rank}}, {{parserank}}, {{data}});
```

#### Metadata description

```yaml
  "alltables": {{alltables}},
  "corpus_type": "pubmed",
  "extension": "db",
  "file": {{file}},
  "indexed": False,
  "origin": "dataset",
  "structure": "reseaulu",
  "tablenames": {{tablenames}},
  "textual_fields": {{textual_fields}},
  "totaltables": {{totaltables}},
  "uri": {{uri}},
  "version": {{version}},
```

## PubMed nbib extra tags

```
# @see https://github.com/holub008/nbib

- [xxx] CI    TagParser(Category.STUDY, 'copyright'),
- [xxx] CN    TagParser(Category.STUDY, 'corporate_author'),
- [xxx] COIS  TagParser(Category.STUDY, 'conflict_of_interest'),  # note: documentation incorrectly calls this 'COI'
- [xxx] DEP   DateTimeParser(Category.STUDY, 'electronic_publication_date'),
- [xxx] JID   TagParser(Category.STUDY, 'nlm_journal_id'),  # not an integer because sometimes suffixed with 'R'
- [xxx] LR    DateTimeParser(Category.STUDY, 'last_revision_date'),
- [xxx] OT    TagParser(Category.KEYWORD, 'keyword'),
- [xxx] OWN   TagParser(Category.STUDY, 'citation_owner'),
- [xxx] PHST  PubMedHistoryParser(),
- [xxx] PL    TagParser(Category.STUDY, 'place_of_publication'),
- [xxx] PMC   PMCIDParser(Category.STUDY, 'pmcid'),
- [xxx] PST   TagParser(Category.STUDY, 'publication_status'),
- [xxx] SI    TagParser(Category.STUDY, 'secondary_source'),
- [xxx] STAT  TagParser(Category.STUDY, 'nlm_status'),
- [xxx] TT    TagParser(Category.STUDY, 'transliterated_title'),
```

## PubMed All Tags

```
# @source https://pubmed.ncbi.nlm.nih.gov/help/#pubmed-format

AB    Abstract                                 // English language abstract taken directly from the published article
AD    Affiliation                              // Author or corporate author addresses
AID   Article Identifier                       // Article ID values supplied by the publisher may include the pii (controlled publisher identifier), doi (digital object identifier), or book accession
AU    Author                                   // Authors
BTI   Book Title                               // Book Title
CI    Copyright Information                    // Copyright statement provided by the publisher
CIN   Comment In                               // Reference containing a comment about the article
CN    Corporate Author                         // Corporate author or group names with authorship responsibility
COI   Conflict of Interest                     // Conflict of interest statement
CON   Comment On                               // Reference upon which the article comments
CP    Chapter                                  // Book chapter
CRDT  Create Date                              // The date the citation record was first created
CRF   Corrected and republished from           // Final, correct version of an article
CRI   Corrected and republished in             // Original article that was republished in corrected form
CTDT  Contribution Date                        // Book contribution date
CTI   Collection Title                         // Collection Title
DCOM  Completion Date                          // NLM internal processing completion date
DDIN  Dataset described in                     // Citation for the primary article resulting from a dataset
DRIN  Dataset use reported in                  // Citation for an article that uses a dataset from another scientific article
DEP   Date of Electronic Publication           // Electronic publication date
DP    Publication Date                         // The date the article was published
DRDT  Date Revised                             // Book Revision Date
ECF   Expression of Concern For                // Reference containing an expression of concern for an article
ECI   Expression of Concern In                 // Cites the original article for which there is an expression of concern
EDAT  Entrez Date                              // The date the citation was added to PubMed; the date is set to the publication date if added more than 1 year after the date published
EFR   Erratum For                              // Cites the original article for which there is a published erratum; as of 2016, partial retractions are considered errata
EIN   Erratum In                               // Cites a published erratum to the article
ED    Editor                                   // Book editors
EN    Edition                                  // Book edition
FAU   Full Author Name                         // Full Author Names
FED   Full Editor Name                         // Full Editor Names
FIR   Full Investigator                        // Full investigator or collaborator name
FPS   Full Personal Name as Subject            // Full Personal Name of the subject of the article
GN    General Note                             // Supplemental or descriptive information related to the document
GR    Grant Number                             // Research grant numbers, contract numbers, or both that designate financial support by any agency of the US PHS or other funding agencies
GS    Gene Symbol                              // Abbreviated gene names (used 1991 through 1996)
IP    Issue                                    // The number of the issue, part, or supplement of the journal in which the article was published
IR    Investigator                             // Investigator or collaborator
IRAD  Investigator Affiliation                 // Investigator or collaborator addresses
IS    ISSN                                     // International Standard Serial Number of the journal
ISBN  ISBN                                     // International Standard Book Number
JID   NLM Unique ID                            // Unique journal ID in the NLM catalog of books, journals, and audiovisuals
JT    Full Journal Title                       // Full journal title from NLM cataloging data
LA    Language                                 // The language in which the article was published
LID   Location ID                              // The pii or doi that serves the role of pagination
LR    Modification Date                        // Citation last revision date
MH    MeSH Terms                               // NLM Medical Subject Headings (MeSH) controlled vocabulary
MHDA  MeSH Date                                // The date MeSH terms were added to the citation. The MeSH date is the same as the Entrez date until MeSH are added
OAB   Other Abstract                           // Abstract supplied by an NLM collaborating organization
OABL  Other Abstract Language                  // Language of an abstract available from the publisher
OCI   Other Copyright Information              // Copyright owner
OID   Other ID                                 // Identification numbers provided by organizations supplying citation data
ORI   Original Report In                       // Cites the original article associated with the patient summary
OT    Other Term                               // Non-MeSH subject terms (keywords) either assigned by an organization identified by the Other Term Owner, or generated by the author and submitted by the publisher
OTO   Other Term Owner                         // Organization that may have provided the Other Term data
OWN   Owner                                    // Organization acronym that supplied citation data
PB    Publisher                                // Publishers of Books & Documents citations
PG    Pagination                               // The full pagination of the article
PHST  Publication History Status Date          // Publisher supplied dates regarding the article publishing process and PubMed date stamps:
PL    Place of Publication                     // Journal's (country only) or book’s place of publication
PMCR  PMC Release                              // Availability of PMC article
PMID  PubMed Unique Identifier                 // Unique number assigned to each PubMed citation
PS    Personal Name as Subject                 // Individual is the subject of the article
PST   Publication Status                       // Publication status
PT    Publication Type                         // The type of material the article represents
RF    Number of References                     // Number of bibliographic references for Review articles
RIN   Retraction In                            // Retraction of the article
RN    EC/RN Number                             // Includes chemical, protocol or disease terms. May also a number assigned by the Enzyme Commission or by the Chemical Abstracts Service.
ROF   Retraction Of                            // Article being retracted
RPF   Republished From                         // Article being cited has been republished or reprinted in either full or abridged form from another source
RPI   Republished In                           // Article being cited also appears in another source in either full or abridged form
RRI   Retracted and Republished In             // Final, republished version of an article
RRF   Retracted and Republished From           // Original article that was retracted and republished
SB    Subset                                   // Journal or citation subset values representing specialized topics
SFM   Space Flight Mission                     // NASA-supplied data space flight/mission name and/or number
SI    Secondary Source Identifier              // Identifies secondary source databanks and accession numbers of molecular sequences discussed in articles
SO    Source                                   // Composite field containing bibliographic information
SPIN  Summary For Patients In                  // Cites a patient summary article
STAT  Status Tag                               // Used for internal processing at NLM
TA    Journal Title Abbreviation               // Standard journal title abbreviation
TI    Title                                    // The title of the article
TT    Transliterated Title                     // Title of the article originally published in a non-English language, in that language
UIN   Update In                                // Update to the article
UOF   Update Of                                // The article being updated
VI    Volume                                   // Volume number of the journal
VTI   Volume Title                             // Book Volume Title
```

### Related documentation

```
# @source https://gitlab.com/cortext/cortext-methods/istex

Mapping0[Text0 -> Tuple0[Sequence0[Sequence1[Sequence2[[Text1, Any0]]]], Type0[Any0]]]

Semantics:

Mapping0: the database
Text0: table name
Sequence0: first index (id)
Sequence1: second index (rank)
Sequence2: third index (parserank)
Text1: source file for the data point
Any0: value of the data point
Type0: type of all data points in the table


// Sequences{0,1,2} are actually implemented as integer-valued columns in the table.
// Any0 is actually more restrictive than Any, more like:
// Union[Text, int, float, Sequence[Union[Text, int, float]]]
// Information about a single document thus fixes a single index at Sequence0:
// Mapping0[Text0 -> Tuple0[Sequence1[Sequence2[[Text1, Any0]]], Type0]]
// If we drop the table and type:
// Sequence1[Sequence2[[Text1, Any0]]]
// If we drop the source file:
// Sequence1[Sequence2[Text1]])
```

## Features

### Functional

- parse .nbib to .sqlite

### Non-functional

- deduplication
- errors handling
- logging
- versioning

## References

### Documentation

- CorText storage: https://docs.cortext.net/data-parsing/#cortext-manager-data-storage-philosophy
- PubMed User Guide: https://pubmed.ncbi.nlm.nih.gov/help
- PubMed XML doc: https://dtd.nlm.nih.gov/ncbi/pubmed/
- PubMed XML DTD: https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd
- PubMed NBIB doc: https://pubmed.ncbi.nlm.nih.gov/help/#pubmed-format

### Related code source

- CorText XML PubMed parser: https://github.com/cortext/cortext-methods/blob/master/parser_science/parser_science_se.py#L994
- CorText ISTEX parser: https://gitlab.com/cortext/cortext-methods/istex
- CorText Library: https://gitlab.com/cortext/cortext-methods/cortextlib
- NBIB Parser: https://github.com/holub008/nbib

### Test datasets

- [hetercat.nbib](https://pubmed.ncbi.nlm.nih.gov/?term=heterogenous+catalyst)
- [pesticides.nbib](https://pubmed.ncbi.nlm.nih.gov/?term=pesticide+exposure+in+children)
