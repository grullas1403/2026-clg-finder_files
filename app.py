import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime

st.set_page_config(
    page_title="CampusCompass",
    page_icon="🎓",
    layout="wide"
)

DB = "campuscompass.db"
VISIT_FEE = 49  # Demonstration only; not an official college fee.

COLLEGES = [
    {
        "name": "REVA University",
        "location": "Yelahanka, Bengaluru",
        "type": "Private University",
        "courses": ["Engineering", "CSE", "AI & ML", "Management"],
        "admission": ["Management", "University Admission"],
        "fees": None,
        "website": "https://www.reva.edu.in",
        "about": "Explore engineering, technology and undergraduate programmes."
    },
    {
        "name": "Sapthagiri NPS University",
        "location": "Bengaluru",
        "type": "Private University",
        "courses": ["Engineering", "CSE", "AI & ML"],
        "admission": ["Management", "University Admission"],
        "fees": None,
        "website": "https://snpsu.edu.in",
        "about": "Explore engineering programmes and admission options."
    },
    {
        "name": "Ramaiah University of Applied Sciences",
        "location": "Bengaluru",
        "type": "Private University",
        "courses": ["Engineering", "Management", "Design"],
        "admission": ["University Admission"],
        "fees": None,
        "website": "https://www.msruas.ac.in",
        "about": "Explore applied sciences and professional programmes."
    },
    {
        "name": "Christ University",
        "location": "Bengaluru",
        "type": "Deemed University",
        "courses": ["Engineering", "Science", "Commerce", "Management"],
        "admission": ["University Admission"],
        "fees": None,
        "website": "https://christuniversity.in",
        "about": "Explore undergraduate programmes and campus facilities."
    },
    {
        "name": "Indian Institute of Science (IISc)",
        "location": "CV Raman Road, Bengaluru",
        "type": "Research Institution",
        "courses": ["Science", "Research", "Engineering-related programmes"],
        "admission": ["Programme-specific Admission"],
        "fees": None,
        "website": "https://iisc.ac.in",
        "about": "Check official programme eligibility and admission requirements."
    },
    {
        "name": "Acharya Institutes",
        "location": "Soladevanahalli, Bengaluru",
        "type": "Institution Group",
        "courses": ["Engineering", "CSE", "AI & ML", "Management"],
        "admission": ["KCET", "Management", "Other Entrance"],
        "fees": None,
        "website": "https://www.acharya.ac.in",
        "about": "Explore programmes and campus facilities."
    },
    {
        "name": "St Joseph's University",
        "location": "Bengaluru",
        "type": "University",
        "courses": ["Science", "Commerce", "Arts", "Management"],
        "admission": ["University Admission"],
        "fees": None,
        "website": "https://www.sju.edu.in",
        "about": "Explore undergraduate programmes."
    },
    {
        "name": "Dhanwantari Group of Institutions",
        "location": "Karnataka",
        "type": "Institution Group",
        "courses": ["Verify available programmes"],
        "admission": ["Institution-specific Admission"],
        "fees": None,
        "website": "",
        "about": "Verify the exact institution and available courses."
    },
    {
        "name": "JAIN University",
        "location": "Bengaluru",
        "type": "Deemed University",
        "courses": ["Engineering", "CSE", "Management", "Commerce"],
        "admission": ["University Admission"],
        "fees": None,
        "website": "https://www.jainuniversity.ac.in",
        "about": "Explore professional and undergraduate programmes."
    },
    {
        "name": "PES University",
        "location": "Bengaluru",
        "type": "Private University",
        "courses": ["Engineering", "CSE", "AI & ML", "Management"],
        "admission": ["KCET", "University Entrance", "Other Routes"],
        "fees": None,
        "website": "https://www.pes.edu",
        "about": "Check programme-specific admission requirements."
    },
    {
        "name": "Alliance University",
        "location": "Anekal, Bengaluru",
        "type": "Private University",
        "courses": ["Engineering", "Management", "Law", "Commerce"],
        "admission": ["University Admission"],
        "fees": None,
        "website": "https://www.alliance.edu.in",
        "about": "Explore professional programmes and campus facilities."
    },
    {
        "name": "Presidency University",
        "location": "Bengaluru",
        "type": "Private University",
        "courses": ["Engineering", "CSE", "AI & ML", "Management"],
        "admission": ["University Admission", "Other Routes"],
        "fees": None,
        "website": "https://presidencyuniversity.in",
        "about": "Explore programmes and admission requirements."
    },
    {
        "name": "RR Institutions",
        "location": "Bengaluru",
        "type": "Institution Group",
        "courses": ["Engineering", "CSE", "Health Sciences"],
        "admission": ["KCET", "Management", "Other Routes"],
        "fees": None,
        "website": "https://www.rrinstitutions.com",
        "about": "Check the exact course and admission route."
    },
    {
        "name": "Nitte Meenakshi Institute of Technology",
        "location": "Yelahanka, Bengaluru",
        "type": "Engineering Institution",
        "courses": ["Engineering", "CSE", "AI & ML"],
        "admission": ["KCET", "Management", "Other Entrance"],
        "fees": None,
        "website": "https://nmit.ac.in",
        "about": "Explore engineering programmes and admission requirements."
    },
    {
        "name": "RV University",
        "location": "Bengaluru",
        "type": "Private University",
        "courses": ["Engineering", "CSE", "Design", "Management"],
        "admission": ["University Admission"],
        "fees": None,
        "website": "https://rvu.edu.in",
        "about": "Explore interdisciplinary programmes."
    },
    {
        "name": "New Horizon College of Engineering",
        "location": "Marathahalli, Bengaluru",
        "type": "Engineering Institution",
        "courses": ["Engineering", "CSE", "AI & ML"],
        "admission": ["KCET", "Management", "Other Entrance"],
        "fees": None,
        "website": "https://newhorizonindia.edu",
        "about": "Explore engineering programmes and campus facilities."
    },
    {
        "name": "ABBS",
        "location": "Bengaluru",
        "type": "Institution Group",
        "courses": ["Management", "Commerce", "Other programmes"],
        "admission": ["Institution-specific Admission"],
        "fees": None,
        "website": "https://www.abbs.edu.in",
        "about": "Verify the exact institution and programme."
    },
    {
        "name": "BMS College of Engineering",
        "location": "Basavanagudi, Bengaluru",
        "type": "Engineering Institution",
        "courses": ["Engineering", "CSE", "AI & ML"],
        "admission": ["KCET", "Management", "Other Entrance"],
        "fees": None,
        "website": "https://www.bmsce.ac.in",
        "about": "Check current engineering programmes and admission routes."
    },
    {
        "name": "Meenakshi Academy of Higher Education and Research",
        "location": "Bengaluru",
        "type": "Deemed University",
        "courses": ["Health Sciences", "Other programmes"],
        "admission": ["Programme-specific Admission"],
        "fees": None,
        "website": "https://maher.ac.in",
        "about": "Check available programmes and eligibility."
    }
]


