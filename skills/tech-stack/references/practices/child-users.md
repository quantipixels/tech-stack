# Apps with child users

Store rules below are quoted from their sources; the rest are our defaults, stricter than the stores. Age thresholds and consent are legal questions: each project records its jurisdictions and their sources.

### Separate child app — default (over one app gated by account type)
setting: when the adult app carries social, commerce or other adult-only features; both apps share one backend and client core
why: our choice, not a store rule; Google's Families policy applies whenever "one of the target audiences for your app is children", and Apple 5.1.4 requires children's privacy compliance from any app able to share a minor's personal information, "the ability to chat" included; a separate app keeps adult features out of that scope and out of the child's reach
verified: 2026-10-23 · https://support.google.com/googleplay/android-developer/answer/9893335 · https://developer.apple.com/app-store/review/guidelines/

### Third-party ads, analytics and crash SDKs in a child app — rejected
setting: analytics first-party and server-side; crash data from App Store Connect and Play Console
why: our default; the stores allow some "in limited cases" (Apple 1.3) and Families requires approved or self-certified SDKs, so each one needs a review of what it sends about a child; none removes that review
verified: 2026-10-23 · https://developer.apple.com/app-store/review/guidelines/ · https://support.google.com/googleplay/android-developer/answer/9893335

### Content-free push to a child's device — default (over payloads that carry message text)
setting: a generic visible alert, then the app syncs over its own connection; the app works without push permission; on the web, show a generic notification for each push and never rely on silent push
why: Apple 4.5.4: push "should not be used to send sensitive personal or confidential information" and "must not be required for the app to function"; Chrome accepts only `userVisibleOnly: true` subscriptions; carrying no content at all is our stricter choice
verified: 2026-10-23 · https://developer.apple.com/app-store/review/guidelines/ · https://web.dev/articles/push-notifications-subscribing-a-user

### Birth month and year — default (over a full date of birth)
setting: collect only the age data the applicable rules need; keep child protections until a threshold is certainly reached (the month after the birth month); configure thresholds per jurisdiction and purpose, each with its source
why: Apple 5.1.4 allows a birthdate "only for the purpose of complying with these statutes"; less data held about a child, and thresholds that differ by country and feature stay configuration
verified: 2026-10-23 · https://developer.apple.com/app-store/review/guidelines/
