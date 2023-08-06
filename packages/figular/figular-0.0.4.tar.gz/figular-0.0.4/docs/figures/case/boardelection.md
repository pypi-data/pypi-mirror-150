<!--
SPDX-FileCopyrightText: 2021-2 Galagic Limited, et. al. <https://galagic.com>

SPDX-License-Identifier: CC-BY-SA-4.0

figular generates visualisations from flexible, reusable parts

For full copyright information see the AUTHORS file at the top-level
directory of this distribution or at
[AUTHORS](https://gitlab.com/thegalagic/figular/AUTHORS.md)

This work is licensed under the Creative Commons Attribution 4.0 International
License. You should have received a copy of the license along with this work.
If not, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
-->

# Case/BoardElection

This figure was created for the OSI Board Election. See our blog post for more
background information. It shows the current members of an organisation in a
central org chart, surrounded by two clusters of candidates who are hoping to
become members by election. However it could be repurposed to show any two sets
of concepts grouped in circles around an org chart.

* [Suggested Purpose](#suggested-purpose)
* [Usage](#usage)
* [Limitations](#limitations)
* [Examples](#examples)

## Suggested Purpose

* To show candidates standing for election to an organisation
* To show two sets of concepts related to an organisation (if we replace
  the two candidate clusters with concepts)

## Usage

### On the Website

Here's what you should see when you first visit the [Board
Election](https://figular.com/tryit/case/boardelection/) page:

![A screenshot of https://figular.com/tryit/case/boardelection](website_screenshot.png)

You can enter data to change the figure in the text box at the top left of the
page. The format follows the [markdown](https://en.wikipedia.org/wiki/Markdown)
language and should be mostly self-explanatory if you compare it to the graphic
produced. To be precise:

* The first section defines the overall title and subtitle:

```markdown
> # Title
> ## Subtitle
> ---
```

* This is follow by two identical sections which define the candidate lists,
  along with their titles and subtitles:

```markdown
> # Individual Candidates
> ## Elected by members to serve two year terms.
> Candidate One
> Candidate Two
> Candidate Three
> ...
```

* Finally this is followed by a section which defines the central org chart:

```markdown
> Board
> Board Member One|Director,2,24|Board
> Board Member Two|Director,3,24|Board
> Board Member Three|Director,3,24|Board
> Board Member Four|Director,5,24|Board
> Board Member Five|Director,7,24|Board
> Board Member Six|Director,9,24|Board
> Board Member Seven|Director,10,24|Board
> Board Member Eight|Director,14,24|Board
```

  The format here is that for our [org chart
  (docs)](https://gitlab.com/thegalagic/figular/-/blob/main/docs/figures/org/orgchart.md)
  figure, so follow that link for more information. There is an addition to the
  format though - where we specify a role for each person we also include the
  term they have served and the total term, separated by commas:

> Director,2,24

  This means this director has served 2 months of their 24 month term. Fields
  are separated by commas. These numbers lead to the creation of the pie chart
  that accompanies each person in the org chart. If you don't want the pie chart
  you can just leave out the numbers.

### At the Cmdline

This figure will accept one large string of the markdown data:

```bash
fig case/boardelection "# The Board
## Election Candidates
---
# Individual Candidates
## Elected by members to serve two year terms.
Candidate One
Candidate Two
Candidate Three
Candidate Four
Candidate Five
Candidate Six
Candidate Seven
---
# Corporate Candidates
## Elected by corporate members to serve three year terms.
Candidate One
Candidate Two
Candidate Three
Candidate Four
Candidate Five
Candidate Six
Candidate Seven
Candidate Eight
Candidate Nine
---
Board
Board Member One|Director,2,24|Board
Board Member Two|Director,3,24|Board
Board Member Three|Director,3,24|Board
Board Member Four|Director,5,24|Board
Board Member Five|Director,7,24|Board
Board Member Six|Director,9,24|Board
Board Member Seven|Director,10,24|Board
Board Member Eight|Director,14,24|Board"
```

## Limitations

* We only support two clusters of candidates either side of the central org chart.
* The head or top of the organisation is removed as are the lines connecting
  members to the head.
* No styling options are available.

## Examples

![The OSI Board Election 2022. In the center we see the OSI board members with
their roles and terms served. Either side are clusters of the individual
 candidates and affiliate candidates](example_osi.svg)

### On the Website

Enter the following into the text box:

```text
# OSI BOARD
## ELECTION 2022
---
# INDIVIDUAL CANDIDATES
## Elected by individual members to serve two year terms.
Amanda Brock
Hilary Richardson
Jean-Brunel Webb-Benjamin
Jim Hall
Josh Berkus
Kevin P. Fleming
Myrle Krantz
Rossella Sblendido
Tetsuya Kitahata
---
# AFFILIATE CANDIDATES
## Elected by affiliate members to serve three year terms.
Benito Gonzalez
Carlo Piana
Gael Blondelle
George DeMet
Lior Kaplan
Marco A. Gutierrez
Matt Jarvis
Pamela Chestek
---
OSI Board
Josh Simmons|Former Chair,22,24|OSI Board
Pamela Chestek|Director,35,36|OSI Board
Megan Byrd-Sanicki|Former Vice Chair,23,24|OSI Board
Italo Vignoli|Director,23,36|OSI Board
Aeva Black|Assistant Secretary,7,20|OSI Board
Hong Phuc Dang|Director,7,32|OSI Board
Catharina Maracke|Chair,7,20|OSI Board
Thierry Carrez|Vice Chair,7,32|OSI Board
Justin Colannino|Director,2,24|OSI Board
Tracy Hinds|Director,2,10|OSI Board
```

### At the Cmdline

```bash
fig case/boardelection "# OSI BOARD
## ELECTION 2022
---
# INDIVIDUAL CANDIDATES
## Elected by individual members to serve two year terms.
Amanda Brock
Hilary Richardson
Jean-Brunel Webb-Benjamin
Jim Hall
Josh Berkus
Kevin P. Fleming
Myrle Krantz
Rossella Sblendido
Tetsuya Kitahata
---
# AFFILIATE CANDIDATES
## Elected by affiliate members to serve three year terms.
Benito Gonzalez
Carlo Piana
Gael Blondelle
George DeMet
Lior Kaplan
Marco A. Gutierrez
Matt Jarvis
Pamela Chestek
---
OSI Board
Josh Simmons|Former Chair,22,24|OSI Board
Pamela Chestek|Director,35,36|OSI Board
Megan Byrd-Sanicki|Former Vice Chair,23,24|OSI Board
Italo Vignoli|Director,23,36|OSI Board
Aeva Black|Assistant Secretary,7,20|OSI Board
Hong Phuc Dang|Director,7,32|OSI Board
Catharina Maracke|Chair,7,20|OSI Board
Thierry Carrez|Vice Chair,7,32|OSI Board
Justin Colannino|Director,2,24|OSI Board
Tracy Hinds|Director,2,10|OSI Board"
```