# ---------------- DATABASE ----------------

def connect():
    return sqlite3.connect(DB)


def setup_database():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                college TEXT NOT NULL,
                reviewer TEXT NOT NULL,
                category TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                college TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                route TEXT NOT NULL,
                visit_date TEXT NOT NULL,
                visitors INTEGER NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL
            )
        """)


def get_college(name):
    return next((c for c in COLLEGES if c["name"] == name), None)


def get_reviews(name):
    with connect() as con:
        return pd.read_sql_query(
            """
            SELECT reviewer, category, rating, comment, created_at
            FROM reviews
            WHERE college = ?
            ORDER BY id DESC
            """,
            con,
            params=(name,)
        )


def average_rating(name):
    reviews = get_reviews(name)
    if reviews.empty:
        return None
    return round(float(reviews["rating"].mean()), 1)


def show_card(college):
    rating = average_rating(college["name"])
    rating_text = "No reviews yet" if rating is None else f"{rating}/5"
    fee_text = "Not verified" if college["fees"] is None else f"₹{college['fees']:,}"

    st.markdown(f"""
    <div class="college-card">
        <span class="tag">{college['type']}</span>
        <h3>{college['name']}</h3>
        <p class="muted">📍 {college['location']}</p>
        <p><b>Courses:</b> {", ".join(college['courses'])}</p>
        <p><b>Admission:</b> {", ".join(college['admission'])}</p>
        <p><b>Fees:</b> {fee_text}</p>
        <p><b>Community rating:</b> ⭐ {rating_text}</p>
    </div>
    """, unsafe_allow_html=True)

    if college["website"]:
        st.markdown(f"[Official website ↗]({college['website']})")


setup_database()

# ---------------- PREMIUM DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(145deg, #080d1b, #10182c, #11152b);
    color: #f7f8ff;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid #28344d;
}
h1, h2, h3 { font-family: 'Manrope', sans-serif; }
.hero {
    padding: 34px;
    border-radius: 24px;
    border: 1px solid #424b79;
    background: linear-gradient(120deg, #1a2a4a, #27204a, #121c34);
    margin-bottom: 22px;
}
.hero h1 { font-size: 40px; }
.hero p, .muted { color: #c4cfee; }
.muted { font-size: 13px; }
.tag {
    display: inline-block;
    background: #302b58;
    border: 1px solid #6556a8;
    color: #e2ddff;
    padding: 6px 11px;
    border-radius: 30px;
    font-size: 12px;
}
.college-card {
    padding: 20px;
    margin-bottom: 14px;
    min-height: 230px;
    border-radius: 18px;
    background: linear-gradient(145deg, #1a263f, #11192c);
    border: 1px solid #2e3c59;
}
div.stButton > button {
    border-radius: 10px;
    background: linear-gradient(120deg, #6558d9, #8658ef);
    color: white;
    font-weight: 700;
}
div[data-testid="stMetric"] {
    border: 1px solid #303e5d;
    background: #18233a;
    padding: 14px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------

with st.sidebar:
    st.markdown("# 🎓 CampusCompass")
    st.caption("Discover. Compare. Visit.")
    page = st.radio(
        "MENU",
        [
            "Dashboard",
            "Explore Colleges",
            "College Details",
            "Compare Colleges",
            "Student Reviews",
            "Campus Visit"
        ]
    )
    st.divider()
    st.caption("Verify official information before applying.")


# ---------------- DASHBOARD ----------------

if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <span class="tag">YOUR CAMPUS. YOUR FUTURE.</span>
        <h1>Find a college that fits your ambition.</h1>
        <p>Discover colleges, compare admission routes and plan campus visits.</p>
    </div>
    """, unsafe_allow_html=True)

    with connect() as con:
        visits_count = con.execute(
            "SELECT COUNT(*) FROM visits"
        ).fetchone()[0]
        reviews_count = con.execute(
            "SELECT COUNT(*) FROM reviews"
        ).fetchone()[0]

    a, b, c, d = st.columns(4)
    a.metric("COLLEGES", len(COLLEGES))
    b.metric("REVIEWS", reviews_count)
    c.metric("VISIT REQUESTS", visits_count)
    d.metric("DEMO VISIT FEE", f"₹{VISIT_FEE}")

    st.caption(
        "₹49 is a demonstration value only. It is not an official college charge. "
        "No payment is collected."
    )

    search = st.text_input(
        "Quick search",
        placeholder="Search REVA, CSE, AI & ML..."
    )

    if search:
        matches = [
            c for c in COLLEGES
            if search.lower() in (
                c["name"] + " " + c["location"] + " " +
                " ".join(c["courses"])
            ).lower()
        ]
        st.subheader(f"{len(matches)} matching colleges")
        for i in range(0, len(matches), 2):
            columns = st.columns(2)
            for j, column in enumerate(columns):
                if i + j < len(matches):
                    with column:
                        show_card(matches[i + j])

    st.subheader("Featured colleges")
    featured = [
        get_college("REVA University"),
        get_college("Sapthagiri NPS University"),
        get_college("PES University"),
        get_college("RV University")
    ]

    columns = st.columns(2)
    for i, college in enumerate(featured):
        with columns[i % 2]:
            show_card(college)

    st.info("Confirm fees, course availability and admission eligibility officially.")


