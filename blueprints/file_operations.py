"""
CSV import and export routes for Finance Tracker.
"""

"""
CSV import and export routes for Finance Tracker.
"""

import csv
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    Response
)

from flask_login import login_required
from werkzeug.utils import secure_filename

from src.database import SessionLocal
from src.db_models import TransactionDB
import csv
import io

file_operations_bp = Blueprint(
    "file_operations",
    __name__
)


ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    """
    Check whether the uploaded file has an allowed extension.
    """

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@file_operations_bp.route(
    "/import",
    methods=["GET", "POST"]
)
@login_required
def import_transactions():
    """
    Upload a CSV file and preview the first 5 rows.
    """

    if request.method == "GET":
        return render_template("import.html")

    # Check whether a file was included in the request
    if "file" not in request.files:
        flash("No file selected.", "error")

        return redirect(
            url_for("file_operations.import_transactions")
        )

    file = request.files["file"]

    # Check whether the filename is empty
    if file.filename == "":
        flash("Please select a CSV file.", "error")

        return redirect(
            url_for("file_operations.import_transactions")
        )

    # Allow only CSV files
    if not allowed_file(file.filename):
        flash("Only CSV files are allowed.", "error")

        return redirect(
            url_for("file_operations.import_transactions")
        )

    # Make the filename safe
    filename = secure_filename(file.filename)

    try:
        # Read the uploaded CSV file
        file_content = file.stream.read().decode("utf-8")

        csv_reader = csv.DictReader(
            io.StringIO(file_content)
        )

        rows = list(csv_reader)

        if not rows:
            flash("The CSV file is empty.", "error")

            return redirect(
                url_for("file_operations.import_transactions")
            )

        # Store all CSV rows temporarily for confirmation
        session["pending_import"] = rows

        # Preview only the first 5 rows
        preview_rows = rows[:5]

        return render_template(
        "import_preview.html",
        filename=filename,
        preview_rows=preview_rows,
        total_rows=len(rows)
)

    except Exception:
        flash(
            "Unable to read the CSV file. Please check its format.",
            "error"
        )

        return redirect(
            url_for("file_operations.import_transactions")
        )
    

@file_operations_bp.route(
    "/confirm-import",
    methods=["POST"]
)
@login_required
def confirm_import():
    """
    Confirm and import pending CSV transactions into the database.
    """

    rows = session.get("pending_import")

    if not rows:
        flash(
            "No pending CSV import found. Please upload the file again.",
            "error"
        )

        return redirect(
            url_for("file_operations.import_transactions")
        )

    db_session = SessionLocal()

    imported_count = 0
    skipped_count = 0

    try:
        for row in rows:

            try:
                amount = float(row["amount"])

                category = row["category"].strip().title()

                transaction_type = (
                    row["transaction_type"]
                    .strip()
                    .lower()
                )

                transaction_date = datetime.strptime(
                    row["date"].strip(),
                    "%Y-%m-%d"
                ).date()

                # Validate amount
                if amount <= 0:
                    skipped_count += 1
                    continue

                # Validate category
                if not category:
                    skipped_count += 1
                    continue

                # Validate transaction type
                if transaction_type not in (
                    "income",
                    "expense"
                ):
                    skipped_count += 1
                    continue

                transaction = TransactionDB(
                    amount=amount,
                    category=category,
                    transaction_type=transaction_type,
                    date=transaction_date
                )

                db_session.add(transaction)

                imported_count += 1

            except (
                ValueError,
                KeyError,
                TypeError
            ):
                skipped_count += 1
                continue

        db_session.commit()

        # Remove temporary CSV data after successful import
        session.pop("pending_import", None)

        flash(
            f"{imported_count} transactions imported successfully. "
            f"{skipped_count} invalid rows skipped.",
            "success"
        )

    except Exception:

        db_session.rollback()

        flash(
            "An error occurred while importing transactions.",
            "error"
        )

    finally:
        db_session.close()

    return redirect(
        url_for("transactions.transactions")
    )

@file_operations_bp.route("/export")
@login_required
def export_transactions():
    """
    Export all transactions from the database as a CSV file.
    """

    db_session = SessionLocal()

    try:
        transactions = db_session.query(
            TransactionDB
        ).all()

        output = io.StringIO()

        writer = csv.writer(output)

        # Write CSV header
        writer.writerow([
            "id",
            "amount",
            "category",
            "transaction_type",
            "date"
        ])

        # Write transaction rows
        for transaction in transactions:
            writer.writerow([
                transaction.id,
                transaction.amount,
                transaction.category,
                transaction.transaction_type,
                transaction.date if transaction.date else ""
            ])

        csv_data = output.getvalue()

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={
                "Content-Disposition":
                    "attachment; filename=transactions_export.csv"
            }
        )

    finally:
        db_session.close()

@file_operations_bp.route("/export-pdf")
@login_required
def export_pdf():
    """
    Generate and download a basic PDF financial report.
    """

    db_session = SessionLocal()

    try:
        transactions = db_session.query(
            TransactionDB
        ).all()

        # Calculate dashboard totals
        total_income = sum(
            transaction.amount
            for transaction in transactions
            if transaction.transaction_type == "income"
        )

        total_expense = sum(
            transaction.amount
            for transaction in transactions
            if transaction.transaction_type == "expense"
        )

        balance = total_income - total_expense

        # Create PDF in memory
        pdf_buffer = io.BytesIO()

        document = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        elements = []

        # Report title
        elements.append(
            Paragraph(
                "Finance Tracker Report",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        # Summary section
        elements.append(
            Paragraph(
                f"Total Income: INR {total_income:.2f}",
                styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                f"Total Expense: INR {total_expense:.2f}",
                styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                f"Balance: INR {balance:.2f}",
                styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                f"Total Transactions: {len(transactions)}",
                styles["Heading3"]
            )
        )

        elements.append(Spacer(1, 25))

        # Transaction table header
        table_data = [
            [
                "ID",
                "Date",
                "Category",
                "Type",
                "Amount"
            ]
        ]

        # Add transaction rows
        for transaction in transactions:

            transaction_date = (
                transaction.date.strftime("%Y-%m-%d")
                if transaction.date
                else "N/A"
            )

            table_data.append([
                str(transaction.id),
                transaction_date,
                transaction.category,
                transaction.transaction_type.title(),
                f"INR {transaction.amount:.2f}"
            ])

        transaction_table = Table(
            table_data,
            repeatRows=1
        )

        transaction_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, 0),
                    8
                )
            ])
        )

        elements.append(transaction_table)

        # Build PDF
        document.build(elements)

        pdf_buffer.seek(0)

        return Response(
            pdf_buffer.getvalue(),
            mimetype="application/pdf",
            headers={
                "Content-Disposition":
                    "attachment; filename=finance_report.pdf"
            }
        )

    finally:
        db_session.close()