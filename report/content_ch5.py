"""Chapter Five: Discussion, Conclusion and Recommendations."""

CHAPTER_FIVE = [
    ("chapter", "CHAPTER FIVE", "DISCUSSION, CONCLUSION AND RECOMMENDATIONS"),

    ("h2", "5.1", "Introduction"),
    ("p", "This chapter interprets the results reported in Chapter Four and draws the "
          "study to a close. Section 5.2 summarises what was found. Section 5.3 "
          "interprets those findings. Section 5.4 assesses each objective stated in "
          "Section 1.4 against the evidence. Section 5.5 compares the system with those "
          "reviewed in Chapter Two, and Section 5.6 states its advantages. Section 5.7 "
          "records the challenges encountered. Sections 5.8 and 5.9 state the "
          "implications and the contribution of the study. Section 5.10 concludes and "
          "Section 5.11 recommends further work."),

    ("h2", "5.2", "Summary of Findings"),
    ("p", "The study set out to determine whether the administrative and communication "
          "failures identified in Chapter One could be addressed by a system that "
          "unifies academic and financial records within a single term-scoped data model "
          "and enforces institutional rules in software rather than by human vigilance. "
          "A system realising that design was built and evaluated, and the following "
          "findings emerged."),
    ("p", "First, the correctness rules that administrators presently enforce by "
          "attention proved to be expressible as machine-checkable invariants without "
          "exception. Every rule elicited during requirements gathering, including the "
          "assessment weight budget, the room allocation constraint, the deletion "
          "restrictions on records with dependants, the overpayment prohibition and the "
          "uniqueness of a registration within a term, was implemented and shown by test "
          "to reject the operations it was intended to reject. No rule was encountered "
          "that required human judgement and therefore resisted encoding."),
    ("p", "Second, the guarantee of exactly-once effect for repeated operations was "
          "obtained economically. Four uniqueness constraints, listed in Table 4.2, "
          "deliver idempotency for registration, register marking, score entry and "
          "notification dispatch. The corresponding service-layer checks make the "
          "behaviour graceful rather than merely safe, but the guarantee itself rests on "
          "the database and therefore survives a defect in the service layer."),
    ("p", "Third, the architectural separation held under test. The routers contain no "
          "domain logic, with the consequence that no rule can be bypassed by entering "
          "the system through a different endpoint, and the two domain exceptions "
          "translate into the whole system's status-code semantics through nine lines of "
          "code."),
    ("p", "Fourth, the treatment of ungraded assessments proved to be a substantive "
          "design decision rather than a detail. Normalising the weighted result over "
          "the weight actually graded produces a defensible mid-semester standing where "
          "the conventional computation produces a misleading one, and converges on the "
          "conventional value once grading is complete."),
    ("p", "Fifth, term scoping proved to be the decision on which the coherence of the "
          "model rests. Because enrolments, timetable slots, assessments, fee structures "
          "and invoices all carry a term identifier, the same course can be run, graded "
          "and billed in successive semesters without the records of one contaminating "
          "another, and any past semester can be reconstructed exactly."),

    ("h2", "5.3", "Interpretation of Results"),
    ("p", "The interpretation that the study supports is that the failures described in "
          "Chapter One are not failures of diligence but failures of architecture. The "
          "duplicate invoice, the assessment scheme summing to one hundred and ten "
          "percent, the double-booked lecture room and the reminder sent three days late "
          "are all instances of a rule that everyone knows being violated because nothing "
          "checks it. Where the check exists and is placed on the path that every "
          "mutation must traverse, the violation becomes impossible rather than merely "
          "unlikely, and the reliability of the record ceases to depend on the attention "
          "of the person operating it."),
    ("p", "This bears directly on the common assumption that digitisation is itself the "
          "remedy. It is not. A spreadsheet is already digital, and the assessment "
          "weightings in it still fail to sum correctly. What distinguishes the system "
          "built here from the spreadsheet it replaces is not that the data are in a "
          "database but that the rules are executable and are positioned where they "
          "cannot be circumvented. A database with no constraints and validation "
          "scattered through the user interface would reproduce the spreadsheet's "
          "failure mode at greater speed and with more authority."),
    ("p", "The placement of those rules is therefore the substantive claim, and it is "
          "the claim that the router inspection in Section 4.11 substantiates. Because "
          "the dashboard reaches the domain only through the same interface that any "
          "other client would use, the dashboard holds no privileged path into the data, "
          "and the system's correctness does not depend on the dashboard being the only "
          "way in. This is what makes the guarantee durable under the change that "
          "institutional systems reliably undergo: the addition of a bulk import, a "
          "mobile application, an integration with another system, or a script written "
          "by an administrator in a hurry."),
    ("p", "The idempotency results admit a similar interpretation. It is tempting to "
          "regard exactly-once behaviour as a refinement to be added once the system "
          "works, but the evidence here is that it is inseparable from the operations "
          "themselves. A billing run is not a correct billing run that additionally "
          "happens to be idempotent; a billing run that duplicates invoices when retried "
          "is simply incorrect, because retries are a normal consequence of timeouts and "
          "interruptions rather than an exceptional event. The same holds of the "
          "notification cycle, which by design executes far more often than the "
          "granularity of the rule it evaluates and would therefore send a reminder on "
          "every scan interval were the guard absent."),
    ("p", "Finally, the grading result illustrates that a computation may be "
          "arithmetically correct and practically useless. Aggregating over the full "
          "declared weight is not a mistake in arithmetic; it is a mistake about what "
          "the number is for. A mid-semester standing exists to tell a lecturer which "
          "students are struggling, and a computation that reports a student with full "
          "marks in everything graded so far as failing cannot serve that purpose. This "
          "kind of requirement is not discoverable by reasoning about the specification "
          "in advance; it was found by building the computation, looking at its output "
          "on real-shaped data, and recognising the output as wrong, which is an "
          "argument for the iterative process adopted in Section 3.2.3."),

    ("h2", "5.4", "Achievement of Objectives"),
    ("p", "Each objective stated in Section 1.4 is assessed below against the evidence "
          "reported in Chapter Four."),
    ("p", "The first objective, to analyse institutional record-keeping and "
          "communication processes and derive requirements from them, was achieved. "
          "Documentary analysis, staff interviews and review of existing systems, as "
          "described in Section 3.2.2, produced the twenty-seven functional requirements "
          "of Table 3.1, the ten non-functional requirements of Table 3.2 and the user "
          "stories of Table 3.3. The requirements are traceable to institutional "
          "practice rather than assumed, and the invariants among them were derived "
          "specifically from the failures staff reported."),
    ("p", "The second objective, to design a normalised term-scoped data model and a "
          "layered architecture sharing a single source of truth, was achieved. The "
          "model of Figure 3.4 comprises fifteen tables in third normal form, in which "
          "the enrolment mediates between students and courses within a term and "
          "attendance and assessment records attach to the enrolment rather than to the "
          "student and course separately. The architecture of Figure 3.2 separates "
          "routing, domain logic and data access, and the separation was verified by "
          "inspection in Section 4.11."),
    ("p", "The third objective, to implement the system with institutional rules encoded "
          "as enforced invariants, was achieved. Eleven modules were implemented across "
          "the layers, exposing the interface documented in Appendix B, with every rule "
          "of Table 3.1 implemented in the service layer and reinforced where "
          "expressible by the database constraints of Table 4.2. The test cases marked "
          "with an asterisk in Section 4.8 verify that each invariant refuses the "
          "operations it exists to refuse."),
    ("p", "The fourth objective, to implement automated offset-based notification with "
          "exactly-once delivery, was achieved. The scheduler executes the cycle without "
          "user intervention; offsets are resolved through the three-level fallback of "
          "Section 3.6.1; and the dispatch guard, backed by its uniqueness constraint, "
          "delivers the exactly-once guarantee verified by test cases TC-65 and TC-78. "
          "The qualification stated in Section 1.8 stands: the guarantee was verified by "
          "controlled invocation of the cycle rather than over a genuine multi-week "
          "period."),
    ("p", "The fifth objective, to test and evaluate the system against its "
          "requirements, was achieved. Eighty-two test cases were designed to cover "
          "every functional requirement and every non-functional requirement admitting "
          "discrete verification, with deliberately invalid input supplied wherever a "
          "requirement expresses a prohibition. The results are reported in Section 4.9 "
          "and the traceability of requirements to test cases in Section 4.11."),

    ("h2", "5.5", "Comparison with Existing Systems"),
    ("p", "Table 5.1 compares the implemented system with the classes of system "
          "reviewed in Chapter Two, across the capabilities that Section 2.6 identified "
          "as the gaps this project addresses."),
    ("comparison_table", "5.1", "Comparison of the implemented system with existing systems",
     ["Capability", "Learning management systems", "Commercial student information systems", "Open-source school systems", "Institutional portals", "Kaime"],
     [
         ["Course catalogue and materials", "Full", "Partial", "Partial", "Partial", "Catalogue only; no materials"],
         ["Term-scoped registration", "No", "Yes", "Limited", "Varies", "Yes"],
         ["Timetabling with clash detection", "No", "Yes", "Partial", "Rare", "Yes"],
         ["Attendance with rate computation", "Partial", "Yes", "Yes", "Rare", "Yes"],
         ["Weighted grading and grade point average", "Yes", "Yes", "Partial", "Partial", "Yes"],
         ["Defensible mid-semester standings", "No", "Rare", "No", "No", "Yes"],
         ["Fee structures and billing", "No", "Yes", "Yes", "Partial", "Yes"],
         ["Idempotent bulk operations", "Not stated", "Varies", "Not stated", "Rare", "Yes, by construction"],
         ["Automated offset-based notification", "Partial", "Partial", "Rare", "Manual", "Yes"],
         ["Exactly-once delivery guarantee", "Not stated", "Not stated", "No", "No", "Yes, constraint-backed"],
         ["Rules single-sourced in a service layer", "Varies", "Varies", "Varies", "Rarely", "Yes, verified"],
         ["Licensing cost", "None", "High", "None", "Development cost", "None"],
         ["Learning content delivery", "Full", "Partial", "Partial", "No", "Out of scope"],
         ["Admissions and human resources", "No", "Yes", "Partial", "Partial", "Out of scope"],
         ["Student self-service portal", "Yes", "Yes", "Yes", "Yes", "Out of scope"],
     ]),
    ("p", "The comparison should be read with its limits in view. The implemented "
          "system is narrower than every commercial student information system in the "
          "table: it has no admissions module, no human-resource management, no hostel "
          "or library function and no student-facing portal, and a mature commercial "
          "product has been hardened by years of operation across many institutions in a "
          "way that a single academic year's work cannot match. The claim advanced here "
          "is not that the system is more capable, but that within the scope it does "
          "cover it closes the four specific gaps of Section 2.6, and does so at no "
          "licensing cost and at a complexity a single department can operate."),

    ("h2", "5.6", "Advantages of the New System"),
    ("p", "Six advantages follow from the design and are supported by the evaluation."),
    ("p", "The first is a single source of truth. Because the academic and financial "
          "domains share one database, a student registered once is available to "
          "enrolment, grading, billing and notification without re-entry, and the "
          "reconciliation between separate academic and financial systems is eliminated "
          "rather than automated."),
    ("p", "The second is the mechanical enforcement of rules. Duplicate registrations, "
          "over-budget assessment schemes, room clashes, overpayments and the deletion of "
          "records with live dependants are refused at the point of attempt, with a "
          "message stating the reason, rather than being discovered during reconciliation "
          "or not at all."),
    ("p", "The third is safety under repetition. Every bulk operation may be retried "
          "after an interruption without duplicating its effect, which converts an "
          "interrupted billing run from an incident requiring manual reversal into an "
          "operation the operator simply repeats."),
    ("p", "The fourth is automated and auditable communication. Reminders are dispatched "
          "on a declared schedule without staff intervention, and the dispatch history "
          "records what was sent to whom, when, and with what outcome, including "
          "failures, so that the question of whether a student was informed has an "
          "answer."),
    ("p", "The fifth is the defensibility of derived figures. An attendance rate "
          "computed from recorded sittings, and a result computed from declared "
          "weightings with the graded proportion reported alongside it, are auditable in "
          "a way that a handwritten register and a private spreadsheet are not."),
    ("p", "The sixth is cost and extensibility. The system is built entirely on "
          "open-source components with no licensing cost, deploys as a single process, "
          "and exposes a documented interface through which additional clients can be "
          "built without re-implementing any rule."),

    ("h2", "5.7", "Challenges Encountered"),
    ("p", "Several difficulties were encountered and are recorded here because their "
          "resolution shaped the system."),
    ("p", "The most consequential was the treatment of partially graded courses, "
          "discussed in Sections 3.6.2 and 5.3. The first implementation aggregated over "
          "the full declared weight and produced mid-semester standings that were "
          "arithmetically correct and practically worthless. Recognising the defect "
          "required looking at the output on realistic data rather than reasoning about "
          "the specification, and resolving it required reconsidering what the number "
          "was for."),
    ("p", "The second was determining where each rule belongs. Some invariants, such as "
          "the uniqueness of a course code, are naturally expressed as database "
          "constraints. Others, such as the assessment weight budget, require aggregation "
          "across rows and are naturally expressed in the service layer. Others still, "
          "such as the room clash, could be expressed in either place, and the decision "
          "to place them in the service layer was taken so that the rejection message "
          "could name the conflicting booking, which a constraint violation cannot do. "
          "Arriving at a consistent principle, namely that the service layer owns rules "
          "requiring explanation and the database owns rules requiring guarantee, took "
          "several iterations."),
    ("p", "The third was the testing of time-dependent behaviour. Reminder offsets are "
          "expressed in days, and verifying a seven-day, three-day, one-day and same-day "
          "sequence in real time would consume a week per test case. The resolution was "
          "to make the processing cycle accept the current time as a parameter and to "
          "expose it as an internal endpoint, so that the logic could be exercised "
          "against controlled dates. This is a partial resolution, as Section 1.8 notes: "
          "it verifies the dispatch logic thoroughly but does not exercise the scheduler "
          "over a genuine multi-week period."),
    ("p", "The fourth was the design of bulk operations. Marking a register or entering "
          "an assessment's scores concerns many records at once, and the question of "
          "what should happen when one entry in a submission is invalid admits two "
          "answers. Accepting the valid entries and reporting the invalid ones leaves the "
          "operator with a partially marked register and no clear picture of what was "
          "recorded. The alternative, adopted here, validates the entire submission "
          "before persisting any part of it, so that a submission either takes effect "
          "completely or not at all."),
    ("p", "The fifth was schema evolution. Requirements discovered during later "
          "increments required changes to tables that earlier increments already "
          "depended on. Maintaining every change as an Alembic migration rather than "
          "altering the schema directly made these changes safe and reversible, at the "
          "cost of discipline in a phase of the work where direct alteration is "
          "continually tempting."),

    ("h2", "5.8", "Implications of the Study"),
    ("p", "For institutional practice, the study implies that the recurring "
          "administrative errors described in Chapter One are addressable by design "
          "rather than by exhortation. Instructing staff to check assessment weightings "
          "more carefully is a weaker intervention than a system that refuses an "
          "over-budget scheme, because the former depends on sustained attention and the "
          "latter does not. Institutions procuring or commissioning administrative "
          "software might reasonably ask not only what a system stores but which rules it "
          "refuses to let them break."),
    ("p", "For system procurement, the study implies that the integration of academic "
          "and financial data is not a convenience but a determinant of correctness. Fee "
          "liability is determined by programme, level and term; where those attributes "
          "live in a different system from the billing, they must be copied, and copies "
          "diverge. This is an argument for a shared model rather than for interfaces "
          "between separate models."),
    ("p", "For software practice in comparable projects, the study implies that "
          "idempotency and constraint placement are design-time concerns rather than "
          "later refinements. The four uniqueness constraints of Table 4.2 were "
          "inexpensive to declare while the tables were being designed and would have "
          "been considerably more troublesome to introduce afterwards, against data "
          "already containing the duplicates they prohibit."),
    ("p", "For students, the implication is a change in the reliability of institutional "
          "communication. A reminder delivered on a declared schedule, whose delivery is "
          "recorded, is a different kind of service from an announcement whose arrival "
          "depends on a member of staff remembering and on the student happening to look."),

    ("h2", "5.9", "Contribution of the Project"),
    ("p", "The principal contribution of this project is the artefact itself: a working, "
          "documented, openly licensed school management and notification system "
          "covering terms, students, courses, enrolment, timetabling, attendance, "
          "grading, fees and automated communication, deployable by a department or "
          "small institution at no licensing cost."),
    ("p", "Beyond the artefact, the study contributes a design position that the "
          "evaluation substantiates: that in an institutional records system the "
          "correctness rules should be enumerated explicitly, implemented once in a "
          "service layer through which every mutation passes, and reinforced by database "
          "constraints wherever they are expressible as uniqueness or referential "
          "conditions. The corollary, verified here by inspection, is that no rule should "
          "reside in a user interface, because a rule in a user interface is absent from "
          "every other path into the data."),
    ("p", "The study contributes, more specifically, the term-scoped model of Figure "
          "3.4, in which the enrolment mediates between the durable student and course "
          "entities and the time-bound records of attendance and assessment attach to it. "
          "This structure makes it impossible to record a mark for an unregistered "
          "student and makes any past semester exactly reconstructible, and is "
          "transferable to other institutional systems independently of the "
          "implementation reported here."),
    ("p", "Finally, the study contributes the normalising treatment of partially graded "
          "courses described in Section 3.6.2, together with the practice of reporting "
          "the graded proportion alongside the resulting percentage, which addresses a "
          "real and commonly mishandled requirement in academic records systems."),

    ("h2", "5.10", "Conclusion"),
    ("p", "This study set out to design, implement and evaluate an integrated web-based "
          "school management and automated notification system, in response to the "
          "fragmentation of institutional records and the unreliability of institutional "
          "communication described in Chapter One. That aim was achieved. A system of "
          "fifteen tables and eleven functional modules was designed following the Design "
          "Science Research paradigm, implemented through iterative and incremental "
          "development as a three-tier application with a strictly layered application "
          "tier, and evaluated against twenty-seven functional and ten non-functional "
          "requirements by means of eighty-two test cases."),
    ("p", "The evidence supports three conclusions. The institutional rules that are "
          "presently enforced by human vigilance can be expressed without exception as "
          "machine-checkable invariants, and once so expressed they are violated no "
          "longer. Exactly-once behaviour under repetition can be obtained economically "
          "by treating uniqueness constraints as idempotency keys, and is a precondition "
          "of correctness rather than an optional refinement in any system whose "
          "operations may be retried. And scoping every academic and financial "
          "association to an academic term, with the enrolment as the hinge of the "
          "model, yields records that remain independently accurate across successive "
          "semesters."),
    ("p", "The conclusions are bounded by the limitations stated in Section 1.8 and "
          "restated here without qualification. The system was evaluated functionally "
          "rather than in live institutional operation over a complete semester with "
          "real records; the notification subsystem was exercised through controlled "
          "invocation rather than over a genuine multi-week period; per-role "
          "authorisation of the school-management endpoints remains to be completed; and "
          "the requirements were drawn from a single institutional context. What the "
          "study establishes is that the design behaves as intended under systematic "
          "test, not that it has been proven in service. The recommendations that follow "
          "are directed principally at closing that gap."),

    ("h2", "5.11", "Recommendations for Future Work"),
    ("p", "The following are recommended, in the order in which they should be "
          "undertaken."),
    ("num", "Complete the authorisation layer. The authentication primitives exist, but "
            "the school-management endpoints are not yet constrained by role. Roles "
            "corresponding to the actors of Figure 3.3 should be defined and enforced as "
            "a dependency on each endpoint, so that a lecturer cannot issue invoices and "
            "a finance officer cannot alter grades. This is a precondition for any "
            "deployment beyond a trusted internal network."),
    ("num", "Establish an automated regression test suite. The test cases of Section "
            "4.8 were executed manually. Encoding them as an automated suite executed on "
            "every change would convert them from a record of one evaluation into a "
            "standing guarantee, and is the single change that would most improve the "
            "maintainability of the system."),
    ("num", "Conduct a pilot deployment over a complete semester. Operating the system "
            "with real records for one semester in one department would test the "
            "properties this study could not: sustained data-entry burden, staff "
            "adoption, behaviour at institutional data volumes, and the adequacy of the "
            "error messages under conditions where the operator did not build the system."),
    ("num", "Implement a student self-service portal. Students are presently subjects of "
            "records and recipients of messages. A read-only portal exposing a student's "
            "own enrolments, attendance rate, results and fee balance would use the "
            "existing interface without new domain logic, and would substantially "
            "increase the system's value to its largest constituency."),
    ("num", "Implement a short-message notification channel. The channel abstraction was "
            "designed for this and requires only a new implementation of the interface. "
            "Given the prevalence of mobile telephony relative to electronic mail among "
            "students, this is likely to improve delivery materially. [SOURCE NEEDED: "
            "evidence on mobile telephone versus electronic mail reach among students in "
            "the relevant context]"),
    ("num", "Extend billing to support instalments, scholarships and partial waivers. "
            "The present model bills a single amount per structure per student. "
            "Institutional practice frequently involves payment in instalments across a "
            "semester and bursary awards that reduce liability, neither of which the "
            "current invoice model represents."),
    ("num", "Add reporting and analytics. The system holds the data required for "
            "attendance-risk identification, grade distribution analysis, fee collection "
            "reporting and progression tracking, but presents these only as per-course "
            "and per-student views. Aggregate reporting at programme and institutional "
            "level would serve management decisions the present views cannot."),
    ("num", "Introduce prerequisite and credit-load validation at enrolment. The system "
            "currently permits any active student to enrol in any active course. "
            "Institutional practice imposes prerequisites and minimum and maximum credit "
            "loads per semester, both of which are natural extensions of the enrolment "
            "service and would be enforced by the same mechanism as the existing rules."),
    ("num", "Migrate notification dispatch to a distributed task queue should the "
            "subscriber population grow substantially. The in-process scheduler was "
            "selected in Section 2.4.4 for operational simplicity at the present scale. "
            "The channel abstraction and the orchestration contract were designed so "
            "that this migration would not disturb the logic determining what is sent to "
            "whom."),
]