# ---------------- EXPLORE COLLEGES ----------------

elif page == "Explore Colleges":
    st.title("Explore Colleges")
    search = st.text_input("Search by college, course or location")

    course_list = sorted({
        course for college in COLLEGES
        for course in college["courses"]
    })

    course_filter = st.selectbox(
        "Course",
        ["All courses"] + course_list
    )

    route_filter = st.selectbox(
        "Admission route",
        [
            "All routes",
            "KCET",
            "Management",
            "University Admission",
            "Other Entrance"
        ]
    )

    matches = []

    for college in COLLEGES:
        searchable = (
            college["name"] + " " + college["location"] + " " +
            college["type"] + " " + " ".join(college["courses"]) + " " +
            " ".join(college["admission"])
        ).lower()

        if search and search.lower() not in searchable:
            continue

        if course_filter != "All courses" and course_filter not in college["courses"]:
            continue

        if route_filter != "All routes" and route_filter not in college["admission"]:
            continue

        matches.append(college)

    st.subheader(f"{len(matches)} matching colleges")

    if not matches:
        st.warning("No results found. Change your search or filters.")

    for i in range(0, len(matches), 2):
        columns = st.columns(2)
        for j, column in enumerate(columns):
            if i + j < len(matches):
                with column:
                    show_card(matches[i + j])


