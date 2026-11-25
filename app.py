from flask import Flask, render_template, redirect, url_for, send_from_directory
import json
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Published research (shown on /research). Add new reports here.
#    Each report needs its PDF in static/reports/ and a cover in static/v2/covers/ (see gen_thumbs.py).
with open(os.path.join(BASE_DIR, "data", "reports.json"), encoding="utf-8") as f:
    REPORTS = json.load(f)

# ── Site settings. Edit these in one place.
SITE = {
    "contact_email": "contact@vantedgeorg.com",
    "tally_form_id": "Yj4KK0",        # "Get in touch" Tally form: the code after tally.so/r/
    "waitlist_tally_id": "EqxrRB",    # Tally form on /waitlist ("Join the waitlist" + "Interested to join?")
    "booking_url": "https://calendly.com/contact-vantedgeorg/30min",  # "Book a free call"
    "book_tally_id": "9N7bjp",              # Tally form on /book ("Book a call"), the code after tally.so/r/
}

DIVISION_LABELS = {"ma": "M&A", "dcm": "DCM", "markets": "Global Markets", "equity": "Equity Research"}
TYPE_LABELS = {"deal": "Deal analysis", "newsletter": "Newsletter", "sector": "Sector report",
               "capital": "Capital markets", "deepdive": "Deep dive"}


def page(template, **ctx):
    """Render a page with the shared layout values (templates/layout.html)."""
    return render_template(
        template,
        S=url_for("static", filename="v2/"),
        contact_email=SITE["contact_email"],
        tally_form_id=SITE["tally_form_id"],
        waitlist_url=url_for("waitlist"),
        waitlist_tally_id=SITE["waitlist_tally_id"],
        booking_url=SITE["booking_url"],
        book_tally_id=SITE["book_tally_id"],
        home=url_for("home"),
        research_url=url_for("research"),
        partners_url=url_for("partnerships"),
        faq_url=url_for("faq"),
        book_url=url_for("book"),
        **ctx,
    )


@app.route("/")
def home():
    """Homepage — built from the Vantedge Website Figma file (hero photo replaced by static/hero.mp4)."""
    return page("home.html")


@app.route("/research")
def research():
    """Research page — built from the Figma file; cards come from data/reports.json."""
    filters = [d for d in ("ma", "dcm", "markets") if any(r["division"] == d for r in REPORTS)]
    return page("research.html", reports=REPORTS, filters=filters,
                division_labels=DIVISION_LABELS, type_labels=TYPE_LABELS)


@app.route("/partnerships")
def partnerships():
    """Partnerships page — partner university chapters (moved off the homepage)."""
    return page("partnerships.html")


@app.route("/faq")
def faq():
    """FAQ page — questions from firms and candidates."""
    return page("faq.html")


@app.route("/book")
def book():
    """Book a call — landing page for firms, with the Calendly calendar embedded."""
    return page("book.html")


@app.route("/waitlist")
def waitlist():
    """Waitlist page — Tally form styled like the homepage 'Get in touch' card."""
    return page("waitlist.html")


@app.route("/portal")
def portal():
    return render_template("portal.html")


@app.route("/favicon.ico")
def favicon():
    """Browsers and Google look for /favicon.ico at the site root."""
    return send_from_directory(os.path.join(BASE_DIR, "static"), "favicon.ico", mimetype="image/x-icon")


# ── Old pages from the previous site: send visitors to the matching place on the new site
OLD_URLS = {
    "/about": "/#about", "/our-story": "/#about",
    "/contact": "/#contact", "/thankyou": "/#contact",
    "/team": "/#advisor",
    "/apply": "/waitlist", "/careers": "/waitlist",
    "/for-firms": "/#start",
    "/preview": "/", "/preview/research": "/research",
}


@app.route("/about")
@app.route("/our-story")
@app.route("/contact")
@app.route("/thankyou")
@app.route("/team")
@app.route("/apply")
@app.route("/careers")
@app.route("/for-firms")
@app.route("/preview")
@app.route("/preview/research")
def old_page():
    from flask import request
    return redirect(OLD_URLS[request.path], code=301)


@app.route("/team/<path:_member>")
def old_team_member(_member):
    return redirect("/#advisor", code=301)


@app.route("/divisions/<path:_division>")
def old_division(_division):
    return redirect("/research", code=301)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
