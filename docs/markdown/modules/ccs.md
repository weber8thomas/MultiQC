---
title: CCS
displayed_sidebar: multiqcSidebar
description: >
  PacBio tool that generates highly accurate single-molecule consensus reads (HiFi Reads)
---

<!--
~~~~~ DO NOT EDIT ~~~~~
This file is autogenerated from the MultiQC module python docstring.
Do not edit the markdown, it will be overwritten.

File path for the source of this content: multiqc/modules/ccs/ccs.py
~~~~~~~~~~~~~~~~~~~~~~~
-->

:::note
PacBio tool that generates highly accurate single-molecule consensus reads (HiFi Reads)

[https://github.com/PacificBiosciences/ccs](https://github.com/PacificBiosciences/ccs)
:::

CCS takes multiple subreads of the same SMRTbell molecule and combines them
using a statistical model to produce one highly accurate consensus sequence,
also called HiFi read, with base quality values. This tool powers the Circular
Consensus Sequencing workflow in SMRT Link.

### File search patterns

```yaml
ccs/v4:
  contents: ZMWs generating CCS
  max_filesize: 1024
  num_lines: 2
ccs/v5:
  contents: '"id": "ccs_processing"'
  fn: "*.json"
```