# ---------------- COLLEGE DETAILS ----------------

elif page == "College Details":
    st.title("College Details")
    name = st.selectbox("Select a college", [c["name"] for c in COLLEGES])
    college = get_college(name)

    st.markdown(f"""
    <div class="hero">
        <span class="tag">{college['type']}</span>
        <h1>{college['name']}</h1>
        <p>📍 {college['location']}</p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.subheader("About")
        st.write(college["about"])

        st.subheader("Courses")
        for course in college["courses"]:
            st.write("•", course)

        st.subheader("Official website")
        if college["website"]:
            st.markdown(f"[Open official website]({college['website']})")
        else:
            st.warning("Official website needs verification.")

    with right:
        st.subheader("Admission routes")
        for route in college["admission"]:
            st.write("•", route)

        st.subheader("Fee structure")
        if college["fees"] is None:
            st.warning(
                "Fees have not been verified. Ask the admissions office "
                "for the current course-specific fee structure."
            )
        else:
            st.write(f"₹{college['fees']:,}")

        st.subheader("Faculty and teaching")
        st.write(
            "Independent faculty ratings are not yet available. "
            "Read genuine student reviews and visit the campus."
        )

        st.subheader("Campus visit")
        st.write(
            "Visit requests are not confirmed bookings. Contact the college "
            "to confirm permission and availability."
        )

    st.divider()
    st.subheader("Student reviews")
    reviews = get_reviews(name)

    if reviews.empty:
        st.info("No reviews have been submitted yet.")
    else:
        st.write(f"Average rating: {reviews['rating'].mean():.1f}/5")
        for _, row in reviews.iterrows():
            with st.container(border=True):
                st.write(f"**{row['reviewer']}** · {row['category']}")
                st.write(f"⭐ {row['rating']}/5")
                st.write(row["comment"])
                st.caption(row["created_at"])


# ---------------- COMPARE COLLEGES ----------------

elif page == "Compare Colleges":
    st.title("Compare Colleges")

    names = [c["name"] for c in COLLEGES]

    selected = st.multiselect(
        "Select up to four colleges",
        names,
        default=["REVA University", "Sapthagiri NPS University"],
        max_selections=4
    )

    if len(selected) < 2:
        st.info("Select at least two colleges.")
    else:
        rows = []

        for name in selected:
            college = get_college(name)
            rating = average_rating(name)

            rows.append({
                "College": name,
                "Location": college["location"],
                "Type": college["type"],
                "Courses": ", ".join(college["courses"]),
                "Admission": ", ".join(college["admission"]),
                "Fees": "Not verified" if college["fees"] is None else f"₹{college['fees']:,}",
                "Community rating": "No reviews" if rating is None else f"{rating}/5"
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        st.caption("Missing fee information does not mean a college is cheaper.")


# ---------------- STUDENT REVIEWS ----------------

elif page == "Student Reviews":
    st.title("Student Reviews")
    st.caption("Submit honest reviews based on your own experience.")

    college_name = st.selectbox(
        "College",
        [c["name"] for c in COLLEGES]
    )

    reviewer = st.text_input("Display name")

    category = st.selectbox(
        "Review category",
        [
            "Overall experience",
            "Faculty and teaching",
            "Infrastructure",
            "Placements",
            "Campus life",
            "Admission process",
            "Student support"
        ]
    )

    rating = st.slider("Rating", 1, 5, 4)
    comment = st.text_area("Your review", max_chars=1500)

    st.caption("Do not include private or sensitive information.")

    if st.button("Submit review", use_container_width=True):
        if not reviewer.strip() or not comment.strip():
            st.error("Enter your display name and review.")
        else:
            with connect() as con:
                con.execute(
                    """
                    INSERT INTO reviews
                    (college, reviewer, category, rating, comment, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        college_name,
                        reviewer.strip(),
                        category,
                        int(rating),
                        comment.strip(),
                        datetime.now().isoformat(timespec="seconds")
                    )
                )

            st.success("Review saved successfully.")
            st.rerun()

    st.divider()
    st.subheader("Recent reviews")

    filter_name = st.selectbox(
        "Show reviews for",
        [c["name"] for c in COLLEGES],
        key="review_filter"
    )

    reviews = get_reviews(filter_name)

    if reviews.empty:
        st.info("No reviews available yet.")
    else:
        st.write(
            f"Average rating: {reviews['rating'].mean():.1f}/5 "
            f"({len(reviews)} reviews)"
        )

        for _, row in reviews.iterrows():
            with st.container(border=True):
                st.write(f"**{row['reviewer']}** · {row['category']}")
                st.write(f"⭐ {row['rating']}/5")
                st.write(row["comment"])
                st.caption(row["created_at"])


