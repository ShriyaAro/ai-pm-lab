\## dbt-core-01

Tracking risk: No (dbt transforms warehouse data; nothing about collection changes)

Data collection changes: none

Reporting changes: catalog.json was silently skipped on `dbt build --write-catalog`; now fixed

Other changes: Python 3.10 now supported; fix for false "TableNotFound" errors during analyze; new test helpers (internal)

Most important change: catalog.json is written again (it was silently missing)



\## dbt-core-02

Tracking risk: None (dbt doesn’t collect data), but the ClickHouse default change could affect reports.)

Data collection changes: None

Reporting changes:New ClickHouse driver

Other changes: AI assiatant for dbt code, DB metric view materialization, Compiled SQL output in quiet mode, Docs website fix, Product name change in command line

Most important change: ClickHouse teams- dbt new connection driver





\## segment-analytics-next-03

Tracking risk: Yes, It only affects visitors whose stores disagree- cookie now always win

Data collection changes: cookie always wins-the resync of every store, 

Reporting changes: before and after the upgrade will impact the numbers in case of visitors \& sessions

Other changes: If someone had set the option to false, that’s now ignored.

Most important change: AnonymousId collection no longer opt-in 



\## segment-analytics-next-04

Tracking risk: Yes, email recognition changed automatically; values may be classified differently downstream.

Data collection changes:  stricter email detection- collection method change

Reporting changes:  stricter email detection

Other changes: New optional setting (off by default): cookie wins anonymousId conflicts if enabled.

Most important change: Stricter email detection 

