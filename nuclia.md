# Replacing Sphinx Search with Nuclia Search in Plone

## Overview

This documentation outlines the process of replacing Sphinx search in a Plone site with Nuclia search. The goal is to explain the approach taken and provide instructions for replicating the process in another project.

## Approach

### Data Indexing and Processing

To achieve the transition, the following steps were taken:

1. **Generate Nuclia Sync Data:**
   - Iterate through `.md` files in the repository [docs](https://github.com/plone/documentation/tree/6.0/docs) .
   - Calculate the hash of each file and store the mapping in `nuclia_sync.json`.

2. **Extract Headings:**
   - Use regular expressions to extract headings from Markdown files.
   - Store the extracted headings and slugs for document URLs.

3. **Upload Documents:**
   - Utilize the `NucliaUpload` class from the `nuclia` SDK.
   - Generated slugs, Extracted headings, Nuclia `API_KEY` and constructed URLs for `.md` can be passed in the class method.

4. **Synchronize Documents:**
   - Compare hashes to determine whether to upload, update, or delete documents, when changes are made.
   - Handle document deletions using the `NucliaKB` class.

5. **GitHub Actions Workflow:**
   - Created a synchronization workflow triggered by a `push` event.
   - Defined the steps for checking out code, setting up the Python environment, running the sync script, and committing changes back to the repository.

## Replication Steps

Follow these steps to replicate the process in your own project:

### Set Up

Copy this in your terminal to clone plone/documentation

```bash
 git clone `<repository-url>`

 pip install -q -r requirements-initial.txt

 pip install -q -r requirements.txt
```

### Global Configuration

1. **PUBLIC_URL:**
    - Set the URL of your website
2. **API Key:**
    - Obtain the API key from your nuclia Knowledge Box.
3. **Knowledge Base URL:**
    - Set up the variable to define the Nuclia knowledge box URL.

### Indexing and Syncing

1. **Generate Nuclia Sync Data:**

    ```bash
    python3 upload.py
    ```

2. **Sync Documents:**

- Run the `sync` function to upload, update, or delete documents in Nuclia.

### GitHub Actions

- **Workflow Setup:**
     Modify the GitHub Actions workflow `nuclia_sync.yml` to match your repository structure.

>## Usage Notes
>
>- Ensure that the API key and knowledge base URL are correctly configured.
>- Regularly update the sync process to keep the knowledge base up to date.
>- Troubleshoot issues by checking API key validity and document URLs.

### Conclusion

Replacing Sphinx search with Nuclia search brings improved search functionality to Plone sites. Feel free to reach out for assistance or clarification on any aspect of this documentation.

Happy syncing and searching!