# ---------------- CAMPUS VISIT ----------------

elif page == "Campus Visit":
    st.title("Plan a Campus Visit")

    st.markdown("""
    <div class="hero">
        <span class="tag">CAMPUS EXPERIENCE</span>
        <h1>Explore before you decide.</h1>
        <p>Prepare questions about fees, faculty, facilities and admissions.</p>
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        f"₹{VISIT_FEE} is a demonstration value only. "
        "No payment is collected. Do not charge visitors without permission."
    )

    with st.form("visit_form"):
        college_name = st.selectbox(
            "Choose college",
            [c["name"] for c in COLLEGES]
        )
        full_name = st.text_input("Full name")
        email = st.text_input("Email")
        phone = st.text_input("Phone number")
        route = st.selectbox(
            "Admission interest",
            [
                "KCET",
                "Management",
                "University Admission",
                "Other entrance",
                "Just exploring"
            ]
        )
        visit_date = st.date_input(
            "Preferred visit date",
            min_value=date.today()
        )
        visitors = st.number_input(
            "Number of visitors",
            min_value=1,
            max_value=10,
            value=1
        )
        notes = st.text_area("Questions for the college")
        consent = st.checkbox(
            "I understand this is a request, not a confirmed booking."
        )
        submitted = st.form_submit_button(
            "Submit visit request",
            use_container_width=True
        )

    if submitted:
        clean_phone = (
            phone.strip()
            .replace("+", "")
            .replace(" ", "")
            .replace("-", "")
        )
        valid_email = "@" in email and "." in email.split("@")[-1]

        if not full_name.strip():
            st.error("Enter your name.")
        elif not valid_email:
            st.error("Enter a valid email address.")
        elif not clean_phone.isdigit() or len(clean_phone) < 10:
            st.error("Enter a valid phone number.")
        elif not consent:
            st.error("Confirm that you understand the booking terms.")
        else:
            with connect() as con:
                cursor = con.execute(
                    """
                    INSERT INTO visits
                    (college, name, email, phone, route, visit_date,
                     visitors, notes, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        college_name,
                        full_name.strip(),
                        email.strip(),
                        phone.strip(),
                        route,
                        visit_date.isoformat(),
                        int(visitors),
                        notes.strip(),
                        datetime.now().isoformat(timespec="seconds")
                    )
                )
                request_id = cursor.lastrowid

            st.success(
                f"Request saved locally. Reference: CC-{request_id:05d}"
            )
            st.info(
                "The request has not been sent to the college. "
                "Contact the college directly to confirm your visit."
            )


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div style="text-align:center;color:#9baaca;padding:16px">
    <b>CampusCompass</b> · Discover your next campus.<br>
    <small>
        Verify fees, admissions, placements and campus visit arrangements
        with official institutions.
    </small>
</div>
""", unsafe_allow_html=True)