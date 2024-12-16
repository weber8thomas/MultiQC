"""
Generate documentation for MultiQC modules and changelog.

Usage:
    python scripts/make_docs.py <docs_repo_path>
"""

from datetime import datetime
import json
import os
from typing import Dict
import yaml
import argparse
from pathlib import Path
from textwrap import dedent, indent
import subprocess

from multiqc import config, report, BaseMultiqcModule


def main():
    TEST_DATA_DIR = Path("test-data")
    if not TEST_DATA_DIR.exists():
        print("Cloning test-data to test-data")
        subprocess.run(["git", "clone", "https://github.com/MultiQC/test-data.git", TEST_DATA_DIR], check=True)

    OUTPUT_PATH = Path("docs")

    # Load search patterns
    sp_by_mod: Dict[str, Dict] = dict()
    with (Path(config.MODULE_DIR) / "search_patterns.yaml").open() as f:
        for k, v in yaml.safe_load(f).items():
            mod_id = k.split("/")[0]
            sp_by_mod.setdefault(mod_id, {})[k] = v

    # Generate module documentation
    modules_data = []
    for mod_id, entry_point in config.avail_modules.items():
        if mod_id == "custom_content":
            continue

        mod_data_dir = TEST_DATA_DIR / "data/modules" / mod_id
        assert mod_data_dir.exists() and mod_data_dir.is_dir(), mod_data_dir

        report.analysis_files = [mod_data_dir]
        report.search_files([mod_id])

        module_cls = entry_point.load()
        module: BaseMultiqcModule = module_cls()

        modules_data.append(
            {
                "id": f"modules/{mod_id}",
                "data": {
                    "name": f"{module.name}",
                    "summary": f"{module.info}",
                },
            }
        )

        docstring = module_cls.__doc__ or ""

        if module.extra:
            extra = "\n".join(line.strip() for line in module.extra.split("\n") if line.strip())
            extra += "\n\n"
        else:
            extra = ""

        text = f"""\
---
title: {module.name}
displayed_sidebar: multiqcSidebar
description: >
{indent(module.info, "    ")}
---

<!--
~~~~~ DO NOT EDIT ~~~~~
This file is autogenerated from the MultiQC module python docstring.
Do not edit the markdown, it will be overwritten.

File path for the source of this content: multiqc/modules/{mod_id}/{mod_id}.py
~~~~~~~~~~~~~~~~~~~~~~~
-->

:::note
{module.info}

{", ".join([f"[{href}]({href})" for href in module.href])}
:::

{extra}{dedent(docstring)}

### File search patterns

```yaml
{yaml.dump(sp_by_mod[mod_id]).strip()}
```
    """

        # Remove double empty lines
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")

        module_md_path = OUTPUT_PATH / "markdown/modules" / f"{mod_id}.md"
        module_md_path.parent.mkdir(parents=True, exist_ok=True)
        with module_md_path.open("w") as fh:
            fh.write(text)
        print(f"Generated {module_md_path}")

    mdx_path = OUTPUT_PATH / "markdown/modules.mdx"
    with mdx_path.open("w") as fh:
        fh.write(
            f"""\
---
title: Supported Tools
description: Tools supported by MultiQC
displayed_sidebar: multiqcSidebar
---

<!--
~~~~~ DO NOT EDIT ~~~~~
This file is autogenerated. Do not edit the markdown, it will be overwritten.
~~~~~~~~~~~~~~~~~~~~~~~
-->

MultiQC currently has modules to support {len(config.avail_modules)} bioinformatics tools, listed below.

Click the tool name to go to the MultiQC documentation for that tool.

:::tip[Missing something?]
If you would like another tool to to be supported, please [open an issue](https://github.com/MultiQC/MultiQC/issues/new?labels=module%3A+new&template=module-request.yml).
:::

import MultiqcModules from "@site/src/components/MultiqcModules";

<MultiqcModules
modules={{{str(json.dumps(modules_data))}}}
/>

    """
        )

    # Format markdown files
    subprocess.run(["npx", "prettier", "--write", "docs/markdown/modules/*.md"], check=True)
    subprocess.run(["npx", "prettier", "--write", "docs/markdown/modules.mdx"], check=True)


if __name__ == "__main__":
    main()