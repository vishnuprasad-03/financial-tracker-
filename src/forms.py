"""
WTForms for Finance Tracker.
"""

from flask_wtf import FlaskForm

from wtforms import (
    FloatField,
    StringField,
    DateField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    NumberRange
)


class TransactionForm(FlaskForm):
    """
    Transaction form.
    """

    amount = FloatField(
        "Amount",
        validators=[
            DataRequired(),
            NumberRange(
                min=0.01,
                message="Amount must be greater than zero."
            )
        ]
    )

    category = StringField(
        "Category",
        validators=[
            DataRequired(
                message="Category cannot be empty."
            )
        ]
    )

    transaction_type = SelectField(
        "Type",
        choices=[
            ("income", "Income"),
            ("expense", "Expense")
        ],
        validators=[
            DataRequired()
        ]
    )

    date = DateField(
        "Date",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Add Transaction"
    )