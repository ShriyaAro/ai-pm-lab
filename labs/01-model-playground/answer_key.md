\## dbt-core-01

Tracking risk: No

Data collection changes:No

Reporting changes:Yes

Other changes:Yes

Most important change:`dbt build 'write-catalog` writes `catalog.json` again; since the preview that shipped #13328 the implied index default for build/check overrode the explicit flag and the catalog was silently skipped.



