# Replacing Sphinx Search with Nuclia Search in Plone

## Overview

This documentation outlines the process of replacing Sphinx search in a Plone site with Nuclia search. The goal is to explain the approach taken and provide instructions for replicating the process in another project.

## Approach

To achieve the transition from Sphinx to Nuclia search, we took an approach as shown in the following generalized outline.

1. Generate Nuclia sync data

    -   Iterate through `.md` files in the repository [docs](https://github.com/plone/documentation/tree/6.0/docs) .
    -   Calculate the hash of each file and store the mapping in `nuclia_sync.json`.

2. Extract Headings

    -   Use regular expressions to extract headings from Markdown files.
    -   Store the extracted headings and slugs for document URLs.

3. Upload Documents

    -   Utilize the `NucliaUpload` class from the `nuclia` SDK.
    -   Generated slugs, Extracted headings, Nuclia `API_KEY` and constructed URLs for `.md` can be passed in the class method.

4. Synchronize Documents

    -   Compare hashes to determine whether to upload, update, or delete documents, when changes are made.
    -   Handle document deletions using the `NucliaKB` class.

5. GitHub Actions Workflow

    -   Created a synchronization workflow triggered by a `push` event.
    -   Defined the steps for checking out code, setting up the Python environment, running the sync script, and committing changes back to the repository.

## Replication steps

Follow these steps to replicate the process in your own project:

### Pre-requisites

-   See [installation](https://6.docs.plone.org/install/index.html) for requirements to build Plone 6 Documentation.
-   See `Training <inv:training:std:lable:installation>` for requirements to build Plone Training.

### Global configuration for `upload.py`

1.  `PUBLIC_URL`
    -   Set the URL of your website.

2.  `API Key`
    -   Set this variable with the API key of your knowledge box.

3.  `KB`
    -   Set up this variable with your knowledge box URL.

### Indexing and syncing

1.  Generate Sync Document

    -   Make sure to create a `json` file and replace each path of `json` file being read or written inside `upload` script with the path of your `json` file.
    -   Fill the `json` with content as given below this is essential for syncing old and new data.

        ```json
        {
            "docs" : {

            }
        }
        ```

2.  Populate Sync Document

    -   Running the `upload` script will now eventually handle the syncing and indexing to the knowledge box.    

     ```bash
     python3 upload.py
     ```

### Integrating the widget

-   Nuclia provides with it's own widget code for our use. 

-   Choose the functionalities you want your widget to have from the widget generator tab. 

-   You will be provided with a code snippet from nuclia which can be used for integration.

-   To perform style changes to the widget you may have to use CSS or other alternatives.

### GitHub Actions

Modify the GitHub Actions workflow `nuclia_sync.yml` to match your repository structure.

## Usage notes

-   Ensure that the API key and knowledge box URL are correctly configured.
-   Troubleshoot issues by checking the API key validity and document URLs.

## Conclusion

Replacing Sphinx search with Nuclia search brings improved search functionality to Plone sites.
Feel free to reach out for assistance or clarification on any aspect of this documentation.
Happy syncing and searching!
