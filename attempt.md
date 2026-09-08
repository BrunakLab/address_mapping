# Geographical code mapping


``` r
info_file <- Sys.getenv("QUARTO_EXECUTE_INFO")
info <- fromJSON(info_file)
print(info)
```

    $`document-path`
    [1] "/home/jenswaaben/phd/software/adress_mapping/attempt.qmd"

    $format
    $format$identifier
    $format$identifier$`display-name`
    [1] "Github (GFM)"

    $format$identifier$`target-format`
    [1] "gfm"

    $format$identifier$`base-format`
    [1] "gfm"


    $format$execute
    $format$execute$`fig-width`
    [1] 7

    $format$execute$`fig-height`
    [1] 5

    $format$execute$`fig-format`
    [1] "retina"

    $format$execute$`fig-dpi`
    [1] 300

    $format$execute$`df-print`
    [1] "default"

    $format$execute$error
    [1] FALSE

    $format$execute$eval
    [1] TRUE

    $format$execute$cache
    NULL

    $format$execute$freeze
    [1] FALSE

    $format$execute$echo
    [1] TRUE

    $format$execute$output
    [1] TRUE

    $format$execute$warning
    [1] TRUE

    $format$execute$include
    [1] TRUE

    $format$execute$`keep-md`
    [1] FALSE

    $format$execute$`keep-ipynb`
    [1] FALSE

    $format$execute$ipynb
    NULL

    $format$execute$enabled
    NULL

    $format$execute$daemon
    NULL

    $format$execute$`daemon-restart`
    [1] FALSE

    $format$execute$debug
    [1] FALSE

    $format$execute$`ipynb-filters`
    list()

    $format$execute$`ipynb-shell-interactivity`
    NULL

    $format$execute$`plotly-connected`
    [1] TRUE


    $format$render
    $format$render$`keep-tex`
    [1] FALSE

    $format$render$`keep-typ`
    [1] FALSE

    $format$render$`keep-source`
    [1] FALSE

    $format$render$`keep-hidden`
    [1] FALSE

    $format$render$`prefer-html`
    [1] FALSE

    $format$render$`output-divs`
    [1] FALSE

    $format$render$`output-ext`
    [1] "md"

    $format$render$`fig-align`
    [1] "default"

    $format$render$`fig-pos`
    NULL

    $format$render$`fig-env`
    NULL

    $format$render$`code-fold`
    [1] "none"

    $format$render$`code-overflow`
    [1] "scroll"

    $format$render$`code-link`
    [1] FALSE

    $format$render$`code-line-numbers`
    [1] FALSE

    $format$render$`code-tools`
    [1] FALSE

    $format$render$`tbl-colwidths`
    [1] TRUE

    $format$render$`merge-includes`
    [1] TRUE

    $format$render$`inline-includes`
    [1] FALSE

    $format$render$`preserve-yaml`
    [1] FALSE

    $format$render$`latex-auto-mk`
    [1] TRUE

    $format$render$`latex-auto-install`
    [1] TRUE

    $format$render$`latex-clean`
    [1] TRUE

    $format$render$`latex-min-runs`
    [1] 1

    $format$render$`latex-max-runs`
    [1] 10

    $format$render$`latex-makeindex`
    [1] "makeindex"

    $format$render$`latex-makeindex-opts`
    list()

    $format$render$`latex-tlmgr-opts`
    list()

    $format$render$`latex-input-paths`
    list()

    $format$render$`latex-output-dir`
    NULL

    $format$render$`link-external-icon`
    [1] FALSE

    $format$render$`link-external-newwindow`
    [1] FALSE

    $format$render$`self-contained-math`
    [1] FALSE

    $format$render$`format-resources`
    list()

    $format$render$variant
    [1] "+autolink_bare_uris+emoji+footnotes+gfm_auto_identifiers+pipe_tables+strikeout+task_lists+tex_math_dollars"


    $format$pandoc
    $format$pandoc$standalone
    [1] TRUE

    $format$pandoc$`default-image-extension`
    [1] "png"

    $format$pandoc$to
    [1] "commonmark"


    $format$language
    $format$language$`toc-title-document`
    [1] "Table of contents"

    $format$language$`toc-title-website`
    [1] "On this page"

    $format$language$`related-formats-title`
    [1] "Other Formats"

    $format$language$`related-notebooks-title`
    [1] "Notebooks"

    $format$language$`source-notebooks-prefix`
    [1] "Source"

    $format$language$`other-links-title`
    [1] "Other Links"

    $format$language$`code-links-title`
    [1] "Code Links"

    $format$language$`launch-dev-container-title`
    [1] "Launch Dev Container"

    $format$language$`launch-binder-title`
    [1] "Launch Binder"

    $format$language$`article-notebook-label`
    [1] "Article Notebook"

    $format$language$`notebook-preview-download`
    [1] "Download Notebook"

    $format$language$`notebook-preview-download-src`
    [1] "Download Source"

    $format$language$`notebook-preview-back`
    [1] "Back to Article"

    $format$language$`manuscript-meca-bundle`
    [1] "MECA Bundle"

    $format$language$`section-title-abstract`
    [1] "Abstract"

    $format$language$`section-title-appendices`
    [1] "Appendices"

    $format$language$`section-title-footnotes`
    [1] "Footnotes"

    $format$language$`section-title-references`
    [1] "References"

    $format$language$`section-title-reuse`
    [1] "Reuse"

    $format$language$`section-title-copyright`
    [1] "Copyright"

    $format$language$`section-title-citation`
    [1] "Citation"

    $format$language$`appendix-attribution-cite-as`
    [1] "For attribution, please cite this work as:"

    $format$language$`appendix-attribution-bibtex`
    [1] "BibTeX citation:"

    $format$language$`appendix-view-license`
    [1] "View License"

    $format$language$`title-block-author-single`
    [1] "Author"

    $format$language$`title-block-author-plural`
    [1] "Authors"

    $format$language$`title-block-affiliation-single`
    [1] "Affiliation"

    $format$language$`title-block-affiliation-plural`
    [1] "Affiliations"

    $format$language$`title-block-published`
    [1] "Published"

    $format$language$`title-block-modified`
    [1] "Modified"

    $format$language$`title-block-keywords`
    [1] "Keywords"

    $format$language$`callout-tip-title`
    [1] "Tip"

    $format$language$`callout-note-title`
    [1] "Note"

    $format$language$`callout-warning-title`
    [1] "Warning"

    $format$language$`callout-important-title`
    [1] "Important"

    $format$language$`callout-caution-title`
    [1] "Caution"

    $format$language$`code-summary`
    [1] "Code"

    $format$language$`code-tools-menu-caption`
    [1] "Code"

    $format$language$`code-tools-show-all-code`
    [1] "Show All Code"

    $format$language$`code-tools-hide-all-code`
    [1] "Hide All Code"

    $format$language$`code-tools-view-source`
    [1] "View Source"

    $format$language$`code-tools-source-code`
    [1] "Source Code"

    $format$language$`tools-share`
    [1] "Share"

    $format$language$`tools-download`
    [1] "Download"

    $format$language$`code-line`
    [1] "Line"

    $format$language$`code-lines`
    [1] "Lines"

    $format$language$`copy-button-tooltip`
    [1] "Copy to Clipboard"

    $format$language$`copy-button-tooltip-success`
    [1] "Copied!"

    $format$language$`repo-action-links-edit`
    [1] "Edit this page"

    $format$language$`repo-action-links-source`
    [1] "View source"

    $format$language$`repo-action-links-issue`
    [1] "Report an issue"

    $format$language$`back-to-top`
    [1] "Back to top"

    $format$language$`search-no-results-text`
    [1] "No results"

    $format$language$`search-matching-documents-text`
    [1] "matching documents"

    $format$language$`search-copy-link-title`
    [1] "Copy link to search"

    $format$language$`search-hide-matches-text`
    [1] "Hide additional matches"

    $format$language$`search-more-match-text`
    [1] "more match in this document"

    $format$language$`search-more-matches-text`
    [1] "more matches in this document"

    $format$language$`search-clear-button-title`
    [1] "Clear"

    $format$language$`search-text-placeholder`
    [1] ""

    $format$language$`search-detached-cancel-button-title`
    [1] "Cancel"

    $format$language$`search-submit-button-title`
    [1] "Submit"

    $format$language$`search-label`
    [1] "Search"

    $format$language$`toggle-section`
    [1] "Toggle section"

    $format$language$`toggle-sidebar`
    [1] "Toggle sidebar navigation"

    $format$language$`toggle-dark-mode`
    [1] "Toggle dark mode"

    $format$language$`toggle-reader-mode`
    [1] "Toggle reader mode"

    $format$language$`toggle-navigation`
    [1] "Toggle navigation"

    $format$language$`crossref-fig-title`
    [1] "Figure"

    $format$language$`crossref-tbl-title`
    [1] "Table"

    $format$language$`crossref-lst-title`
    [1] "Listing"

    $format$language$`crossref-thm-title`
    [1] "Theorem"

    $format$language$`crossref-lem-title`
    [1] "Lemma"

    $format$language$`crossref-cor-title`
    [1] "Corollary"

    $format$language$`crossref-prp-title`
    [1] "Proposition"

    $format$language$`crossref-cnj-title`
    [1] "Conjecture"

    $format$language$`crossref-def-title`
    [1] "Definition"

    $format$language$`crossref-exm-title`
    [1] "Example"

    $format$language$`crossref-exr-title`
    [1] "Exercise"

    $format$language$`crossref-ch-prefix`
    [1] "Chapter"

    $format$language$`crossref-apx-prefix`
    [1] "Appendix"

    $format$language$`crossref-sec-prefix`
    [1] "Section"

    $format$language$`crossref-eq-prefix`
    [1] "Equation"

    $format$language$`crossref-lof-title`
    [1] "List of Figures"

    $format$language$`crossref-lot-title`
    [1] "List of Tables"

    $format$language$`crossref-lol-title`
    [1] "List of Listings"

    $format$language$`environment-proof-title`
    [1] "Proof"

    $format$language$`environment-remark-title`
    [1] "Remark"

    $format$language$`environment-solution-title`
    [1] "Solution"

    $format$language$`listing-page-order-by`
    [1] "Order By"

    $format$language$`listing-page-order-by-default`
    [1] "Default"

    $format$language$`listing-page-order-by-date-asc`
    [1] "Oldest"

    $format$language$`listing-page-order-by-date-desc`
    [1] "Newest"

    $format$language$`listing-page-order-by-number-desc`
    [1] "High to Low"

    $format$language$`listing-page-order-by-number-asc`
    [1] "Low to High"

    $format$language$`listing-page-field-date`
    [1] "Date"

    $format$language$`listing-page-field-title`
    [1] "Title"

    $format$language$`listing-page-field-description`
    [1] "Description"

    $format$language$`listing-page-field-author`
    [1] "Author"

    $format$language$`listing-page-field-filename`
    [1] "File Name"

    $format$language$`listing-page-field-filemodified`
    [1] "Modified"

    $format$language$`listing-page-field-subtitle`
    [1] "Subtitle"

    $format$language$`listing-page-field-readingtime`
    [1] "Reading Time"

    $format$language$`listing-page-field-wordcount`
    [1] "Word Count"

    $format$language$`listing-page-field-categories`
    [1] "Categories"

    $format$language$`listing-page-minutes-compact`
    [1] "{0} min"

    $format$language$`listing-page-category-all`
    [1] "All"

    $format$language$`listing-page-no-matches`
    [1] "No matching items"

    $format$language$`listing-page-words`
    [1] "{0} words"

    $format$language$`listing-page-filter`
    [1] "Filter"

    $format$language$draft
    [1] "Draft"


    $format$metadata
    $format$metadata$title
    [1] "Geographical code mapping"

    $format$metadata$format
    $format$metadata$format$gfm
    named list()

    $format$metadata$format$html
    named list()


    $format$metadata$project
    named list()

``` r
# Access document path
info$`document-path`
```

    [1] "/home/jenswaaben/phd/software/adress_mapping/attempt.qmd"

``` r
# Access format information
info$format$identifier$`target-format`
```

    [1] "gfm"
