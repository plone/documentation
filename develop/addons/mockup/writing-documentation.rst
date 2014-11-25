Writing documentation for Mockup
================================

The documentation for Mockup is automatically generated from comments in
pattern code. The structure is as follows::

    /* PATTERN TITLE
     *
     * Options:
     *    OPTION_TITLE(TYPE): DESCRIPTION
     *
     * Documentation:
     *   # Markdown title
     *
     *   Markdown structured description text
     *
     *   # Example
     *
     *   {{ EXAMPLE_ANCHOR }}
     *
     * Example: EXAMPLE_ANCHOR
     *    <div class="pat-PATTERN_NAME"></div>
     *
     * License:
     *   License text, if it differs from the package's license, which is
     *   declared in package.json.
     *
     */

