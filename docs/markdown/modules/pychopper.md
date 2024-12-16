---
title: Pychopper
displayed_sidebar: multiqcSidebar
description: >
  Identifies, orients, trims and rescues full length Nanopore cDNA reads. Can also rescue fused reads
---

<!--
~~~~~ DO NOT EDIT ~~~~~
This file is autogenerated from the MultiQC module python docstring.
Do not edit the markdown, it will be overwritten.

File path for the source of this content: multiqc/modules/pychopper/pychopper.py
~~~~~~~~~~~~~~~~~~~~~~~
-->

:::note
Identifies, orients, trims and rescues full length Nanopore cDNA reads. Can also rescue fused reads

[https://github.com/nanoporetech/pychopper](https://github.com/nanoporetech/pychopper)
:::

The module parses the pychopper stats file. Pychopper needs to be run with the `-S stats_output` option to create the file. The name of the output file defines the sample name.

The stats file is a three column `tsv` file with the format `category name value`.

Currently only two stats are displayed in MultiQC. Two bargraphs are created for the read classication and the strand orientation of the identified full length transcripts. Additional stats could be included on further request.

The general stats table contains a value that displays the percentage of full length transcripts. This value is calculated from the cumulative length of reads where Pychopper found primers at both ends.

### File search patterns

```yaml
pychopper:
  contents: "Classification\tRescue"
  num_lines: 6
```