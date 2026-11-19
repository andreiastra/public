# Explore Your Shore! and iNaturalist

A summary of [Explore Your Shore!](https://exploreyourshore.ie/) and how it relates to this project's iNaturalist observations.

> **Sources and limits:** based on the public pages of exploreyourshore.ie, biodiversityireland.ie, maps.biodiversityireland.ie and seasearchireland.ie. I did not find any page that mentions iNaturalist as an accepted source. Statements marked **(not confirmed)** need checking with the project directly.

---

## 1. What Explore Your Shore! is

- Ireland's marine biodiversity citizen science platform, run by the **National Biodiversity Data Centre (NBDC)** and funded by the **Environmental Protection Agency**.
- Aims:
  - build a baseline dataset of intertidal plants and animals in Ireland;
  - use intertidal species as bio-indicators of climate change and water quality;
  - raise public awareness of those issues.
- Context: in 2018 fewer than 4% of the 100,000 records sent to the NBDC were coastal marine species. The project was set up to change that.
- Contact: Dave Wall, Citizen Science Officer, NBDC (`dwall@biodiversityireland.ie`).

### Surveys

| Type | Survey | Focus |
|---|---|---|
| Own surveys | Seashore Spotter | Casual records of any marine species, any time, anywhere |
| | Big Beach Biodiversity Survey | Species cast ashore on beaches |
| | Great Rocky Shore BioBlitz | As many species as possible from a rocky shore |
| | Adopt-a-Rockpool | Repeat recording of one rockpool |
| Partner surveys | **Seasearch Ireland** | Diving and snorkelling surveys of sub-tidal species and habitats |
| | Angel Shark Project, Irish Whale and Dolphin Group, Purse Search, Irish Basking Shark Project, Big Jellyfish Hunt, Marine Turtle Records, KelpRes, KingSearch, Coastwatch Europe, BioProtect, angling survey | Species- or topic-specific recording |

Most of the site's own surveys are **intertidal**. The sub-tidal link is Seasearch Ireland.

### What happens to submitted records

From the Seashore Spotter and BioBlitz pages:

1. An expert checks the species identification and the position.
2. Validated records are added to the **Explore Your Shore! dataset** on [Biodiversity Maps](https://maps.biodiversityireland.ie/Dataset/305) (dataset 305) as open-access data.
3. Validated records are also shared with **EMODnet Biology (European Ocean Biodiversity Information System)** and **GBIF**, and feed UNESCO monitoring of Essential Ocean Variables.

---

## 2. How it relates to iNaturalist

Explore Your Shore! and iNaturalist are separate systems, but they overlap in two places.

### Shared downstream: GBIF

- The NBDC is Ireland's **GBIF node**. All open data on Biodiversity Maps, including Explore Your Shore!, is published to GBIF.
- iNaturalist also publishes **Research Grade** observations to GBIF (as the "iNaturalist Research-grade Observations" dataset).
- So both can end up in GBIF, but as **separate datasets via separate routes**. An iNaturalist observation does not become an Explore Your Shore! record because both reach GBIF.

### Seasearch Ireland

- Seasearch Ireland collects sub-tidal species and habitat records from volunteer divers and regularly submits validated records to the NBDC (53,231 at the time of the Explore Your Shore! page).
- Seasearch has its own **online observer record submission**.
- This is the route for dive records. See also [`Aligning_iNaturalist_Observations_with_Seasearch_Standards.md`](Aligning_iNaturalist_Observations_with_Seasearch_Standards.md).

### Comparison with Northern Ireland

Ulster Wildlife's **ShoreNI** survey tells participants to upload photos to iNaturalist. Explore Your Shore! does not say the same on any page I could read.

---

## 3. Can iNaturalist observations be contributed to Explore Your Shore!?

**Short answer:** not automatically, and I found no documented import from iNaturalist **(not confirmed)**. Contributing means submitting records through the project's own forms.

| Question | Finding |
|---|---|
| Does Explore Your Shore! pull in iNaturalist observations? | No evidence of this on the pages read **(not confirmed)** |
| Is there an iNaturalist project or collection for it? | None found **(not confirmed)** |
| Can you submit the same photos by hand? | Yes. Seashore Spotter takes photos through its online form, and you can tick "species unidentified". |
| Is there a route for dive records? | Yes. Seasearch Ireland observer records can be submitted online. |
| Does the project accept sub-tidal records? | Its own surveys are intertidal. Sub-tidal data comes via Seasearch. |

### Practical options

1. **Dive observations (most relevant):** submit through **Seasearch Ireland**'s online observer records. These go to the NBDC and appear on Biodiversity Maps.
2. **Intertidal or shore observations:** submit through **Seashore Spotter** or the relevant survey form, re-uploading the photo and location.
3. **General Irish records:** the NBDC runs a general recording portal (<https://records.biodiversityireland.ie/>), which accepts all species.
4. **Keep iNaturalist as the main record.** Research Grade observations reach GBIF through iNaturalist anyway.

### Things to watch

- **Duplicates:** a record in iNaturalist and in an NBDC dataset will show up twice in GBIF. This is normal but worth knowing.
- **Location accuracy:** Explore Your Shore! validation checks position. Obscured or imprecise iNaturalist coordinates should be corrected on the form.
- **Licence:** NBDC open data is published under CC-BY. Check it is compatible with your iNaturalist licence choice.
- **Site names:** the canonical names in [`Preferred_dive_site_names_ireland.txt`](Preferred_dive_site_names_ireland.txt) would make form submissions consistent.

---

## 4. Suggested next steps

- [ ] Email the NBDC (Dave Wall) to ask whether iNaturalist observations can be accepted, bulk-uploaded or linked.
- [ ] Ask Seasearch Ireland whether they take iNaturalist-based records, and what extra data they need (see the Seasearch alignment guide).
- [ ] Check the **Data** and **Bio-Indicators** pages on exploreyourshore.ie for downloadable species lists to compare with this project's Irish species list.
- [ ] Optionally add the Explore Your Shore! and Seasearch Ireland links to the README's profile section.

---

## 5. Links

- Explore Your Shore!: <https://exploreyourshore.ie/>
- Seasearch Ireland (on Explore Your Shore!): <https://exploreyourshore.ie/marine-surveys/seasearch-ireland/>
- Seashore Spotter: <https://exploreyourshore.ie/surveys/seashore-spotter/>
- Explore Your Shore! dataset: <https://maps.biodiversityireland.ie/Dataset/305>
- Biodiversity Maps (about): <https://maps.biodiversityireland.ie/About>
- NBDC citizen science recording portal: <https://records.biodiversityireland.ie/>
- Seasearch Ireland: <https://seasearchireland.ie/>
- iNaturalist profile: <https://www.inaturalist.org/people/andreiastra>
