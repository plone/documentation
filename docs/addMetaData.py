import os
import logging
metadata_check = """---
myst:
"""
metadata = """---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

"""
logging.basicConfig()
logger = logging.getLogger("addMetaData")
logger.setLevel(logging.INFO)

logger.info("Add html_meta snippet if necessary.")
count_files = {
    "modified": 0,
    "unmodified": 0,
}
docs_dir = "./docs" if os.path.isdir("./docs") else "."

for root, dirs, files in os.walk(docs_dir):
    for name in files:
        if name.endswith(".md"):
            filename = os.path.join(root, name)
            # print(filename)
            with open(filename, "r+") as f:
                data = f.read()
                if not data.startswith(metadata_check):
                    f.seek(0)
                    f.write(metadata)
                    f.write(data)
                    count_files["modified"] += 1
                    logger.info(f"{filename} html_meta prepended.")
                else:
                    count_files["unmodified"] += 1
logger.info(f'html_meta snippet added to {count_files["modified"]} files.')
logger.info(f'{count_files["unmodified"]} files unmodified.')
